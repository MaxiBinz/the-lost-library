"""Reproduce one fixed, post-exposure image-span calculation."""
import hashlib
import json
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).parent


def main():
    protocol = json.loads((HERE / 'protocol.json').read_text())
    obj = next(item for item in json.loads((ROOT / 'data/fragments.json').read_text()) if item['id'] == 'mpo-10370')
    cap = next(item for item in obj['captures'] if item['path'] == protocol['source'])
    path = ROOT / cap['path']
    sha = hashlib.sha256(path.read_bytes()).hexdigest()
    assert sha == cap['sha256']
    with Image.open(path) as image:
        assert image.size == (cap['width'], cap['height'])
    points = protocol['fixed_points']
    ruler_px = points['ruler_marks_cm_1_and_21_x'][1] - points['ruler_marks_cm_1_and_21_x'][0]
    text_px = points['glyph_interior_x'][1] - points['glyph_interior_x'][0]
    span = text_px * 20 / ruler_px
    cautious = (text_px - 40) * 20 / (ruler_px + 8)
    assert ruler_px == 982 and text_px == 1000
    observations = []
    for name, region, body in [
        ('I92-10370-text-span', points['text_span_region_xywh'], 'Same visible text line with selected interior glyph positions at x=400 and x=1400; positions are not the ends of the complete writing field.'),
        ('I92-10370-ruler', points['ruler_region_xywh'], 'Photographic ruler: manually selected x=118 and x=1100 correspond approximately to the 1 cm and 21 cm marks.'),
    ]:
        x, y, w, h = region
        assert 0 <= x < x+w <= cap['width'] and 0 <= y < y+h <= cap['height']
        observations.append({'id': name, 'type':'Annotation', 'motivation':'describing',
          'body':{'type':'TextualBody','value':body,'language':'en'},
          'target':{'source':cap['path'],'selector':{'type':'FragmentSelector','conformsTo':'http://www.w3.org/TR/media-frags/','value':f'xywh={x},{y},{w},{h}'}},
          'fragment_id':'mpo-10370','source_url':cap['url'],'sha256':sha,
          'image_dimensions':[cap['width'],cap['height']],'rights_url':obj['rights_url'],'attribution':obj['attribution'],
          'observer':'Codex AI, post-exposure; 2026-11-03','independent_confirmation':False})
    (HERE/'observations.json').write_text(json.dumps({'version':'1.0.0','annotations':observations},indent=2,ensure_ascii=False)+'\n')
    result={'date':protocol['date'],'source_sha256':sha,'source_regions':[o['id'] for o in observations],
      'ruler_px_per_cm':ruler_px/20,'interior_glyph_span_px':text_px,
      'apparent_span_cm':round(span,3),'illustrative_min_span_cm':round(cautious,3),
      'catalogue_ii64_width_cm':18.5,
      'interpretation':'The selected Swedish glyph positions span about 20.4 cm in the image. A conservative chosen point/ruler perturbation remains about 19.4 cm. This is conditional on the ruler scale applying to the text plane; the Finnish value is catalogue metadata, not an image measurement.',
      'not_established':['full Swedish written-area width','Finnish physical measurement','same or different medieval book','same or different account','physical exclusion','novel discovery','independent confirmation']}
    (HERE/'results.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'span_cm':result['apparent_span_cm'],'illustrative_min_cm':result['illustrative_min_span_cm']}))


if __name__ == '__main__':
    main()
