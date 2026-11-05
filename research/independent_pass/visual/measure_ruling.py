"""Reproduce a small, post-review source-image staff-spacing check.

No fitting or acquisition. Ruler anchors were read approximately by the AI
observer, not an expert. Their numbered intervals are not asserted to be cm.
These measurements cannot identify a book or calibrate identity probabilities.
"""
from pathlib import Path
import hashlib
import json
import numpy as np
from PIL import Image

ROOT=Path(__file__).resolve().parents[3]
OUT=Path(__file__).resolve().parent
SPECS=[
 {'fragment_id':'mpo-1385','path':'data/images/mpo-1385-capture-2.jpg',
  'sha256':'0a3f4c6bd4b94d8616b081feebbb8e41d2460b26d3a62ecedb76218912f35f1f',
  'windows':[[470,65,260,65],[470,158,260,63],[470,249,260,66],[470,338,260,66]],
  'approx_ruler_anchor_rows':{'0':632,'10':345}},
 {'fragment_id':'mpo-10406','path':'data/images/mpo-10406-capture-2.jpg',
  'sha256':'817ae2d3e4d65c91bae80c6d56ff009bd669252a039c63e7e9488afc9b3440eb',
  'windows':[[470,45,260,64],[470,140,260,65],[470,228,260,65],[470,320,260,65]],
  'approx_ruler_anchor_rows':{'0':594,'10':316}},
]

def main():
 results=[]
 for spec in SPECS:
  p=ROOT/spec['path'];assert hashlib.sha256(p.read_bytes()).hexdigest()==spec['sha256']
  with Image.open(p) as image: a=np.asarray(image).astype(float)
  staves=[]
  for x,y,w,h in spec['windows']:
   q=a[y:y+h,x:x+w]
   redness=(q[:,:,0]-q[:,:,1]).mean(axis=1)
   selected=[]
   for i in np.argsort(redness)[::-1]:
    if all(abs(int(i)-j)>9 for j in selected):selected.append(int(i))
    if len(selected)==4:break
   rows=sorted(y+i for i in selected)
   staves.append({'region_xywh':[x,y,w,h],'line_peak_rows':rows,
                  'interline_pixels':np.diff(rows).tolist(),
                  'staff_pitch_pixels':(rows[-1]-rows[0])/3})
  pitch=sum(s['staff_pitch_pixels'] for s in staves)/len(staves)
  anchors=spec['approx_ruler_anchor_rows'];scale=(anchors['0']-anchors['10'])/10
  # Sensitivity bound only: endpoints +/-1 px, ruler anchors +/-4 px.
  # It excludes perspective/nonplanarity and is NOT a confidence interval.
  lower=(pitch-2/3)/(scale+0.8);upper=(pitch+2/3)/(scale-0.8)
  results.append({**spec,'staves':staves,'mean_staff_pitch_pixels':pitch,
    'approx_pixels_per_numbered_ruler_interval':scale,
    'staff_pitch_per_numbered_ruler_interval':pitch/scale,
    'endpoint_sensitivity_range':[lower,upper]})
 result={'assessment_date':'2026-10-22','experiment':'post-review gross ruling-scale incompatibility check on H02',
  'observer':'Codex AI source inspection; no independent expert adjudication',
  'method':'Four visually selected four-line staffs per capture. Row mean(R-G); greedy four strongest peaks separated by >=10 pixels, visually checked by the AI observer against the displayed source. Normalize to approximate ruler numeral positions.',
  'results':results,'outcome':'No gross ruling-scale incompatibility detected in these samples; similar spacing is non-identifying.',
  'limits':['Selected windows and approximate ruler anchors were chosen after inspecting both sources; not blind or preregistered.','Numbered ruler intervals are not certified physical units. Source perspective, surface warping and lighting are not corrected.','Sensitivity ranges are deterministic endpoint perturbations, not statistical confidence intervals.','Comparable ruling does not prove same book, same hand, shared workshop, date or provenance.','No threshold or benchmark predictor was modified; this is a descriptive case check.']}
 (OUT/'measurements.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(result,indent=2))
if __name__=='__main__':main()
