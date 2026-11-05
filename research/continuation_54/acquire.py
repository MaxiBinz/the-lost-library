"""Single-attempt public GETs of the eight predeclared exact painting URLs."""
import hashlib
import io
import json
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def main():
    p = json.loads((HERE/'protocol.json').read_text())
    ledger = HERE/'download_receipts.json'
    receipts = json.loads(ledger.read_text()) if ledger.exists() else []
    output = HERE/'captures.json'
    doc = json.loads(output.read_text()) if output.exists() else {'version':'1.0.0','date':'2026-10-30','captures':[]}
    (HERE/'images').mkdir(exist_ok=True)
    for request in p['requested_sources']:
        if any(r['url'] == request['url'] for r in receipts):
            continue  # Neither success nor failure is requested a second time.
        assert len(receipts) < p['acquisition_bounds']['maximum_requests']
        raw = (ROOT/request['manifest']).read_bytes()
        assert hashlib.sha256(raw).hexdigest() == request['manifest_sha256']
        m = json.loads(raw)
        value = m
        for key in request['manifest_locator'].split('/'):
            value = value[int(key)] if isinstance(value, list) else value[key]
        assert value == request['url']
        rights = next(v['value']['none'][0] for v in m['metadata'] if 'Rights' in v['label'].get('en', []))
        assert rights == request['rights_url'] == 'http://creativecommons.org/publicdomain/mark/1.0/'
        maximum = min(p['acquisition_bounds']['maximum_bytes_per_response'],
            p['acquisition_bounds']['maximum_total_bytes'] - sum(r['bytes_received'] for r in receipts))
        assert maximum > 0
        receipt = {'date':'2026-10-30', 'url':request['url'], 'saved':False,
                   'bytes_received':0, 'retry':False}
        try:
            with urlopen(request['url'], timeout=p['acquisition_bounds']['timeout_seconds']) as response:
                content = response.read(maximum+1)
                receipt.update(status=response.status, final_url=response.url,
                    content_type=response.headers.get('Content-Type'), bytes_received=len(content))
            assert len(content) <= maximum
            image = Image.open(io.BytesIO(content)); image.load()
            assert image.format == 'JPEG' and image.size == (request['width'], request['height'])
            target = ROOT/request['path']; target.write_bytes(content)
            receipt.update(saved=True, path=request['path'], sha256=hashlib.sha256(content).hexdigest())
            doc['captures'].append({'physical_object_id':request['object_id'], 'path':request['path'],
                'url':request['url'], 'sha256':receipt['sha256'], 'width':image.width, 'height':image.height,
                'bytes':len(content), 'canvas_id':request['canvas_id'],
                'capture_index':request['source_capture_index'], 'manifest':request['manifest'],
                'manifest_locator':request['manifest_locator'], 'rights_url':rights,
                'rights_scope':request['rights_scope'], 'attribution':'Riksarkivet; National Archives of Sweden',
                'side_assignment':None, 'role':'Native photograph of an existing object; no new leaf or independent witness'})
        except HTTPError as error:
            receipt.update(status=error.code, error='HTTP response; stopped without retry or alternate route')
        except (URLError, TimeoutError, AssertionError, OSError, ValueError) as error:
            receipt.update(error=str(error))
        receipts.append(receipt); save(ledger, receipts); save(output, doc)
        print(json.dumps(receipt), flush=True)
        if not receipt['saved']:
            return


if __name__ == '__main__':
    main()
