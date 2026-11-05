"""Record the observed Fr8994 word boundary; no Finnish image is synthesized."""
import hashlib
import json
from pathlib import Path
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PATH4 = 'data/images/mpo-8994-capture-4-1808px.jpg'
PATH1 = 'data/images/mpo-8994-capture-1-1802px.jpg'
SITES = [
    ('I40-8994-nocte', PATH4, [365, 225, 1115, 65],
     'gius mar tir ola uus nocte precedente diem',
     '[Egre]gius martyr Olavus nocte precedente diem',
     'The first complete lower text row continues the Egregius initial/first syllables visible above it. It reads nocte precedente diem; the supplied incipit prefix is not silently treated as ink in this crop.'),
    ('I40-8994-passion', PATH4, [365, 385, 1110, 70],
     'su e pas sio nis splen dore a mictum',
     'sue passionis splendore amictum',
     'The next row includes sue before passionis. The literal target reading is retained separately from concordances which may omit or normalize a word.'),
    ('I40-8994-contemplatur', PATH4, [365, 545, 1125, 75],
     'Contempla tur ihesum a stantem si bi ac',
     'Contemplatur Ihesum astantem sibi ac',
     'The row continues the Egregius responsory. The christogram is expanded provisionally as Ihesum; no melody or unique variant is claimed.'),
    ('I40-8994-tempus-est', PATH4, [365, 700, 1135, 80],
     'di centem . Veni ca re me us tempus est',
     'dicentem. Veni care meus tempus est',
     'The last visible text row in capture4 ends tempus est. A concordance continues ut laborum, exactly the opening reported for IV156 ff9–11. This supports a conditional textual-fit test, not a verified leaf boundary, physical adjacency or join.'),
    ('I40-8994-exultabat', PATH1, [300, 350, 1150, 230],
     'Exulta bat rex plus quam credi po test iam labo ris sui suauissimos fructus pregus[...]',
     'Exultabat rex plusquam credi potest iam laboris sui suavissimos fructus pregus[...]',
     'The observed upper span includes the verse of the preceding Florebat fides responsory, before the already observed third-nocturn rubric. The captured span is broader than the third-nocturn incipits alone; complete capture/side mapping remains unresolved.'),
]


def main():
    record = next(r for r in json.loads((ROOT / 'data/fragments.json').read_text()) if r['id'] == 'mpo-8994')
    captures = {c['path']: c for c in record['captures']}
    annotations = []
    panels = []
    for ident, path, box, literal, normalized, meaning in SITES:
        capture = captures[path]
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == capture['sha256']
        x, y, w, h = box
        with Image.open(ROOT / path) as im:
            assert im.size == (capture['width'], capture['height'])
            assert 0 <= x < x+w <= im.width and 0 <= y < y+h <= im.height
            panels.append((ident, path, box, im.crop((x, y, x+w, y+h)).convert('RGB')))
        annotations.append({'id': ident, 'type': 'Annotation', 'motivation': 'describing',
            'body': {'type': 'TextualBody', 'value': meaning, 'language': 'en'},
            'target': {'source': path, 'selector': {'type': 'FragmentSelector',
                'conformsTo': 'http://www.w3.org/TR/media-frags/', 'value': 'xywh='+','.join(map(str, box))}},
            'fragment_id': record['id'], 'source_url': capture['url'], 'sha256': capture['sha256'],
            'image_dimensions': [capture['width'], capture['height']], 'rights_url': record['rights_url'],
            'literal_candidate': literal, 'normalized_candidate': normalized,
            'observer': 'Codex AI exploratory source reading, 2026-10-27', 'independent_confirmation': False,
            'interpretation_limits': ['Local manuscript pixels and catalogue/concordance text are separate evidence bases.',
                'No Finnish original inspected; capture4 is not independently assigned to a complete medieval surface.',
                'No physical join, immediate adjacency, complete numbering correspondence, new codex or scholarly novelty established.']})
    (HERE / 'observations.json').write_text(json.dumps({'version': '1.0.0', 'assessment_date': '2026-10-27',
        'annotations': annotations}, ensure_ascii=False, indent=2)+'\n')
    selected = [p for p in panels if p[0] != 'I40-8994-exultabat']
    proof = Image.new('RGB', (1240, sum(crop.height+65 for _, _, _, crop in selected)+100), 'white')
    draw = ImageDraw.Draw(proof);offset = 0
    for ident, path, box, crop in selected:
        draw.text((10, offset+5), ident+' / '+path, fill='black')
        draw.text((10, offset+22), 'xywh='+str(box)+'; original source pixels; no generated detail', fill='black')
        proof.paste(crop, (10, offset+45));offset += crop.height+65
    for i, line in enumerate([
        'Observed: ... Veni care meus tempus est | Expected continuation: ut laborum ...',
        'The IV156 catalogue reports ut laborum at the opening of ff9-11; its original image remains uninspected.',
        'This is a conditional textual-fit candidate, not a physical join or an established book attribution.'
    ]):draw.text((10, offset+12+i*22), line, fill='black')
    proof.save(HERE / 'boundary-review.png')
    print(json.dumps({'regions': len(annotations), 'source_hashes_and_bounds_verified': True,
                      'Finnish_original_verified': False, 'physical_adjacency_established': False}))


if __name__ == '__main__':
    main()
