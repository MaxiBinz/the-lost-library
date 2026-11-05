# E33: Fr 8994 text changes the opening-signature test

25 October 2026. Four native-width versions of existing Riksarkivet photographs were acquired from their cached official IIIF manifest, under its Public Domain Mark. They add 1,261,947 download bytes and four image files, with no new physical object. Original pixels, primary predictors and the frozen ten-case reviews remain intact. Receipts include a failed local DNS attempt before the successful network-enabled acquisition; no archive access restriction was encountered on this IIIF service.

## Direct observations

The numeral-bearing photograph clearly shows the red four-stroke sign already observed in E32. It also has an abbreviated red rubric beginning `In .iij°.` and the black-text incipit `Nec propria salute contentus`. The rubric is provisionally expanded as **In tertio nocturno**. Another photograph shows an upper-margin red `k` and the candidate responsory incipit `Deuenerat martir`; another shows `Egre / gius mar / tir olauus`. Literal readings, expansions, five exact regions and image hashes are recorded separately in [the E33 observations](research/continuation_33/observations.json).

These are partial photographs of the catalogue's one-leaf object. Their ordinals do not establish recto/verso or a complete physical stitch. A modern [performance booklet](https://www.lawostore.no/assets/files-rte/booklet_lawo/LWC1106_Consortium_Vocale_Historia_Sancti_Olavi_Ebooklet_lettersize.pdf) supports identifying the incipits within the third nocturn of the St Olaf office; it is not an independent transcription of Fr 8994, and supplies no target melody or distinctive variant.

## A conditional conflict rather than a simple match

The [official indexed Finnish catalogue](https://fragmenta.kansalliskirjasto.fi/handle/10024/1300) describes F.m.IV.157 f.8 with the notation `[k] iiijr - k [v]` and text from the **first** nocturn, within *Regnante illustrissimo* through the beginning of the verse of *Iustus vero*. Its ff.9–10 begin *Egregius* in the **third** nocturn at a later stated signature range.

Thus the same-address interpretation proposed in E31 now has counterevidence: Fr 8994's numeral-bearing photograph reaches the third nocturn, unlike the Finnish catalogue's first-nocturn f.8 range. If both addresses are the same unique unrepeated location in the same section/service, that is incompatible with a straightforward single-book attribution. Those premises remain unverified. Bracketed components in the Finnish notation are supplied, its own description warns about interleaved units, and repeated numbering, composite structure, duplicated offices, side mapping and catalogue/OCR error remain alternatives. H03 remains C in the preserved review; no unconditional same-codex exclusion is established.

This is a new local source comparison, with **no first-notice or novelty claim**. The full Taitto discussion and relevant Keskiaho publications remain unread. The next highest-value test is to inspect Finnish f.8 and ff.9–10 and determine the actual numbering units, followed by exact text/side comparison. Fr 20278 remains a missing comparator.

## Access and reproduction

The official index lists a whole-fragment PDF, 28 TIFFs and Public Domain Mark for IV.157. The ordinary browser record and the separately documented OAI-PMH metadata route displayed verification pages, left untouched. The Finnish listing is not a fetched or inspected scan. No guessed bitstream route, restriction bypass, contact, upload or publication occurred.

```sh
./.venv/bin/python research/continuation_33/check_sources.py
```

The check verifies saved image bytes, dimensions and region bounds and writes the [structured comparison](research/continuation_33/results.json). It does not reproduce a human/AI reading or prove historical truth. Acquisition is not required for offline replay. These observations are a dated overlay for the amended lead register and knowledge model; they do not overwrite historical E31/E32 reports or frozen reviews.
