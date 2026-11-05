# E45: service labels and partial corresponding Dedication passages

29 October 2026, Europe/Vienna. E44 made progress: nine source photographs, explicit failed discriminators and a verified review package were completed. E45 re-examines all nine retained photographs for a stronger test of the existing Fr 8066/Fr 9620 pair. **The same-book question remains unresolved. No new codex, exclusion, distinctive variant or discovery is established.**

## Direct source results

The [protocol](research/continuation_45/protocol.json) preserves the nine image hashes and the frozen/core inputs. All nine photographs and prior E44 references were already known, so this is exploratory AI reinspection. [manual_readings.json](research/continuation_45/manual_readings.json) accounts for every capture and retains uncertainty and contrary material. Eight exact regions are exported as [annotations](research/continuation_45/observations.json).

Fr 8066 capture2 has a red **lau/des** heading immediately before the large Domum initial. This directly labels that local block as Laudes. The following retained text includes Domus mea, Haec est domus, Bene fundata and Lapides preciosi; capture4 includes Mane surgens. Its next red heading appears to name second vespers before Ante aram, but the abbreviated prefix remains less secure than vesperis. This is a partial service map, not a complete edition or medieval-side assignment.

Fr 9620 capture1 has a source-visible **Inuitato/rium** label introducing a large-initial notated passage. Its following words are incompletely deciphered. The likely Hoc in templo cue remains reference-assisted from E44. A heading does not automatically assign all surrounding items or establish their exact positions.

The full pass also retains material that a simple different-service explanation would miss:

| Passage | Fr 8066 | Fr 9620 | What follows |
|---|---|---|---|
| Jacob/ladder passage | Candidate Vidi[t?] Iacob beginning in capture1 and a continuation including celos tangebat et angelos de/scendentes in capture2 | Partial Vidi[t?] Ia... and celos tangebat et d[e?]... in capture4 | A real partial textual correspondence; uncertain letters and lost right-hand text prevent a secure word-order variant. No angelos omission is asserted. |
| In loco isto | Verse text includes et enim dominus est in loco/isto et ego... | Capture5 retains ...est in loco isto et ego... with the prefix missing | Phrase-level correspondence; the missing prefix cannot confirm or contradict et enim. |

These are two corresponding passage windows, **not two independently identified responsories**. A decorated initial cannot decide genre. No complete duplicated office opening at one verified service position is demonstrated, and no immediate physical adjacency or seam follows. The [service figure](research/continuation_45/service-review.png) and [parallel-text figure](research/continuation_45/parallel-text-review.png) were visually checked; they contain separate raw PDM source crops, without restoration or stitching.

## Reference and prior-art scope

A new indexed [Cantus entry](https://cantusdatabase.org/chant/233459/) classifies a related Jacob passage as a verse in another witness. Direct open returned Cache miss and was stopped. An indexed [Cantus Index feast list](https://109www.cantusindex.org/feast/12008000?page=10) also lists related wording in another genre. These caution against assigning the local item from its incipit. No local chant ID, reference melody, witness image or full reference page is imported. The possible terminal t in Vidi[t?] was reconsidered after this reference exposure and remains uncertain, with the earlier reading preserved in the revision log.

The complete printed pp.293–294/PDF7–8 of [Grajewski2022](https://doi.org/10.25167/ls.4818) were visually inspected, including footnote11 and table2, with p292 text context. All29 PDF pages were text-searched, not read in full. Footnote11 explicitly excludes the other Ant49 fragments lacking Catherine chants. The published8201/8304 rejection therefore does not adjudicate this Dedication pair. This is a paper-specific scope clarification, not proof of wider originality. The private PDF/renders remain excluded from the archive. Exact scope and source hash are in [sources.json](research/continuation_45/sources.json).

## Decision and next test

The complete duplicated-opening argument is **unestablished with these photographs**. The partial corresponding passages remain available for a bounded musical/underlay comparison. Compare the actual celos-tangebat-et windows, preserving uncertain rule function, note events, syllable alignment and clipped text. Do not import the indexed melody, fill missing words or promote generic agreement to identity. Known Aboense control-source coverage remains a separate audit; it must not be counted as prospective discovery.

Version1.9.0 retains168 overlapping entries/117 pairs and595 claims, with888 entities and117 regions. The existing E44 same-codex interpretation is enriched, not promoted;49 pairs still have metadata/availability triage only. Frozen cases remain2E/7C/1D and all frozen/core/E35 hashes are unchanged. No new image was acquired:188 working source files and the1,669,530,774-byte conservative transfer plan remain within bounds. No contact, upload or publication occurred. Neither completion nor a global blocker is justified.

Reproduce the saved manual records and check their provenance offline:

```sh
.venv/bin/python research/continuation_45/record_evidence.py
.venv/bin/python research/continuation_45/check_sources.py
.venv/bin/python -m lost_library knowledge build
.venv/bin/python -m lost_library knowledge validate
.venv/bin/python -m lost_library knowledge export
```

Use `check_sources.py --require-private` locally to require the retained reading PDF; the shared archive reports its intentional absence. The checker verifies hashes, dimensions, coverage, coordinates and declared limits. It does not independently validate the readings, full office positions, attribution or novelty. Current validation and archive replay outcomes are recorded in [VALIDATION_REPORT.md](VALIDATION_REPORT.md) and [package_verification.json](output/research/package_verification.json).
