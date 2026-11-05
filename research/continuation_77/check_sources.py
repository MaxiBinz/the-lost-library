"""Check retained source bounds and uncertainty; not Latin or history accuracy."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def read(path):
    return json.loads((ROOT / path).read_text())

def main():
    result = read('research/continuation_77/results.json')
    annotations = read('research/continuation_77/observations.json')['annotations']
    captures = {}
    for path in ('research/continuation_44/captures.json', 'research/continuation_54/captures.json'):
        captures.update({c['path']: c for c in read(path)['captures']})
    assert {a['id'] for a in annotations} == set(result['source_regions'])
    for item in annotations:
        path = item['target']['source']
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == item['sha256'] == captures[path]['sha256']
        x, y, w, h = map(int, item['target']['selector']['value'].removeprefix('xywh=').split(','))
        width, height = item['image_dimensions']
        assert min(x, y) >= 0 and min(w, h) > 0 and x + w <= width and y + h <= height
        assert not item['independent_confirmation']
    for key in ('same_service_occurrence_verified', '8066_physical_seam_verified', '10437_full_office_omission_verified',
                'independent_source_review', 'melody_compared', 'different_book_established', 'new_codex_relationship',
                'novelty_cleared', 'new_discovery'):
        assert not result[key]
    assert result['new_source_images'] == result['new_download_bytes'] == 0
    states = {x['id']: x['decision_state'] for x in read('data/lead_register.v1.json')['leads']}
    assert states == read('research/continuation_69/decisions.before.json')['states']
    graph = read('data/knowledge.v1.json')
    claim = next(c for c in graph['claims'] if c['id'] == 'interpretation:E77-dedication-order-comparison')
    assert claim['status'] == 'unresolved' and not claim['same_service_occurrence_verified'] and not claim['independent_confirmation']
    assert set(claim['supports']) == {'evidence:' + i for i in result['source_regions']}
    assert all(next(e for e in graph['evidence'] if e['id'] == ref)['image'] for ref in claim['supports'])
    print(json.dumps({'image_hashes_and_regions_valid': True, 'historical_readings_independently_verified': False,
                      'service_positions_verified': False, 'decisions_unchanged': True}))

if __name__ == '__main__':
    main()
