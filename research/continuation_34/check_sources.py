"""Verify E34's retained regions and test protocol offline; no image editing."""
import hashlib
import json
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent


def main():
    protocol = json.loads((HERE / 'protocol.json').read_text())
    result = json.loads((HERE / 'results.json').read_text())
    annotations = json.loads((HERE / 'observations.json').read_text())['annotations']
    for a in annotations:
        path = a['target']['source']
        assert path in protocol['inputs']
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == a['sha256']
        with Image.open(ROOT / path) as im:
            assert list(im.size) == a['image_dimensions']
            x, y, w, h = map(int, a['target']['selector']['value'][5:].split(','))
            assert 0 <= x < x+w <= im.width and 0 <= y < y+h <= im.height
    assert not result['independent_confirmation'] and not result['novelty_cleared']
    assert result['new_downloads'] == 0
    print(json.dumps({'verified_regions':len(annotations), 'scope':result['scope'], 'side_mapping':'unresolved'}))


if __name__ == '__main__':
    main()
