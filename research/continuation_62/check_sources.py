"""Reproduce the E62 image-availability audit without inferring identity."""
import collections
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def read(path):
    return json.loads((ROOT / path).read_text())


def main():
    records = read('data/fragments.json') + read('data/comparison_sources.v1.json')
    before = read('research/continuation_62/register.before.json')
    after = {lead['id']: lead for lead in read('data/lead_register.v1.json')['leads']}
    by_object = collections.defaultdict(set)
    for record in records:
        physical = record.get('physical_object_id', record['id'])
        if record.get('image_path'):
            by_object[physical].add(record['image_path'])
        for capture in record.get('captures', []):
            if capture.get('path') and capture.get('physical_object_id', physical) == physical:
                by_object[physical].add(capture['path'])
    changed, objects, missing_paths = set(), set(), set()
    assert set(before) == set(after)
    for lead_id, old in before.items():
        lead = after[lead_id]
        assert old['decision_state'] == lead['decision_state']
        now = lead.get('required_inputs', {}).get('available_primary_images', {})
        assert set(old['available_primary_images']) == set(now)
        for physical, previous in old['available_primary_images'].items():
            expected = set(previous) | by_object[physical]
            later = {c['path'] for c in read('research/continuation_65/captures.json')['captures'] if c['physical_object_id'] == physical}
            assert set(now[physical]) == expected | later, (lead_id, physical)
            assert len(now[physical]) == len(set(now[physical])), (lead_id, physical)
            added = expected - set(previous)
            if added:
                changed.add(lead_id)
                objects.add(physical)
                missing_paths.update(added)
    for path in missing_paths:
        assert (ROOT / path).is_file(), path
    graph = read('data/knowledge.v1.json')
    images = {e['path']: e for e in graph['entities'] if e['type'] == 'ImageDerivative'}
    captures = {e['id']: e for e in graph['entities'] if e['type'] == 'Capture'}
    for physical in objects:
        for path in by_object[physical]:
            assert captures[images[path]['capture']]['physical_object'] == 'object:' + physical
            sha = images[path].get('sha256')
            if sha:
                assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == sha, path
    actual = {'affected_leads': len(changed), 'affected_objects': len(objects),
              'distinct_previously_unlisted_paths': len(missing_paths),
              'decisions_unchanged': True, 'new_source_images': 0,
              'new_historical_discovery': False}
    assert actual == read('research/continuation_62/results.json')
    print(json.dumps(actual))


if __name__ == '__main__':
    main()
