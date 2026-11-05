"""Record selected Fr8311 text windows and a bounded prior-art comparison."""
import hashlib
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]

def main():
    p=json.loads((HERE/'protocol.json').read_text())
    record=next(r for r in json.loads((ROOT/'data/fragments.json').read_text()) if r['id']=='mpo-8311')
    caps={c['path']:c for c in record['captures']}
    readings=[
      ('I57-8311-sudore','data/images/mpo-8311-capture-2.jpg',[90,15,680,430],'[... in sudo]re vultus tui [...]', 'A provisional In sudore opening continues over successive visible staff lines. The bottom contains a Pro-like beginning; its continuation on another photo is a text-order hypothesis, not a demonstrated physical seam.'),
      ('I57-8311-abel','data/images/mpo-8311-capture-3.jpg',[230,140,680,380],'[...] eo quod obedisti voci uxoris tue [...] / Ubi est abel frater tuus [...]','A Pro-eo-quod-oboedisti continuation candidate precedes a decorated Ubi est Abel opening within this photograph. This supports two known-work candidates but is not a complete edition or physical side map.'),
      ('I57-8311-maledicta','data/images/mpo-8311-capture-4.jpg',[220,75,680,400],'Maledicta terra in opere tuo [...] / Miserere mei deus [...]','A Maledicta-terra verse candidate is followed by a Miserere-mei opening; the earlier Abel ending is a plausible textual context. No exact melody or diagnostic book identity is inferred.')]
    annotations=[]
    for ident,path,xywh,literal,body in readings:
        s=next(x for x in p['sources'] if x['path']==path);c=caps[path]
        assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==s['sha256']
        x,y,w,h=xywh;assert 0<=x<x+w<=s['width'] and 0<=y<y+h<=s['height']
        annotations.append({'id':ident,'type':'Annotation','motivation':'describing','body':{'type':'TextualBody','value':body,'language':'en'},
          'target':{'source':path,'selector':{'type':'FragmentSelector','conformsTo':'http://www.w3.org/TR/media-frags/','value':'xywh='+','.join(map(str,xywh))}},
          'fragment_id':'mpo-8311','source_url':c['url'],'sha256':s['sha256'],'image_dimensions':[s['width'],s['height']],
          'rights_url':record['rights_url'],'attribution':record['attribution'],'literal_candidate':literal,'normalized_candidate':None,
          'observer':'Codex AI; unblinded reinspection, 2026-11-01','independent_confirmation':False,
          'interpretation_limits':['Partial provisional reading; no complete chant or melody edition.','Photograph index is not a medieval side or demonstrated physical join.']})
    (HERE/'observations.json').write_text(json.dumps({'version':'1.0.0','annotations':annotations},ensure_ascii=False,indent=2)+'\n')
    out={'version':'1.0.0','date':'2026-11-01','selected_lead':'fr8311-chant','source_regions':[a['id'] for a in annotations],
      'prior_regions':['O-mpo-8311-1-5','O-mpo-8311-1-6'],
      'local_reading':'Dum deambularet / Vocem tuam candidates, In sudore / Pro eo candidates, Ubi est Abel / Maledicta terra candidates and a following Miserere opening are visible in the four selected photos. Exact complete work transcriptions and medieval side mapping remain incomplete.',
      'work_candidates':['006537','006537a','006937','006937a','007804','007804a','003774'],
      'prior_art':{'url':'https://epub.uni-regensburg.de/51986/3/Historiae%20Trevirenses_Appendix_Brink.pdf',
        'locator':'Printed p.29, indexed Trier Bistumsarchiv Ms.480 fols.51v–52r; web-reader text, visual PDF page not inspected after screenshot cache miss.',
        'comparison':'The published inventory lists the three candidate responsories consecutively, followed by Miserere, and includes Pro-eo and Maledicta-terra verses. Its first responsory verse is 006537b, while Fr8311 has a 006537a candidate. The complete photographed sequence and physical order in Fr8311 are not established.',
        'scope':'Published index, not inspected Trier original or melody; no rarity, direct copying or manuscript identity established.'},
      'failed_routes':['https://cantusdatabase.org/chant/463836/','https://cantusdatabase.org/chant/179885/','https://cantusdatabase.org/chant/432697/','https://cantusdatabase.org/chant/409417/','https://cantusdatabase.org/chant/493520/'],
      'decisions':'All historical lead states and frozen reviews unchanged; candidate identifications remain provisional.','source_photo_views_inspected':4,
      'new_source_files':0,'new_download_bytes':0,'new_discovery':False,'exact_melody_verified':False,
      'complete_side_map':False,'physical_join_established':False,'new_codex_attribution':False,'independent_confirmation':False,
      'next_test':'Do not treat this partial repertory order as a unique signature. Further identity work requires a distinctive corresponding text variant, a physical feature, or an original-side map; seek a genuinely discriminating retained-source question.'}
    (HERE/'results.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'regions':len(annotations),'views':4,'unique_sequence_established':False}))
if __name__=='__main__':main()
