# E51: Current dataset releases and original-address limits

30 October 2026. Continuation of the existing discovery goal and its25October amendment. No new target family, recognition tuning, external message or publication.

## Result

The latest official BOMPAC releases still distribute the identical two workbooks used in the project. The unresolved source disagreement around BOMPAC-4861 and the published8201/8304 rejection therefore remains present in the **current XLSX distribution**. This closes a version/currentness gap, not the historical argument or novelty audit.

A fixed primary comparison of Fr10370/Fr20274 inspects all six retained target photographs plus two selected Fr8994 mark controls. It recovers **no secure comparable original folio/quire address** across the pair. Fr10370's already recorded ij/II and k-like marks are reused evidence. Fr20274 has an uncertain red upper-margin sign and a later pencil library identifier. No shared/conflicting medieval address, book attribution, exclusion or catalogue correction is established.

## Official release check

The [metadata protocol](research/continuation_51/protocol.json) uses the documented anonymous public Records API. The two old HTML record failures were not retried. Exact returned latest-version links identify [combined v1.1](https://doi.org/10.5281/zenodo.19046496) and [raw v1.1](https://doi.org/10.5281/zenodo.19047125), both dated16March2026. Their concept IDs, version relations and latest flags are retained; record-number magnitude alone was not used to infer currentness.

Three requests returned200 and saved31,373 bytes. Every response is hash-pinned in [metadata receipts](research/continuation_51/metadata_receipts.json). All five original file receipts—two workbooks, two readmes and the Kaasik commentary—match the latest publisher MD5 and size values. The local retained bytes also pass MD5/SHA checks. The review archive includes both actual workbooks; private reading PDFs remain excluded, with their original receipts available for comparison.

The descriptions say v1.1 adds CSV with unchanged data. The new CSV files were **not downloaded or checked**. Publisher release wording, checked workbook identity and untested CSV equivalence are kept separate. Exact E48 workbook-cell findings therefore apply to the currently distributed XLSX files, including the4861 co-assignment of8201/8304. Neither checksum identity nor this version check proves the reconstruction correct, supplies an authorial pair-level argument, or establishes a novel correction. [Machine-readable comparison](research/continuation_51/metadata_comparison.json).

## Source-image margin test

The [primary protocol](research/continuation_51/primary_protocol.json) was saved before fresh target inspection. This is an explicitly unblinded audit:10370 text/marks and20274 chant work had already been seen. Four10370 and two20274 photographs were selected by exact canvas/highest retained resolution; they are not six leaves. Medieval sides remain unknown.

The source-visible observations are:

- Fr10370 capture1 has the previously recorded two-stroke ij-like sign, compatible with catalogue II; capture3 has the previously recorded k-like mark. The8994 IIII/k controls show how similar conventions can occur elsewhere, not a unique identity fingerprint.
- Fr20274 capture1 has a red angular glyph with flanking punctuation. Candidate shape f-like/4-like is retained without secure diplomatic reading, numeric normalization or address assignment.
- Fr20274 capture2 has a pencil reference provisionally read **KB / A103 k / CXVIII**. Its components correspond to the pinned catalogue's KB / A103 / k118 reference. It is a later identifier, not medieval folio118.
- The rotated account heading on10370 capture4 is excluded from original foliation. The text-bearing strip at capture2's edge has no accepted address, attachment or physical-join interpretation.

Four new precise regions and four reused prior mark regions support this record. [Manual readings](research/continuation_51/manual_readings.json), [annotations](research/continuation_51/observations.json), and the visually inspected [PDM-only crop figure](research/continuation_51/mark-review.png) preserve both the observations and their limits. No image was reconstructed or generated; only retained pixels were cropped and fitted using nearest-neighbour display.

The full k-series reference may matter to the missing Fr20106/k95 crosswalk. The20274 reference and an indexed Uppsala source-list example do not establish that crosswalk or identify the previously found A103 psalter as the same physical object. The source-list PDF open failed with Cache miss and was stopped. Earlier truncated search output is not used as positive or negative evidence. [Source/access notes](research/continuation_51/sources.json).

## Register, resources and next work

Version1.15.0 retains168 overlapping lead/question entries and117 pair leads, with923 entities,631 claims and139 regions. Decision totals remain72 unresolved,87 previously documented,3 contradicted,5 supported and1 not testable. The frozen ten remain2E/7C/1D. One first-primary-comparison flag changes after this actual pair test: **29 source-only pairs still lack a first direct comparison**. Completion of this fixed address audit does not mean completed historical adjudication. The E50 layout test still explicitly has partial photo coverage.

Current-release provenance enriches existing source/interpretation entities rather than creating another codex or independent vote. The single added supported claim describes the later20274 library reference; it is not a same-codex claim. The A103 candidate remains a CatalogRecord with no accepted physical-object link. E50's strict historical31→30 transition is checked against the pinned pre-E51 register; E51 separately verifies30→29. No historical decision is changed to inflate progress.

No new source image or workbook was downloaded. The working source inventory stays194. The conservative transfer plan is **1,671,104,323 bytes**, including the existing1GB reserve. Exact lifetime traffic is unverified, and web-reader/search traffic is not separately measured.

Continue discriminating tests on the existing unresolved queue. Do not repeat generic red-glyph resemblance or treat a different feast as evidence of different books. A future10370/20274 address argument needs readable original marks, a demonstrated addressing convention and source/surface mapping. The20106 opening and unread Finnish scholarship remain specific dependencies, not a global stop. No original scientific discovery or independent confirmation is established; the goal remains active and incomplete.

## Reproduce

```sh
.venv/bin/python research/continuation_51/record_evidence.py
.venv/bin/python research/audit_resources.py
.venv/bin/python -m lost_library knowledge build
.venv/bin/python -m lost_library knowledge validate
.venv/bin/python research/continuation_51/check_sources.py
.venv/bin/python -m lost_library knowledge export
```

These steps use retained sources. Do not rerun completed metadata requests. Source checks establish provenance, literal metadata consistency, bounds and state transitions; they are not an independent paleographic reading or historical adjudication. Full archive verification is recorded in `output/research/package_verification.json`; frozen metrics and case-screen output must remain unchanged.
