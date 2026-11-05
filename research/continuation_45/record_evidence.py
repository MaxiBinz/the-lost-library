"""Serialize the retained E45 manual readings; replay is not new inspection."""
import json
from pathlib import Path
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def main():
    manual = json.loads((HERE / 'manual_readings.json').read_text())
    captures = {c['path']: c for c in json.loads((ROOT / 'research/continuation_44/captures.json').read_text())['captures']}
    annotations, panels = [], []
    for row in manual['regions']:
        cap = captures[row['path']]
        x, y, w, h = row['xywh']
        with Image.open(ROOT / row['path']) as image:
            panels.append(image.crop((x, y, x+w, y+h)).convert('RGB'))
        annotations.append({'id': row['id'], 'type': 'Annotation', 'motivation': 'describing',
            'body': {'type': 'TextualBody', 'value': row['observation']+' '+row['limit'], 'language': 'en'},
            'target': {'source': row['path'], 'selector': {'type': 'FragmentSelector',
                'conformsTo': 'http://www.w3.org/TR/media-frags/', 'value': 'xywh='+','.join(map(str,row['xywh']))}},
            'fragment_id': cap['physical_object_id'], 'source_url': cap['url'], 'sha256': cap['sha256'],
            'image_dimensions': [cap['width'], cap['height']], 'rights_url': cap['rights_url'],
            'literal_candidate': row['literal_candidate'], 'normalized_candidate': row['normalized_candidate'],
            'observer': manual['reader'], 'independent_confirmation': False,
            'interpretation_limits': [row['limit'], manual['prior_exposure']]})
    (HERE / 'observations.json').write_text(json.dumps({'version':'1.0.0', 'assessment_date':'2026-10-29', 'annotations':annotations}, ensure_ascii=False, indent=2)+'\n')
    result = {k:v for k,v in manual.items() if k not in ['regions','capture_coverage']}
    result.update({'pair':['mpo-8066','mpo-9620'], 'source_photographs_reviewed':9,
        'observations':[a['id'] for a in annotations], 'pair_state':'unresolved',
        'new_download_bytes':0, 'new_source_files':0,
        'unchanged_inputs':json.loads((HERE / 'protocol.json').read_text())['frozen_inputs']})
    (HERE / 'results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    for filename,indices in [('service-review.png',range(3)),('parallel-text-review.png',range(3,len(panels)))]:
        proof = Image.new('RGB',(1100,sum(panels[i].height+48 for i in indices)+36),'white')
        draw = ImageDraw.Draw(proof); y=0
        for i in indices:
            draw.text((10,y+6),manual['regions'][i]['id']+' / raw separate source region',fill='black')
            proof.paste(panels[i],(10,y+28)); y+=panels[i].height+48
        draw.text((10,y+5),'No complete corresponding office opening, distinctive variant or codex identity is established.',fill='black')
        proof.save(HERE / filename)
    print(json.dumps({'source_photographs_reviewed':9,'regions':len(annotations),'pair_state':'unresolved'}))


if __name__ == '__main__':
    main()
