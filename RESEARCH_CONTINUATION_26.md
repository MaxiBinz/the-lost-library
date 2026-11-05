# Research continuation E26: target rows in the BOMPAC datasets

**Date:** 24 October 2026. **Question:** do the published BOMPAC workbooks already record the target Stockholm–Helsinki groupings, and what exactly do those records claim? This is a prior-art audit, not a new image-attribution test.

## Finding

The row-level BOMPAC payload is now downloaded, checksum-verified against the published Zenodo MD5 values, and inspected. The combined workbook contains one row per fragment, 69 columns and 29,586 data rows. The query retained only rows whose `Row_exclusion` field says `Include row`.

The combined dataset assigns Fr 8994, Fr 10370, Fr 10406, Fr 10407 and Fr 10437, together with the 23 listed F.m. IV.156 folio entries, to reconstruction **BOMPAC-5324** (28 included rows). It assigns Fr 1385 and Fr 20274–20278, together with the 14 listed F.m. IV.157 folios, to **BOMPAC-912** (20 included rows). The workbook places Fr 8994 and Fr 20274 in separate reconstructed units.

The raw MPO workbook shows how the Swedish-only and combined records differ. It groups the five Codex 1505 fragments as `M-1217` (five entries), Fr 20274–20278 as `C-35` / Ant 99 (five entries), and Fr 1385 by itself as `F-1385` (one entry). The combined BOMPAC workbook then brings the Ant 99 records, Fr 1385 and IV.157 folios together under BOMPAC-912. For the listed target rows, the raw workbook's explicit ambiguity and correction cells are blank; blank cells are not proof that every underlying historical attribution is certain.

The source metadata also clarifies why the Taitto volume matters. The preserved raw MPO note for Fr 8994 describes it as similar to Ant 99 and Helsinki Ant 156/157 and cites Taitto 2001, pp. 161–168; it also points to Fr 1385. The Fr 1385 note calls that fragment the same manuscript as Taitto's Ant 157. Those are two different strengths of statement: resemblance is not identity. The combined dataset's row fields show the same broad profile for Fr 8994 and Fr 20274—both antiphonaries, Quadr notation, four music lines and close written-area dimensions—while assigning them to separate BOMPAC units. That compatibility is not enough to override the unit split.

The dataset readme describes BOMPAC units as reconstructions of once-intact manuscripts, while also warning that the inherited CCM, Codex and FM signa can overlap and may not cover every fragment thought to come from a codex. It calls the combined workbook research data prepared for the BOMPAC project, rather than institutional catalogue data. The raw-metadata readme says the underlying research metadata is incomplete and work-in-progress. These qualifications matter: the spreadsheet records a published reconstruction, but it does not provide fresh image-based proof, a second independent adjudication, or a guarantee against later revision.

## Effect on the project

This closes an important gap in the earlier prior-art audit: target-level BOMPAC rows are no longer unknown. The broad claim that our project independently links Stockholm and Helsinki fragments is already established prior work. More specifically, BOMPAC's published grouping separates Fr 8994/Codex 1505/IV.156 from Fr 20274/Ant 99/IV.157. Any future claim that these targets belong to one book would need unusually clear, source-visible evidence and a direct account of why it revises that existing reconstruction.

This result does **not** prove that the BOMPAC grouping is correct or that the manuscripts have no subtler shared relationship. It does not resolve hand, workshop, textual dependence, or composite-history possibilities. Local H03 therefore remains **C / unresolved**, and the frozen ten-case queue remains unchanged. Reproducing BOMPAC's own rows is not a new scientific discovery.

The strategy should now narrow from broad family mapping to one falsifiable challenge: read the exact Taitto passage cited by Fr 8994, then compare complete corresponding text, foliation/quire evidence and diagnostic physical features against the BOMPAC split. The National Library's viewer has been tried through both the web reader and an ordinary browser; the former returned `Cache miss` and the latter displayed a security check. A separate [Finna catalogue record](https://www.finna.fi/Record/fikka.3965551) also displayed a security check in a normal browser. No challenge was solved or bypassed, and this does not prove that the book is restricted or universally unavailable. The [National Library's open-data record](https://data.nationallibrary.fi/bib/me/W00057022000) confirms the 2001 text volume and digital-object link, but the specific pages remain unread. Do not use generic staff spacing, similar dimensions or cross-collection integration as novelty evidence. If no distinctive evidence survives, a well-supported replication/negative report remains the honest outcome. A specialist review becomes most useful once that compact, source-linked claim exists; it is not needed to run the remaining local tests.

## Reproduction and source files

Run from the project root with Python that has `openpyxl` available:

```sh
python research/continuation_26/bompac/target_crosswalk.py
```

The script verifies all five published MD5 checksums, queries the combined and raw MPO sheets in read-only mode, and writes [target_crosswalk_results.json](research/continuation_26/bompac/target_crosswalk_results.json). The original workbooks and readmes are under `research/continuation_26/bompac/`. Official records: [Stockholm–Helsinki combined dataset](https://doi.org/10.5281/zenodo.17511106) and [BOMPAC raw metadata](https://doi.org/10.5281/zenodo.17701360). The peer-reviewed introduction to the combined dataset is Eskola, “Fragments Combined,” [Fragmentology 8 (2025), pp. 233–240](https://doi.org/10.24446/no5r).

No model, image similarity score, new manuscript image, independent expert judgment, queue edit, contact, or publication was involved in E26.
