"""Render measured pilot results into inspectable Markdown reports, offline."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    v = json.loads((ROOT / 'data/validation.json').read_text())
    summary = json.loads((ROOT / 'data/ingestion_summary.json').read_text())
    experiment = json.loads((ROOT / 'data/evidence_experiment.json').read_text())
    evidence = json.loads((ROOT / 'data/review_bundle.json').read_text())
    regions = len(evidence['observations'])
    frame = v['results']['test']['same_genre']
    rows = []
    for method, result in frame['methods'].items():
        m = result['book_macro']
        rows.append(f"| {method} | {m['precision@5']:.4f} | {m['recall@5']:.4f} | {m['hit@5']:.4f} | {m['mrr']:.4f} |")
    table = '\n'.join(rows)
    control = next(c for c in v['literature_controls'] if c['left_id'] == 'mpo-1385' and c['right_id'] == 'mpo-20274')
    transfer = '\n'.join(f"| {method} | {data['rank_interval_all_imaged_records']} | {data['accepted_at_catalogue_calibration_threshold']} |" for method, data in control['methods'].items())
    validation = f'''# Validation report

Assessment updated: 22 October 2026. **Exploratory retrieval pilot and source-screening case study; no validated new attribution.** Machine-readable results: [validation](data/validation.json), [evidence experiment](data/evidence_experiment.json).

## Data and evaluation units

The current store has {summary['records']} records, {summary['physical_objects_with_images']} imaged physical objects and {summary['source_image_files']} source JPEGs. Features use {v['sample_images']} primary captures; two Finnish records share one physical leaf. Additional views are not additional test objects. Source rows may contain multiple leaves. Ten MPO reference groups contain six selected records each. Whole-book splits are development (285,270,875), calibration (1200,609,276), and test (1104,434,920,674). Twelve separate Beauvais leaf records form one supplementary positive control. They are not twelve independent books or a Nordic identity benchmark.

Each query searches other physical representatives within its split. Both sides/alternate views stay together; identical-hash and physical grouping checks prevent direct capture leakage. Same-genre evaluation skips queries with no different-book same-genre negative. Development/calibration therefore evaluate two books/12 queries each despite containing three planned groups; test evaluates four books/24 queries. Full exclusions and per-book metrics are in JSON. Catalogue group labels are provisional and may inherit historical errors; they are not independent expert truth.

## Methods and selection

Nine fixed methods compare metadata, layout, frozen ResNet18 embeddings and transparent combinations. Metadata uses missing-tolerant script/notation/layout/date/dimensions; cross-collection prose and structured dimensions are not assumed equivalent. Catalogue contents are sanitized summaries, not manuscript OCR or exact chant sequences. Explicit association labels, codex/CCM identifiers, account provenance and provider labels are excluded as predictors. Inherited catalogue dates/measurements can still leak group identity indirectly.

ResNet18 IMAGENET1K_V1 gives512-dimensional raw and fixed-paper-crop embeddings, CPU inference, no fitting. Weight SHA-256: `{v['model']['weights_sha256']}`. Layout descriptors are image-pattern proxies, not measured physical staff spacing or scribe identification. No specialized handwriting/music recognizer was adopted: no checked target transcription set exists for validating one. The amended goal continues source research with available methods; missing literature limits the affected originality claims.

Development/calibration require a complex method to improve MRR over metadata by at least0.02 on both partitions. None does; metadata remains selected. Test outcomes were inspected during the earlier pilot. Later ingestion/provenance repairs and added literature diagnostics are disclosed. Predictors/weights were not tuned after test, and main reference metrics remain identical to the archived initial results. This does not make the current experiment preregistered or newly untouched.

## Held-out book retrieval: same-genre gallery

All rates are fractions, macro-averaged across four reference book groups. Expected tie-aware metrics avoid identifier-based success. Each query has five same-label relevant gallery objects, which explains the equality of P@5 and recall@5 here.

| Method | P@5 | Recall@5 | Hit@5 | MRR |
|---|---:|---:|---:|---:|
{table}

Metadata P@5's descriptive book-bootstrap95% interval is0.875–1.000. Four books cannot support a strong population generalization; an MRR interval of1–1 in this selected sample does not establish certainty. No advanced variant improves the selected baseline.

## False acceptance is the critical failure

The selected calibration threshold is{v['thresholds']['metadata']['threshold']:.6f}. On132same-genre test pairs it gives60TP,40FP,0FN,32TN against catalogue labels: precision0.60 and false-positive rate40/72=0.5556. These denominators differ from top-k retrieval. Difficult-negative strata overlap and remain catalogue-derived; shared catalogue tokens do not establish identical chants or different scribes. Reliable identity-probability calibration was not achieved.

All nine methods accept published different-book8201–8304. Grajewski's p293 argument was re-read in the actual article and its table visually checked. Rejecting that pair using the publication is a scholarly-reference decision, not independent model improvement. Its antiphon continuity positive20106–8201 lacks the20106image and remains visually unevaluable.

## Target transfer

Documented positive1385–20274 is tested against the wider physical gallery, independently of the main split's retrieval claims. This diagnostic was added after initial review, not used to tune predictors.

| Method | Rank interval | Accepted at its calibration threshold |
|---|---|---|
{transfer}

Metadata ranks it26 and rejects it. A successful closed-gallery MRR therefore does not demonstrate useful identity discrimination for this target. No target-generalization accuracy can be inferred from this one selected check.

## Frozen evidence screen

Ten comparisons were frozen before this source/region review: seven controls or existing suggestions and the first three unestablished Fr1385 suggestions. The latter all belong to Ant39/Codex1200 and are correlated. Every case was screened; none was discarded from reporting. Outcomes: two previously documented positives(E), one published rejection(D), seven unresolved(C), zeroA/B and zero new confirmed findings. This is not a ten-example accuracy estimate. Existing scholarly labels informed the decisions, and one positive has no second image.

Fr8311's provisional image reading supports candidate Cantus006537/006537a and the catalogue's Septuagesima description. Concordances in distinct books show why that chant alone is not identifying evidence. No pitches or melodic variants were transcribed. Fr20274's overlapping photographs and the two-column25592comparison expose concrete capture/layout risks; neither proves a new physical attribution.

The independent source pass compared two candidate Fr20274 antiphon incipits against Hallqvist2020 edited C435, printedp6/PDF53, then checked higher-resolution invitatory wording against the apparatus and edited C23, printedp20/PDF67. The comparison separates visible source readings, the edited text and manuscript states reported by the editor. Apparent absence of separate pium, Matri…condolentes before procida…, and the written transition from Venite to Immolandus are provisional observations, not a unique witness fingerprint. No direct C435 manuscript-image inspection, melody or performance inference is claimed. See [text_collation.v2.json](data/text_collation.v2.json).

H02's selected decorated initials share traits also found among the Ant39 controls. Approximate ruler-normalized staff spacing shows no gross incompatibility, with overlapping endpoint-perturbation ranges. That is compatibility evidence, not same-book proof or a calibrated physical measurement. A full-deposit crosswalk resolves Hy49 to Fr25592 but leaves its historical association unresolved. Fr10370's II/ij-like and k-like marks are recorded separately from its conditional side assignment and already published placement. The hVIII–hIX catalogue comparison remains unresolved: different feast labels alone do not demonstrate incompatible text.

The export contains {regions} source regions and {len(evidence.get('context_checks', []))} supporting context checks, separate from the unchanged ten-pair queue. A possible reciprocal error in Duba2023's image-scaling equation is documented with dimensional derivation and three analytic controls; it is an implementation correction, not a historical discovery or a claim of first notice. These are post-review descriptive checks. No predictive method was fitted or newly validated. See [INDEPENDENT_RESEARCH_PASS.md](INDEPENDENT_RESEARCH_PASS.md).

## Reproduction and limits

Run `python -m lost_library run --offline`, then `python research/evidence_audit.py`. The evidence exporter checks frozen queue identity, exact source hashes and pixel bounds before exporting all cases. Unit tests protect source integrity, physical/capture leakage, tie handling and published controls; they cannot certify medieval identity. The final cached end-to-end replay succeeded without new source downloads. Numerical output is reproducible; provenance timestamps may change serialized hashes.

No independent specialist has reviewed our readings, no originals were examined, target side mapping is incomplete, and relevant Keskiaho/Taitto reading remains incomplete. These dependencies constrain particular claims; the amended goal permits further independent source tests. See [scientific limitations](SCIENTIFIC_LIMITATIONS.md) and the optional [reviewer packet](REVIEWER_PACKET.md).
'''
    (ROOT / 'VALIDATION_REPORT.md').write_text(validation)
    (ROOT / 'MATCHING_RESULTS.md').write_text('''# Matching results

The selected retrieval method is metadata; advanced generic-image methods do not demonstrate an improvement. Scores measure compatibility, not identity probability.

The full170suggestions are in [matches.json](data/matches.json). The frozen ten-comparison evidence queue is separate from this raw ranking; inspect [EVIDENCE_DOSSIERS.md](EVIDENCE_DOSSIERS.md) and [data/review_bundle.json](data/review_bundle.json). Three unexplained Fr1385 suggestions (4223,8311,8455) all belong to catalogueAnt39/Codex1200 and remain ambiguous after screening.

The known1385–20274 association ranks26 under metadata and is rejected at its threshold; the published different-book8201–8304 ranks first and is accepted. These failures limit the apparent high closed-gallery retrieval metrics. No new manuscript association is established. Exact methods, denominators, uncertainty and transfer diagnostics are in [VALIDATION_REPORT.md](VALIDATION_REPORT.md).
''')
    print('Wrote validation and matching reports from current JSON outputs.')


if __name__ == '__main__':
    main()
