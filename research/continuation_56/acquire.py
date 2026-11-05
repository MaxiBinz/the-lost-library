"""Bounded single attempts on two exact public museum TIFF download links."""
import hashlib
import json
from pathlib import Path
import time
from urllib.request import urlopen
from urllib.error import HTTPError, URLError

from PIL import Image

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]


def save(path,value):
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')


def main():
    protocol=json.loads((HERE/'protocol.json').read_text())
    bounds=protocol['acquisition_amendment']
    source_doc=json.loads((HERE/'source_files.json').read_text())
    ledger=HERE/'download_receipts.json';out=HERE/'captures.json'
    receipts=json.loads(ledger.read_text()) if ledger.exists() else []
    captures=json.loads(out.read_text()) if out.exists() else {'version':'1.0.0','date':'2026-10-31','captures':[]}
    (HERE/'images').mkdir(exist_ok=True)
    for q in source_doc['sources']:
        if any(r['url']==q['url'] for r in receipts):continue
        assert len(receipts)<bounds['maximum_requests']
        maximum=min(bounds['maximum_image_bytes_per_file'],bounds['maximum_additional_download_bytes']-sum(r['bytes_received'] for r in receipts))
        r=dict(date='2026-10-31',url=q['url'],saved=False,bytes_received=0,retry=False)
        target=ROOT/q['path'];partial=target.with_suffix('.part')
        start=time.monotonic()
        try:
            with urlopen(q['url'],timeout=15) as response:
                r.update(status=response.status,final_url=response.url,content_type=response.headers.get('Content-Type'))
                declared=response.headers.get('Content-Length')
                if declared is not None:assert int(declared)<=maximum,'Advertised response exceeds bound'
                with partial.open('wb') as stream:
                    while True:
                        assert time.monotonic()-start<bounds['timeout_seconds_per_request'],'Overall request deadline exceeded'
                        chunk=response.read(min(1024*1024,maximum+1-r['bytes_received']))
                        if not chunk:break
                        stream.write(chunk);r['bytes_received']+=len(chunk)
                        assert r['bytes_received']<=maximum,'Response exceeds bound'
            with Image.open(partial) as im:
                assert im.format=='TIFF' and im.size==(q['width'],q['height'])
                assert getattr(im,'n_frames',1)==1
                im.load()
                display=im.convert('RGB');display.thumbnail((2200,2200))
                display.save(ROOT/q['display_derivative_path'],'JPEG',quality=95)
            partial.replace(target)
            r.update(saved=True,path=q['path'],sha256=hashlib.sha256(target.read_bytes()).hexdigest())
            for path,role in [(q['path'],'Native museum TIFF'),(q['display_derivative_path'],'Local RGB display JPEG, thumbnail2200, quality95')]:
                with Image.open(ROOT/path) as im:w,h=im.size
                captures['captures'].append(dict(physical_object_id=q['physical_object_id'],source_photo_id=q['source_photo_id'],
                    capture_index=q['source_capture_index'],path=path,url=q['url'],sha256=hashlib.sha256((ROOT/path).read_bytes()).hexdigest(),
                    width=w,height=h,bytes=(ROOT/path).stat().st_size,rights_url=q['rights_url'],attribution=q['attribution'],
                    source_record_url=q['source_record_url'],source_description='research/continuation_56/source_files.json',
                    provenance_locator='sources/'+str(q['source_capture_index']),role=role,
                    derivative_of=q['path'] if path!=q['path'] else None,medieval_side=None))
        except (HTTPError,URLError,TimeoutError,AssertionError,OSError,ValueError) as error:
            r['error']=str(error)+'; stopped without retry or alternate resolution'
            if partial.exists():partial.unlink()
        r['elapsed_seconds']=round(time.monotonic()-start,3)
        receipts.append(r);save(ledger,receipts);save(out,captures)
        print(json.dumps(r),flush=True)


if __name__=='__main__':
    main()
