"""Check recorded regions and declared sensitivity, not musical correctness."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def read(path):
    return json.loads((ROOT / path).read_text())

def main():
    result = read('research/continuation_80/results.json')
    readings = read('research/continuation_80/readings.json')
    comparison = read('research/continuation_80/comparison.json')
    annotations = read('research/continuation_80/observations.json')['annotations']
    assert {a['id'] for a in annotations} == set(result['source_regions'])
    for row, note, calculated in zip(readings['items'], annotations, comparison['items']):
        path = row['path']
        assert path == note['target']['source']
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == row['sha256'] == note['sha256']
        x,y,w,h = map(int, note['target']['selector']['value'].removeprefix('xywh=').split(','))
        width,height = note['image_dimensions']
        assert min(x,y) >= 0 and min(w,h) > 0 and x+w <= width and y+h <= height
        assert all(x <= px < x+w and y <= py < y+h for px,py in row['points'])
        (x1,y1),(x2,y2) = row['points']
        assert abs((y2-y1-row['rule_slope']*(x2-x1))-calculated['nominal_y_down_px']) < .001
        assert not note['independent_confirmation']
    assert [v['direction'] for v in comparison['items'][0]['sensitivity']] == ['lower_on_page']*3
    assert [v['direction'] for v in comparison['items'][1]['sensitivity']] == ['lower_on_page','unresolved','unresolved']
    assert all(v['range_staff_spacings'][0] <= 0 <= v['range_staff_spacings'][1] for v in comparison['between_source_difference_ranges'])
    for key in ('full_melody_collated','equal_interval_proven','absolute_pitches_transcribed','compound_sign_adjudicated',
                'comparator_manuscript_images_inspected','book_relationship_established','independent_confirmation','new_discovery'):
        assert not result[key]
    assert result['new_source_images'] == result['new_download_bytes'] == 0
    states = {r['id']:r['decision_state'] for r in read('data/lead_register.v1.json')['leads']}
    assert states == read('research/continuation_69/decisions.before.json')['states']
    graph = read('data/knowledge.v1.json')
    claim = next(c for c in graph['claims'] if c['id'] == 'interpretation:E80-dedication-domini-notes')
    assert claim['status'] == 'unresolved' and not claim['equal_interval_proven'] and not claim['independent_confirmation']
    assert set(claim['supports']) == {'evidence:'+i for i in result['source_regions']}
    previous = next(c for c in graph['claims'] if c['id'] == 'interpretation:E79-dedication-opening-notes')
    assert previous['later_context'] == result['interpretation']
    print(json.dumps({'source_regions_valid':True,'wide_8066_direction_unresolved':True,
                      'musical_reading_independently_verified':False,'decisions_unchanged':True}))

if __name__ == '__main__':
    main()
