"""Record E53's retained-source comparisons; no acquisitions or score changes."""
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
    p=read('research/continuation_53/protocol.json')
    readings=read('research/continuation_53/readings.v2.json')
    sources={s['path']:s for s in p['fixed_sources']}
    records={r['id']:r for r in read('data/fragments.json')}
    annotations=[]
    for r in readings['regions']:
        c=sources[r['path']]
        assert hashlib.sha256((ROOT/r['path']).read_bytes()).hexdigest()==c['sha256']
        x,y,w,h=r['xywh']
        assert 0<=x<x+w<=c['width'] and 0<=y<y+h<=c['height']
        record=records[c['object_id']]
        attribution=c['attribution'] or ('Source institution: '+record['raw']['Collection Name']+'; Fragmentarium '+record['raw']['Fragmentarium ID'])
        annotations.append({'id':r['id'],'type':'Annotation','motivation':'describing',
            'body':{'type':'TextualBody','value':r['body'],'language':'en'},
            'target':{'source':r['path'],'selector':{'type':'FragmentSelector',
                'conformsTo':'http://www.w3.org/TR/media-frags/','value':'xywh='+','.join(map(str,r['xywh']))}},
            'fragment_id':c['object_id'],'source_url':c['url'],'sha256':c['sha256'],
            'image_dimensions':[c['width'],c['height']],'rights_url':c['rights_url'],'attribution':attribution,
            'literal_candidate':r['literal'],'normalized_candidate':r['normalized'],
            'display_rotation_degrees':r['display_rotation_degrees'],
            'observer':readings['observer'],'independent_confirmation':False,
            'interpretation_limits':readings['limits']})
    save('observations.json',{'version':'1.0.0','date':'2026-10-30','annotations':annotations})
    matrix=[]
    for l in p['selected_existing_leads']:
        a,b=l['pair'];objects=readings['object_summaries']
        hymn_pair={a,b}=={'mpo-10349','mpo-25592'}
        different_columns=objects[a]['columns_visible']!=objects[b]['columns_visible']
        matrix.append({'lead_id':l['id'],'pair':[a,b],
            'comparison_scope':'Initial direct comparison of selected surviving text/service and copying-field context; no full diagnostic variant collation or historical book adjudication.',
            'contexts':{x:objects[x] for x in [a,b]},
            'source_regions':list(dict.fromkeys(i for x in [a,b] for i in objects[x]['regions'])),
            'visible_field_counts':[objects[a]['columns_visible'],objects[b]['columns_visible']],
            'local_field_design_difference':different_columns,
            'unchanged_uniform_template_challenged':different_columns,
            'complete_source_photo_coverage':all(objects[x]['full_manifest_photo_coverage'] for x in [a,b]),
            'selected_view_inspection_complete':True,'initial_primary_comparison_recorded':True,
            'hymn_comparison':readings['hymn_comparison'] if hymn_pair else None,
            'complete_corresponding_diagnostic_work_established':False,
            'historical_same_codex_excluded':False,'historical_adjudication_complete':False,
            'decision_state':'unresolved','independent_confirmation':False,
            'limits':'Different sections, copying changes and composite volumes remain alternatives. Equal column counts or standard liturgical text are compatibility only. Incomplete photo/text coverage is not evidence of absence.',
            'next_test':('Establish exact whole-hymn/work identity and a genuinely corresponding diagnostic variant before comparing music. The currently selected openings probably belong to different known works; do not repeat a generic Jesu-word match.' if hymn_pair else
                'Seek a securely corresponding text/work sequence or original physical/quire feature. Retain source-photo gaps and section/composite alternatives; generic genre/layout alone cannot adjudicate the book.')})
    save('pair_comparisons.json',{'version':'1.0.0','date':'2026-10-30','comparisons':matrix,
        'source_controls':p['controls'],'scope':'All eight selected existing edges; controls and source assertions remain attributed separately.'})
    # PDM manuscript pixels only. The CC BY Beauvais sources stay linked at
    # their exact original source regions, with institution/rights attribution.
    figure_ids=['I53-10349-jesu','I53-25592-jesu','I53-25592-a-patre']
    regions={r['id']:r for r in readings['regions']}
    proof=Image.new('RGB',(1500,700),'white');draw=ImageDraw.Draw(proof)
    for i,ident in enumerate(figure_ids):
        r=regions[ident];x,y,w,h=r['xywh']
        draw.text((i*500+8,8),ident+'; source pixels',fill='black')
        with Image.open(ROOT/r['path']) as im:
            crop=im.crop((x,y,x+w,y+h)).convert('RGB')
        scale=min(480/crop.width,560/crop.height)
        crop=crop.resize((round(crop.width*scale),round(crop.height*scale)),Image.Resampling.NEAREST)
        proof.paste(crop,(i*500+8,35))
    draw.text((10,625),'Source candidates are qualified; post-reference reading is preserved separately. Similar Jesu words are not a diagnostic same-work variant.',fill='black')
    draw.text((10,646),'No reference music, generated detail, historical book decision, original-side assignment or scientific novelty.',fill='black')
    proof.save(HERE/'hymn-review.png')
    save('results.json',{'version':'1.0.0','date':'2026-10-30',
        'selected_existing_leads':[r['lead_id'] for r in matrix], 'pair_comparisons_recorded':len(matrix),
        'new_source_regions':[a['id'] for a in annotations],
        'candidate_chant_identifications':readings['reference_assisted_recheck'],
        'direct_result':'15 retained photo views support limited direct comparisons of eight existing Hy49/Fr10349-related pairs. The four Codex434 first views and25173 have one broad field versus10349/Hy49 two-field layouts; this challenges an unchanged uniform copying design, not every historical same-volume explanation. Beauvais Mass cues and Hy49 hymn blocks are locally visible.',
        'hymn_result':readings['hymn_comparison'], 'prior_art_countercheck':readings['prior_art_countercheck'],
        'interpretation':'No secure corresponding diagnostic text, unique address or physical join establishes a new book relationship. Similar hymns provisionally belong to different known works. Published source memberships, ordinary layout compatibility and section/composite alternatives remain distinct.',
        'source_photo_views_inspected':len(readings['coverage']), 'new_source_files':0,
        'working_source_files_after':200, 'conservative_transfer_plan_after':1673000850,
        'selected_view_inspection_complete':True,'complete_group_source_photo_coverage':False,
        'complete_diplomatic_or_music_collation':False,'historical_adjudication_complete':False,
        'initial_primary_comparisons_recorded':len(matrix),'primary_pair_tests_still_pending':16-len(matrix),
        'decision_state':'unresolved','new_codex_attribution':False,'new_historical_exclusion':False,
        'new_catalogue_correction':False,'novelty_cleared':False,'new_discovery':False,
        'independent_confirmation':False,'goal_complete':False,'global_blocker_established':False,
        'next_test':'Inspect the remaining eight existing original-target/Ant39 pairs, prioritizing secure original marks and actual text context. E53 does not exhaust higher-resolution/full-side or exact-work work; retain those specific gaps without repeating generic layout or Jesu-incpit screens.'})
    print(json.dumps({'limited_pair_comparisons':len(matrix),'retained_photo_views':len(readings['coverage']),
        'source_regions':len(annotations),'first_comparisons_still_pending':16-len(matrix),
        'new_source_files':0,'historical_decisions':'unchanged/unresolved'}))


if __name__=='__main__':
    main()
