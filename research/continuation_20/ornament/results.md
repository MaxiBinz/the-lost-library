# Controlled letter comparison: H02 ornament

23 October 2026. Provisional AI source inspection; no independent expert review. This pass acquired no source image, changed no predictor or threshold, and left the frozen ten-pair queue unchanged. It adds a same-letter check to the earlier comparison, whose selected letters differed.

**Result:** Fr 1385 and Fr 10406 have candidate A initials with a closely related ornamental vocabulary. Selected Ant 39 A forms differ. This gives a more specific local description, but it does not establish a unique feature, a common hand/decorator or one book. Exact liturgical function remains incompletely matched, and the known wrong-book control repeats the broader vocabulary in a different letter class.

## Scope and selection

All four existing derivatives for each of Fr 1385, 10406, 4223, 8311, 8455, 8201 and 8304 were screened: 28 files. Their hashes and image dimensions were checked. The first interpretable large ornamental A candidate in capture order was selected where available; auxiliary comparisons use the first clear R in 1385/8455 and the first clear *De…* D in 8201/8304. This rule was applied after viewing the sources, so the selection is exploratory, neither blind nor preregistered.

Small text capitals, plain filled blue/red display initials, other letter types, partial/damaged forms and uncertain forms were excluded from strict same-letter comparison. The lower-edge primary 4223 initial is partial, so the complete capture 3 candidate is used. No clear complete large A was selected in the four 8455 derivatives and no large R in 10406; neither is a claim of absence from the medieval book. A large 10406 capture 4 form was not pooled with A because the letter/word interpretation was not secured. Full selection/exclusion inventory is in `results.json`.

The rubric and decorative role are retained as uncertainties. These are large ornamental initials adjacent to notation and chant text. Their exact antiphon/verse/hymn roles have not all been independently established. Same letter is a narrower control than the previous pass; it does not automatically make the liturgical function equivalent.

## Executed comparisons

| Letter and source | Visible result | Consequence |
|---|---|---|
| A: Fr 1385 capture 4, *Auertantur…*, and Fr 10406 capture 3, *Ades…* | Both have pale body fields, a long red stem stripe, small lozenges and a toothed dark left edge. The 1385 lower lozenge appears dark; 10406's is red. Their right body/crossbar arrangements differ. | The earlier resemblance survives candidate letter matching. Variation within a book remains possible; neither resemblance nor these differences decides identity. |
| A: Ant 39 Fr 4223 capture 3 and Fr 8311 capture 2 | The 4223 candidate has a large upper loop and narrow patterned upright; 8311 has a compartmented/lattice-like crossbar and long lower flourish. Comparable long red-filled stems and paired simple lozenges are not securely visible. | A local contrast with the H02 samples. Two selected controls, uncertain full incipits and unmatched exact roles cannot establish rarity or exclusivity. |
| R: Fr 1385 *Rex…* and Ant 39 Fr 8455 *Reges…* | Both have pale spaces and toothed dark contours. A red stem fill and lozenges are not securely visible in the 8455 sample. A verse-like marker precedes that example. | The richer H02 trait combination is not shown in this R control, but exact function equivalence is unproved. There is no H02 same-R pair because no suitable 10406 R was selected. |
| D: Fr 8201/8304, each *De…* | Both have a red stem, pale right body, small lozenge-like marks, parallel bars and a scalloped dark left border. This is the existing published same-hand/different-book pair. | The general red/pale/lozenge/scallop vocabulary fails to distinguish that known wrong-book pair even with letter identity controlled. These D forms are an auxiliary test, not an A-specific counterexample. Their exact local roles also need confirmation. |

The D forms were initially mistaken for A during inspection. Checking their following *e* corrected that reading before the final annotations were created. The R in 8455 was likewise not scored as having a red stem merely because another 8455 initial has one. These corrections matter: pooling different letters or borrowing a feature from a different glyph would make the target appear more or less distinctive without source support.

## Traceability and interpretation

`observations.json` contains eight region annotations with exact source endpoints, SHA-256 hashes, pixel selectors, literal candidate contexts and limits. `matched-letters.png` shows selected original pixels; enlargement and arrangement add no detail. The seven overview sheets retain the screened captures for the selection audit. Letter readings remain provisional; full chant identifications are not supplied or silently completed.

The published 8201/8304 decision comes from the existing [Grajewski study](https://doi.org/10.25167/ls.4818), read and documented in the parent investigation. Agreement with that reference is not an independent attribution result. The A samples in H02 are themselves unresolved candidates, so they cannot serve as a labelled same-book training set.

Run from the project root:

```sh
.venv/bin/python research/continuation_20/ornament/analyze.py
```

This checks all 28 source hashes/dimensions, validates all eight region selectors using the existing evidence validator, regenerates the original-pixel sheets and reproduces the structured manual-observation table. It does not automatically recognise initials or validate the observer's interpretation.

## Next test justified by this result

Verify complete incipits and local rubrics to match exact decorative roles. Then compare multiple occurrences of the same A in actual known same-book and known same-hand/different-book material. That would test whether the right-body construction, lozenge placement or contour vocabulary helps distinguish production from identity. Text succession, complete opening signatures and physical evidence remain separate channels. No A/B promotion, new attribution, scientific novelty or method-accuracy claim follows from the current samples.
