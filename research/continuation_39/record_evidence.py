"""Retain five source regions and a PDM-only note-position inspection figure."""
import hashlib
import json
from pathlib import Path
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SITES = [
    ('I39-target-opening-signs', 'target', None, [225, 275, 340, 260],
     'Opening signs and notes above Dolor cessit cum remain unclassified in this test; no absolute pitch or complete opening transcription is asserted.'),
    ('I39-target-nobis', 'target', 'nobis-vite-spem', [900, 275, 415, 260],
     'Selected Nobis vite spem staff positions are provisionally compatible with C23; the upper vi event remains uncertain. No exact seven-note or full-melody identity is accepted.'),
    ('I39-C23-nobis', 'c23', 'nobis-vite-spem', [830, 1035, 415, 230],
     'C23 Nobis vite spem supplies the reference contour. The vi upper event was clarified with the published score after retaining v1; this is literature-assisted, not independent adjudication.'),
    ('I39-target-petition', 'target', 'fac-nos-virgo', [690, 520, 365, 235],
     'Selected Fac nos Virgo staff positions are provisionally compatible with C23. The upper nos event lies between nominal staff positions and remains unresolved, rather than declared a variant.'),
    ('I39-C23-petition', 'c23', 'fac-nos-virgo', [925, 1250, 430, 225],
     'C23 Fac nos Virgo provides a provisional relative contour of 0,1,2,3,3,1,0. These numbers are diatonic staff steps within this window, not semitones or absolute pitches.'),
]


def main():
    readings = json.loads((HERE / 'readings.v3.json').read_text())
    records = json.loads((ROOT / 'data/fragments.json').read_text()) + json.loads((ROOT / 'data/comparison_sources.v1.json').read_text())
    records = {record['id']: record for record in records}
    annotations = []
    panels = []
    for ident, source_key, phrase, box, meaning in SITES:
        source = readings['sources'][source_key]
        path = ROOT / source['path']
        assert hashlib.sha256(path.read_bytes()).hexdigest() == source['sha256']
        record = records['mpo-20274' if source_key == 'target' else 'uub-c23-0139']
        capture = next(c for c in record['captures'] if c['path'] == source['path'])
        x, y, w, h = box
        with Image.open(path) as original:
            assert 0 <= x < x+w <= original.width and 0 <= y < y+h <= original.height
            crop = original.crop((x, y, x+w, y+h)).convert('RGB')
            dimensions = list(original.size)
        positions = source['phrases'].get(phrase, []) if phrase else []
        draw = ImageDraw.Draw(crop)
        for event in positions:
            px, py = event['pixel'];cx, cy = px-x, py-y
            assert 0 <= cx < w and 0 <= cy < h
            uncertain = len(event['relative_staff_steps']) != 1 or None in event['relative_staff_steps']
            color = '#bf5d00' if uncertain else '#225da8'
            draw.ellipse((cx-10, cy-10, cx+10, cy+10), outline=color, width=2)
            draw.text((cx+11, cy-17), str(event['slot']), fill=color)
        panels.append((ident, source['path'], box, crop))
        annotations.append({'id': ident, 'type': 'Annotation', 'motivation': 'describing',
            'body': {'type': 'TextualBody', 'value': meaning, 'language': 'en'},
            'target': {'source': source['path'], 'selector': {'type': 'FragmentSelector',
                       'conformsTo': 'http://www.w3.org/TR/media-frags/', 'value': 'xywh='+','.join(map(str, box))}},
            'fragment_id': record['id'], 'source_url': capture['url'], 'sha256': source['sha256'],
            'image_dimensions': dimensions, 'rights_url': record['rights_url'],
            'literal_candidate': 'Provisional manually located noteheads; see readings.v1/v2/v3.json for positions and alternatives.',
            'normalized_candidate': None if phrase is None else str([e['relative_staff_steps'] for e in positions]),
            'observer': readings['observer'], 'independent_confirmation': False,
            'interpretation_limits': ['Relative staff positions only; clefs and absolute pitches unverified.',
                'Two target upper events remain unresolved; no full-melody, unique-branch or codex identity.'],
            'note_position_record': 'research/continuation_39/readings.v3.json'})
    (HERE / 'observations.json').write_text(json.dumps({'version': '1.0.0', 'assessment_date': '2026-10-27',
        'annotations': annotations}, ensure_ascii=False, indent=2) + '\n')
    proof = Image.new('RGB', (760, sum(crop.height+90 for _, _, _, crop in panels)+45), 'white')
    draw = ImageDraw.Draw(proof)
    draw.text((10, 8), 'Manual positions: blue = provisional clear, orange = unresolved. No generated manuscript detail.', fill='black')
    offset = 40
    for ident, path, box, crop in panels:
        draw.text((10, offset+5), ident, fill='black')
        draw.text((10, offset+22), path, fill='black')
        draw.text((10, offset+39), 'xywh='+str(box), fill='black')
        proof.paste(crop, (10, offset+65));offset += crop.height+90
    proof.save(HERE / 'note-review.png')
    print(json.dumps({'regions': len(annotations), 'manual_centres': 28,
                      'source_hashes_and_bounds_verified': True, 'independent_confirmation': False}))


if __name__ == '__main__':
    main()
