# The Lost Library

A local research prototype for comparing medieval music-manuscript fragments. **No new manuscript attribution is confirmed.** The project includes a reproducible exploratory benchmark, a documented reconstruction demonstration, a frozen ten-comparison review queue and exact image-region evidence.

Start with the [research paper](RESEARCH_PAPER.md) and [research guide](RESEARCH_GUIDE.md), followed by [PROJECT_STATE.md](PROJECT_STATE.md), [FINAL_REPORT.md](FINAL_REPORT.md), [VALIDATION_REPORT.md](VALIDATION_REPORT.md), [EVIDENCE_DOSSIERS.md](EVIDENCE_DOSSIERS.md) and [REVIEWER_PACKET.md](REVIEWER_PACKET.md). Earlier source passes are in [INDEPENDENT_RESEARCH_PASS.md](INDEPENDENT_RESEARCH_PASS.md) and the linked continuation reports. The [research goal](RESEARCH_GOAL.md) preserves the original ambition; missing sources and independent review remain explicit limitations of the bounded study.

## Run locally

Tested on Python3.12, macOS arm64. Use an existing compatible Python installation:

```sh
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m lost_library run --offline
.venv/bin/python -m lost_library serve --port 8765
```

Open `http://127.0.0.1:8765/viewer/`. The server binds loopback only. Stop with Ctrl-C. Windows uses `.venv\Scripts\python.exe` instead. The viewer itself is buildless HTML/CSS/JavaScript; Node is required only for its automated checks. The port can be changed if occupied.

Dependency installation needs network access. `--offline` prevents archive fetching during ingestion; it does not make pip installation offline. With the supplied images/features, the replay uses cached feature arrays and needs no new model download. Recomputing frozen visual features requires the official ResNet18 weight file at `data/models/checkpoints/resnet18-f37072fd.pth`; the feature extractor obtains it from PyTorch when necessary. Its hash is recorded in `data/features.json`. There are no paid API, cloud or authentication dependencies.

## Reproduce individual steps

```sh
.venv/bin/python -m lost_library ingest --offline
.venv/bin/python -m lost_library features
.venv/bin/python -m lost_library evaluate
.venv/bin/python -m lost_library match
.venv/bin/python -m lost_library reconstruct
.venv/bin/python -m lost_library evidence
.venv/bin/python -m lost_library export
.venv/bin/python research/evidence_audit.py
.venv/bin/python research/audit_resources.py
.venv/bin/python research/write_research_reports.py
.venv/bin/python -m lost_library search Åbo --limit 5
.venv/bin/python -m unittest discover -s tests -v
node --test tests/viewer.test.cjs
```

Run from the project root. `run --offline` combines ingestion, cached features, evaluation, matching, reconstruction, evidence export and viewer export. It preserves validated alternate captures. Provenance timestamps may change serialized hashes; scientific metrics and source-image bytes should remain unchanged. The original pilot snapshot is under `data/experiments/v1-initial/`. The frozen review queue and its reviews must remain paired; changing it requires a new version, not overwriting the selection.

Network retrieval without `--offline`, `research/fetch_evidence_captures.py` and `research/fetch_scholarly_sources.py` are explicit bounded acquisition steps, not needed to browse or reproduce cached results. Do not rerun failed requests as an access workaround. Source ordinals never imply folio sides.

## Research data

- `research/mpo.csv`: original versioned CC0 metadata, with version and checksum receipts.
- `data/fragments.json` / SQLite: original metadata, normalized fields, rights and provenance.
- `data/images/`: 167 core JPEGs representing 120 imaged physical objects. Three auxiliary comparison pages add six files: two C23 TIFF/JPEG pairs and two Fr 7292 resolution variants of a single IIIF canvas, making 173 working source files overall.
- `data/features.*`, `validation.json`, `matches.json`: frozen-model/layout features, measured evaluation and170ranked suggestions.
- `data/hypotheses.v1.json`: immutable ten-comparison selection.
- `data/hypothesis_reviews.v1.json`, `observations.v9.json`, `review_bundle.json`: local screening, 63 source-linked pixel annotations and complete export. Earlier observation versions are retained. `text_collation.v2.json` separates the visible target from edited texts and reported witness states.
- `data/context_checks.v11.json`: thirteen supporting family/source checks kept outside the ten frozen hypotheses; CTX07 and CTX09 record BOMPAC prior-art checks, CTX10 records Walta 2013, CTX11 the earlier Fragmenta labels and CTX12 the detailed catalogue wording and foliation lead, and CTX13 the source-linked Fr 8994 mark plus the common-signature caveat.
- `research/independent_pass/`: E19 method, crosswalk, conditional-constraint, ruling and textual tests.
- `research/continuation_20/`: intrinsic Fr 10370 order, letter-controlled ornament, Helsinki access/boundary assertions and ten-site actual C23 collation.
- `research/continuation_21/` and `research/continuation_22/`: ruler-calibrated layout measurements, one metadata-matched different-codex control, current BOMPAC/CODICUM prior-art review, source hashes and limits. The control shows staff pitch alone is not distinctive.
- `research/continuation_30/`: read-only, checksum-verified query of published BOMPAC assignments for model suggestions H08–H10; no image or queue change.
- `research/continuation_31/` and `research/continuation_32/`: official Fragmenta relationship labels, an unverified `k`/IV lead, one region-linked Fr 8994 mark, and access outcomes; no queue change.
- `data/comparison_sources.v1.json`: two C23 pages and one auxiliary Fr 7292 page with image hashes and rights; excluded from core predictors, labels and frozen queue.
- `data/evidence_experiment.json`: source-based decisions/abstentions, not a blind improved classifier.
- `research/scholarship/receipts.json`: public scholarly-source receipts. PDFs are retained privately for reading and excluded from the release package.

See [DATA_RIGHTS.md](DATA_RIGHTS.md) and [THIRD_PARTY.md](THIRD_PARTY.md) before redistribution. Project code licensing has not been selected by the owner; no blanket licence over third-party images or scholarship is asserted. Public GitHub publication, external contact and public hosting have not occurred.

## Reproduce the independent source pass

```sh
.venv/bin/python research/independent_pass/methods/method_checks.py
.venv/bin/python research/independent_pass/crosswalk/audit_crosswalk.py
.venv/bin/python research/independent_pass/crosswalk/check_source_constraints.py
.venv/bin/python research/independent_pass/visual/measure_ruling.py
.venv/bin/python research/independent_pass/text/collate_target.py
.venv/bin/python research/independent_pass/integrate.py
.venv/bin/python -m lost_library evidence
.venv/bin/python -m lost_library export
```

These checks use cached sources. Their selected passages and measurements were inspected after the original benchmark; they are descriptive source tests, not a new blind validation. Fr 10370 remains contextual evidence rather than an additional frozen relationship. A possible scaling-formula erratum is distinct from a new historical attribution.

## Reproduce E20 source checks

```sh
.venv/bin/python research/continuation_20/intrinsic_10370/check_order.py
.venv/bin/python research/continuation_20/ornament/analyze.py
.venv/bin/python research/continuation_20/integrate_registration.py
```

The ten-site textual comparison is retained in `research/continuation_20/c23/collation.json`, with exact source regions and editorial-versus-direct-reading limits. The cached registration result is inspectable in `registration/feature_results.json`; rerunning its optional OpenCV script requires independently installing the exact public wheel recorded in `registration/dependency_receipt.json`. It tested only declared boundary regions and did not establish a capture join. The C23 acquisition scripts are not required to inspect the cached results. No capture ordinal alone is treated as a medieval side; no current corrected reading is silently treated as an original witness state. These are selected descriptive source checks, not a new blind recognition benchmark.

## Reproduce E21 layout measurements

```sh
.venv/bin/python research/continuation_21/ruling_pitch_check.py
.venv/bin/python research/continuation_21/integrate.py
.venv/bin/python -m lost_library evidence
.venv/bin/python -m lost_library export
```

The E21 report records manual ruler and staff-line coordinates, source hashes, uncertainty, full-catalogue counts and non-random metadata limits. Image regions were selected after inspection; this does not validate layout as an identity classifier.

## Reproduce E22 control and prior-art audit

```sh
.venv/bin/python research/continuation_22/matched_staff_control.py
.venv/bin/python research/continuation_22/integrate.py  # only when starting from the pre-E22 data snapshot
.venv/bin/python -m lost_library evidence
.venv/bin/python -m lost_library export
.venv/bin/python research/continuation_20/checks.py
.venv/bin/python research/audit_resources.py
```

The Fr 7292 image is one different-codex control, not an independent attribution label or a representative sample. Its result only tests whether this particular staff pitch is unique; it does not establish a shared hand or book.

## Reproduce E24 H03 catalogue-layout check

```sh
.venv/bin/python research/continuation_24/h03_layout_screen.py
.venv/bin/python research/continuation_24/integrate_context.py
.venv/bin/python -m lost_library evidence
.venv/bin/python -m lost_library export
```

The check verifies the pinned MPO CSV hash and compares the candidate pair's catalogue written-area values with a same-notation, same-staff-count, same-row-count subset, then with the Antiphonarium subset. It includes Fr 20274's literal `11 (33)` row value. The pair-defined size box is post hoc, the dimensioned records are incomplete, and the catalogue carries the prior grouping; use the result only as layout-compatibility context, not as a prevalence estimate or physical identity test. The integration script rebuilds CTX08 from the immutable v5 context snapshot and leaves the frozen hypothesis queue untouched.

## Reproduce E26 BOMPAC target crosswalk

```sh
python research/continuation_26/bompac/target_crosswalk.py
python research/continuation_26/bompac/integrate_context.py
python -m lost_library evidence
python -m lost_library export
```

This read-only query verifies five published Zenodo MD5 checksums and reports the BOMPAC combined and raw MPO unit assignments. It refreshes CTX07 in the viewer but does not alter the frozen queue, predictors or manuscript images. See [E26](RESEARCH_CONTINUATION_26.md) for the interpretation and limitations.

## Reproduce E27 related-unit crosswalk

```sh
.venv/bin/python research/continuation_27/related_unit_crosswalk.py
.venv/bin/python research/continuation_27/integrate_context.py
.venv/bin/python -m lost_library evidence
.venv/bin/python -m lost_library export
```

The read-only query verifies the published checksums for the combined and raw BOMPAC workbooks, then records the included rows for BOMPAC-9531, BOMPAC-912 and BOMPAC-5324. Integration adds CTX09 and updates H03–H05's prior-art context without changing the frozen queue, predictors or manuscript images. See [E27](RESEARCH_CONTINUATION_27.md) for the source distinction and limitations.

## Reproduce E28 prior-art context

```sh
.venv/bin/python research/continuation_28/integrate_context.py
.venv/bin/python -m lost_library evidence
.venv/bin/python -m lost_library export
```

E28 records Walta 2013's indexed discussion of a broad Naantali-related group that includes IV.156, IV.157 and IV.173, while noting several hands and uncertainty about the production site. E29/E31 check the official Fragmenta records: they separate stylistic resemblance and suggested Codex 1505 links from specific same-codex labels. The IV.157 catalogue's `k`/IV opening-signature notation may align with Fr 8994's recorded foliation, but both source images have not been compared. These source categories and the signature lead establish no new attribution. Full Taitto/Keskiaho passages remain to be read. See [E28](RESEARCH_CONTINUATION_28.md), [E29](RESEARCH_CONTINUATION_29.md), [E31](RESEARCH_CONTINUATION_31.md) and the [prior-art ledger](research/PRIOR_ART_LEDGER.md).

## Reproduce E29 catalogue context

```sh
.venv/bin/python research/continuation_29/integrate_context.py
.venv/bin/python -m lost_library evidence
.venv/bin/python -m lost_library export
```

CTX11 records the catalogue labels without adding images, observations or a hypothesis. The queue hash and classifications remain unchanged.

## Reproduce E30 H08–H10 BOMPAC crosswalk

```sh
./.venv/bin/python research/continuation_30/bompac_suggestion_crosswalk.py
./.venv/bin/python research/continuation_30/integrate.py
./.venv/bin/python -m lost_library evidence
./.venv/bin/python -m lost_library export
```

The query verifies the published MD5 values for the already downloaded combined and raw MPO workbooks. It records that BOMPAC groups Fr 4223/8311/8455 together and assigns Fr 1385 elsewhere. These are related published reconstruction datasets, not fresh image analysis or independent adjudication; the cases remain unresolved. See [E30](RESEARCH_CONTINUATION_30.md).

## Reproduce E32 catalogue and image context

```sh
./.venv/bin/python research/continuation_32/integrate.py
./.venv/bin/python -m lost_library evidence
./.venv/bin/python -m lost_library export
```

CTX12 records official relationship labels and the foliation lead. CTX13 links the visible Fr 8994 mark to its pixels and records that the signature convention is common; H03 remains C.

## What AI does

It ranks compatibility and proposes inspectable readings and observations. Each reviewed region identifies a source image, exact pixels and SHA-256. Literal candidate readings, normalized search terms and database identities are separate. These observations are provisional and have no independent expert endorsement. A common chant, same scribe or high score is not proof of one codex. No reconstructed notes or audio are fabricated.

The existing amended goal is active; no replacement scientific objective was needed. Relevant unread scholarship limits novelty claims for particular questions; provisional source work can continue without waiting for expert contact. Independent confirmation requires actual competent independent scrutiny. See [OPEN_QUESTIONS.md](OPEN_QUESTIONS.md) for the next tests.

## Current E33/E34 research and knowledge overlay

The [complete lead audit](RESEARCH_CONTINUATION_34.md) and [knowledge model](MANUSCRIPT_KNOWLEDGE.md) implement the 25 October amendment to the existing goal. All 170 ranking rows are retained, with 117 pair leads and 159 overlapping lead/question entries; 93 pairs still have catalogue/availability triage only. No discovery or independent confirmation is claimed. E33's Fr 8994 reading creates a conditional content-conflict test; E34 supports chant succession without establishing a seam or side map.

```sh
.venv/bin/python research/continuation_33/check_sources.py
.venv/bin/python research/continuation_34/check_sources.py
.venv/bin/python -m lost_library knowledge build
.venv/bin/python -m lost_library knowledge validate
.venv/bin/python -m lost_library knowledge export
```

Serve locally and open `/viewer/knowledge.html` to inspect claims, missing inputs and all 70 cited image regions. The historical ten-case review remains separate. The current working inventory is 177 image files, including four new resolutions of existing Fr 8994 photographs. Earlier numerical summaries above describe their dated snapshots. E20's full-fragment-file hash check belongs to its historical snapshot; use the new source/knowledge checks for the updated capture inventory, without changing the frozen experiment.

## E35/E36 source follow-up — 27 October 2026

The [E35 overlap experiment](RESEARCH_CONTINUATION_35.md) and [E36 continuation controls](RESEARCH_CONTINUATION_36.md) extend the active goal. The Aboense demonstration now selects the actual boundary captures, with provisional side mapping. Two exact phrase continuations support already catalogued edges; a generic Alleluia boundary remains weaker. The overlay version 1.1.0 contains 163 overlapping entries and 77 regions. No new attribution or novelty is established. Run `.venv/bin/python research/continuation_36/record_evidence.py` for the seven new region/hash/declared-string checks; E35's optional OpenCV replay instructions are in its report. No acquisition is required.

## E37 source continuation — 27 October 2026

The [latest source result](RESEARCH_CONTINUATION_37.md) identifies one shorter Fr 20274 antiphon ending, preserving limits on whole-office and codex attribution. Four new manuscript regions bring the overlay to 81 regions and 165 overlapping entries. Use `.venv/bin/python research/continuation_37/check_sources.py --require-private` locally to verify the retained scholarly reading copies; omit the flag in the review archive, which deliberately excludes those copyrighted PDFs. The shared manuscript pixels and metadata remain available offline. No discovery or publication is established.

## E38 follow-up — 27 October 2026

The [E38 comparison](RESEARCH_CONTINUATION_38.md) now includes actual C23 folio 69r. Run `.venv/bin/python research/continuation_38/check_sources.py` to verify its original/derivative hashes, three regions and label receipts offline. The current overlay has 166 overlapping entries and 84 regions; 179 working manuscript files remain within the resource limits. Text agreement does not establish a melodic match or a new codex. No publication occurred.

## E39 follow-up — 27 October 2026

The [E39 musical comparison](RESEARCH_CONTINUATION_39.md) retains 12 provisional concordances and two unresolved events across two selected windows. Run `.venv/bin/python research/continuation_39/compare_notes.py`, then `record_evidence.py` and `check_sources.py` from the same folder path. Use `--require-private` for the locally retained method/dissertation PDFs; omit it in the review archive, where their absence is explicit. No exact melody or new book attribution is established. Current overlay: 167 overlapping entries, 89 regions.

## E40 follow-up — 27 October 2026

The [E40 source test](RESEARCH_CONTINUATION_40.md) adds five regions and an unresolved placement interpretation with explicit falsifiers. Run `.venv/bin/python research/continuation_40/record_evidence.py` and `.venv/bin/python research/continuation_40/check_sources.py` offline; do not replay the failed acquisition. The current ontology has 168 overlapping entries and 94 regions. No physical join or new codex is established.

## E44 source comparison — 29 October 2026

The [Fr 8066/Fr 9620 check](RESEARCH_CONTINUATION_44.md) inspects nine native photographs. Shared five-rule bands and Dedication language do not identify one book; a likely hymn cue is reference-assisted. No new codex or confirmed catalogue correction is established. Run `.venv/bin/python research/continuation_44/check_sources.py` offline; `record_evidence.py` reproduces the retained observations, not a new reading. Current overlay: 168 entries/117 pairs, 887 entities, 595 claims, 109 regions; 49 pairs remain metadata-only. The inventory has188 source files for existing objects and the conservative transfer plan is1,669,530,774bytes. Earlier numerical summaries describe dated snapshots.

## E45 service/text follow-up — 29 October 2026

[E45](RESEARCH_CONTINUATION_45.md) directly records Laudes/invitatory labels and partial corresponding verse passages. Neither a full duplicated office opening nor a secure distinctive variant is established. Run `.venv/bin/python research/continuation_45/check_sources.py` offline; add `--require-private` to require the locally retained reading PDF. Current overlay:168 entries/117 pairs,888 entities,595 claims,117 regions;49 pairs remain metadata-only. The188-file inventory and transfer plan are unchanged. Next is actual music/underlay comparison, with no melody imported from a concordance.

## E46 music/context check — 29 October 2026

[E46](RESEARCH_CONTINUATION_46.md) records five-versus-two candidate head groups and a probable work mismatch, with no same-chant variant or book exclusion. Full interval transcription remains incomplete. Run `.venv/bin/python research/continuation_46/compare_notes.py`, then `record_evidence.py` and `check_sources.py` from that folder path; add `--require-private` only to the source checker to require the earlier local guide. Current overlay:168 entries/117 pairs,891 entities,598 claims,123 regions;49 pairs remain metadata-only. No new source files or publication.

The latest [E47 source audit](RESEARCH_CONTINUATION_47.md) credits13 previously uncredited Aboense control pairings from exact published workbook rows. The ontology retains168 entries/117 pairs and123 source regions;36 pairs remain metadata-only. This is a correction to the project register, not a new historical finding. The existing research goal remains incomplete.

[E48](RESEARCH_CONTINUATION_48.md) audits the remaining36 source-only comparisons: five published control pairings are credited and31 direct primary pair tests remain explicitly pending. A BOMPAC-4861 co-assignment conflicts with the published8201/8304 rejection; both source assertions remain separate. This is a reviewable source-reconciliation issue with novelty uncleared, not a new codex discovery.

[E49](RESEARCH_CONTINUATION_49.md) inspects the actual eight8201/8304 photos. It supports the8304 opening but leaves full replication of the published exclusion dependent on Fr20106. Four qualified source regions raise the overlay to127; an A103 catalogue candidate remains unmerged without an exact physical crosswalk. No new discovery is established.

[E50](RESEARCH_CONTINUATION_50.md) adds a bounded primary layout test of Fr10349/Fr2862, with a qualified field-design distinction and unresolved book identity. Thirty source-only pair tests remain pending. Six exact source files bring the working inventory to194; the source ledger preserves both failed requests and partial coverage. No new discovery or public release is established.

## E51 source update — 30 October 2026

[E51](RESEARCH_CONTINUATION_51.md) checks current BOMPAC release identity and the10370/20274 margins. Current XLSX inputs are unchanged; no secure comparable original address or new discovery results.29 source-only pairs still lack a first direct comparison. The local archive includes retained metadata receipts, exact source regions and source checks; no public release has occurred.

## E52 source update — 30 October 2026

[E52](RESEARCH_CONTINUATION_52.md) adds13 limited Ant49 context/layout comparisons and seven exact regions. General appearance fails the known wrong-pair control; candidate chant-function and mixed-block observations do not establish a new book.16 pairs still lack a first direct comparison.200 source files remain within the existing limits. The source-pixel figure, receipts and checks are included locally; no publication has occurred.

## E53 source update — 30 October 2026

[E53](RESEARCH_CONTINUATION_53.md) adds eight limited retained-source comparisons and nine precise regions. Similar hymn openings provisionally represent different known works; no original book finding is established. Eight existing pairs still lack a first direct comparison.200 source files/resources are unchanged. The source-pixel figure and offline checks are packaged locally; no public release has occurred.

## E54: initial coverage and unresolved identity

E54 records eight limited direct comparisons using27 selected photographs. No new attribution, historical exclusion or catalogue correction is established. Zero stored pairs await a first limited comparison; historical adjudication and diagnostic text/music collation remain incomplete. All lead decisions and frozen2E/7C/1D reviews are unchanged. Version1.18.0 retains168 entries/117 pairs,958 entities,640 claims and167 regions.208 working source files; conservative transfer plan1,675,854,139bytes including the existing1GB reserve. Exact lifetime traffic remains unverified. See [E54](RESEARCH_CONTINUATION_54.md). Reproduce its source checks with `.venv/bin/python research/continuation_54/check_sources.py`. No public release has occurred.

## E55: unresolved musical detail

E55 tests the two E39 upper-note uncertainties against local staff geometry. Both retain3/4 alternatives; four of twelve complete rule fits fail, and two spem anchors also widen under the same sensitivity. No new pitch, melodic variant, book attribution or discovery is established. Knowledge1.19.0 has959 entities,641 claims and167 regions across168 entries/117 pairs. Lead states and frozen2E/7C/1D are unchanged.208 source files and the conservative1,675,854,139-byte plan are unchanged. [E55](RESEARCH_CONTINUATION_55.md) and `research/continuation_55/check_sources.py` preserve the failed fits and exact source anchors. The goal remains active; no public release occurred.

## E56: Turku fragment C

E56 links Turku museum record TKM23245:3 provisionally to Codices Fennici fragment C through matching attributed descriptions. CF describes two folios in a damaged bifolium; the museum counts one object. An older Helsinki description agrees on the bifolium, while the later one-folio/archive description remains unresolved. CF and the museum copy print F.m. II.157; IV.157 is a plausible intended reference, not a confirmed correction. No images were newly inspected, and the published sewing-hole/placement proposal is credited to its source. No new discovery is established. See [E56](RESEARCH_CONTINUATION_56.md).
# Current research update — E57

[E57](RESEARCH_CONTINUATION_57.md) records provisional Fr 8311 chant readings and a published Trier parallel, including a differing first verse. No new attribution or discovery is established; source order and melody remain unresolved. The research goal remains active.

# Current research update — E58

[E58](RESEARCH_CONTINUATION_58.md) compares Fr 8311 photograph boundaries and finds two indexed examples of the same six candidate chant/verse IDs. Image overlap, complete original order and book identity remain unverified. The research goal remains active.

# Current research update — E59

[E59](RESEARCH_CONTINUATION_59.md) adds relevant 2025 scholarship on IV.156 and keeps its proposed book-use setting distinct from the unresolved Fr 8994 relationship. The f.9 source-image test and the research goal remain open.

# Current research update — E60

[E60](RESEARCH_CONTINUATION_60.md) identifies a conditional opening-text conflict between Fr 10370 and the indexed IV.156 f.8 description. Their shared original address and book identity remain unverified; the research goal remains active.

# Current research update — E61

[E61](RESEARCH_CONTINUATION_61.md) records an additional Fr 10370 chant candidate and an indexed non-adjacent liturgical-order example. The Finnish page, same-book relationship and k-II interpretation remain unresolved; the research goal remains active.

