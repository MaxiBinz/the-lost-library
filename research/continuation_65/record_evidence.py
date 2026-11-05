"""Record the retained, unblinded 8201 source region and the reading limits."""
import hashlib,json
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
c=json.loads((HERE/'captures.json').read_text())['captures'][0]; path=ROOT/c['path']
assert hashlib.sha256(path.read_bytes()).hexdigest()==c['sha256']
with Image.open(path) as im: assert im.size==(c['width'],c['height'])
x,y,w,h=350,245,760,155;assert x+w<=c['width'] and y+h<=c['height']
a={'id':'I65-8201-ending','type':'Annotation','motivation':'describing','fragment_id':'mpo-8201',
 'body':{'type':'TextualBody','value':'The first retained photograph begins within the surviving phrase, provisionally pulchrior sponso superno placuit, followed by a red cue. The visible final letter of sponso is o-like; the reading is reference-exposed. The missing beginning is not supplied from the comparator as a local reading.','language':'en'},
 'target':{'source':c['path'],'selector':{'type':'FragmentSelector','conformsTo':'http://www.w3.org/TR/media-frags/','value':f'xywh={x},{y},{w},{h}'}},
 'source_url':c['url'],'sha256':c['sha256'],'image_dimensions':[c['width'],c['height']],
 'rights_url':c['rights_url'],'attribution':c['attribution'],
 'literal_candidate':'pulchrior sponso superno placuit','normalized_candidate':'pulchrior sponso superno placuit',
 'observer':'Codex AI, prior reference exposure; 2026-11-01, exact model checkpoint unavailable','independent_confirmation':False,
 'interpretation_limits':['One fragmentary ending, not the beginning or the Fr20106 original.','No independently verified note-by-note transcription, page adjacency, or original side assignment.']}
b=dict(a)
b.update(id='I65-8201-next-chant',
 body={'type':'TextualBody','value':'The decorated initial and following text provisionally read Traditur ergo a patre doctoribus, after the surviving pulchrior ending on the same photographed surface. The selection and identification follow exposure to the published study and indexed Vienna sequence.','language':'en'},
 target={'source':c['path'],'selector':{'type':'FragmentSelector','conformsTo':'http://www.w3.org/TR/media-frags/','value':'xywh=325,385,1085,260'}},
 literal_candidate='Traditur ergo a patre doctoribus',normalized_candidate='Traditur ergo a patre doctoribus',
 interpretation_limits=['Selected after source and reference exposure; no blind reading.','A shared two-chant sequence does not establish book identity, exact melody, or physical adjacency to Fr20106.'])
(HERE/'observations.json').write_text(json.dumps({'version':'1.0.0','annotations':[a,b]},indent=2)+'\n')
