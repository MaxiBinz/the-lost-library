# E99: the contested Catherine reconstruction's dating conflict

**3 November 2026.** E98 improved the review package but did not resolve the Fr 8994 mark. This pass checks a different existing problem: the competing published claims about Fr 8201, Fr 8304 and Fr 20106 in Ant 49. The source audit was selected after the records and earlier disagreement were known; it is not blind.

## What the dataset actually says

All eight records in the pinned [BOMPAC combined workbook](https://doi.org/10.5281/zenodo.17511106), reconstruction **BOMPAC-4861**, are marked as included. Six retain the original catalogue date **15th century**; two, Fr 20106 and Fr 20107, retain **14th century**. Yet the separate, harmonized `Dating_BOMPAC` field reads **1301–1400 for all eight**, and every row explicitly carries `Dating_BOMPAC_conflict = Conflict`. The exact rows, column-cell references and file checksum are in [results.json](research/continuation_99/results.json).

The dataset's own readme, PDF pp. 2–3, says that conflicting dates within a reconstructed unit are harmonized by preferring the narrowest range, then the earlier value, and that the original dates and conflict field remain available. The six-versus-two pattern and equal-century ranges are consistent with this documented rule. These are not eight independent 14th-century datings, and the conflict flag is **the dataset's own notice**, not an error newly discovered by this project. The audit does not independently establish which date is right or why the individual cataloguers chose it.

The [2022 Catherine study](https://doi.org/10.25167/ls.4818), p. 293, already notes differing dates while associating Fr 20106 with Fr 8201 and separating Fr 8304. The dataset puts all three in the same unit. As explained in [E48](RESEARCH_CONTINUATION_48.md), these are competing published reconstructions; the group-wide harmonized date cannot be treated as independent evidence for either joining or separating the fragments. Fr 20106's original has not been inspected here, so neither the published association nor exclusion is newly adjudicated. Shared original catalogue fields can also be inherited, and the project matcher uses catalogue date as one weighted input rather than an independently verified date.

## Consequence

Retain the two source date descriptions and the dataset conflict beside the published book-identity disagreement. Do not use the harmonized date as an independent palaeographical observation, silently replace the source dates, or treat the earlier century as established. The best historical test remains the exact Fr 20106 original, its side/extent and the Catherine boundary; dating would require an independent source-specific assessment with suitable controls. No novelty, new attribution, physical exclusion or independent review is claimed.

Reproduce the eight-row extraction from the already checksum-verified local workbook:

```sh
.venv/bin/python research/continuation_99/audit.py
```

The script verifies the original workbook's hash and exact eight source identifiers; it records values rather than adjudicating dates. No source was downloaded, no matching model or frozen review was modified, and no external contact or publication occurred. The research goal remains active.
