"""Check provenance and declared scope; not an independent historical reading."""
import hashlib,json
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[2]
def read(p):return json.loads((ROOT/p).read_text())
def main():
    res=read('research/continuation_60/results.json'); anns=read('research/continuation_60/observations.json')['annotations']
    assert len(anns)==2 and [a['id'] for a in anns]==res['source_regions']
    for a in anns:
        p=a['target']['source']; assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==a['sha256']
        with Image.open(ROOT/p) as im: assert list(im.size)==a['image_dimensions']
        x,y,w,h=map(int,a['target']['selector']['value'][5:].split(','));W,H=a['image_dimensions'];assert 0<=x<x+w<=W and 0<=y<y+h<=H
        assert not a['independent_confirmation']
    for k in ['finnish_image_inspected','same_address_verified','physical_identity_rejected','catalogue_error_proved','new_discovery','independent_confirmation']:assert res[k] is False
    assert res['new_source_images']==res['new_download_bytes']==0
    after={x['id']:x['decision_state'] for x in read('data/lead_register.v1.json')['leads']}
    assert after==read('research/continuation_60/decisions.before.json')['states'] and after['iv156-1505']=='unresolved'
    graph=read('data/knowledge.v1.json');ids={e['annotation_id'] for e in graph['evidence']};assert set(res['source_regions']+res['reused_regions'])<=ids
    assert any(c['id']=='interpretation:E60-10370-iv156' and c['status']=='unresolved' for c in graph['claims'])
    for path,sha in graph['frozen_inputs'].items():assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==sha
    print(json.dumps({'new_regions':2,'historical_decisions':'unchanged','finnish_page_inspected':False,'exclusion':False}))
if __name__=='__main__':main()
