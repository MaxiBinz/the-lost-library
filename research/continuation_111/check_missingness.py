#!/usr/bin/env python3
"""Compare original and combined layout missingness in pinned BOMPAC workbooks."""
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
MPO_CSV = ROOT / 'research/mpo.csv'
HASHES = {
    COMBINED: 'b6c13ca276372492927020ccdb1edf607b76028066f815c5cf426121238398c3',
    RAW: '7f2e75d15b5b0f162108c1118dbfd8af4b9919602cda41852e67baafeb510bd9',
    MPO_CSV: 'f5d2825703be19fd1994bc0b91724c32c67c36535622d5554c37b4029592d00b',
}
for path, expected in HASHES.items():
    assert hashlib.sha256(path.read_bytes()).hexdigest() == expected, path

def integer(value):
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, float) and value.is_integer():
        return int(value)
    if isinstance(value, str) and value.strip().isdigit():
        return int(value.strip())
    return None

def category(value):
    if value is None or (isinstance(value, str) and not value.strip()):
        return 'blank'
    if isinstance(value, str) and value.strip().upper() == 'NULL':
        return 'literal_NULL'
    number = integer(value)
    return f'numeric_{number}' if number is not None else 'other_nonempty'

def rows(path, sheet, fields):
    wb = load_workbook(path, read_only=True, data_only=True)
    it = wb[sheet].iter_rows(values_only=True)
    next(it)
    header = list(next(it))
    assert all(header.count(k) == 1 for k in fields)
    positions = {k: header.index(k) for k in fields}
    for number, row in enumerate(it, 3):
        yield number, {k: row[i] for k, i in positions.items()}, {
            k: f'{get_column_letter(i + 1)}{number}' for k, i in positions.items()}
    wb.close()

raw = defaultdict(list)
for n, values, cells in rows(RAW, 'Blad1', ['fragment_id', 'spaltenzahl', 'Row_exclusion']):
    key = integer(values['fragment_id'])
    if key is not None:
        raw[key].append((n, values, cells))

csv_rows = defaultdict(list)
with MPO_CSV.open(encoding='utf-8-sig', newline='') as source:
    for row in csv.DictReader(source):
        key = integer(row['signatur'])
        if key is not None:
            csv_rows[key].append(row)

counts = Counter()
matrix = Counter()
examples = []
fields = ['Fr_number', 'Fr_reference', 'Database', 'Columns', 'No_of_leaves', 'Row_exclusion']
for n, values, cells in rows(COMBINED, 'Sheet1', fields):
    if values['Database'] != 'MPO' or values['Row_exclusion'] != 'Include row':
        continue
    counts['included_mpo'] += 1
    key = integer(values['Fr_number'])
    if key is None or values['Fr_reference'] != f'Fr {key}':
        counts['bad_exact_reference'] += 1
        continue
    matches = raw.get(key, [])
    if len(matches) != 1:
        counts['missing_or_nonunique_raw_id'] += 1
        continue
    raw_n, original, original_cells = matches[0]
    if original['Row_exclusion'] != 'Include row':
        counts['raw_row_not_included'] += 1
        continue
    counts['matched_included'] += 1
    a, b = category(original['spaltenzahl']), category(values['Columns'])
    matrix[(a, b)] += 1
    if a in ('blank', 'literal_NULL') and b in ('numeric_1', 'numeric_2'):
        counts['original_blank_or_NULL_combined_1_or_2'] += 1
        if len(csv_rows[key]) != 1:
            counts['source_csv_missing_or_duplicate'] += 1
        elif category(csv_rows[key][0]['spaltenzahl']) in ('blank', 'literal_NULL'):
            counts['source_csv_also_blank_or_NULL'] += 1
            counts[f"source_csv_{category(csv_rows[key][0]['spaltenzahl'])}"] += 1
        else:
            counts['source_csv_nonblank'] += 1
        if len(examples) < 5:
            examples.append({'fragment': values['Fr_reference'], 'raw_row': raw_n,
                'raw_cell': original_cells['spaltenzahl'], 'raw_value': original['spaltenzahl'],
                'combined_row': n, 'combined_cell': cells['Columns'],
                'combined_value': values['Columns'], 'leaves': values['No_of_leaves'],
                'leaves_cell': cells['No_of_leaves']})

assert counts['included_mpo'] == sum(counts[k] for k in ('matched_included', 'bad_exact_reference', 'missing_or_nonunique_raw_id', 'raw_row_not_included'))
assert sum(matrix.values()) == counts['matched_included']
assert counts['original_blank_or_NULL_combined_1_or_2'] == sum(matrix[(a,b)] for a in ('blank','literal_NULL') for b in ('numeric_1','numeric_2'))
assert counts['original_blank_or_NULL_combined_1_or_2'] == sum(counts[k] for k in ('source_csv_also_blank_or_NULL', 'source_csv_missing_or_duplicate', 'source_csv_nonblank'))
result = {'date': '2026-11-04', 'source_sha256': {str(k.relative_to(ROOT)): v for k, v in HASHES.items()},
          'population': dict(counts), 'matrix': [{'raw': a, 'combined': b, 'count': n} for (a,b),n in sorted(matrix.items())],
          'examples': examples, 'limits': 'Related source datasets; blank/NULL is a field state, not an independent judgment of the fragment. Numeric combined fields may have another source; provenance and intent remain unverified. No historical layout or root cause established.'}
(ROOT / 'research/continuation_111/results.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
print(json.dumps(result, ensure_ascii=False, indent=2))
