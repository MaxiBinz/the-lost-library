"""Check retained provenance and caveats; web OCR and original manuscripts are not replayed."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def read(path):
    return json.loads((ROOT / path).read_text())

def main():
    result = read('research/continuation_72/results.json')
    sources = read('research/continuation_72/sources.json')
    annotations = read('research/continuation_65/observations.json')['annotations']
    ending = next(a for a in annotations if a['id'] == 'I65-8201-ending')
    assert hashlib.sha256((ROOT / ending['target']['source']).read_bytes()).hexdigest() == ending['sha256']
    assert ending['literal_candidate'] in result['local_target']
    assert 'erat decora nimis' in result['comparison'] and 'decora nimis enituit' in result['published_target']
    assert 'not independent medieval witnesses' in result['limits']
    assert {s['id'] for s in sources['sources']} == {'grajewski-2022', 'fr8201', 'lmlo-ba49', 'ah52-386', 'ah-source-index'}
    for key in ('fr20106_inspected', 'barbara_medieval_original_inspected', 'printed_page_image_inspected',
                'barbara_office_in_fr20106_established', 'published_association_refuted',
                'new_historical_discovery', 'independent_confirmation'):
        assert not result[key]
    assert result['new_source_images'] == result['new_download_bytes'] == 0
    states = {x['id']: x['decision_state'] for x in read('data/lead_register.v1.json')['leads']}
    assert states == read('research/continuation_69/decisions.before.json')['states']
    print(json.dumps({'target_image_checksum_verified': True, 'historical_text_replayed': False,
                      'independent_witnesses_inferred': False, 'decisions_unchanged': True}))

if __name__ == '__main__':
    main()
