# E89: A reuse-context control for the Fr 10370 / Fr 20278 question

**E90 follow-up:** The actual Fr 10370 reuse heading has now been inspected. It appears to name Christiern Philipsson and a Finland provision account spanning 1610–1611, making its comparison with Haapanen's truncated II.64 heading more specific. Whether they refer to the same or different accounts or objects remains unresolved; do not assume either. [E90](RESEARCH_CONTINUATION_90.md).

**2 November 2026.** E88 added published laboratory evidence and its limits; it did not settle any book attribution. This pass tests a tempting alternative signal: whether an account associated with the same named official and year identifies a medieval book.

## The published observations

The Swedish MPO record retained in the project describes **Fr 20278** as an antiphonal leaf and gives the account description `Christiern Philipssons räk för tull i Åbo 1611`: Christiern Philipsson's account for customs in Turku, 1611. The published Finnish IV.157 description lists the same item under Ant 99 and distinguishes that grouping from the suggested Codex 1505 group. The source does not supply a current image of Fr 20278 in our retained record. [Source crosswalk](research/independent_pass/crosswalk/audit.json); [search-indexed institutional description](https://fragmenta.kansalliskirjasto.fi/handle/10024/1300).

An independently published older catalogue, Toivo Haapanen, [*Gradualia, Lectionaria missae*](https://www.doria.fi/bitstream/handle/10024/100895/Verzeichnis_der_mittelalterlic.pdf?sequence=1), 1925, p.39, entry **64**, describes eight leaves of a gradual and transcribes among its reused-account inscriptions a 1611 provision account bearing the name **Christiern Philipsson**. Its format and description concern Mass chants, not the St Olaf/St Lawrence office material catalogued for Fr 20278. The catalogue groups several account dates and explicitly assigns some inscriptions to specific folios; the 1611 name-and-account inscription is **not explicitly assigned to a particular folio in the passage we read**. Its text is a catalogue transcription, not a new reading of the parchment.

The retained BOMPAC workbook calls the Finnish item **F.m.II.64** and puts its folios 6 and 7 in a single row with account year 1611. It assigns that row to **BOMPAC-11814**; Fr 20278 is in **BOMPAC-912**, and Fr 10370 in **BOMPAC-5324**. The checksum-checked [extraction](research/continuation_89/workbook_rows.json) and [script](research/continuation_89/check_reuse_control.py) preserve the exact fields. The two book-attribution systems and the 1925 source are not three independent readings of the same writing. The dated row supports a possible folio-level lead, but it does not by itself prove which folio bears the specific name in the earlier catalogue.

## What this controls

If the two 1611 account headings refer to the same historical person, and the documented gradual and antiphonal fragments are correctly distinguished, then that person's accounts were associated with material catalogued from **at least two different medieval books**. This would be a useful counterexample to treating a shared account holder and year as a unique book fingerprint. It also makes an administrative comparison of Fr 10370 and Fr 20278 interesting without making it decisive.

The identical patronymic and year do **not** alone prove the two historical people were identical, where or by whom each account was bound, or that the existing medieval group assignments are correct. Composite books, reuse from several books together, copying or catalogue errors, and detached-account histories remain possibilities. The 1610 Fr 10370 account was already attributed by the indexed IV.157 catalogue to a Christiern Philipsson and linked by the project to the `48:7` record; at E89 that was a source-based crosswalk, not an independent reading of the Fr 10370 account heading. E90 adds a provisional direct reading and keeps whether the 10370/II.64 accounts are the same open. Related or separate accounts are contextual evidence, not proof of a physical join, same workshop or original library.

## Result and next test

This is a **new-to-this-project, post-selection control drawn from published catalogues**, not an established historical discovery. It weakens any proposal to resolve the IV.156/IV.157 split solely through a name or date. It does not establish that Fr 10370 and Fr 20278 are different or the same book. The better test remains exact visible medieval text, side/folio marks and possible physical structure; if the historical reuse path is pursued, first verify the original account inscriptions and a non-circular identification of the official across records. Do not turn the suggested II.64 folio crosswalk into a proven one.

We inspected Haapanen's p.39 through the institutional repository's extracted PDF text and queried the previously retained workbook. No original image was examined or downloaded, no independent reviewer or historian checked the readings, and novelty beyond this project is unassessed. No source route was bypassed, no outreach was sent, and the image inventory and recorded transfer plan remain unchanged; web-reader traffic is unmeasured.

```sh
.venv/bin/python research/continuation_89/check_reuse_control.py
```

The script verifies the pinned workbook MD5 and extracts the three explicit rows. It checks provenance and arithmetic identifiers, not the old catalogue's transcription, historical identity or a physical relationship.
