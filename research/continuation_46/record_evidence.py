"""Record source regions and PDM-only figures from retained E46 readings."""
import hashlib
import json
from pathlib import Path
from PIL import Image,ImageDraw

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]


def save(name,value):
    (HERE/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')


def main():
    readings=json.loads((HERE/'readings.v2.json').read_text())
    compared=json.loads((HERE/'comparison.json').read_text())
    caps={c['path']:c for c in json.loads((ROOT/'research/continuation_44/captures.json').read_text())['captures']}
    sites=[]
    for key,s in readings['sources'].items():
        count=s['celos_visible_head_count']
        sites.append({'id':f'I46-{key}-music-window','path':s['path'],'xywh':s['window_xywh'],
            'source_key':key,'literal':'celos tangebat et',
            'body':f'The selected celos word span has {count} candidate noteheads. Labels refer to manual pixel locations, not absolute pitches. The tan sign in8066 has uncertain segmentation; no full same-work melodic variant is established.'})
    for key,box in [('8066',[260,0,250,150]),('9620',[340,1310,240,210])]:
        sites.append({'id':f'I46-{key}-left-sign','path':readings['sources'][key]['path'],'xywh':box,
            'source_key':None,'literal':None,
            'body':'The actual left-of-system signs and rules were inspected. The8066 field is partly cut by the photograph/fold;9620 retains C-shaped and lower tail-like signs. Exact clef/rule interpretation and absolute pitches remain unverified, rather than copied from a reference.'})
    sites += [
        {'id':'I46-8066-verse-end','path':readings['sources']['8066']['path'],'xywh':[280,150,1070,390],
         'source_key':None,'literal':'[...] descendentes et ascendentes per eam [a]it. Gloria patri [...]',
         'body':'The local Jacob passage continues with descending/ascending angels and per eam ait, followed by Gloria patri. This supports a provisional responsory-verse interpretation; the exact parent work and007763zd assignment remain qualified.'},
        {'id':'I46-9620-ending','path':readings['sources']['9620']['path'],'xywh':[350,1550,530,155],
         'source_key':None,'literal':'dixit uere locus iste sa[...]',
         'body':'Closer reference-exposed source inspection supports dixit, replacing E45\'s uncertain pxit. The preserved ending supports candidate antiphon005415; missing text after sa is not restored and the local service position is not imported.'}
    ]
    annotations=[];panels=[]
    for row in sites:
        cap=caps[row['path']];raw=(ROOT/row['path']).read_bytes()
        assert hashlib.sha256(raw).hexdigest()==cap['sha256']
        x,y,w,h=row['xywh']
        with Image.open(ROOT/row['path']) as im:
            assert 0<=x<x+w<=im.width and 0<=y<y+h<=im.height
            crop=im.crop((x,y,x+w,y+h)).convert('RGB')
        panel=crop.resize((w*2,h*2),Image.Resampling.NEAREST)
        if row['source_key']:
            d=ImageDraw.Draw(panel);source=readings['sources'][row['source_key']]
            for e in source['events']+source['optional_events']:
                px,py=e['pixel'];cx,cy=(px-x)*2,(py-y)*2
                colour='#225da8' if e['counted_as_candidate_notehead'] else '#bf6b00'
                d.ellipse((cx-9,cy-9,cx+9,cy+9),outline=colour,width=2)
                d.text((cx+10,cy-16),e['id'],fill=colour)
        panels.append(panel)
        annotations.append({'id':row['id'],'type':'Annotation','motivation':'describing',
            'body':{'type':'TextualBody','value':row['body'],'language':'en'},
            'target':{'source':row['path'],'selector':{'type':'FragmentSelector',
                'conformsTo':'http://www.w3.org/TR/media-frags/','value':'xywh='+','.join(map(str,row['xywh']))}},
            'fragment_id':cap['physical_object_id'],'source_url':cap['url'],'sha256':cap['sha256'],
            'image_dimensions':[cap['width'],cap['height']],'rights_url':cap['rights_url'],
            'literal_candidate':row['literal'],'normalized_candidate':None,
            'observer':readings['observer'],'independent_confirmation':False,
            'interpretation_limits':readings['limits'],'note_position_record':'research/continuation_46/readings.v2.json'})
    save('observations.json',{'version':'1.0.0','assessment_date':'2026-10-29','annotations':annotations})
    for filename,indices in [('note-review.png',range(4)),('context-review.png',range(4,6))]:
        proof=Image.new('RGB',(max(panels[i].width for i in indices)+20,
                              sum(panels[i].height+42 for i in indices)+44),'white')
        d=ImageDraw.Draw(proof);y=0
        for i in indices:
            d.text((10,y+6),sites[i]['id']+' / nearest-neighbour2x; no new manuscript detail',fill='black')
            proof.paste(panels[i],(10,y+28));y+=panels[i].height+42
        d.text((10,y+4),'Blue: provisional candidate heads. Orange: unresolved segmentation. No verified same-chant variant or book exclusion.',fill='black')
        proof.save(HERE/filename)
    result={'version':'1.0.0','date':'2026-10-29','pair':['mpo-8066','mpo-9620'],
        'scope':'Two fixed surviving phrase windows, head grouping and qualified work/context identification; incomplete interval transcription.',
        'observations':[a['id'] for a in annotations],
        'result':'The selected celos window has five candidate heads in8066 and two in9620. A nominal tan/ge direction contrast fails wider sensitivity. The reference-assisted endings point to a responsory verse and an antiphon rather than a securely aligned pair of the same complete chant. No diagnostic melodic variant or book decision follows.',
        'candidate_identifications':readings['context_recheck']['candidate_identifications'],
        'local_visible_head_group_difference':True,'same_complete_chant_identification_established':False,
        'diagnostic_melodic_variant_established':False,'robust_direction_contrast':compared['robust_direction_contrast'],
        'melodic_identity_established':False,'absolute_pitches_verified':False,
        'same_codex_established':False,'different_codex_established':False,'physical_join_established':False,
        'catalogue_correction_confirmed':False,'novelty_cleared':False,'independent_confirmation':False,'new_discovery':False,
        'pair_state':'unresolved','new_working_source_files':0,'new_recorded_file_download_bytes':0,
        'web_reader_transfer_bytes':None,'limits':readings['limits'],
        'pair_next_test':'Validate the candidate work/verse identifications against the retained full context. Further book inference needs a genuinely corresponding distinctive variant or physical/quire evidence; do not repeat same-setting comparisons of provisionally different chant items.',
        'next_action':'Audit actual published-source coverage for the six existing Aboense control objects and13 metadata-only Codex1104 pairings, keeping mere shared catalogue label distinct from documented reconstruction membership. This is source credit, not a prospective new codex; then prioritize an existing discovery lead with discriminating source evidence.',
        'unchanged_inputs':json.loads((HERE/'protocol.json').read_text())['frozen_inputs']}
    save('results.json',result)
    print(json.dumps({'regions':len(annotations),'candidate_centres':compared['candidate_primary_centres'],
        'uncertain_centres':compared['optional_uncertain_centres'],'pair_state':'unresolved'}))


if __name__=='__main__':
    main()
