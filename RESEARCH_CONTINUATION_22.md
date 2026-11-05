# Research continuation E22: a matched layout control and current prior art

**Date:** 24 October 2026. **Scope:** test whether the E21 staff-pitch resemblance distinguishes the existing Codex 1505 group, and recheck public BOMPAC/CODICUM work. The frozen ten-pair queue, core collection, predictors and thresholds remain unchanged. These are supporting source checks, not a new relationship hypothesis.

## A different-codex page has the same staff pitch

E21's full MPO screen identified Fr 7292 as the closest available control inside the exact Codex 1505 written-area range. The pinned catalogue describes Fr 7292 as a fifteenth-century antiphonary with Quadr notation, four music lines, eleven main-text rows, a 35 × 22.5 cm written area, and the separate catalogue group Codex 1306. It therefore matches the target on genre, notation, staff count, text-row count and written-area range while providing a catalogue-labelled different-codex example. That label comes from MPO itself and is not independent expert adjudication.

Before retrieving its image, I selected Fr 7292 from the metadata result rather than choosing a page after seeing its music. Its official IIIF manifest marks the reproduction Public Domain. In image 1, two manually selected four-rule systems give a mean interval of **5.543 mm**. The photographed 0-to-20 cm ruler span is 878 pixels. The E21 Codex 1505 images average **5.602 mm**, so the control differs by about **0.059 mm**—far below the roughly **0.5 mm** conservative uncertainty from manual line selection, before perspective and page-warp effects.

This is a direct, source-image counterexample to treating a 5.6 mm staff pitch as a unique Codex 1505 fingerprint. It does not tell us whether any specific leaves share a book, scribe or workshop. The control is only one leaf, is not matched for hand, and its different-codex label comes from the same catalogue. The measurements are post-inspection and have not been independently repeated.

The exact source hash, image regions, ruler endpoints, manually selected staff-line centers, calculations and caveats are in [the reproducible result](research/continuation_22/matched_staff_results.json), [the source annotations](research/continuation_22/observations.json), [the calculation script](research/continuation_22/matched_staff_control.py), and [the image receipt](research/continuation_22/image_receipt.json). It is integrated as auxiliary context CTX06, outside the hypothesis queue and core benchmark.

## BOMPAC and CODICUM already cover broad cross-collection integration

The open 2025 Fragmentology research note *Fragments Combined* documents the Stockholm–Helsinki BOMPAC dataset: 29,230 fragments integrated from MPO, Fragmenta membranea and supplementary records; it reports approximately 12,300 catalogue codices. The authors describe harmonizing metadata and explicitly characterize the dataset as research data rather than a replacement for institutional records. Its cited dataset DOI is `10.5281/zenodo.17511106`. The article was read; the dataset payload itself could not be retrieved through the connected browser search route, so no row-level result for Fr 10370 or Codex 1505 is claimed.

CODICUM's living Nordic Survey describes an overview assembled from published and unpublished catalogues, electronic databases and correspondence. Its Helsinki entry reports 5,435 manuscript fragments grouped into 1,544 codices and lists both Taitto's antiphonary catalogue and BOMPAC metadata. BOMPAC's article reports 5,434 Fragmenta membranea records; this one-record difference is unresolved and may reflect a later update or different scope. I have not silently reconciled the counts. The survey is collection-level, not a source-level adjudication of the fragments in this investigation. The current CODICUM pages inspected did not supply a new target-specific ruling.

This confirms that joining Nordic fragment catalogues or publishing a combined metadata corpus is already established work; that broad integration cannot be presented as our original contribution. It does **not** settle the specific text, sequence, side-orientation or attribution questions. The next meaningful claim must arise from primary-source evidence beyond inherited catalogue grouping. The public BOMPAC and CODICUM checks are recorded as auxiliary context CTX07 and in the updated [prior-art ledger](research/PRIOR_ART_LEDGER.md).

An exact-title/ISBN search for the unread Keskiaho chapter found the University of Helsinki bibliographic record but no chapter text or newly available lawful access route. The result adds no reading of the chapter and does not clear novelty; it is recorded so the same search is not repeated as if it were new evidence.

## Current conclusion and next test

E22 strengthens a negative result about layout: one well-matched different-codex page shares the measured staff pitch. The existing group remains plausible, but pitch alone cannot distinguish it. Broad database integration is also prior art. The highest-value remaining work is exact text and side ordering in the unresolved fragments, tested against complete corresponding sources and honest alternatives. A true same-hand/different-book image set could improve the codicological control if it becomes legitimately available; no such label is assumed here.

The source and download receipts remain within the existing limits. No contact, paid access, external upload, catalogue edit or publication occurred. The matched page is retained as an auxiliary comparator, not added to the core benchmark or to the ten frozen relationships.
