# E110 — tracing the column discrepancy through the local research

**4 November 2026.** A source-lineage and counterfactual check following [E108](RESEARCH_CONTINUATION_108.md)–[E109](RESEARCH_CONTINUATION_109.md). This does not claim a manuscript discovery or independently verify every historical analysis.

## Current data lineage

The current local matcher reads normalized values from `data/fragments.json`; its metadata score includes a `columns` feature. The current ingestion code builds the MPO column value from the original `spaltenzahl` field in the local source CSV, not the BOMPAC combined workbook's `Columns` field.

For all **115 current local MPO records**, the saved normalized value equals the current parser's result for the exact unique CSV record. For those same 115 records, the CSV's raw `spaltenzahl` string agrees with the exact included record in the checksum-verified raw BOMPAC workbook. This includes missing and qualified source values under the parser's existing rules; it does **not** establish that the catalogue is physically correct or that its uncertainty is fully preserved.

Among 100 local records where both the saved value and the combined-workbook field are integers, **64 differ and 36 agree**. Fifteen other local records lack a comparable integer in one or both fields. These are convenience-selected local records, not an estimate of errors in the complete collection. The result shows that a straight switch to the combined field would alter local feature inputs; it does not mean the present pipeline made that switch.

## Controlled substitution, without changing the project

The script recomputes the existing metadata score for each of the 170 saved candidate rows and, where possible, substitutes the combined-workbook value **only in temporary copies**. For 110 rows at least one MPO operand had numeric values in both places. All 110 recomputed baseline metadata scores matched the saved metadata values to `1e-12`. Of those 110, **16 metadata scores changed** under the counterfactual and 94 did not. These are candidate rows, not necessarily independent fragment pairs. Rankings, image scores, frozen inputs and actual saved results were not recomputed or modified; no change in historical model accuracy is claimed.

For example, the Fr 10349 / Fr 2862 metadata score changes from approximately **0.698 to 0.809** if the combined value is substituted. The raw records and [E50's image comparison](RESEARCH_CONTINUATION_50.md) describe two narrow columns for Fr 10349 and one broad column for Fr 2862; the substituted combined values make that one feature agree. This is a demonstration of a **false appearance of compatibility**, subject to E50's existing limits on full image coverage and physical identity. Neither score is an identity probability or proof of a historical relationship.

The code for [E91](research/continuation_91/compare_layout.py) does extract the combined `Columns` field for Fr 10370, but its reported difference is calculated from written height and width, not column count; the stored and raw column values for Fr 10370 agree. Its other measurement and leaf-identity uncertainties remain. The source-code search cannot certify every external, manual, earlier or unpublished analysis.

## Reproduce and boundaries

```sh
.venv/bin/python research/continuation_110/audit.py
```

The script verifies both workbook hashes, checks exact unique local IDs and raw records, records the local input hashes, and writes [results.json](research/continuation_110/results.json), including all changed candidate rows and computed scores. It makes no changes to the local source metadata, model, candidate queue or published data. A zero-difference outcome here means field lineage, not an independent judgement of palaeography or truth. Maintainer confirmation and current-version verification for E108 remain open; no contact or publication occurred.
