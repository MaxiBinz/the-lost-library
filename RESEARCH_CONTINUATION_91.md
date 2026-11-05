# E91: A catalogue layout check and an unavailable data route

**E92 follow-up:** An image-based Swedish interior text span is about 20.4 cm under a same-plane ruler assumption, and about 19.4 cm under specified illustrative point shifts. The Finnish measurement remains catalogue-only and the account-heading leaf unidentified. [E92](RESEARCH_CONTINUATION_92.md).

**2 November 2026.** E90 made progress by reading the retained Fr 10370 account heading and identifying a more specific comparison with Haapanen's II.64 description. E91 tests a counterpoint: are the two records physically and descriptively interchangeable?

## A difference in reported writing fields

The published, previously retained BOMPAC workbook records the following for the exact rows, including only rows marked `Include row`:

| Record | Published reconstruction | Record extent | Reported written area, height × width | Rows |
| --- | --- | --- | --- | --- |
| Fr 10370 | BOMPAC-5324 | 1 leaf | 36 × 23 | 11 |
| F.m.II.64, ff.6–7 | BOMPAC-11814 | 2 leaves | 24.5 × 18.5 | 9 |

The source fields describe **written areas**, not the complete size of the reused parchment or the size of the account booklet. These values are treated as centimetres, consistent with the source's corresponding MPO string and Haapanen's catalogue conventions; the combined workbook's general readme describes the measurement fields but does not explicitly spell out their units. The Swedish row retains the institutional `schriftraum1` value `36.0 x 23.0`. The values differ by **11.5** in reported height and **4.5** in reported width. These are published catalogue measurements, not fresh independent measurements from both leaves. Their exact measurement methods and whether the II.64 values were taken separately on ff.6–7 are unknown.

The two-leaf row is one catalogue fragment record, not proof that either leaf carries the provision heading. Haapanen's [1925 entry 64, p.39](https://www.doria.fi/bitstream/handle/10024/100895/Verzeichnis_der_mittelalterlic.pdf?sequence=1) describes these numbered leaves as Sunday material in a gradual; the retained Fr 10370 catalogue describes Mary Magdalene office material in an antiphonal. These are different reported contents, but the source descriptions are not exhaustive image transcriptions and the relevant Finnish parchment has not been examined.

Taken together, these differences are **counterevidence to treating the records as an obvious one-to-one physical alias**. They do not exclude related accounts, separate covers, a different relevant II.64 leaf, damaged or incomplete measurement, a catalogue mapping error, or a composite book. Nor does a writing-field difference by itself prove that fragments are from separate medieval books. We retain the account-heading comparison as unresolved and do not declare an attribution, physical exclusion or catalogue correction. The [checksum-verified workbook extraction](research/continuation_91/layout_comparison.json) and [script](research/continuation_91/compare_layout.py) retain the precise values and calculation.

## Access attempt

The latest official BOMPAC raw-metadata record identifies separately published fragment-level metadata, its field readme, and a bailiff-record dataset. These are potentially useful for identifying II.64's exact 1611 account. We made **one ordinary request for each of three distinct files**, using the exact published URLs and expected sizes/checksums from the retained [official release metadata](research/continuation_51/raw-latest.json). All three failed before response because the environment could not resolve the hostname; no files were saved and there was no access-control challenge. The [receipts](research/continuation_91/download_receipts.json) retain the exact URLs and errors. The acquisition script refuses to run again while the receipts exist. A normal web-reader attempt to screenshot two pages of the already indexed Haapanen PDF returned cache-miss errors; the printed catalogue was not visually checked and the screenshots were not retried.

The missing metadata and original II.64 images remain **access dependencies**, not historical evidence. A future comparison needs the inscription-bearing II.64 folio identified, original images or faithful full descriptions, and checks of the two copying fields and account identifiers. No downloaded manuscript image, new codex, same-account finding, physical exclusion or independent expert review resulted. The conservative working-image and transfer totals remain unchanged; unmeasured web-reader traffic is not an exact zero.

```sh
.venv/bin/python research/continuation_91/compare_layout.py
```

This checks workbook identity and arithmetic, not the truth, physical comparability or provenance of each catalogue measurement.
