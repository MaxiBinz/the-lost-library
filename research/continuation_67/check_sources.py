"""Validate local bookkeeping and boundaries; this does not verify historical sources."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def read(path):
    return json.loads((ROOT / path).read_text())

def main():
    result = read('research/continuation_67/results.json')
    sources = read('research/continuation_67/sources.json')
    graph = read('data/knowledge.v1.json')
    claim = next(c for c in graph['claims'] if c['id'] == 'interpretation:E67-sziget-candidate')
    assert claim['status'] == 'unresolved' and not claim['same_book_proved']
    assert not claim['current_holding_verified'] and not claim['original_inspected']
    for key in ['same_hungarian_book_proved', 'modern_custody_verified', 'hungarian_manuscript_inspected', 'szilagyi_article_read', 'fr20106_image_inspected', 'historical_same_codex_proved', 'new_historical_discovery', 'independent_confirmation']:
        assert not result[key]
    assert result['new_source_images'] == result['new_download_bytes'] == 0
    assert 'private' in sources['gabriel_1942']['limit']
    assert '1851' in sources['almanac_1861']['assertion']
    states = {x['id']: x['decision_state'] for x in read('data/lead_register.v1.json')['leads']}
    assert states == read('research/continuation_67/decisions.before.json')['states']
    assert read('data/resource_audit.json')['working_source_capture_files'] == 209
    print(json.dumps({'crosswalk': 'unresolved', 'original_inspected': False, 'new_discovery': False, 'decisions': 'unchanged'}))

if __name__ == '__main__':
    main()
