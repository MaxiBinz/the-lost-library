# Bounded validation audit and retrospective metadata diagnostic

Completed 20 October 2026 (Europe/Vienna). The metadata source and image request below were first examined on 19 October; the deterministic computation was rerun on 20 October. This note adds evidence to Phase 0. It does not report a trained AI system, a blind benchmark, or a new manuscript relationship.

## Finding

A simple metadata compatibility ranking retrieves two documented Graduale Aboense relationships near the top of full genre-specific galleries. It **also ranks a published same-hand, different-book comparison uniquely first**, while a complete-case filter **excludes a published compatible same-book fragment**. This is a concrete failure case for treating compatible dimensions, broad script and notation as sufficient identity evidence. It supports soft handling of missing data and the need for textual/codicological contradiction checks before visual retrieval is interpreted.

The experiment does **not** establish whether AI visual features will improve matching. That claim still needs the independent, multi-codex experiment specified below and in the feasibility report.

## 1. Sources and evaluator-only labels

- Source data: the cached **CC0 MPO export**, [Zenodo 17287665](https://zenodo.org/records/17287665), `research/mpo.csv`, 22,909 records. Source SHA-256: `f5d2825703be19fd1994bc0b91724c32c67c36535622d5554c37b4029592d00b`.
- **7960–7961** and **8343–8344**: the source records explicitly describe continuous texts. These are already documented same-codex relationships in Graduale Aboense, not discoveries. The notes containing these assertions are read by the evaluator only and excluded from matching features.
- **8201–20106** and **8201–8304**: Czesław Grajewski, [*Offices of St. Catherine of Alexandria*](https://doi.org/10.25167/ls.4818), p.293, supplies a compatible same-book comparison and an explicit different-book comparison. The primary [article PDF](https://czasopisma.uni.opole.pl/index.php/ls/article/download/4818/4236/13686) was inspected again in this cycle. Its argument combines chant continuity and contradictory liturgical positions, while distinguishing book identity from a shared hand. These are published interpretations, not newly adjudicated labels. They should be checked with a specialist before a definitive gold set is frozen.

The source article's substantive claim is summarized here rather than copied. The catalogue's own shared Codex 1146 label is **not** used as ground truth: that is the label the published comparison challenges.

## 2. Exact diagnostic method

Reproduce from the project root:

```sh
python3 research/metadata_retrieval_diagnostic.py
```

The script uses the complete cached export and an explicit feature whitelist. It never uses CCM/codex assignments, institution, account provenance, image URLs, contents, literature, or remarks in ranking. Identifiers connect input to evaluator labels and never break score ties.

For each query, the initial gallery contains **every other record of exactly the same `sachtitel`**, including records without image pointers. A deliberately strict complete-case filter then requires five categorical fields and two parsed dimension pairs. It is tested as a possible failure mechanism, not recommended as a production filter.

The nine equally weighted comparisons are:

1. Exact raw-field agreement on `schrift`, `notation`, `notenlinien`, `spaltenzahl` and `zeilenzahl1`.
2. Numerical agreement within **0.5 cm** on each of the two components of `format` and `schriftraum1`.

The compatibility score is the fraction of nine agreements. The numerical tolerance is an elementary retrospective choice related to the catalogue's measurement rounding; it is **not an empirically calibrated threshold**. Asterisks and uncertainty markers remain in the saved raw features. Parsing a damaged measurement into a number does not reconstruct the original leaf size. This weakness is part of why a high compatibility score cannot identify a book.

The choices and queries were made **after** the reference relationships had already been read. The diagnostic is therefore retrospective and selection-biased. It has no training stage, no fitted parameters and no held-out performance claim. Catalogue descriptive fields may themselves inherit a group description; source independence has not been established. Masking explicit codex labels does not eliminate that indirect leakage risk.

## 3. Observed outputs

| Query → reviewed candidate | Published/catalogue relationship | Exact-type gallery before filter | Eligible gallery after filter | Compatibility | Tie-aware rank |
|---|---|---:|---:|---:|---:|
| 7960 → 7961 | Documented same-codex textual continuity | 1,321 gradual records | 792 | 9/9 | 1–4 |
| 8343 → 8344 | Documented same-codex textual continuity | 1,321 gradual records | 792 | 9/9 | 1–7 |
| 8201 → 20106 | Published compatible same-book comparison | 2,099 antiphonal records | 1,221 | Not scored: excluded | No rank |
| 8201 → 8304 | Published same-hand, **different-book** comparison | 2,099 antiphonal records | 1,221 | 9/9 | **1, uniquely** |

Ranks are intervals over score ties. No arbitrary identifier or catalogue order is used to turn a tie into an apparent successful first hit. Thus 7961 is guaranteed to occur in the first four tied positions; 8344 is somewhere within a seven-way leading tie. A single top-1 or top-5 accuracy figure would conceal this distinction.

The positive candidate **20106** lacks `schrift`, `spaltenzahl`, `format` and `schriftraum1`, causing its exclusion. It is not a failed image matcher: no image was scored. This demonstrates a concrete false exclusion by complete-case filtering, while the differently dated but textually compatible fragment remains invisible to that filter.

The published negative **8304** agrees with 8201 on all five categorical fields; the leaf-size height difference is 0.5 cm and all remaining dimensional components pass the tolerance. It therefore receives maximal compatibility and the unique leading position. A maximal score is plainly **not** a calibrated probability of same-codex identity.

Do not compute corpus precision/recall from this four-comparison diagnostic. The thousands of other gallery items were not adjudicated; lack of a known association does not make them negative. The query examples were chosen for pedagogical/diagnostic value, and two positives come from one already studied codex. The observed complete-case retention counts are data-selection counts, not model recall estimates.

## 4. Reproducibility check

The script was executed twice consecutively after the final raw-feature logging change. Both runs produced byte-identical result JSON and the four expected eligibility/rank outputs were inspected.

- [Script](metadata_retrieval_diagnostic.py)
- [Results, full whitelisted features and evaluator labels](metadata_retrieval_diagnostic.json)
- Script SHA-256: `c92e166e080c94015837e29d40d853fb4eb68dd6648313eed7411e45c80383b3`
- Result JSON SHA-256: `bf8f5318d97f1de3a924e42504d7a3233f8a84717407cc4ec3832f5765d1b491`

These hashes describe the delivered versions; editing the script will appropriately change its hash. Rerunning needs only the Python standard library and the cached CSV. No network, paid service, model download, or image processing is required.

## 5. Additional real-image check for the difficult negative

The cached manifest for 8304 had already been retrieved, but its image had not been tested. A single **59,532-byte** JPEG was now actually fetched (HTTP 200, `image/jpeg`) at [800-pixel width](https://lbiiif.riksarkivet.se/v3/arkis!R1008304_00001/full/800,/0/default.jpg), with a 1 MB response cap. It was decoded and visually inspected: the sample contains manuscript text, musical notation, coloured initials, a ruler and a folded/obscured lower region. It is suitable to include as a real image in a later expert-reviewed hard-negative pair, subject to crop/side identification.

- [Saved sample](evidence/mpo_8304_goal_sample.jpg)
- [Timestamped request/rights receipt](evidence/goal_negative_image_access.json)
- SHA-256: `b0e5a3a3066f0da51a4f6c94fa04ac833b4a0dc8d1488998f4ca6a02432797bb`
- Rights: Public Domain Mark 1.0 in its cached source manifest.

The 8201 sample was already cached. No visual identity algorithm was run on either image, and visual inspection here is not an independent palaeographic confirmation of the published relationship. The one new image improves benchmark readiness, while the key positive image for 20106 remains unverified.

## 6. Smallest defensible next validation protocol

The next experiment should test **whether visual/layout evidence adds value over metadata and text**, not merely whether a selected known positive looks similar. It must be reviewed before a full pilot begins. The following is an executable design, with data gates clearly separated from evidence already obtained.

### Data gate and ledger

1. Assemble a versioned object/leaf/capture ledger with exact holder IDs, physical fragment grouping, source images, per-image rights, authoritative relationship citation, and accepted/rejected/uncertain labels. A specialist checks the positive and difficult-negative labels, including the Grajewski interpretation.
2. Obtain at least **eight independently distinguished codices** if numerical calibration and a small held-out test are intended: two development, three calibration and three test codices. This is a proposed minimum planning target, **not an achieved sample** or a claim that three calibration books suffice for stable probability estimates. If independent books cannot be secured, reduce the claim to a case study and report ranks rather than probabilities.
3. Each evaluated codex needs multiple distinct physical fragments so one can be withheld as a query while another remains in the gallery. Keep all sides/captures/crops of a physical fragment together. Disputed same-family books remain in the same partition conservatively until independence is established.
4. Beauvais supplies a non-Nordic positive control and Graduale Aboense supplies known Nordic continuity cases. The two published Ant 49 books offer the unusually valuable same-hand negative, but membership/image gaps must be resolved first. Do not assume the other required independent books or negative labels already exist in usable form.

### Frozen comparison

- Hide association identifiers and relationship prose; audit parent-inherited dates/dimensions for indirect leakage. Keep all books used for feature/threshold selection out of the untouched test partition.
- Use the same gallery for metadata-only, metadata+chant/text, and metadata+text+frozen visual/layout retrieval. Any missing-value policy, candidate filter, feature weights and tie rule are fixed on development books. Freeze thresholds before opening test labels.
- Include confirmed different manuscripts with identical chants/texts; similar hands from different books; the same region/period; similar notation; the known same-hand comparison; and queries with no correct gallery item. Do not relabel unlinked material as negative.
- Count known positives lost during filtering. Compare cropped and uncropped images to test capture-background shortcuts, and report cross-institution results separately.

### Metrics and decision

- Report tie-aware Hit@1/5/10, recall@k and MRR only for queries with known relevant gallery objects, alongside their denominators. Report unmatched-query false acceptance/rejection separately.
- Review an entire preregistered queue of, for example, the top 30 distinct predicted pairs. Show confirmed-positive precision, unresolved coverage and lower/upper bounds; never select only easy predictions for adjudication.
- Measure known-label recall including filter losses, and false positives by difficult-negative subtype. State the pair universe; a balanced artificial test does not establish real-world precision.
- Use codex-level macro results and grouped uncertainty. Assess calibration on separate books only; show reliability counts and Brier score if the independent data support them. Otherwise explicitly decline probability claims.
- The test supports advancement only if visual features improve a frozen baseline without losing crucial known positives and with an acceptable expert-review false-positive burden. A negative result is useful. Recovering a documented association remains validation; it is never a new discovery.

## Assessment

The new evidence supports **CONDITIONAL GO**, not an unconditional GO or a claim that AI matching has been validated. A realistic metadata baseline now has both a demonstrated recovery behaviour and a demonstrated failure against a documented difficult negative. The next useful work is reference-label/access curation and a genuinely independent visual-addition experiment, rather than a larger reconstruction system.
