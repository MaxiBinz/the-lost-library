"""Check E52 source provenance, complete pair coverage and inferential limits.

No network or independent historical/paleographic adjudication.
"""
import hashlib
import json
from pathlib import Path

from PIL import Image

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]


def read(path):
    return json.loads((ROOT/path).read_text())


def main():
    p=read('research/continuation_52/protocol.json')
    for path,expected in p['frozen_inputs'].items():
        assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==expected,path
    snap=p['register_before_overlay']
    assert hashlib.sha256((ROOT/snap['path']).read_bytes()).hexdigest()==snap['sha256']
    receipts=read('research/continuation_52/download_receipts.json')
    caps=read('research/continuation_52/captures.json')['captures']
    assert len(receipts)==len({r['url'] for r in receipts})==8
    assert {r['url'] for r in receipts}=={r['url'] for r in p['requested_sources']}
    assert len(caps)==sum(bool(r['saved']) for r in receipts)==6
    assert not any(r['retry'] for r in receipts)
    assert sum(c['bytes'] for c in caps)==sum(r['bytes_received'] for r in receipts)==1896527
    assert sum(r['bytes_received'] for r in receipts)<=p['acquisition_bounds']['maximum_total_bytes']
    assert all(r['bytes_received']<=p['acquisition_bounds']['maximum_bytes_per_response'] for r in receipts)
    failed={r['url'] for r in receipts if not r['saved']}
    assert failed=={'https://lbiiif.riksarkivet.se/arkis!R1008072_00003/full/max/0/default.jpg',
                    'https://lbiiif.riksarkivet.se/arkis!R1008073_00001/full/max/0/default.jpg'}
    for c in caps:
        raw=(ROOT/c['path']).read_bytes()
        assert len(raw)==c['bytes'] and hashlib.sha256(raw).hexdigest()==c['sha256']
        with Image.open(ROOT/c['path']) as im:
            assert im.format=='JPEG' and im.size==(c['width'],c['height'])
        request=next(r for r in p['requested_sources'] if r['url']==c['url'])
        assert hashlib.sha256((ROOT/c['manifest']).read_bytes()).hexdigest()==request['manifest_sha256']
        m=read(c['manifest']);value=m
        for key in c['manifest_locator'].split('/'):
            value=value[int(key)] if isinstance(value,list) else value[key]
        assert value==c['url'] and c['side_assignment'] is None
        rights=next(r['value']['none'][0] for r in m['metadata'] if 'Rights' in r['label'].get('en',[]))
        assert c['rights_url']==rights=='http://creativecommons.org/publicdomain/mark/1.0/'
    readings=read('research/continuation_52/readings.v3.json')
    v1=read('research/continuation_52/readings.v1.json')
    assert v1['new_reading_candidates']==readings['new_reading_candidates'][:4]
    coverage=readings['coverage']
    assert len(coverage)==len({c['path'] for c in coverage})==24
    assert all(c['full_photo_viewed'] and c['medieval_side'] is None for c in coverage)
    assert not any(c['object_id']=='mpo-8072' and c['source_capture_index']==2 for c in coverage)
    assert any(c['object_id']=='mpo-8073' and c['path']=='data/images/mpo-8073.jpg' for c in coverage)
    for c in p['retained_group_sources']+p['fallback_first_thumbnails']:
        assert hashlib.sha256((ROOT/c['path']).read_bytes()).hexdigest()==c['sha256']
    expected={c['path'] for c in caps+p['retained_group_sources']}|{'data/images/mpo-8073.jpg'}
    assert {c['path'] for c in coverage}==expected
    annotations=read('research/continuation_52/observations.json')['annotations']
    assert len(annotations)==len(readings['new_reading_candidates'])==7
    for a,r in zip(annotations,readings['new_reading_candidates']):
        assert a['id']==r['id'] and a['literal_candidate']==r['literal']
        assert a['normalized_candidate'] is None and not a['independent_confirmation']
        assert hashlib.sha256((ROOT/r['path']).read_bytes()).hexdigest()==a['sha256']
        x,y,w,h=r['xywh']
        with Image.open(ROOT/r['path']) as im:
            assert a['image_dimensions']==list(im.size)
            assert 0<=x<x+w<=im.width and 0<=y<y+h<=im.height
        assert a['target']['selector']['value']=='xywh='+','.join(map(str,r['xywh']))
    matrix=read('research/continuation_52/pair_comparisons.json')['comparisons']
    assert len(matrix)==len({r['lead_id'] for r in matrix})==13
    assert {r['lead_id'] for r in matrix}=={r['id'] for r in p['selected_existing_leads']}
    graph=read('data/knowledge.v1.json');evidence={e['annotation_id'] for e in graph['evidence']}
    assert set(readings['prior_rule_observations_reused'])<=evidence
    assert len(readings['prior_rule_observations_reused'])==6
    for row in matrix:
        assert set(row['pair'])<=set(p['fixed_objects']) and len(row['pair'])==2
        assert set(row['primary_regions'])<=evidence
        assert row['sampled_rule_counts']==[5,5] and row['known_wrong_control_also_shares_sampled_layout']
        assert row['initial_primary_comparison_recorded'] and row['decision_state']=='unresolved'
        for key in ['layout_discriminates_book_identity','complete_corresponding_diagnostic_passage_established',
                    'secure_join_or_original_address_established','historical_adjudication_complete','independent_confirmation']:
            assert row[key] is False,key
        assert row['all_planned_photo_views_inspected']==('mpo-8072' not in row['pair'])
    result=read('research/continuation_52/results.json')
    assert result['source_photo_views_inspected']==24 and result['new_source_files']==6
    assert result['pair_comparisons_recorded']==result['initial_primary_comparisons_recorded']==13
    for key in ['all_planned_group_photo_views_inspected','primary_group_test_completed',
                'historical_adjudication_complete','full_diplomatic_or_music_collation_completed',
                'new_codex_attribution','new_historical_exclusion','new_catalogue_correction',
                'novelty_cleared','new_discovery','independent_confirmation','goal_complete','global_blocker_established']:
        assert result[key] is False,key
    before={r['id']:r for r in read(snap['path'])['leads']}
    live_register=read('data/lead_register.v1.json')
    snapshot='research/continuation_53/lead_register.before.json'
    if (ROOT/snapshot).exists():
        pinned=read('research/continuation_53/protocol.json')['register_before_overlay']
        assert hashlib.sha256((ROOT/snapshot).read_bytes()).hexdigest()==pinned['sha256']
        historical=read(snapshot)
    else:
        historical=live_register
    now={r['id']:r for r in historical['leads']}
    assert before.keys()==now.keys() and len(now)==168
    old_pending={k for k,v in before.items() if v.get('primary_pair_test_pending')}
    pending={k for k,v in now.items() if v.get('primary_pair_test_pending')}
    assert len(old_pending)==29 and len(pending)==16 and pending<=old_pending
    assert old_pending-pending=={r['lead_id'] for r in matrix}
    assert all(before[k]['decision_state']==now[k]['decision_state'] for k in before)
    live_pending={r['id'] for r in live_register['leads'] if r.get('primary_pair_test_pending')}
    assert live_pending<=pending
    for row in matrix:
        live=now[row['lead_id']]
        assert live['test_execution'].startswith('E52 direct Ant49 group-context comparison')
        assert not live['group_primary_comparison']['historical_adjudication_complete']
    claims={c['id']:c for c in graph['claims']}
    for item in result['candidate_chant_identifications']:
        c=claims['interpretation:E52:'+item['cantus_id']]
        assert c['predicate']=='chant_identification' and c['status']=='unresolved' and c['candidate_only']
        assert not c['exact_melody_verified'] and not c['local_liturgical_position_verified']
    c=claims['observation:E52-two-occurrences']
    assert c['predicate']=='melodic_excerpt_comparison' and not c['same_chant_item_established']
    assert not c['exact_pitch_intervals_transcribed'] and not c['historical_book_decision']
    c=claims['observation:E52-mixed-blocks']
    assert c['predicate']=='describes' and not c['whole_book_genre_assigned'] and not c['historical_book_decision']
    resource=read('data/resource_audit.json')
    later_captures=read('research/continuation_54/captures.json')['captures']
    later_captures += read('research/continuation_65/captures.json')['captures']
    later_bytes=sum(resource['receipt_subtotals'][k] for k in ['research/continuation_54/download_receipts.json','research/continuation_56/metadata_receipts.json','research/continuation_56/download_receipts.json','research/continuation_65/download_receipt.json'])
    assert result['working_source_files_after']==200
    assert resource['working_source_capture_files']==200+len(later_captures)
    assert resource['receipt_subtotals']['research/continuation_52/download_receipts.json']==1896527
    assert result['conservative_transfer_plan_after']==1673000850
    assert resource['conservative_planning_total_bytes']==1673000850+later_bytes+resource['receipt_subtotals']['research/continuation_88/supplement_receipt.json']+resource['receipt_subtotals']['research/continuation_114/download_receipt.json']
    assert not resource['exact_lifetime_transfer_total_verified']
    print(json.dumps({'checked_source_files':6,'confirmed_saved_bytes':1896527,'unretried_timeouts':2,
        'new_regions_checked':7,'prior_rule_regions_reused':6,'limited_pair_comparisons':13,
        'historical_first_comparisons_still_pending':16,'current_first_comparisons_still_pending':len(live_pending),
        'historical_decisions':'unchanged',
        'scope':'Source provenance and complete selected-pair coverage; no independent source reading, book adjudication or scientific novelty.'}))


if __name__=='__main__':
    main()
