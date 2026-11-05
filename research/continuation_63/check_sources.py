"""Check source integrity and limited claims, not art-historical truth."""
import hashlib,json
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[2]
def read(p):return json.loads((ROOT/p).read_text())
def main():
 p=read('research/continuation_63/protocol.json'); r=read('research/continuation_63/results.json')
 receipt=read('research/continuation_63/download_receipt.json'); requested=p['acquisition']
 manifest=(ROOT/requested['manifest']).read_bytes(); assert hashlib.sha256(manifest).hexdigest()==requested['manifest_sha256']
 m=json.loads(manifest); assert m['items'][0]['items'][0]['items'][0]['body']['id']==receipt['url']==requested['url']
 assert not receipt['saved'] and receipt['bytes_received']==0 and not receipt['retry']
 assert not (ROOT/requested['path']).exists()
 annotations=read('research/continuation_63/observations.json')['annotations']
 assert [a['id'] for a in annotations]==r['source_regions']
 for a in annotations:
  path=ROOT/a['target']['source']; assert hashlib.sha256(path.read_bytes()).hexdigest()==a['sha256']
  with Image.open(path) as im: assert list(im.size)==a['image_dimensions']
  x,y,w,h=map(int,a['target']['selector']['value'][5:].split(',')); W,H=a['image_dimensions']
  assert 0<=x<x+w<=W and 0<=y<y+h<=H
 for k in ['same_book_proved','different_book_proved','common_hand_proved','feature_uniqueness_proved','new_historical_discovery','independent_confirmation']:
  assert r[k] is False
 assert r['new_source_images']==r['new_download_bytes']==0
 live={x['id']:x['decision_state'] for x in read('data/lead_register.v1.json')['leads']}
 assert live==read('research/continuation_63/decisions.before.json')['states']
 graph=read('data/knowledge.v1.json'); evidence={e['annotation_id'] for e in graph['evidence']}
 assert set(r['source_regions']+r['reused_control_regions'])<=evidence
 claim=next(c for c in graph['claims'] if c['id']=='observation:E63-selected-D')
 assert claim['predicate']=='stylistic_similarity' and claim['status']=='supported'
 assert all(not claim[k] for k in ['same_book_proved','different_book_proved','feature_uniqueness_proved','independent_confirmation'])
 lead=next(l for l in read('data/lead_register.v1.json')['leads'] if l.get('frozen_hypothesis')=='H04')
 assert lead['decision_state']=='unresolved' and lead['frozen_category']=='C'
 print(json.dumps({'new_regions':len(annotations),'reused_control_regions':len(r['reused_control_regions']),'downloaded_bytes':receipt['bytes_received'],'h04':'unresolved','decisions':'unchanged'}))
if __name__=='__main__':main()
