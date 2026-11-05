"""Check E51 metadata, source pixels, scoped claims and one pair transition.

These are provenance/consistency checks, not an independent reading of marks,
a historical adjudication, CSV validation or a novelty search.
"""
import csv
import hashlib
import json
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def read(path):
    return json.loads((ROOT / path).read_text())


def main():
    protocol = read('research/continuation_51/protocol.json')
    p = read('research/continuation_51/primary_protocol.json')
    for path, expected in {**protocol['inputs'], **protocol['frozen_inputs'], **p['frozen_inputs']}.items():
        assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest() == expected, path
    receipts = read('research/continuation_51/metadata_receipts.json')
    assert len(receipts) == len({r['url'] for r in receipts}) == 3
    assert len(receipts) <= protocol['bounds']['maximum_requests']
    assert sum(r['bytes_received'] for r in receipts) == 31373
    assert sum(r['bytes_received'] for r in receipts) < protocol['bounds']['maximum_total_metadata_bytes']
    for receipt in receipts:
        raw = (HERE/receipt['file']).read_bytes()
        assert receipt['saved'] and receipt['status'] == 200 and not receipt['retry']
        assert len(raw) == receipt['bytes_received'] <= protocol['bounds']['maximum_bytes_per_response']
        assert hashlib.sha256(raw).hexdigest() == receipt['sha256']
    query = read('research/continuation_51/records-query.json')
    assert {r['id'] for r in query['hits']['hits']} == {17511106, 17701360}
    assert receipts[0]['url'] == protocol['initial_metadata_url']
    for old, receipt in zip(sorted(query['hits']['hits'], key=lambda r:r['id']), receipts[1:]):
        assert receipt['url'] == old['links']['latest']
    current = [read('research/continuation_51/' + n) for n in ['combined-latest.json', 'raw-latest.json']]
    assert [r['id'] for r in current] == [19046496, 19047125]
    assert [r['conceptrecid'] for r in current] == ['17511104', '17701359']
    for r in current:
        assert r['metadata']['version'] == 'v1.1'
        assert r['metadata']['publication_date'] == '2026-03-16'
        rel = r['metadata']['relations']['version']
        assert len(rel) == 1 and rel[0]['is_last'] and rel[0]['index'] == 1
        assert rel[0]['parent']['pid_value'] == r['conceptrecid']
        assert 'unchanged' in r['metadata']['description'] and 'csv' in r['metadata']['description']
    old_receipt = read('research/continuation_26/bompac/download_receipt.json')['files']
    comparison = read('research/continuation_51/metadata_comparison.json')
    assert len(comparison['file_comparisons']) == 5
    actual_files, missing_private = [], []
    for row in comparison['file_comparisons']:
        old = old_receipt[row['label']]
        r = next(r for r in current if r['id'] == row['current_version_record'])
        file = next(f for f in r['files'] if f['key'] == row['file'])
        assert row['file'] == old['filename'] and row['bytes'] == old['bytes'] == file['size']
        assert row['published_current_md5'] == old['md5'] == file['checksum'].removeprefix('md5:')
        assert row['sha256'] == old['sha256'] and row['doi'] == r['doi']
        path = ROOT/row['path']
        if path.exists():
            raw = path.read_bytes()
            assert len(raw) == row['bytes']
            assert hashlib.md5(raw).hexdigest() == row['published_current_md5']
            assert hashlib.sha256(raw).hexdigest() == row['sha256']
            actual_files.append(row['file'])
        else:
            assert path.suffix == '.pdf', 'Both actual workbooks are required in the review package'
            missing_private.append(row['file'])
    assert {'Stockholm-Helsinki-Frs-Combined-BOMPAC.xlsx','MPO_BOMPAC.xlsx'} <= set(actual_files)
    assert not comparison['new_csv_bytes_downloaded_or_checked'] and not comparison['novelty_cleared']
    caps = {c['path']: c for c in p['fixed_sources']}
    assert len(caps) == 6
    assert len({c['canvas_id'] for c in caps.values()}) == 6
    for path, c in caps.items():
        assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest() == c['sha256']
        with Image.open(ROOT/path) as im:
            assert im.size == (c['width'], c['height'])
        assert c['medieval_side'] is None and c['rights_url'] == 'http://creativecommons.org/publicdomain/mark/1.0/'
    readings = read('research/continuation_51/manual_readings.json')
    assert {(r['object_id'], r['source_capture_index']) for r in readings['coverage']} == {
        (c['object_id'], c['source_capture_index']) for c in caps.values()}
    assert all(r['full_photo_viewed'] and r['medieval_side'] is None for r in readings['coverage'])
    assert readings['controls_reviewed'] == ['I33-8994-roman', 'I33-8994-k']
    assert readings['reused_observations'] == ['V-10370-mark', 'V-10370-kmark']
    for control in p['known_mark_controls']:
        assert hashlib.sha256((ROOT/control['target']['source']).read_bytes()).hexdigest() == control['sha256']
    annotations = read('research/continuation_51/observations.json')['annotations']
    assert len(annotations) == len(readings['regions']) == 4
    for a, r in zip(annotations, readings['regions']):
        c = caps[r['path']]
        assert a['id'] == r['id'] and a['sha256'] == c['sha256']
        assert a['target']['source'] == r['path'] and a['literal_candidate'] == r['literal']
        assert a['normalized_candidate'] is None and not a['independent_confirmation']
        x, y, w, h = r['xywh']
        assert 0 <= x < x+w <= c['width'] and 0 <= y < y+h <= c['height']
        assert a['target']['selector']['value'] == 'xywh=' + ','.join(map(str, r['xywh']))
    with (ROOT/'research/mpo.csv').open(encoding='utf-8-sig') as handle:
        rows = {r['signatur']:r for r in csv.DictReader(handle)}
    assert rows['20274']['institution'] == 'KB'
    assert rows['20274']['bestandsbezeichnung'] == 'A 103' and rows['20274']['bestandssignatur'] == 'k 118 /'
    assert rows['20106']['bestandsbezeichnung'] == 'A 103' and rows['20106']['bestandssignatur'] == 'k  95---Episcopus--'
    assert not rows['20106']['iiif_manifest'] and not rows['20106']['bildbetrachter']
    result = read('research/continuation_51/results.json')
    assert result['metadata_audit'] == comparison and result['metadata_response_bytes'] == 31373
    assert result['primary_pair_test_executed'] and result['primary_pair_test_completed']
    assert result['all_planned_target_views_inspected'] and result['initial_primary_comparison_recorded']
    for key in ['historical_same_codex_adjudication_complete', 'secure_comparable_original_address_recovered',
                'shared_original_address_established', 'conflicting_original_address_established',
                'new_historical_exclusion', 'new_20106_crosswalk', 'new_discovery',
                'independent_confirmation', 'goal_complete', 'global_blocker_established']:
        assert result[key] is False, key
    before_path = p['register_before_overlay']['path']
    assert hashlib.sha256((ROOT/before_path).read_bytes()).hexdigest() == p['register_before_overlay']['sha256']
    before = {l['id']:l for l in read(before_path)['leads']}
    live_register=read('data/lead_register.v1.json')
    snapshot='research/continuation_52/lead_register.before.json'
    if (ROOT/snapshot).exists():
        pinned=read('research/continuation_52/protocol.json')['register_before_overlay']
        assert hashlib.sha256((ROOT/snapshot).read_bytes()).hexdigest()==pinned['sha256']
        historical=read(snapshot)
    else:
        historical=live_register
    now = {l['id']:l for l in historical['leads']}
    assert before.keys() == now.keys() and len(now) == 168
    old_pending = {k for k,v in before.items() if v.get('primary_pair_test_pending')}
    new_pending = {k for k,v in now.items() if v.get('primary_pair_test_pending')}
    assert len(old_pending) == 30 and len(new_pending) == 29
    assert old_pending - new_pending == {result['selected_lead']} and new_pending <= old_pending
    assert all(before[k]['decision_state'] == now[k]['decision_state'] for k in before)
    live_pending={l['id'] for l in live_register['leads'] if l.get('primary_pair_test_pending')}
    assert live_pending<=new_pending
    live_pair=next(l for l in live_register['leads'] if l['id']==result['selected_lead'])
    assert not live_pair['primary_pair_test_pending'] and live_pair['decision_state']=='unresolved'
    pair = now[result['selected_lead']]
    assert pair['decision_state'] == 'unresolved' and pair['test_execution'].startswith('E51 direct margin/address audit')
    graph = read('data/knowledge.v1.json')
    claim = next(c for c in graph['claims'] if c['id'] == 'observation:E51-library-reference')
    assert claim['predicate'] == 'describes' and claim['object'] == 'record:mpo-20274'
    assert not claim['medieval_folio_assigned'] and not claim['new_20106_crosswalk']
    primary = next(c for c in graph['claims'] if c['id'] == 'interpretation:E48-unit4861')
    assert primary['status'] == 'unresolved' and 'current_distribution_recheck' in primary
    candidate = next(e for e in graph['entities'] if e['id'] == 'record:manuscripta-101111')
    assert candidate['physical_object'] is None and candidate['crosswalk_status'] == 'unresolved'
    resource = read('data/resource_audit.json')
    later_captures=read('research/continuation_52/captures.json')['captures'] if (ROOT/'research/continuation_52/captures.json').exists() else []
    later_captures += read('research/continuation_54/captures.json')['captures']
    later_captures += read('research/continuation_65/captures.json')['captures']
    assert resource['working_source_capture_files'] == 194+len(later_captures)
    assert result['working_source_files_after'] == 194
    assert resource['receipt_subtotals']['research/continuation_51/metadata_receipts.json'] == 31373
    later=sum(resource['receipt_subtotals'].get(k,0) for k in ['research/continuation_52/download_receipts.json','research/continuation_54/download_receipts.json','research/continuation_56/metadata_receipts.json','research/continuation_56/download_receipts.json','research/continuation_65/download_receipt.json'])
    assert result['conservative_transfer_plan_after'] == 1671104323
    assert resource['conservative_planning_total_bytes'] == 1671104323+later+resource['receipt_subtotals']['research/continuation_88/supplement_receipt.json']+resource['receipt_subtotals']['research/continuation_114/download_receipt.json']
    assert not resource['exact_lifetime_transfer_total_verified']
    print(json.dumps({'current_release_ids':[r['id'] for r in current], 'file_receipts_matching_latest_metadata':5,
        'actual_retained_files_checked_in_this_copy':actual_files,
        'private_reading_pdfs_absent_from_this_copy':missing_private,
        'metadata_response_bytes':31373, 'new_regions_checked':4, 'reused_mark_regions':4,
        'historical_primary_pairs_without_initial_comparison':29,
        'current_primary_pairs_without_initial_comparison':len(live_pending), 'historical_book_decision':'unresolved',
        'scope':'Metadata/pixel provenance and state transition; no independent reading, scientific novelty or CSV equivalence.'}))


if __name__ == '__main__':
    main()
