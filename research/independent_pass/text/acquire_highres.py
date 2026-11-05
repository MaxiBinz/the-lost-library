"""Six bounded higher-resolution derivatives; never replace frozen source pixels."""
import hashlib,io,json,sys
from datetime import datetime,timezone
from pathlib import Path
from urllib.request import Request,urlopen
from urllib.parse import urlsplit
from PIL import Image
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT))
from lost_library.pipeline import parse_manifest,permitted_rights,build_database

def sha(data):return hashlib.sha256(data).hexdigest()
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def predictor(r):return [(x['id'],x['normalized'],(x.get('image') or {}).get('sha256')) for x in r]
def main():
 p=ROOT/'data/fragments.json';records=json.loads(p.read_text());before=predictor(records)
 receipt=Path(__file__).with_name('highres_receipts.json');log=json.loads(receipt.read_text()) if receipt.exists() else []
 budget=json.loads((ROOT/'data/resource_audit.json').read_text())
 assert budget['conservative_planning_total_bytes']+27_000_000+30_000_000<3_000_000_000
 downloads_path=ROOT/'data/downloads.json';downloads=json.loads(downloads_path.read_text())
 for ident in ('20274','10370'):
  record=next(r for r in records if r['id']=='mpo-'+ident)
  manifest=json.loads((ROOT/f'data/manifests/{ident}.json').read_text())
  canvases=manifest.get('items') or manifest['sequences'][0]['canvases']
  for index in ((0,1) if ident=='20274' else (0,1,2,3)):
   if any(r['id']==ident and r['capture_index']==index for r in log):continue
   assert len(list((ROOT/'data/images').glob('*.jpg')))<300
   subset=dict(manifest)
   if manifest.get('items'):subset['items']=[canvases[index]]
   else:subset['sequences']=[dict(manifest['sequences'][0],canvases=[canvases[index]])]
   info=parse_manifest(subset);assert permitted_rights(info['rights'])
   width=min(2000,int(info.get('native_width') or 2000))
   url=info['service'].rstrip('/')+f'/full/{width},/0/default.jpg'
   assert urlsplit(url).hostname=='lbiiif.riksarkivet.se' and urlsplit(url).scheme=='https'
   name=f'data/images/mpo-{ident}-capture-{index+1}-{width}px.jpg';dest=ROOT/name
   assert not dest.exists(), 'Do not silently overwrite source bytes'
   item={'id':ident,'capture_index':index,'url':url,'destination':name,'requested_at_utc':datetime.now(timezone.utc).isoformat(),'purpose':'Target reading/side-mark test; higher resolution of existing photograph, not another leaf','bytes_received':0};data=b''
   try:
    with urlopen(Request(url,headers={'User-Agent':'LostLibraryResearch/0.1 bounded source comparison'}),timeout=30) as response:
     data=response.read(5_000_001);item.update(status=response.status,content_type=response.headers.get('Content-Type'),final_url=response.url)
    assert len(data)<=5_000_000,'Per-image5MB cap exceeded'
    with Image.open(io.BytesIO(data)) as image:w,h=image.size;image.verify()
    dest.write_bytes(data)
    cap={'path':name,'url':url,'sha256':sha(data),'width':w,'height':h,'bytes':len(data),'canvas_id':info['canvas_id'],'physical_object_id':record.get('physical_object_id',record['id']),'capture_index':index,'resolution_variant':True,'label':f'Manifest image{index+1}, {width}px derivative (same photograph; not a new side)','rights_url':info['rights']}
    if not record.get('captures'):record['captures']=[{'path':record['image_path'],**record['image'],'physical_object_id':record.get('physical_object_id',record['id']),'capture_index':0}]
    record['captures'].append(cap);item.update(saved=True,sha256=sha(data),capture=cap)
    dump(p,records)
   except Exception as error:item.update(saved=False,error=str(error),status=getattr(error,'code',item.get('status')))
   item['bytes_received']=len(data);log.append(item);downloads.append(item);dump(receipt,log);dump(downloads_path,downloads)
   print(ident,index,item['saved'],item.get('bytes_received'),item.get('error',''),flush=True)
 assert predictor(records)==before,'Frozen predictor inputs changed'
 build_database(ROOT,records)
 summary_path=ROOT/'data/ingestion_summary.json';s=json.loads(summary_path.read_text());images=list((ROOT/'data/images').glob('*.jpg'));s.update(source_image_files=len(images),stored_image_bytes=sum(x.stat().st_size for x in images),new_download_bytes=sum(x.get('bytes_received',0) for x in downloads));dump(summary_path,s)
if __name__=='__main__':main()
