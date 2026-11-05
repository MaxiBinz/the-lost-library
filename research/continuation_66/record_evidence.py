"""Record post-exposure local reading; does not mechanically verify the Latin."""
import hashlib,json
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
c=json.loads((ROOT/'research/continuation_65/captures.json').read_text())['captures'][0]; f=ROOT/c['path']
assert hashlib.sha256(f.read_bytes()).hexdigest()==c['sha256']
with Image.open(f) as im:assert im.size==(c['width'],c['height'])
a={'id':'I66-8201-nobilis','type':'Annotation','motivation':'describing','fragment_id':'mpo-8201',
 'body':{'type':'TextualBody','value':'Following Traditur, the large red N begins a candidate responsory reading Nobilis et pulchra virgo katherina beata. The next written line includes spernit vaga gaudia mundi. Reading and word separation are reference-exposed and provisional.','language':'en'},
 'target':{'source':c['path'],'selector':{'type':'FragmentSelector','conformsTo':'http://www.w3.org/TR/media-frags/','value':'xywh=295,645,1110,300'}},
 'source_url':c['url'],'sha256':c['sha256'],'image_dimensions':[c['width'],c['height']],'rights_url':c['rights_url'],'attribution':c['attribution'],
 'literal_candidate':'Nobilis et pulchra virgo katherina beata [...] spernit vaga gaudia mundi',
 'normalized_candidate':'Nobilis et pulchra virgo Katherina beata ... spernit vaga gaudia mundi',
 'observer':'Codex AI, post-exposure image reading, 2026-11-02; exact model checkpoint unavailable','independent_confirmation':False,
 'interpretation_limits':['No independent reader has checked the Latin or source extent.','The source-text resemblance with a published edition is not proof of physical manuscript identity, musical identity, ancestry or geographical origin.']}
(HERE/'observations.json').write_text(json.dumps({'version':'1.0.0','annotations':[a]},indent=2,ensure_ascii=False)+'\n')
