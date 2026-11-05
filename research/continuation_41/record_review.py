"""Retain the AI's manual raw-pixel audit; this does not classify new images."""
import collections
import hashlib
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def distinct(points):
    kept = []
    for point in points:
        if all(math.dist(point, other) > 2 for other in kept):
            kept.append(point)
    return len(kept)


def main():
    # These are observations of the retained sheets, not algorithmic labels,
    # independent ground truth, probabilities or a new historical attribution.
    generic = 'isolated_generic_similarity'
    mismatch = 'context_mismatch'
    insufficient = 'insufficient_context'
    consistent = 'distinctive_context_consistent'
    rows = {
        '8994-1-2': [
            (generic, 'Single square note/stem; neighbouring ink differs.'),
            (insufficient, 'Fold/frame-edge feature; no distinctive shared context identified at this outlier.'),
            (insufficient, 'Fold ridge near the clipped right top edge; broader text lies on different sides of the band.'),
            (generic, 'Similar minims in different neighbouring word contexts.'),
            (insufficient, 'Lower/upper fold band; adjacent visible words do not provide a repeated passage.'),
            (insufficient, 'Fold ridge at the clipped right top edge; little common context.'),
            (generic, 'Similar small paired notational marks; neighbouring text differs.'),
            (generic, 'Notehead/stem resemblance with different neighbouring notes.'),
            (insufficient, 'Narrow ridge/black mark near right frame edge; insufficient shared context.'),
            (insufficient, 'Fold band near right frame edge; no distributed shared writing established.'),
            (generic, 'Small note/ligature resemblance; different surrounding notation.'),
            (generic, 'Ruling and note-stem vicinity; no distinctive ink sequence.'),
            (insufficient, 'Fold band close to right frame edge; no continuous repeated text.'),
            (insufficient, 'Small fold/ruling context; a common larger patch is not established.'),
            (insufficient, 'Fold ridge close to right frame edge; no continuous repeated text.'),
            (insufficient, 'Fold/ruling context with very limited common vertical coverage.'),
            (generic, 'Similar small note/stem; neighbouring word and notes differ.'),
            (mismatch, 'Left point is in a word; right point is among notes.'),
            (generic, 'Isolated notehead/stem with different adjacent notation.'),
            (mismatch, 'Left decorated initial/penwork is paired with right musical notation.'),
            (insufficient, 'Fold/ridge near clipped right top edge; adjacent initial is outside any demonstrated shared band.'),
            (generic, 'Small note resemblance; the adjacent oblique ligature differs.'),
            (generic, 'Similar paired square marks; broader ink sequence not shared.'),
            (insufficient, 'Fold/frame-edge outlier with no distinctive shared local sequence.'),
            (generic, 'Isolated notehead/stem and ruling; neighbours differ.'),
        ],
        '8994-3-4': [
            (generic, 'Similar oblique ligature, different neighbouring notes.'),
            (generic, 'Square note and oblique continuation are common shapes; context differs.'),
            (generic, 'Common square/oblique notation with different adjacent events.'),
            (generic, 'Minim/letter resemblance within different words.'),
            (generic, 'Common square/stem pattern; adjacent oblique shape differs.'),
            (mismatch, 'Word/minims on left versus musical notation on right.'),
            (generic, 'Single square/stem at ruling; different neighbours.'),
            (mismatch, 'Left word is paired with the right decorated initial/vertical border.'),
            (mismatch, 'Same location as point 7, another saved orientation: word versus decorated initial.'),
            (generic, 'Unmarked ruling vicinity without distinctive shared ink.'),
            (generic, 'Common letter/minim shapes, with a decorated initial and different word context on right.'),
            (generic, 'Nearby orientation of the previous letter-form resemblance; word context differs.'),
            (generic, 'Single square/stem; surrounding notes and words differ.'),
            (generic, 'Small minim/letter cluster in differing neighbouring context.'),
            (generic, 'Same position as point 13, another saved orientation of the minim resemblance.'),
            (mismatch, 'Left small word/minims versus right large decorated initial vicinity.'),
            (mismatch, 'Left small word/minims versus right decorated initial.'),
            (generic, 'Single square note/stem; different adjacent notation.'),
            (generic, 'Simple paired/square marks with differing adjacent notes.'),
            (generic, 'Ruling vicinity below an isolated note; no distinctive common sequence.'),
            (generic, 'Ruling and square/stem, different broader context.'),
            (generic, 'Simple note/ruling pattern with different neighbours.'),
            (mismatch, 'Left ruling below a note versus right decorated initial top.'),
            (generic, 'Common letter shapes in different neighbouring words.'),
            (generic, 'Single notehead/stem and ruling, different neighbouring events.'),
        ],
        '20274-overlap-positive': [
            (consistent, 'Same initial, nearby pale curved mark and ruling sequence.'),
            (consistent, 'Same multi-letter ink sequence and red ruling.'),
            (consistent, 'Same initial/letter sequence and neighbouring square marks.'),
            (consistent, 'Same multi-letter sequence, penwork and ruling.'),
            (consistent, 'Same multi-letter sequence and ink contours.'),
            (generic, 'Mostly blank/ruling context with a small vertical mark; this patch alone is weak.'),
        ],
        '8994-1-3-nonrepeat': [
            (generic, 'Similar minim strokes in different word context.'),
            (generic, 'Single square note/stem; neighbouring events differ.'),
            (generic, 'Same positions as previous item; another saved orientation.'),
            (generic, 'Similar vertical notation/rule motif, with different neighbouring note groups.'),
            (generic, 'Same positions as previous item; another saved orientation.'),
            (generic, 'Common vertical two-square motif; adjacent neumes and text differ.'),
            (generic, 'Same positions as previous item; another saved orientation.'),
        ],
    }
    manifest = json.loads((HERE / 'review_manifest.json').read_text())
    review = {'version': '1.0.0', 'date': '2026-10-28',
        'reviewer': 'project AI, manual visual inspection of all four retained raw-patch sheets and E35 original-pixel fold strip',
        'independent_review': False, 'blind': False,
        'scope': 'Local raw-pixel context assessment only; no new fitting, medieval-side assignment or historical book label.',
        'coordinate_manifest': 'research/continuation_41/review_manifest.json',
        'unit_warning': 'Stored descriptor correspondences include repeated orientations/nearby points; counts are not independent observations or accuracy estimates.',
        'comparisons': {}}
    for ident, observations in rows.items():
        items = manifest['selections'][ident]['items']
        assert len(items) == len(observations)
        review['comparisons'][ident] = [dict(index=item['index'],
            ransac_inlier=item['ransac_inlier'], outcome=observation[0], observation=observation[1])
            for item, observation in zip(items, observations)]
    (HERE / 'manual_review.json').write_text(json.dumps(review, indent=2)+'\n')
    summaries = {}
    for ident, observations in review['comparisons'].items():
        items = manifest['selections'][ident]['items']
        inliers = [item for item in items if item['ransac_inlier']]
        summaries[ident] = {'reviewed_correspondences': len(items),
            'manual_outcomes': dict(collections.Counter(r['outcome'] for r in observations)),
            'reviewed_inliers': len(inliers),
            'inlier_outcomes': dict(collections.Counter(r['outcome'] for r in observations if r['ransac_inlier'])),
            'distinct_inlier_positions_2px_left_right': [distinct([r['sources'][s]['point_xy'] for r in inliers]) for s in [0, 1]],
            'original_screen_passed': manifest['selections'][ident]['original_screen_passed']}
    fixed = ['research/continuation_35/protocol.json', 'research/continuation_35/feature_results.json',
        'research/continuation_35/results.json', 'data/fragments.json', 'research/mpo.csv']
    fixed += list(json.loads((ROOT / 'research/continuation_33/results.json').read_text())['frozen_inputs'])
    result = {'version': '1.0.0', 'date': '2026-10-28',
        'question': json.loads((HERE / 'protocol.json').read_text())['question'],
        'summaries': summaries,
        'direct_result': 'All ten 1/2 inliers lie in the narrow fold/frame-edge band: the right points are within 37px of the top, and left points within 36px of the bottom. This remains insufficient context for a secure local identification. The six 3/4 inliers include two orientations of a word-to-decorated-initial mismatch and otherwise generic note/minim/ruling similarities. No candidate patch is assessed as distinctive shared context.',
        'control_result': 'Five of six deterministic positive-control patches show the same multi-feature writing context; the sixth is weak ruling context. The seven nonrepeat-control inliers show generic motifs at four distinct positions. These are selected patch audits, not an accuracy or sensitivity estimate.',
        'interpretation': 'The manual audit explains why small residuals or a few matching glyphs cannot promote either failed E35 boundary. It does not refute the possibility that the 1/2 fold band repeats photographed detail. Incompatible selected keypoints do not prove that entire photographs cannot overlap.',
        'prior_exposure': 'Post hoc, nonblind AI review of already inspected images/feature results; not independent confirmation.',
        'optional_row_audit': 'Not performed in E41. Any future row-count consistency must include deliberately mismatched grouping controls and cannot alone establish a medieval side.',
        'next_test': 'Audit whole-capture text-row coverage and exact boundary text using the existing photos, including wrong-grouping controls; seek distinctive uninterrupted source context before assigning a complete surface. E40 Finnish original and prior-art dependencies remain separate.',
        'accepted_photographic_overlap': False, 'complete_surface_map_established': False,
        'physical_join_established': False, 'new_codex_attribution': False,
        'novelty_cleared': False, 'independent_confirmation': False,
        'changed_e35_screen': False, 'new_download_bytes': 0,
        'unchanged_inputs': {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in fixed}}
    (HERE / 'results.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(summaries, indent=2))


if __name__ == '__main__':
    main()
