"""Check E50 acquisition/source integrity, arithmetic, scope and one tested pair."""
import hashlib
import json
import math
from pathlib import Path

from PIL import Image

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]


def read(path):
    return json.loads((ROOT/path).read_text())


def main():
    p=read('research/continuation_50/primary_protocol.json')
    for path,expected in p['frozen_inputs'].items():
        assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==expected,path
    before_path=p['register_before_overlay']['path']
    assert hashlib.sha256((ROOT/before_path).read_bytes()).hexdigest()==p['register_before_overlay']['sha256']
    receipts=read('research/continuation_50/download_receipts.json')
    captures=read('research/continuation_50/captures.json')['captures']
    assert len(receipts)==8 and len({r['url'] for r in receipts})==8
    assert {r['url'] for r in receipts}=={r['url'] for r in p['requested_sources']}
    assert not any(r['retry'] for r in receipts)
    assert len(captures)==sum(bool(r['saved']) for r in receipts)==6
    assert sum(c['bytes'] for c in captures)==1542176
    assert sum(r['bytes_received'] for r in receipts)<=p['acquisition_bounds']['maximum_total_bytes']
    for c in captures:
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
        assert c['rights_url']=='http://creativecommons.org/publicdomain/mark/1.0/'
    readings=read('research/continuation_50/manual_readings.json')
    assert len(readings['coverage'])==9 and len({r['path'] for r in readings['coverage']})==9
    assert all(r['complete_capture_viewed'] and r['medieval_side'] is None for r in readings['coverage'])
    assert readings['missing_source_view']['capture_index']==3
    assert not any(r['object_id']=='mpo-2862' and r['capture_index']==3 for r in readings['coverage'])
    assert not next(r for r in receipts if 'R1002862_00003' in r['url'])['saved']
    assert not next(r for r in receipts if 'R1010349_00001' in r['url'])['saved']
    annotations=read('research/continuation_50/observations.json')['annotations']
    assert len(annotations)==len(readings['regions'])==8
    for a,r in zip(annotations,readings['regions']):
        assert a['id']==r['id'] and a['target']['source']==r['path']
        assert hashlib.sha256((ROOT/r['path']).read_bytes()).hexdigest()==a['sha256']
        x,y,w,h=r['xywh']
        with Image.open(ROOT/r['path']) as im:
            assert 0<=x<x+w<=im.width and 0<=y<y+h<=im.height
        assert a['target']['selector']['value']=='xywh='+','.join(map(str,r['xywh']))
        assert not a['independent_confirmation']
    comparison=read('research/continuation_50/field_comparison.json')
    for src,out in zip(readings['field_measurements'],comparison['measurements']):
        (x0,c0),(x1,c1)=src['ruler_x_cm']
        expected=abs(src['field_x_bounds'][1]-src['field_x_bounds'][0])/abs(x1-x0)*abs(c1-c0)
        assert math.isclose(expected,out['nominal_field_width_cm'],abs_tol=1e-12)
    assert [r['endpoint_tolerance_px'] for r in comparison['sensitivity_comparison']]==[10,20,30,40,50]
    assert all(r['ranges_separate'] for r in comparison['sensitivity_comparison'])
    assert comparison['sensitivity_comparison'][-1]['ranges_separate_with_additional_scale'] is False
    result=read('research/continuation_50/results.json')
    assert result['primary_pair_test_executed'] and result['initial_primary_comparison_recorded']
    assert not result['primary_pair_test_completed'] and not result['all_planned_target_views_inspected']
    for key in ['original_leaf_fold_map_established','historical_same_codex_excluded',
        'uniform_layout_unconditionally_excluded','catalogue_correction_established',
        'new_discovery','independent_confirmation','goal_complete','global_blocker_established']:
        assert result[key] is False,key
    before={l['id']:l for l in read(before_path)['leads']}
    live_register=read('data/lead_register.v1.json')
    snapshot='research/continuation_51/lead_register.before.json'
    if (ROOT/snapshot).exists():
        pinned=read('research/continuation_51/primary_protocol.json')['register_before_overlay']
        assert hashlib.sha256((ROOT/snapshot).read_bytes()).hexdigest()==pinned['sha256']
        current=read(snapshot)
    else:
        current=live_register
    now={l['id']:l for l in current['leads']}
    assert before.keys()==now.keys() and len(now)==168
    old_pending={k for k,v in before.items() if v.get('primary_pair_test_pending')}
    new_pending={k for k,v in now.items() if v.get('primary_pair_test_pending')}
    assert len(old_pending)==31 and len(new_pending)==30
    assert old_pending-new_pending=={result['selected_lead']} and new_pending<=old_pending
    assert all(before[k]['decision_state']==now[k]['decision_state'] for k in before)
    live_pending={l['id'] for l in live_register['leads'] if l.get('primary_pair_test_pending')}
    assert live_pending<=new_pending
    live_pair=next(l for l in live_register['leads'] if l['id']==result['selected_lead'])
    assert not live_pair['primary_pair_test_pending'] and live_pair['decision_state']=='unresolved'
    assert live_pair['primary_pair_test_execution_state'].startswith('Partial;')
    assert now[result['selected_lead']]['decision_state']=='unresolved'
    assert now[result['selected_lead']]['test_execution'].startswith('E50 direct visible-layout test')
    graph=read('data/knowledge.v1.json')
    claim=next(c for c in graph['claims'] if c['id']=='observation:E50-layout')
    assert claim['predicate']=='stylistic_similarity' and claim['polarity']=='negative'
    assert not claim['historical_same_codex_excluded'] and not claim['uniform_layout_unconditionally_excluded']
    assert claim['post_inspection_measurements'] and claim['wider_scale_sensitivity_overlaps']
    entities={e['id']:e for e in graph['entities']}
    for c in captures:
        assert entities['image:'+c['path']]['sha256']==c['sha256']
    resource=read('data/resource_audit.json')
    later_captures=read('research/continuation_52/captures.json')['captures'] if (ROOT/'research/continuation_52/captures.json').exists() else []
    later_captures += read('research/continuation_54/captures.json')['captures']
    later_captures += read('research/continuation_65/captures.json')['captures']
    assert resource['working_source_capture_files']==194+len(later_captures)
    assert result['conservative_transfer_plan_after']==1671072950
    later=sum(v for k,v in resource['receipt_subtotals'].items() if k in {'research/continuation_51/metadata_receipts.json','research/continuation_52/download_receipts.json','research/continuation_54/download_receipts.json','research/continuation_56/metadata_receipts.json','research/continuation_56/download_receipts.json','research/continuation_65/download_receipt.json'})
    assert resource['conservative_planning_total_bytes']==1671072950+later+resource['receipt_subtotals']['research/continuation_88/supplement_receipt.json']+resource['receipt_subtotals']['research/continuation_114/download_receipt.json']
    assert not resource['exact_lifetime_transfer_total_verified']
    access=read('research/continuation_50/access_results.json')
    assert not access['exact_physical_crosswalk_established'] and not access['image_pointer_verified']
    print(json.dumps({'saved_native_source_files':6,'confirmed_successful_bytes':1542176,
        'source_regions_checked':8,'historical_working_source_files':194,
        'current_working_source_files':resource['working_source_capture_files'],'historical_primary_pair_tests_still_pending':30,
        'current_primary_pair_tests_still_pending':len(live_pending),
        'historical_same_codex_excluded':False,
        'scope':'Source integrity, scope, arithmetic and one primary-test transition; not historical adjudication, performance validation or novelty.'}))


if __name__=='__main__':
    main()
