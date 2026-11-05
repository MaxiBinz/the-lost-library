# E44: Ant 49 Dedication text and ruling check

29 October 2026, Europe/Vienna. The existing Fr 8066/Fr 9620 comparison has now received direct source inspection. **It remains unresolved; no new codex, different-book exclusion or confirmed catalogue correction is established.** The preliminary interruption had produced only a protocol and previews; [resumption.json](research/continuation_44/resumption.json) records that as no progress. The completed work below is separate.

## Sources and predictions

The [protocol](research/continuation_44/protocol.json) asks whether the two Dedication passages duplicate a corresponding office opening or instead occupy different sections, and whether their ruling differs. Catalogue notes and the published 8201–8304 rejection were already known: this is exploratory AI reading, with no blind or independent adjudication.

All nine exact painting-image URLs listed in the two retained Riksarkivet IIIF manifests were acquired successfully: four photographs for Fr 8066 and five for Fr 9620, totaling **2,769,595 bytes**. Each has its original canvas, URL, dimensions, hash, rights and receipt in [captures.json](research/continuation_44/captures.json) and [download_receipts.json](research/continuation_44/download_receipts.json). Public Domain Mark 1.0 comes from each manifest's Rights metadata. No endpoint was invented, failed route retried, new physical object created or medieval side assigned. These are additional files for existing objects.

All nine native photographs and the six earlier first-capture images were inspected. Four fixed control windows use Fr 8201, 8304, 8072 and 8073, including the published different-book pair. The eleven new region annotations retain literal candidates and uncertainty separately from interpretation. [Initial readings](research/continuation_44/inspection.v1.json) are preserved; [version 2](research/continuation_44/inspection.v2.json) discloses a later reference-assisted revision.

## What the pixels support

| Test | Observation | Consequence |
|---|---|---|
| Proposed four-/five-rule split | Both selected native music bands show five horizontal rules, apparently four dark and one red. All four lower-resolution control bands also show five. | The proposed split is unsupported in these windows. This feature occurs across the published different-book control and cannot identify one codex. |
| Different book genres | Both catalogue records say Antiphonarium and both originals contain notated chant. | E43's possible hymn-book interpretation is withdrawn. Fr 9620's hymn reference describes an item/incipit within the material. |
| Corresponding Dedication opening | Fr 8066 includes Domum tuam, Domus mea and other church-building texts; Fr 9620 includes O quam metuendus and Fundata est domus. Captures are partial and some text is cropped or damaged. | No complete duplicated opening at one verified service/position has been demonstrated. Shared Dedication language supplies compatibility, not identity or exclusion. |
| Fr 8066 relative order | Capture 2 ends die and capture 3 begins rum. | A candidate dierum continuation supports relative reading order only; no complete medieval side or physical seam follows. |

The [ruling figure](research/continuation_44/ruling-review.png) and [text figure](research/continuation_44/text-review.png) show separate raw source crops, not a reconstructed page. Both were visually reviewed. The ruling count describes visible rules; their precise musical function and absolute pitch remain unverified.

The Fr 8066 source note says three black rules plus one red; Fr 9620 says four black plus one red. Normalized notation fields retain the source's uncertain four-line description. The inspected pixels raise a possible descriptive/counting discrepancy. An extra guide rule, counting convention or source error must be distinguished before proposing a correction. First notice has not been checked; no institutional metadata was edited.

## Reference assistance and prior art

The Fr 9620 short cue was first read uncertainly as Hoc e[st?] illud. After a chant-reference search and fresh raw-image inspection, the better provisional reading is **Hoc i[n?] templo**. The terminal word is clearer than the abbreviated middle. No following hymn words were supplied from a reference.

The directly read [Cantus Network Seckau structured edition](https://gams.uni-graz.at/o:cantus.seckau3/sdef:TEI/get?locale=en&mode=view:structure), section 125, uses that hymn in several office contexts and places Dedication material across different services. This supplies a plausible comparison and cautions against assigning the local service from the incipit alone. It is another witness's edited text; its source images and full edition were not inspected. Two Cantus entries and one CAVET result were available only through search indexing; direct opens returned Cache miss and were stopped. [sources.json](research/continuation_44/sources.json) records each scope. No exact local chant ID, imported office position, novel variant or independent confirmation is claimed.

## Register, checks and next action

Knowledge version **1.8.0** contains **168 overlapping entries, 117 pair leads, 887 entities, 595 claims and 109 regions**. The existing 8066/9620 pair and Ant 49 audit are enriched; no candidate family is added. **49 pairs** still have only metadata/availability triage, down from E43's 50. The 43 Beauvais source-credit repairs remain intact. Frozen cases stay **2E/7C/1D, zero A/B**, and all frozen/core/E35 files retain their hashes. Shared catalogue assignment is still not book identity.

The resource audit now counts **188 working source files**: 171 core files, eight external comparison files and nine additional Fr 8066/9620 files. The conservative transfer plan is **1,669,530,774 bytes**, including the existing 1 GB reserve, within the 300-file/3 GB bounds. No outreach, upload or publication occurred.

Source-provenance/region checks, knowledge validation, all 61 Python tests and both Node viewer files pass. These validate records and software behavior, not independent historical truth. A scoped live browser check verified the unresolved pair, revised reading, retained native image and correct red box; [viewer_review.json](research/continuation_44/viewer_review.json) records both screenshots. Full accessibility and historical adjudication remain open. Final extracted archive replay outcomes and exact archive hash/count are recorded in [package_verification.json](output/research/package_verification.json).

Reproduce the retained observations offline, without fetching anything:

```sh
.venv/bin/python research/continuation_44/record_evidence.py
.venv/bin/python research/continuation_44/check_sources.py
.venv/bin/python research/audit_resources.py
.venv/bin/python -m lost_library knowledge build
.venv/bin/python -m lost_library knowledge validate
.venv/bin/python -m lost_library knowledge export
```

Next, map the retained Dedication sequences to source-visible rubrics and service positions, preserving gaps. Test a duplicated opening only at a verified corresponding position. If no diagnostic overlap survives, record that limit and select the next existing primary-image pair rather than repeat generic ruling compatibility. Investigate the line-count convention separately before any catalogue-correction claim. Finnish originals and unread prior art remain specific dependencies of their own attribution questions. Remaining local source work means neither goal completion nor a global blocker is justified.
