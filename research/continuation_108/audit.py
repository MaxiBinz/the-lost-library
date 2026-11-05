#!/usr/bin/env python3
"""Audit two published workbook fields; do not change either source dataset."""
from collections import Counter, defaultdict
import csv
import hashlib
import json
from pathlib import Path
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter

ROOT = Path(__file__).resolve().parents[2]
COMBINED = ROOT / 'research/continuation_26/bompac/Stockholm-Helsinki-Frs-Combined-BOMPAC.xlsx'
RAW = ROOT / 'research/continuation_26/bompac/raw_metadata/MPO_BOMPAC.xlsx'
HASHES = {COMBINED: 'b6c13ca276372492927020ccdb1edf607b76028066f815c5cf426121238398c3',
          RAW: '7f2e75d15b5b0f162108c1118dbfd8af4b9919602cda41852e67baafeb510bd9'}
for path, expected in HASHES.items():
    assert hashlib.sha256(path.read_bytes()).hexdigest() == expected, str(path)

def integer(value):
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)) and int(value) == value:
        return int(value)
    if isinstance(value, str) and value.strip().isdigit():
        return int(value.strip())
    return None

def read_rows(path, sheet, fields):
    wb = load_workbook(path, read_only=True, data_only=True)
    it = wb[sheet].iter_rows(values_only=True)
    next(it)  # first row is group headings
    header = list(next(it))
    assert all(header.count(field) == 1 for field in fields)
    for n, row in enumerate(it, 3):
        yield n, {field: row[header.index(field)] for field in fields}, {
            field: f'{get_column_letter(header.index(field) + 1)}{n}' for field in fields}
    wb.close()

raw_fields = ['fragment_id', 'spaltenzahl', 'leaves', 'Row_exclusion']
raw = defaultdict(list)
for n, values, cells in read_rows(RAW, 'Blad1', raw_fields):
    key = integer(values['fragment_id'])
    if key is not None:
        raw[key].append((n, values, cells))

fields = ['Fr_number', 'Fr_reference', 'Database', 'No_of_leaves', 'Columns', 'Row_exclusion']
numeric = Counter()
finnish = Counter()
join = Counter()
examples = {}
disagreements = []
for n, values, cells in read_rows(COMBINED, 'Sheet1', fields):
    if values['Database'] == 'FM' and values['Row_exclusion'] == 'Include row':
        left = integer(values['No_of_leaves'])
        right = integer(values['Columns'])
        if left is not None and right is not None:
            finnish['both_numeric'] += 1
            finnish['equal'] += left == right
            finnish['different'] += left != right
    if values['Database'] != 'MPO' or values['Row_exclusion'] != 'Include row':
        continue
    numeric['included_mpo_rows'] += 1
    leaves = integer(values['No_of_leaves'])
    columns = integer(values['Columns'])
    if leaves is not None and columns is not None:
        numeric['both_numeric'] += 1
        numeric['equal'] += leaves == columns
        numeric['different'] += leaves != columns
    else:
        numeric['at_least_one_nonnumeric_or_blank'] += 1
    key = integer(values['Fr_number'])
    if key is None or values['Fr_reference'] != f'Fr {key}':
        join['bad_exact_reference'] += 1
        continue
    matches = raw.get(key, [])
    if len(matches) != 1:
        join['missing_or_nonunique_raw_id'] += 1
        continue
    raw_n, raw_values, raw_cells = matches[0]
    if raw_values['Row_exclusion'] != 'Include row':
        join['raw_row_not_included'] += 1
        continue
    original = integer(raw_values['spaltenzahl'])
    if original in (1, 2) and columns in (1, 2):
        join['eligible_rows'] += 1
        join[f'raw_{original}_combined_{columns}'] += 1
        if original != columns:
            disagreements.append({'fragment': values['Fr_reference'], 'combined_row': n, 'raw_row': raw_n,
                                  'raw_spaltenzahl': original, 'combined_columns': columns,
                                  'combined_leaves': leaves, 'raw_cell': raw_cells['spaltenzahl'],
                                  'combined_cell': cells['Columns']})
    else:
        join['outside_numeric_1_2_subset'] += 1
    if key in (607, 8994, 25592):
        examples[str(key)] = {'combined_row': n, 'combined_values': values, 'combined_cells': cells,
                              'raw_row': raw_n, 'raw_values': raw_values, 'raw_cells': raw_cells}

assert set(examples) == {'607', '8994', '25592'}
assert numeric['both_numeric'] == numeric['equal'] + numeric['different']
assert finnish['both_numeric'] == finnish['equal'] + finnish['different']
assert join['eligible_rows'] == sum(join[f'raw_{a}_combined_{b}'] for a in (1, 2) for b in (1, 2))
assert len(disagreements) == join['raw_1_combined_2'] + join['raw_2_combined_1']
result = {'date': '2026-11-04',
          'combined': {'path': str(COMBINED.relative_to(ROOT)), 'sha256': HASHES[COMBINED], 'sheet': 'Sheet1'},
          'raw': {'path': str(RAW.relative_to(ROOT)), 'sha256': HASHES[RAW], 'sheet': 'Blad1'},
          'scope': 'Included MPO rows; exact numeric fragment ID and Fr reference; exactly one raw workbook match; both rows included; raw and combined 1 or 2 for the comparison matrix.',
          'mpo_leaves_vs_columns': dict(numeric), 'fm_leaves_vs_columns': dict(finnish),
          'raw_columns_vs_combined': dict(join), 'examples': examples,
          'limits': 'Field consistency is not physical validation, a confirmed cause, current-release verification, first notice or an assessment of every fragment.'}
out = ROOT / 'research/continuation_108/results.json'
out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
with (ROOT / 'research/continuation_108/disagreement_candidates.csv').open('w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['fragment', 'combined_row', 'raw_row', 'raw_spaltenzahl',
                                           'combined_columns', 'combined_leaves', 'raw_cell', 'combined_cell'])
    writer.writeheader()
    writer.writerows(disagreements)
print(json.dumps({'mpo_leaves_vs_columns': dict(numeric), 'fm_leaves_vs_columns': dict(finnish),
                  'raw_columns_vs_combined': dict(join)}, indent=2))
