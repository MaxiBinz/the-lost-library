"""Compare declared manual staff positions without turning ambiguity into agreement."""
import csv
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def compare_slot(left, right):
    # Compatibility of alternatives is not a verified matching note. None
    # represents uncertain event segmentation, not a rest or zero pitch.
    if len(left) != 1 or len(right) != 1 or None in left or None in right:
        return 'unresolved'
    return 'agree' if left[0] == right[0] else 'different'


def compare(readings):
    target = readings['sources']['target']['phrases']
    reference = readings['sources']['c23']['phrases']
    assert target.keys() == reference.keys()
    rows = []
    for phrase in target:
        assert len(target[phrase]) == len(reference[phrase])
        for left, right in zip(target[phrase], reference[phrase]):
            assert left['slot'] == right['slot'] and left['underlay'] == right['underlay']
            rows.append({'phrase': phrase, 'slot': left['slot'], 'underlay': left['underlay'],
                         'target_staff_steps': left['relative_staff_steps'],
                         'c23_staff_steps': right['relative_staff_steps'],
                         'result': compare_slot(left['relative_staff_steps'], right['relative_staff_steps']),
                         'target_pixel': left['pixel'], 'c23_pixel': right['pixel']})
    return {'version': '1.0.0', 'input': 'research/continuation_39/readings.v3.json',
            'scope': 'Two selected phrase windows, each independently normalized to staff-step zero; no absolute pitches or full melody',
            'potential_aligned_positions': len(rows),
            'provisional_agree': sum(row['result'] == 'agree' for row in rows),
            'unresolved': sum(row['result'] == 'unresolved' for row in rows),
            'different': sum(row['result'] == 'different' for row in rows),
            'rows': rows, 'melodic_identity_established': False, 'independent_confirmation': False,
            'limits': 'Calculates consistency of declared AI readings, not reading truth, rare variants, book identity or population accuracy.'}


def main():
    result = compare(json.loads((HERE / 'readings.v3.json').read_text()))
    (HERE / 'comparison.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    with (HERE / 'note_positions.csv').open('w', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(result['rows'][0]))
        writer.writeheader()
        writer.writerows(result['rows'])
    print(json.dumps({key: value for key, value in result.items() if key != 'rows'}, ensure_ascii=False))


if __name__ == '__main__':
    main()
