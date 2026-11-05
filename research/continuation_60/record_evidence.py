"""Record fixed source-pixel regions and the conditional comparison."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[2];HERE=ROOT/'research/continuation_60'
def write(name,obj):(HERE/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def main():
 r=next(r for r in json.loads((ROOT/'data/fragments.json').read_text()) if r['id']=='mpo-10370')
 caps={c['path']:c for c in r['captures']}
 specs=[('I60-10370-top','data/images/mpo-10370-capture-1-1700px.jpg',[265,190,1180,200],
         '[...le]ne circa ministeria que sedens secus pedes domini audie[...]',
         'Uppermost preserved written line on the image bearing the II-like mark. Candidate continuation of Satagebat igitur, 004816; beginning is cut within a word and the reading was reference-assisted.'),
        ('I60-10370-sequence','data/images/mpo-10370-capture-1-1700px.jpg',[270,380,1170,750],
         '[...] verba oris eius / Non est Martha [...] / Et respondens [...]',
         'Same photograph shows an ending followed by two decorated chant openings, provisionally Non est Martha and Et respondens. This supports a Matins-context candidate, not a full edition or unique identity.')]
 out=[]
 for ident,path,xywh,literal,body in specs:
  c=caps[path];sha=hashlib.sha256((ROOT/path).read_bytes()).hexdigest();assert sha==c['sha256']
  x,y,w,h=xywh;assert x+w<=c['width'] and y+h<=c['height']
  out.append({'id':ident,'type':'Annotation','motivation':'describing','body':{'type':'TextualBody','value':body,'language':'en'},
   'target':{'source':path,'selector':{'type':'FragmentSelector','conformsTo':'http://www.w3.org/TR/media-frags/','value':f'xywh={x},{y},{w},{h}'}},
   'fragment_id':'mpo-10370','source_url':c['url'],'sha256':sha,'image_dimensions':[c['width'],c['height']],
   'rights_url':r['rights_url'],'attribution':r['attribution'],'literal_candidate':literal,'observer':'Codex AI, unblinded and reference-assisted; 2026-11-01','independent_confirmation':False,
   'interpretation_limits':['No full diplomatic edition, Finnish image, unique addressing convention or medieval side mapping.']})
 write('observations.json',{'version':'1.0.0','annotations':out})
 result={'version':'1.0.0','date':'2026-11-01','source_regions':[a['id'] for a in out],
  'reused_regions':['V-10370-mark','V-10370-kmark'],
  'local_reading':'The numeral-bearing capture begins within a line tentatively matching Satagebat igitur 004816, then shows Non est Martha and Et respondens candidates; this is unblinded and reference-assisted.',
  'finnish_assertion':'The indexed IV.156 folio 8 entry gives [k] ijr to k [iij] verso and says its opening continues with ihesu of Haec corde compuncta at lauds. The underlying Finnish leaf and OCR-ambiguous full page were not read.',
  'conditional_result':'If both II-like addresses identify the same unique original page and both openings are complete and correctly mapped, the different reported opening words require revision of at least one premise or the proposed identity. No direct Finnish page comparison or exclusion is established.',
  'alternatives':['Swedish sign or Finnish bracketed address is wrong or differently understood','same address repeats or resets in separate sections','one image is cropped or side mapping differs','catalogue boundary or OCR is wrong','composite volume or later rearrangement'],
  'known_prior_art':'The Finnish catalogue already places the Fr10370 wrapper between IV.157 folios 7 and 8; BOMPAC assigns Fr10370 and IV.156 to unit 5324. The catalogue wrapper crosswalk and combined-dataset assignment are prior assertions, not our independently verified physical placements.',
  'next_test':'Obtain an authoritative IV.156 folio 8 original opening and signature and inspect Fr10370 exact capture-side mapping; compare the texts and test address uniqueness/reset and composite alternatives. Read relevant Taitto/Keskiaho sources before originality claims.',
  'finnish_image_inspected':False,'same_address_verified':False,'physical_identity_rejected':False,'catalogue_error_proved':False,'new_discovery':False,'independent_confirmation':False,'new_source_images':0,'new_download_bytes':0}
 write('results.json',result)
 print(json.dumps({'new_regions':len(out),'conditional_conflict':True,'exclusion':False}))
if __name__=='__main__':main()
