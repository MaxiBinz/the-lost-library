# E34: Complete lead audit, practical knowledge model and Fr 8994 follow-up

25 October 2026. This implements the user's amendment to the existing goal. The previous goal and full amendment are preserved in `research/goals/`; historical reports, the ten-pair queue, its reviews, rankings, features and evaluation remain intact. No new attribution, independent confirmation or cleared originality is established. The goal remains active.

## Complete coverage, with an honest boundary

The [versioned register](data/lead_register.v1.json) accounts for all 170 saved directional ranking rows, reconciled to 113 unordered physical-object pairs. Adding the existing dossiers and diagnostic controls gives **117 pair leads**. All ten frozen hypotheses, 16 dossiers, 13 crosslinks, 13 current context checks and named feasibility/auxiliary questions are represented. There are **159 lead/question entries**, including overlapping topic and control views; they are not 159 distinct pair hypotheses or independent findings. The 129 core catalogue records resolve to 128 explicit physical object IDs. Finnish recto/verso records share one object; shared codex labels do not merge archival objects. The two C23 page records likewise share their external comparison object. Turku Ms. c remains unresolved.

Every pair now has a descriptive comparison of 13 actual inherited catalogue fields, date-interval overlap, source reconstruction labels, available primary images and missing inputs. Across 1,521 field comparisons there are 889 exact agreements, 268 differences and 364 missing comparisons. Four pair descriptions have nonoverlapping recorded date intervals. These are repeated, selected catalogue descriptions, not independent observations, calibrated rarity estimates or physical exclusions. Mixed sections, trimming, dating error and composite history remain alternatives.

**Ninety-three pair leads have only catalogue/availability triage.** Fourteen have earlier dossiers and ten have frozen source reviews. This continuation does not pretend that all 117 received new manual manuscript comparisons or that primary-source investigation is exhausted. Each row records its next stronger text/structure test and what can still be done locally. Missing material does not create a negative assertion.

## What has actually been tested

| Lead | Existing/new test and present result | Highest-value remaining test |
|---|---|---|
| Fr 10370 order, marks, placement | Existing direct verse/mark reading supports photograph 2→3 text order. Fixed registration did not establish seams. The published insertion between IV.157 ff.7/8 is credited separately from the qualified Codex 1505 suggestion. | Complete corresponding boundary text and original side/numbering convention; no new placement claimed. |
| IV.156/157 hVIII–hIX | Existing indexed descriptions and explicit consistency-premise check remain conditional. Different feast names alone do not establish incompatible text. | Both source addresses and full text, reset/composite/description alternatives. |
| Fr 1385/10406 ornament/layout | Existing controlled initial comparisons, manual ruler measurements and the Fr 7292 different-codex pitch control show resemblance but no unique fingerprint. | Diagnostic text, structure or distinctive variants beyond shared production. |
| Fr 20274 witness text | Existing ten-site actual-C23/edition comparison: seven current/standard agreements, one written-scope difference, two unavailable target sites. No distinctive shared uncorrected error. | Independently readable diagnostic variants; original C435 pages remain uninspected. |
| Fr 8994 IIII/k | New E33 native-image reading finds third-nocturn material against the proposed Finnish address's indexed first-nocturn description. This is conditional counterevidence. | Finnish f.8 and ff.9–10, Fr 20278, complete unique address and section mapping. |
| Fr 8994 partial photographs | New E34 inspection finds chant succession consistent with relative reading order; two further source regions recorded. No overlapping detail, seam or reliable medieval side map established. | Complete boundary transcription or repeated photographed detail; no failed registration is claimed. |
| Fr 4223/8311/8455 versus Fr 1385 | Existing exact BOMPAC crosswalk separates the three candidates in unit 258 from Fr 1385 in unit 912. These are related research-data assignments, not independent image rejections. | Primary text/structure test of the separation; frozen H08–H10 remain C. |
| IV.173 / Hy 49 / Ant 242 / Ant 99 | Existing exact alias and catalogue/workbook checks distinguish same codex, suggestion and broad style group. Two-column/one-column differences do not exclude a composite. | Fr 29666 image and cited passages; adjudicate specific relations separately. |
| Fr 8311 chant | Retained provisional Cantus 006537/006537a identification is a concordant chant, not a book fingerprint. | Literal pixel and distinctive variant checks; no untranscribed melody imported. |
| Positive/negative controls | Retain the published 8201–8304 same-hand/different-book rejection, 8201–20106 positive and documented Aboense/IV.160 relations. Model failures remain unchanged. | Missing comparator images and source-specific review; no tuning to erase failure. |
| Duba scaling ratio | Existing dimensional derivation and three analytic controls support the prose ratio, separately from attribution work. | Check later errata/uses and first notice; no original methodological contribution claimed. |

## New local source follow-up

A [protocol](research/continuation_34/protocol.json) stated the partial-photo hypothesis, alternatives and predicted evidence before the new boundary inspection. It discloses prior E33 exposure; this is exploratory, not blind or preregistered discovery research. All four retained native-width JPEGs were inspected without editing or new downloads.

The incipits in the numeral-bearing photograph, second partial photograph, k-bearing photograph and fourth photograph are consistent with the sequence *Nec propria*, *Novo rerum*, *Predicacionis*, *Devenerat*, *Egregius*. The [original performance publisher's listing](https://new.lawo.no/produkt/historia-sancti-olavi-2/) is an identification/order aid, not a primary manuscript witness. Partial literal readings remain separate from normalized chant identifications in the [two new regions](research/continuation_34/observations.json). No exact repeated photographed detail or full boundary transcription was established. Text order cannot by itself prove same surface or recto/verso.

This leaves E33's conditional conflict unresolved. The [official Finnish catalogue](https://fragmenta.kansalliskirjasto.fi/handle/10024/1300) is indexed evidence, not an inspected scan. Actual same unrepeated address, matching section/service, source accuracy and intrinsic side mapping remain unverified. No new exclusion or novelty claim follows.

## Implemented knowledge model

[MANUSCRIPT_KNOWLEDGE.md](MANUSCRIPT_KNOWLEDGE.md) records twelve competency questions, a concise model and the required project examples, written before implementation. [The JSON overlay](data/knowledge.v1.json) contains 853 entities, 568 attributed claims and 70 image regions: the preserved 63 plus five E33 and two E34 regions. Counts describe representation, not independent evidence. The model preserves scoped identifiers, distinct physical objects/records/captures/derivatives, separate reconstruction concepts, claim basis/stance/polarity/status, source snapshots, evidence links and explicit missing dependencies. The source's historical date stays unknown where not available; import dates do not assert a medieval or publication date.

Qualified Codex 1505–IV.157 claims coexist with documented IV.157–Ant 99 claims and BOMPAC assignments. IV.173 broad-group membership stays separate from its specific Ant 242 relation. A published negative 8201–8304 same-codex claim coexists with positive same-hand/catalogue-assignment claims and the retained computational suggestion. No transitive identity closure or confidence calibration is performed.

The [schema](data/knowledge.schema.v1.json) documents the vocabulary; the CLI validator additionally checks entity/evidence/dependency references, source hashes, image bounds, complete lead coverage and unchanged frozen files. [JSON-LD export](data/knowledge.v1.jsonld) keeps attributed claims reified, with the complete original payload retained; it is an MVP interchange path, not a claim of full CIDOC-CRM/TEI conformance. The [local inspection page](viewer/knowledge.html) supports lead/state filtering, source-linked details, original image regions and competing entity claims. The historical review remains separate.

## Reproduce and inspect

Run from the project directory with its environment; no acquisition or model reranking is needed:

```sh
.venv/bin/python research/continuation_33/check_sources.py
.venv/bin/python research/continuation_34/check_sources.py
.venv/bin/python -m lost_library knowledge build
.venv/bin/python -m lost_library knowledge validate
.venv/bin/python -m lost_library knowledge export
.venv/bin/python -m unittest discover -s tests -v
node --test tests/viewer.test.cjs tests/knowledge-viewer.test.cjs
```

Serve the project with `.venv/bin/python -m lost_library serve` and inspect `/viewer/knowledge.html`. The full lead rows include prior sources, support, counterevidence, actual work performed, missing inputs, next tests and state-change criteria. Historical E20 checks pin an older entire `fragments.json`; they are historical-snapshot checks and are not silently weakened for E33's added resolution variants. Current audits instead verify all retained images and preserve the primary input/frozen experiment hashes.

## Remaining work and resource limits

No claim meets the novelty standard. Taitto's exact discussion, relevant Keskiaho passages and Walta's full chapter remain unread; failed access is not evidence of originality. Corresponding Finnish images and several Swedish comparators remain missing. Ordinary browser record/OAI access met verification pages left untouched. No outreach, upload, publication or restriction bypass occurred.

The inventory is 171 core image files plus six auxiliary source/derivative files, **177 working files** against 300. The conservative download plan is **1,215,649,599 bytes** against 3 GB, including a 1 GB reserve for incompletely logged earlier traffic. E33 added 1,261,947 bytes; E34 added no downloads or physical objects. The next highest-value test is the actual Finnish folio-8/9–10 signature and text comparison. Meanwhile the register explicitly retains locally feasible primary comparisons instead of declaring a global access blocker. Continue the amended goal; do not treat the inventory or ontology as scientific completion.
