# Research continuation E32: local foliation mark and its diagnostic limits

**Date:** 25 October 2026. **Question:** does source inspection make the Fr 8994 opening-signature lead more specific, and how diagnostic is this signature convention?

## Result

I inspected the upper margin of the first retained Fr 8994 image. In the source-linked region, a small red mark visibly consists of four adjacent vertical strokes. This is consistent with the Swedish MPO catalogue's transcription of old foliation `1r IIII; 1v k`. The pixels confirm only the four-stroke mark in this capture; they do not independently identify its medieval side or securely read the paired `k` on another capture. The observation is linked to [a precise image region](data/observations.v9.json) and the source JPEG hash.

A second detail changes the weight of the clue. The official indexed description for F.m.IV.156 explains the opening-signature convention: a small red letter at the head of the verso paired with a Roman numeral at the head of the recto. It says that this practice was not infrequent in late-medieval codices and early printed books and points to Antiphoners 34, 157, 170 and 173. The `k`/Roman-numeral format alone is therefore not distinctive evidence for one codex. Fr 8994's St Olaf contents and F.m.IV.157's described folio-8 Olavi passage still define a precise test, but exact text, foliation sequence and side comparison are required.

## Source access and prior art

The official Finna record identifies Taitto's *Antiphonaria: text* (IV:1) as a digitized publication associated with Turku, and the NLF record exposes a digital-object URI. The page-viewer route had already returned `Cache miss` for the cited pages in E25. A new ordinary browser visit to the Finna record displayed a Cloudflare security-verification page. No verification was attempted or bypassed; no Taitto page text was obtained.

The University of Helsinki research portal confirms two distinct works by Jesse Keskiaho: the peer-reviewed 2008 journal article, pp. 318–350, and the peer-reviewed 2019 chapter, pp. 51–67. The official publisher's series page lists the 2018 volume containing the chapter. These routes provide bibliographic details, not the arguments in the two full texts. Both works and Taitto's cited pages remain unread; originality for H03 is not cleared. No paid copy was purchased.

## Interpretation and limits

H03 remains category C. The image now gives us a source-linked observation consistent with one catalogue foliation mark. The signature convention itself is documented as common enough that it cannot carry the claim alone. No Fr 20278 or F.m.IV.157 image was available for a paired comparison, and no exact Olavi text collation was completed. This update establishes no new attribution, exclusion, physical join, or originality claim.

The frozen ten-case queue, predictors, thresholds, and image inventory are unchanged. No expert was contacted, no image was downloaded, and no external catalogue or public site was edited. The goal remains active.

## Next test

If normal official access yields the missing images, compare the complete `k`/`IIII` opening-signature sequence, side orientation, and exact Olavi text and chant boundaries across Fr 8994, Fr 20278 and F.m.IV.157. Read Taitto pp. 161–168 and both Keskiaho discussions before stating novelty. If the images or texts remain unavailable or the feature proves commonplace, keep H03 unresolved and follow the existing frozen queue rather than amplifying the signature resemblance.

## Sources and reproduction

- [Official F.m.IV.156 catalogue entry](https://fragmenta.kansalliskirjasto.fi/handle/10024/1299)
- [Official F.m.IV.157 catalogue entry](https://fragmenta.kansalliskirjasto.fi/handle/10024/1300)
- [Taitto IV:1 Finna record](https://www.finna.fi/Record/fikka.3965551?lng=en-gb)
- [Keskiaho 2008 institutional record](https://researchportal.helsinki.fi/en/publications/en-grupp-handskrifter-fr%C3%A5n-slutet-av-1400-talet-fr%C3%A5n-n%C3%A5dendals-sc/)
- [Keskiaho 2019 institutional record](https://researchportal.helsinki.fi/en/publications/en-grupp-handskrifter-fr%C3%A5n-n%C3%A5dendal-nya-r%C3%B6n/)
- [Publisher's Scripta maiora catalogue](https://www.medievalia.nu/skriftserien/scripta-maiora/)
- Structured result: [research/continuation_32/results.json](research/continuation_32/results.json)

Reintegrate and reproduce the evidence export with:

```sh
./.venv/bin/python research/continuation_32/integrate.py
./.venv/bin/python -m lost_library evidence
./.venv/bin/python -m lost_library export
```
