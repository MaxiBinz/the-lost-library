# E52: Ant49 group comparisons and a repeated-incipit trap

30 October 2026. The preceding turn made progress through current-release verification and a primary margin audit. Its archive job is terminal and passed. This continuation executes a predeclared comparison of the existing Ant49 group; it does not add a target family or relax the frozen tests.

## Scientific result

No new book attribution or exclusion is established. All 13 previously source-only pair leads within the six-object Ant49 group now have a **limited direct comparison of surviving text context and page construction**. Their historical decisions remain unresolved. The known different-book pair shares the same general layout, so that feature cannot decide the other pairings. This is a documented failed discriminator, not a recognition improvement.

Two source details explain further traps:

- Fr8072 has two *Veni sponsa* occurrences. The first ends with *in eternum*; the second continues with *pro cuius amore* and the blood/martyrdom wording, with visibly different notational elaboration. They provisionally fit known antiphon005328 and responsory007828. Equal incipits need not mean the same chant item, and different settings need not imply different books.
- Fr8073 has an explicit *Super magnificat antiphona* rubric alongside blocks of continuous verse-like text. A hymn reference or unnotated verse block cannot by itself classify the whole book or split this fragment from an antiphonal.

These are source-linked local observations. The antiphon/responsory distinction is already documented in chant catalogues; no new liturgical practice, distinct tradition or scientific novelty is claimed.

## Fixed group and access

The [protocol](research/continuation_52/protocol.json) fixes Fr8066, Fr8072, Fr8073, Fr8201, Fr8304 and Fr9620, all already present in the candidate set. Their 15 possible pair edges comprise 13 pending first comparisons, the published8201/8304 same-hand/different-book control and the earlier8066/9620 comparison. BOMPAC-4861 co-assignment and the competing published rejection remain credited separately.

Eight exact native painting URLs for8072/8073 were taken from the retained official manifests before acquisition. Six succeeded, saving **1,896,527 bytes**.8072 capture3 and8073 capture1 timed out; neither URL was retried or requested through an alternate client. Subsequent runs skipped every recorded success/failure and continued only the other predeclared photographs. All requests are terminal. [Receipts](research/continuation_52/download_receipts.json) and [capture descriptors](research/continuation_52/captures.json) preserve the exact paths, canvases, dimensions, hashes and PDM Rights-metadata statements.

The inspection covers **24 distinct photo views**:17 retained group photographs, six newly saved files and8073's retained800px first-photo thumbnail.8072 capture3 remains unseen.8073's first photo was inspected at lower resolution after its native request failed. The planned complete group photo coverage therefore remains incomplete. Photographs are not additional leaves, and no medieval recto/verso map is assigned.

## Observations and controls

[Reading version1](research/continuation_52/readings.v1.json) preserves literal candidates before the new reference lookup. [Version2](research/continuation_52/readings.v2.json) distinguishes the two8072 occurrences after source-context review. [Version3](research/continuation_52/readings.v3.json) adds complete inspected-photo coverage, native staff regions and all six object summaries. The original four literal candidates remain unchanged.

The six general five-rule observations were **already recorded in E44** and are explicitly reused. The new native8072/8073 bands agree with those earlier thumbnail observations. They are not six fresh discoveries, independent votes or an accepted catalogue correction. The published wrong8201/8304 pair also shares five-rule staves and a broad writing field. There is no defensible membership partition from that feature.

The8072 repeated incipit has two different visible continuations; no complete interval or pitch transcription is supplied. The local work IDs remain qualified. Indexed [Graz antiphon metadata](https://cantusdatabase.org/chant/247223/) and [responsory metadata](https://cantusdatabase.org/chant/247233/) support the distinction. The [St Gall391 index](https://cantusdatabase.org/chant/460369/) already lists both works in one witness. These records describe other sources; their melodies, positions and provenance are not transferred to8072. The partial *Regem virginum* cue and invitatory rubric support only a candidate001151 identification.

Two direct Cantus page opens returned Cache miss and were stopped. The evidence used from those pages is explicitly labelled search-indexed text. No reference manuscript image, reference score or complete office edition was imported. Tentative8073 *Felix terra* searches did not establish a work identification, rarity or novelty. [Exact source/access notes](research/continuation_52/sources.json).

Seven precise new regions record the visible details. The [source-pixel figure](research/continuation_52/text-review.png) was visually inspected; it uses crops and nearest-neighbour fitting only. No AI-generated manuscript detail or reconstructed page is presented. A visible repeated boundary between8072 photographs is a photographic mapping clue, not a new cross-fragment join or final medieval-side assignment.

## All pair results and their limits

The [13-row comparison matrix](research/continuation_52/pair_comparisons.json) reports every selected edge, each object's actual context, source regions, shared layout, photo-coverage limits, unresolved state and next discriminating test. Different feasts/genres and generic text cues do not exclude one book. No exhaustive chant census, complete corresponding diagnostic variant, physical join or secure original address is established.

Exactly 13 first-comparison flags change, from29 to **16 remaining without an initial direct comparison**. This counts actual limited source comparisons, not 13 completed historical adjudications. The group test remains explicitly incomplete at its planned full-photo scope. All historical decision states and the frozen2E/7C/1D outcomes stay unchanged.

Knowledge version1.16.0 contains168 overlapping entries/117 pair leads,939 entities,636 claims and146 regions. Three known Chant concepts have separate unresolved local identification claims; two supported observations describe source features only. New files link to existing objects/canvases, with no added physical object, identity closure or medieval side. E50/E51 retain strict historical transitions through pinned snapshots while E52 separately checks29→16.

The working inventory is **200 source files**. The conservative transfer plan is **1,673,000,850 bytes**, including the existing1GB reserve. Timeout and web-reader traffic can be unmeasured; this is not an exact lifetime network total. No outreach, upload, external catalogue edit or publication occurred.

## Next test and reproduction

Proceed through the remaining16 existing pairs. Within Ant49, general layout comparison has reached its useful limit: a future book argument needs exact corresponding work/service evidence, a distinctive supported variant or physical/quire evidence. Complete8073 work identification and the missing20106 opening remain separate actionable lines. Do not repeat failed source routes or substitute another generic image screen.

```sh
.venv/bin/python research/continuation_52/record_evidence.py
.venv/bin/python research/audit_resources.py
.venv/bin/python -m lost_library knowledge build
.venv/bin/python -m lost_library knowledge validate
.venv/bin/python research/continuation_52/check_sources.py
.venv/bin/python -m lost_library knowledge export
```

These steps use retained files. Acquisition is receipt-aware and must not re-request completed URLs. The checker validates source provenance, region bounds, complete selected-edge coverage, historical state preservation and inferential limits. It does not independently validate the AI readings or establish novelty. Archive verification and frozen replay checks are recorded in `output/research/package_verification.json`. The discovery goal remains active and incomplete.
