"""One bounded request for the manifest's exact public painting URL; never retry."""
import hashlib,io,json
from pathlib import Path
from urllib.error import HTTPError,URLError
from urllib.request import urlopen
from PIL import Image

ROOT=Path(__file__).resolve().parents[2]; HERE=Path(__file__).resolve().parent
p=json.loads((HERE/'protocol.json').read_text())['acquisition']; receipt_path=HERE/'download_receipt.json'
if receipt_path.exists():
    raise SystemExit('Receipt exists; no repeat request.')
raw=(ROOT/p['manifest']).read_bytes(); assert hashlib.sha256(raw).hexdigest()==p['manifest_sha256']
m=json.loads(raw); b=m['items'][0]['items'][0]['items'][0]['body']; assert b['id']==p['url']
assert m['items'][0]['id']==p['canvas_id']
assert any(p['rights'] in v.get('value',{}).get('none',[]) for v in m['metadata'])
r={'url':p['url'],'saved':False,'bytes_received':0,'retry':False}
try:
    with urlopen(p['url'],timeout=35) as response:
        content=response.read(p['max_bytes']+1)
        r.update(status=response.status,final_url=response.url,content_type=response.headers.get('Content-Type'),bytes_received=len(content))
    assert len(content)<=p['max_bytes']
    im=Image.open(io.BytesIO(content));im.load();assert im.format=='JPEG' and im.size==(p['width'],p['height'])
    (ROOT/p['path']).write_bytes(content)
    r.update(saved=True,path=p['path'],sha256=hashlib.sha256(content).hexdigest(),width=im.width,height=im.height)
except (HTTPError,URLError,TimeoutError,OSError,AssertionError,ValueError) as e:
    r.update(error=str(e),status=getattr(e,'code',None))
receipt_path.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
