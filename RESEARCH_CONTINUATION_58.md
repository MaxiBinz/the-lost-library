# E58: Fr 8311 capture boundaries and stronger prior-art counterexamples

1 November 2026. E57 added provisional chant readings. This follow-up examines their photographic boundaries and checks whether the stronger combination of three responsories **and their three verse IDs** is already indexed elsewhere. It does not introduce a new manuscript family or a new book attribution.

## The photographs

The four retained Riksarkivet views were already seen during E54, E57, and again before the [E58 protocol](research/continuation_58/protocol.json); this is an unblinded assessment. A [review image](research/continuation_58/seam-review.png) juxtaposes fixed strips from the bottom of capture 1 and top of capture 2, and the bottom of capture 3 and top of capture 4. It is a review aid, not an aligned reconstruction. Source dimensions, hashes, and crop coordinates are in [review_sources.json](research/continuation_58/review_sources.json); [annotations](research/continuation_58/observations.json) retain the exact source links.

The bottom of capture 1 provisionally ends with *Vocem tuam audivi in paradiso et*. The damaged upper line of capture 2 appears compatible with its continuation *timui eo quod nudus [essem]*. Capture 3 ends with words provisionally consistent with the end of the *Ubi est Abel* responsory; capture 4 preserves later text consistent with that same responsory, followed by *Maledicta terra*. Both are plausible **textual continuities**, subject to independent reading. They do not themselves demonstrate the same original surface: no distinctive common ink or damage has been securely matched across either comparison. Occlusion and folds limit the result. The order of original sides, seam, and complete sequence remain unverified. The catalogue describes one leaf, but that is a separate source assertion, not independent image-overlap proof.

## The stronger sequence is already indexed

Search-indexed Cantus folio navigation for **Aachen Domarchiv G 20, 060v** lists, successively, 006537, 006537a, 006937, 006937a, 007804 and 007804a. A result from this same Aachen page had been encountered before E57's protocol, but its complete six-ID run was not recorded then. Its direct page opening had failed in E57 and was not retried; the [search-indexed listing](https://cantusdatabase.org/chant/179885/) is the evidence here.

Independently, search-indexed Cantus navigation for [Utrecht University Library Ms. 406, 065v](https://cantusdatabase.org/chant/493518/) lists the same six IDs successively. The exact Utrecht direct page attempted in E58 returned a cache miss; its linked institutional image viewer was inaccessible through the web tool. No source image was inspected. The Utrecht index puts *domine* after *Vocem tuam*; the Fr 8311 photograph provisionally lacks it. Aachen's indexed incipit has *Vocem tuam audivi* without that word. Utrecht labels the reference passage Sexagesima, while Aachen's index and Fr 8311's catalogue use Septuagesima. These are catalogue/index descriptions, not independently confirmed service assignments or complete textual collations. The common sequence is an **ID-level** comparison, not identical melody or full spelling.

The directly opened [Mont-Renaud index](https://musmed.eu/chant/198989) also lists all six IDs, but it inserts another responsory and verse between *Pro eo* and *Ubi est Abel*; it is not another example of the same consecutive six-item run. The web-reader text of Ingrid Sperber's 2019 edition of the [1519 Nidaros breviary](https://www.bokselskap.no/wp-content/themes/bokselskap2/tekster/pdf/breviarium.pdf), printed pp. 186 and 192, places *Ubi* and *Miserere* on one occasion, while *Dum* and *In sudore* occur on Thursday. This is useful for recognising alternatives, not a transcription of Fr 8311 or the original printed book.

These examples strengthen E57's narrower Trier comparison: **the same six candidate identifiers and their order are already indexed in at least two other manuscripts**. They do not demonstrate that all six followed that order on the original Fr 8311 leaf, that any melody matches, that the combination is common in a defined population, or that a source is copied from another. They make the six-ID pattern a poor standalone identifier and leave possible smaller differences for properly controlled future comparison.

## State and reproduction

No new manuscript image was downloaded; the 208-source-file inventory and 1,675,860,841-byte conservative plan remain unchanged. Search and web-reader traffic is unmeasured within the existing reserve. All frozen reviews and historical lead states remain unchanged. This is a source-comparison and provenance improvement, not a novel scientific discovery or independent review. Exact access results, including unsuccessful requests, are in [sources.json](research/continuation_58/sources.json).

```sh
.venv/bin/python research/continuation_58/check_sources.py
.venv/bin/python -m lost_library knowledge validate
```

The checks validate image hashes, dimensions, annotation bounds and the scope recorded in the knowledge graph. They do not certify a Latin reading, the external index, or book identity. Continue the broader authorized research using a discriminating source-based test; do not infer uniqueness from this sequence.
