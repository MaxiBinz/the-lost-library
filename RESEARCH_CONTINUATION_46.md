# E46: notehead comparison and probable chant-work mismatch

29 October 2026, Europe/Vienna. E45 made progress by recording service labels, partial corresponding text and a paper-specific prior-art limit. E46 executes the selected musical/underlay check on the existing Fr8066/Fr9620 pair. **The selected word is notated differently, but the passages probably represent different related chant items. No same-chant melodic variant, new book, exclusion or discovery is established.**

## Fixed source comparison

The [protocol](research/continuation_46/protocol.json) fixes the two retained photographs and the words celos tangebat et. All relevant images and earlier references were already known: this is exploratory AI reading, not a blind or independent test. [readings.v1.json](research/continuation_46/readings.v1.json) preserves the manual source points before the new work-context lookup. [Version2](research/continuation_46/readings.v2.json) adds the reference-assisted interpretation without moving any source point, changing a head count or importing reference music.

Fifteen primary candidate notehead centres and one explicitly optional/uncertain part of the8066 tan sign are recorded. In the fixed **celos** span,8066 has **five candidate heads**, whereas9620 has **two simple stemmed heads**. The underlay and selected groups are directly visible in the [note-review figure](research/continuation_46/note-review.png). Shafts are not counted as additional notes. These are provisional manual note readings, not independent musical adjudication.

The tan-to-ge positions nominally rise by about7 deskewed pixels in8066 and fall by about13 in9620. These are image coordinates, not pitches. Sensitivity at3/4/5px centre tolerances, with a±0.02px-per-pixel rule-slope perturbation, makes the8066 direction unresolved at the wider bounds. The uncertain tan segmentation is also retained. **A robust direction contrast is not accepted.** These post-inspection bounds are sensitivity assumptions, not statistical confidence intervals or a fitted acceptance threshold. [comparison.json](research/continuation_46/comparison.json) reproduces the arithmetic.

The left-of-system signs were inspected too. The8066 field is partly clipped/folded;9620 preserves C-shaped and lower tail-like signs. Their full clef/rule function remains unadjudicated. **The planned complete diatonic interval transcription remains incomplete.** No absolute pitches, rhythm, chromatic inflection, modern score, audio or full melodic identity is supplied.

## Why the different local notation does not settle the book

The [context figure](research/continuation_46/context-review.png) preserves an important distinction:

- 8066 continues with descending/ascending angels and per eam ait, followed by Gloria patri and the Laudes block. This fits a **responsory-verse candidate**, compared with published Cantus007763zd.
- 9620 visibly has **dixit uere locus iste sa[...]**. The initial word is clearer than E45's uncertain pxit; the missing end after sa is not restored. Its wording fits the known **antiphon candidate005415**, Vidit Jacob scalam summitas ejus.

These are reference-assisted candidate identifications, not confirmed exact local IDs. The [indexed antiphon record](https://cantusdatabase.org/chant/248539/) and the previously retained [indexed verse record](https://cantusdatabase.org/chant/233459/) describe different known work contexts. The new direct antiphon open returned Cache miss and was stopped; the earlier failed verse route was not retried. No original reference manuscript or reference melody was used to refit either target. Other indexed witnesses put005415 in different service positions, so no local position is transferred.

**A probable work/genre mismatch can explain the musical difference.** The result challenges use of this shared phrase as a securely corresponding same-chant variant; it does not establish different books or separate whole-book genres. Shared biblical words, ordinary ornament, alternative sections, several hands and composite structure remain relevant alternatives.

## Methods and inference scope

The [Hungarian Neume Catalogue](https://neume.zti.hu/en_projekt.asp) basic-sign discussion and [Gilányi2022](https://doi.org/10.23714/rzt.fragmenta.publ.1011), relevant web-reader text pp4–7, supplied general notation context. No target provenance or subtype was assigned from these regional examples. The linked table image failed to open; PDF screenshot calls exposed references rather than a visible page image, so no visual method-figure review is claimed. No new PDF was saved or full25-page reading claimed. The previously retained Cantus entry guide remains a private method reference. Exact read/access scope is in [sources.json](research/continuation_46/sources.json).

The version1.10.0 overlay has **168 entries/117 pair leads,891 entities,598 claims and123 regions**. Two known external Chant concepts have separate unresolved local identification claims; a narrowly scoped observation records the head grouping. None merges physical objects or establishes a new codex. The pair remains unresolved,49 other pairs remain metadata-only, and the frozen ten cases stay2E/7C/1D. All frozen/core/E35 hashes remain unchanged.

No new source image or retained reading file was acquired:188 working source files and the1,669,530,774-byte conservative planning total remain unchanged. Web-reader traffic is unmeasured and falls within the existing planning reserve; this is not a claim of zero total network traffic. The figures use only retained PDM manuscript pixels enlarged with nearest-neighbour interpolation, with no new manuscript detail. No outreach, upload or publication occurred.

## Next action and reproduction

Keep the candidate work identifications and exact local positions qualified. Any further book inference needs genuinely corresponding distinctive text/music or physical/quire evidence. Repeating same-setting comparisons of provisionally different works will not resolve it. The next population task is to audit actual published-source coverage for the six existing Aboense control objects and13 metadata-only Codex1104 pairings, before spending discovery effort on known controls. Shared catalogue labels alone must not supply that credit. This remains the existing lead audit, not a new target family or scientific success criterion.

```sh
.venv/bin/python research/continuation_46/compare_notes.py
.venv/bin/python research/continuation_46/record_evidence.py
.venv/bin/python research/continuation_46/check_sources.py
.venv/bin/python -m lost_library knowledge build
.venv/bin/python -m lost_library knowledge validate
.venv/bin/python -m lost_library knowledge export
```

Use `check_sources.py --require-private` locally to require the retained earlier guide. The archive intentionally excludes it. The checker verifies hashes, bounds, preserved source points and arithmetic; it does not independently validate note readings, chant IDs, historical identity or novelty. Current tests and extracted replay outcomes are recorded in [VALIDATION_REPORT.md](VALIDATION_REPORT.md) and [package_verification.json](output/research/package_verification.json). The goal remains incomplete and active; available work remains.
