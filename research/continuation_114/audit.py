"""Compare published v1.1 CSV against the pinned workbook, field by field.

This verifies data representations, not historical layouts or publisher intent.
"""
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

from openpyxl import load_workbook

ROOT = Path(__file__).resolve().parents[2]
CSV = ROOT / 'research/continuation_114/Stockholm-Helsinki-Frs-Combined-BOMPAC.csv'
XLSX = ROOT / 'research/continuation_26/bompac/Stockholm-Helsinki-Frs-Combined-BOMPAC.xlsx'
assert hashlib.sha256(CSV.read_bytes()).hexdigest() == '4d7ba58bb422ed5c331518284919c42ceba2648412ecf5576f0bea09874db304'
assert hashlib.md5(CSV.read_bytes()).hexdigest() == '2db8890e0616786a3b6461c9c737da1c'
assert hashlib.sha256(XLSX.read_bytes()).hexdigest() == 'b6c13ca276372492927020ccdb1edf607b76028066f815c5cf426121238398c3'

FIELDS = ['Index', 'Fr_number', 'Fr_reference', 'Database', 'Row_exclusion', 'No_of_leaves', 'Columns']

def norm(v):
    if v is None:
        return ''
    if isinstance(v, (int, float)) and not isinstance(v, bool):
        return str(int(v)) if v == int(v) else str(v)
    return str(v).strip()

with CSV.open(encoding='utf-8-sig', newline='') as f:
    reader = csv.reader(f, delimiter=';')
    next(reader)
    header = next(reader)
    assert all(header.count(k) == 1 for k in FIELDS)
    indices = {k: header.index(k) for k in FIELDS}
    csv_rows = [{k: norm(row[i]) for k, i in indices.items()} for row in reader]

wb = load_workbook(XLSX, read_only=True, data_only=True)
rows = wb['Sheet1'].iter_rows(values_only=True)
next(rows)
header = list(next(rows))
assert all(header.count(k) == 1 for k in FIELDS)
indices = {k: header.index(k) for k in FIELDS}
xlsx_rows = [{k: norm(row[i]) for k, i in indices.items()} for row in rows]
wb.close()

assert len(csv_rows) == len(xlsx_rows) == 29586
assert len({r['Index'] for r in csv_rows}) == len(csv_rows)
differences = Counter()
examples = {}
for number, (c, x) in enumerate(zip(csv_rows, xlsx_rows), 3):
    assert c['Index'] == x['Index'], f'Index mismatch at data row {number}'
    for k in FIELDS:
        if c[k] != x[k]:
            differences[k] += 1
            examples.setdefault(k, {'data_row': number, 'csv': c[k], 'xlsx': x[k]})

mpo = [r for r in csv_rows if r['Database'] == 'MPO' and r['Row_exclusion'] == 'Include row']
numeric = [r for r in mpo if r['Columns'].isdigit() and r['No_of_leaves'].isdigit()]
equal = sum(r['Columns'] == r['No_of_leaves'] for r in numeric)
result = {
    'date': '2026-11-04', 'data_rows': len(csv_rows), 'compared_fields': FIELDS,
    'comparison': 'row-order and unique Index matched; blank/None normalized; numeric XLSX cells stringified; values stripped of surrounding whitespace',
    'csv_sha256': '4d7ba58bb422ed5c331518284919c42ceba2648412ecf5576f0bea09874db304',
    'xlsx_sha256': 'b6c13ca276372492927020ccdb1edf607b76028066f815c5cf426121238398c3',
    'different_values_by_field': dict(differences), 'first_difference_per_field': examples,
    'included_mpo': len(mpo), 'included_mpo_integer_counts': len(numeric),
    'included_mpo_integer_counts_equal': equal,
    'limits': 'Only listed fields compared; integer test is narrower than any general numeric test; neither source correctness, cause, prior notice nor a historical manuscript conclusion is established.'
}
(ROOT / 'research/continuation_114/results.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
