# Visual-source tests: a limited falsification pass

22 October 2026. Observer: a Codex AI agent, not an independent expert. No source image was acquired by this agent. Existing images were inspected directly; all four Fr 10370 higher-resolution views acquired centrally were subsequently inspected. The frozen pair queue and classifications were not changed.

## 1. Fr 10370: upper-margin signs and a conditional side test

Updated after central acquisition of all four higher-resolution views. The1700-pixel first photograph has a red upper-margin sign with two main strokes, the second descending/curving. Candidate reading **ij**, compatible with the catalogue's normalized **II**. Exact source: `data/images/mpo-10370-capture-1-1700px.jpg`, SHA-256 `07efe2e1f8f87f31156630a7fe5340f78600c78ddc31d7fad930e5ae81f8a409`, xywh `754,77,100,85`.

A **k-like red upper-margin sign is now directly visible** on image 3: `data/images/mpo-10370-capture-3-1728px.jpg`, SHA-256 `b1258668d90ca011960ab4ff85f25fb79c0c3c636ad626ceb4fa90af8f6de28b`, xywh `780,114,155,105`. This supersedes the earlier statement that k was unobserved. The k-bearing view has different uppermost music/text from the numeral-bearing view. Both readings remain provisional AI observations.

The source record describes one leaf and assigns `1r:k;1v:II`. Our images now support the existence of both kinds of mark, but **do not independently determine the medieval recto/verso assignment**. Under the Finnish Roman-on-recto/letter-on-verso scheme, the inferred side labels reverse the Swedish catalogue's labels. That is a concrete conditional source-label/convention conflict. Differing catalogue orientation, a mistaken label, marking variation or different books remain alternatives. It is not, by itself, an exclusion of same-book membership.

### Capture seams: avoid a stronger claim than the pixels establish

The bottom of image1contains the upper portion of a large pale/grey ornamental initial. The top of image2contains a complementary lower initial portion and following text. These are **consistent with successive partial views of the same writing surface**, but this check has not registered a pixel overlap or securely identified a complete shared text row. The prior wording “overlapping writing area” was too strong and is qualified here. Image ordinal cannot establish opposite sides.

Candidate correspondence regions: image1xywh `234,1290,1179,127`; image2xywh `232,25,1163,100`. Image 2 source is `data/images/mpo-10370-capture-2-1739px.jpg`, SHA-256 `fe8019fd85f078f5f552e9aa4befbae21bee8522506a1f77385d032a0499ee58`.

Images3and4were also inspected directly. The lower image3initial is a tall two-compartment form at the right; image4begins with a different broad B-like initial closer to the centre. I could not establish a literal shared text row or exact seam. **No 3/4overlap or complete stitch is claimed from their order.** Image 4 source is `data/images/mpo-10370-capture-4-1742px.jpg`, SHA-256 `2f2d35bf4253989714fda7877403a48bc4cd58bffa2e893469968546a9c1594f`; inspected upper band xywh `300,0,1180,190`.

**Falsification outcome:** the ordinal-only procedure “image1is recto, image2is verso” is unsupported. The sign-to-side claim can now be tested using the actually visible II/ij and k marks, while distinguishing source labels from an independently reconstructed orientation. Secure textual order, physical folding/binding relationships or other intrinsic orientation evidence is the next test.

The Fr 1385primary photograph contains a small red upper-edge mark at xywh `270,30,90,48`, but it is clipped. I cannot independently read IX versus D from those pixels. No isolated old foliation mark was securely identified in the four available Fr 10406captures. Later cursive account annotations must not be substituted for medieval foliation.

## 2. H02: ornament is more specific than broad layout, but remains non-identifying

Two selected Fr 1385 initials and two Fr 10406 initials share a concrete ornamental vocabulary: pale/grey areas, a longitudinal red shaft stripe, small lozenges and a dark/scalloped outer contour. Exact sources/regions are in `observations.json`; `initial_comparison.png` shows unchanged pixels enlarged with nearest-neighbour sampling.

This is compatible with related production, but the frequency of the motif combination was not measured. The selected letters and their functions differ. I do not attribute an individual scribe or decorator. A long red/black stripe also appears in selected Fr 4223 and Fr 8455 initials, falsifying the idea that that simple feature alone distinguishes this target pair from the Ant 39 lookalikes. Fr 8311's sampled flourished/compartmented initial differs, but that is not a same-book exclusion: different letters and decorative roles can have different forms in one book.

## 3. H02: a reproducible ruling-scale incompatibility check

`measure_ruling.py` checks source hashes and measures four visually selected four-line staffs in each of the two second captures. The algorithm takes row means of R–G and selects the four strongest separated peaks. All resulting lines were checked visually by the AI observer. Full pixel windows and peaks are in `measurements.json`.

| Source | Mean interline pixels | Approx. pixels per numbered ruler interval | Normalized pitch | Endpoint sensitivity range |
|---|---:|---:|---:|---:|
| Fr 1385, capture 2 | 15.75 | 28.7 | 0.549 | 0.511–0.588 |
| Fr 10406, capture 2 | 15.50 | 27.8 | 0.558 | 0.519–0.599 |

Ruler anchors were read approximately from the source images. A numbered interval is **not certified here as a centimetre**. The ranges perturb staff endpoints by ±1 pixel and ruler anchors by ±4 pixels; they are deterministic sensitivity bounds, not statistical confidence intervals. Perspective, curved parchment, camera geometry and unequal light remain additional unmodelled error. Window/anchor selection occurred after viewing the sources; this is not a blind test or a new benchmark predictor.

**Falsification outcome:** no gross ruling-scale incompatibility was detected in these selected samples. Similar staff spacing supplies no unique identity, common hand, date or provenance. No score, threshold or reference metric was modified.

## 4. What the observations warrant

- A capture ordinal cannot be used as a folio-side assignment in the inspected Fr 10370material; II/ij and k marks are now both observed, with medieval side assignments still conditional.
- H02 has concrete compatible ornament/ruling observations, with explicit controls showing why a simple ornamental feature is not unique.
- A proposed foliation-scheme contradiction remains conditional until actual sides/text order are established.
- None of these observations establishes a new same-book association, a new exclusion, an individual hand or scientific originality. Category C remains appropriate for the unresolved comparisons.

## 5. Next tests we can conduct ourselves

1. Use the now-observed II/ij and k marks and associated text to test side order; keep catalogue recto/verso names distinct from independently derived orientation.
2. Establish text continuity/order rather than equating image ordinal and side. A shared initial or shared song alone cannot establish book identity.
3. Extend the full ornamental-motif comparison to all available relevant initials while controlling for letter identity/function, then report its prevalence in known same-book and wrong-book controls. Do not fit a rule to these five selected objects and call it validated.
4. Obtain calibrated higher-resolution views only if needed for repeated letterform ductus; current small glyphs do not support a defensible individual-scribe diagnosis.

`observations.json` contains 17 source/hash/bounds-verified annotations. The auxiliary Fr 10370 observations are contextual evidence for the target-family audit, not an eleventh frozen relationship. They should not be attached to a pair that does not contain Fr 10370 merely to satisfy an exporter. Analysis derivatives are excluded from the working source-image count.
