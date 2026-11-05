# The Lost Library — guide to the research project

**Status: bounded research manuscript for review, 5 November 2026.** The project sought a new relationship among Nordic medieval manuscript fragments. It has not established one. The frozen investigation and its documented Ant 49 follow-up are reported as a case study with unresolved questions, rather than as an exhaustive proof that no discovery is possible. No specialist has independently reviewed the findings.

## Start here

1. [Research paper](RESEARCH_PAPER.md): the question, methods, complete ten-case outcome, retrieval results, data-quality observation and limitations.
2. [Evidence dossiers](EVIDENCE_DOSSIERS.md): each candidate, sources, contrary evidence and exact region identifiers. The dossiers include older dated snapshots; read their context with the [current project state](PROJECT_STATE.md).
3. [Validation report](VALIDATION_REPORT.md): test splits, denominators, thresholds, leakage limits and reproduction commands. The pilot is exploratory, not independent confirmation of a historical claim.
4. [Reviewer packet](REVIEWER_PACKET.md): questions and source regions for eventual specialist review. It is a draft, not correspondence; nobody has been contacted.
5. [Rights and licence status](DATA_RIGHTS.md) and [third-party material](THIRD_PARTY.md): review these before sharing. Code licensing is not yet selected and the package does not grant rights over other collections or publications.

The local review archive, `output/research/lost-library-review.zip` when present, is a checksummed snapshot with its own manifest and verification receipt. Its manifest states exactly which version of each file is included; later notes are not automatically included. The archive excludes privately retained scholarly PDFs and model weights. A repository release is a separate selection and may be newer.

## Claims at a glance

- **Manuscript reconstruction:** ten frozen cases: two previously documented associations, one previously published rejection and seven unresolved. No new physical attribution or exclusion is established.
- **Automated retrieval:** the small closed-gallery baseline performed well at ranking but its threshold produced many false positives and accepted a published different-book pair. The results are not identity probabilities or a general accuracy estimate.
- **Dataset observation:** a reproducible discrepancy affects some column-count values in the checked combined BOMPAC dataset. Its cause, first notice, full impact and independent review remain open. It is not a medieval discovery.
- **Historical leads:** the Finnish IV.156 f. 8 / Swedish Fr 10406 overlap, the date conflict for IV.173 / Fr 25592 and the Fr 8073 hymn reading are conditional. Exact missing images, transcriptions and prior literature are recorded in the paper and [open questions](OPEN_QUESTIONS.md).

## Reproduce and review

Follow the setup and offline replay instructions in [README](README.md). The [paper](RESEARCH_PAPER.md) and [review packet](REVIEWER_PACKET.md) point to exact audit scripts and source-region records. The archive's checks establish integrity and reproducibility at their stated scope; they do not establish historical correctness, novelty or independent review.

The research manuscript is a draft for the project owner's review, not an independently peer-reviewed paper. Missing Finnish images, source literature and independent readings remain limitations and possible later follow-up. No library or researcher was contacted during the investigation.
