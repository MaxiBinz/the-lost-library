"""Merge source checks without changing the frozen attribution queue or labels.

This records post-review evidence. It does not fit a model or supply independent
expert labels. Earlier observation versions remain available unchanged.
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
QUEUE_SHA = 'b3e299a7c600584ce44518db1f5c30c3301edae0a07a8b009075498f64ccec47'


def load(name):
    return json.loads((ROOT / name).read_text())


def dump(name, value):
    (ROOT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def append_unique(values, value):
    if value not in values:
        values.append(value)


def main():
    assert hashlib.sha256((ROOT / 'data/hypotheses.v1.json').read_bytes()).hexdigest() == QUEUE_SHA
    previous = load('data/observations.v3.json')['annotations']
    visual = load('research/independent_pass/visual/observations.json')['annotations']
    text = load('research/independent_pass/text/observations.json')['annotations']
    annotations = previous + visual + text
    assert len(annotations) == len({o['id'] for o in annotations}) == 36
    dump('data/observations.v4.json', {
        '@context': 'http://www.w3.org/ns/anno.jsonld', 'version': '4.0.0',
        'assessment_date': '2026-10-22',
        'scope': 'Source observations including supporting context outside the unchanged ten-pair queue; no new attribution labels.',
        'inputs': ['data/observations.v3.json', 'research/independent_pass/visual/observations.json',
                   'research/independent_pass/text/observations.json'],
        'annotations': annotations,
    })
    document = load('data/hypothesis_reviews.v1.json')
    document.update(version='1.2.0', observations_path='data/observations.v4.json',
                    context_checks_path='data/context_checks.v1.json')
    for review in document['reviews']:
        review['review_state'] = 'local source tests recorded; no independent expert review'
        for observation in visual:
            if review['id'] in observation.get('review_pair_ids', []):
                assert observation['fragment_id'] in (review['left_id'], review['right_id'])
                append_unique(review['observation_ids'], observation['id'])
        if review['id'] in ('H01', 'H03'):
            review['supporting'] = [x for x in review['supporting'] if not x.startswith('The source capture has two consecutive')]
            append_unique(review['supporting'], 'Two visible antiphon incipits agree with the office sequence in Hallqvist2020 edited C435, printedp6/PDF53. The higher-resolution invitatory comparison now distinguishes edited C435, its apparatus-reported manuscript state and edited C23 (PDF67).')
            append_unique(review['against'], 'The apparent absence of separate pium and Matri…condolentes before procida… agree with the standard edited wording, not a unique book fingerprint. The edition reports different states for C435. No direct inspection of C435 manuscript images is claimed.')
            append_unique(review['against'], 'No hymn entry is visible between Venite and Immolandus in the inspected continuous target region. This is a written-layout observation; abbreviated practice, different book function or a hymn elsewhere remain alternatives.')
            for observation in text:
                append_unique(review['observation_ids'], observation['id'])
            append_unique(review['sources'], 'https://lup.lub.lu.se/student-papers/record/9032430/file/9032431.pdf#page=67')
            append_unique(review['sources'], 'data/text_collation.v2.json')
        if review['id'] == 'H02':
            append_unique(review['supporting'], 'Selected initials share pale-grey shafts, red stripes/lozenges and black scalloping. Four staff windows per capture, normalized by approximate ruler intervals, show no gross ruling-scale incompatibility; endpoint perturbation ranges overlap.')
            append_unique(review['against'], 'Related ornamental traits also occur among Ant39 controls. Ruler readings are approximate and perspective is not calibrated; no certified physical size, same hand or same book is established.')
            review['next_evidence_needed'] = 'Compare additional uncommon letterforms and securely paired opening signatures; verify corresponding text and side conventions. Ruling compatibility and broad decoration alone cannot decide identity.'
            append_unique(review['sources'], 'research/independent_pass/visual/findings.md')
            append_unique(review['sources'], 'research/independent_pass/visual/measurements.json')
        if review['id'] == 'H03':
            append_unique(review['supporting'], 'An older Finnish IV157 description already places Swedish account48/ChristiernPhilipssons1610 between Helsinki ff7and8. The pinned CSV uniquely maps that description to Fr10370. This is contextual published evidence, not a new placement or proof for every Codex1505 leaf.')
            review['next_evidence_needed'] = 'Compare corresponding actual words and complete opening addresses against the Helsinki leaves. Resolve present-fragment versus medieval-side conventions. Fr10370 context is kept separately; the previously documented placement does not independently establish the entire proposed group.'
            append_unique(review['sources'], 'https://fragmenta.kansalliskirjasto.fi/handle/10024/1300')
            append_unique(review['sources'], 'research/independent_pass/crosswalk/audit.md')
        if review['id'] == 'H05':
            review['prior_status'] = 'Previously suggested same-book association; Hy49 alias resolved in the pinned deposit'
            append_unique(review['supporting'], 'A full-deposit crosswalk uniquely maps Hy49 to Fr25592. The Finnish source distinguishes accepted Ant242/Fr29666 from suggested Hy49 and Ant99 relations; a unique identifier does not resolve that historical suggestion.')
            review['next_evidence_needed'] = 'Verify the historical relation using corresponding text, opening signatures and physical structure. The Hy49=25592 identifier is resolved in this dataset; the substantial layout conflict still has composite-book and description-error alternatives.'
            append_unique(review['sources'], 'research/independent_pass/crosswalk/audit.md')
        if review['id'] in ('H08', 'H09', 'H10'):
            append_unique(review['against'], 'Selected decorated initials provide a control for shared ornamental vocabulary; resemblance in these traits is not unique to H02 and cannot identify a book or scribe.')
        assert not review['new_discovery'] and not review['independent_expert_review']
    dump('data/hypothesis_reviews.v1.json', document)
    context = [
        {
            'id': 'CTX01', 'title': 'Fr10370 marks and previously documented placement',
            'record_ids': ['mpo-10370'],
            'observation_ids': [o['id'] for o in visual if o['fragment_id'] == 'mpo-10370'],
            'summary': 'Higher-resolution source regions show II/ij-like and k-like top-margin signs. A unique source-account crosswalk identifies the leaf already placed between IV157 ff7and8 by an older catalogue description.',
            'outcome': 'Sign inventory is source-supported provisionally; placement is previously documented. No new adjacency or catalogue error established.',
            'limits': ['Photograph indices are not medieval page sides.', 'Complementary portions in images1/2 suggest continuation, but no pixel registration or shared complete row proves an overlap.', 'The MPO meaning of1r/1v has not been established; the side-pattern mismatch remains conditional.', 'The older placement and later suggested group assertion have different scope.'],
            'sources': ['https://fragmenta.kansalliskirjasto.fi/handle/10024/1300', 'research/independent_pass/crosswalk/audit.md', 'research/independent_pass/crosswalk/side_convention_note.json', 'research/independent_pass/visual/findings.md'],
        },
        {
            'id': 'CTX02', 'title': 'Repeated opening address: conditional consistency check',
            'record_ids': [], 'observation_ids': [],
            'summary': 'Indexed institutional descriptions assign hVIII–hIX to IV156f2 and IV157f5 with different feast labels. All16combinations of four explicit consistency premises were evaluated.',
            'outcome': 'Unresolved. Different feast labels alone do not demonstrate mutually incompatible text or different books.',
            'limits': ['The source readings came from public indexed institutional text with OCR noise; corresponding manuscript images were not verified.', 'Unique unrepeated numbering, correct transcription, the same physical position and incompatible text must all be established.', 'Reset numbering, composite volumes, side labels and incomplete summaries remain alternatives.'],
            'sources': ['https://fragmenta.kansalliskirjasto.fi/handle/10024/1299', 'https://fragmenta.kansalliskirjasto.fi/handle/10024/1300', 'research/independent_pass/crosswalk/source_constraints.json'],
        },
        {
            'id': 'CTX03', 'title': 'Published image-scaling formula: possible erratum',
            'record_ids': [], 'observation_ids': [],
            'summary': 'Duba2023 printedp64/PDF66 prose scales width by Smin/Sn; the displayed equation reverses this ratio. Dimensional derivation and three analytic controls preserve physical size with the prose ratio.',
            'outcome': 'Use width × Smin/Sn when rescaling to Smin pixels/mm. This is an implementation correction and possible typographical erratum.',
            'limits': ['No claim of first notice, originality or new historical finding.', 'The checks use synthetic analytic examples, not measured manuscript data.', 'No specialist or author confirmation has been received.'],
            'sources': ['https://www.fragmentology.ms/article/view/4499', 'research/independent_pass/methods/methods.md', 'research/independent_pass/methods/protocol-results.json'],
        },
    ]
    dump('data/context_checks.v1.json', {'version': '1.0.0', 'assessment_date': '2026-10-22',
        'scope': 'Supporting checks, not additional frozen attribution hypotheses or independent expert decisions.',
        'checks': context})
    print(json.dumps({'regions': len(annotations), 'context_checks': len(context), 'queue_sha256': QUEUE_SHA}))


if __name__ == '__main__':
    main()
