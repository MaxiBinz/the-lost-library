"""Check source region and uncertainty; not historical or linguistic accuracy."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def read(path):
    return json.loads((ROOT / path).read_text())

def main():
    result = read('research/continuation_78/results.json')
    annotation = read('research/continuation_78/observations.json')['annotations'][0]
    path = annotation['target']['source']
    cap = next(c for c in read('research/continuation_54/captures.json')['captures'] if c['path'] == path)
    assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == annotation['sha256'] == cap['sha256']
    x, y, w, h = map(int, annotation['target']['selector']['value'].removeprefix('xywh=').split(','))
    width, height = annotation['image_dimensions']
    assert min(x, y) >= 0 and min(w, h) > 0 and x+w <= width and y+h <= height
    for key in ('008036_locally_confirmed', 'original_comparators_inspected', '10437_full_antiphon_omission_proven',
                'exact_complete_sequence_matched', 'physical_side_map_verified', 'historical_book_relationship_established',
                'independent_confirmation', 'new_discovery'):
        assert not result[key]
    assert result['new_source_images'] == result['new_download_bytes'] == 0
    states = {x['id']: x['decision_state'] for x in read('data/lead_register.v1.json')['leads']}
    assert states == read('research/continuation_69/decisions.before.json')['states']
    graph = read('data/knowledge.v1.json')
    claim = next(c for c in graph['claims'] if c['id'] == 'interpretation:E78-10437-verse')
    assert claim['status'] == 'unresolved' and not claim['full_antiphon_omission_proven'] and not claim['independent_confirmation']
    previous = next(c for c in graph['claims'] if c['id'] == 'interpretation:E77-dedication-order-comparison')
    assert previous['later_qualification'] == result['consequence']
    print(json.dumps({'image_hash_and_region_valid': True, 'reading_independently_verified': False,
                      'omission_established': False, 'decisions_unchanged': True}))

if __name__ == '__main__':
    main()
