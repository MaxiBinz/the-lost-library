"""Check retained-image provenance and scope; this is not a transcription review."""
import hashlib, json
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[2]
def read(p): return json.loads((ROOT/p).read_text())
def main():
    p=read('research/continuation_58/protocol.json')
    src=read('research/continuation_58/review_sources.json')
    anns=read('research/continuation_58/observations.json')['annotations']
    assert len(src)==len(anns)==4 and [s['source'] for s in src]==p['source_paths']
    for s,a in zip(src,anns):
        assert hashlib.sha256((ROOT/s['source']).read_bytes()).hexdigest()==s['sha256']==a['sha256']
        with Image.open(ROOT/s['source']) as im: assert list(im.size)==s['source_size']==a['image_dimensions']
        x,y,x2,y2=s['crop_xyxy'];w,h=s['source_size'];assert 0<=x<x2<=w and 0<=y<y2<=h
        assert a['target']['selector']['value']==f'xywh={x},{y},{x2-x},{y2-y}'
        assert not a['independent_confirmation']
    r=read('research/continuation_58/results.json')
    assert r['regions']==[a['id'] for a in anns]
    for field in ['full_local_sequence_verified','photographic_overlap_demonstrated','original_surface_map_verified','new_discovery','independent_confirmation','new_codex_attribution']: assert r[field] is False
    assert r['new_source_files']==r['new_download_bytes']==0
    graph=read('data/knowledge.v1.json'); ids={e['annotation_id'] for e in graph['evidence']}
    assert set(r['regions'])<=ids
    before={x['id']:x['decision_state'] for x in read('research/continuation_57/lead_register.before.json')['leads']}
    after={x['id']:x['decision_state'] for x in read('data/lead_register.v1.json')['leads']}
    assert before==after and after['fr8311-chant']=='unresolved'
    print(json.dumps({'retained_images':4,'regions':4,'historical_decisions':'unchanged','claim':'no verified overlap or discovery'}))
if __name__=='__main__':main()
