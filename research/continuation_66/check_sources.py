"""Check region integrity and research boundaries, not the Latin or cited editions."""
import hashlib,json
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[2]
def read(p):return json.loads((ROOT/p).read_text())
def main():
 r=read('research/continuation_66/results.json'); s=read('research/continuation_66/sources.json'); ann=read('research/continuation_66/observations.json')['annotations'][0]
 path=ROOT/ann['target']['source'];assert hashlib.sha256(path.read_bytes()).hexdigest()==ann['sha256']
 with Image.open(path) as im:assert list(im.size)==ann['image_dimensions']
 x,y,w,h=map(int,ann['target']['selector']['value'][5:].split(','));W,H=ann['image_dimensions'];assert 0<=x<x+w<=W and 0<=y<y+h<=H
 assert ann['id'] in r['source_regions'] and 'vaga' in ann['literal_candidate']
 graph=read('data/knowledge.v1.json');assert set(r['source_regions']+r['reused_regions'])<={e['annotation_id'] for e in graph['evidence']}
 claim=next(c for c in graph['claims'] if c['id']=='interpretation:E66-8201-nobilis');assert claim['status']=='unresolved' and not claim['historical_same_codex_proved'] and not claim['external_originals_inspected']
 for k in ['fr20106_image_inspected','museum_manuscript_image_inspected','hungarian_manuscript_inspected','musical_match_verified','historical_same_codex_proved','new_historical_discovery','independent_confirmation']:assert not r[k]
 assert r['new_source_images']==r['new_download_bytes']==0
 states={x['id']:x['decision_state'] for x in read('data/lead_register.v1.json')['leads']};assert states==read('research/continuation_66/decisions.before.json')['states']
 assert 'inadvertently requested twice' in s['failed_routes'][-1]['outcome']
 assert read('data/resource_audit.json')['working_source_capture_files']==209
 print(json.dumps({'source_regions':1,'reused_regions':2,'originals_inspected':False,'new_discovery':False,'decisions':'unchanged','repeated_screenshot_disclosed':True}))
if __name__=='__main__':main()
