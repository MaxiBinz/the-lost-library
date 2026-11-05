"""Check provenance and limits only; browser-viewed manuscript pixels are not replayed."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def read(path):
    return json.loads((ROOT / path).read_text())

def main():
    result = read('research/continuation_70/results.json')
    sources = read('research/continuation_70/sources.json')
    assert {x['folio'] for x in result['source_observations']} == {'122r', '125v', '126r'}
    assert result['vatican_selected_original_views_inspected']
    for key in ['full_offices_collated', 'identical_full_rubrics_verified', 'fr20106_inspected', 'published_exclusion_refuted', 'target_same_codex_proved', 'new_discovery', 'independent_confirmation']:
        assert not result[key]
    assert result['saved_new_source_images'] == result['saved_download_bytes'] == 0
    assert 'no source screenshots or files saved' in sources['vatican_viewer']['access']
    graph = read('data/knowledge.v1.json')
    claim = next(c for c in graph['claims'] if c['id'] == 'interpretation:E70-pal527-opening')
    assert claim['status'] == 'unresolved' and not claim['exact_duplicate_rubric_verified']
    assert not claim['original_images_saved'] and not claim['independent_confirmation']
    states = {x['id']: x['decision_state'] for x in read('data/lead_register.v1.json')['leads']}
    assert states == read('research/continuation_69/decisions.before.json')['states']
    print(json.dumps({'folio_locators_recorded': True, 'images_saved': False, 'reading_replayed': False, 'target_identity_unresolved': True, 'decisions_unchanged': True}))

if __name__ == '__main__':
    main()
