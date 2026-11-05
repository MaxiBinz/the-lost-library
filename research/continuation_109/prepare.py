#!/usr/bin/env python3
"""Prepare a reproducible, stratified, image-name-masked local check."""
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import random
from openpyxl import load_workbook

ROOT = Path(__file__).resolve().parents[2]
COMBINED = ROOT / 'research/continuation_26/bompac/Stockholm-Helsinki-Frs-Combined-BOMPAC.xlsx'
RAW = ROOT / 'research/continuation_26/bompac/raw_metadata/MPO_BOMPAC.xlsx'
assert hashlib.sha256(COMBINED.read_bytes()).hexdigest() == 'b6c13ca276372492927020ccdb1edf607b76028066f815c5cf426121238398c3'
assert hashlib.sha256(RAW.read_bytes()).hexdigest() == '7f2e75d15b5b0f162108c1118dbfd8af4b9919602cda41852e67baafeb510bd9'

def rows(path, sheet):
    wb = load_workbook(path, read_only=True, data_only=True)
    it = wb[sheet].iter_rows(values_only=True)
    next(it)
    header = next(it)
    for row in it:
        yield dict(zip(header, row))
    wb.close()

raw = defaultdict(list)
for r in rows(RAW, 'Blad1'):
    if r.get('Row_exclusion') == 'Include row' and isinstance(r.get('fragment_id'), int):
        raw[r['fragment_id']].append(r)
local = {}
for f in json.loads((ROOT / 'data/fragments.json').read_text()):
    if f['id'].startswith('mpo-'):
        p = ROOT / (f.get('image_path') or '')
        if p.is_file() and f.get('image', {}).get('width', 0) >= 600:
            local[int(f['id'][4:])] = f

strata = defaultdict(list)
for r in rows(COMBINED, 'Sheet1'):
    n = r.get('Fr_number')
    if (r.get('Database') != 'MPO' or r.get('Row_exclusion') != 'Include row'
            or not isinstance(n, int) or r.get('Fr_reference') != f'Fr {n}'
            or n in (607, 8994, 25592) or n not in local or len(raw[n]) != 1):
        continue
    orig, comb = raw[n][0].get('spaltenzahl'), r.get('Columns')
    if orig in (1, 2) and comb in (1, 2):
        group = 'raw2_combined1' if (orig, comb) == (2, 1) else ('raw1_combined2' if (orig, comb) == (1, 2) else 'agreement')
        f = local[n]
        strata[group].append({'fragment': n, 'original_columns': orig, 'combined_columns': comb,
                              'leaves': r.get('No_of_leaves'), 'image': f['image_path'],
                              'sha256': f['image']['sha256'], 'stratum': group})
assert len(strata['raw1_combined2']) >= 6 and len(strata['agreement']) >= 3, {k: len(v) for k, v in strata.items()}
rng = random.Random(20261104)
chosen = []
for group, count in (('raw1_combined2', 6), ('agreement', 3)):
    chosen.extend(rng.sample(sorted(strata[group], key=lambda x: x['fragment']), count))
rng.shuffle(chosen)
scratch = Path('/private/tmp/lost_library_masked_columns_109')
scratch.mkdir(exist_ok=True)
for i, item in enumerate(chosen):
    item['label'] = chr(65 + i)
    target = ROOT / item['image']
    assert hashlib.sha256(target.read_bytes()).hexdigest() == item['sha256']
    link = scratch / f"{item['label']}.jpg"
    if link.is_symlink():
        link.unlink()
    if link.exists():
        raise RuntimeError(f'Unexpected existing non-symlink: {link}')
    link.symlink_to(target)
out = {'seed': 20261104, 'selection': 'Six random local raw-one/combined-two cases and three agreements; previous visual examples excluded. No other-direction candidate was available locally.',
       'pool_sizes': {k: len(v) for k, v in strata.items()}, 'items': chosen,
       'limits': 'Convenience sample of retained photos; capture and edge coverage vary. Does not estimate population error or substitute for expert review.'}
(ROOT / 'research/continuation_109/selection.json').write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n')
print('Masked images ready:', ', '.join(str(scratch / f'{chr(65+i)}.jpg') for i in range(len(chosen))))
