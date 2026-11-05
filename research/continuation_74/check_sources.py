"""Check image provenance and uncertainty, not Latin reading accuracy."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def read(path):
    return json.loads((ROOT / path).read_text())

def main():
    result = read('research/continuation_74/results.json')
    annotations = read('research/continuation_74/observations.json')['annotations']
    caps = {c['path']:c for c in read('research/continuation_52/captures.json')['captures']}
    assert {a['id'] for a in annotations} == set(result['source_regions'])
    for a in annotations:
        path = a['target']['source']
        assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest() == a['sha256'] == caps[path]['sha256']
        x,y,w,h = map(int,a['target']['selector']['value'].removeprefix('xywh=').split(','))
        width,height = a['image_dimensions']
        assert min(x,y)>=0 and min(w,h)>0 and x+w<=width and y+h<=height
        assert not a['independent_confirmation']
    assert 'car-' in annotations[0]['literal_candidate'] and annotations[1]['literal_candidate'].startswith('nis')
    for key in ('recto_verso_verified','immediate_physical_adjacency_verified','external_source_image_inspected',
                'unique_variant_verified','new_codex_relationship','new_discovery','independent_confirmation'):
        assert not result[key]
    assert result['new_source_images'] == result['new_download_bytes'] == 0
    states={x['id']:x['decision_state'] for x in read('data/lead_register.v1.json')['leads']}
    assert states == read('research/continuation_69/decisions.before.json')['states']
    graph=read('data/knowledge.v1.json')
    claim=next(c for c in graph['claims'] if c['id']=='interpretation:E74-8073-text-boundary')
    assert claim['status']=='unresolved' and not claim['recto_verso_verified'] and not claim['independent_confirmation']
    print(json.dumps({'image_hashes_and_regions_valid':True,'text_reading_independently_verified':False,
                      'side_assignment_established':False,'decisions_unchanged':True}))

if __name__ == '__main__':
    main()
