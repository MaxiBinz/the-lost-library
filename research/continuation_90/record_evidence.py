"""Pin the observed Fr 10370 reuse heading and the separate catalogue comparison."""
import hashlib
import json
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).parent
CAPTURE = 'data/images/mpo-10370-capture-4-1742px.jpg'
REGION = 'I51-10370-reuse-heading'


def main():
    fragments = json.loads((ROOT / 'data/fragments.json').read_text())
    obj = next(item for item in fragments if item['id'] == 'mpo-10370')
    capture = next(item for item in obj['captures'] if item['path'] == CAPTURE)
    source = ROOT / CAPTURE
    digest = hashlib.sha256(source.read_bytes()).hexdigest()
    assert digest == capture['sha256']
    with Image.open(source) as image:
        assert image.size == (capture['width'], capture['height'])
    existing = json.loads((ROOT / 'research/continuation_51/observations.json').read_text())
    annotation = next(item for item in existing['annotations'] if item['id'] == REGION)
    assert annotation['target']['source'] == CAPTURE
    result = {
        'date': '2026-11-02',
        'observation_type': 'AI visual reading, post-exposure and reference-assisted',
        'source_image': CAPTURE,
        'source_url': capture['url'],
        'source_sha256': digest,
        'reused_annotation': REGION,
        'view_transform': '90 degrees counter-clockwise; original-pixel region remains in the existing annotation',
        'visible_candidates': [
            'A large heading provisionally reads Christiern Philipsson[s?]; final letters are obscured by a folded corner.',
            'The following line contains a provision-account phrase, provisionally Reckenskap för Proffianten, and Finlandh.',
            'A smaller line provisionally includes 1610 and 1611; a large 1610 is separately visible below.',
        ],
        'printed_comparator': {
            'source': 'https://www.doria.fi/bitstream/handle/10024/100895/Verzeichnis_der_mittelalterlic.pdf?sequence=1',
            'locator': 'Haapanen 1925 p.39 no.64, extracted PDF text',
            'scope': 'A truncated provision-account description contains Christiern Philipsson, Finland and 1611; it does not identify a leaf for that heading in the read passage.',
        },
        'interpretation': 'Shared name, account subject, Finland and 1611 make a related-account comparison specific; they do not establish the same surviving account or physical parchment object.',
        'alternatives': ['Distinct accounts by one person with similar headings', 'Different same-named people',
                         'Repeated title or copied administrative text', 'Inaccurate reading or attribution',
                         'A physical cross-identification or an association requiring further archival evidence'],
        'next_test': 'Compare an authenticated image or exact archival record of II.64 ff.6–7 with this heading, including its handwriting, complete wording and account provenance; assess whether the descriptions refer to distinct accounts or an error in object mapping.',
        'finnish_original_seen': False, 'independent_reading': False,
        'same_account_proved': False, 'same_object_proved': False, 'new_codex_established': False,
    }
    (HERE / 'results.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'capture_sha256_valid': True, 'reused_region': REGION, 'source_dimensions': list(image.size)}))


if __name__ == '__main__':
    main()
