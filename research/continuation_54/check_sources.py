"""Offline E54 source integrity, coverage and explicitly limited transitions."""
import hashlib
import json
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def read(path):
    return json.loads((ROOT / path).read_text())


def main():
    p = read('research/continuation_54/protocol.json')
    for path, sha in p['frozen_inputs'].items():
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == sha, path
    snap = p['register_before_overlay']
    assert hashlib.sha256((ROOT / snap['path']).read_bytes()).hexdigest() == snap['sha256']
    caps = read('research/continuation_54/captures.json')['captures']
    receipts = read('research/continuation_54/download_receipts.json')
    assert len(caps) == len(receipts) == len(p['requested_sources']) == 8
    requests = {r['url']: r for r in p['requested_sources']}
    assert len(requests) == 8 and len({r['url'] for r in receipts}) == 8
    records = {r['id']: r for r in read('data/fragments.json')}
    for c, receipt in zip(caps, receipts):
        q = requests[c['url']]
        assert receipt['saved'] and receipt['status'] == 200 and receipt['retry'] is False
        assert receipt['url'] == c['url'] == receipt['final_url']
        assert receipt['path'] == c['path'] == q['path']
        assert receipt['sha256'] == c['sha256']
        assert receipt['bytes_received'] == c['bytes'] <= p['acquisition_bounds']['maximum_bytes_per_response']
        assert (ROOT / c['path']).stat().st_size == c['bytes']
        manifest = read(c['manifest'])
        canvas = manifest['items'][c['capture_index']]
        body = canvas['items'][0]['items'][0]['body']
        assert canvas['id'] == c['canvas_id'] == q['canvas_id']
        assert body['id'] == c['url'] and body['width'] == c['width'] and body['height'] == c['height']
        assert c['rights_url'] == records[c['physical_object_id']]['rights_url'] == 'http://creativecommons.org/publicdomain/mark/1.0/'
    sources = {r['path']: r for r in p['retained_sources']}
    sources.update({r['path']: dict(r, object_id=r['physical_object_id']) for r in caps})
    assert len(sources) == 27 and len({r['object_id'] for r in sources.values()}) == 8
    for path, s in sources.items():
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == s['sha256'], path
        with Image.open(ROOT / path) as im:
            assert im.size == (s['width'], s['height'])
    readings = read('research/continuation_54/readings.v1.json')
    assert len(readings['coverage']) == 27
    assert {r['path'] for r in readings['coverage']} == sources.keys()
    assert all(r['full_retained_photo_viewed'] and r['medieval_side'] is None for r in readings['coverage'])
    for ident, obj in readings['object_summaries'].items():
        selected = {sources[r['path']]['canvas_id'] for r in readings['coverage'] if r['object_id'] == ident}
        count = len(read('data/manifests/' + ident.removeprefix('mpo-') + '.json')['items'])
        assert obj['full_manifest_photo_coverage'] == (len(selected) == count)
        assert not obj['original_address_function_established'] and obj['medieval_side'] is None
    graph = read('data/knowledge.v1.json')
    evidence = {r['annotation_id'] for r in graph['evidence']}
    annotations = read('research/continuation_54/observations.json')['annotations']
    assert len(annotations) == len(readings['regions']) == 12
    for a, r in zip(annotations, readings['regions']):
        s = sources[r['path']]
        x, y, w, h = r['xywh']
        assert a['id'] == r['id'] and a['id'] in evidence and a['sha256'] == s['sha256']
        assert a['literal_candidate'] == r['literal'] and a['normalized_candidate'] is None
        assert 0 <= x < x+w <= s['width'] and 0 <= y < y+h <= s['height']
        assert a['target']['selector']['value'] == 'xywh=' + ','.join(map(str, r['xywh']))
        assert a['rights_url'] == 'http://creativecommons.org/publicdomain/mark/1.0/' and a['attribution']
        assert not a['independent_confirmation']
    assert set(readings['prior_regions_reused']) <= evidence
    matrix = read('research/continuation_54/pair_comparisons.json')['comparisons']
    assert len(matrix) == len({r['lead_id'] for r in matrix}) == 8
    assert {r['lead_id'] for r in matrix} == {r['id'] for r in p['selected_existing_leads']}
    for row in matrix:
        assert row['initial_primary_comparison_recorded'] and row['selected_view_inspection_complete']
        assert row['decision_state'] == 'unresolved' and set(row['source_regions']) <= evidence
        assert row['complete_source_photo_coverage'] == all(row['contexts'][i]['full_manifest_photo_coverage'] for i in row['pair'])
        for key in ['complete_corresponding_diagnostic_work_established', 'unique_shared_original_address_established',
                    'historical_same_codex_excluded', 'historical_adjudication_complete', 'independent_confirmation']:
            assert row[key] is False, key
    before = {r['id']: r for r in read(snap['path'])['leads']}
    now = {r['id']: r for r in read('data/lead_register.v1.json')['leads']}
    assert before.keys() == now.keys() and len(now) == 168
    pending_before = {i for i, r in before.items() if r.get('primary_pair_test_pending')}
    pending_now = {i for i, r in now.items() if r.get('primary_pair_test_pending')}
    assert len(pending_before) == 8 and not pending_now
    assert pending_before - pending_now == {r['lead_id'] for r in matrix}
    assert all(before[i]['decision_state'] == now[i]['decision_state'] for i in before)
    for row in matrix:
        live = now[row['lead_id']]
        assert live['test_execution'].startswith('E54 direct selected-source comparison')
        assert not live['retained_primary_comparison']['historical_adjudication_complete']
    claims = {r['id']: r for r in graph['claims']}
    assert not claims['observation:E54-marks']['shared_ix_independently_read']
    assert not claims['observation:E54-marks']['unique_shared_original_address_established']
    assert not claims['observation:E54-reuse']['original_quire_structure_established']
    assert not claims['observation:E54-reuse']['physical_join_established']
    result = read('research/continuation_54/results.json')
    total = sum(r['bytes_received'] for r in receipts)
    assert total == result['new_source_bytes'] == 2853289
    assert result['pair_comparisons_recorded'] == result['initial_primary_comparisons_recorded'] == 8
    assert result['source_photo_views_inspected'] == 27 and result['new_source_files'] == 8
    assert result['selected_view_inspection_complete'] and result['primary_pair_tests_still_pending'] == 0
    for key in ['complete_group_source_photo_coverage', 'complete_diplomatic_or_music_collation',
                'historical_adjudication_complete', 'new_codex_attribution', 'new_historical_exclusion',
                'new_catalogue_correction', 'novelty_cleared', 'new_discovery', 'independent_confirmation',
                'goal_complete', 'global_blocker_established']:
        assert result[key] is False, key
    resource = read('data/resource_audit.json')
    assert result['working_source_files_after']==208
    assert resource['working_source_capture_files']==208+len(read('research/continuation_65/captures.json')['captures'])
    assert resource['receipt_subtotals']['research/continuation_54/download_receipts.json'] == total
    assert result['conservative_transfer_plan_after']==1675854139
    assert resource['conservative_planning_total_bytes']==1675854139+resource['receipt_subtotals']['research/continuation_56/metadata_receipts.json']+resource['receipt_subtotals']['research/continuation_56/download_receipts.json']+resource['receipt_subtotals']['research/continuation_65/download_receipt.json']+resource['receipt_subtotals']['research/continuation_88/supplement_receipt.json']+resource['receipt_subtotals']['research/continuation_114/download_receipt.json']
    assert not resource['exact_lifetime_transfer_total_verified']
    print(json.dumps(dict(native_source_files=8, saved_bytes=total, inspected_photographs=27,
        source_regions=12, initial_comparisons=8, first_comparisons_still_pending=0,
        historical_decisions='unchanged; unresolved', goal_complete=False,
        scope='Source integrity and limited-comparison coverage; no independent transcription or historical adjudication.')))


if __name__ == '__main__':
    main()
