# E108 — a reproducible column-count discrepancy in BOMPAC research data

**E114 update, 4 November:** Zenodo's combined record lists v1.1 as newest of two releases. The newly inspected v1.1 CSV matches this workbook in seven specified fields on all 29,586 rows, and reproduces the 22,248 equal Swedish column/leaf count pairs. Its publisher checksum matches. This verifies the affected CSV fields, not all CSV content, the separate raw dataset's latest version, cause or first notice. [E114](RESEARCH_CONTINUATION_114.md).

**E109 follow-up:** A small, identity-masked check supports the original description in four further readable mismatch examples; three selected images were unassessable. The same report quantifies a 13.7 percentage-point difference for the pre-existing 1/2-value subset and provides an exact candidate-row list. It does not estimate the error rate of the full corpus. [E109](RESEARCH_CONTINUATION_109.md).

**E110 impact follow-up:** The 115 current local Swedish records preserve values derived from the original MPO field. A temporary substitution of combined values changes 16 of 110 eligible saved candidate metadata scores; actual frozen results remain unchanged. This is a controlled illustration, not a past-results error or score calibration. [E110](RESEARCH_CONTINUATION_110.md).

**4 November 2026. Status: probable data-quality defect; first notice and the authors' intent are unverified.** This is a finding about a research dataset, not a medieval manuscript attribution or independent specialist review.

## What was checked

The [combined BOMPAC dataset](https://doi.org/10.5281/zenodo.17511106) readme (p. 3, “Measurements”) describes a field for the number of columns. In its checksum-verified workbook, among **22,553 included MPO rows**, both `Columns` and `No_of_leaves` are numeric on **22,248** rows. They are equal on **all 22,248**. The other 305 are outside this numeric comparison. For contrast, among included FM rows where both values are numeric, the fields are equal on 3,364 and different on 1,925 (5,289 total). The pattern is therefore specific to the selected MPO rows, not a general identity across the workbook.

For an additional source comparison, join included MPO rows to exactly one included `fragment_id` in the separately published [raw MPO workbook](https://doi.org/10.5281/zenodo.17701360), then retain only rows where both original `spaltenzahl` and combined `Columns` are exactly numeric 1 or 2. Of **14,415** eligible rows, **5,598** disagree: 3,783 are original 2 versus combined 1, and 1,815 are original 1 versus combined 2. The other 8,817 agree. These are comparisons of published fields, not a physical survey or proof that the original value is correct in every case. The 8,138 included MPO rows outside this 1/2 subset are not assessed by the matrix. Counts are fragment records, not independent medieval books.

| Exact example | Raw `spaltenzahl` | Combined `Columns` | Combined `No_of_leaves` | Retained photograph |
| --- | ---: | ---: | ---: | --- |
| Fr 25592 / Hy 49 | 2 | 1 | 1 | [capture 3](data/images/mpo-25592-capture-3.jpg) shows two parallel writing fields. |
| Fr 607 | 1 | 2 | 2 | [first capture](data/images/mpo-607.jpg) shows one broad main writing field; a short inset is present. |
| Fr 8994 | 1 | 1 | 1 | Agreement is consistent with either field because the two counts coincide. |

The photos are selected, previously available public-domain-marked Riksarkivet captures. They support the two **visible-surface** examples, not a verification of every side, the whole dataset or the raw source's accuracy in general. We did not inspect original objects. For Fr 25592 the image and raw column count also agree with the already documented E27/E53 two-column observation.

## Interpretation and impact

The exact equality in the Swedish subset, the opposite-direction source disagreements, and the two visible controls make mistaken duplication or mapping of leaf counts a **strong hypothesis**. They do not reveal the software cause, rule out a different intended meaning, prove the issue was previously unreported, or establish that the maintainers have not corrected it elsewhere. The readme's description and the original field definitions should be checked with the dataset maintainers before calling the cause confirmed. A search for these field names found no explicit notice, but indexing is incomplete and novelty remains open.

Filtering Swedish records by the combined `Columns` field is unsafe without resolving this discrepancy. Do not overwrite the published data or automatically replace all values: uncertain or missing original descriptions and image interpretation still need review. The local matching pipeline parses the original MPO `spaltenzahl` ([pipeline.py](lost_library/pipeline.py)) and its stored records for Fr 607, Fr 8994 and Fr 25592 preserve 1, 1 and 2 respectively. This checks those examples and the ingest path, not every past analysis or any claimed model quality.

The two source workbooks are the previously retained 2025-release files with verified SHA-256 and published MD5 receipts. On 30 October the project's [version audit](research/continuation_51/metadata_comparison.json) found the same workbook bytes in v1.1 (March 2026), which added CSVs described as unchanged. We have **not** verified that no later version or correction exists today. On 4 November ordinary web-reader opens of `https://zenodo.org/api/records/17511106/versions/latest` and `https://zenodo.org/api/records/17701360/versions/latest` were reported inaccessible; those exact routes must not be retried. No source file was downloaded or externally shared.

## Reproduce

```sh
.venv/bin/python research/continuation_108/audit.py
```

The script verifies both source hashes, matches exact fragment IDs, counts numeric values, records excluded categories and writes [results.json](research/continuation_108/results.json), including source cells for the three examples. A separate SQLite count of numeric values reproduced 22,248/22,248 for MPO and 3,364 equal plus 1,925 unequal for FM. These are computation checks, not independent expert review. Two candidate dated hymnary comparator manifests (`https://lbiiif.riksarkivet.se/arkis!R1002145/manifest` and `https://lbiiif.riksarkivet.se/arkis!R1001493/manifest`) were each opened once and reported inaccessible by the web reader; neither must be retried. This pass did not resolve Fr 25592's age.
