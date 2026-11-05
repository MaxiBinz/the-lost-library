"""Create source-linked regions for the exploratory first-four-note comparison."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def main():
    captures = {}
    for name in ('research/continuation_44/captures.json', 'research/continuation_54/captures.json'):
        captures.update({c['path']: c for c in json.loads((ROOT / name).read_text())['captures']})
    rows = [
        ('I79-10437-hec', 'mpo-10437', 'research/continuation_54/images/Fr10437-capture-1-native.jpg',
         [770, 720, 400, 170], 'Hec est domus [...]',
         'Four candidate square noteheads over Hec / est / do- / mus; third is visually lower relative to the adjacent rule, then the fourth returns higher.'),
        ('I79-8066-hec', 'mpo-8066', 'research/continuation_44/images/Fr8066-capture-3-native.jpg',
         [1080, 310, 375, 160], 'Hec est domus [...]',
         'Four candidate Hufnagel-style noteheads over Hec / est / do- / mus appear roughly level in this selected field.')
    ]
    annotations = []
    for ident, fragment, path, box, literal, body in rows:
        cap = captures[path]
        annotations.append({
            'id': ident, 'type': 'Annotation', 'motivation': 'describing', 'fragment_id': fragment,
            'body': {'type': 'TextualBody', 'value': body, 'language': 'en'},
            'target': {'source': path, 'selector': {'type':'FragmentSelector', 'conformsTo':'http://www.w3.org/TR/media-frags/', 'value':'xywh=' + ','.join(map(str, box))}},
            'source_url': cap['url'], 'sha256': cap['sha256'], 'image_dimensions': [cap['width'], cap['height']],
            'rights_url': cap['rights_url'], 'attribution': cap['attribution'], 'literal_candidate': literal,
            'normalized_candidate': None, 'observer':'Codex AI; post-selection, reference-exposed reading, 2026-11-02; exact checkpoint unavailable',
            'independent_confirmation': False,
            'interpretation_limits':['Notehead centres, sign grouping, staff function and text underlay are manually assigned and unreviewed.',
                                     'The short contour does not establish absolute pitch, complete melodic identity, book identity or originality.']
        })
    (ROOT / 'research/continuation_79/observations.json').write_text(json.dumps({'version':'1.0.0', 'annotations':annotations}, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'annotations':len(annotations)}))

if __name__ == '__main__':
    main()
