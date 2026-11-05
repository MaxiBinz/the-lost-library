"""Record qualified E49 source regions and a PDM-only pixel review figure."""
import hashlib
import json
from pathlib import Path

from PIL import Image,ImageDraw

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]


def read(path):
    return json.loads((ROOT/path).read_text())


def save(name,value):
    (HERE/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')


def main():
    protocol=read('research/continuation_49/protocol.json')
    readings=read('research/continuation_49/manual_readings.json')
    caps={c['path']:c for c in protocol['fixed_sources']}
    annotations=[]
    panels=[]
    for row in readings['regions']:
        c=caps[row['path']]
        assert hashlib.sha256((ROOT/c['path']).read_bytes()).hexdigest()==c['sha256']
        x,y,w,h=row['xywh']
        with Image.open(ROOT/c['path']) as im:
            assert 0<=x<x+w<=im.width and 0<=y<y+h<=im.height
            crop=im.crop((x,y,x+w,y+h)).convert('RGB')
        panels.append((row['id'],crop.resize((w*3,h*3),Image.Resampling.NEAREST)))
        annotations.append({'id':row['id'],'type':'Annotation','motivation':'describing',
            'body':{'type':'TextualBody','value':row['body']+' '+row['status'],'language':'en'},
            'target':{'source':c['path'],'selector':{'type':'FragmentSelector',
                'conformsTo':'http://www.w3.org/TR/media-frags/','value':'xywh='+','.join(map(str,row['xywh']))}},
            'fragment_id':c['object_id'],'source_url':c['url'],'sha256':c['sha256'],
            'image_dimensions':[c['width'],c['height']],'rights_url':c['rights_url'],
            'literal_candidate':row['literal'],'normalized_candidate':row['normalized'],
            'observer':readings['observer'],'independent_confirmation':False,
            'interpretation_limits':readings['limits']})
    save('observations.json',{'version':'1.0.0','date':'2026-10-30','annotations':annotations})
    proof=Image.new('RGB',(max(im.width for _,im in panels)+20,
        sum(im.height+36 for _,im in panels)+30),'white')
    draw=ImageDraw.Draw(proof)
    y=0
    for label,im in panels:
        draw.text((10,y+4),label+' / nearest-neighbour3x; no new manuscript detail',fill='black')
        proof.paste(im,(10,y+26))
        y+=im.height+36
    draw.text((10,y+4),'Reference-exposed provisional readings. Only one complete local Catherine opening is established.',fill='black')
    proof.save(HERE/'rubric-review.png')
    save('results.json',{'version':'1.0.0','date':'2026-10-30','pair':['mpo-8201','mpo-8304'],
        'captures_inspected':8,'source_regions':[a['id'] for a in annotations],
        'direct_result':readings['direct_result'],'interpretation':readings['interpretation'],
        'limits':readings['limits'],'8304_local_opening_supported':True,
        '8201_second_complete_office_opening_established':False,
        'published_duplicate_opening_argument_fully_replicated':False,
        'published_20106_8201_continuity_independently_verified':False,
        'published_rejection_refuted':False,'new_historical_exclusion_established':False,
        'frozen_classification':'D, retained published rejection; no silent review rewrite',
        'source_only_pair_tests_remaining':31,
        'catalogue_access_result':'A legitimate canonical Manuscripta A103 record was found, but describes a36-leaf early psalter and does not explicitly identify Fr20106 or its Catherine opening. The shelfmark match is not a verified physical crosswalk; no images or guessed URLs were acquired.',
        'next_test':'Resolve the exact Fr20106 physical holding/catalogue-image crosswalk or find an explicit source that reproduces its opening. Keep the canonical A103 psalter separate until that link is demonstrated; do not download its corpus merely from a shelfmark coincidence. Continue other existing primary pair tests independently.',
        'new_source_files':0,'retained_file_acquisition_bytes':0,
        'network_accounting':'Web-reader/search traffic unmeasured within the existing planning reserve.',
        'new_discovery':False,'independent_confirmation':False,'goal_complete':False,
        'global_blocker_established':False})
    print(json.dumps({'source_captures_inspected':8,'new_regions':len(annotations),
        'local_complete_openings_established':1,'full_published_argument_replicated':False}))


if __name__=='__main__':
    main()
