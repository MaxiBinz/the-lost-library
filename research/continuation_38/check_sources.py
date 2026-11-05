"""Offline provenance/scope checks, separate from reading truth and novelty."""
import hashlib
import json
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent


def sha(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def main():
    receipt = json.loads((HERE / 'download_receipt.json').read_text())
    result = json.loads((HERE / 'results.json').read_text())
    assert 'Folio 69r' in (HERE / 'c23-69r-viewer.ax.txt').read_text()
    assert 'Public Domain Mark' in (HERE / 'c23-record.ax.txt').read_text()
    assert receipt['saved'] and receipt['folio_label'] == 'Folio 69r'
    assert sha(ROOT / receipt['local_path']) == receipt['sha256']
    assert sha(ROOT / receipt['derivative']['path']) == receipt['derivative']['sha256']
    annotations = json.loads((HERE / 'observations.json').read_text())['annotations']
    assert set(result['observations']) == {a['id'] for a in annotations}
    for a in annotations:
        assert sha(ROOT / a['target']['source']) == a['sha256']
        with Image.open(ROOT / a['target']['source']) as im:
            assert list(im.size) == a['image_dimensions']
            x, y, w, h = map(int, a['target']['selector']['value'][5:].split(','))
            assert 0 <= x < x+w <= im.width and 0 <= y < y+h <= im.height
    frozen = json.loads((ROOT / 'research/continuation_33/results.json').read_text())['frozen_inputs']
    assert frozen == {p: sha(ROOT / p) for p in frozen}
    assert not result['new_codex_attribution'] and not result['novelty_cleared']
    assert not result['whole_office_recension_established'] and not result['independent_confirmation']
    assert result['music_test']['state'] == 'unperformed'
    assert not result['music_test']['melodic_identity_established']
    print(json.dumps({'verified_regions': len(annotations), 'original_and_derivative_hashes_verified': True,
                      'folio_and_rights_label_receipts_present': True, 'frozen_inputs_unchanged': True,
                      'scope': 'Provenance and declared claim limits only, not independent reading validation.'}))


if __name__ == '__main__':
    main()
