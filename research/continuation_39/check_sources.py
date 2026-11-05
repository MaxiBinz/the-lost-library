"""Check retained sources and uncertainty propagation; not independent music review."""
import argparse
import hashlib
import json
from pathlib import Path
from PIL import Image

from compare_notes import compare

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def sha(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--require-private', action='store_true')
    args = parser.parse_args()
    readings = json.loads((HERE / 'readings.v3.json').read_text())
    comparison = json.loads((HERE / 'comparison.json').read_text())
    assert comparison == compare(readings)
    assert comparison['potential_aligned_positions'] == 14
    assert (comparison['provisional_agree'], comparison['unresolved'], comparison['different']) == (12, 2, 0)
    for source in readings['sources'].values():
        assert sha(ROOT / source['path']) == source['sha256']
        with Image.open(ROOT / source['path']) as im:
            for events in source['phrases'].values():
                for event in events:
                    x, y = event['pixel']
                    assert 0 <= x < im.width and 0 <= y < im.height
    annotations = json.loads((HERE / 'observations.json').read_text())['annotations']
    for annotation in annotations:
        assert sha(ROOT / annotation['target']['source']) == annotation['sha256']
        with Image.open(ROOT / annotation['target']['source']) as im:
            assert list(im.size) == annotation['image_dimensions']
            x, y, w, h = map(int, annotation['target']['selector']['value'][5:].split(','))
            assert 0 <= x < x+w <= im.width and 0 <= y < y+h <= im.height
    frozen = json.loads((ROOT / 'research/continuation_33/results.json').read_text())['frozen_inputs']
    assert frozen == {path: sha(ROOT / path) for path in frozen}
    assert sha(ROOT / 'data/fragments.json') == 'eb85c5e64fcd296f931cceb95050f0c36ff1f2e1cf0a9ba874827477c4c867ed'
    method = json.loads((HERE / 'method_receipt.json').read_text())
    urberg = json.loads((ROOT / 'research/continuation_37/results.json').read_text())['previously_published']['Urberg2016']
    private = [(method['path'], method['sha256']), (urberg['private_pdf'], urberg['sha256'])]
    missing = []
    for path, expected in private:
        if (ROOT / path).exists():
            assert sha(ROOT / path) == expected
        else:
            missing.append(path)
    if args.require_private:
        assert not missing, missing
    result = json.loads((HERE / 'results.json').read_text())
    assert not any(result[key] for key in ['melodic_identity_established', 'full_melody_verified',
        'new_codex_attribution', 'whole_office_recension_established', 'novelty_cleared', 'independent_confirmation'])
    print(json.dumps({'regions_checked': len(annotations), 'note_anchors_checked': 28,
        'provisional_agree': 12, 'unresolved': 2, 'frozen_and_core_inputs_unchanged': True,
        'excluded_private_reading_copies_missing_here': missing,
        'scope': 'Checks provenance, bounds and declared comparison arithmetic, not music truth or novelty.'}))


if __name__ == '__main__':
    main()
