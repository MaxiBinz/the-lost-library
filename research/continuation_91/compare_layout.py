"""Compare catalogue-reported copying fields for the two specified records."""
import hashlib
import json
from pathlib import Path

import openpyxl

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).parent
BOOK = ROOT / 'research/continuation_26/bompac/Stockholm-Helsinki-Frs-Combined-BOMPAC.xlsx'
EXPECTED = 'ae9572cd4df5e5bccc241e8423ddf0c1'
FIELDS = ('Fr_reference', 'Database_or_institution', 'BOMPAC-reconstruction',
          'No_of_leaves', 'Type_hierarchy_1', 'Written_area_height_1',
          'Written_area_width_1', 'Columns', 'Rows', 'Account year', 'format',
          'schriftraum1', 'Row_exclusion')
WANTED = {'Fr 10370', 'F.m.II.64, fols. 6 & 7'}


def main():
    data = BOOK.read_bytes()
    assert hashlib.md5(data).hexdigest() == EXPECTED
    sheet = openpyxl.load_workbook(BOOK, read_only=True, data_only=True).active
    rows = sheet.iter_rows(values_only=True)
    next(rows)
    names = next(rows)
    columns = {name: names.index(name) for name in FIELDS}
    found = {}
    for row in rows:
        key = row[columns['Fr_reference']]
        if key in WANTED and row[columns['Row_exclusion']] == 'Include row':
            assert key not in found
            found[key] = {name: row[index] for name, index in columns.items()}
    assert set(found) == WANTED
    fr = found['Fr 10370']
    fm = found['F.m.II.64, fols. 6 & 7']
    out = {'workbook_sha256': hashlib.sha256(data).hexdigest(), 'units': 'cm',
           'rows': found,
           'difference_fr_minus_fm_cm': {
               'written_area_height': fr['Written_area_height_1'] - fm['Written_area_height_1'],
               'written_area_width': fr['Written_area_width_1'] - fm['Written_area_width_1']},
           'interpretation': 'Catalogue values only; leaf-specific coverage and measurement comparability unverified.'}
    (HERE / 'layout_comparison.json').write_text(json.dumps(out, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps(out['difference_fr_minus_fm_cm']))


if __name__ == '__main__':
    main()
