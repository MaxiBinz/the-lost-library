"""Pin two exposed source regions for a bounded chant-context comparison."""
import hashlib
import json
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).parent


def main():
    prior = json.loads((ROOT/'research/continuation_54/observations.json').read_text())
    region = next(x for x in prior['annotations'] if x['id'] == 'I54-10407-irregabat')
    fragments = json.loads((ROOT/'data/fragments.json').read_text())
    obj = next(x for x in fragments if x['id']=='mpo-10406')
    cap = next(c for c in obj['captures'] if c['path']=='data/images/mpo-10406.jpg')
    specs = [
      ('I93-10407-secus', region['target']['source'], region['source_url'], region['sha256'], region['image_dimensions'], region['rights_url'], region['attribution'], [430,20,1150,420], 'Selected writing provisionally fits Secus pedes domini astans; the end of the preceding text is also in view.'),
      ('I93-10406-tail', cap['path'], cap['url'], cap['sha256'], [cap['width'],cap['height']], obj['rights_url'], obj['attribution'], [110,50,530,135], 'Selected text includes capillis capitis sui tergebat and osculabatur pedes eius et unguento ungebat; its beginning is not visible in this crop.')]
    annotations=[]
    for ident,path,url,expected,dimensions,rights,credit,box,body in specs:
        image_path=ROOT/path
        sha=hashlib.sha256(image_path.read_bytes()).hexdigest()
        assert sha==expected
        with Image.open(image_path) as im:
            assert list(im.size)==dimensions
        x,y,w,h=box
        assert 0<=x<x+w<=dimensions[0] and 0<=y<y+h<=dimensions[1]
        annotations.append({'id':ident,'type':'Annotation','motivation':'describing',
          'body':{'type':'TextualBody','value':body,'language':'en'},
          'target':{'source':path,'selector':{'type':'FragmentSelector','conformsTo':'http://www.w3.org/TR/media-frags/','value':f'xywh={x},{y},{w},{h}'}},
          'fragment_id':'mpo-10407' if '10407' in ident else 'mpo-10406',
          'source_url':url,'sha256':sha,'image_dimensions':dimensions,'rights_url':rights,'attribution':credit,
          'observer':'Codex AI; post-exposure, reference-assisted; 2026-11-03','independent_confirmation':False})
    (HERE/'observations.json').write_text(json.dumps({'version':'1.0.0','annotations':annotations},ensure_ascii=False,indent=2)+'\n')
    result={'date':'2026-11-03','source_regions':[x['id'] for x in annotations],
      'reused_regions':['I54-10407-irregabat','I60-10370-top','I60-10370-sequence'],
      'target_readings':'Fr 10407 provisionally contains Secus pedes and Irrigabat; Fr 10370 preserves the Satagebat passage and the following Non est Martha / Et respondens candidates. Fr 10406 has a similar biblical passage that also occurs at the end of In diebus illis (003224); its opening is unseen.',
      'reference':'https://cantusdatabase.org/chant/402231/',
      'control':'Paris Latin 12044 indexes the same 10407/10370 chant types in this broad order, with several chants and responsories between Irrigabat and Satagebat. This is a different book and its index is not a reading of the Swedish leaves.',
      'conclusion':'Shared standard liturgical sequence is compatible with, but neither unique evidence for, same book nor proof of immediate adjacency. The 10406 tail alone cannot securely identify the work or an edge-to-edge continuation.',
      'same_book_newly_proved':False,'adjacency_proved':False,'novelty_proved':False,'independent_review':False}
    (HERE/'results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'new_regions':len(annotations),'reused_regions':len(result['reused_regions'])}))


if __name__=='__main__':
    main()
