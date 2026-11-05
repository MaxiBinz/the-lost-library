"""Record selected image regions; transcription is exploratory, not verified."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def read(path):
    return json.loads((ROOT / path).read_text())

def main():
    caps = {}
    for filename in ('research/continuation_44/captures.json', 'research/continuation_54/captures.json'):
        caps.update({c['path']: c for c in read(filename)['captures']})
    observations = [
        ('I77-8066-die', 'mpo-8066', 'research/continuation_44/images/Fr8066-capture-2-native.jpg',
         [280, 395, 1055, 290], 'lau/des. Domum tuam domine decet sanctitudo in longitudine die[-]',
         'Laudes rubric and Domum tuam; the visible text ends die at the edge of the writing.',
         'The continuation in capture 3 is inferred from complementary text, not a verified common physical seam.'),
        ('I77-8066-domus-hec', 'mpo-8066', 'research/continuation_44/images/Fr8066-capture-3-native.jpg',
         [425, 150, 1035, 460], 'rum. Euouae. a. Domus mea domus orationis vocabitur. Euouae. a. Hec est domus [...]',
         'The top text ends rum, followed by a Domus mea antiphon and Hec est domus; the relation to capture 2 is provisional.',
         'Do not treat the inferred split as a physical seam or independently verified service identity.'),
        ('I77-10437-order', 'mpo-10437', 'research/continuation_54/images/Fr10437-capture-1-native.jpg',
         [250, 385, 1290, 665], 'Domum tuam [...] in longitudinem dierum. D[ominu]s reg[n...?] Euouae. a. Hec est domus [...]',
         'The selected field appears to place Hec est domus after the Domum tuam antiphon and a short psalm cue; small text and rubrics overlap the reading area.',
         'Service rubric and exact reading order require independent checking; this cannot establish absence of Domus mea elsewhere.'),
        ('I77-10437-later-cue', 'mpo-10437', 'research/continuation_54/images/Fr10437-capture-2-native.jpg',
         [390, 270, 350, 175], '[V?] Domus me[...]. [marker?] Domus or[...].',
         'Another selected photograph contains a small Domus me... cue and a following abbreviated response.',
         'The cue is not transcribed as a complete antiphon; its function, relation to the other capture and medieval side remain unverified.')
    ]
    annotations = []
    for ident, fragment, path, box, literal, body, limit in observations:
        cap = caps[path]
        annotations.append({
            'id': ident, 'type': 'Annotation', 'motivation': 'describing', 'fragment_id': fragment,
            'body': {'type': 'TextualBody', 'value': body, 'language': 'en'},
            'target': {'source': path, 'selector': {'type': 'FragmentSelector', 'conformsTo': 'http://www.w3.org/TR/media-frags/',
                       'value': 'xywh=' + ','.join(map(str, box))}},
            'source_url': cap['url'], 'sha256': cap['sha256'], 'image_dimensions': [cap['width'], cap['height']],
            'rights_url': cap['rights_url'], 'attribution': cap['attribution'], 'literal_candidate': literal,
            'normalized_candidate': None, 'observer': 'Codex AI; reference-exposed reading, 2026-11-02; exact model checkpoint unavailable',
            'independent_confirmation': False, 'interpretation_limits': [limit]
        })
    (ROOT / 'research/continuation_77/observations.json').write_text(json.dumps({'version': '1.0.0', 'annotations': annotations}, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'annotations': len(annotations)}))

if __name__ == '__main__':
    main()
