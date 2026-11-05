# Research continuation E31: official Fragmenta relationship labels and a foliation lead

**Date:** 25 October 2026. **Question:** what do the official Finnish catalogue records say about same-codex relations versus suggestions among F.m.IV.156, IV.157, IV.173, Ant 99, Codex 1505, Fr 1385 and Hy 49?

## Result

The National Library of Finland's detailed Fragmenta entries use distinct labels for **same codex**, **suggested relation**, and a wider stylistic/liturgical group. The IV.157 entry identifies Ant 99 and Fr 1385 as from the same codex, but lists Codex 1505 as a suggestion. The IV.156 entry describes strong stylistic resemblance to IV.157 and also lists Codex 1505 as suggested. The directly opened IV.173 entry describes a wider group of at least 18 sources with uniform stylistic traits and Åbo-diocesan liturgical use; it identifies Ant 242/Fr 29666 as same codex, while Hy 49/Fr 25592 and Ant 99 are suggestions. It does not turn membership in that broad group into a same-book claim.

The IV.173 entry also says that the group's Naantali origin is strongly suggested by the provenance of one member, but cautions that production at the monastery cannot be directly deduced from the quantity or quality of surviving books and notes that export from Vadstena remains possible. The source itself therefore separates the broad group from a proven common codex or scriptorium attribution.

One precise test lead emerged. The IV.157 entry places the St Olaf office on folio 8 and gives its opening-signature notation as `[k] iiijr - k [v]`. Fr 8994's catalogue record notes old foliation `1r IIII; 1v k`; the Ant 99 catalogue record Fr 20278 also lists St Olaf and St Lawrence. These details may align, but their notation and side orientation have not been compared on both source images. This is a question to test, not a join or attribution.

## Interpretation and limits

This is useful source clarification and a narrower next test, not a new manuscript discovery. It supports keeping H03 unresolved (category C): the official catalogue says the Codex 1505 link is suggested, and the BOMPAC workbooks assign Codex 1505 and Ant 99 to different reconstruction units. Neither dataset supplies a fresh physical examination. The possible `k`/`IV` correspondence could sharpen the test if the relevant scans are available, but it cannot override those limits until the writing, folio sequence and chant boundaries are checked directly.

The IV.173 page opened directly through the normal web route. The detailed IV.156 and IV.157 entry text appeared in searches of the official Fragmenta pages, while direct opens returned HTTP 403; no access control was bypassed. The full printed discussion at Taitto 2001, pp. 161–168, and Keskiaho's 2019 chapter remain unread. No local image of Fr 20278 or F.m.IV.157 is present in the working image inventory, so the proposed three-way source comparison is not yet possible. The frozen queue, image inventory, predictors and thresholds are unchanged; no expert was contacted.

## Strategy consequence

Continue the existing goal; no replacement goal is needed. Narrow the next pass to an image-level check of the opening-signature and St Olaf sequence on Fr 8994, Fr 20278 and F.m.IV.157, using only normal official access. If either missing image cannot be obtained through a legitimate ordinary route, keep H03 at C and move to another predeclared source test rather than repeating broad metadata or similarity searches. The specific prior-art claim is now clearer, but originality is still not established.

## Sources and reproduction

- [Official Fragmenta entry for F.m.IV.156](https://fragmenta.kansalliskirjasto.fi/handle/10024/1299)
- [Official Fragmenta entry for F.m.IV.157](https://fragmenta.kansalliskirjasto.fi/handle/10024/1300)
- [Official Fragmenta entry for F.m.IV.173](https://fragmenta.kansalliskirjasto.fi/handle/10024/1314)
- [Structured result](research/continuation_31/fragmenta_relationship_results.json)

The review integration is reproduced with:

```sh
./.venv/bin/python research/continuation_31/integrate.py
./.venv/bin/python -m lost_library evidence
./.venv/bin/python -m lost_library export
```
