"""Check source hashes and stated arithmetic, not musical or historical truth."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def read(path):
    return json.loads((ROOT / path).read_text())

def main():
    result = read('research/continuation_79/results.json')
    readings = read('research/continuation_79/readings.json')
    comparison = read('research/continuation_79/comparison.json')
    annotations = read('research/continuation_79/observations.json')['annotations']
    assert {a['id'] for a in annotations} == set(result['source_regions'])
    for item, annotation, computed in zip(readings['items'], annotations, comparison['items']):
        path = item['path']
        assert path == annotation['target']['source']
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == item['sha256'] == annotation['sha256']
        x, y, w, h = map(int, annotation['target']['selector']['value'].removeprefix('xywh=').split(','))
        width, height = annotation['image_dimensions']
        assert min(x, y) >= 0 and x+w <= width and y+h <= height
        assert all(x <= px < x+w and y <= py < y+h for px, py in item['xys'])
        (x1,y1), (x2,y2) = item['xys'][1:3]
        expected = y2-y1-item['red_rule_slope_y_per_x']*(x2-x1)
        assert abs(expected-computed['nominal_y_down_px']) < .001
        assert not annotation['independent_confirmation']
    for bounds in comparison['between_source_difference_ranges']:
        assert bounds['range_staff_spacings'][0] <= 0 <= bounds['range_staff_spacings'][1]
        assert not bounds['excludes_zero']
    assert not comparison['between_source_difference_robustly_established']
    for key in ('same_complete_melody_verified','exact_pitch_transcribed','robust_between_source_contrast_established',
                'target_distinctive_variant_confirmed','book_identity_established','different_book_control_verified',
                'comparator_manuscript_images_inspected','novelty_cleared','independent_confirmation','new_discovery'):
        assert not result[key]
    assert result['new_source_images'] == result['new_download_bytes'] == 0
    states = {x['id']: x['decision_state'] for x in read('data/lead_register.v1.json')['leads']}
    assert states == read('research/continuation_69/decisions.before.json')['states']
    graph = read('data/knowledge.v1.json')
    claim = next(c for c in graph['claims'] if c['id'] == 'interpretation:E79-dedication-opening-notes')
    assert claim['status'] == 'unresolved' and not claim['independent_confirmation'] and not claim['robust_between_source_contrast_established']
    assert set(claim['supports']) == {'evidence:' + ident for ident in result['source_regions']}
    print(json.dumps({'source_regions_valid': True, 'intervals_overlap_under_assumptions': True,
                      'notes_independently_verified': False, 'decisions_unchanged': True}))

if __name__ == '__main__':
    main()
