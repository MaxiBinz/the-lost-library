"""Record an unblinded, reference-assisted reading and its limits."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];HERE=ROOT/'research/continuation_61'
def write(name,value):(HERE/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
def main():
 record=next(r for r in json.loads((ROOT/'data/fragments.json').read_text()) if r['id']=='mpo-10370')
 path='data/images/mpo-10370-capture-4-1742px.jpg';cap=next(c for c in record['captures'] if c['path']==path)
 sha=hashlib.sha256((ROOT/path).read_bytes()).hexdigest();assert sha==cap['sha256']
 x,y,w,h=290,10,900,690;assert x+w<=cap['width'] and y+h<=cap['height']
 ann={'id':'I61-10370-gloriosa','type':'Annotation','motivation':'describing',
  'body':{'type':'TextualBody','value':'Damaged, partially erased lower-field passage, provisionally Gloriosa diei huius sollempnia and later caelos meruit a[...], consistent with responsory 006779. It does not establish the lost end of the writing or original page boundary.','language':'en'},
  'target':{'source':path,'selector':{'type':'FragmentSelector','conformsTo':'http://www.w3.org/TR/media-frags/','value':f'xywh={x},{y},{w},{h}'}},
  'fragment_id':'mpo-10370','source_url':cap['url'],'sha256':sha,'image_dimensions':[cap['width'],cap['height']],
  'rights_url':record['rights_url'],'attribution':record['attribution'],
  'literal_candidate':'Gloriosa diei [...] sollempnia deuota celebremus [...] qua beata maria [...] celos meruit a[...]',
  'observer':'Codex AI, unblinded and reference-assisted, 2026-11-01; model checkpoint unavailable','independent_confirmation':False,
  'interpretation_limits':['Reading is provisional, selected and incomplete; erasure prevents a complete terminal transcription.','Capture order does not establish original side, physical adjacency or a complete surface.']}
 write('observations.json',{'version':'1.0.0','annotations':[ann]})
 out={'version':'1.0.0','date':'2026-11-01','source_regions':[ann['id']],
  'local_observation':'The exposed lower-field words in Fr10370 capture4 provisionally fit responsory Gloriosa diei 006779; the final line is incomplete and the right side is erased.',
  'comparison':'In the search-indexed Barcelona Ms.2322 f.097v, Gloriosa 006779 and its verse occur before a versicle, a first lauds antiphon, and then Haec corde compuncta. This is an example of non-immediate liturgical order, not proof of Fr10370/IV156 page order.',
  'finnish_context':'The indexed IV156 folio8 opening is within Haec corde compuncta at lauds. A Matins-to-lauds progression is plausible if the candidate identifications and original surface order hold, but no unique identity or immediate adjacency follows.',
  'e60_effect':'The comparison does not resolve the E60 same-address conditional conflict; placing the Swedish fragment earlier than f8 requires a different address, reset, side interpretation or another explanation if the compared k-II mark is assumed unique.',
  'reference_source_directly_opened':False,'finnish_image_inspected':False,'complete_final_text_verified':False,'same_book_proved':False,'adjacent_pages_proved':False,'e60_conflict_resolved':False,'new_discovery':False,'independent_confirmation':False,'new_source_images':0,'new_download_bytes':0,
  'next_test':'Obtain and inspect IV156 f8 original, verify the Swedish mark/side mapping and the unique-address assumptions. Use any further text comparison to test exact written boundaries, not broad feast similarity.'}
 write('results.json',out);print(json.dumps({'new_source_regions':1,'finnish_image':False,'same_book_proved':False}))
if __name__=='__main__':main()
