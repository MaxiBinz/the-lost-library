"""Verify source integrity and limited scope, not the historical reading."""
import hashlib,json
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[2]
def read(p):return json.loads((ROOT/p).read_text())
def main():
 p=read('research/continuation_57/protocol.json')
 for path,sha in p['frozen_inputs'].items():assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==sha,path
 snap=p['register_before'];assert hashlib.sha256((ROOT/snap['path']).read_bytes()).hexdigest()==snap['sha256']
 for s in p['sources']:
  assert hashlib.sha256((ROOT/s['path']).read_bytes()).hexdigest()==s['sha256']
  with Image.open(ROOT/s['path']) as im:assert im.size==(s['width'],s['height'])
 annotations=read('research/continuation_57/observations.json')['annotations'];assert len(annotations)==3
 for a in annotations:
  s=next(s for s in p['sources'] if s['path']==a['target']['source']);x,y,w,h=map(int,a['target']['selector']['value'][5:].split(','))
  assert 0<=x<x+w<=s['width'] and 0<=y<y+h<=s['height'] and a['sha256']==s['sha256']
  assert a['rights_url']=='http://creativecommons.org/publicdomain/mark/1.0/' and not a['independent_confirmation']
 before={r['id']:r for r in read(snap['path'])['leads']};live={r['id']:r for r in read('data/lead_register.v1.json')['leads']}
 assert before.keys()==live.keys() and all(before[k]['decision_state']==live[k]['decision_state'] for k in before)
 assert live['fr8311-chant']['decision_state']=='unresolved' and live['fr8311-chant']['test_execution'].startswith('E57')
 result=read('research/continuation_57/results.json');assert result['source_photo_views_inspected']==4 and result['new_source_files']==0
 for k in ['new_discovery','exact_melody_verified','complete_side_map','physical_join_established','new_codex_attribution','independent_confirmation']:assert not result[k]
 evidence={e['annotation_id'] for e in read('data/knowledge.v1.json')['evidence']};assert set(result['source_regions']+result['prior_regions'])<=evidence
 print(json.dumps({'source_views':4,'new_regions':3,'historical_decisions':'unchanged','new_discovery':False}))
if __name__=='__main__':main()
