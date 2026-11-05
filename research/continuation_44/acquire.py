"""Acquire only exact painting-image URLs in two already retained manifests."""
import hashlib
import io
import json
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import urlopen
from PIL import Image

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
MAX_BYTES=8_000_000


def save(path,value):
    path.write_text(json.dumps(value,indent=2)+'\n')


def main():
    receipt_path=HERE/'download_receipts.json'
    receipts=json.loads(receipt_path.read_text()) if receipt_path.exists() else []
    captures_path=HERE/'captures.json'
    doc=json.loads(captures_path.read_text()) if captures_path.exists() else {'version':'1.0.0','date':'2026-10-29','captures':[]}
    (HERE/'images').mkdir(exist_ok=True)
    for ident in ['8066','9620']:
        path=f'data/manifests/{ident}.json'
        manifest=json.loads((ROOT/path).read_text())
        rights=next(r['value']['none'][0] for r in manifest['metadata'] if 'Rights' in r['label'].get('en',[]))
        assert rights=='http://creativecommons.org/publicdomain/mark/1.0/'
        for ordinal,canvas in enumerate(manifest['items'],1):
            body=canvas['items'][0]['items'][0]['body'];url=body['id']
            # A completed success or failure is never automatically retried.
            if any(r['url']==url for r in receipts):
                continue
            record={'url':url,'manifest':path,'manifest_sha256':hashlib.sha256((ROOT/path).read_bytes()).hexdigest(),
                'locator':f'items/{ordinal-1}/items/0/items/0/body/id','date':'2026-10-29',
                'saved':False,'bytes_received':0,'source_capture':ordinal}
            try:
                with urlopen(url,timeout=45) as response:
                    content=response.read(MAX_BYTES+1)
                    record.update(status=response.status,content_type=response.headers.get('Content-Type'),
                        final_url=response.url,bytes_received=len(content))
                assert len(content)<=MAX_BYTES,'Declared per-image transfer cap exceeded'
                image=Image.open(io.BytesIO(content));image.load()
                assert image.format=='JPEG'
                assert image.size==(body['width'],body['height'])
                target=HERE/'images'/f'Fr{ident}-capture-{ordinal}-native.jpg'
                target.write_bytes(content)
                record.update(saved=True,path=str(target.relative_to(ROOT)),sha256=hashlib.sha256(content).hexdigest(),
                    width=image.width,height=image.height,rights_url=rights)
                doc['captures'].append({'physical_object_id':'mpo-'+ident,'path':record['path'],
                    'url':url,'sha256':record['sha256'],'width':image.width,'height':image.height,
                    'bytes':len(content),'canvas_id':canvas['id'],'capture_index':ordinal-1,
                    'manifest':path,'manifest_locator':record['locator'],'rights_url':rights,
                    'attribution':'Riksarkivet; National Archives of Sweden',
                    'side_assignment':None,'role':'Additional retained original photograph; not an extra leaf or independent witness'})
            except HTTPError as error:
                record.update(status=error.code,error='HTTP response; no retry or alternate-client access')
            except (URLError,TimeoutError,AssertionError,OSError) as error:
                record.update(error=str(error))
            receipts.append(record);save(receipt_path,receipts);save(captures_path,doc)
            print(json.dumps({k:record.get(k) for k in ['url','status','saved','bytes_received','error']}),flush=True)
            if not record['saved']:
                return


if __name__=='__main__':
    main()
