# E82: auditing the Turku II.157 shelfmark

**E83 correction:** A handlist attributed to the same cataloguer explicitly associates museum fragment C with IV.156. This is substantial contrary evidence to preferring IV.157; neither intended replacement is established. The bounded shelfmark inventory below is unaffected. [E83](RESEARCH_CONTINUATION_83.md).

2 November 2026. **Result: the literal shelfmark is a stronger candidate for a catalogue-reference error, but the proposed replacement IV.157 is not confirmed.** The earlier content comparison [E81](RESEARCH_CONTINUATION_81.md) explains why IV.157 is plausible. This pass tests whether the II.157 form fits the institution's documented numbering and a pinned research dataset.

The National Library's [IIa collection page](https://fragmenta.kansalliskirjasto.fi/handle/10024/3), read through indexed text, reports 129 catalogue items. Its [collection guide](https://fragmenta.kansalliskirjasto.fi/page/esittely) distinguishes the gradual and lectionary divisions and reports 129 graduals and seven lectionaries. A separately published [2026 inventory](https://www.doria.fi/handle/10024/195377) describes its coverage as the gradual fragments II.1–129. These counts and the inventory's coverage support the interpretation that the usual unlettered gradual sequence ends at 129; the 2026 inventory's coverage statement alone is not proof that no unusual number exists.

To test the number sequence in a separate available artifact, [the audit script](research/continuation_82/audit_shelfmarks.py) scanned all 29,586 rows, including excluded rows, of the checksum-verified published [BOMPAC combined workbook](https://doi.org/10.5281/zenodo.17511106). Each of its `Fr_reference`, `FM_signum` and `FM_signum_BOMPAC` fields contains all 129 distinct II numbers 1–129, IIb numbers 1–7, and no explicit II.157 match under the recorded pattern. IV.157 produces 48 matching cell occurrences in those fields, a positive control for the parser, **not** 48 distinct fragments. The [machine-readable output](research/continuation_82/workbook_inventory.json) retains field-specific number sets, matching rows and checksums. A workbook is not an exhaustive historical or current catalogue, and the scan covers only three fields and specified formats.

This is **not three independent counts of the manuscripts**: the institutional summary, the 2026 inventory and BOMPAC use or describe related collection data. Nonetheless the institutional series size, documented II.1–129 coverage, complete workbook sequence and separately documented IV.157 content make a literal II.157 reference difficult to reconcile with the normal current shelfmark system. An obsolete alias, an exceptional or omitted record, a transposed identifier, or a different referent remains possible. The observed reference problem and the hypothesized IV.157 emendation are distinct propositions: neither the intended shelfmark nor the cataloguer's sewing-hole evidence has been independently confirmed. First notice and novelty are unknown.

## Specific follow-up and scope

Check a reliable historical concordance or the cataloguer's original supporting material for the intended shelfmark; separately reconcile Turku museum fragment C with archive Ms. c and inspect relevant originals where legitimately available. If the intended reference is confirmed, preserve the original `II.157`, the evidence for a corrected form, and the relationship and physical-placement questions separately. The [reviewer packet](REVIEWER_PACKET.md) records these concrete questions; no message has been sent.

No manuscript image, article or dataset was newly downloaded. The web evidence above is indexed source text, not a newly opened complete IIa catalogue. No frozen hypothesis or historical book decision changed. No new codex attribution, verified correction, independent expert review or originality claim is made.

Reproduce the local scan:

```sh
.venv/bin/python research/continuation_82/audit_shelfmarks.py
```
