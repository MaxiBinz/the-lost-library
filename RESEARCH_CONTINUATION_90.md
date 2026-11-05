# E90: Reading the Fr 10370 reuse heading

**E91 follow-up:** The published II.64 ff.6–7 and Fr 10370 workbook rows report substantially different written areas and different contents/record extents. This cautions against treating the rows as an obvious physical alias, while the actual II.64 heading leaf and comparability remain unverified. [E91](RESEARCH_CONTINUATION_91.md).

**2 November 2026.** E89 identified a possible control in an older catalogue, but had not read the later account heading on the retained Fr 10370 image. This pass examines that heading directly. The image and name were already known, so the reading is exploratory, unblinded and reference-assisted.

## What the image shows

The [retained Riksarkivet photograph](data/images/mpo-10370-capture-4-1742px.jpg), viewed rotated 90° counter-clockwise, shows a large heading approximately **Christiern Philipsson[s?]**. The far right of the name is obscured by a folded corner. The following line appears to contain **Reckenskap för Proffianten** and **Finlandh**. A smaller line appears to contain the years **1610** and **1611**, while a large **1610** is separately visible underneath. These are provisional visual readings, not a full diplomatic transcription or a specialist's reading of early modern Swedish. The [existing source-image annotation](research/continuation_51/observations.json) `I51-10370-reuse-heading` identifies the original unrotated pixels. Its source capture hash and dimensions are rechecked by [the local recording script](research/continuation_90/record_evidence.py).

This provides direct image support for the prior catalogue's association of the 1610 wrapper with the named person; it does not establish medieval page orientation, book identity or the historical person's biography. The image was previously inspected for the existence of an account heading in E51, but the name, account subject and dates were not transcribed there.

## A more specific comparison—and a new alternative

Haapanen's [1925 catalogue, p.39 no.64](https://www.doria.fi/bitstream/handle/10024/100895/Verzeichnis_der_mittelalterlic.pdf?sequence=1), records a truncated heading for a **Christiern Philipsson provision account**, mentions **Finland** and gives **1611** in its description of the gradual assemblage II.64. The BOMPAC record assigns II.64 ff.6–7 an account year of 1611, but Haapanen's read passage does not explicitly put his named heading on those leaves. The 1925 text is an older catalogue reading, not a second direct observation made in this pass.

The name, type of account, region and year therefore overlap more specifically with the Fr 10370 image than E89's same-name comparison alone suggested. This raises a useful archival question: **do the two descriptions refer to related or separate provision accounts, or is there an unrecognized record/object cross-reference?** This is a hypothesis to investigate, not an identified duplicate or joining fragment. Similar administrative headings can recur; Haapanen's ellipses omit the details needed to establish identical wording or dates. We cannot establish whether the same person, same account, same binding, or same piece of parchment is involved. Different book types, catalogue units and described measurements must also be assessed before accepting any physical identification. Fr 20278's separately catalogued 1611 *customs* account remains a third record, not the provision account by default.

## Next test and limits

Compare an authenticated view or exact archival description of **II.64 ff.6–7** with the entire Fr 10370 heading, including handwriting, wording, date range, folio shape and current/earlier account identifiers. Check that those are the leaves that actually carry the heading before treating them as a comparison. Distinct contemporary accounts, a repeated title, a catalogue error, a composite or secondary reuse, and a mistaken reading are all plausible alternatives. This question is separate from the medieval Fr 10370 / IV.156 f.8 opening conflict and from the previous IV.157 placement.

No Finnish image, underlying account or independent reading was obtained. Neither a same-account claim, a physical crosswalk, nor a new medieval codex is established; first notice is unknown. The existing region was reused, with no additional source image or downloaded file. [Structured results](research/continuation_90/results.json). The frozen research decisions remain unchanged.

```sh
.venv/bin/python research/continuation_90/record_evidence.py
```

The script verifies image identity and the existing region link; it does not validate the paleographic reading or any historical conclusion.
