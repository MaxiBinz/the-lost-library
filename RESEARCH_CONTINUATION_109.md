# E109 — masked image check and practical impact of the column discrepancy

**4 November 2026.** Follow-up to [E108](RESEARCH_CONTINUATION_108.md): the research dataset issue remains distinct from a medieval codex attribution. This is an internal quality check, not independent expert review.

## A bounded, identity-masked image check

Using the previously retained local photos, we selected with seed `20261104` six cases where raw MPO says one column and the combined workbook says two, plus three agreement cases. Previously viewed E108 examples Fr 607, Fr 8994 and Fr 25592 were excluded. After those exclusions the eligible local pools comprised 60 mismatch cases in this direction and 35 agreements; no additional local case in the opposite mismatch direction met the image and metadata criteria. These are convenience pools of existing images, not a representative sample of the full collection.

The [selection script](research/continuation_109/prepare.py) stored the identity and expected values and presented nine source files under shuffled letter-only symlinks. The [image readings](research/continuation_109/blind_observations.json) were saved **before** the identity mapping was opened. The reader knew the 6-to-3 sampling scheme and had previously worked with some project images; this was identity-masked, not fully blinded or independently reviewed. No new images were acquired, and the symlinks did not create derivatives.

| Selected cases | Outcome on the visible capture |
| --- | --- |
| Six raw-one / combined-two disagreements | Four (Fr 4473, 6360, 6779 and 8343) show one main field, provisionally consistent with the raw value; two (Fr 2863 and 3872) are unassessable because of cropping or damage. |
| Three agreements | Two (Fr 4983 and 641) show one main field, consistent with both records; one (Fr 8694) is unassessable. |

These observations concern the **visible photographed surfaces**, not all sides or the entire original codices. Some readings are tentative; obscured or cropped material remains uncertain. The sample has no independently evaluated opposite-direction cases; the previously inspected Fr 25592 remains a selected example in that direction. The source-to-label mapping and image hashes are in [selection.json](research/continuation_109/selection.json); `.venv/bin/python research/continuation_109/score.py` checks those hashes and reproduces the outcome. Agreement controls happen to be one-column examples in this sample; they do not test sensitivity to two-column views.

## Illustration of analytical impact

Within E108's fixed subset of **14,415 included MPO records** with exact unique raw joins and both values equal to 1 or 2, the raw records give one column for **2,738 (19.0%)**; the combined field gives one column for **4,706 (32.6%)**. That is a **13.7 percentage-point difference** in this selected subset. These are fragment records, not separate medieval books, and the raw descriptions are not automatically correct. The population excludes missing, nonnumeric, other-valued and nonmatching records; do not generalize the percentages to the full corpus or published historical conclusions. We have not established that any particular published analysis used the affected field.

The offline E108 audit also emits [5,598 disagreement candidates](research/continuation_108/disagreement_candidates.csv) with both source row and cell references. This is a **review list**, not 5,598 individually proven errors or a corrected catalogue. The sources and data licence remain credited in E108. Two targeted official Zenodo latest-version endpoints had already failed and were not retried; a newer correction or an earlier notice remains possible. No external correction, request or publication has been sent.
