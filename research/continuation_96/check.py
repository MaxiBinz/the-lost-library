#!/usr/bin/env python3
"""Recompute a post-inspection scale comparison; does not validate its input readings."""
import hashlib
import json
from pathlib import Path

from PIL import Image

root = Path(__file__).resolve().parents[2]
data = json.loads((root / 'research/continuation_96/measurement.json').read_text())
path = root / data['target_image']
assert hashlib.sha256(path.read_bytes()).hexdigest() == data['sha256']
with Image.open(path) as img:
    assert list(img.size) == data['dimensions']
    height = img.height
y0, y1 = data['ruler']['y_pixels']
assert 0 <= y0 < y1 < height
dist_mm = 10 * data['ruler']['distance_cm']
delta_rule = data['sensitivity']['rule_endpoint_each_px']
delta_ruler = data['sensitivity']['ruler_endpoint_each_px']
for n, (top, bottom) in enumerate(data['systems_y_top_bottom'], 1):
    assert 0 <= top < bottom < height
    width = bottom - top
    center = width * dist_mm / (y1 - y0)
    lo = (width - 2 * delta_rule) * dist_mm / (y1 - y0 + 2 * delta_ruler)
    hi = (width + 2 * delta_rule) * dist_mm / (y1 - y0 - 2 * delta_ruler)
    print(f'system {n}: {center:.2f} mm; coordinate illustration {lo:.2f}–{hi:.2f} mm')
print('IV.173 reported: 17 mm; comparison assumes the same staff-height convention')
print('This checks arithmetic and file identity, not line readings or physical accuracy.')
