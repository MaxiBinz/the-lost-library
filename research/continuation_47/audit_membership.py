"""Read-only, exact-row prior-source audit of the six retained Aboense controls.

No workbook writes, network access, matcher changes or physical identity closure.
The related raw and combined BOMPAC deposits are not independent evidence votes.
"""
from __future__ import annotations

import collections
import hashlib
import json
from pathlib import Path

from openpyxl import load_workbook
from openpyxl.utils import get_column_letter

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
COMBINED = 'research/continuation_26/bompac/Stockholm-Helsinki-Frs-Combined-BOMPAC.xlsx'
RAW = 'research/continuation_26/bompac/raw_metadata/MPO_BOMPAC.xlsx'
IDS = [7957, 7960, 7961, 8343, 8344, 9242]
COMBINED_FIELDS = ['Fr_reference', 'Database_or_institution', 'BOMPAC-reconstruction',
    'Frs_per_unit', 'Fr_in_unit', 'FM_signum_BOMPAC', 'CCM_signum_BOMPAC',
    'Codex_signum_BOMPAC', 'Identification_comment', 'Row_exclusion', 'Exclusion_criteria']
RAW_FIELDS = ['fragment_id', 'unit_HK', 'unit_NB_HK', 'frs_per_unit_HK',
    'fr_in_unit_IDX_HK', 'ccmsignum_HK', 'codex_HK', 'signum_comments_HK', 'general_notes_HK']


def read(path):
    return json.loads((ROOT / path).read_text())


def save(name, value):
    (HERE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def source_rows(path, sheet, fields, key, targets, unit_key):
    """Preserve all exact identifier matches, including excluded/duplicate rows."""
    wb = load_workbook(ROOT / path, read_only=True, data_only=True)
    ws = wb[sheet]
    rows = ws.iter_rows(values_only=True)
    next(rows)
    headers = list(next(rows))
    assert all(headers.count(k) == 1 for k in fields + [key, unit_key])
    found = []
    units = set()
    for index, row in enumerate(rows, 3):
        data = dict(zip(headers, row))
        if data.get(key) in targets:
            found.append((index, data))
            units.add(data[unit_key])
    assert None not in units and len(units) == 1, 'Ambiguous target reconstruction'
    members = []
    for index, row in enumerate(ws.iter_rows(min_row=3, values_only=True), 3):
        data = dict(zip(headers, row))
        if data.get(unit_key) in units:
            members.append((index, data))

    def project(row):
        index, data = row
        return {'excel_row': index, 'values': {k: data.get(k) for k in fields},
                'cells': {k: f'{get_column_letter(headers.index(k)+1)}{index}' for k in fields}}

    result = {'path': path, 'sha256': hashlib.sha256((ROOT / path).read_bytes()).hexdigest(),
        'sheet': sheet, 'header_row': 2, 'first_data_row': 3,
        'source_dimensions_including_header_rows': [ws.max_row, ws.max_column],
        'unit': next(iter(units)), 'target_rows': [project(r) for r in found],
        'unit_rows': [project(r) for r in members],
        'target_identifier_match_counts': {str(t): sum(d.get(key) == t for _, d in found) for t in sorted(targets)},
        'unit_identifier_duplicates': {str(k): v for k, v in collections.Counter(d.get(key) for _, d in members).items() if v > 1}}
    assert all(n == 1 for n in result['target_identifier_match_counts'].values()), 'Missing/duplicate exact target identifier'
    assert not result['unit_identifier_duplicates'], 'Ambiguous unit membership'
    wb.close()
    return result


def main():
    protocol = read('research/continuation_47/protocol.json')
    for path, expected in {**protocol['source_inputs'], **protocol['frozen_inputs']}.items():
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == expected, path
    combined = source_rows(COMBINED, 'Sheet1', COMBINED_FIELDS, 'Fr_reference',
                           {'Fr '+str(i) for i in IDS}, 'BOMPAC-reconstruction')
    raw = source_rows(RAW, 'Blad1', RAW_FIELDS, 'fragment_id', set(IDS), 'unit_HK')
    assert combined['unit'] == 'BOMPAC-4795' and raw['unit'] == 'C-1481'
    assert all(r['values']['Row_exclusion'] == 'Include row' for r in combined['unit_rows'])
    assert all(r['values']['FM_signum_BOMPAC'] == 'FM.II.44' for r in combined['unit_rows'])
    assert len(combined['unit_rows']) == 31 and len(raw['unit_rows']) == 7
    assert {r['values']['Fr_in_unit'] for r in combined['unit_rows']} == set(range(1, 32))
    assert {r['values']['Frs_per_unit'] for r in combined['unit_rows']} == {31}
    assert {r['values']['frs_per_unit_HK'] for r in raw['unit_rows']} == {7}
    assert {r['values']['fr_in_unit_IDX_HK'] for r in raw['unit_rows']} == set(range(1, 8))
    ctargets = {r['values']['Fr_reference']: r for r in combined['target_rows']}
    rtargets = {r['values']['fragment_id']: r for r in raw['target_rows']}
    core = read('data/fragments.json')
    memberships = []
    for ident in IDS:
        record = [r for r in core if r['id'] == f'mpo-{ident}']
        assert len(record) == 1 and record[0]['physical_object_id'] == f'mpo-{ident}'
        c, r = ctargets[f'Fr {ident}'], rtargets[ident]
        memberships.append({'object_id': f'mpo-{ident}', 'record_id': f'mpo-{ident}',
            'source_record': record[0]['source_url'], 'combined_row': c, 'raw_row': r,
            'reconstruction': combined['unit'], 'finnish_signum': c['values']['FM_signum_BOMPAC'],
            'basis': 'source_assertion', 'independent_confirmation': False,
            'scope': 'Explicit published BOMPAC reconstruction assignment; not a new physical attribution, adjacency or source-image validation.'})
    baseline = read('research/continuation_47/lead_register.before.json')
    member_objects = {'object:'+m['object_id'] for m in memberships}
    pairs = [l for l in baseline['leads'] if l['id'].startswith('pair-') and len(l['subjects']) == 2 and set(l['subjects']) <= member_objects]
    repairs = [l['id'] for l in pairs if l['test_execution'] == 'metadata and availability triage only']
    assert len(pairs) == 15 and len(repairs) == 13
    save('memberships.json', {'version': '1.0.0', 'date': '2026-10-29',
        'combined': combined, 'raw': raw, 'memberships': memberships,
        'source_records': [{'doi': '10.5281/zenodo.17511106', 'license': 'CC BY 4.0'},
                           {'doi': '10.5281/zenodo.17701360', 'license': 'CC BY 4.0'}],
        'grain': 'Workbook records, not necessarily single leaves. The24 Finnish rows each name a two-folio record;31 is not a leaf/image count.',
        'independence_limit': 'These related BOMPAC deposits can share catalogue and research provenance. Their agreement is not independent confirmation.'})
    result = {'version': '1.0.0', 'date': '2026-10-29',
        'result': 'All six retained Aboense controls have unique included rows explicitly assigned to BOMPAC-4795 with FM.II.44. The related raw data assigns them to C-1481. Credit13 previously metadata-only pair leads as already documented controls.',
        'totals': {'all_leads': len(baseline['leads']), 'pair_leads': sum(l['id'].startswith('pair-') for l in baseline['leads']),
            'retained_members_checked': 6, 'all_member_pairings': 15, 'source_credit_repairs': len(repairs),
            'baseline_metadata_only_pairs': 49, 'remaining_metadata_only_pairs': 49-len(repairs),
            'combined_unit_rows': len(combined['unit_rows']), 'raw_unit_rows': len(raw['unit_rows']),
            'combined_unit_institutions': dict(collections.Counter(r['values']['Database_or_institution'] for r in combined['unit_rows']))},
        'repair_leads': repairs, 'already_reviewed_pair_leads': [l['id'] for l in pairs if l['id'] not in repairs],
        'remaining_metadata_only_leads': [{'lead_id': l['id'], 'subjects': l['subjects'],
            'relationship_type': l['relationship_type'], 'prior': l['already_published'],
            'required_inputs': l['required_inputs']} for l in baseline['leads']
            if l['test_execution'] == 'metadata and availability triage only' and l['id'] not in repairs],
        'limits': ['Internal source-credit correction, not a correction to scholarship or a new discovery.',
            'No new physical object, leaf, capture, source region or independently confirmed same-codex assertion.',
            'Published reconstruction membership does not establish physical joins, adjacency, side mapping, date or completeness.',
            'Fr28175 is a seventh source record, not a newly imaged core object. The24 Finnish paired-folio rows are not24 single leaves or verified available captures.',
            'Taitto/Haapanen attribution history and E36 direct continuity observations remain credited separately. This workbook audit does not reread Taitto2002.'],
        'next_test': 'Audit the remaining36 existing pair leads against already retained explicit source assignments; do not re-screen known controls as novel candidates. Then choose a discriminating primary-source test from the genuinely unresolved remainder. Keep scope/source dependencies explicit.',
        'new_discovery': False, 'independent_confirmation': False, 'goal_complete': False,
        'global_blocker_established': False, 'acquired_bytes': 0, 'new_source_files': 0}
    save('results.json', result)
    print(json.dumps(result['totals'], indent=2))


if __name__ == '__main__':
    main()
