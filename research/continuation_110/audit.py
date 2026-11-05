#!/usr/bin/env python3
"""Trace current local MPO column metadata to the retained original sources."""
import csv
import copy
import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from openpyxl import load_workbook

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from lost_library.pipeline import normalize_mpo
from lost_library.matching import metadata_score
CSV = ROOT / 'research/mpo.csv'
FRAGMENTS = ROOT / 'data/fragments.json'
RAW = ROOT / 'research/continuation_26/bompac/raw_metadata/MPO_BOMPAC.xlsx'
COMBINED = ROOT / 'research/continuation_26/bompac/Stockholm-Helsinki-Frs-Combined-BOMPAC.xlsx'
EXPECTED = {RAW:'7f2e75d15b5b0f162108c1118dbfd8af4b9919602cda41852e67baafeb510bd9',
            COMBINED:'b6c13ca276372492927020ccdb1edf607b76028066f815c5cf426121238398c3'}
for p, h in EXPECTED.items():
    assert hashlib.sha256(p.read_bytes()).hexdigest() == h

def read_sheet(p, name):
    wb = load_workbook(p, read_only=True, data_only=True)
    it = wb[name].iter_rows(values_only=True)
    next(it)
    h = next(it)
    for values in it:
        yield dict(zip(h, values))
    wb.close()

with CSV.open(encoding='utf-8-sig', newline='') as f:
    local_rows = defaultdict(list)
    for row in csv.DictReader(f):
        local_rows[row['signatur']].append(row)
raw_rows = defaultdict(list)
for row in read_sheet(RAW, 'Blad1'):
    if isinstance(row.get('fragment_id'), int) and row.get('Row_exclusion') == 'Include row':
        raw_rows[str(row['fragment_id'])].append(row)
combined_rows = defaultdict(list)
for row in read_sheet(COMBINED, 'Sheet1'):
    if row.get('Database') == 'MPO' and row.get('Row_exclusion') == 'Include row':
        if isinstance(row.get('Fr_number'), int) and row.get('Fr_reference') == f"Fr {row['Fr_number']}":
            combined_rows[str(row['Fr_number'])].append(row)

records = [r for r in json.loads(FRAGMENTS.read_text()) if r['id'].startswith('mpo-')]
assert len({r['id'] for r in records}) == len(records)
counts = Counter()
issues = []
examples = []
for record in records:
    key = record['id'][4:]
    counts['local_mpo_records'] += 1
    if len(local_rows[key]) != 1:
        counts['csv_missing_or_duplicate'] += 1
        continue
    row = local_rows[key][0]
    expected = normalize_mpo(row)['columns']
    stored = record.get('normalized', {}).get('columns')
    counts['csv_exact_match'] += 1
    if expected == stored:
        counts['stored_equals_current_csv_parser'] += 1
    else:
        counts['stored_differs_current_csv_parser'] += 1
        issues.append({'id':record['id'], 'csv':row.get('spaltenzahl'), 'parsed':expected, 'stored':stored})
    if len(raw_rows[key]) == 1:
        original = raw_rows[key][0].get('spaltenzahl')
        original_string = '' if original is None else str(original).strip()
        if row.get('spaltenzahl', '').strip() == original_string:
            counts['local_csv_matches_raw_workbook_string'] += 1
        else:
            counts['local_csv_differs_raw_workbook_string'] += 1
            issues.append({'id':record['id'], 'csv':row.get('spaltenzahl'), 'raw_workbook':original})
    else:
        counts['raw_missing_or_duplicate'] += 1
    if len(combined_rows[key]) == 1:
        combined = combined_rows[key][0].get('Columns')
        if isinstance(stored, int) and isinstance(combined, int):
            counts['stored_and_combined_numeric'] += 1
            if stored == combined:
                counts['stored_equals_combined_numeric'] += 1
            else:
                counts['stored_differs_combined_numeric'] += 1
                examples.append({'id':record['id'], 'stored':stored, 'combined':combined})
        else:
            counts['stored_or_combined_nonnumeric'] += 1
    else:
        counts['combined_missing_or_duplicate'] += 1

by_id = {r['id']: r for r in json.loads(FRAGMENTS.read_text())}
matches_path = ROOT / 'data/matches.json'
counterfactual = Counter()
changed_pairs = []
for match in json.loads(matches_path.read_text()):
    left, right = by_id[match['left_id']], by_id[match['right_id']]
    first, second = copy.deepcopy(left), copy.deepcopy(right)
    replaced = False
    for record in (first, second):
        if not record['id'].startswith('mpo-'):
            continue
        key = record['id'][4:]
        if len(combined_rows[key]) != 1:
            continue
        alternative = combined_rows[key][0].get('Columns')
        if isinstance(alternative, int) and isinstance(record['normalized'].get('columns'), int):
            record['normalized']['columns'] = alternative
            replaced = True
    if not replaced:
        continue
    counterfactual['candidate_rows_with_numeric_substitution'] += 1
    original = metadata_score(left, right)[0]
    alternate = metadata_score(first, second)[0]
    frozen = match.get('scores', {}).get('metadata')
    if isinstance(frozen, (int, float)) and abs(original - frozen) < 1e-12:
        counterfactual['recomputed_baseline_equals_saved_metadata'] += 1
    if abs(original - alternate) > 1e-12:
        counterfactual['metadata_score_changed'] += 1
        changed_pairs.append({'left':left['id'], 'right':right['id'], 'current':original, 'counterfactual':alternate})
    else:
        counterfactual['metadata_score_unchanged'] += 1

out = {'counts':dict(counts), 'issues':issues, 'stored_vs_combined_examples':examples,
       'counterfactual':dict(counterfactual), 'counterfactual_changed_pairs':changed_pairs,
       'inputs':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [CSV,FRAGMENTS,RAW,COMBINED,matches_path]},
       'scope':'Current saved local MPO records, current ingestion parser and existing 170 candidate rows. Counterfactual substitutes published combined values in copies only; it does not change saved data, rank or model performance, replay historical model runs, prove every earlier analysis unaffected, or verify every image.'}
(ROOT/'research/continuation_110/results.json').write_text(json.dumps(out, ensure_ascii=False, indent=2)+'\n')
print(json.dumps({'local_records':dict(counts), 'counterfactual':dict(counterfactual)},indent=2))
