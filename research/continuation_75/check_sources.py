"""Check image provenance and qualification; do not certify Latin readings."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def read(path):
    return json.loads((ROOT / path).read_text())

def main():
    result = read('research/continuation_75/results.json')
    annotations = read('research/continuation_75/observations.json')['annotations']
    assert {a['id'] for a in annotations} == set(result['source_regions'])
    for annotation in annotations:
        path = annotation['target']['source']
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == annotation['sha256']
        x, y, w, h = map(int, annotation['target']['selector']['value'].removeprefix('xywh=').split(','))
        width, height = annotation['image_dimensions']
        assert min(x, y) >= 0 and min(w, h) > 0 and x + w <= width and y + h <= height
        assert not annotation['independent_confirmation']
    for key in ('same_ink_verified', 'recto_verso_verified', 'immediate_physical_adjacency_verified',
                'external_source_image_inspected', 'new_codex_relationship', 'new_discovery', 'independent_confirmation'):
        assert not result[key]
    assert result['new_source_images'] == result['new_download_bytes'] == 0
    states = {x['id']: x['decision_state'] for x in read('data/lead_register.v1.json')['leads']}
    assert states == read('research/continuation_69/decisions.before.json')['states']
    graph = read('data/knowledge.v1.json')
    claim = next(c for c in graph['claims'] if c['id'] == 'interpretation:E75-8073-responsory-context')
    assert claim['status'] == 'unresolved' and not claim['same_ink_verified'] and not claim['independent_confirmation']
    assert all(next(e for e in graph['evidence'] if e['id'] == 'evidence:' + ident)['image'] for ident in result['source_regions'])
    print(json.dumps({'image_hashes_and_regions_valid': True, 'text_reading_independently_verified': False,
                      'physical_overlap_established': False, 'decisions_unchanged': True}))

if __name__ == '__main__':
    main()
