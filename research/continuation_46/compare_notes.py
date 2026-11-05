"""Describe declared manual windows; never turn them into codex scores."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def height(source, event):
    (x1,y1),(x2,y2)=source['local_reference_rule']
    x,y=event['pixel']
    return y1+(y2-y1)*(x-x1)/(x2-x1)-y


def compare(readings):
    sources=readings['sources']
    counts={key:sum(e['underlay_candidate'].startswith(('ce','los')) for e in s['events'])
            for key,s in sources.items()}
    directions=[]
    for key,source in sources.items():
        tan=next(e for e in source['events'] if e['underlay_candidate'].startswith('tan'))
        ge=next(e for e in source['events'] if e['underlay_candidate']=='ge')
        change=height(source,ge)-height(source,tan)
        dx=abs(ge['pixel'][0]-tan['pixel'][0])
        sensitivity=[]
        for tolerance in [3,4,5]:
            # Manual centre bounds plus an exploratory slope perturbation.
            # These are sensitivity assumptions, never confidence intervals.
            spread=2*tolerance+0.02*dx
            lower,upper=change-spread,change+spread
            direction='rise' if lower>0 else ('fall' if upper<0 else 'unresolved')
            sensitivity.append({'centre_tolerance_px':tolerance,'slope_perturbation_px_per_px':0.02,
                'range_px':[round(lower,3),round(upper,3)],'direction':direction})
        directions.append({'source':key,'nominal_height_change_px':round(change,3),
            'sensitivity':sensitivity,'exact_diatonic_interval':None})
    robust=all({row['sensitivity'][i]['direction'] for row in directions}=={'rise','fall'}
               for i in range(3))
    return {'version':'1.0.0','input':'research/continuation_46/readings.v2.json',
        'scope':'Fixed three-word windows: visible head groups and exploratory deskewed direction only.',
        'candidate_celos_head_counts':counts,'celos_head_count_difference':counts['8066']!=counts['9620'],
        'candidate_primary_centres':sum(len(s['events']) for s in sources.values()),
        'optional_uncertain_centres':sum(len(s['optional_events']) for s in sources.values()),
        'tan_to_ge_directions':directions,'robust_direction_contrast':robust,
        'direction_limit':'The8066 direction becomes unresolved at wider tolerance; optional tan segmentation remains. No certified interval contrast.',
        'same_complete_chant_identification_established':False,'diagnostic_melodic_variant_established':False,
        'melodic_identity_established':False,'same_codex_established':False,'different_codex_established':False,
        'novelty_cleared':False,'independent_confirmation':False,
        'interpretation':readings['interpretation'],
        'limits':readings['limits']}


def main():
    result=compare(json.loads((HERE/'readings.v2.json').read_text()))
    (HERE/'comparison.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['candidate_celos_head_counts','candidate_primary_centres',
        'optional_uncertain_centres','robust_direction_contrast','diagnostic_melodic_variant_established']}))


if __name__=='__main__':
    main()
