"""Reproduce a bounded visual-direction sensitivity check, not pitch transcription."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def main():
    readings = json.loads((ROOT / 'research/continuation_79/readings.json').read_text())
    directions = []
    for item in readings['items']:
        x1, y1 = item['xys'][1]
        x2, y2 = item['xys'][2]
        dx = x2 - x1
        nominal = y2 - y1 - item['red_rule_slope_y_per_x'] * dx
        ranges = []
        for tolerance in readings['tolerances_px']:
            radius = 2 * tolerance + readings['slope_perturbation_y_per_x'] * abs(dx)
            lo, hi = nominal - radius, nominal + radius
            spacing = item['staff_spacing_px']
            spacing_error = readings['staff_spacing_tolerance_px']
            scaled = [value / scale for value in (lo, hi) for scale in (spacing-spacing_error, spacing+spacing_error)]
            ranges.append({'centre_tolerance_px': tolerance, 'range_y_down_px': [round(lo, 3), round(hi, 3)],
                           'range_staff_spacings': [round(min(scaled), 4), round(max(scaled), 4)],
                           'direction': 'lower_on_page' if lo > 0 else ('higher_on_page' if hi < 0 else 'unresolved')})
        directions.append({'id': item['id'], 'nominal_y_down_px': round(nominal, 3), 'sensitivity': ranges})
    difference_ranges = []
    for left, right in zip(directions[0]['sensitivity'], directions[1]['sensitivity']):
        lo = left['range_staff_spacings'][0] - right['range_staff_spacings'][1]
        hi = left['range_staff_spacings'][1] - right['range_staff_spacings'][0]
        difference_ranges.append({'centre_tolerance_px': left['centre_tolerance_px'],
                                  'range_staff_spacings': [round(lo, 4), round(hi, 4)],
                                  'excludes_zero': lo > 0 or hi < 0})
    result = {'coordinate_scope':'est to do- only; relative to selected local red rule', 'items':directions,
              'between_source_difference_ranges': difference_ranges,
              'between_source_difference_robustly_established':all(x['excludes_zero'] for x in difference_ranges), 'pitch_transcribed':False,
              'selected_centres_independently_verified':False}
    (ROOT / 'research/continuation_79/comparison.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result))

if __name__ == '__main__':
    main()
