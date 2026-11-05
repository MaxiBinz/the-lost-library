# Published-method application: orientation, calibration and reconstruction

22 October 2026, Europe/Vienna. Local AI research pass. No specialist endorsement or new historical attribution is claimed. The controlling research goal was read before execution.

## Source actually read

William Duba, “Finding the Prior Leaf: Manuscript Fragments and Original Codices,” *Fragmentology*6 (2023), pp.5–65, DOI[10.24446/j9en](https://doi.org/10.24446/j9en). [Official article record](https://www.fragmentology.ms/article/view/4499).

The journal's article PDF endpoint could not be retrieved because of TLS transport failures; no body data were received and there was no access-denial bypass. An official [Fragmentarium full-issue mirror](https://fragmentarium.ms/uploads/descriptions/F-u1fn/62301/Fragmentology_6_FullIssue.pdf) returned200. After the parent increased this internal task's cap from8MB to27MB, one26,149,638-byte PDF was acquired. SHA-256:`daa2a0a3ecebfeb40788a64f0313079ad8379612db565889fbb4e5772c7009af`.

The complete article text was read: printed5–65 = PDF7–67. Selected methodological pages24,43,63,64 were rendered and visually inspected. The full-issue PDF, extracted text and page/ruler previews remain private reading materials and are excluded from release; receipts preserve all attempts. No source manuscript image was acquired by this subtask.

## What the publication supplies

The article separates present fragment order from the original codex's structure (pp.7–21/PDF9–23). Orientation uses text, folds, binding and paratext, with later reuse potentially confusing those clues. Layout extrapolation requires a matching reference text and calibrated measurements (pp.23–44/PDF25–46). Its small pseudo-fragment experiment exposes errors from unsuitable editions and ambiguous measurement instructions (pp.34–38/PDF36–40). Missing-leaf and gathering reconstructions add further assumptions (pp.44–58/PDF46–60). The appendix explains physical image calibration and common-scale comparison (pp.61–64/PDF63–66).

These are published methods available for us to apply ourselves. They are not an automatic same-book classifier, and their empirical error ranges are not a validated tolerance for our Nordic chant fragments.

## Concrete source correction: the scaling ratio

Printedp.64/PDF66 contains an internal discrepancy. Its prose instructs multiplication by the lowest scale divided by the current scale, `Smin/Sn`. The displayed formula reverses that ratio to `Sn/Smin`. The discrepancy was checked on the rendered page, rather than inferred from extracted mathematical text.

Our dimensional derivation is straightforward. An object of length`L` photographed at`Sn`pixels/mm has width`W=L*Sn`. At the common scale`Smin`, its target width must be`L*Smin=W*Smin/Sn`. Using the displayed reciprocal enlarges the higher-resolution object instead of bringing it to the common lower scale.

The executable[method_checks.py](method_checks.py) tests three analytic controls. Equal scales pass either expression, so that control alone would miss the error. At8pixels/mm, an800pixel object is100mm long; at4pixels/mm it must become400pixels. The displayed reciprocal makes1600pixels, representing400mm at the intended common scale. A second unequal-scale control produces the same contradiction.

**Classification:** a reproducible implementation correction / possible typographical erratum in an adopted method. This is not a new medieval attribution, and we have not established that the discrepancy has never previously been noticed or corrected.

## Application to the existing research queue

The current frozen queue references12records,11imaged physical objects and nine pairs with images for both objects. The audit verified hashes for42stored capture files in those queue records, including two newly added resolution variants of Fr20274. The variants share existing canvas identifiers and are not additional source photographs or medieval sides. The frozen selection itself is unchanged.

The Fr20274upper/lower photographs were visually rechecked against their existing overlap annotations. Their shared writing area supports treating them as overlapping views. A sequence from image1toimage2 is therefore not a demonstrated recto-to-verso transition. Its original side designation remains unresolved; no missing-leaf count or new association follows.

The source's calibration method supplies a productive next task. Each photograph should have its own ruler-based scale, validated at distant intervals and, where possible, on both axes. An exploratory ruler-crop inspection was performed, but exact tick selection and perspective uncertainty were not settled sufficiently to publish a physical measurement. Consequently this pass reports no millimetre staff spacing or inferred original dimensions. Preview markings are exploratory and are not measurement evidence.

The full per-object and per-pair outputs, formulas, derivation, analytic controls, source page map and an eight-step local protocol are in[protocol-results.json](protocol-results.json). Regenerate that file with:

```sh
.venv/bin/python research/independent_pass/methods/method_checks.py
```

Run from the project root. The queue inventory is a dated snapshot: later capture additions can legitimately change its counts and fragments-file hash.

## Remaining method-specific limits

A chant's syllables and words do not occupy a constant amount of musical space. Melismas, rubrics, initials, missing music and differing notation density could break a character-count extrapolation even when an edition identifies the right office. We therefore require validation on the actual genre and layout before using text length to calculate the missing pages of an antiphonal. We do not import prose-manuscript accuracy claims as guarantees for music manuscripts.

Other explicit restrictions are unchanged: photographs do not alone identify hair/flesh sides; reuse holes do not automatically identify original binding; common chants and similar ruling do not independently identify one codex. No current dossier category is promoted by this method check. These limitations concern particular inferences and do not require stopping the remaining source research.
