"""Sensitivity of two manually selected note movements, in staff spacings."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def main():
    data = json.loads((ROOT / 'research/continuation_80/readings.json').read_text())
    output = []
    for item in data['items']:
        (x1, y1), (x2, y2) = item['points']
        dx = x2-x1
        nominal = y2-y1-item['rule_slope']*dx
        scenarios = []
        for tolerance in data['centre_tolerances_px']:
            radius = 2*tolerance+data['slope_perturbation_px_per_px']*abs(dx)
            lo, hi = nominal-radius, nominal+radius
            spacing = item['staff_spacing_px']
            err = data['spacing_tolerance_px']
            scaled = [n/d for n in (lo, hi) for d in (spacing-err, spacing+err)]
            scenarios.append({'centre_tolerance_px':tolerance, 'range_y_down_px':[round(lo,3),round(hi,3)],
                              'range_staff_spacings':[round(min(scaled),4),round(max(scaled),4)],
                              'direction':'lower_on_page' if lo>0 else ('higher_on_page' if hi<0 else 'unresolved')})
        output.append({'id':item['id'], 'nominal_y_down_px':round(nominal,3), 'sensitivity':scenarios})
    differences = []
    for left, right in zip(output[0]['sensitivity'], output[1]['sensitivity']):
        lo = left['range_staff_spacings'][0]-right['range_staff_spacings'][1]
        hi = left['range_staff_spacings'][1]-right['range_staff_spacings'][0]
        differences.append({'centre_tolerance_px':left['centre_tolerance_px'], 'range_staff_spacings':[round(lo,4),round(hi,4)],
                            'excludes_zero':lo>0 or hi<0})
    result = {'scope':'do- to mi- of domini; movement relative to local rule', 'items':output,
              'between_source_difference_ranges':differences,
              'same_exact_interval_established':False, 'absolute_pitch_transcribed':False, 'independent_review':False}
    (ROOT / 'research/continuation_80/comparison.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))

if __name__ == '__main__':
    main()
