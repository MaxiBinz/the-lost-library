# Validation report

Assessment updated: 24 October 2026. **Exploratory retrieval pilot and source-screening case study; no validated new attribution.** Machine-readable results: [validation](data/validation.json), [evidence experiment](data/evidence_experiment.json).

## Data and evaluation units

The current store has 129 records, 120 imaged physical objects and 167 source JPEGs. Features use 121 primary captures; two Finnish records share one physical leaf. Additional views are not additional test objects. Source rows may contain multiple leaves. Ten MPO reference groups contain six selected records each. Whole-book splits are development (285,270,875), calibration (1200,609,276), and test (1104,434,920,674). Twelve separate Beauvais leaf records form one supplementary positive control. They are not twelve independent books or a Nordic identity benchmark.

Each query searches other physical representatives within its split. Both sides/alternate views stay together; identical-hash and physical grouping checks prevent direct capture leakage. Same-genre evaluation skips queries with no different-book same-genre negative. Development/calibration therefore evaluate two books/12 queries each despite containing three planned groups; test evaluates four books/24 queries. Full exclusions and per-book metrics are in JSON. Catalogue group labels are provisional and may inherit historical errors; they are not independent expert truth.

## Methods and selection

Nine fixed methods compare metadata, layout, frozen ResNet18 embeddings and transparent combinations. Metadata uses missing-tolerant script/notation/layout/date/dimensions; cross-collection prose and structured dimensions are not assumed equivalent. Catalogue contents are sanitized summaries, not manuscript OCR or exact chant sequences. Explicit association labels, codex/CCM identifiers, account provenance and provider labels are excluded as predictors. Inherited catalogue dates/measurements can still leak group identity indirectly.

ResNet18 IMAGENET1K_V1 gives512-dimensional raw and fixed-paper-crop embeddings, CPU inference, no fitting. Weight SHA-256: `f37072fd47e89c5e827621c5baffa7500819f7896bbacec160b1a16c560e07ec`. The layout descriptors are image-pattern proxies, not physical staff measurements or scribe identification. E21 separately reports manually selected, ruler-calibrated staff intervals from two sources; these were not predictors and do not update the benchmark. No specialized handwriting/music recognizer was adopted: no checked target transcription set exists for validating one. The amended goal continues source research with available methods; missing literature limits the affected originality claims.

Development/calibration require a complex method to improve MRR over metadata by at least0.02 on both partitions. None does; metadata remains selected. Test outcomes were inspected during the earlier pilot. Later ingestion/provenance repairs and added literature diagnostics are disclosed. Predictors/weights were not tuned after test, and main reference metrics remain identical to the archived initial results. This does not make the current experiment preregistered or newly untouched.

## Held-out book retrieval: same-genre gallery

All rates are fractions, macro-averaged across four reference book groups. Expected tie-aware metrics avoid identifier-based success. Each query has five same-label relevant gallery objects, which explains the equality of P@5 and recall@5 here.

| Method | P@5 | Recall@5 | Hit@5 | MRR |
|---|---:|---:|---:|---:|
| metadata | 0.9500 | 0.9500 | 1.0000 | 1.0000 |
| layout | 0.5333 | 0.5333 | 0.8750 | 0.8512 |
| embedding | 0.7667 | 0.7667 | 1.0000 | 0.9722 |
| embedding_raw | 0.8417 | 0.8417 | 1.0000 | 0.9792 |
| metadata_layout | 0.9167 | 0.9167 | 1.0000 | 1.0000 |
| metadata_embedding | 0.9250 | 0.9250 | 1.0000 | 1.0000 |
| metadata_text | 0.9167 | 0.9167 | 1.0000 | 1.0000 |
| fusion | 0.8833 | 0.8833 | 1.0000 | 1.0000 |
| fusion_text | 0.9000 | 0.9000 | 1.0000 | 1.0000 |

Metadata P@5's descriptive book-bootstrap95% interval is0.875–1.000. Four books cannot support a strong population generalization; an MRR interval of1–1 in this selected sample does not establish certainty. No advanced variant improves the selected baseline.

## False acceptance is the critical failure

The selected calibration threshold is0.775811. On132same-genre test pairs it gives60TP,40FP,0FN,32TN against catalogue labels: precision0.60 and false-positive rate40/72=0.5556. These denominators differ from top-k retrieval. Difficult-negative strata overlap and remain catalogue-derived; shared catalogue tokens do not establish identical chants or different scribes. Reliable identity-probability calibration was not achieved.

All nine methods accept published different-book8201–8304. Grajewski's p293 argument was re-read in the actual article and its table visually checked. Rejecting that pair using the publication is a scholarly-reference decision, not independent model improvement. Its antiphon continuity positive20106–8201 lacks the20106image and remains visually unevaluable.

## Target transfer

Documented positive1385–20274 is tested against the wider physical gallery, independently of the main split's retrieval claims. This diagnostic was added after initial review, not used to tune predictors.

| Method | Rank interval | Accepted at its calibration threshold |
|---|---|---|
| metadata | [26, 26] | False |
| layout | [67, 67] | True |
| embedding | [11, 11] | True |
| embedding_raw | [6, 6] | True |
| metadata_layout | [29, 29] | True |
| metadata_embedding | [19, 19] | False |
| metadata_text | [20, 20] | True |
| fusion | [24, 24] | True |
| fusion_text | [19, 19] | True |

Metadata ranks it26 and rejects it. A successful closed-gallery MRR therefore does not demonstrate useful identity discrimination for this target. No target-generalization accuracy can be inferred from this one selected check.

## Frozen evidence screen

Ten comparisons were frozen before this source/region review: seven controls or existing suggestions and the first three unestablished Fr1385 suggestions. The latter all belong to Ant39/Codex1200 and are correlated. Every case was screened; none was discarded from reporting. Outcomes: two previously documented positives(E), one published rejection(D), seven unresolved(C), zeroA/B and zero new confirmed findings. This is not a ten-example accuracy estimate. Existing scholarly labels informed the decisions, and one positive has no second image.

Fr8311's provisional image reading supports candidate Cantus006537/006537a and the catalogue's Septuagesima description. Concordances in distinct books show why that chant alone is not identifying evidence. No pitches or melodic variants were transcribed. Fr20274's overlapping photographs and the two-column25592comparison expose concrete capture/layout risks; neither proves a new physical attribution.

The independent source pass compared two candidate Fr20274 antiphon incipits against Hallqvist2020 edited C435, printedp6/PDF53, then checked higher-resolution invitatory wording against the apparatus and edited C23, printedp20/PDF67. The comparison separates visible source readings, the edited text and manuscript states reported by the editor. Apparent absence of separate pium, Matri…condolentes before procida…, and the written transition from Venite to Immolandus are provisional observations, not a unique witness fingerprint. No direct C435 manuscript-image inspection, melody or performance inference is claimed. See [text_collation.v2.json](data/text_collation.v2.json).

H02's selected decorated initials share traits also found among the Ant39 controls. E19's preliminary ruler-normalized staff-spacing comparison shows no gross incompatibility, but that earlier endpoint-perturbation screen was not calibrated. E21 separately calibrates selected Fr10370/10406 staff intervals at about 5.6 mm each; this supports page-layout consistency, not same-book proof. A full-deposit crosswalk resolves Hy49 to Fr25592 but leaves its historical association unresolved. Fr10370's II/ij-like and k-like marks are recorded separately from its conditional side assignment and already published placement. The hVIII–hIX catalogue comparison remains unresolved: different feast labels alone do not demonstrate incompatible text.

The export contains 36 source regions and 3 supporting context checks, separate from the unchanged ten-pair queue. A possible reciprocal error in Duba2023's image-scaling equation is documented with dimensional derivation and three analytic controls; it is an implementation correction, not a historical discovery or a claim of first notice. These are post-review descriptive checks. No predictive method was fitted or newly validated. See [INDEPENDENT_RESEARCH_PASS.md](INDEPENDENT_RESEARCH_PASS.md).

## Reproduction and limits

Run `python -m lost_library run --offline`, then `python research/evidence_audit.py`. The evidence exporter checks frozen queue identity, exact source hashes and pixel bounds before exporting all cases. Unit tests protect source integrity, physical/capture leakage, tie handling and published controls; they cannot certify medieval identity. The final cached end-to-end replay succeeded without new source downloads. Numerical output is reproducible; provenance timestamps may change serialized hashes.

No independent specialist has reviewed our readings, no originals were examined, target side mapping is incomplete, and relevant Keskiaho/Taitto reading remains incomplete. These dependencies constrain particular claims; the amended goal permits further independent source tests. See [scientific limitations](SCIENTIFIC_LIMITATIONS.md) and the optional [reviewer packet](REVIEWER_PACKET.md).

## E21 supplementary source check

The E21 ruling-pitch experiment is a reproducible, post-inspection descriptive check, not a change to the frozen benchmark. It uses two Fr 10370 and three Fr 10406 four-rule systems, with explicit ruler endpoints and center coordinates recorded in [`ruling_pitch_results.json`](research/continuation_21/ruling_pitch_results.json). The means are approximately 5.6 mm in both fragments. The complete 22,909-row MPO export screen finds 9,196 Quadr/four-line entries, 197 with 11 text rows, and 149 with parseable written-area dimensions; three other records fall in the exact target size box and ten in the ±1 cm sensitivity box. These catalogue counts are not a random sample or a rarity estimate; the source itself supplies the Codex 1505 grouping. The result supports consistency, not independent confirmation. See [full E21 protocol and limits](research/continuation_21/ruling_pitch_results.md).

The E21 reproduction script verified the pinned image and CSV checksums and reproduced the measurements and catalogue counts. The updated evidence export contains 60 source-linked regions and five supporting context checks; the frozen queue and predictors are unchanged. All 35 Python tests, the viewer test, the evidence/export commands, and the source-integrity and resource audits passed after integration. These checks establish package consistency and repeatability, not historical truth, uniqueness, or independent scholarly confirmation.

## E22 supplementary control and current checks

The [E22 control report](RESEARCH_CONTINUATION_22.md) records one metadata-selected different-codex page, Fr 7292. Its measured 5.543 mm pitch is effectively the same as the E21 target mean of 5.601 mm within the conservative manual uncertainty. This falsifies the claim that this approximate pitch is unique in the available matched catalogue sample; one control cannot estimate prevalence or validate a classifier. Selection was not blind, and Codex 1306 is an MPO label rather than independent adjudication.

The evidence export now validates 62 regions and seven context checks. The source-integrity check verifies hashes/dimensions for all six auxiliary comparison files and confirms three auxiliary comparison pages remain outside the frozen queue and core gallery. All 35 Python tests, the viewer test, the E22 measurement reproduction, evidence/export, and resource audit pass. The audit counts 173 working image files and a 1,192,461,796-byte planning total including a 1 GB reserve; exact lifetime traffic is still unverified. These checks establish data consistency and arithmetic reproducibility, not historical truth or originality.

## E24 H03 metadata screen and evidence export

The [E24 script](research/continuation_24/h03_layout_screen.py) verifies the pinned MPO CSV SHA-256, computes the Quadr/four-line/11-row and Antiphonarium cohorts, and reproduces H03's dimension sensitivity counts. It reports 244 broad-cohort records (154 dimensioned), 97 Antiphonaria (52 dimensioned), and same-genre match counts of 2, 7 and 8 for the candidate-pair box expanded by 0, 0.5 and 1 cm. This is a reproducible metadata query, not an image measurement or a test of historical truth.

The separate context integration script adds CTX08 without changing the frozen ten-pair queue. The evidence export reports ten cases, 62 validated regions and eight context checks. Final E24 checks: all **35 Python unit tests** and the viewer test passed; the E20/E22/E24 source-integrity check reports 10 cases, 62 regions, eight contexts, unchanged core data and thresholds, and no confirmed new finding; the E24 query reproduced its 244/154 and 97/52 denominators and 2/7/8 same-genre sensitivity counts; all **167 core source-image hashes and dimensions** passed; the resource audit reports **173 working image files** and a conservative **1,192,461,796-byte** plan against 3 GB, with exact lifetime traffic still unverified. Evidence and static-site exports completed with 129 fragments and 170 ranked matches. The generated site data includes CTX08 and the viewer JavaScript points to E24; visual inspection through the loopback browser was blocked by the browser policy gate, so this turn verifies the static bundle and automated viewer checks rather than the live rendered card. These technical checks establish consistency and repeatability, not originality or attribution truth.

## E26 BOMPAC row-level prior-art check and current verification

The read-only [E26 query](research/continuation_26/bompac/target_crosswalk.py) matches the five locally retained BOMPAC file MD5 checksums to Zenodo's published values and writes the exact target memberships to [target_crosswalk_results.json](research/continuation_26/bompac/target_crosswalk_results.json). It reproduces BOMPAC-5324 (28 included combined rows) and BOMPAC-912 (20 rows), plus raw MPO units M-1217 (five Codex 1505 leaves), C-35 (five Ant 99 leaves), and F-1385 (singleton). These are dataset assertions, not an image analysis or independent historical verdict.

Integration refreshes CTX07 in `data/context_checks.v7.json`; it does not modify `data/hypotheses.v1.json`, the predictor inputs, threshold or source images. The evidence export still reports **10 cases, 62 validated regions, eight context checks, 2 E / 7 C / 1 D, and zero newly confirmed findings**. The E20 source-integrity script confirms the queue SHA, core fragment data, predictors and thresholds are unchanged; all **167 core image hashes and dimensions** pass. All **35 Python tests** and the viewer test pass. The updated resource audit counts 173 working image files and a conservative **1,214,387,652-byte** plan against the 3 GB limit; the exact lifetime transfer total remains unverified. Browser visual/accessibility review remains incomplete. These checks support reproducibility and data integrity only; they do not establish attribution, originality or expert confirmation.

Reproduce the E26 source query and integrate it with:

```sh
.venv/bin/python research/continuation_26/bompac/target_crosswalk.py
.venv/bin/python research/continuation_26/bompac/integrate_context.py
.venv/bin/python -m lost_library evidence
.venv/bin/python -m lost_library export
.venv/bin/python -m unittest discover -s tests -q
node --test tests/viewer.test.cjs
.venv/bin/python research/continuation_20/checks.py
.venv/bin/python research/audit_resources.py
```

## E27 prior-art crosswalk and current checks

The [E27 query](research/continuation_27/related_unit_crosswalk.py) verified both published workbook checksums and reproduced the included rows in BOMPAC-9531, BOMPAC-912 and BOMPAC-5324. It distinguishes the catalogue's explicit Ant 242/Fr 29666 same-codex link from its broader suggestions; BOMPAC places IV.173, Fr 29666 and Fr 25592 together, while Ant 99/IV.157 remains in a separate unit. This is a published-source crosswalk, not new manuscript evidence or an independent historical verdict. See [the E27 report](RESEARCH_CONTINUATION_27.md).

Integration adds CTX09 and updates H03–H05's context while preserving the frozen queue hash. The export at that stage reported **10 cases, 62 validated regions, nine context checks, 2 E / 7 C / 1 D, and zero newly confirmed findings**; the static-site export contained 129 fragments and 170 ranked matches. The E20 source-integrity check confirmed the unchanged queue, core fragment data, predictors and thresholds; all **167 core image hashes and dimensions** passed. All **35 Python tests** and the viewer test passed. The resource audit counted 173 working image files and a conservative **1,214,387,652-byte** planning total against the 3 GB ceiling; exact lifetime transfer remains unverified. The ordinary Fr 29666 archive route showed a CAPTCHA, which was not interacted with; this does not establish general unavailability. These checks support reproducibility and data integrity, not historical truth or originality.

## E28 prior-art refinement and current checks

The [E28 record](RESEARCH_CONTINUATION_28.md) documents the institutional metadata and indexed excerpt for Ville Walta's peer-reviewed 2013 chapter. The excerpt describes a broad group that includes F.m.IV.156, IV.157 and IV.173, with several hands and uncertain place of production. The full PDF timed out, so E28 treats this as a prior-art lead rather than a full-chapter review. Its main consequence is interpretive: the E27 catalogue and BOMPAC memberships may describe different relationship levels; no contradiction or new historical finding is established.

The [E29 integration script](research/continuation_29/integrate_context.py) adds CTX11, points the review data to context v10 and preserves the frozen queue hash. The current evidence export reports **10 cases, 62 validated regions, 11 context checks, 2 E / 7 C / 1 D, and zero newly confirmed findings**. The static-site export contains 129 fragments and 170 ranked matches. The E27 workbook query verified two published checksums and reproduced all eight selected rows. The E20 source-integrity check confirms the unchanged queue, core fragments, predictors and thresholds; all **167 core image hashes and dimensions** pass. All **35 Python unit tests** and the viewer test pass. The resource audit counts **173 working image files** and a conservative **1,214,387,652-byte** plan against 3 GB; exact lifetime transfer remains unverified. E29 added no manuscript images or image transfers. Full browser visual/accessibility review remains incomplete. These checks confirm package consistency and repeatability, not historical truth or originality.

Reproduce the current checks with:

```sh
.venv/bin/python research/continuation_27/related_unit_crosswalk.py
.venv/bin/python research/continuation_28/integrate_context.py
.venv/bin/python research/continuation_31/integrate.py
.venv/bin/python -m lost_library evidence
.venv/bin/python -m lost_library export
.venv/bin/python research/continuation_20/checks.py
.venv/bin/python research/evidence_audit.py
.venv/bin/python research/audit_resources.py
.venv/bin/python -m unittest discover -s tests -v
node --test tests/viewer.test.cjs
```

## E30 H08–H10 prior-reconstruction crosswalk and current checks

The read-only [E30 query](research/continuation_30/bompac_suggestion_crosswalk.py) rechecks the published MD5 values for the two already downloaded BOMPAC workbooks and preserves the ten-case queue hash. It finds Fr 4223/8311/8455 together in BOMPAC-258 / Ant-39 / Codex-1200 / F.m.IV.159, while Fr 1385 is in BOMPAC-912 / Ant-99 / F.m.IV.157. The raw workbook groups the suggestions in C-17 and lists Fr 1385 as singleton F-1385. These related workbook assignments are prior reconstruction data, not fresh image proof or independent expert adjudication; H08–H10 remain C.

The E30 integration updates only the source context for those three reviews; it leaves all labels, observations, images, predictors, thresholds and the frozen queue unchanged. Reproduction completed: the BOMPAC MD5 checks passed, evidence export reported **10 cases, 62 regions, 11 context checks, 2 E / 7 C / 1 D, zero newly confirmed findings**, and the site export reported **129 fragments, 170 matches and 16 dossiers**. All **35 Python unit tests**, the Node viewer test, the E20 source-integrity check, the 167-image evidence audit and the resource audit passed. The resource audit remains 173 working image files and a conservative 1,214,387,652-byte plan against 3 GB; exact lifetime traffic remains unverified. The local release archive now includes the two CC BY 4.0 BOMPAC workbook inputs, passes checksum verification and extracted offline replay, and contains 548 allowlisted files. These checks verify reproducibility and package consistency, not historical truth, novelty or physical identity. Full responsive/accessibility review remains incomplete.

## E31 official catalogue context and current checks

The [E31 result](research/continuation_31/fragmenta_relationship_results.json) records the exact relationship labels exposed by the National Library of Finland's official Fragmenta entries and the possible `k`/IV opening-signature test lead. Its integration adds CTX12 and updates H03's evidence text without changing any case classification, image annotation, predictor, threshold or queue entry. The current evidence export reports **10 cases, 62 regions, 12 context checks, 2 E / 7 C / 1 D, zero newly confirmed findings**; the site export reports **129 fragments, 170 matches and 16 dossiers**. The E20 source-integrity check confirms the frozen data remain unchanged. All **35 Python unit tests**, the Node viewer test and the offline source-integrity script passed.

The local review archive was rebuilt with the E31 files: 551 allowlisted files. Archive checksums and extracted offline replay passed; see `output/research/package_verification.json` for the current byte count and SHA-256. Scientific metrics and frozen screening results were unchanged. No manuscript image was added. These checks establish reproducible packaging, not historical truth, originality or physical identity. Full responsive/accessibility review remains incomplete.

## E32 source-linked observation and current package

E32 adds one source-linked annotation on the existing Fr 8994 image, not a new image or hypothesis. The mark is consistent with the catalogue's `IIII` transcription, while the official IV.156 indexed description says this opening-signature convention was not infrequent. The observation therefore sharpens a test lead but does not make it a distinctive codex fingerprint. H03 remains C.

The current evidence export reports **10 cases, 63 regions, 13 context checks, 2 E / 7 C / 1 D, and zero newly confirmed findings**; the static-site export reports **129 fragments, 170 matches and 16 dossiers**. All **35 Python unit tests** and the Node viewer test passed. The evidence audit checked 167 source-image hashes/dimensions with no hash failures; the resource audit counts 173 working image files and a conservative 1,214,387,652-byte plan against 3 GB, with exact lifetime traffic still unverified.

The rebuilt local review archive contains **558 files**. Its exact byte count and SHA-256 are recorded in `output/research/package_verification.json`. Archive checksums and extracted offline replay passed; scientific metrics and frozen screen results were unchanged. This verifies reproducibility and package integrity, not attribution, novelty, or full installation. Responsive layout, accessibility and unexercised viewer workflows remain incompletely reviewed.


## Current E33/E34 overlay checks — 25 October 2026

All 45 Python tests and both Node viewer test files pass. The new regression checks cover explicit physical identity versus shared labels, qualified associations, the coexistence of same-hand and published negative same-codex claims, image-resolution grouping, missing inputs versus negatives, full lead coverage, confidence/identity promotion rejection and invalid regions.

E33 verifies five native-image regions and E34 verifies two further regions against the original source bytes and dimensions. The current image audit checks 171 core files without hash failures; six auxiliary source/derivative files make 177 working files. All five E33-pinned hypothesis/review/ranking/feature/validation hashes remain unchanged. The old E20 whole-fragments-file hash is retained for its historical snapshot; it is not weakened to accept the legitimately expanded capture list.

The knowledge CLI builds and validates 159 overlapping lead/question entries, 853 entities, 568 claims and 70 regions, covering all 170 ranking rows, ten hypotheses, 16 dossiers, 13 crosslinks and 13 context checks. JSON-LD export retains reified claims. Successful validation checks evidence traceability and extraction consistency, not historical truth or originality. Ninety-three pair leads have only catalogue/availability triage.

A real local browser check exercised lead filtering, the E33 conflict dossier, the native third-nocturn image region and entity inspection showing competing same-hand/negative same-codex claims. The highlighted source image was visually inspected and a proof saved in `output/research/knowledge-review.png`. Full responsive/accessibility review remains incomplete. Current archive checksum, extracted knowledge validation and unchanged-metric offline replay results are recorded in `output/research/package_verification.json`.

## E35/E36 verification — 27 October 2026

All 49 Python tests and both Node test files pass. New regression checks preserve the weaker generic Alleluia boundary, keep failed registration separate from negative codex assertions, select the actual reviewed capture while leaving side mapping provisional, and reject missing reviews/unregistered passage images. E33's five regions, E34's two regions and E36's seven regions pass source hash/dimension/bounds checks. E35 fixed replay produces the reported six results without changed thresholds or ROIs; both positive controls pass and neither candidate passes. Knowledge v1.1.0 validates 855 entities, 573 claims, 77 regions and 163 overlapping entries while preserving all five frozen files. JSON-LD export has 1,429 reified/entity/payload nodes.

The browser check opened the Aboense Continuity II target and visibly selected Fr 8344 source capture 3, with its endpoint, hash and provisional mapping note. A proof screenshot is retained at `output/research/e36-capture-review.png`. This scoped check does not establish full interface accessibility or validate the reading independently. The working inventory remains 177 source/derivative files and the conservative transfer plan stays 1,215,649,599 bytes. E35/E36 add no downloads. The current review archive and extracted replay outcome are recorded in `output/research/package_verification.json`; no public release occurred.

## E37/E38 verification — 27 October 2026

All 52 Python tests and both Node viewer test files pass. The added regressions distinguish a selected chant ending from whole-office/codex identity, retain separate older/replacement C23 pages, and resolve only the acquired 69r dependency while keeping C435 originals missing. They also preserve `melodic_identity_established=false`: text agreement is not a pitch result.

E37’s four manuscript regions pass source/hash/dimension/bounds checks; strict local verification also checks the two private reading PDFs. E38’s three regions, original TIFF and declared JPEG derivative pass provenance checks, with retained explicit Folio 69r and Public Domain Mark labels. These checks do not independently validate source readings or novelty. All 171 core source files pass the separate integrity audit, and the core fragment/metadata hashes plus five frozen experiment files remain unchanged. Four auxiliary page records now add eight files, for 179 working manuscript files. The conservative transfer plan is 1,665,678,026 bytes including the existing 1 GB reserve.

Knowledge v1.3.0 builds/validates 166 overlapping entries, 117 pair leads, 864 entities, 578 claims and 84 regions; JSON-LD has 1,443 reified/entity/payload nodes. Ninety-three pair leads remain at catalogue/availability triage. A scoped live browser check exercised E37/E38 lead filtering, the revised source dependency, actual manuscript-image loading and exact red region boxes. Proofs are retained at `output/research/e37-region-review.png` and `output/research/e38-region-review.png`. Full accessibility/responsive review and independent reading adjudication remain incomplete.

The local review archive is regenerated after these updates. Its exact file count/hash, extracted knowledge validation and unchanged-metric offline replay outcome are recorded in `output/research/package_verification.json`. Private scholarly PDFs, full extracted text and scholarly page renders remain excluded. No public publication occurred.

## E39 verification — 27 October 2026

All 56 Python tests and both Node viewer test files pass. New checks preserve ambiguous overlapping alternatives and optional-event uncertainty rather than counting them as matches; a graph regression keeps the 12-concordance/2-unresolved excerpt claim unresolved and denies absolute/full melodic identity. Five source regions and 28 manual anchors pass hash/dimension/bounds checks. The strict local checker also verifies the method and Urberg PDF hashes. These checks validate provenance and declared arithmetic, not the source reading independently.

The working manuscript inventory remains 179 files; the guide PDF raises the conservative transfer plan to 1,666,761,179 bytes. The five frozen files and core fragments remain unchanged. Knowledge version1.4.0 contains 167 overlapping entries, 865 entities, 579 claims and 89 regions; JSON-LD has 1,445 nodes. Current package checks are recorded in `output/research/package_verification.json`, including extracted E39 source checks. Private PDFs and reading renders remain excluded.

The E39 scoped live browser check exercised lead filtering, the unresolved comparison record with its prior-art/uncertainty limits, and the target petition region over the retained original image. The red box was visually checked and a proof retained at `output/research/e39-region-review.png`. This does not add an independent music reading or full accessibility review.

## E40 verification — 27 October 2026

All 57 Python tests and both Node viewer test files pass. The new graph regression prevents a source-defined word-boundary fit from becoming a physical join, verified edge, accepted signature succession or independently confirmed attribution. E40’s offline checker verifies five source regions, declared-string consistency, the unchanged five frozen files/core fragments and the recorded zero-body HTTP403 outcome without repeating any access. These checks do not independently validate paleography, the Finnish description or novelty.

The version1.5.0 overlay builds and validates 168 entries, 117 pair leads, 867 entities, 580 claims and 94 regions; JSON-LD has 1,448 nodes. The live browser check exercised the unresolved E40 lead, its missing-original/numbering/surface limits, and the actual terminal-row red box. The retained proof is `output/research/e40-region-review.png`. Full accessibility and source adjudication remain incomplete.

Working source files remain 179; the conservative transfer plan remains 1,666,761,179 bytes, including the reserve. The regenerated local archive’s exact count/hash and extracted source/knowledge/offline replay checks are recorded in `output/research/package_verification.json`. No publication occurred.

## E41 verification — 28 October 2026

All 57 Python tests and both Node viewer test files pass. The E41 checker accounts for all 50 candidate and 13 selected control correspondences, verifies source hashes/dimensions/coordinates/crop bounds, preserves original inlier flags and all E35/core/frozen inputs, and checks the declared inference limits. It does not independently validate the manual source-context judgments. Repeated orientations remain disclosed rather than counted as independent confirmations.

Knowledge version1.5.1 builds and validates 168 entries, 867 entities, 580 claims and 94 regions; JSON-LD still has 1,448 nodes. E41 augments the existing E35 lead and two unresolved imaging claims without adding a new lead or historical relationship. The live browser check displayed the updated supporting observations, unresolved state, scope and next test; `output/research/e41-context-audit.png` retains the visible proof. This is a scoped rendering check, not a full accessibility audit or independent manuscript review.

The manuscript inventory and transfer plan remain unchanged. The local review archive includes the four PDM raw-patch sheets and the reproducible selection/record/check scripts. Its exact file count/hash and extracted source/knowledge/offline replay results are recorded in `output/research/package_verification.json`. Private scholarly PDFs and page renders remain excluded. No public publication occurred.

## E42 verification — completed 29 October 2026

The source audit began28 October. All58 Python tests and both Node viewer test files pass. The new graph regression preserves the unresolved N[o?] split versus the narrowly supported phrase fit, while denying physical adjacency/join, complete surface mapping, accepted photographic overlap, new attribution, novelty clearance and independent confirmation for both claims. The offline checker verifies four source hashes/dimensions, four new region locators, two existing reused regions, all four declared pairings and the identical11-row sums. These checks do not independently certify the manual counts or literal readings.

Knowledge version1.6.0 builds/validates168 entries,868 entities,582 claims and98 regions; JSON-LD contains1,451 nodes. The live browser check displayed the revised E34 lead, its wrong-grouping/row-count limit and remaining mapping dependency, then the actual new upper-row Christum-eius region with a correctly placed red box. The retained proof is `output/research/e42-boundary-region.png`. This is a scoped rendering/provenance check, not full accessibility testing or independent source review.

The local review archive explicitly includes the two PDM E42 figures and source/record/check data, with an extracted E42 source check added to the existing knowledge/source/offline replay verification. Its exact final count/hash and replay outcomes are in `output/research/package_verification.json`. The manuscript inventory, conservative transfer plan, core/frozen/E35 inputs and private-PDF exclusions remain unchanged. No publication or external contact occurred.

## E43 verification — 29 October 2026

All60 Python tests and both Node viewer test files pass. New regressions keep the43 repaired published-control leads separate from unresolved computational claims, require twelve exact canvas-linked source assertions, and preserve the published H06 rejection and unresolved Codex1146 pairs. The source checker accounts for all168 lead identifiers and117 pair identifiers against the preserved baseline, verifies twelve working-image hashes and parent-manifest service locators, and reconciles43 repaired credits plus50 remaining metadata-only pairs with the baseline93. It does not independently validate the reconstruction's historical assignments or any new pair-level image reading.

Knowledge version1.7.0 builds/validates168 entries,870 entities,594 claims and98 regions; JSON-LD contains1,465 nodes with identity closure disabled. Frozen/core inputs remain unchanged. Source-defined control credit changes overlapping lead-state totals without producing new scientific findings or completing the goal. The archive verifier now includes extracted E43 source/accounting checks alongside the existing source/knowledge/offline replay checks. Its exact final count/hash and replay outcomes are in `output/research/package_verification.json`. Private source exclusions,179 manuscript files and the conservative transfer plan remain unchanged; no public publication occurred.

## E44 verification — 29 October 2026

All61 Python tests and both Node viewer test files pass. The E44 source checker verifies nine exact manifest painting URLs, PDM rights, original/receipt hashes and dimensions, eleven region bounds, the preserved v1 versus reference-assisted v2 revision, and unchanged core/frozen/E35 inputs. It checks the declared inference limits, not the correctness of the paleographic reading, musical rule functions, service mapping, a catalogue correction or novelty.

Knowledge version1.8.0 builds/validates168 entries/117 pairs,887 entities,595 claims and109 regions. JSON-LD contains1,483 nodes with identity closure disabled. The8066/9620 pair stays unresolved;49 pairs remain metadata-only. No new object or automatic side assignment is created. Existing source assertions and the published8201/8304 rejection remain separate from computational suggestions.

A scoped live browser check verified the exact pair's unresolved detail, revised rubric text, new original-image link and correctly placed red box on the actual photograph. Proofs: `output/research/e44-rubric-region.png` and `output/research/e44-source-box.png`; exact scope/hashes are in `research/continuation_44/viewer_review.json`. Full responsive/accessibility testing and independent source adjudication remain incomplete.

Working source files188; conservative transfer plan1,669,530,774bytes including the existing reserve. The local archive verifier includes extracted E44 provenance/revision checks alongside E37–E43, knowledge validation and offline replay of the frozen metrics. Exact final archive count/hash and replay outcomes are in `output/research/package_verification.json`. Private scholarly PDFs remain excluded. No publication occurred.

## E45 verification — 29 October 2026

All61 Python tests and both Node viewer files pass. The expanded Ant49 regression keeps the source-map follow-up separate from a complete duplicate, distinctive variant or different-codex claim. The E45 checker verifies all nine fixed source hashes/dimensions, complete retained-capture coverage, eight region selectors and frozen/core/E35 hashes. It verifies the private paper hash when present; `--require-private` requires that local reading copy. The shareable archive explicitly reports its intentional absence. These checks do not independently validate readings, full liturgical positions, musical identity, manuscript attribution or novelty.

Knowledge version1.9.0 builds/validates168 entries/117 pairs,888 entities,595 claims and117 regions; JSON-LD has1,484 nodes with identity closure disabled. The existing unresolved E44 claim is enriched without creating a new candidate or historical attribution. Forty-nine pair leads remain metadata-only. Eight source-region crops and both PDM-only figures were visually inspected; complete relevant Grajewski pages included the footnote/table. No new E45 live-browser rendering or full accessibility review is claimed.

No acquisition:188 working source files and the1,669,530,774-byte conservative transfer plan remain unchanged. E45 private paper-page renders are excluded, while its two manuscript-only figures are explicitly allowlisted. The archive verifier includes extracted E45 coverage/provenance checks, E37–E44 checks, knowledge validation and offline replay. Exact current archive count/hash and final replay outcomes are in `output/research/package_verification.json`. Frozen metrics and case-screen results remain unchanged; no publication occurred.

## E46 verification — 29 October 2026

All62 Python tests and both Node viewer files pass. The new regression keeps the two different external Chant concepts and their local identification claims qualified, and prevents a visible head-group difference from becoming a same-work variant or different-book assertion. An initial test run correctly rejected a stale generated snapshot after a report edit; rebuilding the knowledge inputs restored full validation without weakening the provenance check or changing source readings.

The E46 checker verifies both source images,15 primary candidate centres, one retained optional sign, six annotation bounds, unchanged v1/v2 source points, comparison arithmetic and all frozen/core/E35 hashes. The existing private Cantus-guide hash is checked when present; `--require-private` requires it locally, while the archive explicitly reports its absence. These checks do not independently adjudicate noteheads, clefs, work IDs, service positions, historical identity or novelty. The wider direction sensitivity remains unresolved, and exact interval transcription is incomplete.

Knowledge version1.10.0 builds/validates168 entries/117 pairs,891 entities,598 claims and123 regions. JSON-LD has1,490 nodes with identity closure disabled. Candidate chant identifications remain unresolved and the same-codex pair is not promoted. Forty-nine pairs remain metadata-only. Both manuscript-only E46 figures were visually inspected; no new live-browser rendering or full accessibility review is claimed.

No retained-file acquisition:188 working source files and the1,669,530,774-byte conservative transfer plan are unchanged. Web-reader traffic remains unmeasured within the planning reserve. The package explicitly includes the two PDM-only E46 figures and excludes private method papers/renders. Its extracted E46/E37–E45 source checks, knowledge validation and offline replay are recorded with the exact current archive count/hash in `output/research/package_verification.json`. Frozen metrics and case-screen results remain unchanged; no publication occurred.

## E47 verification — 29 October 2026

All62 Python tests and both Node viewer test files pass. Knowledge version1.11.0 builds/validates168 entries/117 pairs,893 entities,605 claims and123 regions. JSON-LD has1,499 nodes with identity closure disabled. No new live-browser rendering or image-inspection claim is made for this dataset-only update.

The E47 standard-library ZIP/XML checker independently resolves the two workbook sheets by name and checks38 unit rows, exact headers/cell addresses, literal values and all six target identifier matches across each source worksheet. It rejects formulas in the inspected columns and verifies all13 changed register states, the unchanged remaining decision states,36 metadata-only pairs, seven attributable reconstruction claims and frozen/core/E35 hashes. It does not independently adjudicate historical identity, adjacency, physical conjugacy or novelty. The openpyxl extraction is read-only, with workbook source checksums pinned before and after.

The E43 source checker still passes, preserving its43 Beauvais source-credit repairs and historical50-pair remainder while permitting the current subset of36. The published different-book control and frozen2E/7C/1D classifications remain unchanged. Resource accounting remains188 working source files and the1,669,530,774-byte conservative plan. No network acquisition occurred in E47.

The review package includes the already allowlisted CC BY4.0 workbooks, E47 protocol/baseline/extraction/checker and exact source-row results. Private scholarly reading files/renders remain excluded. Extracted E37–E47 source checks, knowledge validation, full offline replay and exact archive size/checksum are recorded in `output/research/package_verification.json`; frozen metrics and case-screen outputs must remain unchanged. No publication occurred.

## E48 verification — 30 October 2026

All62 Python tests and both Node viewer test files pass. Knowledge version1.12.0 builds/validates168 entries/117 pairs,898 entities,629 claims and123 regions. JSON-LD has1,528 nodes with identity closure disabled. No new manuscript-image reading or live-browser rendering is claimed. The read-only source extraction was rerun with bundled Python/openpyxl3.1.5 before the final build.

The E48 independent standard-library ZIP/XML checker verifies46 exact target rows and191 source-unit rows, header/cell values, all36 selected leads, exactly five changed decision states and31 explicitly pending primary pair tests. It preserves13 unresolved contested-unit pairs,23 literal source-assignment claims, the separately qualified project interpretation of their unit semantics and the published8201/8304 rejection. It checks Fr20106's retained KB A103 metadata and absent viewer/manifest fields, plus all frozen/core/E35 hashes. Optional retained reading-file hashes are checked locally; their absence from the review archive is reported rather than treated as missing manuscript evidence. These are extraction/provenance checks, not independent historical adjudication or novelty clearance.

E47's exact after-register is pinned in the E48 protocol. Its checker retains the full historical13-state transition/36-pair remainder assertions against that snapshot and verifies that the13 repairs persist in the live data. Later source work therefore does not require weakening the historical transition check or falsely freezing the live population. The existing E43 checks and published negative control remain preserved.

The local package includes the already allowlisted source workbooks, E48 scripts/protocol/results/source metadata and the E47 historical snapshot. It excludes reading PDFs and private page renders. Extracted E37–E48 source checks, knowledge validation and full offline replay are recorded with the exact archive size/hash in `output/research/package_verification.json`; scientific metrics and frozen case-screen output must remain unchanged. No publication, outreach or file acquisition occurred. Web-reader/search traffic remains unmeasured within the existing planning reserve.

## E49 verification — 30 October 2026

All62 Python tests and both Node viewer test files pass. Knowledge version1.13.0 builds/validates168 entries/117 pairs,901 entities,629 claims and127 source regions. JSON-LD has1,531 nodes with identity closure disabled. No claim count, historical decision or frozen result changes. The new catalogue candidate is a CatalogRecord with unknown physical object and unresolved crosswalk; it does not expand the physical corpus.

All eight retained source photographs and the four-region PDM-only review figure were visually inspected. The checker verifies image hashes/dimensions, annotation bounds and literal/normalized reading agreement, exact20106 source-record fields, preserved31 pending primary pair tests, the unmerged record and all frozen/core/E35 hashes. It explicitly rejects a completed two-opening replication, independently verified20106 continuity, a refutation of the published rejection or a new historical exclusion. The optional private reference hash is checked locally and its absence is reported in extracted copies. These checks preserve source integrity and inferential scope; they do not independently adjudicate readings or novelty. No new live-browser UI verification is claimed.

The package explicitly allowlists only the E49 manuscript-pixel review figure in addition to the existing assets; it contains no new catalogue screenshot or copyrighted paper page. Private reading references/renders remain excluded. Exact archive size/hash, extracted E37–E49 source checks, knowledge validation and full offline replay are recorded in `output/research/package_verification.json`. Scientific metrics and frozen case-screen outputs must remain unchanged. No acquisition, outreach or publication occurred; web-reader/search traffic remains unmeasured within the existing planning reserve.

## E50 verification — 30 October 2026

All62 Python tests and both Node viewer test files pass. Knowledge version1.14.0 builds/validates168 entries/117 pairs,915 entities,630 claims and135 regions; JSON-LD has1,546 nodes with identity closure disabled. All historical decision states and frozen2E/7C/1D cases remain unchanged. The negative stylistic-similarity observation is scoped to visible copying-field layout, with historical same-codex identity unresolved.

The E50 primary comparison is explicitly marked partly executed: `primary_pair_test_completed` and `all_planned_target_views_inspected` remain false. The pending-count transition records the first direct comparison, not completion of the original full-view plan. Seven target photo views, two retained control views, the coordinate review and the PDM-only layout figure were visually inspected. The checker verifies six successful source files against hashes/dimensions and exact manifest pointers, two recorded un-retried failures, eight region bounds, approximate ruler arithmetic/all sensitivities, resource accounting and exactly one primary-test transition. The widest combined endpoint/scale assumptions overlap; original leaf/fold mapping, unconditional layout exclusion, historical book exclusion, catalogue correction, improved recognition and novelty remain unestablished. A timed-out request may have unmeasured traffic despite no saved body.

The exact post-E49/pre-E50 register is pinned in the primary protocol. E48/E49 source checks retain strict historical31-pending assertions against it and report the current subset; their checks pass. E50 separately verifies that exactly the selected actually inspected pair accounts for the change to30 pending tests. No old state-transition assertion was discarded. Source integrity tests are not independent historical or reading adjudication. No new live-browser UI review is claimed.

Resource audit:194 working source files,1,542,176 confirmed new successful bytes, and a1,671,072,950-byte conservative transfer plan including the existing1GB reserve. Six added source files link to existing objects/canvases. The package explicitly includes them and the layout figure, with recorded PDM Rights-metadata scope, and excludes the ancillary coordinate review and private reading copies/renders. Exact archive size/hash, extracted E37–E50 source checks, knowledge validation and full offline replay are recorded in `output/research/package_verification.json`; frozen metrics and case-screen output must remain unchanged. No outreach, upload or public release occurred.

## E51 verification — 30 October 2026

All62 Python tests and both Node viewer test files pass. Knowledge version1.15.0 validates168 entries/117 pairs,923 entities,631 claims and139 regions; JSON-LD has1,555 nodes with identity closure disabled. All historical decision states, frozen input hashes and2E/7C/1D cases remain unchanged. No fresh live-browser UI validation is claimed.

E51 checks three retained API responses against byte lengths/hashes, follows only exact returned latest-version links, verifies version/concept/latest relations, and compares all five retained-file MD5/size receipts to current publisher metadata. Both workbooks must be present and byte-verified in an extracted copy. Private reading PDFs are checked when present; their absence is explicitly reported in the archive. New CSV bytes remain untested. This establishes checked release/file identity, not historical correctness or novelty.

All six target source photographs, two retained8994 control crops and the new PDM-only mark figure were visually inspected. The source checker verifies source hashes/dimensions, exact region bounds, four reused prior mark regions, later-reference/catalogue correspondence and explicit uncertainty. The completed fixed address audit is separate from unresolved original side mapping and historical same-codex adjudication. Only the later20274 reference-description claim is newly supported; no original folio, shared/conflicting address or20106 crosswalk is accepted.

The pre-E51 register is pinned in its primary protocol. E50's strict historical31→30 transition uses that exact snapshot and checks the live pending subset/partial-test limits. E51 independently checks30→29, exactly the selected actually inspected pair, with every historical decision unchanged. These are state/provenance checks, not independent image adjudication.

Resources remain194 source files. Three metadata responses add31,373 logged bytes, producing a1,671,104,323-byte conservative plan including the existing1GB reserve; exact lifetime traffic remains unverified. The package explicitly allowlists the new manuscript-pixel figure, includes both retained workbooks and metadata receipts, and excludes private reading copies/renders. Extracted E37–E51 source checks, knowledge validation, full offline replay and exact archive size/hash are recorded in `output/research/package_verification.json`; scientific metrics and frozen case-screen output must remain unchanged. No outreach, upload or public release occurred.

## E52 verification — 30 October 2026

All62 Python tests and both Node viewer test files pass. Knowledge version1.16.0 validates168 entries/117 pairs,939 entities,636 claims and146 regions. The JSON-LD export has1,576 nodes with identity closure disabled. Historical decision totals, frozen input hashes, scientific metrics and2E/7C/1D cases remain unchanged. No fresh live-browser UI validation is claimed.

The E52 checker verifies eight unique predeclared requests, six saved JPEG hashes/dimensions/exact manifest painting pointers, two recorded un-retried timeouts, PDM Rights metadata,24 distinct inspected-photo records, seven new region bounds and six reused E44 rule regions. Source photo coverage remains partial:8072 capture3 is unseen, and8073 capture1 uses its retained800px thumbnail after a native timeout. The protocol and result retain incomplete group-test/full-collation/historical-adjudication flags.

The full13-row matrix covers exactly the predeclared pending Ant49 edges; the two previously studied edges remain separate controls. The pinned pre-E52 register supports an exact29→16 first-comparison transition, with every historical decision unchanged. Those13 flags represent limited direct context/layout comparisons, not13 completed historical tests. E50/E51 retain strict historical transitions through pinned snapshots and check the live pending subset; their source checks pass.

Literal reading version1 is preserved before reference lookup. Three local work identifications remain unresolved candidates, and the two supported observations describe repeated-incipit context and mixed verse/antiphon blocks. No exact pitch intervals, transferred external melody/position, whole-book genre, secure join/address, historical exclusion or novelty is accepted. Five-rule appearance is already shared by the known wrong pair. Source/contract checks are not independent reading adjudication.

Six source files add1,896,527 confirmed saved bytes, bringing the working inventory to200 and the conservative transfer plan to1,673,000,850bytes, including the existing1GB reserve. Timeout/web-reader traffic can be unmeasured. The package explicitly includes the permitted new photographs and visually inspected source-pixel figure, preserves the request ledger and excludes scratch crops/private reading sources. Extracted E37–E52 source checks, knowledge validation, full offline replay and exact archive size/hash are recorded in `output/research/package_verification.json`; frozen metrics/case-screen output must remain unchanged. No outreach, upload, external edit or publication occurred.

## E53 verification — 30 October 2026

All62 Python tests and both Node viewer test files pass. An initial Python run after report edits correctly rejected a stale PROJECT_STATE input snapshot; rebuilding the evidence index corrected the stale hashes, and the full62-test rerun passed. No validator or scientific gate was weakened. Knowledge version1.17.0 validates168 entries/117 pairs,943 entities,638 claims and155 regions; JSON-LD has1,582 nodes with identity closure disabled. All historical decision states, frozen hashes and2E/7C/1D outcomes are unchanged.

The E53 checker verifies hashes/dimensions/rights for15 retained photo views, nine new source-region bounds and attribution, four reused E50 layout regions, unchanged pre-lookup literal candidates and a complete matrix of eight selected existing edges. Five sampled field-count differences challenge an unchanged uniform template only. Seven objects have just one selected view; full source-photo, original-side and diplomatic/music coverage are not claimed. Scratch180-degree displays do not modify originals or annotation coordinates.

Two hymn identifications remain unresolved local candidates. Indexed external witnesses support a probable work mismatch and demonstrate that Tu-fabricator is already documented elsewhere; no index omission becomes a novelty claim. No external reference image, melody or service position is transferred. Source-integrity checks are not independent paleographic or historical adjudication.

The pinned pre-E53 register preserves E52's strict29→16 transition; E53 separately verifies exactly eight first-comparison changes,16→8, with every historical decision unchanged. These flags count limited first source comparisons, not completed book tests. No fresh live-browser UI validation is claimed.

No source file was acquired. The inventory remains200 and the conservative transfer plan remains1,673,000,850bytes, including the existing1GB reserve. Web-reader/search traffic is unmeasured. The package includes the new visually inspected PDM-only hymn figure and attributed source annotations; scratch rotations/candidate crops/private reading copies remain excluded. Extracted E37–E53 source checks, knowledge validation, full offline replay and exact archive size/hash are recorded in `output/research/package_verification.json`; scientific metrics and frozen case-screen output must remain unchanged. No outreach, upload, external edit or publication occurred.

## E54 validation scope —31October2026

E54 preserves the frozen core/review hashes and tests exact manifest URLs, eight successful source receipts,27-view selected coverage, twelve source regions, unchanged lead decisions and the eight-to-zero initial-comparison transition. Historical E53 transitions remain pinned to the pre-E54 register rather than checked against a later live count. Zero first-pending flags does not establish completed historical tests.

All62 Python tests, both Node viewer test files, E54 source checks and knowledge validation passed. The final tracked-document build is repeated after this report update; knowledge export and extracted archive source/replay results are recorded in `output/research/package_verification.json` and its terminal logs. A source integrity check cannot independently certify an AI transcription. No new statistical recognition claim is tested.

## E55 validation scope —31October2026

The source checker recomputes local geometry and the PDM proof in scratch space, verifies all28 unchanged E39 anchors, keeps both3/4 target alternatives, records four failed complete-rule models and checks the all168-entry inventory. Two spem controls widen under the same sensitivity. No pitch accuracy, melodic variant, recognition gain or codex truth is validated. Full suite and archive terminal results are recorded under `output/research/`.

E55 terminal verification: all62 Python tests, both Node viewer test files, deterministic source recomputation and knowledge validation passed. Frozen inputs remain unchanged. The subsequent final tracked-document build/export and extracted archive replay are identified by `output/research/package_verification.json`; no independent transcription or historical truth is claimed by these checks.

## E56 verification scope

The E56 checker verifies the retained TEI hash, two no-retry TIFF failures, unchanged historical lead states and resource totals. It checks what the retained TEI says, not physical sewing holes or the correctness of its shelfmark. Final archive checks are recorded in output/research/package_verification.json.
# E57 validation scope — 1 November 2026

The E57 source checker verifies frozen-input and image hashes, annotation bounds, unchanged lead decisions and qualified result fields. It cannot establish that the unblinded text readings are correct, that the photographed sides are consecutive, or that the published comparison was independently transcribed. No predictive scores were adjusted. Extracted archive checks and replay are recorded in `output/research/package_verification.json`. [E57](RESEARCH_CONTINUATION_57.md).

# E58 validation scope — 1 November 2026

The new checker verifies retained-image hashes, crop bounds, unchanged lead decisions and explicit non-identity fields. It does not independently verify the text readings, image continuity, external indexes, or historical identity. Extracted archive checks and offline replay are recorded in `output/research/package_verification.json`. [E58](RESEARCH_CONTINUATION_58.md).

# E59 validation scope — 1 November 2026

The source checker verifies recorded source metadata, frozen hashes and unchanged historical decisions. It does not certify the AI-assisted Finnish interpretation, review the published image, or validate the authors' historical conclusions. Archive and replay results are in `output/research/package_verification.json`. [E59](RESEARCH_CONTINUATION_59.md).

# E60 validation scope — 1 November 2026

The E60 checker verifies retained-source hashes, region bounds, frozen inputs, unchanged decisions and explicit unresolved fields. It does not certify the text reading, Finnish catalogue transcription, unique address or historical exclusion. Extracted archive checks and replay are in `output/research/package_verification.json`. [E60](RESEARCH_CONTINUATION_60.md).

# E61 validation scope — 1 November 2026

The E61 source checker verifies the selected local image hash, region bounds, frozen inputs and unchanged historical decisions. It cannot certify a reading, the indexed witness, surface order or book identity. Archive checks and replay are recorded in `output/research/package_verification.json`. [E61](RESEARCH_CONTINUATION_61.md).

