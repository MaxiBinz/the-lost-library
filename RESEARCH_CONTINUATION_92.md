# E92: Direct Swedish image check of a catalogue-width contrast

**3 November 2026.** E91 made progress by identifying the reported written-area mismatch and recording the unavailable metadata routes. This pass tests the Swedish side of that comparison directly against its retained photograph. It does **not** inspect the Finnish original.

## A visible lower bound

On [Fr 10370 photograph 3](data/images/mpo-10370-capture-3-1728px.jpg), the same medieval text line contains visible writing at selected interior x positions **400** and **1400**. These are not the full line's endpoints: writing extends beyond them. On the same photograph, manually selected ruler marks for **1 cm** and **21 cm** lie at x positions **118** and **1100**. Under a simple common-scale assumption, the selected writing positions are approximately **20.37 cm apart**. Thus the apparent line occupies at least that much horizontal distance in this image; it is not a complete measurement of the page's written area.

As a sensitivity illustration, moving the two selected writing positions **20 pixels inward each**, and the two ruler points **4 pixels outward each**, gives approximately **19.39 cm**. These point adjustments were chosen for an exploratory robustness check; they are not measured errors, a confidence interval, or a correction for perspective, curvature, camera optics or ruler placement. The text and ruler may not lie exactly in the same plane. The horizontal scale of about 49.1 px/cm is similar to the 49.55 px/cm vertical ruler calibration previously recorded on this same photograph in [E21](RESEARCH_CONTINUATION_21.md); these are not independent measurements of a second object.

## What can be inferred

The published BOMPAC row for **II.64 ff.6–7** gives a written-area width of **18.5**; E91 treats the value as centimetres while noting that the combined readme did not explicitly state units. If the Finnish value is centimetres, applies to the particular relevant leaf and was measured comparably, the Swedish photograph's selected line is wider even under the stated point shifts. This is additional Swedish image evidence against an uncomplicated one-to-one physical alias; it is **not a Finnish measurement or a proof of different medieval books**. The II.64 inscription-bearing leaf, actual layout, field boundaries and possible composite structure are unresolved. A direct comparison of complete original surfaces and a source-specific account crosswalk remains necessary.

The image, positions and target were already known when selected: this is an unblinded AI observation, not an untouched test or independent review. The two image regions and coordinates are recorded in [observations.json](research/continuation_92/observations.json), with calculations and uncertainties in [results.json](research/continuation_92/results.json). They are views of the **same existing image**, not new fragments or independent corroboration. No new manuscript image, acquisition, attribution, physical exclusion, catalogue correction or discovery is claimed; the frozen decision states remain unchanged.

```sh
.venv/bin/python research/continuation_92/measure.py
```

The script checks the source hash and annotation bounds and reproduces the calculation. It does not verify manually chosen points, the optical geometry or the Finnish catalogue value.
