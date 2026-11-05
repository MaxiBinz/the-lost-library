"""Verify E53 source/coverage integrity and scoped state transitions, offline."""
import hashlib
import json
from pathlib import Path

from PIL import Image

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]


def read(path):
    return json.loads((ROOT/path).read_text())


def main():
    p=read('research/continuation_53/protocol.json')
    for path,expected in p['frozen_inputs'].items():
        assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==expected,path
    snap=p['register_before_overlay']
    assert hashlib.sha256((ROOT/snap['path']).read_bytes()).hexdigest()==snap['sha256']
    sources={r['path']:r for r in p['fixed_sources']}
    assert len(sources)==15 and len({r['object_id'] for r in sources.values()})==9
    for path,r in sources.items():
        assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==r['sha256']
        with Image.open(ROOT/path) as im:
            assert im.size==(r['width'],r['height'])
        assert r['medieval_side'] is None
        assert r['rights_url'] in {'http://creativecommons.org/publicdomain/mark/1.0/','http://creativecommons.org/licenses/by/4.0/'}
    v1=read('research/continuation_53/readings.v1.json')
    readings=read('research/continuation_53/readings.v2.json')
    assert readings['regions']==v1['regions'],'Pre-lookup literal candidates/coordinates must remain separate from revised readings'
    assert len(readings['coverage'])==15
    assert {r['path'] for r in readings['coverage']}==sources.keys()
    assert all(r['full_retained_photo_viewed'] and r['medieval_side'] is None for r in readings['coverage'])
    graph=read('data/knowledge.v1.json');evidence={r['annotation_id'] for r in graph['evidence']}
    annotations=read('research/continuation_53/observations.json')['annotations']
    assert len(annotations)==len(readings['regions'])==9
    for a,r in zip(annotations,readings['regions']):
        s=sources[r['path']];x,y,w,h=r['xywh']
        assert a['id']==r['id'] and a['sha256']==s['sha256']
        assert a['literal_candidate']==r['literal'] and a['normalized_candidate'] is None
        assert 0<=x<x+w<=s['width'] and 0<=y<y+h<=s['height']
        assert a['target']['selector']['value']=='xywh='+','.join(map(str,r['xywh']))
        assert a['display_rotation_degrees']==r['display_rotation_degrees'] in {0,180}
        assert a['rights_url']==s['rights_url'] and a['attribution'] and not a['independent_confirmation']
    assert set(readings['prior_layout_regions_reused'])<=evidence
    matrix=read('research/continuation_53/pair_comparisons.json')['comparisons']
    assert len(matrix)==len({r['lead_id'] for r in matrix})==8
    assert {r['lead_id'] for r in matrix}=={r['id'] for r in p['selected_existing_leads']}
    for row in matrix:
        assert row['initial_primary_comparison_recorded'] and row['selected_view_inspection_complete']
        assert row['decision_state']=='unresolved' and set(row['source_regions'])<=evidence
        assert row['local_field_design_difference']==(row['visible_field_counts'][0]!=row['visible_field_counts'][1])
        assert row['complete_source_photo_coverage']==all(row['contexts'][x]['full_manifest_photo_coverage'] for x in row['pair'])
        for key in ['complete_corresponding_diagnostic_work_established','historical_same_codex_excluded','historical_adjudication_complete','independent_confirmation']:
            assert row[key] is False,key
    assert sum(r['local_field_design_difference'] for r in matrix)==5
    result=read('research/continuation_53/results.json')
    assert result['pair_comparisons_recorded']==result['initial_primary_comparisons_recorded']==8
    assert result['source_photo_views_inspected']==15 and result['new_source_files']==0
    assert result['selected_view_inspection_complete']
    for key in ['complete_group_source_photo_coverage','complete_diplomatic_or_music_collation',
                'historical_adjudication_complete','new_codex_attribution','new_historical_exclusion',
                'new_catalogue_correction','novelty_cleared','new_discovery','independent_confirmation',
                'goal_complete','global_blocker_established']:
        assert result[key] is False,key
    before={r['id']:r for r in read(snap['path'])['leads']}
    post=read('research/continuation_54/protocol.json')['register_before_overlay']
    assert hashlib.sha256((ROOT/post['path']).read_bytes()).hexdigest()==post['sha256']
    now={r['id']:r for r in read(post['path'])['leads']}
    live_register=read('data/lead_register.v1.json')
    live={r['id']:r for r in live_register['leads']}
    assert before.keys()==now.keys() and len(now)==168
    old={k for k,r in before.items() if r.get('primary_pair_test_pending')}
    pending={k for k,r in now.items() if r.get('primary_pair_test_pending')}
    assert len(old)==16 and len(pending)==8 and pending<=old
    assert old-pending=={r['lead_id'] for r in matrix}
    live_pending={k for k,r in live.items() if r.get('primary_pair_test_pending')}
    assert live_pending<=pending
    assert all(before[k]['decision_state']==now[k]['decision_state'] for k in before)
    for row in matrix:
        live_row=live[row['lead_id']]
        assert live_row['test_execution'].startswith('E53 direct retained-source comparison')
        assert not live_row['retained_primary_comparison']['historical_adjudication_complete']
    claims={c['id']:c for c in graph['claims']}
    for item in result['candidate_chant_identifications']:
        c=claims['interpretation:E53:'+item['candidate_cantus_id']]
        assert c['predicate']=='chant_identification' and c['candidate_only'] and c['status']=='unresolved'
        assert not c['exact_complete_local_work_confirmed'] and not c['exact_melody_verified']
        assert not c['local_liturgical_position_verified'] and not c['independent_confirmation']
    resource=read('data/resource_audit.json')
    later_captures=read('research/continuation_54/captures.json')['captures']
    later_captures += read('research/continuation_65/captures.json')['captures']
    later_bytes=sum(resource['receipt_subtotals'][k] for k in ['research/continuation_54/download_receipts.json','research/continuation_56/metadata_receipts.json','research/continuation_56/download_receipts.json','research/continuation_65/download_receipt.json'])
    assert result['working_source_files_after']==200
    assert resource['working_source_capture_files']==200+len(later_captures)
    assert result['conservative_transfer_plan_after']==1673000850
    assert resource['conservative_planning_total_bytes']==1673000850+later_bytes+resource['receipt_subtotals']['research/continuation_88/supplement_receipt.json']+resource['receipt_subtotals']['research/continuation_114/download_receipt.json']
    assert not resource['exact_lifetime_transfer_total_verified']
    print(json.dumps({'retained_photo_views_checked':15,'new_regions_checked':9,'limited_pair_comparisons':8,
        'historical_first_comparisons_still_pending':8,'current_first_comparisons_still_pending':len(live_pending),'new_source_files':0,'historical_decisions':'unchanged',
        'scope':'Source/coverage integrity and eight initial-comparison transitions; no independent reading, historical adjudication or scientific novelty.'}))


if __name__=='__main__':
    main()
