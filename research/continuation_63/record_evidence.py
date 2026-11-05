"""Record two post-exposure source regions; no identity or reliability scoring."""
import hashlib,json
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
records={r['id']:r for r in json.loads((ROOT/'data/fragments.json').read_text())}
items=[
 ('I63-iv173-dignare','finn-iv173','data/images/fm-IV173-2.jpg',[375,738,95,142],
  'The D of Dignare has a red stem, pale right body with two red diamond-like marks, a dark outer contour and dark projections on the left. Its role is a verse within the Te Deum, not necessarily equivalent to the compared Fr1385 initial.', 'Dignare…'),
 ('I63-1385-dabit','mpo-1385','data/images/mpo-1385.jpg',[90,123,55,67],
  'The candidate D of Dabit has a red vertical stem and a pale right field with a colored mark. The retained photograph is low resolution; fine edge, inner construction and number or color of marks are not secure.', 'Dabit…')]
annotations=[]
for aid,rid,path,box,observation,literal in items:
 r=records[rid]; cap=next(c for c in r.get('captures',[]) if c['path']==path)
 sha=hashlib.sha256((ROOT/path).read_bytes()).hexdigest();assert sha==cap['sha256']
 with Image.open(ROOT/path) as im: assert im.size==(cap['width'],cap['height'])
 x,y,w,h=box;assert 0<=x<x+w<=cap['width'] and 0<=y<y+h<=cap['height']
 annotations.append({'id':aid,'type':'Annotation','motivation':'describing','fragment_id':rid,
  'body':{'type':'TextualBody','value':observation,'language':'en'},
  'target':{'source':path,'selector':{'type':'FragmentSelector','conformsTo':'http://www.w3.org/TR/media-frags/','value':f'xywh={x},{y},{w},{h}'}},
  'source_url':cap['url'],'sha256':sha,'image_dimensions':[cap['width'],cap['height']],
  'rights_url':r['rights_url'],'attribution':r['attribution'],'literal_candidate':literal,
  'observer':'Codex AI, post-exposure inspection, 2026-11-01; exact model checkpoint unavailable',
  'independent_confirmation':False,'interpretation_limits':['Selected after previous exposure; not a blind or independent reading.','Decorative function differs or is incompletely matched; feature overlap is not evidence of one book.']})
(HERE/'observations.json').write_text(json.dumps({'version':'1.0.0','annotations':annotations},indent=2,ensure_ascii=False)+'\n')
print('Recorded two source-linked regions')
