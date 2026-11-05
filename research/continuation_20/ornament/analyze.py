"""Reproduce a bounded, manually observed same-letter ornament comparison.

No image acquisition or fitted classifier. The feature statements below are
provisional AI visual observations, not automatically measured labels.
"""
import hashlib
import json
from pathlib import Path
import sys

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from lost_library.evidence import validate_observation

IDS = ('1385', '10406', '4223', '8311', '8455', '8201', '8304')
SPECS = [
    {'id': 'C20-A-1385', 'record': '1385', 'capture': 4, 'region': [175, 56, 85, 112],
     'letter': 'A', 'literal_context': 'Auertantur retrorsum…',
     'letter_confidence': 'Candidate A supported by following uertantur; provisional AI reading.',
     'traits': {'longitudinal_red_stem': 'visible', 'pale_body_field': 'visible', 'small_lozenges': 'red upper and dark lower', 'toothed_dark_left_contour': 'visible', 'long_loop_extension': 'small left foot only'},
     'body': 'Candidate A, followed by uertantur retrorsum. Pale body fields, a longitudinal red left-stem stripe, red upper/dark lower lozenges and a toothed dark left edge are visible. Small left-foot flourish. Compare the candidate A in10406, not only letters of other shapes.'},
    {'id': 'C20-A-10406', 'record': '10406', 'capture': 3, 'region': [248, 415, 80, 112],
     'letter': 'A', 'literal_context': 'Ades…',
     'letter_confidence': 'Candidate A supported by following des; provisional AI reading.',
     'traits': {'longitudinal_red_stem': 'visible', 'pale_body_field': 'visible', 'small_lozenges': 'red upper and lower', 'toothed_dark_left_contour': 'visible', 'long_loop_extension': 'small left foot only'},
     'body': 'Candidate A, followed by des. Pale body fields, a longitudinal red stripe, two red lozenges and a dark toothed left contour are visible. Relative to the1385A, the right body is a more continuous curved field and the lower lozenge appears red rather than dark. Letter construction and decoration can vary within a book; no exclusion follows.'},
    {'id': 'C20-A-4223', 'record': '4223', 'capture': 3, 'region': [178, 96, 128, 180],
     'letter': 'A', 'literal_context': 'A p[…]hetis…',
     'letter_confidence': 'Candidate A from shape and following text; abbreviation expansion not secured.',
     'traits': {'longitudinal_red_stem': 'not visibly red-filled in this sample', 'pale_body_field': 'paper-coloured spaces, not a colour measurement', 'small_lozenges': 'not securely visible', 'toothed_dark_left_contour': 'angular teeth visible', 'long_loop_extension': 'large upper-left loop'},
     'body': 'Candidate A with a large upper-left loop, angular dark left contours and a narrow patterned upright. No comparable long red-filled shaft or pair of interior lozenges is securely visible. The precise liturgical role is not independently established, so this is not a fully role-matched exclusion control.'},
    {'id': 'C20-A-8311', 'record': '8311', 'capture': 2, 'region': [676, 330, 78, 134],
     'letter': 'A', 'literal_context': 'A […]',
     'letter_confidence': 'Candidate A by form; complete following word not securely transcribed.',
     'traits': {'longitudinal_red_stem': 'not securely visible', 'pale_body_field': 'paper-coloured compartments', 'small_lozenges': 'not securely visible', 'toothed_dark_left_contour': 'visible', 'long_loop_extension': 'long lower-left flourish'},
     'body': 'Candidate A has a narrow diagonal right leg, compartmented/lattice-like crossbar and long lower-left flourish. No long red-filled shaft or paired simple lozenges is securely visible. Its local rubric/chant function is unresolved; apparent difference is not a book or hand exclusion.'},
    {'id': 'C20-R-1385', 'record': '1385', 'capture': 2, 'region': [239, 154, 72, 101],
     'letter': 'R', 'literal_context': 'Rex…',
     'letter_confidence': 'Candidate R supported by following ex.',
     'traits': {'longitudinal_red_stem': 'visible', 'pale_body_field': 'visible', 'small_lozenges': 'red and dark', 'toothed_dark_left_contour': 'visible', 'long_loop_extension': 'not conspicuous'},
     'body': 'Candidate R followed by ex. Long red stem, pale body, small red/dark lozenges and toothed outer left contour. This is a same-letter comparison with the8455Reges initial, but their exact decorative/liturgical functions are not shown equivalent.'},
    {'id': 'C20-R-8455', 'record': '8455', 'capture': 3, 'region': [659, 305, 105, 120],
     'letter': 'R', 'literal_context': 'Reges…',
     'letter_confidence': 'Candidate R supported by following eges.',
     'traits': {'longitudinal_red_stem': 'not securely visible at this resolution', 'pale_body_field': 'visible', 'small_lozenges': 'not securely visible', 'toothed_dark_left_contour': 'large angular teeth', 'long_loop_extension': 'not conspicuous'},
     'body': 'Candidate R followed by eges has a pale narrow stem/bowl and large angular teeth on the left. A red stem filling and small lozenges are not securely visible. A red verse-like marker precedes it, so function equivalence to the1385R is unverified.'},
    {'id': 'C20-D-8201', 'record': '8201', 'capture': 2, 'region': [644, 98, 94, 105],
     'letter': 'D', 'literal_context': 'De…',
     'letter_confidence': 'Candidate D supported by following e; initial A misidentification during inspection was corrected.',
     'traits': {'longitudinal_red_stem': 'visible, broad', 'pale_body_field': 'visible', 'small_lozenges': 'dark', 'toothed_dark_left_contour': 'visible', 'long_loop_extension': 'not conspicuous'},
     'body': 'Candidate D followed by e: broad red stem, pale right body, two dark lozenges, parallel crossbars and scalloped dark left border. This belongs to the previously published same-hand/different-book pair; the existing reference decision is not our new discovery.'},
    {'id': 'C20-D-8304', 'record': '8304', 'capture': 3, 'region': [365, 210, 81, 90],
     'letter': 'D', 'literal_context': 'De…',
     'letter_confidence': 'Candidate D supported by following e; not an A-specific control.',
     'traits': {'longitudinal_red_stem': 'visible', 'pale_body_field': 'visible', 'small_lozenges': 'red/pale at available pixels', 'toothed_dark_left_contour': 'visible', 'long_loop_extension': 'not conspicuous'},
     'body': 'Candidate D followed by e repeats a red stem, pale right body, small lozenge-like internal marks, parallel crossbars and dark scalloped left border. The two D samples are an auxiliary same-letter hard-negative comparison, not a test of A-specific exclusivity or an independently established common hand.'},
]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    records = {r['id']: r for r in json.loads((ROOT / 'data/fragments.json').read_text())}
    inventory = []
    for n in IDS:
        record = records['mpo-' + n]
        captures = record['captures']
        overview = Image.new('RGB', (1200, 1000), 'white')
        draw = ImageDraw.Draw(overview)
        for i, capture in enumerate(captures):
            path = ROOT / capture['path']
            assert sha(path) == capture['sha256'], path
            with Image.open(path) as source:
                assert list(source.size) == [capture['width'], capture['height']]
                thumb = source.convert('RGB')
                thumb.thumbnail((590, 460))
            x, y = (i % 2) * 600, (i // 2) * 500
            overview.paste(thumb, (x, y + 28))
            draw.text((x + 8, y + 5), capture['path'], fill='black')
            inventory.append({'record_id': record['id'], 'capture_ordinal': i + 1,
                              'path': capture['path'], 'sha256': capture['sha256'],
                              'image_dimensions': [capture['width'], capture['height']]})
        overview.save(OUT / (n + '-overview.jpg'))
    annotations, examples = [], []
    sheet = Image.new('RGB', (1200, 860), 'white')
    draw = ImageDraw.Draw(sheet)
    for i, spec in enumerate(SPECS):
        record = records['mpo-' + spec['record']]
        capture = record['captures'][spec['capture'] - 1]
        x, y, w, h = spec['region']
        annotation = {
            'id': spec['id'], 'type': 'Annotation', 'motivation': 'describing',
            'fragment_id': record['id'], 'body': {'type': 'TextualBody', 'value': spec['body'], 'language': 'en'},
            'target': {'source': capture['path'], 'selector': {'type': 'FragmentSelector', 'conformsTo': 'http://www.w3.org/TR/media-frags/', 'value': 'xywh=' + ','.join(map(str, spec['region']))}},
            'source_url': capture['url'], 'sha256': capture['sha256'],
            'observer': 'Codex AI source inspection,2026-10-23; exact model/checkpoint not exposed',
            'verification': 'Provisional AI observation; no independent expert review',
            'interpretation_limits': ['Post-review manual selection, not blind or preregistered.', 'Letter identity and liturgical function are candidate readings, not independent labels.', 'No same-book, same-hand or same-decorator inference from these features.'],
            'reading': {'literal_candidate': spec['literal_context'], 'normalized_search_text': '', 'certainty': spec['letter_confidence'], 'external_references': []},
        }
        validate_observation(ROOT, annotation, records)
        annotations.append(annotation)
        examples.append({k: v for k, v in spec.items() if k != 'body'} | {'source_path': capture['path'], 'sha256': capture['sha256']})
        with Image.open(ROOT / capture['path']) as image:
            crop = image.crop((x, y, x+w, y+h)).resize((w*2, h*2), Image.Resampling.NEAREST)
            crop.thumbnail((270, 365))
        xx, yy = (i % 4) * 300, (i // 4) * 430
        sheet.paste(crop, (xx + 10, yy + 35))
        draw.text((xx + 10, yy + 5), spec['id'], fill='black')
    sheet.save(OUT / 'matched-letters.png')
    result = {
        'version': '1.0.0', 'assessment_date': '2026-10-23',
        'scope': 'Post-review same-letter ornament falsification; no classifier, new attribution or independent validation.',
        'selection_rule': 'Screen all four existing captures for each of seven records. Select the first clearly interpretable major ornamental A candidate in capture order where available, plus first clear R in1385/8455 and first clear De-initial D in8201/8304. Different letters, plain filled blue/red display letters, small text capitals, partial/damaged forms and uncertain readings are excluded from strict same-letter comparison. Selection was made after viewing the target and controls.',
        'inventory': inventory, 'examples': examples,
        'exclusions': [
            {'record_id': 'mpo-8455', 'letter': 'A', 'reason': 'No securely legible complete large ornamental A selected from these four derivatives; absence in the medieval book is not inferred.'},
            {'record_id': 'mpo-10406', 'letter': 'R', 'reason': 'No securely legible large ornamental Rex/Reges-like R selected; an H02 same-R test is unavailable.'},
            {'record_id': 'mpo-4223', 'region': 'primary capture lower edge', 'reason': 'Partial initial at crop/damage boundary not used in place of the complete capture3A candidate.'},
            {'record_id': 'mpo-1385', 'region': 'capture3', 'reason': 'Damaged/faint lower ornamental traces do not securely identify a letter.'},
            {'record_id': 'mpo-10406', 'region': 'capture4 large initial', 'reason': 'Following word/letter interpretation not secured in this pass; not pooled with A.'},
            {'records': ['mpo-1385','mpo-10406','mpo-4223','mpo-8311','mpo-8455','mpo-8201','mpo-8304'], 'reason': 'Other letter types and plain blue/red display initials do not enter the A/R/D ornament comparison.'},
        ],
        'tests': [
            {'id': 'C20-O1', 'question': 'Does the1385/10406ornament resemblance survive controlling candidate letter identity?', 'result': 'Yes descriptively: their selected A candidates share pale fields, long red stem, small lozenges and toothed dark contour. Right-body/crossbar arrangement and lower-lozenge colour differ. Shared letter identity removes one confound, not common production or book identity.'},
            {'id': 'C20-O2', 'question': 'Does that same-A combination also appear in the selected Ant39A controls?', 'result': 'Not securely in the two selected4223/8311samples: these have different loop/compartment structures and no comparable long red-filled shaft/paired simple lozenges securely visible. This is a local contrast, not rarity or exclusivity: the samples and exact functions are not representative/independently established.'},
            {'id': 'C20-O3', 'question': 'Does the1385/8455same-R comparison supply a fully matched negative?', 'result': 'No. Both have pale bodies and toothed contours, but a red fill/lozenges are not securely visible in8455. The8455verse-like marker also prevents assuming function equivalence. This auxiliary contrast cannot identify a book.'},
            {'id': 'C20-O4', 'question': 'Can a red-stem/pale-field/lozenge/scallop vocabulary distinguish the published wrong-book8201/8304pair?', 'result': 'No in the selected same-D samples: both show that vocabulary. This is a separate letter-class control, not an A-specific counterexample or a new rejection. The precise local liturgical functions are not independently secured.'},
        ],
        'outcome': 'H02 decoration remains compatible and somewhat more specifically described after a same-A check, but no validated identity discriminator or scientific attribution is obtained. A-specific exclusivity is unestablished; strict function matching remains incomplete.',
        'next_evidence_needed': ['Verify complete incipits/rubrics to match exact decorative role.', 'Compare more occurrences of the same A in actual known same-book and same-hand/different-book material before proposing a discriminatory feature.', 'Keep text succession, opening signatures and physical evidence independent from ornamental resemblance.'],
        'independent_expert_review': False, 'new_discovery': False,
        'source_reference_for_hard_negative': 'https://doi.org/10.25167/ls.4818',
        'queue_sha256': sha(ROOT / 'data/hypotheses.v1.json'),
        'source_downloads': 0,
    }
    assert len(inventory) == 28 and len(annotations) == 8
    assert result['queue_sha256'] == 'b3e299a7c600584ce44518db1f5c30c3301edae0a07a8b009075498f64ccec47'
    for name, value in [('results.json', result), ('observations.json', {'@context': 'http://www.w3.org/ns/anno.jsonld', 'version':'1.0.0', 'annotations':annotations})]:
        (OUT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'source_files_hash_checked':len(inventory), 'source_regions_validated':len(annotations), 'letter_classes':['A','R','D'], 'new_discovery':False, 'queue_sha256':result['queue_sha256']}))


if __name__ == '__main__':
    main()
