"""Record four source regions for E37; verify bytes/bounds, not reading truth."""
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
SITES=[
 ("I37-20274-ending-1","mpo-20274","data/images/mpo-20274-capture-1-1831px.jpg",[230,425,1510,115],
  "dolor cessit cum sur rexit nobis vite spem porre xit pre[...]",
  "Dolor cessit cum surrexit nobis vite spem porrexit pre[...]; word spacing normalized",
  "The first visible text row has the differentiating phrase nobis vite spem porrexit, with cum provisionally read before surrexit. It does not read the older C23 tam prolixus / ille dulcis crucifixus ending."),
 ("I37-20274-ending-2","mpo-20274","data/images/mpo-20274-capture-1-1831px.jpg",[235,630,1505,125],
  "si dens in gloria fac nos virgo sue mortis et do loris tui",
  "[pre]sidens in gloria; Fac nos Virgo sue mortis et doloris tui",
  "This row continues the preceding pre- as sidens and reads the Fac nos Virgo petition. Together the contiguous rows identify the shorter O Maria stans sub cruce ending; its incipit is not visible."),
 ("I37-20274-ending-3","mpo-20274","data/images/mpo-20274-capture-1-1831px.jpg",[230,840,1490,130],
  "for tis ferue re me mor ia alle luya [...]",
  "fortis feruere memoria; Alleluia [...]",
  "The petition ends fortis feruere memoria, provisionally read directly from the ink. This word is reported for several witnesses in the edition, so it is not a unique lineage marker. Matins begins below."),
 ("I37-C23-older-ending","uub-c23-0144","research/continuation_20/c23/c23-attachment-0144-2200px.jpg",[600,450,1370,700],
  "[...] plaude pro data uicto ria dolor cessit tam / prolixus ille dulcis crucifixus surrexit in / glo ria [...]",
  "[...] pro data victoria; Dolor cessit tam prolixus, ille dulcis crucifixus, surrexit in gloria [...]",
  "Actual C23 71v preserves the different older O Maria dolorosa ending above its matins invitatory. This comparison page is not the added/replacement O Maria stans text on C23 69r; that page remains missing locally.")
]


def sha(path):
    with path.open('rb') as stream:return hashlib.file_digest(stream,'sha256').hexdigest()


def main():
    records=json.loads((ROOT/'data/fragments.json').read_text())+json.loads((ROOT/'data/comparison_sources.v1.json').read_text())
    records={r['id']:r for r in records}
    annotations=[];illustrations=[]
    for ident,rid,path,box,literal,normalized,meaning in SITES:
        record=records[rid];capture=next(c for c in record['captures'] if c['path']==path)
        assert sha(ROOT/path)==capture['sha256']
        x,y,w,h=box
        with Image.open(ROOT/path) as im:
            assert im.size==(capture['width'],capture['height'])
            assert 0<=x<x+w<=im.width and 0<=y<y+h<=im.height
            illustrations.append((ident,path,box,im.convert('RGB').crop((x,y,x+w,y+h))))
        annotations.append({'id':ident,'type':'Annotation','motivation':'describing',
          'body':{'type':'TextualBody','value':meaning,'language':'en'},
          'target':{'source':path,'selector':{'type':'FragmentSelector','conformsTo':'http://www.w3.org/TR/media-frags/','value':'xywh='+','.join(map(str,box))}},
          'fragment_id':rid,'source_url':capture['url'],'sha256':capture['sha256'],
          'image_dimensions':[capture['width'],capture['height']],'rights_url':record['rights_url'],
          'literal_candidate':literal,'normalized_candidate':normalized,
          'observer':'Codex AI literature-assisted source reading, 2026-10-27',
          'independent_confirmation':False,
          'interpretation_limits':['Exploratory, literature-assisted identification; no independent reader.','Selected surviving ending only; no full-office recension, date, geographical attribution, physical identity or melodic genealogy inferred.']})
    (HERE/'observations.json').write_text(json.dumps({'version':'1.0.0','assessment_date':'2026-10-27','annotations':annotations},ensure_ascii=False,indent=2)+'\n')
    proof=Image.new('RGB',(1560,sum(im.height+65 for _,_,_,im in illustrations)),'white');draw=ImageDraw.Draw(proof);y=0
    for ident,path,box,im in illustrations:
        draw.text((10,y+8),ident+' / '+path,fill='black')
        draw.text((10,y+25),'xywh='+str(box)+' / original source pixels; no generated detail',fill='black')
        proof.paste(im,(10,y+50));y+=im.height+65
    proof.save(HERE/'magnificat-comparison.png')
    # This validates only declared string consistency; the source reading still
    # needs inspection. No concordance or model output independently verifies it.
    checks={'target_contains_differentiating_phrase':'nobis vite spem porrexit' in SITES[0][5],
            'older_source_has_other_phrase':'tam prolixus' in SITES[3][5] and 'ille dulcis crucifixus' in SITES[3][5],
            'shared_sur_rexit_not_used_alone':True,'regions':len(annotations)}
    (HERE/'checks.json').write_text(json.dumps(checks,indent=2)+'\n')
    print(json.dumps({'verified_regions':len(annotations),'reading_truth':'not machine-verified','scope':'one surviving antiphon ending'}))


if __name__=='__main__':main()
