"""Check correction provenance and source boundaries, not the historical reading."""
import hashlib
import json
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]

def read(path):
    return json.loads((ROOT / path).read_text())

def main():
    annotation = read('research/continuation_69/observations.json')['annotations'][0]
    image_path = ROOT / annotation['target']['source']
    assert hashlib.sha256(image_path.read_bytes()).hexdigest() == annotation['sha256']
    with Image.open(image_path) as image:
        width, height = image.size
    x, y, w, h = map(int, annotation['target']['selector']['value'][5:].split(','))
    assert 0 <= x < x + w <= width and 0 <= y < y + h <= height
    graph = read('data/knowledge.v1.json')
    original = next(e for e in graph['evidence'] if e['annotation_id'] == 'I49-8304-opening')
    assert original['superseded_by'] == 'evidence:I69-8304-opening-corrected'
    assert 'sollempnitas' in original['original_annotation']['literal_candidate']
    assert 'sollempni[a?]' in original['literal_candidate']
    assert any(e['annotation_id'] == annotation['id'] for e in graph['evidence'])
    result = read('research/continuation_69/results.json')
    for field in ['target_fr20106_inspected', 'vatican_manuscript_inspected', 'same_explicit_rubric_verified', 'published_exclusion_refuted', 'target_same_codex_proved', 'new_discovery', 'independent_confirmation']:
        assert not result[field]
    states = {x['id']: x['decision_state'] for x in read('data/lead_register.v1.json')['leads']}
    assert states == read('research/continuation_69/decisions.before.json')['states']
    receipt = read('research/continuation_69/download_receipt.json')
    assert receipt['attempts'] == 1 and receipt['bytes_saved'] == 0
    print(json.dumps({'earlier_reading_preserved': True, 'supersession_visible': True, 'historical_claims_unverified': True, 'decisions_unchanged': True}))

if __name__ == '__main__':
    main()
