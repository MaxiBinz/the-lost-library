"""Trace two reuse descriptions and the Swedish date mark; no source modified."""
import csv
import hashlib
import json
from pathlib import Path
from PIL import Image
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter

root = Path(__file__).resolve().parents[2]
book = root / 'research/continuation_26/bompac/Stockholm-Helsinki-Frs-Combined-BOMPAC.xlsx'
csv_path = root / 'research/mpo.csv'
image = root / 'data/images/mpo-10406-capture-3.jpg'
hashes = {
    book: 'b6c13ca276372492927020ccdb1edf607b76028066f815c5cf426121238398c3',
    csv_path: 'f5d2825703be19fd1994bc0b91724c32c67c36535622d5554c37b4029592d00b',
    image: 'ad15525ab9eaeb67b603ade9120886e2c5c8caecb5ebfbebef9bd478a09bfbb9',
}
for path, digest in hashes.items():
    assert hashlib.sha256(path.read_bytes()).hexdigest() == digest

wanted = ['Fr_reference', 'Database', 'BOMPAC-reconstruction', 'No_of_leaves',
          'Account year', 'Area', 'Province', 'Bailiwick', 'Archival_collection_accounts',
          'bestandssignatur', 'Row_exclusion']
wb = load_workbook(book, read_only=True, data_only=True)
it = wb['Sheet1'].iter_rows(values_only=True)
next(it)
header = list(next(it))
assert all(header.count(k) == 1 for k in wanted)
positions = {k: header.index(k) for k in wanted}
rows = {}
for n, row in enumerate(it, 3):
    if row[positions['Fr_reference']] in ('Fr 10406', 'F.m.IV.156, fol. 8'):
        values = {k: row[i] for k, i in positions.items()}
        key = values['Fr_reference']
        assert key not in rows
        rows[key] = {'row': n, 'values': values,
                     'cells': {k: f'{get_column_letter(i + 1)}{n}' for k, i in positions.items()}}
wb.close()
assert set(rows) == {'Fr 10406', 'F.m.IV.156, fol. 8'}
assert all(r['values']['Row_exclusion'] == 'Include row' for r in rows.values())
assert rows['Fr 10406']['values']['Account year'] == 1608
assert rows['F.m.IV.156, fol. 8']['values']['Account year'] == 1604

with csv_path.open(encoding='utf-8-sig', newline='') as f:
    matched = [r for r in csv.DictReader(f) if r['signatur'] == '10406']
assert len(matched) == 1
assert matched[0]['bestandssignatur'] == '71:2 1608'
with Image.open(image) as im:
    assert im.size == (1000, 659)
    assert 875 + 105 <= im.width and 250 + 215 <= im.height

result = {
    'date': '2026-11-04', 'rows': rows,
    'original_mpo': {'path': str(csv_path.relative_to(root)), 'signatur': '10406',
                     'bestandssignatur': matched[0]['bestandssignatur'],
                     'bestandsbezeichnung': matched[0]['bestandsbezeichnung']},
    'swedish_date_mark': {'path': str(image.relative_to(root)), 'sha256': hashes[image],
                          'dimensions': [1000, 659], 'xywh': [875, 250, 105, 215],
                          'candidate': '1608',
                          'reading': 'Visible after clockwise quarter-turn; date of inscription, source and function unverified.'},
    'finnish_catalogue': {'url': 'https://fragmenta.kansalliskirjasto.fi/handle/10024/1299?show=full',
                          'access': 'Search-indexed text, not direct image or verified print.',
                          'folio_8': 'A heading attributed to f.8 describes Hindrich Jonszon, the Viborg garrison and 1603–1604; exact historical spelling and side marker need source-image review.'},
    'limits': 'Catalogue account years are not binding dates. Distinct descriptions do not exclude multiple uses, an original folio divided between wrappers, catalogue error, or physical overlap; they do not decide medieval book identity.',
    'sources_sha256': {str(p.relative_to(root)): digest for p, digest in hashes.items()},
    'independent_confirmation': False,
}
(root / 'research/continuation_113/results.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'checked_references': list(rows), 'swedish_year': 1608, 'finnish_year': 1604, 'image_box': [875, 250, 105, 215]}, indent=2))
