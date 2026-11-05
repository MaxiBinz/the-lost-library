"""Reproduce post-inspection ruler-normalized field widths and all sensitivities."""
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent


def compare(readings):
    sens=readings['measurement_sensitivity']
    measured=[]
    for src in readings['field_measurements']:
        (x0,c0),(x1,c1)=src['ruler_x_cm']
        pixels=abs(x1-x0);centimetres=abs(c1-c0)
        span=abs(src['field_x_bounds'][1]-src['field_x_bounds'][0])
        rows=[]
        for tolerance in sens['field_endpoint_tolerances_px']:
            ruler_delta=2*sens['ruler_endpoint_tolerance_px']
            low=max(0,span-2*tolerance)*centimetres/(pixels+ruler_delta)
            high=(span+2*tolerance)*centimetres/(pixels-ruler_delta)
            scale=sens['additional_multiplicative_scale_tolerance']
            rows.append({'endpoint_tolerance_px':tolerance,'range_cm':[low,high],
                'with_additional_scale_range_cm':[low*(1-scale),high*(1+scale)]})
        measured.append({'object_id':src['object_id'],'path':src['path'],
            'nominal_field_width_cm':span*centimetres/pixels,'sensitivity':rows})
    comparisons=[]
    for a,b in zip(measured[0]['sensitivity'],measured[1]['sensitivity']):
        comparisons.append({'endpoint_tolerance_px':a['endpoint_tolerance_px'],
            'ranges_separate':a['range_cm'][1]<b['range_cm'][0],
            'ranges_separate_with_additional_scale':a['with_additional_scale_range_cm'][1]<b['with_additional_scale_range_cm'][0]})
    return {'version':'1.0.0','date':'2026-10-30','measurements':measured,
        'sensitivity_comparison':comparisons,'scope':readings['post_inspection_measurement_scope'],
        'historical_same_codex_excluded':False,'catalogue_measurement_corrected':False,
        'independent_confirmation':False,'new_discovery':False}


def main():
    d=json.loads((HERE/'manual_readings.json').read_text())
    result=compare(d)
    (HERE/'field_comparison.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'nominal_field_widths_cm':{r['object_id']:r['nominal_field_width_cm'] for r in result['measurements']},
        'all_sensitivity_outcomes':result['sensitivity_comparison']},indent=2))


if __name__=='__main__':
    main()
