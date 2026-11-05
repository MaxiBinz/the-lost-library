"""Check reproducibility and claim limits, not the catalogue's historical truth."""
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def read(path):
    return json.loads((ROOT / path).read_text())

def main():
    result = read('research/continuation_76/results.json')
    subset = read(result['candidate_rows_path'])
    source = ROOT / subset['source']
    assert hashlib.sha256(source.read_bytes()).hexdigest() == subset['source_sha256']
    with source.open(encoding='utf-8-sig', newline='') as f:
        rows = sorted((r for r in csv.DictReader(f) if r.get('ccmsignum', '').strip() == 'Ant 49'),
                      key=lambda r: int(r['signatur']))
    assert [r['signatur'] for r in rows] == [r['signatur'] for r in subset['rows']]
    assert all(all(row[k] == original.get(k, '') for k in row) for row, original in zip(subset['rows'], rows))
    assert [r['signatur'] for r in rows if 'anna' in r['inhalt'].casefold()] == ['8073']
    for key in ('luebeck_original_inspected', 'exact_comparator_adjacency_verified', 'melody_compared',
                'other_anne_absence_established', 'new_codex_relationship', 'new_discovery', 'independent_confirmation'):
        assert not result[key]
    assert result['new_source_images'] == result['new_download_bytes'] == 0
    states = {x['id']: x['decision_state'] for x in read('data/lead_register.v1.json')['leads']}
    assert states == read('research/continuation_69/decisions.before.json')['states']
    graph = read('data/knowledge.v1.json')
    claim = next(c for c in graph['claims'] if c['id'] == 'interpretation:E76-8073-luebeck-control')
    assert claim['status'] == 'unresolved' and not claim['comparator_original_inspected'] and not claim['melody_compared']
    assert set(claim['supports']) == {'evidence:' + i for i in result['source_regions']}
    print(json.dumps({'catalogue_rows_reproduced': len(rows), 'source_manuscript_inspected': False,
                      'historical_claim_independently_verified': False, 'decisions_unchanged': True}))

if __name__ == '__main__':
    main()
