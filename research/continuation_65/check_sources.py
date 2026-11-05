"""Verify retained photo, resource accounting and scope; not a new reading."""
import hashlib,json
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[2]
def read(p):return json.loads((ROOT/p).read_text())
def main():
 p=read('research/continuation_65/protocol.json')['acquisition'];r=read('research/continuation_65/results.json');receipt=read('research/continuation_65/download_receipt.json'); c=read('research/continuation_65/captures.json')['captures'][0]
 raw=(ROOT/p['manifest']).read_bytes();assert hashlib.sha256(raw).hexdigest()==p['manifest_sha256']; m=json.loads(raw);b=m['items'][0]['items'][0]['items'][0]['body'];assert b['id']==p['url']==c['url']==receipt['url']
 assert m['items'][0]['id']==c['canvas_id'] and receipt['saved'] and not receipt['retry']
 path=ROOT/c['path'];assert hashlib.sha256(path.read_bytes()).hexdigest()==c['sha256']==receipt['sha256']
 assert path.stat().st_size==c['bytes']==receipt['bytes_received']==r['new_download_bytes']==313747
 with Image.open(path) as im: assert im.size==(p['width'],p['height'])==(c['width'],c['height'])
 annotations=read('research/continuation_65/observations.json')['annotations'];assert [a['id'] for a in annotations]==r['source_regions']
 for a in annotations:
  assert a['target']['source']==c['path'] and a['sha256']==c['sha256']
  x,y,w,h=map(int,a['target']['selector']['value'][5:].split(','));assert 0<=x<x+w<=c['width'] and 0<=y<y+h<=c['height']
 graph=read('data/knowledge.v1.json'); assert {a['id'] for a in annotations}<={e['annotation_id'] for e in graph['evidence']}
 entity=next(e for e in graph['entities'] if e['id']=='image:'+c['path']);old=next(e for e in graph['entities'] if e['id']=='image:data/images/mpo-8201.jpg');assert entity['capture']==old['capture']
 claim=next(e for e in graph['claims'] if e['id']=='interpretation:E65-8201-ending');assert claim['status']=='unresolved' and not claim['physical_adjacency_proved']
 for key in ['fr20106_image_inspected','vienna_image_inspected','exact_melody_verified','physical_adjacency_proved','published_rejection_overturned','historical_same_codex_proved','new_historical_discovery','independent_confirmation']:assert not r[key]
 states={l['id']:l['decision_state'] for l in read('data/lead_register.v1.json')['leads']};assert states==read('research/continuation_65/decisions.before.json')['states']
 audit=read('data/resource_audit.json');assert audit['working_source_capture_files']==r['working_source_images_after']==209 and r['conservative_planning_total_after']==1676174588 and audit['conservative_planning_total_bytes']==r['conservative_planning_total_after']+audit['receipt_subtotals']['research/continuation_88/supplement_receipt.json']+audit['receipt_subtotals']['research/continuation_114/download_receipt.json']
 private=ROOT/'research/scholarship/grajewski2022.pdf'
 if private.exists():assert hashlib.sha256(private.read_bytes()).hexdigest()==read('research/continuation_65/sources.json')['grajewski']['sha256']
 print(json.dumps({'source_images':1,'new_physical_objects':0,'source_bytes':c['bytes'],'resource_files':209,'decisions':'unchanged','fr20106_inspected':False,'source_reading_independently_verified':False}))
if __name__=='__main__':main()
