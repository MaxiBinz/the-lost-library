"""Serialize the inspected C23 69r regions; hashes do not validate readings."""
import hashlib
import json
from pathlib import Path
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE = 'research/continuation_38/c23-69r-0139-2200px.jpg'
SITES = [
    ('I38-C23-69r-incipit', [210, 450, 1320, 260],
     'O maria stans sub cruce [...]', 'O Maria stans sub cruce [...]',
     'The explicitly labelled 69r image contains the candidate incipit itself. Fr 20274 retains only its ending, so its missing incipit is not supplied as a literal target reading.'),
    ('I38-C23-69r-ending-a', [210, 1040, 1320, 410],
     '[do]lor cessit cū surrexit nobis vite spem porrex / it presi dens in gloria fac nos virgo sue',
     'Dolor cessit cum surrexit nobis vite spem porrexit presidens in gloria; Fac nos Virgo sue [...]',
     'The actual replacement page has the differentiating shorter ending, including cum, nobis vite spem porrexit and the Fac nos petition. The target agrees at the selected lexical level; this common version is not a codex fingerprint.'),
    ('I38-C23-69r-ending-b', [210, 1420, 1320, 410],
     'mortis et doloris tui for tis feruere me / mo ria alle luya alle luya',
     'mortis et doloris tui fortis feruere memoria; Alleluia, alleluia',
     'The source ending reads feruere, in agreement with the provisional target reading. Notation is visible, but a verified note-by-note collation and melodic identity have not been established.'),
]


def sha(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def main():
    receipt = json.loads((HERE / 'download_receipt.json').read_text())
    assert receipt['saved'] and receipt['bytes_received'] <= 50_000_000
    assert sha(ROOT / receipt['local_path']) == receipt['sha256']
    derivative = receipt['derivative']
    assert sha(ROOT / SOURCE) == derivative['sha256']
    annotations = []
    with Image.open(ROOT / SOURCE) as source:
        assert list(source.size) == derivative['dimensions']
        for ident, box, literal, normalized, meaning in SITES:
            x, y, w, h = box
            assert 0 <= x < x + w <= source.width and 0 <= y < y + h <= source.height
            annotations.append({
                'id': ident, 'type': 'Annotation', 'motivation': 'describing',
                'body': {'type': 'TextualBody', 'value': meaning, 'language': 'en'},
                'target': {'source': SOURCE, 'selector': {'type': 'FragmentSelector',
                    'conformsTo': 'http://www.w3.org/TR/media-frags/',
                    'value': 'xywh=' + ','.join(map(str, box))}},
                'fragment_id': 'uub-c23-0139', 'source_url': receipt['url'],
                'sha256': derivative['sha256'], 'image_dimensions': list(source.size),
                'rights_url': receipt['rights_url'], 'literal_candidate': literal,
                'normalized_candidate': normalized,
                'observer': 'Codex AI exploratory source reading, 2026-10-27',
                'independent_confirmation': False,
                'interpretation_limits': ['Literature-assisted AI reading; no independent reader.',
                    'Selected lexical comparison only; no melodic identity, whole-office recension, date, copying direction or same-codex inference.'],
            })
    (HERE / 'observations.json').write_text(json.dumps({'version': '1.0.0',
        'assessment_date': '2026-10-27', 'annotations': annotations}, ensure_ascii=False, indent=2) + '\n')
    # This side-by-side proof uses only declared PDM manuscript crops. The
    # target panel is E37's complete three-row reading, not synthetic restoration.
    panels = []
    with Image.open(ROOT / 'data/images/mpo-20274-capture-1-1831px.jpg') as target:
        panels.append(('Fr 20274: surviving ending and notation', target.crop((225, 270, 1745, 960))))
    with Image.open(ROOT / SOURCE) as source:
        panels.append(('C23: explicitly labelled 69r, same selected text; pitches uncollated', source.crop((210, 1040, 1530, 1830))))
    proof = Image.new('RGB', (1560, sum(im.height + 55 for _, im in panels)), 'white')
    draw = ImageDraw.Draw(proof)
    y = 0
    for label, crop in panels:
        draw.text((10, y + 8), label, fill='black')
        draw.text((10, y + 24), 'Original manuscript pixels; no generated detail', fill='black')
        proof.paste(crop, (10, y + 45))
        y += crop.height + 55
    proof.save(HERE / 'replacement-comparison.png')
    print(json.dumps({'regions': len(annotations), 'original_and_derivative_hashes_verified': True,
                      'readings_independently_validated': False}))


if __name__ == '__main__':
    main()
