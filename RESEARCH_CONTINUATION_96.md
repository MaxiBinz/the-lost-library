# E96: an existing IV.173 / Fr 11167 candidate receives a scale check

**3 November 2026.** The preceding E95 turn was no progress on a historical question. This pass returns to an existing, unresolved ranked pair, `pair-4da59b5404a8d883782b`. It tests a limited layout prediction rather than assuming either catalogue assignment is correct. The images, the catalogue and the approximate scales were seen before the points and test were recorded; the test is post-exposure and exploratory.

## Comparison

[Fr 11167's retained first photograph](data/images/mpo-11167.jpg) shows a notated antiphonary passage and a ruler. Four manually chosen four-rule music systems span **18.46, 18.79, 18.79 and 18.46 mm** after scaling by the photograph's 1–10 cm ruler marks. With illustrative changes of ±2 pixels at each staff endpoint and ±1 pixel at each ruler endpoint, individual spans range **17.02–20.26 mm**. These ranges test the stated coordinates only; they are not physical-error bounds or confidence intervals.

The [Finnish National Library's indexed IV.173 description](https://fragmenta.kansalliskirjasto.fi/handle/10024/1314) reports a **17 mm** four-line staff. The comparison assumes that value means the total distance from first to fourth rule, as in the project measurement; the catalogue's precise measurement convention, rounding and uncertainty require confirmation. The retained [IV.173 image](data/images/fm-IV173-1.jpg) has no photographed ruler. Its other face and the Fr 11167 image show different texts: IV.173 preserves part of *Te Deum*, whereas Fr 11167's catalogue describes the feast of the patrons of the Swedish realm. Different texts do not by themselves disprove a shared book.

An existing separately catalogued comparator, Fr 7292, yielded approximately **16.63 mm** across three staff intervals in [E22](RESEARCH_CONTINUATION_22.md). It demonstrates that a page from another catalogue group can fall close to the IV.173 value; it is not a verified positive control for IV.173 or a population sample. The Fr 11167 centres are larger than the reported Finnish number, but the illustrative perturbations nearly reach it, and page curvature, geometry, historical staff variation, crop effects and the measurement convention remain unknown. Only one low-resolution view of the two-leaf Fr 11167 object has been examined here.

## Decision

The source gives a **possible layout difference worth checking**, not a reliable same-book exclusion, positive match or scientific discovery. No distinctive corresponding text or physical join was found. The physical leaf, all Fr 11167 surfaces, a ruler-calibrated image of IV.173, and well-established within-book controls would be needed before the distance could bear more strongly on identity. IV.173's accepted/suggested catalogue links and BOMPAC group remain prior assertions, not confirmations of this pair. First notice is unassessed and the relevant scholarship remains partly unread.

The [measurement inputs](research/continuation_96/measurement.json) retain the exact photograph, ruler points, four staff endpoints, source checksum, assumptions and control. Recompute the numbers offline with:

```sh
.venv/bin/python research/continuation_96/check.py
```

The checker verifies the file hash, dimensions, coordinate bounds and arithmetic; it does not validate the selected lines, historical object dimensions or book relationship. No new source image or download, contact, upload or publication occurred. Frozen reviews and model results remain unchanged. The goal remains active.
