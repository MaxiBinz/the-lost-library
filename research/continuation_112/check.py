"""Check the image identities and bounds, not transcription or codex identity."""
import hashlib
import json
from pathlib import Path
from PIL import Image

root = Path(__file__).resolve().parents[2]
data = json.loads((root / 'research/continuation_112/observations.json').read_text())
for item in data['annotations']:
    path = root / item['path']
    assert hashlib.sha256(path.read_bytes()).hexdigest() == item['sha256']
    with Image.open(path) as im:
        assert list(im.size) == item['dimensions']
        x, y, w, h = item['xywh']
        assert x >= 0 and y >= 0 and x + w <= im.width and y + h <= im.height
assert not data['independent_confirmation']
print(f"Verified {len(data['annotations'])} image hashes and selectors; readings are not independently checked.")
