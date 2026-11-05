# E50 — copying-field layout test and bounded Fr20106 lookup

30 October 2026. E49 made progress and its package process was terminal; no live wait was resumed. This continues the existing source/data question and one of the remaining31 primary pair tests. The original discovery goal and frozen queue remain unchanged.

## An actual source test of Fr10349 / Fr2862

The fixed existing lead is **pair-d3edceeb5829ddeac135**. Both objects are catalogued as fourteenth-century antiphonals. Their descriptions report different column/system layouts and note nonoriginal folding for2862. Before fresh image inspection, the [primary protocol](research/continuation_50/primary_protocol.json) specified the alternative explanations: different writing designs, facing/folded pages, capture crops and composite volumes. It selected only this pair, with the already documented2863/2864 same-quire relationship as a limited source control. No new target family, model fitting or performance experiment was introduced.

The inspected photographs show **two narrow writing fields on10349** and **one broad music/text field on2862**. On2862 the staff rules continue across a reuse crease, so that crease does not divide the visible field into two writing columns. Both retained control photographs also show the broad design. This supports a local copying-layout distinction rather than attributing the apparent difference solely to the reuse fold. It does not resolve the exact original leaf/fold map or exclude a composite historical volume.

Seven distinct target photo views and two retained control views were inspected. Source coverage is qualified:10349 capture1 uses its retained800px thumbnail, and2862 capture3 remains unseen after a timed-out request. The other six target views were saved at the exact manifest-listed native URLs. The [manual record](research/continuation_50/manual_readings.json) accounts for every inspected view and the missing one. [Eight region annotations](research/continuation_50/observations.json) preserve the page context, gutter, reuse crease, controls and rulers. The [layout figure](research/continuation_50/layout-review.png) contains only retained PDM manuscript pixels; its fitting and labels add no historical detail.

## Approximate field widths, with all sensitivity outcomes

Post-inspection ruler anchors put the selected fields at approximately **7.4cm on10349** and **15.7cm on2862**. These concern an individual writing field, not the total written area, leaf size or a corrected catalogue measurement. Endpoint selection followed image inspection and is explicitly exploratory.

The [reproducible calculation](research/continuation_50/field_comparison.json) retains10/20/30/40/50px endpoint tolerances,±5px ruler-anchor tolerances and an additional illustrative±20% scale allowance. The intervals remain separate at10–40px with that scale allowance; they overlap at50px. These are sensitivity assumptions, not fitted errors, statistical confidence intervals or photogrammetric calibration. Paper/ruler plane differences and perspective remain limitations. No threshold was selected to classify a book, and the exact catalogue #15/#10 convention remains unadjudicated.

The visible field distinction is useful counterevidence to an unchanged uniform copying layout. **Historical same-codex identity remains unresolved.** Mixed sections, a copying-layout change, composite structure and the qualified original leaf/fold map prevent an unconditional exclusion. The two source-assigned BOMPAC units were already different; neither that fact nor this limited test is a new codex discovery or scholarly correction.

## Acquisition and source access

Eight exact painting-image URLs were selected from the two previously retained institutional manifests. Each URL was attempted once. Six returned successful JPEGs with matching source dimensions, totalling **1,542,176 confirmed bytes**. The first10349 native URL failed DNS in the network-restricted environment and was not retried. A2862 capture3 request timed out and was not retried. Permission to fetch the remaining unattempted public images outside that restricted environment was automatically granted; no remote access restriction was bypassed. The final unattempted capture4 request succeeded. [Receipts](research/continuation_50/download_receipts.json) preserve every outcome.

The six new files depict existing objects and bring the working source-file inventory to **194**. The conservative transfer plan is **1,671,072,950bytes**, including the existing1GB reserve. A timeout can have unmeasured traffic even when no body was saved, so confirmed file bytes are not an exact lifetime network total. The PDM statement is recorded in the manifest's Rights metadata and agrees with the existing object records; absent top-level rights are not silently replaced by a stronger new source statement. Original photographs, canvases and unknown medieval sides remain distinct.

The separate Fr20106 lookup read the exact raw BOMPAC row11947, which supplies an institutional record URL and archival/reference context. One ordinary open of that exact record and one linked library-identifier open both failed in the web reader and were stopped. No alternate-client retry, CAPTCHA interaction or guessed image URL followed. These outcomes do not prove global unavailability. [Access protocol](research/continuation_50/access_protocol.json) and [access results](research/continuation_50/access_results.json) retain the limits. The A103 candidate is still unmerged, and the full published opening argument still needs its correct source crosswalk.

## What changed in the research register

One previously source-only pair now has an **initial direct layout comparison**, with partial photo coverage and an unresolved book decision. The planned all-view inspection remains incomplete. Exactly that pair's primary-test-pending flag changes to false; **30 source-only pairs still have no direct pair test**. This flag counts the absence of an initial primary comparison, not completion of every planned source view or later historical test.

Version1.14.0 retains168 entries/117 pairs,915 entities,630 claims and135 regions. The new supported negative `stylistic_similarity` observation is scoped to visible copying-field layout; it does not become a negative `same_codex` assertion. Six additional source files link to existing physical objects/canvases. All decision states and frozen2E/7C/1D classifications remain unchanged. No new identity closure, catalogue correction, matcher improvement, independent confirmation or novelty claim is accepted.

The exact post-E49/pre-E50 register was preserved before the image-test overlay. E48/E49 checkers retain their strict historical31-pending expectations against that pinned snapshot while reporting the current pending subset. E50's checker separately verifies that exactly this one actual test accounts for the change to30. Historical checks are not discarded or rewritten as current research advances.

## Reproduce and continue

```sh
.venv/bin/python research/continuation_50/measure_fields.py
.venv/bin/python research/continuation_50/record_evidence.py
.venv/bin/python research/audit_resources.py
.venv/bin/python -m lost_library knowledge build
.venv/bin/python -m lost_library knowledge validate
.venv/bin/python research/continuation_50/check_sources.py
.venv/bin/python -m lost_library knowledge export
```

Acquisition is optional and receipt-aware; completed success/failure URLs are never automatically requested again. The source checker validates hashes, exact manifest pointers, bounds, arithmetic, resource accounting and the one primary-test transition. It does not independently judge the images, prove original leaf structure or clear novelty. The failed URLs remain stopped. Other existing primary pair tests can proceed independently of Fr20106 and the unread Finnish scholarship. The next book-level inference needs secure physical/quire or corresponding textual evidence and explicit treatment of composite/section alternatives. The discovery goal remains active and incomplete; no outreach, upload, external edit or publication occurred.
