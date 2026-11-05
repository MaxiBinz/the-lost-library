# E21 — calibrated staff-pitch and catalogue-layout check

**Date:** 24 October 2026  
**Scope:** Existing Codex 1505 grouping, Fr 10370 and Fr 10406; no new relationship hypothesis.  
**Status:** Exploratory, source-linked and reproducible. The frozen ten-pair queue and baseline remain unchanged.

## Result

On two inspected photographs, the four red music rules are spaced about **5.6 mm apart** in both Fr 10370 and Fr 10406. The selected Fr 10370 groups measure 5.584 and 5.651 mm; the three selected Fr 10406 groups each measure about 5.586 mm. This is a close layout agreement between two fragments already catalogued as members of Codex 1505. It is a consistency check, not a new attribution.

The full MPO catalogue shows why this agreement cannot establish identity by itself. The pinned 22,909-record export contains 9,196 records described as four-line Quadr notation. Of those, 197 also record 11 main-text rows, and 149 of those give a parseable written-area size. Three *other* records fall inside the exact written-area range of the five Codex 1505 leaves tested here; ten fall within a broader box extending the target range by 1 cm on each side. One exact-range record is Fr 1385, which the catalogue already cites as a comparator. These are catalogue data, not independently remeasured leaves or a random sample.

So the physical layout supports “these two leaves could share a page design,” but the same broad design occurs elsewhere. The catalogue grouping remains prior evidence, and the new measurement does not independently prove it.

## Reproduction

Run from the project root:

```sh
.venv/bin/python research/continuation_21/ruling_pitch_check.py
```

The script verifies the exact SHA-256 of the source images and both the MD5 and SHA-256 of the pinned MPO CSV, records all ruler and staff-line coordinates, and recomputes the millimetre estimates and catalogue counts. It creates `ruling_pitch_results.json`.

For Fr 10370 capture 3, the manually selected vertical ruler endpoints are the 0 and 20 cm marks at image rows 86 and 1077. The two four-line groups use rows `[407, 434, 462, 490]` and `[566, 594, 622, 650]`. For Fr 10406 capture 4, the 20 and 0 cm marks are at rows 51 and 600; three groups use `[153,168,184,199]`, `[244,258,274,290]`, and `[337,353,368,383]`. Coordinates start at the top-left of each original stored JPEG.

The MPO filter is literal: `notation` begins with `Quadr`, `notenlinien` equals `4`, and `zeilenzahl1` equals `#11`. The exact size range is the min/max written-area range of Codex 1505 records 8994, 10370, 10406, 10407 and 10437: **34.0–36.0 × 22.5–23.0 cm**. The sensitivity range adds 1 cm in every direction. Comparison counts exclude entries labelled Codex 1505.

The official MPO deposit describes the `notation`, `notenlinien`, main-row and written-area fields and gives this source export as version 1.0.0 ([Zenodo dataset record](https://zenodo.org/records/17287665)). The local CSV is 22,909 rows; its checksum matches that deposit. The source dataset itself already contains the Codex 1505 association, so its metadata screen cannot serve as independent confirmation of that association.

## Limitations

- Image regions and coordinates were selected after viewing the photographs. This was not blind, preregistered or independently repeated.
- Ruler endpoints and staff-line centers are manually selected. Approximate ±1 px line-center and ±2 px endpoint uncertainty is retained; perspective, page warping and ruling waviness are not corrected.
- The CSV's 149 dimensioned records are an incomplete, non-random subset of the 197 records with the specified notation and row count. The three and ten matches describe this query only; they are not a rarity estimate.
- The established different-book control Fr 8201/8304 is not a like-for-like Quadr / four-red-rule control: its catalogue identifies Gothic notation and three black plus one red staff line. It remains a useful warning against treating general layout or decoration as a unique book fingerprint, but it is excluded from the matching layout count.
- No hand, workshop, provenance, parchment source, codex identity or new historical finding follows from these measurements.
