"""Bounded, single-attempt acquisition of exact cached-manifest painting URLs."""
import hashlib
import io
import json
from pathlib import Path
from urllib.error import HTTPError,URLError
from urllib.request import urlopen

from PIL import Image

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]


def save(path,value):
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')


def main():
    protocol=json.loads((HERE/'primary_protocol.json').read_text())
    receipt_path=HERE/'download_receipts.json'
    receipts=json.loads(receipt_path.read_text()) if receipt_path.exists() else []
    capture_path=HERE/'captures.json'
    doc=json.loads(capture_path.read_text()) if capture_path.exists() else {'version':'1.0.0','date':'2026-10-30','captures':[]}
    (HERE/'images').mkdir(exist_ok=True)
    limit=protocol['acquisition_bounds']['maximum_total_bytes']
    for requested in protocol['requested_sources']:
        url=requested['url']
        if any(r['url']==url for r in receipts):
            continue
        remaining=limit-sum(r['bytes_received'] for r in receipts)
        assert remaining>0,'Aggregate transfer cap reached'
        mp=ROOT/requested['manifest']
        assert hashlib.sha256(mp.read_bytes()).hexdigest()==requested['manifest_sha256']
        manifest=json.loads(mp.read_text())
        body=manifest
        for key in requested['manifest_locator'].split('/')[:-1]:
            body=body[int(key)] if isinstance(body,list) else body[key]
        assert body['id']==url
        rights=next(r['value']['none'][0] for r in manifest['metadata'] if 'Rights' in r['label'].get('en',[]))
        assert rights==requested['rights_url']=='http://creativecommons.org/publicdomain/mark/1.0/'
        receipt={'date':'2026-10-30','url':url,'manifest':requested['manifest'],
            'manifest_sha256':requested['manifest_sha256'],'locator':requested['manifest_locator'],
            'saved':False,'bytes_received':0,'retry':False}
        try:
            maximum=min(8_000_000,remaining)
            with urlopen(url,timeout=35) as response:
                content=response.read(maximum+1)
                receipt.update(status=response.status,content_type=response.headers.get('Content-Type'),
                    final_url=response.url,bytes_received=len(content))
            assert len(content)<=maximum,'Declared transfer cap exceeded'
            im=Image.open(io.BytesIO(content));im.load()
            assert im.format=='JPEG' and im.size==(body['width'],body['height'])
            target=ROOT/requested['path'];target.write_bytes(content)
            receipt.update(saved=True,path=requested['path'],sha256=hashlib.sha256(content).hexdigest(),
                width=im.width,height=im.height,rights_url=rights)
            doc['captures'].append({'physical_object_id':requested['physical_object_id'],
                'path':receipt['path'],'url':url,'sha256':receipt['sha256'],
                'width':im.width,'height':im.height,'bytes':len(content),
                'canvas_id':requested['canvas_id'],'capture_index':requested['capture_index']-1,
                'manifest':requested['manifest'],'manifest_locator':requested['manifest_locator'],
                'rights_url':rights,'rights_scope':'PDM in manifest metadata Rights; top-level rights absent',
                'attribution':'Riksarkivet; National Archives of Sweden',
                'side_assignment':None,'role':'Additional photograph of an existing object; not a new physical fragment or independent witness'})
        except HTTPError as error:
            receipt.update(status=error.code,error='HTTP response; stopped without retry or alternate route')
        except (URLError,TimeoutError,AssertionError,OSError) as error:
            receipt.update(error=str(error))
        receipts.append(receipt);save(receipt_path,receipts);save(capture_path,doc)
        print(json.dumps({k:receipt.get(k) for k in ['url','status','saved','bytes_received','error']}),flush=True)
        if not receipt['saved']:
            return
    assert len(doc['captures'])<=protocol['acquisition_bounds']['maximum_files']


if __name__=='__main__':
    main()
