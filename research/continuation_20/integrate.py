"""Record E20 source tests without changing the frozen relationship selection.

External witness pages support source comparison only; they are not predictors,
additional retrieval objects or independent expert labels.
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


def append(values, value):
    if value not in values:
        values.append(value)


def main():
    assert hashlib.sha256((ROOT / 'data/hypotheses.v1.json').read_bytes()).hexdigest() == QUEUE_SHA
    inputs = ['data/observations.v4.json',
              'research/continuation_20/intrinsic_10370/observations.json',
              'research/continuation_20/ornament/observations.json',
              'research/continuation_20/c23/observations.json']
    observations = [o for name in inputs for o in load(name)['annotations']]
    assert len(observations) == len({o['id'] for o in observations})
    dump('data/observations.v5.json', {'@context': 'http://www.w3.org/ns/anno.jsonld',
        'version': '5.0.0', 'assessment_date': '2026-10-23', 'inputs': inputs,
        'scope': 'Post-review source tests including external comparison pages; no new attribution or predictor.',
        'annotations': observations})
    reviews = load('data/hypothesis_reviews.v1.json')
    reviews.update(version='1.3.0', assessment_date='2026-10-23',
                   observations_path='data/observations.v5.json',
                   context_checks_path='data/context_checks.v2.json')
    ornament_pairs = {
        'H02': ['C20-A-1385', 'C20-A-10406'],
        'H08': ['C20-A-1385', 'C20-A-4223'],
        'H09': ['C20-A-1385', 'C20-A-8311'],
        'H10': ['C20-R-1385', 'C20-R-8455'],
        'H06': ['C20-D-8201', 'C20-D-8304'],
    }
    for review in reviews['reviews']:
        for ident in ornament_pairs.get(review['id'], []):
            append(review['observation_ids'], ident)
        if review['id'] == 'H02':
            append(review['supporting'], 'A controlled candidate A-to-A comparison retains specific Fr1385/10406 resemblance; the selected Ant39 A examples differ. Exact decorative-function equivalence and A-specific exclusivity remain unverified.')
            append(review['against'], 'The published wrong-book pair repeats the richer motif vocabulary in separate D-to-D samples. This is a different-letter-class control, not an A-specific counterexample. Selected post-review decoration cannot establish identity.')
            append(review['sources'], 'research/continuation_20/ornament/results.md')
        if review['id'] in ('H08', 'H09', 'H10'):
            append(review['against'], 'Letter-controlled examples are now retained separately: selected Ant39 A samples differ from the H02 A samples, while the R comparison is incomplete for red fill/lozenges. This local contrast establishes no rarity, common hand or physical exclusion.')
            append(review['sources'], 'research/continuation_20/ornament/results.md')
        if review['id'] == 'H06':
            append(review['supporting'], 'Selected De-initial D examples share pale fields, red stems, lozenges and toothed contours despite the published different-book decision. This is descriptive corroboration of the limits of ornament, not an independently rediscovered rejection.')
        if review['id'] in ('H01', 'H03'):
            for observation in load('research/continuation_20/c23/observations.json')['annotations']:
                if observation['fragment_id'] == 'mpo-20274':
                    append(review['observation_ids'], observation['id'])
            append(review['supporting'], 'Two actual C23 source pages were acquired from Uppsala Alvin. A declared ten-site comparison retains eight target-evaluable word/structure sites and two unavailable target sites; corrected text, cancelled text and editorial reports remain separate.')
            append(review['against'], 'No distinctive shared uncorrected C23 reading is established. Seven selected sites give current/standard word or cue agreements; the eighth has a visible C23 hymn entry where the target continuous region has none. These are not eight independent identity features or a transmission tree.')
            append(review['sources'], 'research/continuation_20/c23/collation.json')
            append(review['sources'], 'https://www.alvin-portal.org/alvin/view.jsf?pid=alvin-record:160517')
        if review['id'] == 'H03':
            append(review['supporting'], 'Supporting Fr10370 context now has literal verse-prefix/suffix evidence for source-image2→3 order. This improves intrinsic orientation without proving a new relationship involving Fr8994.')
        assert not review['new_discovery'] and not review['independent_expert_review']
    dump('data/hypothesis_reviews.v1.json', reviews)
    checks = load('data/context_checks.v1.json')['checks']
    first = next(c for c in checks if c['id'] == 'CTX01')
    first['title'] = 'Fr10370 text order, marks and previously documented placement'
    first['summary'] = 'Image2 ends with candidate Ardore caritatis succensa quem; image3 begins sepultum noverat sublatum cred[ens?] de sepulchro. The concatenation matches candidate Cantus601029a, supporting2→3 relative text order. Visible margin marks and the earlier catalogue placement remain separately recorded.'
    first['outcome'] = 'Intrinsic relative text order is supported. With the proposed1/2 same-surface association and one-leaf catalogue assertion, numeral-surface before k-surface is consistent with the Finnish medieval-side convention. No general MPO rule, physical stitch, new placement or catalogue error is established.'
    for o in load('research/continuation_20/intrinsic_10370/observations.json')['annotations']:
        append(first['observation_ids'], o['id'])
    append(first['limits'], 'Quem is expanded from an abbreviation and credens is partly uncertain; the normalized reference must not silently replace the literal reading. Cantus text came from public search indexing of primary database records, not inspection of those comparator images.')
    append(first['sources'], 'research/continuation_20/intrinsic_10370/results.json')
    append(first['sources'], 'https://cantusdatabase.org/chant/402240/')
    second = next(c for c in checks if c['id'] == 'CTX02')
    append(second['limits'], 'New indexed IV157 boundary assertions and its proposed interleaving of temporal/sanctoral units caution against an assumed simple global numbering sequence. This is a catalogue interpretation, not verified quire structure.')
    append(second['sources'], 'research/continuation_20/helsinki_access/source_assertions.json')
    c23_observations = load('research/continuation_20/c23/observations.json')['annotations']
    checks.append({
        'id': 'CTX04', 'title': 'Fr20274 against actual C23 pages and the editorial apparatus',
        'record_ids': ['mpo-20274', 'uub-c23-0144', 'uub-c23-0145'],
        'observation_ids': [o['id'] for o in c23_observations] + ['T-20274-invitatory', 'T-20274-order', 'T-20274-transition'],
        'summary': 'A declared ten-site comparison uses actual C23 attachments0144/0145, Fr20274 and Hallqvist PDF67. Eight target sites are evaluable at word/cue/structure level; two remain unavailable. Current readings, visible corrections and editorial reports of old states are recorded separately.',
        'outcome': 'Seven current/standard word or cue agreements and one written-scope difference; no distinctive shared uncorrected C23 error established. This does not establish copying direction, a unique transmission branch or physical identity.',
        'limits': ['Sites were selected after prior target/page review; this is not blind validation or a corpus-frequency test.', 'Cancelled C23 wording is only partly legible; full old states are editorial assertions where specified.', 'The target lacks the end of the second antiphon; two informative sites are explicitly unevaluable.', 'A written hymn cue differs; no performance omission is inferred.', 'C435 original images were not inspected. No melodic or correcting-hand/date inference is made.'],
        'sources': ['research/continuation_20/c23/collation.md', 'research/continuation_20/c23/collation.json',
                    'https://www.alvin-portal.org/alvin/view.jsf?pid=alvin-record:160517',
                    'https://lup.lub.lu.se/student-papers/record/9032430/file/9032431.pdf#page=67'],
    })
    dump('data/context_checks.v2.json', {'version': '2.0.0', 'assessment_date': '2026-10-23',
        'scope': 'Supporting source checks; no additional frozen attribution hypotheses.', 'checks': checks})
    print(json.dumps({'regions': len(observations), 'context_checks': len(checks), 'frozen_pairs': 10}))


if __name__ == '__main__':
    main()
