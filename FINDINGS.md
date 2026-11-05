# Lost Library findings and rejected hypotheses

> Historical feasibility record begun 20 October. Later source research is summarized in [PROJECT_STATE.md](PROJECT_STATE.md), [RESEARCH_CONTINUATION_30.md](RESEARCH_CONTINUATION_30.md), [INDEPENDENT_RESEARCH_PASS.md](INDEPENDENT_RESEARCH_PASS.md) and [FINAL_REPORT.md](FINAL_REPORT.md). The current ten-pair queue retains seven ambiguous cases; no new attribution is confirmed.
Updated 25 October 2026, Europe/Vienna. Findings describe the available evidence; none is a new medieval manuscript attribution.

## Confirmed observations

| Finding | Evidence | What it permits |
|---|---|---|
| A useful public Swedish metadata export exists | [Source](https://zenodo.org/records/17287665), [profile](research/mpo_profile.json), cached CSV/checksum | Filtering and reproducible catalogue audits, with missingness preserved |
| Real Swedish, Finnish and Beauvais images can be obtained | [Initial access receipt](research/access_log.json), [Finnish PDF receipt](research/evidence/finnish_access.json), [Beauvais receipt](research/evidence/beauvais_access.json) | A bounded technical feasibility claim; not full-collection coverage |
| Leading-family image pointers actually work for several exact members | [20 October target receipt](research/target_access_log.json), [summary](research/target_access_summary.json) | Actual small JPEGs for 1385, 20274, 8994 and 25592; per-manifest Public Domain Mark |
| Broad cross-national integration/reconstruction is already prior art | [BOMPAC](https://doi.org/10.5281/zenodo.17511106), [CODICUM](https://www.codicum.eu/about) | An independent contribution must be more precise than combining the collections or building a viewer |
| Same hand and matching catalogue features do not establish one codex | [Published Ant 49 comparison](https://doi.org/10.25167/ls.4818), [actual diagnostic](research/metadata_retrieval_diagnostic.json) | Use text/quire contradictions and expert review rather than interpreting a maximal score as identity |
| A credible catalogue-level attribution audit is identifiable | [IV.157](https://fragmenta.kansalliskirjasto.fi/handle/10024/1300?show=full), [IV.173](https://fragmenta.kansalliskirjasto.fi/handle/10024/1314?show=full), [source audit](research/goal_novelty_audit.md) | Conditional investigation of exact known/suggested edges, not a novelty claim |
| Selected Fr 10370/10406 music rules have similar ruler-calibrated spacing | [E21 image coordinates and hashes](research/continuation_21/ruling_pitch_results.json) | Both selected groups measure about5.6mm per interval; this fits the existing catalogue association but other MPO records share comparable written-area dimensions. It is not a unique identity signal or a new attribution. |
| A metadata-matched different-codex control has the same staff pitch within measurement uncertainty | [E22 control/result](research/continuation_22/matched_staff_results.json), [source receipt](research/continuation_22/image_receipt.json) | Fr 7292/MPO Codex 1306 measures about 5.543 mm versus about 5.601 mm for the target mean. Staff pitch alone is not distinctive; one control does not estimate prevalence or establish a hand/book relationship. |
| H03 candidate written areas are close, but similar-size antiphonaries occur under other catalogue codex groups | [E24 report](RESEARCH_CONTINUATION_24.md), [query script and result](research/continuation_24/h03_layout_screen.py) | Fr 20274 and Fr 8994 are recorded at 36.0×22.5 and 35.5×22.5 cm. At ±0.5 cm, the same-genre subset also includes two Codex 1306 antiphonaries and three other Codex 1505 leaves. Catalogue dimensions support page-format compatibility, not a one-codex attribution or a rarity estimate. |
| Published sources describe several relationship levels for the Naantali-related fragments | [E26](RESEARCH_CONTINUATION_26.md), [E27](RESEARCH_CONTINUATION_27.md), [E28](RESEARCH_CONTINUATION_28.md), [E29](RESEARCH_CONTINUATION_29.md), [machine crosswalk](research/continuation_27/related_unit_crosswalk_results.json) | BOMPAC assigns Codex 1505/IV.156 to 5324, Ant 99/IV.157/Fr 1385 to 912, and IV.173/Ant 242/Fr 29666/Hy 49/Fr 25592 to 9531. Fragmenta explicitly distinguishes same-codex links from suggestions and describes IV.156/IV.157 as stylistically similar; Walta 2013 describes a wider group including IV.156/IV.157/IV.173, with multiple hands and uncertain production site. These are layered prior-art relationships, not a new attribution or proven contradiction. |
| BOMPAC already separates the three H08–H10 model suggestions from their Fr 1385 anchor | [E30 report](RESEARCH_CONTINUATION_30.md), [reproducible crosswalk](research/continuation_30/bompac_suggestion_crosswalk_results.json) | The combined workbook places Fr 4223/8311/8455 in BOMPAC-258 / Ant-39 / Codex-1200 / F.m.IV.159 and Fr 1385 in BOMPAC-912 / Ant-99 / F.m.IV.157; the related raw workbook similarly groups the candidates in C-17 and keeps Fr 1385 in F-1385. This is prior reconstruction data, not fresh image evidence or independent adjudication. It weakens the three model suggestions as new same-codex claims without proving physical incompatibility; all remain C. |
| Nordic cross-collection fragment integration is prior art | [BOMPAC/CODICUM audit](research/continuation_22/bompac_codicum_audit.json), [E26–E30 crosswalks](research/PRIOR_ART_LEDGER.md) | Do not present broad catalogue integration as this project's original contribution. The BOMPAC row assignments are published reconstruction data, not fresh image evidence or independent adjudication. E30 further explains the H08–H10 high-scoring suggestions as lookalikes assigned to a different reconstructed unit from Fr 1385; the cases remain ambiguous. |

## Correction: Fr 28175 was not absent

The first report incorrectly said **Fr 28175 was absent from the export**. A direct identifier search found it. The earlier extraction selected only records with `codex == Codex 1104`, which omitted this row because that field is blank.

The actual row has **CCM Sequ 42**, two leaves, a fifteenth-century date and contents for Laurentii/Mariae assumptio/Mariae nativitas; it has no viewer/IIIF URL. [Direct record evidence](research/goal_identity_crosscheck.json).

This is a corrected research error and an important methodological result: **missing from a codex-filtered result is not missing from the collection or export**. The catalogue's seven-member Graduale Aboense list can be reconciled at record level; image availability remains incomplete. No new leaf was discovered.

## Actual diagnostic outcome

The [reproducible metadata diagnostic](research/metadata_retrieval_diagnostic.py) was rerun locally. It uses full exact-type galleries, hides relationship fields and preserves tie ranks. It was selected retrospectively and is not an AI benchmark.

| Known comparison | Observed result | Interpretation |
|---|---|---|
| 7960 → 7961, documented same book/continuity | Maximal compatibility, leading tie positions 1–4 of 792 eligible gradual records | Known positive can be shortlisted; not uniquely identified |
| 8343 → 8344, documented same book/continuity | Maximal compatibility, leading tie positions 1–7 of 792 eligible gradual records | A top-5 claim would depend on arbitrary tie order |
| 8201 → 20106, published compatible same-book comparison | Excluded for missing fields from the 1,221-item eligible antiphonal gallery | Complete-case filtering loses a known positive |
| 8201 → 8304, published different-book comparison | Maximal compatibility and **unique rank 1** | The baseline fails a documented hard negative |

The source galleries contained 1,321 other gradual records or 2,099 other antiphonal records before complete-case filtering. No assumptions were made about the unknown relationships of other gallery members. No corpus precision/recall, image accuracy, independent-book generalization or calibrated probabilities are supported. [Detailed audit](research/goal_validation_audit.md).

## New target-specific image examination

Four exact Swedish target images were retrieved at 600-pixel width, decoded and visually inspected on 20 October. Total successful transfer, including four manifests, was **216,487 bytes**.

- **Fr 1385:** chant text, red staves, square notation, an initial, damage/folds and a ruler are visible. The capture does not establish original full-leaf dimensions.
- **Fr 20274:** readable chant layout and coloured initial; the supplied view covers only part of the physical area. Do not infer the whole-book ruling count from this one capture.
- **Fr 8994:** actual Codex 1505 comparison image, with large music/text layout, red staves, rubric/initial, ruler and folded lower portion. Resemblance to the comparators is not evidence of a new identity.
- **Fr 25592:** the actual image visibly has **two text columns with interspersed music**, unlike the large one-column chant-page samples. This supports taking the catalogue's layout conflict seriously; it does not independently date the fragment or adjudicate the proposed relationship.

[Actual URLs, statuses, bytes and hashes](research/target_access_log.json). The four manifests identify Public Domain Mark. Larger originals and all capture sides were not downloaded.

## Rejected or downgraded hypotheses

1. **“Cross-border integration itself is new.” — Rejected.** BOMPAC already integrates Stockholm/Helsinki and CODICUM already pursues reunions/virtual books.
2. **“A missing codex field denotes an unknown separate book.” — Rejected.** Fr 28175 directly contradicts this inference.
3. **“Maximal metadata compatibility is persuasive same-book evidence.” — Rejected as a sufficient rule.** The published negative 8201–8304 receives the top score.
4. **“Complete-case filtering is harmless.” — Rejected.** It removes the documented positive 20106.
5. **“A named suggested relation can be used as a positive training label.” — Rejected.** IV.173–Hy 49 has date/layout conflicts, and E27 shows that current catalogue suggestions and BOMPAC unit membership must be kept separate. Expert review is not required to continue the provisional source tests but remains useful for a final adjudication.
6. **“The antiphonal resemblance has just been discovered.” — Rejected.** The catalogue already cites Taitto and Keskiaho; a directly relevant later chapter exists.
7. **“One reconstructed codex validates general AI matching.” — Rejected.** Beauvais is a positive control with domain/rights/capture issues, not a standalone multi-codex discrimination benchmark.

## Important unverified matters

Keskiaho's *En grupp handskrifter från Nådendal: nya rön*, pp.51–67, is identified but unread. The publisher dates the volume 2018; the author's institutional chapter record dates it March 2019. Its conclusions must not be guessed. [Publisher](https://www.medievalia.nu/publikation/cederbom-ferm-nystrom-2018/); [author bibliography](https://researchportal.helsinki.fi/en/publications/en-grupp-handskrifter-fr%C3%A5n-n%C3%A5dendal-nya-r%C3%B6n/).

Current expert agreement, the Turku Ms. c holder/extent, Finnish measurement conventions, independent benchmark labels, and the original-research status of the target remain open. No scholar was contacted. These are explicit conditions on the next phase, rather than reasons to claim an undocumented association.

## Decision

**CONDITIONAL GO for an attribution/exclusion audit of the IV.157-centred family.** The evidence justifies a small source-led investigation. It does not justify an announcement of a newly recovered book or a claim that AI matching is validated. Full reconstruction remains subject to user approval.
