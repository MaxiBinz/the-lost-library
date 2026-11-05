# E87: Testing whether Eskola's reuse study applies to our candidates

**2 November 2026.** This is a bounded literature and metadata check, not a new attribution or provenance determination.

## What the study says

Seppo Eskola's peer-reviewed, open-access article, [“The Provenance of the Swedish-Finnish Manuscript Fragment Collection”](https://doi.org/10.24446/a8ny), *Fragmentology* 8 (2025), 5–45, investigates over 100 manuscripts reused in Johan's duchy in southwest Finland. It combines fragment reuse patterns, the accounts they covered and the officials involved. It differentiates locally and centrally reused material; reuse in one district does not automatically prove a particular medieval institution. Its named study population includes accounts from 1556–1562 and selected local reuse in 1563 (p. 18, note 27). It proposes broader application but explicitly calls for testing it and accounting for changing administrative conditions (pp. 43–45).

This is published work by a BOMPAC researcher, not our new method or an independent validation of BOMPAC's assignments. We inspected the publisher's machine-readable article text, including the sample definition and conclusions, and searched it for 8994, 10370, 156 and 157. Search did not locate the target shelfmarks; that is limited by PDF text extraction and how the author identifies manuscripts. We did not read the inaccessible 2008 or 2019 Keskiaho works by reading their bibliographic citations here.

## Targeted test against the existing workbook

The previously acquired and checksum-checked BOMPAC combined workbook assigns Fr 8994 and Fr 10370 with Finnish IV.156 to reconstruction 5324 and assigns IV.157/Ant 99 to 912. The reproducible [row extraction](research/continuation_87/reuse_audit.py) retains all included rows in those published units and writes their reuse fields to [reuse_audit.json](research/continuation_87/reuse_audit.json). It does not decide whether the units themselves are correct.

| Published unit | Included rows | Rows with numeric account year | Recorded year range | Recorded years 1556–1563 |
| --- | ---: | ---: | --- | ---: |
| 5324 / IV.156 group | 28 | 25 | 1588–1650 | 0 |
| 912 / IV.157 group | 20 | 18 | 1567–1630 | 0 |

These are account years in published metadata, not independently verified binding dates. Missing years, possible attribution errors, omitted or lost fragments, possible audit delays, and the study's own criteria prevent concluding from this query alone that neither original book could appear in its sample. The important practical point is narrower: **none of the dated included rows in these existing reconstructions falls in the stated study window**, so the article's specific results cannot simply be transferred to these leaves. The earliest dated rows of 912 are IV.157 ff.13 and 14 (1567 and 1568); the earliest in 5324 is IV.156 ff.23–24 (1588). The published metadata puts many IV.156 leaves on Karelia accounts from 1602–1604 and others elsewhere; an account's district is not automatically the location of binding or medieval use. Whether a dispersed pattern implies central reuse requires identification of the relevant records, scribes and administrative context, particularly outside the study period.

## Consequence for the research question

The study provides a strong **prior-art baseline and possible controlled follow-up**, but no new direct evidence for either the Fr 8994/IV.156 textual continuation or the Fr 10370/IV.156 versus IV.157 assignment. The two hypotheses remain unresolved; the most discriminating next evidence is still a lawfully available image of IV.156 f.8 or f.9 and a reliable side/number mapping. A future reuse study could examine the underlying accounts and officials across both candidates, with alternative reconstructions and controls specified before interpreting any geographic pattern. It would need to establish which records were actually covered, where and by whom, and assess late central versus local administrative routes rather than presume the earlier duchy result applies.

No image, manuscript, workbook, independent expert review, historical discovery, or contact was added. The frozen queue and decisions remain unchanged. Web text was read in the publisher's viewer; the paper's PDF was not saved locally. The working image inventory and conservative download plan remain as in E86; browser-reader traffic is unmeasured.

Reproduce the workbook extraction locally:

```sh
.venv/bin/python research/continuation_87/reuse_audit.py
```
