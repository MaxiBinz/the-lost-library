#!/usr/bin/env python3
"""Verify the original-image hash and region bounds, not the disputed reading."""
import hashlib
import json
from pathlib import Path
from PIL import Image

root = Path(__file__).resolve().parents[2]
annotation = json.loads((root / 'research/continuation_97/observations.json').read_text())['annotations'][0]
image = root / annotation['target']['source']
assert hashlib.sha256(image.read_bytes()).hexdigest() == annotation['sha256']
with Image.open(image) as im:
    assert list(im.size) == annotation['image_dimensions']
    x, y, w, h = map(int, annotation['target']['selector']['value'].removeprefix('xywh=').split(','))
    assert 0 <= x < x + w <= im.width and 0 <= y < y + h <= im.height
print('Original image identity and annotation bounds verified; reading remains unverified.')
