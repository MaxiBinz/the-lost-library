"""Reproduce a dimensional-invariance check and current capture/face prerequisites.

No new image fetching, fitting, manuscript attribution, or expert review.
The numerical scaling examples are analytic controls, not measured manuscripts.
"""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    controls = []
    for width, source_scale, target_scale in [(800, 4, 4), (800, 8, 4), (1200, 12, 3)]:
        original_mm = width / source_scale
        corrected = width * target_scale / source_scale
        printed = width * source_scale / target_scale
        controls.append({
            'kind': 'analytic scale-invariance control, not empirical manuscript data',
            'width_px': width, 'source_px_per_mm': source_scale,
            'target_px_per_mm': target_scale, 'physical_width_mm': original_mm,
            'prose_ratio_output_px': corrected, 'displayed_ratio_output_px': printed,
            'prose_ratio_preserves_physical_width': abs(corrected / target_scale - original_mm) < 1e-10,
            'displayed_ratio_preserves_physical_width': abs(printed / target_scale - original_mm) < 1e-10,
            'displayed_ratio_physical_error_factor': (printed / target_scale) / original_mm,
        })
    assert all(x['prose_ratio_preserves_physical_width'] for x in controls)
    assert [x['displayed_ratio_preserves_physical_width'] for x in controls] == [True, False, False]

    fragments_path = ROOT / 'data/fragments.json'
    queue_path = ROOT / 'data/hypotheses.v1.json'
    records = {r['id']: r for r in json.loads(fragments_path.read_text())}
    queue = json.loads(queue_path.read_text())['hypotheses']
    ids = sorted({q[k] for q in queue for k in ('left_id', 'right_id')})
    objects, files = [], set()
    for ident in ids:
        r = records[ident]
        captures = r.get('captures', [])
        unique_views = {c.get('canvas_id') or (c.get('label'), c.get('capture_index')) for c in captures}
        for c in captures:
            path = ROOT / c['path']
            assert path.is_file() and sha(path) == c['sha256'], c['path']
            files.add(c['path'])
        objects.append({
            'id': ident, 'physical_object_id': r.get('physical_object_id', ident),
            'catalogued_leaves': r.get('normalized', {}).get('leaves'),
            'stored_capture_files': len(captures), 'distinct_source_view_keys': len(unique_views),
            'source_view_keys': [str(v) for v in sorted(unique_views, key=str)],
            'verified_recto_verso_assignment_from_this_check': False,
            'reason': 'Capture ordinals and resolution variants are not medieval side assignments; no source-side adjudication made by inventory audit.',
        })
    pair_tests = [{
        'hypothesis': q['id'], 'left_id': q['left_id'], 'right_id': q['right_id'],
        'both_objects_have_images': bool(records[q['left_id']].get('image_path') and records[q['right_id']].get('image_path')),
        'direct_join_or_original_quire_conclusion_from_capture_ordinals': 'not justified',
    } for q in queue]
    data = {
        'version': '1.0.0', 'assessment_date': '2026-10-22',
        'source': {'author': 'William Duba', 'title': 'Finding the Prior Leaf: Manuscript Fragments and Original Codices',
                   'doi': '10.24446/j9en', 'article_url': 'https://www.fragmentology.ms/article/view/4499',
                   'read_scope': 'Complete article text, printed5–65/PDF7–67; selected methodological pages rendered and visually inspected',
                   'full_issue_pdf_sha256': 'daa2a0a3ecebfeb40788a64f0313079ad8379612db565889fbb4e5772c7009af',
                   'downloaded_bytes': 26149638,
                   'copy': 'private reading copy, excluded from release'},
        'method_page_map': {
            'leaf_bifolium_and_orientation': {'printed': [7, 21], 'pdf': [9, 23]},
            'calibrated_layout_and_text_extrapolation': {'printed': [23, 44], 'pdf': [25, 46]},
            'missing_leaves_and_gatherings': {'printed': [44, 58], 'pdf': [46, 60]},
            'image_calibration_and_scaling': {'printed': [61, 64], 'pdf': [63, 66]},
        },
        'scaling_consistency': {
            'printed_page': 64, 'pdf_page': 66,
            'prose_operation': 'new_width_px = width_px * Smin / Sn',
            'displayed_equation_operation': 'new_width_px = width_px * Sn / Smin',
            'source_verification': 'Both operations verified on the rendered full page; not inferred only from PDF extraction order.',
            'own_dimensional_derivation': 'An object of length L at Sn pixels/mm has width L*Sn. At Smin pixels/mm its target width is L*Smin, requiring factor Smin/Sn.',
            'conclusion': 'Displayed equation reverses the prose ratio; use Smin/Sn to preserve physical dimensions.',
            'classification': 'Source-backed implementation correction / possible typographical erratum; not claimed first notice or new historical finding.',
            'analytic_controls': controls,
        },
        'capture_orientation_prerequisites': {
            'fragments_sha256': sha(fragments_path), 'queue_sha256': sha(queue_path),
            'objects': objects, 'pair_tests': pair_tests,
            'distinct_queue_records': len(ids),
            'imaged_physical_objects': len({r['physical_object_id'] for r in objects if r['stored_capture_files']}),
            'distinct_stored_capture_files': len(files),
            'pairs_with_two_imaged_objects': sum(p['both_objects_have_images'] for p in pair_tests),
            'conclusion': 'All available queue images pass stored hashes. Source capture grouping alone cannot orient leaves or establish any new same-book association.',
        },
        'target_application': {
            'hypotheses': ['H01', 'H03'], 'fragment_id': 'mpo-20274',
            'view_a': 'data/images/mpo-20274.jpg', 'view_b': 'data/images/mpo-20274-capture-2.jpg',
            'observation': 'Existing overlapping upper/lower writing areas were visually rechecked. New resolution variants in the current store share the same source canvas IDs and are not new sides.',
            'consequence': 'Treat these as two views of an overlapping writing surface; do not derive recto-to-verso continuity or missing-leaf counts from their ordinals.',
            'not_established': ['Original recto/verso designation', 'A new physical association with another object', 'Calibrated staff spacing or original written dimensions from this pass'],
        },
        'protocol': [
            {'step': 1, 'action': 'Separate object, source photograph and resolution derivative; attach source hashes and preserve catalogue wording.', 'record': 'object_id, canvas_id, capture_index, derivative_of, sha256'},
            {'step': 2, 'action': 'Read enough exact text and inspect visible folds/paratext to test orientation; retain multiple orientations if clues conflict.', 'record': 'literal transcription, pixel regions, orientation alternatives'},
            {'step': 3, 'action': 'Calibrate each photograph from explicit ruler ticks, validate distant intervals/axes, and record coordinate choices and perspective limits.', 'record': 'tick coordinates, ruler units, px_per_mm, validation discrepancy'},
            {'step': 4, 'action': 'Compare staff or text-line intervals at a shared physical scale; measure intervals, not the count of baseline endpoints.', 'record': 'source coordinate endpoints, interval count, physical estimate and uncertainty'},
            {'step': 5, 'action': 'Establish which actual edition/witness passage corresponds; test for variants, rubrics and missing material before any text-length extrapolation.', 'record': 'edition identifiers/pages, exact source passage, variant ledger'},
            {'step': 6, 'action': 'For chant, do not substitute character counts for music-system capacity without validation: melisma, rubrics and varying notation density can change spacing.', 'record': 'genre-specific applicability decision; abstain where density is not validated'},
            {'step': 7, 'action': 'Test proposed joins against unchanged positive and difficult-negative controls; treat folds and holes as potentially belonging to later reuse.', 'record': 'positive/negative/unknown outcomes and contrary evidence'},
            {'step': 8, 'action': 'Report only the reconstruction constraints actually observed; leave side, gap and gathering extents unknown when prerequisites fail.', 'record': 'supported constraint, alternatives, exact dependency'},
        ],
        'independent_expert_review': False, 'new_historical_finding': False,
        'limits': ['One AI reading is not expert validation.', 'The source method does not automatically establish manuscript identity.', 'Numerical controls test dimensional consistency, not performance on historical labels.', 'No claim that the scaling inconsistency is unreported in existing errata.', 'No physical millimetre measurement is reported from the exploratory ruler crops.'],
    }
    (OUT / 'protocol-results.json').write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'scaling_controls': len(controls), 'prose_invariance': True, 'display_equation_counterexamples': 2,
                      'queue_pairs': len(pair_tests), 'imaged_pairs': data['capture_orientation_prerequisites']['pairs_with_two_imaged_objects'],
                      'images_hash_checked': len(files), 'output': str(OUT / 'protocol-results.json')}, indent=2))


if __name__ == '__main__':
    main()
