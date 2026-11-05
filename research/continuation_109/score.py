#!/usr/bin/env python3
"""Report masked-image readings without turning unassessable cases into errors."""
from collections import Counter
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
selection = json.loads((ROOT / 'research/continuation_109/selection.json').read_text())
observations = json.loads((ROOT / 'research/continuation_109/blind_observations.json').read_text())
by_label = {r['label']: r for r in observations['readings']}
assert len(by_label) == len(selection['items']) == 9
summary = Counter()
for item in selection['items']:
    assert hashlib.sha256((ROOT / item['image']).read_bytes()).hexdigest() == item['sha256']
    observed = by_label[item['label']]['visible_columns']
    stratum = item['stratum']
    summary[f'{stratum}_selected'] += 1
    if observed is None:
        summary[f'{stratum}_unassessable'] += 1
    else:
        summary[f'{stratum}_assessable'] += 1
        summary[f'{stratum}_matches_raw'] += observed == item['original_columns']
        summary[f'{stratum}_matches_combined'] += observed == item['combined_columns']
print(json.dumps(dict(summary), indent=2))
