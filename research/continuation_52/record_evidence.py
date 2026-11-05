"""Record E52's complete selected-pair matrix and qualified source readings."""
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def read(path):
    return json.loads((ROOT/path).read_text())


def save(name, value):
    (HERE/name).write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n')


def main():
    p = read('research/continuation_52/protocol.json')
    readings = read('research/continuation_52/readings.v3.json')
    caps = read('research/continuation_52/captures.json')['captures']
    sources = {c['path']:c for c in caps + p['retained_group_sources']}
    annotations = []
    for r in readings['new_reading_candidates']:
        c = sources[r['path']]
        raw = (ROOT/r['path']).read_bytes()
        assert hashlib.sha256(raw).hexdigest() == c['sha256']
        with Image.open(ROOT/r['path']) as im:
            dims = list(im.size)
        x,y,w,h = r['xywh']
        assert 0<=x<x+w<=dims[0] and 0<=y<y+h<=dims[1]
        annotations.append({'id':r['id'], 'type':'Annotation', 'motivation':'describing',
            'body':{'type':'TextualBody','value':r['body'],'language':'en'},
            'target':{'source':r['path'],'selector':{'type':'FragmentSelector',
                'conformsTo':'http://www.w3.org/TR/media-frags/','value':'xywh='+','.join(map(str,r['xywh']))}},
            'fragment_id':c.get('physical_object_id',c.get('object_id')), 'source_url':c['url'],
            'sha256':c['sha256'], 'image_dimensions':dims, 'rights_url':c['rights_url'],
            'literal_candidate':r['literal'], 'normalized_candidate':r['normalized'],
            'observer':readings['observer'], 'independent_confirmation':False,
            'interpretation_limits':readings['limits']})
    save('observations.json', {'version':'1.0.0','date':'2026-10-30','annotations':annotations})
    matrix = []
    for lead in p['selected_existing_leads']:
        a,b = lead['pair']
        contexts = {obj:readings['object_summaries'][obj] for obj in [a,b]}
        matrix.append({'lead_id':lead['id'], 'pair':[a,b],
            'comparison_scope':'First direct group-context comparison: actual surviving text/rubrics and copying layout; not a complete same-position text/music collation or historical adjudication.',
            'contexts':contexts,
            'primary_regions':list(dict.fromkeys(i for obj in [a,b] for i in contexts[obj]['regions'])),
            'sampled_rule_counts':[contexts[a]['sampled_staff_rules'],contexts[b]['sampled_staff_rules']],
            'known_wrong_control_also_shares_sampled_layout':True,
            'layout_discriminates_book_identity':False,
            'complete_corresponding_diagnostic_passage_established':False,
            'secure_join_or_original_address_established':False,
            'text_result':'The selected surviving contexts do not establish a complete corresponding diagnostic passage. Different feasts/genres and shared generic cues do not exclude one book. This is not an exhaustive chant census or a claim of no possible correspondence.',
            'all_planned_photo_views_inspected':'mpo-8072' not in [a,b],
            'requested_native_coverage_complete':not {'mpo-8072','mpo-8073'} & {a,b},
            'initial_primary_comparison_recorded':True, 'historical_adjudication_complete':False,
            'decision_state':'unresolved', 'independent_confirmation':False,
            'next_test':'Establish the exact chant/work/service correspondence before comparing distinctive text/music; alternatively obtain secure physical/quire evidence. Generic layout is exhausted as a discriminant in this group. The missing8072 view remains a documented gap, not counterevidence.'})
    save('pair_comparisons.json', {'version':'1.0.0','date':'2026-10-30','comparisons':matrix,
        'fixed_controls':[{'pair':['mpo-8201','mpo-8304'],'scope':'Published same-hand/different-book control; five rules and broad copying field are shared. Published rejection is retained, not independently re-proved.'},
                          {'pair':['mpo-8066','mpo-9620'],'scope':'Earlier unresolved direct comparison; similar Jacob wording probably represents different related items. E44-E46 result retained without promotion.'}],
        'scope':'All13 previously source-only pair edges in the fixed six-object group are reported, plus both previously studied control edges. No cherry-picked survivor or new candidate.'})
    # Only local manuscript pixels; the figure does not reconstruct a page,
    # import reference notes or normalize a difficult source reading.
    ids = ['I52-8072-veni','I52-8072-veni-response','I52-8073-magnificat-rubric','I52-8073-unnotated-verses']
    by = {r['id']:r for r in readings['new_reading_candidates']}
    proof = Image.new('RGB',(1420,1690),'white'); draw = ImageDraw.Draw(proof)
    y=8
    for ident in ids:
        r=by[ident];x0,y0,w,h=r['xywh']
        draw.text((10,y),ident+' - native source crop, nearest-neighbour fit',fill='black')
        with Image.open(ROOT/r['path']) as im:
            crop=im.crop((x0,y0,x0+w,y0+h)).convert('RGB')
        scale=min(1380/crop.width,410/crop.height)
        crop=crop.resize((round(crop.width*scale),round(crop.height*scale)),Image.Resampling.NEAREST)
        proof.paste(crop,(10,y+22));y+=crop.height+48
    draw.text((10,1640),'Two Veni incipits have different continuations/settings. Candidate work IDs are reference-assisted, not new discoveries.',fill='black')
    draw.text((10,1658),'8073 mixes a Magnificat antiphon rubric with continuous verses. No original foliation, join or codex decision.',fill='black')
    proof.save(HERE/'text-review.png')
    byte_total=sum(r['bytes_received'] for r in read('research/continuation_52/download_receipts.json'))
    result={'version':'1.0.0','date':'2026-10-30','selected_existing_leads':[r['lead_id'] for r in matrix],
        'pair_comparisons_recorded':len(matrix), 'new_source_regions':[a['id'] for a in annotations],
        'prior_rule_regions_reused':readings['prior_rule_observations_reused'],
        'candidate_chant_identifications':readings['reference_candidates'],
        'direct_result':'24 distinct source photo views of the six existing Ant49 objects were inspected. The13 previously source-only group edges now have limited direct context/layout comparisons. Five-rule/broad-field resemblance also occurs in the known wrong pair and cannot assign membership.8072 repeats Veni sponsa with two different continuations/settings;8073 has a Magnificat antiphon rubric alongside continuous verse blocks.',
        'interpretation':'Neither shared general layout nor different liturgical sections provides a new same-book or different-book result. The two8072 settings provisionally fit known antiphon/responsory works, so matching an incipit is insufficient before function/context is established. All13 historical decisions remain unresolved.',
        'source_photo_views_inspected':len(readings['coverage']), 'new_source_files':len(caps),
        'confirmed_successful_transfer_bytes':sum(c['bytes'] for c in caps),
        'logged_transfer_bytes':byte_total,'working_source_files_after':194+len(caps),
        'conservative_transfer_plan_after':1671104323+byte_total,
        'all_planned_group_photo_views_inspected':False, 'primary_group_test_completed':False,
        'missing_view':'8072 capture3 timed out and remains unseen;8073 capture1 native timed out, but its retained800px thumbnail was inspected. Neither URL was retried.',
        'primary_pair_tests_still_pending':29-len(matrix),
        'initial_primary_comparisons_recorded':len(matrix), 'historical_adjudication_complete':False,
        'full_diplomatic_or_music_collation_completed':False,
        'new_codex_attribution':False,'new_historical_exclusion':False,'new_catalogue_correction':False,
        'novelty_cleared':False,'new_discovery':False,'independent_confirmation':False,
        'goal_complete':False,'global_blocker_established':False,
        'next_test':'Proceed to the16 existing pairs without an initial direct comparison. For Ant49, stop generic layout comparisons; further discrimination needs exact corresponding work/service or physical/quire evidence. Detailed8073 work identification and the missing20106 source remain separate actionable lines; do not repeat failed image/record routes.'}
    save('results.json',result)
    print(json.dumps({'pair_comparisons':len(matrix),'new_regions':len(annotations),'new_source_files':len(caps),
        'confirmed_bytes':result['confirmed_successful_transfer_bytes'],'source_photo_views_inspected':len(readings['coverage']),
        'first_comparisons_still_pending':result['primary_pair_tests_still_pending'],'historical_decisions':'unchanged/unresolved'}))


if __name__=='__main__':
    main()
