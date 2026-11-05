"""Serialize the retained manual source inspection; replay is not new review."""
import hashlib
import json
from pathlib import Path
from PIL import Image,ImageDraw

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]


def save(path,value):
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')


def main():
    inspection=json.loads((HERE/'inspection.v2.json').read_text())
    captures=json.loads((HERE/'captures.json').read_text())['captures']
    records=json.loads((ROOT/'data/fragments.json').read_text())
    descriptors={c['path']:c for c in captures}
    for r in records:
        if r.get('image_path'):
            descriptors[r['image_path']]={**r['image'],'rights_url':r['rights_url'],
                'physical_object_id':r['physical_object_id']}
    sites=[]
    for row in inspection['source_observations']:
        sites.append({**row,'annotation_id':'I44-'+row['id'],'body':row.get('literal_observation',row.get('literal_candidate'))+' '+row['limit']})
    for row in inspection['controls']:
        sites.append({**row,'annotation_id':'I44-'+row['object_id'].removeprefix('mpo-')+'-control-rules',
            'body':row['observation'],'literal_candidate':None})
    annotations=[];panels={}
    for row in sites:
        path=row['path'];descriptor=descriptors[path]
        assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==descriptor['sha256']
        x,y,w,h=row['xywh']
        with Image.open(ROOT/path) as image:
            assert image.size==(descriptor['width'],descriptor['height'])
            assert 0<=x<x+w<=image.width and 0<=y<y+h<=image.height
            panels[row['annotation_id']]=image.crop((x,y,x+w,y+h)).convert('RGB')
        annotations.append({'id':row['annotation_id'],'type':'Annotation','motivation':'describing',
            'body':{'type':'TextualBody','value':row['body'],'language':'en'},
            'target':{'source':path,'selector':{'type':'FragmentSelector',
                'conformsTo':'http://www.w3.org/TR/media-frags/','value':'xywh='+','.join(map(str,row['xywh']))}},
            'fragment_id':descriptor['physical_object_id'],'source_url':descriptor.get('url'),
            'sha256':descriptor['sha256'],'image_dimensions':[descriptor['width'],descriptor['height']],
            'rights_url':descriptor['rights_url'],'literal_candidate':row.get('literal_candidate'),
            'normalized_candidate':None,'observer':'Codex AI exploratory nonblind source reading,2026-10-29',
            'independent_confirmation':False,'interpretation_limits':[
                'Visible ruled lines are not independently certified staff-function or absolute-pitch readings.',
                'No complete same liturgical address, physical join, manuscript-side map, same codex or catalogue correction established.',
                'Catalogue hymn reference does not classify the whole fragment as a hymn book; incomplete words and reference assistance remain explicit.']})
    save(HERE/'observations.json',{'version':'1.1.0','assessment_date':'2026-10-29','inspection_source':'research/continuation_44/inspection.v2.json','annotations':annotations})
    rule_ids=['I44-8066-rules','I44-9620-rules']+[r['annotation_id'] for r in sites if 'control-rules' in r['annotation_id']]
    proof=Image.new('RGB',(1120,510),'white');draw=ImageDraw.Draw(proof)
    for i,ident in enumerate(rule_ids):
        column=i%2;row=i//2;x=column*560+10;y=[5,220,350][row]
        draw.text((x,y),ident+' / raw source pixels',fill='black');proof.paste(panels[ident],(x,y+30))
    draw.text((10,490),'Counts describe selected ruled bands; no same-book or independent notation judgment.',fill='black')
    proof.save(HERE/'ruling-review.png')
    text_ids=[r['annotation_id'] for r in sites if r['annotation_id'] not in rule_ids]
    proof=Image.new('RGB',(1130,sum(panels[i].height+55 for i in text_ids)+45),'white');draw=ImageDraw.Draw(proof);y=0
    for ident in text_ids:
        draw.text((10,y+6),ident+' / separate raw panel; gaps and uncertainty retained',fill='black')
        proof.paste(panels[ident],(10,y+30));y+=panels[ident].height+55
    draw.text((10,y+5),'No physical stitch, complete chant edition or full medieval side is shown.',fill='black')
    proof.save(HERE/'text-review.png')
    receipts=json.loads((HERE/'download_receipts.json').read_text())
    result={'version':'1.1.0','date':'2026-10-29','pair':['mpo-8066','mpo-9620'],
        'primary_sources_inspected':[c['path'] for c in captures],
        'control_sources':[c['path'] for c in inspection['controls']],
        'observations':[a['id'] for a in annotations],
        'direct_result':'The selected8066 and9620 music bands both show five horizontal rules, apparently four dark and one red. The preselected low-resolution control bands also show five rules. The proposed4-versus5 ruling split is not supported by these inspected pixels.',
        'text_result':'Both originals show notated chant. The8066 sequence includes Domum tuam, Domus mea and other church-building texts;9620 includes O quam metuendus and Fundata est domus. Selected words/rubrics are retained with uncertainty. No complete duplicated office opening at one verified liturgical address is demonstrated.',
        'catalogue_note_issue':'8066 and the four selected controls have a source note saying three black and one red line;9620 says four black and one red. All normalized notation fields retain4?. The visible ruled-band count does not follow that proposed split. A counting convention, a separate guide rule or a source-description error remains to be checked; no definitive catalogue correction or first-notice claim.',
        'correction_to_project_framing':inspection['correction_to_E43_framing'],
        'reference_assisted_revision':inspection['reference_assisted_revision'],
        'not_established':['A confirmed catalogue correction or a new scholarly finding','Different book genres or a uniform copying-unit exclusion','The same complete liturgical position or duplicated office opening','Same hand, same codex, physical adjacency, physical join or complete side map','Improved matching or independent confirmation'],
        'pair_state':'unresolved','four_vs_five_split_supported':False,
        'different_book_genres_established':False,'duplicated_complete_opening_established':False,
        'same_codex_established':False,'physical_join_established':False,
        'catalogue_correction_confirmed':False,'novelty_cleared':False,'independent_confirmation':False,
        'new_discovery':False,'new_physical_objects':0,'new_working_source_files':len(captures),
        'new_download_bytes':sum(r['bytes_received'] for r in receipts),
        'scope':'Bounded primary-image text/ruling compatibility check, not a complete diplomatic edition, historical attribution or source-note correction.',
        'next_test':'Map the retained Dedication sequences to source-visible rubric and service positions, keeping the likely Hoc in templo cue and other-witness concordances provisional. Test a duplicated opening only at a verified corresponding position. If no diagnostic overlap survives, record that limit and move to the next existing primary-image pair; do not repeat generic ruling compatibility. Check the outer-rule function/counting convention separately before proposing a catalogue correction.',
        'unchanged_inputs':json.loads((ROOT/'research/continuation_41/results.json').read_text())['unchanged_inputs']}
    save(HERE/'results.json',result)
    print(json.dumps({'regions':len(annotations),'native_captures':len(captures),
        'download_bytes':result['new_download_bytes'],'pair_state':result['pair_state']}))


if __name__=='__main__':
    main()
