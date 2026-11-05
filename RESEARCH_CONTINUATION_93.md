# E93: A bounded Mary Magdalene sequence comparison

**5 November control:** A separate Barcelona manuscript inventory places *In diebus illis* immediately before *O beate Jacobe* and *O lux et decus* at fol. 095v. This matches the proposed order on Fr 10406 **if** its partially preserved first chant is *In diebus illis*. The Swedish incipit is not visible, and the comparator original was not inspected. It is evidence against treating that three-work order as unique, not proof of Swedish chant identity, physical adjacency or a new codex relationship. [Indexed comparison and limitations](research/continuation_112/control_barcelona.json).

**3 November 2026.** E92 directly measured an interior text span on the Swedish photograph, but did not resolve the II.64 comparison. This pass returns to source text in three already catalogued Codex 1505 leaves. It was selected after viewing the images and is unblinded, reference-assisted and not independently reviewed.

## Observations and limits

On [Fr 10407 photograph 4](research/continuation_54/images/Fr10407-capture-4-native.jpg), one passage provisionally reads *Secus pedes domini astans ... lacrimis plena*, followed lower down by an opening *Irrigabat igitur dominicos Ihesu pedes fracto quoque ...*. These fit the indexed antiphons **004848** and **003412**, respectively. The latter was already noted provisionally in E54; this more specific identification is a project reading, not an expert transcription.

On the existing [Fr 10370 photograph 1](data/images/mpo-10370-capture-1-1700px.jpg), E60 provisionally identified a later part of *Satagebat igitur Martha* (**004816**) followed by candidates for *Non est Martha* (**003915**) and *Et respondens* (**002720**). Its first line starts within the text, so the incipit itself is not visible. These are **reused E60 observations**, not new independent corroboration. All three leaves were already associated as Codex 1505 in the catalogue and in BOMPAC-5324; that published grouping is prior work, not our discovery.

The beginning of [Fr 10406's retained first photograph](data/images/mpo-10406.jpg) shows an ending provisionally readable as *... et capillis capitis sui tergebat et osculabatur pedes eius et unguento ungebat*. A published [Cantus witness for *In diebus illis* 003224](https://cantusdatabase.org/chant/1016926/) contains the same broad ending. The opening of the Swedish chant is not visible, and this biblical wording occurs in other contexts, so an exact identification and an immediate boundary join are **not established**. A standard text of *Irrigabat* 003412 differs in its continuation; a variant, intervening material, unseen capture area or different side mapping remains possible. Do not infer an exclusion of same-book membership from the observed passages.

## Control for an attractive but weak inference

The indexed [Paris, BnF Latin 12044, ff.164r–164v](https://cantusdatabase.org/chant/402231/) gives *Secus pedes* and *Irrigabat* before *Satagebat*, *Non est Martha* and *Et respondens*. It is a separate manuscript witness. Its index places other antiphons, responsories and verses between *Irrigabat* and *Satagebat*. This supplies a concrete counterexample to treating this **general order** as unique to our fragments or as evidence that their photographed edges must meet. It does not show the exact contents or amount of missing text in the Swedish leaves, and we did not inspect the Paris manuscript image.

The comparison therefore supports a mundane interpretation: the selected Swedish passages fit a known liturgical sequence, but they do not establish their order within a physical book, an immediate page boundary, a musical variant or a novel manuscript relationship. Exact texts, medieval side and opening-signature mapping, any hidden lines, and the Finnish comparator must be assessed before a stronger claim. The individual readings, source-image selectors, known prior assignments and alternatives are retained in [structured results](research/continuation_93/results.json), [new regions](research/continuation_93/observations.json), and the earlier E54/E60 regions.

No new manuscript file, contact, source update, independent review, book attribution or historical exclusion was added. The frozen decisions remain unchanged; first notice is unknown. Reproduce source-hash and region-bound checks with:

```sh
.venv/bin/python research/continuation_93/record.py
```

This verifies file identity and selectors, not the readings, reference edition, book identity or originality.
