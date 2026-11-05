# E36: Source-linked Aboense continuation controls and actual capture selection

27 October 2026. All three previously catalogued Graduale Aboense continuities in the existing demonstration were tested against sixteen retained original photographs. This is a bounded control study inside the current lead set, not another manuscript target. The [protocol](research/continuation_36/protocol.json) preceded fresh boundary inspection and discloses catalogue knowledge and possible earlier image exposure. No new discovery or independent confirmation is claimed.

## Direct source results

| Already catalogued edge | Source captures containing the passages | New image-level observation | Limit |
|---|---|---|---|
| Fr 7960 catalogue 2v → Fr 7961 catalogue 1r | 7960 capture 4 → 7961 capture 1 | The main line ends *refugium meum*. A lower-margin *es tu* catchword repeats the next capture's first words, which continue the *Esto mihi* introit. | Directional text plus catchword supports the prior edge. Standard chant words are not a unique book fingerprint or physical seam. |
| Fr 8343 catalogue 1v → Fr 8344 catalogue 1r | 8343 capture 2 → 8344 capture 3 | The first passage ends *Ego sum pastor bonus* and writes a new Alleluia; the second starts *Surrexit Christus et illuxit*. | Consistent with the catalogue but only a generic chant boundary. Immediate adjacency remains unresolved from this image evidence alone. |
| Fr 8344 catalogue 2v → Fr 8343 catalogue 2r | 8344 capture 2 → 8343 capture 3 | The verse ending *psalmum dicite nomini eius* continues *date gloriam laudi eius*, before a doxology cue. | Exact phrase-level directional support for the prior continuation. No unique variant, physical seam or complete quire reconstruction. |

The catalogue's assertions are preserved as prior evidence, available in the [pinned MPO deposit](https://zenodo.org/records/17287665). Local catalogue-side mapping is interpreted from visible contents; **photograph ordinal is not a folio-side rule**. In particular Fr 8344's first photograph does not show the proposed first boundary. Its third photograph supplies the *Surrexit* passage. This changes which image the viewer should show, not the institution's catalogue or a historical attribution.

Seven [exact source regions](research/continuation_36/observations.json) retain literal partial readings separately from normalized searches, image URLs, PDM statements, hashes, coordinates and uncertainty. A [complete sixteen-image inventory](research/continuation_36/inventory.json) discloses the actual inspection scope. The [source-pixel proof](research/continuation_36/boundary-reading-proof.png) enlarges those regions using nearest-neighbour display; it generates no manuscript detail.

## Concordances and controls

Only after the initial region readings were proposed were external identifications checked. [MMMO's B-Br Ms 10127-44 f.096v entry](https://musmed.eu/chant/107721) identifies the *Esto mihi* Mass introit as g00648; its indexed text was available, while the direct reader returned `Cache miss`. The [Cantus inventory at folio 233](https://cantusdatabase.org/source/666647/chants/?folio=233) identifies the *Jubilate deo* verse associated with *Vocem jucunditatis* as g02089a. These are identification aids from other sources, not independent transcriptions of the Swedish fragments or evidence of a unique transmission relationship.

The [indexed Mass inventory at folio 216](https://cantusdatabase.org/source/638308/chants/?folio=216) has more than one *Surrexit Christus et illuxit* alleluia setting. The office antiphon with the same words must not silently supply its ID or melody to this Mass chant. No melodic ID is selected for the Swedish reading, and no notes were imported.

Reversing the I/III boundary readings does not satisfy their specific forward phrase/catchword alignment. The non-neighbour Fr 7960 catchword does not repeat Fr 8344's *Surrexit* beginning. That control belongs to the same published book grouping: non-adjacency is not a different-codex label. These are qualitative consistency checks on selected readings, not an accuracy estimate or an untouched validation of improved manuscript recognition. The generic II boundary remains explicitly weaker.

## Data, viewer and scientific status

The reconstruction generator now selects the six relevant photographs with passage-region IDs and source hashes. The cards and inspection dialog retain provisional mapping notes and the separate strength of each boundary. The two unplaced witnesses still use representative images. The three catalogued edges remain previously documented; the new AI source readings have no independent confirmation.

The knowledge overlay, version 1.1.0, includes these scoped observations and E35. It now has **163 overlapping lead/question entries, 117 physical-pair leads, 855 entities, 573 claims and 77 regions**. E35's imaging relation is separate from physical joining. The seven new regions are outside the frozen 63-region review. Ninety-three pair leads still have only catalogue/availability triage; inspecting these control boundaries does not pretend to complete their primary-source work. All five frozen input hashes retain their E33 values.

No claim meets the discovery or novelty gate. Two exact control boundaries now have inspectable source support, and the demonstration selects better source captures. None of the seven ambiguous frozen attribution cases is resolved by this work. Finnish images, Fr 20278 and relevant Taitto/Keskiaho passages remain missing or unread; missing access is not a negative result. No outreach, upload, publication or new download occurred. The working source inventory remains 177 files, below the 300 limit.

## Reproduce

```sh
.venv/bin/python research/continuation_36/record_evidence.py
.venv/bin/python -m lost_library reconstruct
.venv/bin/python -m lost_library export
.venv/bin/python -m lost_library knowledge build
.venv/bin/python -m lost_library knowledge validate
.venv/bin/python -m lost_library knowledge export
.venv/bin/python -m unittest discover -s tests -v
node --test tests/viewer.test.cjs tests/knowledge-viewer.test.cjs
```

The evidence script verifies bytes, bounds and consistency of the declared readings. It does not automate or independently verify paleography. Full pipeline replay remains restricted to a temporary extracted package so the live frozen files stay unchanged. The current package manifest/verification records its checks separately.

Continue the same amended research goal. The highest-value attribution test remains the paired Finnish signature/full-text comparison; local primary comparisons beyond these controls remain available. Re-running broad visual similarity would not resolve the missing historical distinctions.
