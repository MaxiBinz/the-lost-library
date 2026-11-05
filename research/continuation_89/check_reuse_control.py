#!/usr/bin/env python3
"""Reproduce an exploratory reuse-context control from the retained BOMPAC workbook."""
import hashlib
import json
from pathlib import Path

import openpyxl

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'research/continuation_26/bompac/Stockholm-Helsinki-Frs-Combined-BOMPAC.xlsx'
OUT = Path(__file__).with_name('workbook_rows.json')
EXPECTED_MD5 = 'ae9572cd4df5e5bccc241e8423ddf0c1'
WANTED = {'Fr 10370', 'Fr 20278', 'F.m.II.64, fols. 6 & 7'}
FIELDS = ('Fr_reference', 'BOMPAC-reconstruction', 'FM_signum', 'Area', 'Province',
          'Bailiwick', 'Account year', 'Archival_series', 'Archival_collection_accounts',
          'bestandsbezeichnung', 'bestandssignatur', 'Row_exclusion')


def main():
    payload = SOURCE.read_bytes()
    if hashlib.md5(payload).hexdigest() != EXPECTED_MD5:
        raise ValueError('Workbook differs from the published checksum pinned in E26')
    sheet = openpyxl.load_workbook(SOURCE, read_only=True, data_only=True).active
    rows = sheet.iter_rows(values_only=True)
    next(rows)
    header = next(rows)
    columns = {name: header.index(name) for name in FIELDS}
    found = []
    for row in rows:
        if row[columns['Fr_reference']] in WANTED:
            values = {name: row[index] for name, index in columns.items()}
            if values['Row_exclusion'] == 'Include row':
                found.append(values)
    assert {row['Fr_reference'] for row in found} == WANTED and len(found) == len(WANTED)
    OUT.write_text(json.dumps({'source_sha256': hashlib.sha256(payload).hexdigest(),
                               'rows': found}, indent=2, ensure_ascii=False) + '\n')
    for row in found:
        print(row['Fr_reference'], row['BOMPAC-reconstruction'], row['Account year'])


if __name__ == '__main__':
    main()
