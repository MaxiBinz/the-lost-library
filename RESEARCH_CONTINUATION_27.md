# Research continuation E27: reconciling the F.m.IV.173 candidate group

**Date:** 24 October 2026. **Question:** how do the updated Fragmenta description and the 2025 BOMPAC workbook handle F.m.IV.173, Ant 242/Fr 29666, Hy 49/Fr 25592, Ant 99, and the IV.157/Fr 1385 group?

## Finding

The National Library's public F.m.IV.173 record distinguishes several levels of relationship. It identifies Ant 242/Fr 29666 as from the same codex; lists Hy 49/Fr 25592 and Ant 99 as additional suggestions, with the Ant 99 suggestion attributed to Keskiaho 2010; and describes a larger stylistic/liturgical group. The deposited MPO note for Fr 29666 independently states that it is the same codex as Helsinki Ant 173, citing Taitto 2001, p. 185, while asking readers to compare Hy 49. These are published catalogue claims, not new observations in this project. [Fragmenta F.m.IV.173](https://fragmenta.kansalliskirjasto.fi/handle/10024/1314)

The checksum-verified BOMPAC combined workbook places F.m.IV.173, Fr 29666/Ant 242, and Fr 25592/Hy 49 together in **BOMPAC-9531** (three included rows). It places Ant 99/Fr 20274–20278, F.m.IV.157, and Fr 1385 in **BOMPAC-912** (20 rows), while Fr 8994/Codex 1505 and F.m.IV.156 belong to **BOMPAC-5324** (28 rows). The reproducible query is in [the script](research/continuation_27/related_unit_crosswalk.py) and [machine result](research/continuation_27/related_unit_crosswalk_results.json); it checks the combined and raw-workbook MD5s published with the [combined](https://doi.org/10.5281/zenodo.17511106) and [raw metadata](https://doi.org/10.5281/zenodo.17701360) records.

This clarifies the prior-art picture without deciding the history. BOMPAC's F.m.IV.173 unit agrees with the explicit Ant 242 link and groups Hy 49 with it, but leaves Ant 99 in the IV.157 unit. The current Fragmenta description calls Ant 99 a suggestion within a broader group; it does not say that Ant 99 is a proven same-codex member of IV.173. The sources therefore cannot be reduced to one simple “all these leaves are the same book” claim. Nor does BOMPAC's unit split independently disprove a shared hand, workshop, production group, or more complex history.

The image comparison already in H05 remains unresolved: the available IV.173 photographs show a large one-column music layout, while the four Fr 25592 captures show a denser two-column hymn layout. A codex can contain different sections, so this difference is a reason to test the proposed relation, not a stand-alone rejection. The Fr 25592 metadata also carries a date conflict. Fr 29666, the stated positive comparator, has no verified local image.

## Access check and limits

I opened Fr 29666's ordinary Riksarkivet MPO catalogue URL from its published dataset reference. It displayed a human-verification CAPTCHA. I did not interact with it or try another route around it, and no image was downloaded. This is one route-specific result; it does not show that the record or image is generally unavailable. The comparison can continue from the already-published records and images, but direct image validation of the accepted Fr 29666 association remains pending.

E27 used no new manuscript images, no model scores, and no physical measurements. It establishes a source crosswalk and a prior-art difference, not a novel attribution, exclusion, hand identification, or independent expert verdict. The frozen ten-case queue and baseline predictors remain unchanged. H03, H04, and H05 remain category C.

## Consequence for the next research step

Keep the existing goal active. Narrow source review around the distinctions in the published claims: same codex, shared production/style, and suggested relationship. Where legitimate images are already available, compare diagnostic text/music, openings or signatures, ruling, and physical structure; do not treat a BOMPAC unit or one broad visual resemblance as proof. For the specific Ant 242/IV.173 check, an ordinary authorized image route for Fr 29666 would be useful, but local work can continue without it. The exact Taitto pages and the Keskiaho chapter remain unread, so originality remains uncleared for claims they address.

## Reproduction

From the project root, run:

```sh
.venv/bin/python research/continuation_27/related_unit_crosswalk.py
.venv/bin/python research/continuation_27/integrate_context.py
```

The first command checks the official published checksums and reports the selected included rows. The second adds CTX09 and updates the H03–H05 review context while asserting that the frozen queue hash remains unchanged. Neither command accesses the network or changes manuscript images.
