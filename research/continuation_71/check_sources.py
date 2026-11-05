"""Check catalogue provenance and recorded limits, not manuscript truth."""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def read(path):
    return json.loads((ROOT / path).read_text())

def main():
    with (ROOT / 'research/mpo.csv').open(encoding='utf-8-sig', newline='') as f:
        rows = [r for r in csv.DictReader(f) if r['signatur'] == '20106']
    assert len(rows) == 1
    row = rows[0]
    assert row['blattzahl'] == '1' and row['ccmsignum'] == 'Ant 49'
    assert all(word in row['inhalt'] for word in ('Katharinae', 'Barbarae', 'Novo decurrens lumine'))
    result = read('research/continuation_71/results.json')
    for key in ('fr20106_image_inspected', 'side_order_verified', 'historical_contradiction_established',
                'published_association_refuted', 'published_exclusion_refuted', 'new_discovery',
                'independent_confirmation'):
        assert not result[key]
    assert result['saved_new_source_images'] == result['saved_download_bytes'] == 0
    states = {x['id']: x['decision_state'] for x in read('data/lead_register.v1.json')['leads']}
    assert states == read('research/continuation_69/decisions.before.json')['states']
    print(json.dumps({'catalogue_row_checked': True, 'source_order_verified': False,
                      'historical_contradiction_established': False, 'decisions_unchanged': True}))

if __name__ == '__main__':
    main()
