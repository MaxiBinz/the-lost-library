# E47 — credit the published Aboense reconstruction

29 October 2026. This continues the existing discovery goal and complete-lead audit. No new target family, discovery criterion or model screen is introduced.

The six retained Graduale Aboense controls are explicitly assigned to the same published BOMPAC reconstruction. Thirteen pair leads that previously had only catalogue/availability triage now receive their proper **previously documented** status. This repairs our register, not the scholarly record. No original manuscript attribution or independent confirmation is established.

## Exact source test

The [protocol](research/continuation_47/protocol.json) and immutable [register baseline](research/continuation_47/lead_register.before.json) were saved before inspecting the decisive workbook rows. Selection was fixed to the six existing objects and their15 pairings. Catalogue/Taitto reconstruction credit and E36 observations were already known, so this is a source-credit audit, not a blinded attribution experiment.

The retained, checksum-pinned [combined BOMPAC deposit](https://doi.org/10.5281/zenodo.17511106) assigns all six exact identifiers to **BOMPAC-4795**, with **FM.II.44**, Sequ-42 and Codex-1104. Each has one exact identifier match, an explicit Include row flag and no exclusion criterion. Assignment comes from the reconstruction field, not an inference from the common codex label.

| Object | Combined workbook, Sheet1 row | Raw workbook, Blad1 row |
|---|---:|---:|
| Fr7957 | 7959 | 7959 |
| Fr7960 | 7962 | 7962 |
| Fr7961 | 7963 | 7963 |
| Fr8343 | 8345 | 8345 |
| Fr8344 | 8346 | 8346 |
| Fr9242 | 9242 | 9242 |

In Sheet1, C is the fragment reference, M the explicit reconstruction, U the Finnish signum and BO the inclusion flag. The [related raw deposit](https://doi.org/10.5281/zenodo.17701360) assigns the same six to C-1481. Its D column contains fragment IDs and F the unit. These related deposits can share upstream catalogue/research evidence. Their agreement supplies no independent corroboration. All inspected source cells, exact addresses, unit members and source hashes are retained in [memberships.json](research/continuation_47/memberships.json).

## Count records before counting leaves

The combined unit has31 included rows: seven KA records and24 FM records. The Finnish rows24638–24661 each name a paired-folio record, collectively naming folios1–48. The raw unit has the seven KA identifiers. Both units include Fr28175 as their seventh Swedish record; its missing local image is not repaired by a spreadsheet assignment.

Thus31 is a **dataset-row count**, not a leaf count, newly located objects, available photographs or an image-ready cross-border census. Paired folio labels are source descriptions, not a new physical collation or proof of present conjugacy. No physical leaves or captures are generated from them. The previously credited Haapanen/Taitto reconstruction remains prior work; Taitto2002 was not reread in this iteration.

## Consequence for the research

The overlay version1.11.0 retains168 overlapping lead/question entries and117 physical-pair leads. Thirteen decisions change from unresolved metadata triage to previously documented; the other decisions stay unchanged. Thirty-six pair leads remain metadata-only. The two already reviewed Aboense pair dossiers retain their existing scope, and E36's direct continuity observations remain separate from this source-assignment test.

Six attributable assignment claims connect the retained physical objects to the reconstruction concept. A separate source assertion connects the existing F.m.II.44 concept through the24 source records. Physical objects are not merged. Computational suggestions and their scores remain untouched. No adjacency, side order, exact date, physical join, novel discovery or improved recognition is inferred.

The frozen ten cases remain2E/7C/1D, with no A/B attribution. No new source file or network acquisition was needed:188 working source-image files and the1,669,530,774-byte conservative transfer plan remain unchanged. No outreach, upload, external edit or publication occurred.

## Reproduce and continue

```sh
.venv/bin/python research/continuation_47/audit_membership.py
.venv/bin/python -m lost_library knowledge build
.venv/bin/python -m lost_library knowledge validate
.venv/bin/python research/continuation_47/check_sources.py
.venv/bin/python -m lost_library knowledge export
```

The extraction uses openpyxl3.1.5 in read-only/data-only mode; this run used the bundled Python runtime. No workbook is recalculated, modified or exported. The independent checker uses only Python's standard ZIP/XML reader to resolve sheets by name and check the literal source cells, headers, unit-row set, absence of formulas in the inspected columns, register changes and frozen hashes. This independently checks extraction arithmetic/provenance, not historical truth. Packaging also runs it from the extracted archive.

Next, check the remaining36 existing pair leads against explicit assignments already retained in the project, then select a primary-source test that can distinguish a genuinely unresolved relationship. Keep different unit labels separate from a published different-book rejection. Unread scholarship and missing originals remain claim-specific dependencies. The discovery goal is active and incomplete; these source-credit repairs cannot substitute for scientific success or an exhausted-queue negative result.
