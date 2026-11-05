# Fr 10370: intrinsic text order across two photographed regions

23 October 2026. This is a provisional AI source reading, not independent expert review. No new source image was downloaded and no frozen hypothesis was changed.

**New result:** the final written row of photograph 2 and first written row of photograph 3 form the prefix and suffix of one candidate responsory verse. This supplies textual evidence for **2 → 3** reading order, where the previous pass only had uncertain capture/side mapping.

| Photographed region | Literal candidate reading | Proposed normalization |
|---|---|---|
| [Image 2](../../../data/images/mpo-10370-capture-2-1739px.jpg), xywh `650,490,740,115` | `[A]rdore caritatis succensa quē` | Ardore caritatis succensa quem |
| [Image 3](../../../data/images/mpo-10370-capture-3-1728px.jpg), xywh `345,330,1155,85` | `sepultum nouerat sublatum cred[ens?] de se pul chro` | sepultum noverat sublatum credens de sepulchro |

The bar on `quē` is expanded explicitly to *quem*. The reading *credens* is less secure than the surrounding words and is informed by the parallel; the literal field preserves that uncertainty. *Nouerat* is normalized to *noverat*, and divided syllables to one word. The manuscript's proposed *sepulchro* is retained; the database's standardized *sepulcro* is a separate normalization.

Cantus Database records identify the combined passage as **601029a**, a Matins responsory verse for Mary Magdalene. Complete text was available through public search indexing of [F-Pn Latin 12044 f.165r](https://cantusdatabase.org/chant/402240/), [Wrocław R 503 f.163r](https://cantusdatabase.org/chant/564421/) and [Cambrai 38 f.291v](https://cantusdatabase.org/chant/204152/). No direct Cantus HTML body or comparator manuscript image is claimed. These are concordances in different books, demonstrating why the verse is not a unique codex fingerprint.

The preceding material in image 2 is compatible with the parent responsory *Hic certe praecipuus Mariae Magdalenae*, candidate **601029**, for which the verse is attested. This contextual check helps distinguish a verse continuation from an arbitrary match to a common word. It does not establish exact melodic identity. See the [Cantus responsory record](https://cantusdatabase.org/chant/402239/).

## What this changes

The textual prefix ends the visible written area of image 2 and its suffix begins the visible written area of image 3. Five prefix words followed by eight suffix words agree with the reference after the explicit normalizations. Reversing these two selected regions fails to form that verse. The executable check records this correspondence; the assertions test transcription bookkeeping, not historical truth or OCR accuracy.

Together with the earlier proposed association of photographs 1/2, the result supports a numeral-bearing surface before the k-bearing surface. Given the catalogue's assertion that these photographs belong to one original leaf, this is consistent with the Finnish convention of a numeral at medieval recto and letter at verso. It strengthens a relative-order argument without independently proving all the physical premises. It does not establish what MPO's `1r`/`1v` labels mean.

The existing description already places this leaf between Helsinki IV.157 ff.7/8. That placement remains credited prior evidence. The new local observation is the explicit verse continuation and its source regions; no claim that this text order has never been observed before is made.

## Alternatives and limits

- Repeated chants or an unrecognized photographic rearrangement could defeat a simple adjacency inference. This small comparison does not exhaust those possibilities.
- No registered pixel overlap or physical seam has been established, especially for photographs 1/2 or 3/4.
- The analysis supports relative text order. It does not provide a new book attribution, a proof of MPO catalogue error, a general side-label rule, or independent expert confirmation.
- The readings and comparison were developed after inspecting the selected sources. They are descriptive evidence, not a blind predictor or independent accuracy test.
- Scientific originality remains uncleared. A known chant and known prior placement are not a newly discovered historical relationship.

Run `.venv/bin/python research/continuation_20/intrinsic_10370/check_order.py` from the project root. It validates source hashes and bounds, creates two image-region annotations, checks the explicit forward/reverse transcription comparison and verifies that the frozen queue SHA has not changed. The structured [results](results.json) and [annotations](observations.json) retain exact provenance. Analysis crops duplicate existing source pixels only.
