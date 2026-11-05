# Reconstructing Nordic Medieval Music Manuscripts: A Bounded Evidence Audit and Data-Quality Case Study

**Research manuscript for specialist review · 5 November 2026**  
Author, affiliation and acknowledgements: to be supplied by the project owner. No independent specialist review has been obtained.

## Abstract

Medieval parchment leaves reused in administrative bindings survive across Nordic collections. Computational similarity can help organize candidate relationships, but similar script, notation and liturgical contents do not demonstrate that fragments came from the same book. We report a bounded, AI-assisted investigation of ten predefined comparisons centred on Finnish and Swedish music fragments, together with an exploratory retrieval experiment and a separate audit of a published research dataset. Two comparisons reproduce published associations, one follows a published rejection and seven remain ambiguous. No new historical attribution or exclusion is established. In a small, catalogue-labelled, same-genre gallery, a metadata baseline achieved mean reciprocal rank 1.00 on 24 queries from four test groups, but its selected threshold accepted 40 of 72 catalogue-labelled different-group pairs; all nine tested methods also accepted a published different-book example. The result illustrates the distinction between retrieval within a selected gallery and identification of an unknown book. A separate check found that the combined dataset's column and leaf-count fields were equal for all 22,248 included Swedish records with numeric values; 5,598 of 14,415 eligible exact matches disagreed with original catalogue column values. These are field comparisons, not individually verified historical corrections. Missing images and literature, reference-exposed readings and lack of independent review limit both the historical claims and any claim of novelty. The contribution of this paper is a reproducible, qualified account of the investigation and its evidence limits; neither a new codex nor a general improvement in automated reconstruction is claimed.

**Keywords:** medieval manuscript fragments; liturgical manuscripts; fragment reconstruction; computational retrieval; provenance; data quality; Nordic collections

## 1. Introduction

Parchment from medieval manuscripts was reused in later bindings and administrative records, leaving related leaves dispersed among collections. Researchers have long reconstructed such books through textual, physical and historical evidence; the Fragmentology literature and the BOMPAC dataset provide established methodological and catalogue context [1, 2]. Our question is whether a small, transparent AI-assisted workflow can contribute evidence concerning relationships around Finnish F.m. IV.156, IV.157 and IV.173 and related Swedish fragments, without confusing resemblance with physical identity.

We distinguish a shared book from a shared scribe, workshop, liturgical tradition, repeated text, catalogue alias or later composite volume. Each explanation makes different demands on the evidence. The present case study records both positive and contrary observations, rather than treating a high matching score as a reconstruction. Its scope is a fixed set of ten comparisons and a documented Ant 49 investigation; it is not a census of Nordic fragments.

## 2. Materials and methods

### 2.1 Sources and units

The pilot's frozen catalogue contains 129 records representing 120 imaged physical objects. One object may have several captures and a catalogue record may describe more than one leaf; neither is automatically one independent book or one medieval side. Subsequent research used further images and catalogues, recorded separately in the project inventory. The Swedish source descriptions, Finnish institutional descriptions and combined BOMPAC records are attributed in the evidence dossiers [3–5]. Catalogue assertions, image readings and machine proposals remain separate. Some Finnish catalogue detail was available only through search-indexed text and may contain OCR errors. No original object was physically examined.

For the retrieval pilot, ten Swedish catalogue-defined reference groups contributed six selected records each, split by book into development groups 285, 270 and 875; calibration groups 1200, 609 and 276; and test groups 1104, 434, 920 and 674. Some planned queries were excluded because no different-book same-genre negative was available in their split: the same-genre evaluation used 12 development, 12 calibration and 24 test queries. Catalogue group labels are provisional and may inherit errors. A separate Beauvais control comprises twelve leaves of one manuscript, not twelve independent books. See [validation report](VALIDATION_REPORT.md) and [machine-readable results](data/validation.json) for inclusion rules and losses.

### 2.2 Comparisons and safeguards

Nine fixed methods combined catalogue metadata, image-layout descriptors and frozen ImageNet ResNet-18 representations. Metadata included available script, notation, dimensions, layout and date. Explicit codex and provider identifiers were excluded as predictors, but correlated or inherited catalogue attributes could still leak information. Images of one physical object were grouped to reduce direct leakage. Whole-book splits were used; test results were inspected in an earlier pilot, so the present analysis is not a new, untouched preregistered confirmation.

We retained the metadata baseline unless a more complex method improved mean reciprocal rank by at least 0.02 on both development and calibration partitions. Candidate readings, proposed text sequences, region coordinates and competing explanations were recorded alongside source links. AI-assisted readings were checked against available images or references, but repeated AI readings are not independent human corroboration. The ten relationship dossiers were frozen before the source-region review. Their internal categories are E, previously documented; D, previously rejected in published work; and C, unresolved. They are not independent expert verdicts.

### 2.3 Separate dataset audit

The BOMPAC combined workbook and separately published raw Swedish metadata were checked by checksummed inputs and exact fragment identifiers [3, 4]. We compared included Swedish records where both the combined `Columns` and `No_of_leaves` values were numeric. For a second comparison, we retained exact single-record links where both the raw `spaltenzahl` and combined `Columns` values were numeric 1 or 2. Selected retained source photographs were examined as examples, not as a representative validation sample. The newest listed combined CSV, v1.1 at the 4 November 2026 check, was separately compared with the pinned workbook in seven named fields [6].

## 3. Results

### 3.1 Retrieval and its limits

On the same-genre test gallery, the metadata baseline had P@5 0.95 and mean reciprocal rank 1.00, macro-averaged across four reference groups. Each eligible query had five relevant same-label gallery objects. No more complex method satisfied the prespecified development/calibration improvement rule. The high score is a result for this selected closed gallery, not an estimated probability of book identity.

At the selected calibration threshold, the metadata method produced 60 true positives, 40 false positives, zero false negatives and 32 true negatives across 132 same-genre test pairs, against the catalogue-derived labels. Precision was 0.60 and the false-positive rate was 40/72, or 0.556. This threshold analysis has a different denominator from the retrieval result. All nine methods accepted Fr 8201–Fr 8304, a published different-book comparison in Grajewski's study [7]. The paper's historical interpretation is a reference decision, not an independent improvement of the algorithm. A separately documented positive, Fr 1385–Fr 20274, ranked 26th in the wider physical gallery under metadata and was rejected at that threshold; it was examined after the initial pilot. These examples demonstrate the practical limits of the chosen workflow, without establishing population performance.

### 3.2 Frozen relationship screen

| Case | Comparison | Internal result | Basis and limitation |
|---|---|---|---|
| H01 | Fr 1385 / Fr 20274 | E | Previously documented association; no new physical join established. |
| H02 | Fr 1385 / Fr 10406 | C | Ornament and layout resemblance are not unique book evidence. |
| H03 | Fr 20274 / Fr 8994 | C | Published group assignments differ; opening-signature and Finnish-side evidence remain incomplete. |
| H04 | IV.173 / Fr 1385 | C | A broader stylistic group is distinct from an established same-book association. |
| H05 | IV.173 / Fr 25592 | C | Published suggested grouping conflicts with source catalogue dates and layouts; alternatives remain. |
| H06 | Fr 8201 / Fr 8304 | D | Published rejection, retained as a difficult negative [7]. |
| H07 | Fr 8201 / Fr 20106 | E | Published association [7]; Fr 20106 image not independently examined here. |
| H08 | Fr 1385 / Fr 4223 | C | Published reconstruction groups differ; a physical exclusion is not established. |
| H09 | Fr 1385 / Fr 8311 | C | Published reconstruction groups differ; shared chant context is not unique. |
| H10 | Fr 1385 / Fr 8455 | C | Published reconstruction groups differ; no new physical exclusion established. |

The three final suggestions are correlated members of the same published Ant 39 group, not three independent discoveries. Full provenance, alternative explanations and image regions appear in [the dossiers](EVIDENCE_DOSSIERS.md). The categories summarize our assessment of the bounded evidence; they do not count as a ten-case accuracy study.

### 3.3 Two unresolved historical tests

The Finnish indexed catalogue describes IV.156 f. 8 as ending within *O beate Iacobe* at `intercede]`, with an unexplained closing bracket. A retained Swedish photograph of Fr 10406 provisionally shows the same chant and a passage continuing beyond *intercede*. The published association already exists. The Finnish surface has not been inspected; neither the letters actually surviving there nor independent physical identity of the two pieces is established. Catalogue error, another occurrence of the chant, composite history and incorrect side or object mapping remain alternatives. Other catalogued sources attest the same chant sequence, limiting its specificity. The conditional comparison and counterexamples are documented in [E112](RESEARCH_CONTINUATION_112.md).

For IV.173 and Fr 25592, the BOMPAC reconstruction groups them, but preserves a 12th–13th-century source date for Fr 25592 and a fifteenth-century source date for IV.173. Its common fifteenth-century value is a harmonized field with the dataset's own conflict flag, not two independent datings. Fr 25592's retained images show a dense two-column hymn layout; IV.173 has a broad notated layout. Catalogue descriptions of other books, including a fifteenth-century Swedish gathering with different column counts, caution that layout alone cannot exclude a shared book. They do not resolve these particular dates or prove a connection. Date errors, different sections and composite volumes remain possible [E107](RESEARCH_CONTINUATION_107.md).

The St Anne hymn on Fr 8073 provisionally reads `mulier sancta` and `soluat a reatu` where published comparators have different words. This is a reference-exposed AI image reading, not an independent transcription. The Swedish catalogue identifies Fr 20441 as another witness to the hymn but its disputed stanza was not inspected. Prior occurrence, significance and novelty are unresolved [E74](RESEARCH_CONTINUATION_74.md).

### 3.4 Data-quality observation

In the pinned combined workbook, `Columns` equalled `No_of_leaves` for all 22,248 included Swedish records where both were numeric. Across 14,415 exact links with raw and combined column values both in {1, 2}, 5,598 differed. Another 6,543 exactly linked records had a blank raw column field and a numeric combined value of 1 or 2. These sets address different questions; blanks are not verified errors. Selected visible images of Fr 25592 and Fr 607 support their raw catalogue descriptions in opposite directions, but do not validate every side or every record. The newest listed combined CSV and the pinned workbook agree in seven relevant fields across 29,586 rows. The CSV is another representation of the same dataset, not independent confirmation. The duplication pattern suggests a possible mapping issue, but its cause, intended semantics, notice history and any correction outside the checked release remain unverified [6, 8]. This is a separate research-data observation, not evidence of a medieval attribution.

## 4. Discussion and limitations

The closed-gallery result shows that useful ranking can coexist with substantial false acceptance under a threshold and with failure on a historically difficult pair. Book separation, physical-object grouping and explicit negatives reduce particular sources of leakage; they do not remove dependence on catalogue quality or establish performance on unseen collections. The test contains only four reference books and was previously inspected. No general accuracy or calibrated identity probability follows.

The source-led analyses narrow what would have to be checked next. They do not prove that no novel relationship exists. Relevant Taitto and Keskiaho passages remain unread, several decisive source images and exact page mappings are unavailable, some comparative sources were read only via indexed text, and the AI-assisted readings were not independently reviewed. Separate BOMPAC and catalogue data can share provenance; their agreement is not independent physical confirmation. No claim of first notice is made for the data anomaly, textual readings or methodological observations. Neither institutional endorsement nor expert review is implied.

## 5. Conclusion

The defined investigation did not establish a new manuscript attribution, exclusion or historical discovery. It produced a reproducible set of case-level observations, controls and open questions, and a separately testable dataset discrepancy. The results are suitable as a **research manuscript for specialist review**, subject to author review, source verification and any changes needed for a chosen venue. A later reviewer can test the Finnish leaf, check the Fr 8073 transcription and compare the conflicting dating evidence using the linked regions and dossiers. No library or researcher was contacted as part of this review preparation.

## References

1. Duba, William. “Finding the Prior Leaf: Manuscript Fragments and Original Codices.” *Fragmentology* 6 (2023): 5–65. [https://doi.org/10.24446/j9en](https://doi.org/10.24446/j9en).
2. Eskola, Seppo. “Fragments Combined: A Comprehensive Dataset on Medieval Book Fragments in Stockholm and Helsinki.” *Fragmentology* (2025). [https://doi.org/10.24446/no5r](https://doi.org/10.24446/no5r).
3. BOMPAC. Combined Stockholm–Helsinki fragment research data, v1.1 as listed at the 4 November 2026 check. [https://doi.org/10.5281/zenodo.17511106](https://doi.org/10.5281/zenodo.17511106). Source workbook, checksums and field scope: [E108](RESEARCH_CONTINUATION_108.md), [E114](RESEARCH_CONTINUATION_114.md).
4. BOMPAC. Raw research metadata. [https://doi.org/10.5281/zenodo.17701360](https://doi.org/10.5281/zenodo.17701360). The retained Swedish MPO data also has a [separate deposit](https://zenodo.org/records/17287665). Dataset licences do not imply licences for underlying manuscript images.
5. National Library of Finland, Fragmenta membranea: [IV.156](https://fragmenta.kansalliskirjasto.fi/handle/10024/1299), [IV.157](https://fragmenta.kansalliskirjasto.fi/handle/10024/1300) and [IV.173](https://fragmenta.kansalliskirjasto.fi/handle/10024/1314). Some descriptions were read only in indexed form; see the source ledger.
6. Project audits [E111](RESEARCH_CONTINUATION_111.md) and [E114](RESEARCH_CONTINUATION_114.md), with reproducible checks and exact field scope.
7. Grajewski, Czesław. “Offices of St. Catherine of Alexandria: A Study of Parchment Fragments from Swedish National Archives (Riksarkivet).” *Liturgia Sacra* (2022): 287–315, especially p. 293. [https://doi.org/10.25167/ls.4818](https://doi.org/10.25167/ls.4818).
8. Project data audit [E108](RESEARCH_CONTINUATION_108.md), including exact source hashes, eligible records, counterexamples and reproduction command.

Further literature, sources read only in part and unavailable prior art are identified in [the bibliography](research/bibliography.ris) and [prior-art ledger](research/PRIOR_ART_LEDGER.md).

## Data, code and review status

The package contains the code, permitted source images, structured evidence, checksums and reproduction procedures. See [README](README.md), [data rights](DATA_RIGHTS.md) and [specialist review packet](REVIEWER_PACKET.md). Code licensing is an owner decision. AI assisted source discovery, analysis, transcription proposals and drafting; the project's logs preserve the limits and provenance of these uses. All factual and interpretative claims require responsible author review. The manuscript has not been independently peer reviewed or sent for specialist review.
