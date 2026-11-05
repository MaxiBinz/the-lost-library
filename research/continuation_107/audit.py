#!/usr/bin/env python3
"""Extract the published dating fields for the pre-existing IV.173 candidate unit."""
import hashlib
import json
from pathlib import Path
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'research/continuation_26/bompac/Stockholm-Helsinki-Frs-Combined-BOMPAC.xlsx'
EXPECTED = 'b6c13ca276372492927020ccdb1edf607b76028066f815c5cf426121238398c3'
FIELDS = ['Fr_reference', 'BOMPAC-reconstruction', 'Row_exclusion', 'datierung',
          'Dating_start', 'Dating_end', 'Dating_BOMPAC', 'Dating_BOMPAC_conflict']
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == EXPECTED
wb = load_workbook(SOURCE, read_only=True, data_only=True)
ws = wb['Sheet1']
it = ws.iter_rows(values_only=True)
next(it)
headers = list(next(it))
assert all(headers.count(field) == 1 for field in FIELDS)
rows = []
for n, values in enumerate(it, 3):
    if values[headers.index('BOMPAC-reconstruction')] == 'BOMPAC-9531':
        rows.append({'excel_row': n,
                     'values': {field: values[headers.index(field)] for field in FIELDS},
                     'cells': {field: f'{get_column_letter(headers.index(field)+1)}{n}' for field in FIELDS}})
wb.close()
assert {r['values']['Fr_reference'] for r in rows} == {'Fr 25592', 'Fr 29666', 'F.m.IV.173, fol. 1'}
assert all(r['values']['Row_exclusion'] == 'Include row' for r in rows)
data = {'date': '2026-11-04', 'source': str(SOURCE.relative_to(ROOT)), 'sha256': EXPECTED,
        'sheet': 'Sheet1', 'unit': 'BOMPAC-9531', 'rows': rows,
        'limits': 'Reported catalogue dates and dataset harmonization, not an independent paleographic dating, book attribution or correction.'}
(ROOT / 'research/continuation_107/results.json').write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'unit': data['unit'], 'rows': [r['values'] for r in rows]}, ensure_ascii=False, indent=2))
