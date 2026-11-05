"""Verify retained boundary provenance and declared limits, without new access."""
import hashlib
import json
from pathlib import Path
from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def sha(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def main():
    result = json.loads((HERE / 'results.json').read_text())
    sources = json.loads((HERE / 'sources.json').read_text())
    annotations = json.loads((HERE / 'observations.json').read_text())['annotations']
    assert set(result['observations']) == {a['id'] for a in annotations}
    for annotation in annotations:
        assert sha(ROOT / annotation['target']['source']) == annotation['sha256']
        with Image.open(ROOT / annotation['target']['source']) as im:
            assert list(im.size) == annotation['image_dimensions']
            x, y, w, h = map(int, annotation['target']['selector']['value'][5:].split(','))
            assert 0 <= x < x+w <= im.width and 0 <= y < y+h <= im.height
    terminal = next(a for a in annotations if a['id'] == 'I40-8994-tempus-est')
    assert terminal['normalized_candidate'].endswith('tempus est')
    assert result['test_logic']['expected_following_words'] == sources['catalogue_comparisons'][0]['short_exact_opening'] == 'ut laborum'
    # The preceding assertions check declared string consistency, not the
    # literal reading, the indexed source's accuracy or actual physical order.
    assert not any(result[key] for key in ['physical_join_established', 'physical_adjacency_established',
        'new_codex_attribution', 'novelty_cleared', 'independent_confirmation'])
    assert not result['test_logic']['complete_leaf_edge_verified']
    assert not result['test_logic']['signature_successor_verified']
    assert result['signature_prediction']['predicted_next_recto_numeral'] == 'V'
    assert not result['signature_prediction']['prediction_verified']
    receipt = json.loads((HERE / 'download_receipt.json').read_text())
    assert receipt['status'] == 403 and not receipt['saved'] and receipt['bytes_received'] == 0
    frozen = json.loads((ROOT / 'research/continuation_33/results.json').read_text())['frozen_inputs']
    assert frozen == {path: sha(ROOT / path) for path in frozen}
    assert sha(ROOT / 'data/fragments.json') == 'eb85c5e64fcd296f931cceb95050f0c36ff1f2e1cf0a9ba874827477c4c867ed'
    print(json.dumps({'regions_checked': len(annotations), 'frozen_and_core_inputs_unchanged': True,
        'failed_download_not_replayed': True, 'physical_adjacency_established': False,
        'scope': 'Provenance/bounds/declared-string consistency only, not reading truth, novelty or a Finnish source-image check.'}))


if __name__ == '__main__':
    main()
