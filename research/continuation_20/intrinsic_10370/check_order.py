"""Reproduce a source-bound, provisional chant-text continuation check.

Readings were proposed by AI inspection of cached source photographs before
comparison with Cantus text. This is not OCR, a blind test, or expert review.
No network requests, source mutations or hypothesis-queue changes occur here.
"""
import hashlib
import json
import re
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
QUEUE_SHA = 'b3e299a7c600584ce44518db1f5c30c3301edae0a07a8b009075498f64ccec47'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dump(name, value):
    (OUT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def main():
    assert sha(ROOT / 'data/hypotheses.v1.json') == QUEUE_SHA
    records = json.loads((ROOT / 'data/fragments.json').read_text())
    record = next(r for r in records if r['id'] == 'mpo-10370')
    captures = {c['path']: c for c in record['captures']}
    specs = [
        {
            'id': 'I20-10370-verse-prefix',
            'path': 'data/images/mpo-10370-capture-2-1739px.jpg',
            'region': [650, 490, 740, 115],
            'literal': '[A]rdore caritatis succensa quē',
            'normalized': 'Ardore caritatis succensa quem',
            'body': 'The final written row of this photograph begins the verse: candidate Ardore caritatis succensa que with an abbreviation bar. Quem is an explicit proposed expansion. The decorated initial begins at the left edge of the selected region.',
        },
        {
            'id': 'I20-10370-verse-suffix',
            'path': 'data/images/mpo-10370-capture-3-1728px.jpg',
            'region': [345, 330, 1155, 85],
            'literal': 'sepultum nouerat sublatum cred[ens?] de se pul chro',
            'normalized': 'sepultum noverat sublatum credens de sepulchro',
            'body': 'The first written row of the k-marked photograph continues with candidate sepultum nouerat sublatum cred[ens?] de se pul chro. The word credens is less securely read than the surrounding words; the Cantus parallel informs its proposed normalization.',
        },
    ]
    annotations = []
    for spec in specs:
        c = captures[spec['path']]
        source = ROOT / spec['path']
        assert sha(source) == c['sha256']
        with Image.open(source) as im:
            width, height = im.size
            x, y, w, h = spec['region']
            assert x >= 0 and y >= 0 and x + w <= width and y + h <= height
            im.crop((x, y, x + w, y + h)).save(OUT / (spec['id'] + '.png'))
        annotations.append({
            'id': spec['id'], 'type': 'Annotation', 'motivation': 'describing',
            'fragment_id': 'mpo-10370', 'review_pair_ids': [],
            'body': {'type': 'TextualBody', 'value': spec['body'], 'language': 'en'},
            'target': {'source': spec['path'], 'selector': {'type': 'FragmentSelector',
                'conformsTo': 'http://www.w3.org/TR/media-frags/',
                'value': 'xywh=' + ','.join(map(str, spec['region']))}},
            'source_url': c['url'], 'sha256': c['sha256'],
            'image_dimensions': [width, height],
            'observer': 'Codex AI source inspection, 2026-10-23; exact model/checkpoint not exposed',
            'evidence_kind': 'provisional image reading and external text concordance',
            'verification': 'Provisional AI source reading; no independent expert adjudication',
            'reading': {'literal_candidate': spec['literal'],
                'normalized_search_text': spec['normalized'],
                'certainty': 'provisional; abbreviation expansion and uncertain credens are explicit',
                'cantus_candidate': {'id': '601029a', 'status': 'candidate verse identification, not manuscript identity'},
                'external_references': ['https://cantusdatabase.org/chant/402240/',
                    'https://cantusdatabase.org/chant/564421/',
                    'https://cantusdatabase.org/chant/204152/']},
            'interpretation_limits': [
                'Long text continuation supports relative reading order, not original codex identity.',
                'No registered pixel overlap, physical stitch or direct seam is established.',
                'Roman/letter marks and relative order do not define the MPO catalogue side convention.',
                'Repeated chants or unrecognized photographic rearrangement remain alternatives.',
                'Agreement between AI readings is not independent expert corroboration.',
            ],
        })
    # The reference comes from public indexed primary Cantus records, not a
    # retrieved manuscript image or a direct HTTP body in this step.
    reference = 'Ardore caritatis succensa quem sepultum noverat sublatum credens de sepulcro'
    normalize = lambda s: re.sub(r'[^a-z ]', '', s.lower().replace('sepulchro', 'sepulcro'))
    forward = normalize(' '.join(s['normalized'] for s in specs))
    reverse = normalize(' '.join(s['normalized'] for s in reversed(specs)))
    assert forward == normalize(reference)
    assert reverse != normalize(reference)
    dump('observations.json', {'@context': 'http://www.w3.org/ns/anno.jsonld',
        'version': '1.0.0', 'annotations': annotations})
    result = {
        'assessment_date': '2026-10-23', 'queue_sha256_unchanged': QUEUE_SHA,
        'question': 'Does actual text support an order between the numeral-bearing and k-bearing photographed surfaces?',
        'comparison': {
            'candidate_chant': '601029a', 'genre': 'Matins responsory verse for Mariae Magdalenae',
            'reference_normalized_text': reference,
            'reference_access': 'Full text exposed by public web-search indexing of primary Cantus Database records; no direct source-image inspection or direct HTML body claimed.',
            'references': [
                {'url': 'https://cantusdatabase.org/chant/402240/', 'source': 'F-Pn Latin12044', 'folio': '165r'},
                {'url': 'https://cantusdatabase.org/chant/564421/', 'source': 'PL-WRu R503', 'folio': '163r'},
                {'url': 'https://cantusdatabase.org/chant/204152/', 'source': 'F-CA38', 'folio': '291v'},
            ],
            'forward_normalized_sequence_matches': True,
            'reversed_sequence_matches': False,
            'prefix_word_count': 5, 'suffix_word_count': 8,
            'uncertain_word': 'credens: less secure image reading; normalization supported by reference',
            'unique_identity_claim': False,
        },
        'source_based_outcome': 'Image2 final written row precedes image3 first written row within a single candidate verse. This supplies intrinsic relative text order rather than ordinal-only inference.',
        'orientation_implication': 'Together with the existing proposed image1/2 association, this supports numeral-bearing surface before k-bearing surface. On the catalogue assertion that this is one original leaf, it is consistent with numeral on medieval recto and k on verso, but co-surface/physical mapping and the meaning of MPO1r/1v still require separate verification.',
        'new_information': 'A named-verse prefix/suffix continuation now supplies evidence where the earlier pass had only complementary initials and uncertain side labels.',
        'not_established': ['A physical seam or stitched image', 'A new same-book attribution',
            'A previously unknown placement in IV157', 'A general MPO recto/verso rule',
            'A proven catalogue error', 'Rare variant, melodic identity or historical provenance',
            'Scientific originality or independent expert confirmation'],
        'observations': [s['id'] for s in specs],
        'no_new_source_downloads': True, 'independent_expert_review': False,
    }
    dump('results.json', result)
    print(json.dumps({'source_regions': len(annotations), 'candidate_chant': '601029a',
        'forward_matches': True, 'reverse_matches': False, 'queue_unchanged': True}))


if __name__ == '__main__':
    main()
