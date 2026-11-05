#!/usr/bin/env python3
"""Extract reuse metadata for two existing reconstructions, without network access."""
import hashlib
import json
from pathlib import Path

import openpyxl

ROOT = Path(__file__).resolve().parents[2]
WORKBOOK = ROOT / 'research/continuation_26/bompac/Stockholm-Helsinki-Frs-Combined-BOMPAC.xlsx'
OUT = Path(__file__).with_name('reuse_audit.json')
FIELDS = ['Fr_reference', 'Database_or_institution', 'BOMPAC-reconstruction',
          'Area', 'Province', 'Bailiwick', 'Account year', 'Archival_series',
          'Archival_collection_accounts']


def main():
    digest = hashlib.sha256(WORKBOOK.read_bytes()).hexdigest()
    wb = openpyxl.load_workbook(WORKBOOK, read_only=True, data_only=True)
    rows = wb.active.iter_rows(values_only=True)
    next(rows)
    header = next(rows)
    columns = {name: header.index(name) for name in FIELDS + ['Row_exclusion']}
    result = {key: [] for key in ('BOMPAC-5324', 'BOMPAC-912')}
    for row in rows:
        unit = row[columns['BOMPAC-reconstruction']]
        if unit not in result or row[columns['Row_exclusion']] != 'Include row':
            continue
        result[unit].append({name: row[columns[name]] for name in FIELDS})
    assert len(result['BOMPAC-5324']) == 28
    assert len(result['BOMPAC-912']) == 20
    OUT.write_text(json.dumps({'workbook_sha256': digest, 'rows': result},
                              ensure_ascii=False, indent=2) + '\n')
    for unit, entries in result.items():
        years = [e['Account year'] for e in entries if isinstance(e['Account year'], int)]
        print(f'{unit}: {len(entries)} rows, {len(years)} dated; range {min(years)}–{max(years)}; '
              f'1556–1562: {sum(1556 <= y <= 1562 for y in years)}; '
              f'1563: {sum(y == 1563 for y in years)}')


if __name__ == '__main__':
    main()
