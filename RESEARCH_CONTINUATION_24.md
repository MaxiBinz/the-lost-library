# Research continuation E24: a catalogue-matched H03 layout check

**Date:** 24 October 2026. **Scope:** test whether the close written-area values recorded for Fr 20274 (Ant 99) and Fr 8994 (Codex 1505) are unusual among comparable entries in the pinned MPO catalogue. This is an exploratory source-metadata check for frozen hypothesis H03, not a new hypothesis or independent measurement of the manuscripts.

## Result

The MPO record gives both pages nearly the same written-area size: Fr 8994 is listed as **35.5 × 22.5 cm**, and Fr 20274 as **36.0 × 22.5 cm**. Both are catalogued as fifteenth-century antiphonaries with four-line Quadr notation. Fr 8994 has 11 text rows and a recorded Textualis script; Fr 20274's row field is `11 (33)` and its script and leaf format are blank. This difference in how the row count is written was handled explicitly: the query accepts a leading 11, so it includes both `#11` and `11 (33)`.

The query verified the pinned 22,909-row MPO CSV by SHA-256. It found 244 entries with Quadr notation, four staff lines, and a leading main-text row count of 11. Written-area dimensions are parseable for 154 of those records. The genre-matched subset contains 97 Antiphonaria, with dimensions for 52.

The bounding box formed by the H03 pair itself is narrow: 35.5–36.0 cm wide and exactly 22.5 cm high. That box contains only the pair, but this is mechanically guaranteed by how the box was defined and says nothing about rarity. When expanded by 0.5 cm in each direction, it contains seven dimensioned Antiphonaria: the H03 pair, two entries labelled Codex 1306 (Fr 7292 and Fr 9165), and three other Codex 1505 leaves (Fr 10370, 10406 and 10407). At a 1 cm expansion, Fr 9690 also enters the box. In the broader Quadr/four-line/11-row cohort, an unrelated Graduale OP also fits the 0.5 cm box.

This result supports a modest statement: the H03 pair is compatible with a closely similar page design, and its catalogue dimensions are close. The sensitivity comparison also shows that similar page-area values occur across catalogue codex groups. Neither result can identify a single book. It is not an estimate of how rare the layout is because the catalogue's measured subset is incomplete, non-random, and drawn from the same source that records the existing associations.

## Effect on H03 and next evidence

H03 remains **C / unresolved**. The metadata screen does not establish that Fr 20274 and Fr 8994 are leaves from one codex, the same hand, or a shared workshop. It also does not refute the existing suggestion. The source records differ in available detail: Fr 20274 lacks a whole-leaf size and script description, and neither representative capture set is a complete physical-side inventory.

The next useful evidence for this specific pair is therefore not another coarse size comparison. It is a source-linked reading of any genuinely corresponding liturgical passages, exact foliation or quire/catchword evidence, and a controlled comparison of letterforms and ruling across original images. The relevant Taitto discussion (2001, pp. 161–168 as cited by the Fr 8994 record) remains unread; the access routes already tried are recorded in E23, and a new route should be pursued only if it is genuinely different and legitimate.

The executable [screen](research/continuation_24/h03_layout_screen.py) writes the [machine result](research/continuation_24/h03_layout_results.json). No image was downloaded, no hypothesis or queue item changed, and the frozen queue SHA remains `b3e299a7c600584ce44518db1f5c30c3301edae0a07a8b009075498f64ccec47`. The result is integrated as context check CTX08, outside the frozen queue and model predictors.
