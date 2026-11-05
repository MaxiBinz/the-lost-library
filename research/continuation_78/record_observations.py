"""Record source context without asserting an independently verified reading."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def main():
    path = 'research/continuation_54/images/Fr10437-capture-2-native.jpg'
    caps = json.loads((ROOT / 'research/continuation_54/captures.json').read_text())['captures']
    cap = next(c for c in caps if c['path'] == path)
    annotation = {
        'id': 'I78-10437-lapides-verse-mane', 'type': 'Annotation', 'motivation': 'describing', 'fragment_id': 'mpo-10437',
        'body': {'type': 'TextualBody', 'value': 'The end of Lapides pretiosi is followed by an abbreviated Domus me... / Domus or... cue, a red Ad bened... ant... rubric and a large Mane surgens opening. Verse-and-response interpretation is reference-assisted and provisional.', 'language': 'en'},
        'target': {'source': path, 'selector': {'type': 'FragmentSelector', 'conformsTo': 'http://www.w3.org/TR/media-frags/', 'value': 'xywh=200,15,1315,445'}},
        'source_url': cap['url'], 'sha256': cap['sha256'], 'image_dimensions': [cap['width'], cap['height']],
        'rights_url': cap['rights_url'], 'attribution': cap['attribution'],
        'literal_candidate': 'Lapides preciosi [...] [V?] Domus me[...] [marker?] Domus or[...] Ad bened[...] ant[...] Mane surgens Iacob [...]',
        'normalized_candidate': None, 'observer': 'Codex AI; reference-exposed reading, 2026-11-02; exact model checkpoint unavailable',
        'independent_confirmation': False,
        'interpretation_limits': ['The small markers and abbreviations require independent verification; neither Cantus ID nor missing words are image-confirmed.',
                                  'The relation to capture 1 and the presence or absence of a full Domus mea antiphon around the fold remain unverified.']
    }
    out = ROOT / 'research/continuation_78/observations.json'
    out.write_text(json.dumps({'version': '1.0.0', 'annotations': [annotation]}, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'annotations': 1}))

if __name__ == '__main__':
    main()
