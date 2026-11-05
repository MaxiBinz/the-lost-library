#!/usr/bin/env python3
"""Report source and harmonized dates for one pre-existing contested unit."""
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
EXPECTED_IDS = {'Fr 8066', 'Fr 8072', 'Fr 8073', 'Fr 8201', 'Fr 8304', 'Fr 9620', 'Fr 20106', 'Fr 20107'}

def main():
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == EXPECTED
    wb = load_workbook(SOURCE, read_only=True, data_only=True)
    ws = wb['Sheet1']
    it = ws.iter_rows(values_only=True)
    next(it)
    headers = list(next(it))
    assert all(headers.count(field) == 1 for field in FIELDS)
    rows = []
    for n, values in enumerate(it, 3):
        if values[headers.index('BOMPAC-reconstruction')] == 'BOMPAC-4861':
            rows.append({'excel_row': n,
                         'values': {k: values[headers.index(k)] for k in FIELDS},
                         'cells': {k: f'{get_column_letter(headers.index(k)+1)}{n}' for k in FIELDS}})
    wb.close()
    assert {r['values']['Fr_reference'] for r in rows} == EXPECTED_IDS
    assert len(rows) == len(EXPECTED_IDS)
    result = {'date':'2026-11-03', 'source':str(SOURCE.relative_to(ROOT)), 'sha256':EXPECTED,
              'sheet':'Sheet1', 'unit':'BOMPAC-4861', 'selection':'Existing contested unit; selected after reading the dataset and study; not blind.',
              'rows':rows, 'scope':'A provenance and source-disagreement audit, not an independent dating or a new manuscript attribution.'}
    (ROOT / 'research/continuation_99/results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'source_rows':len(rows), 'source_dates':{v:sum(r['values']['datierung']==v for r in rows) for v in sorted({r['values']['datierung'] for r in rows})},
                      'harmonized_dates':sorted({r['values']['Dating_BOMPAC'] for r in rows}),
                      'conflict_flags':sorted({r['values']['Dating_BOMPAC_conflict'] for r in rows})},ensure_ascii=False))

if __name__ == '__main__':
    main()
