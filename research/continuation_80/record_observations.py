"""Record the selected source regions; no independent transcription is claimed."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def main():
    caps = {}
    for name in ('research/continuation_44/captures.json', 'research/continuation_54/captures.json'):
        caps.update({c['path']: c for c in json.loads((ROOT / name).read_text())['captures']})
    rows = [
        ('I80-10437-domini','mpo-10437','research/continuation_54/images/Fr10437-capture-1-native.jpg',[1120,715,190,165],
         'The first two candidate square noteheads over do-mi of domini appear to descend relative to the local rules; a subsequent compound sign needs separate segmentation.'),
        ('I80-8066-domini','mpo-8066','research/continuation_44/images/Fr8066-capture-3-native.jpg',[440,465,185,105],
         'The first two candidate Hufnagel-style heads over do-mi of domini appear to descend relative to the local red rule; stems and a following joined sign complicate precise reading.')
    ]
    annotations = []
    for ident, fragment, path, box, body in rows:
        cap = caps[path]
        annotations.append({'id':ident,'type':'Annotation','motivation':'describing','fragment_id':fragment,
            'body':{'type':'TextualBody','value':body,'language':'en'},
            'target':{'source':path,'selector':{'type':'FragmentSelector','conformsTo':'http://www.w3.org/TR/media-frags/', 'value':'xywh='+','.join(map(str,box))}},
            'source_url':cap['url'],'sha256':cap['sha256'],'image_dimensions':[cap['width'],cap['height']],
            'rights_url':cap['rights_url'],'attribution':cap['attribution'],'literal_candidate':'domini [...]',
            'normalized_candidate':None,'observer':'Codex AI; post-selection, reference-exposed reading, 2026-11-02; exact checkpoint unavailable',
            'independent_confirmation':False,
            'interpretation_limits':['Notehead centres, underlay, local rule and sign grouping are tentative and unreviewed.',
                                     'A two-note direction does not establish exact interval, full melodic identity or a common parent book.']})
    (ROOT / 'research/continuation_80/observations.json').write_text(json.dumps({'version':'1.0.0','annotations':annotations},ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'annotations':len(annotations)}))

if __name__ == '__main__':
    main()
