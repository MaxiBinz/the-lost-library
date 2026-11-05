"""Check local source and research-state integrity, not historical truth."""
from pathlib import Path
import hashlib,json
from PIL import Image
ROOT=Path(__file__).resolve().parents[2]
def read(p):return json.loads((ROOT/p).read_text())
def main():
 r=read('research/continuation_61/results.json'); a=read('research/continuation_61/observations.json')['annotations'][0]
 p=a['target']['source'];assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==a['sha256']
 with Image.open(ROOT/p) as im:assert list(im.size)==a['image_dimensions']
 x,y,w,h=map(int,a['target']['selector']['value'][5:].split(','));W,H=a['image_dimensions'];assert 0<=x<x+w<=W and 0<=y<y+h<=H
 for k in ['reference_source_directly_opened','finnish_image_inspected','complete_final_text_verified','same_book_proved','adjacent_pages_proved','e60_conflict_resolved','new_discovery','independent_confirmation']:assert r[k] is False
 assert r['new_source_images']==r['new_download_bytes']==0
 live={x['id']:x['decision_state'] for x in read('data/lead_register.v1.json')['leads']};assert live==read('research/continuation_61/decisions.before.json')['states']
 graph=read('data/knowledge.v1.json');assert a['id'] in {x['annotation_id'] for x in graph['evidence']}
 assert any(c['id']=='observation:E61-10370-context' and c['status']=='supported' for c in graph['claims'])
 for p,sha in graph['frozen_inputs'].items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==sha
 print(json.dumps({'source_regions':1,'finnish_page_inspected':False,'identity_proved':False,'decisions':'unchanged'}))
if __name__=='__main__':main()
