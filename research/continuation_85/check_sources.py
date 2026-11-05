"""Check the recorded TEI wording and evidence boundaries, not paleography."""
import hashlib
import json
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
result = json.loads((ROOT / 'research/continuation_85/results.json').read_text())
path = ROOT / result['catalogue']['retained_tei']
assert hashlib.sha256(path.read_bytes()).hexdigest() == result['catalogue']['tei_sha256']
text = ' '.join(' '.join(ET.parse(path).getroot().itertext()).split())
assert result['catalogue']['literal'] in text
assert result['source']['viewer_image_label'] == 'TMMA.FragC_0002_v.jpg'
for key in ('independent_confirmation', 'new_medieval_codex_attribution', 'novelty_cleared',
            'catalogue_correction_confirmed', 'external_correction_submitted', 'frozen_decisions_changed'):
    assert result[key] is False
print('TEI hash, literal catalogue wording and stated review boundaries verified; image reading not tested')
