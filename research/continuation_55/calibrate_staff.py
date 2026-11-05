"""Descriptive source-local staff geometry, not musical recognition.

Retains E39 anchors and explores red-pixel selection plus explicit anchor/rule
uncertainty. Integer alternatives describe a geometric rounding model only;
they do not establish a neume reading or absolute/sounding pitches.
"""
import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
WINDOWS = {
    'target': {
        'nobis-vite-spem': dict(x=[850,1330], bands=[[302,335],[338,371],[376,407],[412,442]]),
        'fac-nos-virgo': dict(x=[720,1100], bands=[[518,544],[552,580],[590,618],[628,656]]),
        'thresholds': [[20,15],[25,20],[35,25]],
    },
    'c23': {
        'nobis-vite-spem': dict(x=[820,1320], bands=[[983,1009],[1022,1048],[1062,1088],[1103,1129]]),
        'fac-nos-virgo': dict(x=[930,1320], bands=[[1262,1288],[1303,1330],[1343,1370],[1382,1410]]),
        'thresholds': [[15,30],[20,40],[25,50]],
    },
}


def read(path):
    return json.loads((ROOT/path).read_text())


def fit_rule(rgb, xrange, band, threshold):
    x1,x2=xrange; y1,y2=band
    q=rgb[y1:y2,x1:x2].astype(float)
    mask=(q[:,:,0]-q[:,:,1]>threshold[0]) & (q[:,:,0]-q[:,:,2]>threshold[1]) & (q[:,:,0]>90)
    # Retain columns with a compact coloured run rather than broad text/rubric.
    points=[]
    for i in range(mask.shape[1]):
        ys=np.flatnonzero(mask[:,i])
        if 1 <= len(ys) <= 12:
            points.append([x1+i,y1+float(np.median(ys))])
    xy=np.array(points)
    if len(xy)<30:
        return dict(valid=False, reason='Fewer than30 selected columns', selected_columns=len(xy))
    keep=np.ones(len(xy),dtype=bool)
    for _ in range(4):
        slope,intercept=np.polyfit(xy[keep,0],xy[keep,1],1)
        residual=xy[:,1]-(slope*xy[:,0]+intercept)
        keep=np.abs(residual)<=4
        if keep.sum()<30:
            return dict(valid=False,reason='Too few robust inliers',selected_columns=len(xy))
    residual=xy[keep,1]-(slope*xy[keep,0]+intercept)
    return dict(valid=True,slope=float(slope),intercept=float(intercept),
                selected_columns=len(xy),inlier_columns=int(keep.sum()),
                residual_abs_p95=float(np.quantile(np.abs(residual),.95)))


def main(output_dir=HERE):
    protocol=read('research/continuation_55/protocol.json')
    readings=read('research/continuation_39/readings.v3.json')
    out=dict(version='1.0.0',date='2026-10-31',
        selection='Existing E39 head anchors retained unchanged; manually located rule search bands after raw-source exposure.',
        scope='Local geometric position only; no independent pitch/neume adjudication.',
        anchor_shift_sensitivity_pixels=[-3,0,3],
        rule_vertical_shift_sensitivity_pixels=[-2,0,2], windows={}, notes=[])
    proof=Image.new('RGB',(1300,710),'white');draw=ImageDraw.Draw(proof)
    for si,(name,s) in enumerate(readings['sources'].items()):
        path=ROOT/s['path'];assert hashlib.sha256(path.read_bytes()).hexdigest()==s['sha256']
        rgb=np.array(Image.open(path).convert('RGB'))
        for pi,(phrase,notes) in enumerate(s['phrases'].items()):
            spec=WINDOWS[name][phrase]
            models=[]
            for th in WINDOWS[name]['thresholds']:
                rules=[fit_rule(rgb,spec['x'],b,th) for b in spec['bands']]
                models.append(dict(threshold_r_minus_g=th[0],threshold_r_minus_b=th[1],rules=rules,
                                   valid=all(r['valid'] for r in rules)))
            ident=name+':'+phrase;out['windows'][ident]=dict(search=spec,models=models)
            for n in notes:
                x,y=n['pixel'];values=[];nominal=[]
                for m in models:
                    if not m['valid']:continue
                    rules=m['rules'];positions=[r['slope']*x+r['intercept'] for r in rules]
                    step=(positions[-1]-positions[0])/6
                    assert step>0
                    nominal.append((positions[-1]-y)/step)
                    for dy in out['anchor_shift_sensitivity_pixels']:
                        for dr in out['rule_vertical_shift_sensitivity_pixels']:
                            # Uniform local shift is a deliberately simple source-
                            # placement sensitivity, not a probabilistic interval.
                            values.append((positions[-1]+dr-(y+dy))/step)
                ints=sorted({int(np.floor(v+.5)) for v in values})
                out['notes'].append(dict(source=name,phrase=phrase,slot=n['slot'],underlay=n['underlay'],
                    original_anchor=n['pixel'],e39_relative_alternatives=n['relative_staff_steps'],
                    geometric_absolute_position_from_bottom_rule_nominal=nominal,
                    geometric_absolute_position_range=[min(values),max(values)] if values else None,
                    geometric_nearest_integer_alternatives=ints,
                    sounding_pitch_adjudicated=False))
            x1,x2=spec['x'];y1=spec['bands'][0][0]-50;y2=spec['bands'][-1][1]+30
            crop=Image.fromarray(rgb).crop((x1,y1,x2,y2))
            dx=si*650+15;dy=pi*350+35
            proof.paste(crop,(dx,dy));draw.text((dx,dy-22),ident+'; raw pixels and rule fit',fill='black')
            central=models[1]
            if central['valid']:
                for r in central['rules']:
                    draw.line([(dx,r['slope']*x1+r['intercept']-y1+dy),
                               (dx+x2-x1,r['slope']*x2+r['intercept']-y1+dy)],fill='blue',width=1)
            for n in notes:
                x,y=n['pixel'];px=dx+x-x1;py=dy+y-y1
                draw.ellipse([px-3,py-3,px+3,py+3],outline='green',width=1)
                draw.text((px+5,py-16),str(n['slot']),fill='green')
    for row in out['notes']:
        zero=next(n for n in out['notes'] if n['source']==row['source'] and n['phrase']==row['phrase'] and n['slot']==1)
        row['geometric_relative_alternatives']=sorted({a-b for a in row['geometric_nearest_integer_alternatives'] for b in zero['geometric_nearest_integer_alternatives']})
    output_dir.mkdir(parents=True,exist_ok=True)
    (output_dir/'staff_calibration.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    proof.save(output_dir/'staff-review.png')
    print(json.dumps({'valid_rule_models':sum(m['valid'] for w in out['windows'].values() for m in w['models']),
                      'models':12,'retained_head_anchors':len(out['notes']),
                      'upper_events':[{k:n[k] for k in ['source','phrase','slot','geometric_absolute_position_range','geometric_relative_alternatives']} for n in out['notes'] if n['slot']==4],
                      'scope':out['scope']}))


if __name__=='__main__':
    main()
