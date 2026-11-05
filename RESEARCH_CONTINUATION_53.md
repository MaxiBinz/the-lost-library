# E53: Hy49 comparisons and a probable hymn-work mismatch

30 October 2026. The user reactivated the existing goal after the paused turn, which made no research changes. E52 remains the preceding completed research phase; its archive process is terminal and verified. No new target family or scientific success criterion is introduced.

## Result

Eight existing Hy49/Fr10349-related pair leads receive limited direct comparisons using15 retained photo views. No new codex, exclusion or catalogue correction is established. All historical decision states remain unchanged; **eight other existing pairs still lack an initial direct comparison**.

The selected *Jesu…* passages in Fr10349 and Fr25592/Hy49 provisionally fit **different known hymns**, not a diagnostic same-hymn variant. Fr10349 reads *Iesu saluator seculi* with the *redemptis ope* continuation. Hy49 has a *Iesu redemptor seculi* candidate with *verbum/patris* context and a following *Tu fabricator* cue. Some Hy49 words remain difficult, and exact complete local IDs, stanza order and melody remain unadjudicated. Similar opening words do not establish a useful textual link between these fragments.

The *Tu fabricator* stanza is already indexed in other medieval witnesses. Its omission from one selected full-text listing is **not evidence of a new local insertion or rarity**. The work comparison narrows the next test; it is not a scientific discovery.

## Fixed comparisons and actual coverage

The [protocol](research/continuation_53/protocol.json) fixes all eight still source-only edges among F-5der, F-5uba, Fr25592, Fr10349, Fr25173 and the four Fr2863/2864/2872/2873 comparators. These are existing candidates. Published Beauvais membership and the source-described Codex434 group are contextual controls, not new reconstructions.

All15 selected retained photographs were inspected. Fr10349 has its retained first thumbnail and three E50 native views; Fr25592 has four retained views. The other seven objects have one selected photograph each. Several institutional manifests contain additional uninspected views, so this is not complete source-photo or original-side coverage. Photographs, fragments and leaves remain distinct.

For reading only, Fr25592 captures2/3 were displayed upright through an exact180-degree transpose. Original JPEGs and annotation coordinates are unchanged. Scratch rotations/candidate crops remain excluded from the review archive. No source file was acquired and no failed access route was retried.

## What the images support

Hy49 has narrow parallel fields with notated openings followed by continuous stanzas. Its selected *A patre unigenitus* cue agrees with the catalogue's hymn context, without independently confirming a complete book attribution.

The Beauvais views contain different local service cues: F-5uba shows *Off.* and *Secreta* rubrics with music and a prose prayer; F-5der preserves the *Galilei/aspicientes in celum* passage. These observations support the already published Mass context. Equal column counts or square notation do not identify Hy49 as part of the Beauvais manuscript.

Fr25173 has a broad notated field with an *off.*-like rubric and an *Exultabunt sancti* candidate. The four Codex434 first views also have broad fields. Fr10349 uses two narrow copying fields. Five selected pairs therefore show a visible field-design difference, challenging an unchanged uniform copying template. Different sections, copying changes or composite volumes remain alternatives to a historical book exclusion. The E50 Fr2863/2864 control observations are explicitly reused, not counted as independent new evidence.

Nine precise new regions and the four reused layout regions are linked in the [annotations](research/continuation_53/observations.json) and [eight-row comparison matrix](research/continuation_53/pair_comparisons.json). The [PDM-only hymn figure](research/continuation_53/hymn-review.png) was visually inspected. CC BY Beauvais image regions retain their source institutions and rights attribution; they are not included in the new figure.

## Work identification and prior-art limits

[Version1](research/continuation_53/readings.v1.json) preserves literal candidates before lookup. [Version2](research/continuation_53/readings.v2.json) keeps those candidates/coordinates unchanged and adds a separately labelled reference-assisted recheck. It also corrects a prose coverage-count typo:seven objects, not six, have one selected photograph.

Primary indexed [Cantus008333](https://cantusindex.org/id/008333) gives the All-Saints hymn and AH51/130 association already present in the Fr10349 catalogue. The [AachenG20 index](https://cantusdatabase.org/chant/181934/) supplies830177 context and separately lists [Tu fabricator as830177a](https://cantusdatabase.org/chant/181935/). A [Utrecht406 list](https://cantusdatabase.org/chant/496703/) also places that stanza after related830179 wording. These are known external concepts and contextual comparisons, not exact local work confirmation, a provenance assignment or new textual practice.

Two direct Cantus Index opens returned Cache miss and were stopped. The evidence used is explicitly search-indexed text. No reference manuscript image, score or melody was imported, and external feast/service positions were not transferred to the local fragments. [Source/access notes](research/continuation_53/sources.json).

## State and next test

Version1.17.0 retains168 overlapping entries/117 pair leads,943 entities,638 claims and155 regions. The two new local hymn-identification claims stay unresolved candidates. There is no new physical object, accepted original-side map, identity closure, score change or independent confirmation. Frozen outcomes remain2E/7C/1D.

Exactly eight first-comparison flags change, from16 to8. This records selected-view source comparisons, not completed historical adjudication or an exhaustive chant census. E52's strict29→16 transition is retained against the pinned pre-E53 snapshot; E53 separately checks16→8 with every historical decision unchanged.

The working source inventory remains200 and the conservative transfer plan remains1,673,000,850bytes, including the existing1GB reserve. Search/web-reader traffic is unmeasured; zero new retained files is not a claim of zero lifetime traffic. No outreach, upload, external edit or publication occurred.

Next inspect the eight remaining original-target/Ant39 pairs, concentrating on original marks and actual text context. The unresolved full-side/higher-resolution and exact-work tasks remain specific gaps. Do not repeat a generic column/style or *Jesu…* word match. The discovery ambition is unachieved; the existing goal remains active and incomplete.

## Reproduce

```sh
.venv/bin/python research/continuation_53/record_evidence.py
.venv/bin/python research/audit_resources.py
.venv/bin/python -m lost_library knowledge build
.venv/bin/python -m lost_library knowledge validate
.venv/bin/python research/continuation_53/check_sources.py
.venv/bin/python -m lost_library knowledge export
```

The checker establishes retained-source integrity, region bounds, selected-pair coverage and the first-comparison transition. It is not independent reading adjudication or novelty validation. Package verification records extracted E37–E53 source checks, knowledge validation and unchanged frozen offline replay results.
