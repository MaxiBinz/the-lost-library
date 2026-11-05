"""One-shot bounded public metadata GET; no authentication, file or image fetches."""
import hashlib
import json
import sys
from pathlib import Path
from urllib.error import HTTPError,URLError
from urllib.parse import urlsplit
from urllib.request import urlopen

HERE=Path(__file__).resolve().parent


def save(path,value):
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')


def main():
    protocol=json.loads((HERE/'protocol.json').read_text())
    ledger_path=HERE/'metadata_receipts.json'
    receipts=json.loads(ledger_path.read_text()) if ledger_path.exists() else []
    url=protocol['initial_metadata_url']
    label='records-query'
    if len(sys.argv)>1:
        assert len(sys.argv)==3
        label,url=sys.argv[1:]
        assert label.replace('-','').isalnum()
        # A follow-up must be an exact public metadata API link in an already
        # retained response; callers cannot invent IDs or mirror endpoints.
        candidates=[]
        for receipt in receipts:
            if not receipt.get('saved'):
                continue
            source=json.loads((HERE/receipt['file']).read_text())
            records=source.get('hits',{}).get('hits',[]) if isinstance(source.get('hits'),dict) else [source]
            for record in records:
                candidates.extend(v for v in record.get('links',{}).values() if isinstance(v,str))
        assert url in candidates,'Follow-up not present in a retained source link'
    parsed=urlsplit(url)
    assert parsed.scheme=='https' and parsed.netloc=='zenodo.org'
    assert parsed.path.startswith('/api/records') and not parsed.username and not parsed.password
    assert not any(r['url']==url for r in receipts),'Completed success/failure URL is never retried'
    assert len(receipts)<protocol['bounds']['maximum_requests']
    remaining=protocol['bounds']['maximum_total_metadata_bytes']-sum(r['bytes_received'] for r in receipts)
    maximum=min(remaining,protocol['bounds']['maximum_bytes_per_response'])
    assert maximum>0
    receipt={'date':'2026-10-30','url':url,'saved':False,'bytes_received':0,'retry':False}
    try:
        with urlopen(url,timeout=30) as response:
            raw=response.read(maximum+1)
            receipt.update(status=response.status,final_url=response.url,
                content_type=response.headers.get('Content-Type'),bytes_received=len(raw))
        assert len(raw)<=maximum,'Bounded metadata response exceeded cap'
        data=json.loads(raw)
        assert isinstance(data,dict)
        filename=label+'.json';(HERE/filename).write_bytes(raw)
        receipt.update(saved=True,file=filename,sha256=hashlib.sha256(raw).hexdigest())
        records=data.get('hits',{}).get('hits',[]) if isinstance(data.get('hits'),dict) else [data]
        print(json.dumps({'record_count':len(records),'records':[{'id':r.get('id'),
            'conceptrecid':r.get('conceptrecid'),'doi':r.get('doi'),
            'title':r.get('metadata',{}).get('title'),'version':r.get('metadata',{}).get('version'),
            'created':r.get('created'),'updated':r.get('updated'),
            'versions':r.get('versions'),'links':r.get('links')} for r in records]},ensure_ascii=False,indent=2),flush=True)
    except HTTPError as error:
        receipt.update(status=error.code,error='HTTP response; stopped without retry or alternate access')
    except (URLError,TimeoutError,AssertionError,OSError,ValueError) as error:
        receipt.update(error=str(error))
    receipts.append(receipt);save(ledger_path,receipts)
    print(json.dumps({'saved':receipt['saved'],'status':receipt.get('status'),
        'bytes_received':receipt['bytes_received'],'error':receipt.get('error')}),flush=True)


if __name__=='__main__':
    main()
