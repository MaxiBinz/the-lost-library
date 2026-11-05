# The Lost Library — Phase 0 feasibility report

> Phase 0 deliverable. Later pilot files in this workspace belong to a separate, currently paused implementation goal. This report preserves the feasibility evidence and decision; subsequent experiments are not presented as Phase 0 results.

**Evidence gathered:** 19–20 October 2026, Europe/Vienna. **Delivery review:** 21 October 2026.  
**Decision:** **CONDITIONAL GO** for a small, specialist-reviewed validation pilot; **no authorization to begin Phase 1 is assumed**.  
**Finding:** Real images and useful metadata exist. An original manuscript relationship has **not** been established, and a sufficiently adjudicated, multi-codex Nordic benchmark has **not** yet been assembled.

## 1. Executive assessment

AI-assisted retrieval is technically plausible and worth a bounded test. This does not yet establish that an independent project will discover an unknown association. The strongest initial technical control is the **Graduale Aboense, Helsinki F.m.II.44 / Swedish MPO Codex 1104, CCM Sequ 42**. The strongest provisional discovery question is narrower: **can a documented uncertainty in the membership of late-fifteenth-century Åbo/Nådendal antiphonal fragments be resolved or extended with independently reviewable evidence?** The latter must first be checked against current scholarship and curatorial knowledge.

Three findings materially change the original premise:

1. The Swedish 2025 export actually contains **22,909 catalogue records**, of which **15,788 (68.9%)** have IIIF manifest URLs. Neither number is a count of successfully downloaded images or distinct medieval books. We retrieved a small, deliberately selected image sample; it supports access feasibility, not collection-wide coverage.
2. **Stockholm–Helsinki integration already exists.** BOMPAC's *Fragments Combined* dataset and publication already harmonize the collections. CODICUM explicitly pursues cross-collection reconnection and virtual reconstruction. Combining the datasets or creating a virtual library would not by itself be an original contribution. [MPO export](https://zenodo.org/records/17287665); [BOMPAC dataset](https://doi.org/10.5281/zenodo.17511106); [Fragments Combined](https://doi.org/10.24446/no5r); [CODICUM objectives](https://www.codicum.eu/about).
3. **Beauvais is a usable positive control, not a complete benchmark.** Its images are retrievable and its scholarly reconstruction provides known associations, but it is one French missal. Mixed rights, imperfect image references, identity reconciliation, difficult negatives, and independent Nordic test books remain to be addressed. [Beauvais reconstruction](https://fragmentarium.ms/overview/F-4ihz).

**Single recommended investigation:** an **attribution and exclusion audit of the Åbo/Nådendal antiphonal family centred on F.m.IV.157**, comparing its documented associates with the qualified links involving **F.m.IV.156, IV.173 and Swedish MPO Codex 1505**. Treat this as a family and competing catalogue interpretations, not one authenticated book. Read the later Keskiaho 2018/2019 chapter before claiming that any attribution remains new. Graduale Aboense is the technical positive control; Beauvais is supplementary validation. Ege leaves offer an easier demonstration but a weaker immediate originality case; legal manuscripts have good examples of access but no better unresolved target was verified here.

During this Phase 0 assessment, no visual AI model was trained or run, and no new join is claimed. A small **retrospective metadata-ranking diagnostic** was executed during the feasibility continuation: it shortlisted documented positives but ranked a published different-book pair uniquely first and excluded a known positive with missing metadata. This is a demonstrated baseline failure, not validated AI performance. Phase 0 used no paid API, cloud compute, large-model training, full reconstruction or public website. The six maintained research records and explicit ranking are linked at the end.

## 2. Evidence standard and scope

This report distinguishes:

- **Observed:** direct HTTP responses, downloaded metadata, decoded image samples, and live catalogue inspection.
- **Documented:** statements in institutional catalogues or identifiable scholarly publications, including counts not independently enumerated here.
- **Proposed:** experimental design, resource estimates, thresholds, and possible future outputs.
- **Unresolved:** access, physical identity, scholarly status, or licensing not sufficiently established.

The count hierarchy is **original codex → surviving physical fragment/bifolium → leaf → recto/verso → image capture/canvas**. A Finnish shelfmark can represent an already reconstructed group of leaves. An MPO row can represent several leaves. A manifest may contain extra photographs, covers, or repeated views. These units must never be added together without a crosswalk. Known textual continuity, same-codex identity, physical joins, adjacency, and shared workshop/hand are different claims.

This was a targeted feasibility investigation, not an exhaustive bibliography, current missing-leaf census, or expert codicological examination. No scholar or institution was contacted. Consequently, silence in a database or an empty literature field is never taken as evidence that a relationship is unknown.

## 3. Verified data access

### 3.1 Swedish MPO: a real, usable metadata export

The [Zenodo record](https://zenodo.org/records/17287665), published 9 October 2025, version 1.0.0, supplies `mpo.csv`. Both the record API and the complete **9,873,242-byte** metadata file returned HTTP 200. Its MD5 matched the advertised `bac851653aa9b0816208a13430154cfb`. This is a small metadata download, not a bulk image download. The export is **CC0**; its metadata licence does not determine every image's rights.

Offline parsing found **22,909 rows, 37 fields, no duplicate nonblank `signatur` identifiers, and 15,788 distinct nonblank manifest URLs**. This enumerates the versioned export, not every current catalogue record. Cataloguing largely dates to 1995–2004; the deposit explains that image-viewer and IIIF links were added in 2025. Publication date is therefore not the date of a complete scholarly reassessment. [Export and schema](https://zenodo.org/records/17287665).

| Filtering or interpretation field | Populated rows / 22,909 | Implication |
|---|---:|---|
| `iiif_manifest`, `bildbetrachter` | 15,788 each, 68.9% | Image pointers; coverage and quality require live tests |
| `sachtitel` | 20,018, 87.4% | Useful manuscript-type filtering |
| `datierung` | 17,265, 75.4% | Broad, uncertain textual dates, not precise production years |
| `format` | 12,355, 53.9% | Often damaged/trimmed dimensions; not original leaf size |
| `schriftraum1` | 11,891, 51.9% | Useful written-space comparison where present |
| `schrift` | 11,264, 49.2% | Broad script labels, not scribal identity |
| `notation`, `notenlinien` | 10,977 / 10,397 | Music-type and staff evidence; blanks do not prove no music |
| `codex` | 6,792, 29.6% | Existing group labels; not reliable gold truth without checking |
| `entstehungsort` | 3,864, 16.9% | Geographic filtering is sparse and often tentative |
| `literatur` | 326, 1.4% | Clearly insufficient for novelty checking |

There are **1,704 distinct populated codex labels**, not 1,704 total surviving books. Blank codex values are unrecorded assignments, not proof of a separate unknown book. Exact title matches give **2,100 Antiphonarium rows, 1,626 with manifests**, and **1,322 Graduale rows, 1,004 with manifests**: a combined **3,422 records / 2,630 image pointers** before date, identity, or quality review. Variant titles are omitted from these deliberately conservative exact-string counts. [Reproducible profile](research/mpo_profile.json); [executed notebook](research/metadata_audit.ipynb).

The 37 columns cover MPO and CCM identifiers; holder/manager; archival reference, account-book collection and reuse year; material; leaf, column and line counts; dimensions; written space; damage and quire observations; script; rubrication; notation and staff lines; remarks; subject/type/title/author; origin/use; dating; printed-book identity; codex label; literature; contents; and viewer/manifest links. The [institutional search form](https://sok.riksarkivet.se/en/mpo) also explains uncertainty and measurements, including dimensions rounded to 0.5 cm. Preserve markers such as `*`, `?`, and `#` rather than coercing them into clean numbers. `bestandssignatur` is a reuse/account reference, not the medieval manuscript's production date.

### 3.2 Swedish IIIF and actual image retrieval

Seven musical records were selected for meaningful known associations and a difficult comparison: MPO **7957, 7960, 7961, 8343, 8344, 8201, 8304**. These are a purposive sample, not a random coverage estimate. The initial run successfully fetched **six manifests, six `info.json` responses, and six 800-pixel-wide JPEGs**; record 8304 timed out. One targeted retry retrieved 8304's manifest, making **seven successfully retrieved manifests in total**, but its image was not tested. The advertised direct native-image URL for 7957 and a retry through its explicit v3 service both timed out; native-size JPEG byte retrieval remains unverified.

| Record | Actual tested sample URL | Initial result | First image service's native dimensions |
|---|---|---|---:|
| 7957 | [JPEG](https://lbiiif.riksarkivet.se/v3/arkis!R1007957_00001/full/800,/0/default.jpg) | HTTP 200, 120,068 bytes | 1213 × 1733 |
| 7960 | [JPEG](https://lbiiif.riksarkivet.se/v3/arkis!R1007960_00001/full/800,/0/default.jpg) | HTTP 200, 138,550 bytes | 1102 × 1760 |
| 7961 | [JPEG](https://lbiiif.riksarkivet.se/v3/arkis!R1007961_00001/full/800,/0/default.jpg) | HTTP 200, 139,539 bytes | 1201 × 1778 |
| 8343 | [JPEG](https://lbiiif.riksarkivet.se/v3/arkis!R1008343_00001/full/800,/0/default.jpg) | HTTP 200, 117,811 bytes | 1264 × 1757 |
| 8344 | [JPEG](https://lbiiif.riksarkivet.se/v3/arkis!R1008344_00001/full/800,/0/default.jpg) | HTTP 200, 142,946 bytes | 1189 × 1775 |
| 8201 | [JPEG](https://lbiiif.riksarkivet.se/v3/arkis!R1008201_00001/full/800,/0/default.jpg) | HTTP 200, 61,322 bytes | 1718 × 1156 |

All six initial manifests use IIIF Presentation 3 and expose Image API services. Their rights metadata identifies **Public Domain Mark 1.0**. A manifest example is [MPO 7957](https://lbiiif.riksarkivet.se/arkis!R1007957/manifest). All six contain four canvases, although 8201 is catalogued as **one leaf**: canvas counts are not fragment counts. The images of 7957 and 8201 were visually inspected. They show actual manuscript notation and text, rulers, reuse/folding/damage, and varying orientation. Layout and notation retrieval are credible; fine letterform discrimination and parchment-side judgments need expert testing at the available native resolution. Image-service access does not establish that higher-resolution originals can be obtained automatically.

The initial audit transferred **812,468 bytes** across successful manifest/info/image requests. [Timestamped log](research/access_log.json) retains successes and failures; [sample summary](research/mpo_sample_summary.json) retains image-service dimensions and rights. Do not convert six successes into a claim that all 15,788 links work. The [MPO information page](https://sok.riksarkivet.se/en/mpo) gives an institutional route for ordering research/publication images; its older wording should be read alongside the newer live IIIF services. No images were ordered.

### 3.3 Finnish Fragmenta membranea

The database introduction documents **9,319 leaves / 18,638 pages**, approximately **1,500 manuscripts**; the collection description reports complete digitization with incomplete cataloguing. The indexed shelfmark browse exposes **1,620 catalogue items**; these are grouped catalogue descriptions, not 1,620 leaves or securely distinct codices. A successful 1,620-item machine harvest was **not** achieved. [Database introduction](https://fragmenta.kansalliskirjasto.fi/page/esittely); [collection description](https://www.kansalliskirjasto.fi/en/collections/fragmenta-membranea-collection); [shelfmark browse](https://fragmenta.kansalliskirjasto.fi/browse?etal=-1&order=ASC&rpp=10000&sort_by=1&type=signum).

Metadata includes shelfmark, contents, genre, language, origin, liturgical use, date, and additional scholarly/codicological notes; full Dublin Core views add identifiers and rights. Catalogues link downloadable whole-group PDFs and individual TIFFs. Those can be very large: the indexed F.m.IV.157 listing gives individual TIFF sizes around **73–136 MB**. They were not bulk-downloaded. [Record F.m.IV.157](https://fragmenta.kansalliskirjasto.fi/handle/10024/1300).

Direct automated requests to the home page, F.m.II.44 record, and a Finna API search returned **HTTP 403** in this environment. Browser inspection of **four full candidate catalogue records** succeeded, along with IV.173's record/viewer, so this is an observed access-path limitation rather than proof that the institution denies public research access. The National Library documents newer IIIF infrastructure and explicitly includes Fragmenta as a pilot collection, but that announcement alone cannot establish a working manifest for a selected book. [National Library IIIF workshop, 27 May 2026](https://www.kansalliskirjasto.fi/fi/tapahtumat/palikat-sekaisin-ota-iiif-perusteet-haltuun).

**Actual Finnish image retrieval succeeded through the official browser viewer.** [F.m.IV.173's METS viewer](https://fragmenta.kansalliskirjasto.fi/viewer/fragmenta.html?item=fd2011-fra0868&handle=10024/1314#page=) rendered a readable chant leaf; its visible save link downloaded the [whole-document PDF](https://fragmenta.kansalliskirjasto.fi/bitstream/handle/10024/1314/F_m_IV_173.pdf?sequence=3). Local verification found **3,030,807 bytes**, PDF magic, two page objects, and SHA-256 `86c4995af128a61631ea2e880e3eb9470bcd20f1fd1cefe427103129605b6ce1`. The record marks the images Public Domain Mark. This is one two-sided leaf, not two fragments. The download took about two minutes. [Saved PDF](research/evidence/F_m_IV_173.pdf); [receipt](research/evidence/finnish_access.json).

**Remaining access gate:** Finnish public image access is established, but a reliable programmatic derivative route and a functioning **Finnish IIIF manifest** for the selected target were **not verified**. The working METS viewer must not be mislabeled as IIIF. Full TIFF retrieval and bulk Finnish metadata export remain untested. These narrower limitations condition automation, rather than justifying a claim that Finnish images are unavailable.

### 3.4 BOMPAC: existing combined metadata, not a new discovery corpus

The [combined-dataset API](https://zenodo.org/api/records/17511106) returned HTTP 200. It advertises an **8,219,923-byte XLSX** and **354,385-byte README PDF**, under **CC BY 4.0**; these files were not downloaded or fully profiled here. Eskola's [research note](https://doi.org/10.24446/no5r) documents **29,230 objects**, including early printed fragments and itemized Helsinki physical objects. Its denominator differs from both the Finnish shelfmark catalogue and the MPO export. These sources overlap; adding their counts would double-count material.

The combined corpus should be the starting crosswalk for a pilot, with the versioned MPO export supplying directly tested IIIF links. Its published warnings about overlapping sigla, inconsistent records, reuse provenance and missing images make reconciliation a necessary scholarly/data step. A combined dataset is not an adjudicated same-codex ground truth set. Preserve creator attribution and source-specific licences when combining CC BY and CC0 metadata.

### 3.5 Beauvais and legal comparison: access actually tested

The [Beauvais IIIF manifest](https://fragmentarium.ms/metadata/iiif/F-4ihz/manifest.json) returned HTTP 200, **220,065 bytes**, with **240 canvases/image references**. Its catalogue reports **122 leaves of an original 309**. These counts were not reconciled into a unique-leaf census. Four child manifests and four actual JPEGs were retrieved; the samples include a musical page at **1200 × 1730 pixels**. Two inspected pages confirm usable manuscript content rather than catalogue thumbnails alone.

| Beauvais child | Actual image sample | Child rights |
|---|---|---|
| Cleveland 1982.141, [F-6zvk](https://fragmentarium.ms/overview/F-6zvk) | [400 × 553 JPEG](https://fragmentarium.ms:443/loris/F-6zvk/CMA_r.JPG/full/400,/0/default.jpg), 70,627 bytes | Public Domain Mark |
| Lima, Set 29 no.15, [F-qbrf](https://fragmentarium.ms/overview/F-qbrf) | [400 × 565 JPEG](https://fragmentarium.ms:443/loris/F-qbrf/Lima_r.JPG/full/400,/0/default.jpg), 61,829 bytes | Public Domain Mark |
| Waseda, [F-g7p5](https://fragmentarium.ms/overview/F-g7p5) | [400 × 589 JPEG](https://fragmentarium.ms:443/loris/F-g7p5/Waseda_r.jpg/full/400,/0/default.jpg), 67,015 bytes | No Known Copyright; not an explicit CC licence |
| Australian National University, [F-5uba](https://fragmentarium.ms/overview/F-5uba) | [1200 × 1730 JPEG](https://fragmentarium.ms:443/loris/F-5uba/Chifley_005_cropped.jp2/full/1200,/0/default.jpg), 527,097 bytes | CC BY 4.0 |

The composite rights statement is insufficient: [Fragmentarium's terms](https://fragmentarium.ms/pages/terms) direct multicollection users to the individual fragments' rights. Four Boston image resource URLs in the aggregate are malformed, although specific service identifiers remain available. No general conclusion that every canvas works is warranted. [Detailed receipt](research/evidence/beauvais_access.json).

For the legal comparison, **Kungliga biblioteket B 193**, Äldre Västgötalagen, has a working [manifest](https://www.manuscripta.se/iiif/100332/manifest.json) and an actually retrieved [800-pixel JPEG](https://iiif.manuscripta.se/iiif/ms-100332/ms-100332_0003.tif/full/800,/0/default.jpg), HTTP 200, **186,621 bytes**. The catalogue identifies two leaves, dated 1200–1250, Västergötland. Only four of its **18 canvases** are medieval leaf sides; other views include bindings. Images are marked public domain; description CC BY 4.0. This verifies a real legal-image route, not an unresolved reconstruction opportunity. [Catalogue](https://www.manuscripta.se/ms/100332); [receipt](research/legal_b193_probe.json).

### 3.6 Continuation: images from the recommended family, not just neighbouring controls

On **20 October**, four further manifests and four actual **600-pixel-wide JPEGs** returned HTTP 200. Together they transferred **216,487 bytes**; all four manifests identify Public Domain Mark. Each JPEG was decoded and visually inspected. These small samples improve target readiness without constituting a corpus download or a book attribution.

| Exact object and role | Tested image | JPEG bytes | What the inspection establishes |
|---|---|---:|---|
| Fr 1385, documented IV.157 associate | [Sample](https://lbiiif.riksarkivet.se/v3/arkis!R1001385_00001/full/600,/0/default.jpg) | 44,134 | Real chant page with red staves, notation, text, folds/damage and ruler |
| Fr 20274, Ant 99 comparator | [Sample](https://lbiiif.riksarkivet.se/v3/arkis!R1020274_00001/full/600,/0/default.jpg) | 55,435 | Readable chant/layout evidence; this capture does not show the whole physical area |
| Fr 8994, Codex 1505 comparison | [Sample](https://lbiiif.riksarkivet.se/v3/arkis!R1008994_00001/full/600,/0/default.jpg) | 37,467 | Large music/text layout, initial/rubric, ruler and folded lower portion |
| Fr 25592, suggested Hy 49 comparison | [Sample](https://lbiiif.riksarkivet.se/v3/arkis!R1025592_00001/full/600,/0/default.jpg) | 25,997 | Two columns with interspersed music, confirming a substantial layout difference requiring reconciliation |

[Timestamped receipt](research/target_access_log.json), [manifest summary](research/target_access_summary.json), [bounded probe script](research/target_access_probe.py). Only the first capture was sampled from each record. These views do not independently establish a full ruling count, original dimensions, date, or codex identity.

The earlier untested **Fr 8304** negative-control image was also retrieved separately: HTTP 200, **59,532 bytes**, [800-pixel JPEG](https://lbiiif.riksarkivet.se/v3/arkis!R1008304_00001/full/800,/0/default.jpg), [receipt](research/evidence/goal_negative_image_access.json). Thus both images for the published 8201/8304 comparison are available, although their attribution still rests on the cited scholarship rather than our visual inspection.

## 4. Existing scholarly and technical work

### CODICUM and Nordic reconstruction

[CODICUM](https://www.codicum.eu/about), active **1 April 2025–31 March 2031**, studies more than 50,000 Nordic fragments and explicitly seeks cross-collection reconnections, virtual books, biomolecular/visual study, and new methods. Its [resources](https://www.codicum.eu/resources) already include a Nordic holdings survey. The [5 May 2026 institutional technical account](https://riksarkivet.se/resurser/codicum-sticker-ut) describes virtual-reconstruction prototype development and AI-assisted conversion of Danish catalogues with scholarly correction. Its [conservation account](https://riksarkivet.se/resurser/provtagning-pagar) describes Swedish photography/sampling during 2026–2027, including previously unpictured material. These are ongoing activities, not evidence that all new photographs are already online. The [news page](https://www.codicum.eu/news) also identifies research on Dominican fragments c.1250–1450.

This is direct overlap. The independent contribution should be a transparent, independently evaluated retrieval/uncertainty method or a specialist-confirmed addition, correction, or exclusion for a specific book. Coordination would avoid duplicating current unpublished work; no such coordination has occurred.

Nordic reconstruction long predates this proposal. The individual candidate records cite Haapanen, Taitto and later revisions. Tahkokallio's [*Fragments Re-Connected* (2023)](https://doi.org/10.54334/mirator.v23i1.125301) publishes cross-collection missal reconnections. Björkvall's [*Liturgical Sequences*](https://doi.org/10.62077/1xxglp) inventories and reconstructs sequence sources. [Fragments Combined](https://doi.org/10.24446/no5r) supplies an integrated research corpus. These are essential comparison sources, not competing suggestions to ignore.

**Important later-scholarship gate:** Jesse Keskiaho's *En grupp handskrifter från Nådendal: nya rön*, pp.51–67, in *Nådendal – Vallis Gratiae*, ISBN 978-91-88568-75-5, directly concerns this group. The [author's institutional bibliography](https://researchportal.helsinki.fi/en/publications/en-grupp-handskrifter-fr%C3%A5n-n%C3%A5dendal-nya-r%C3%B6n/) dates the chapter March **2019**; the [publisher's book page](https://www.medievalia.nu/publikation/cederbom-ferm-nystrom-2018/) dates the volume **2018**. Its contents were **not obtained**; the inspected publisher page exposed no open full text. It may resolve the apparent catalogue ambiguity. Identifying its existence is not reading its conclusions. The proposed question is therefore credible at catalogue level, with present-day novelty conditional, not cleared. [Detailed source audit](research/goal_novelty_audit.md).

Fragmentarium already supports descriptions and virtual reconstruction. The Beauvais reconstruction is a substantial existing result. Ege portfolio research, specialist handlists, and institutional reconstructions likewise precede this project. A new viewer without added evidence would mainly be public interpretation.

### Palaeography, musical analysis, and AI

The [Cross-codex Learning study](https://arxiv.org/abs/2312.04296) shows why scribe identification needs cross-codex evaluation: book-specific visual cues can masquerade as handwriting evidence. A hand may occur in different books; a book may contain several hands. Script and notation labels are useful filters but cannot establish identity. DigiPal/ScandiPal already offers a history of structured digital palaeographic comparison. [Project code](https://github.com/kcl-ddh/digipal).

[OMMR4all's 2024 historic-chant pipeline](https://www.mdpi.com/2076-3417/14/16/7355), [REPERTORIUM](https://repertorium.eu/), and the [Austrian Academy's plainchant recognition work](https://www.oeaw.ac.at/acdh/research/musicology/research/documentation-source-studies/ai-assisted-music-notation-recognition) show that music transcription/retrieval is an existing research field. They do not establish reliable recognition of every damaged Nordic notational tradition, much less same-book identity. Begin with manual chant identification and existing methods; complete OMR is unnecessary for an initial identity experiment.

[Bag of Bags, CVPR Workshops 2026](https://openaccess.thecvf.com/content/CVPR2026W/SINT4CH/html/Gogawale_Bag_of_Bags_Adaptive_Visual_Vocabularies_for_Genizah_Join_Image_CVPRW_2026_paper.html) provides a relevant Genizah retrieval precedent. Its [author code](https://github.com/TAU-CH/midrash_bob) was accessible, but the advertised data directory contained only a placeholder in this audit: downloadable benchmark images were not verified. Hebrew paper/parchment results do not predict performance here. The 2024 [*Reunion helper*](https://www.nature.com/articles/s40494-024-01150-3) addresses same-sheet edge joins, a different task from matching nonadjacent leaves of a codex. None of these published scores is used as an expected project accuracy.

## 5. Five specific candidate or control dossiers

Five concrete targets are identifiable, but they are **not five demonstrated original discovery opportunities**. Two are primarily positive controls, two are mainly difficult comparison/audit cases, and one disputed family is the provisional discovery target. The counts below distinguish listed digitized leaves, untested image pointers and actually retrieved samples. None is an audited census of every surviving leaf.

### 5.1 Graduale Aboense — F.m.II.44 / MPO Codex 1104 / CCM Sequ 42

**Identity, date and origin:** a single already reconstructed gradual, Åbo/Turku liturgical use, dated **1397–1406** in the updated Finnish note; the Swedish export broadly dates its records to the fifteenth century. This is the **recommended first technical control**, not an unknown lost-book identification. [Full Finnish record](https://fragmenta.kansalliskirjasto.fi/handle/10024/1610?show=full).

**Exact holdings and digitized extent:** Helsinki's National Library lists **48 folios / 96 TIFF sides**. The catalogue identifies Swedish Riksarkivet **Fr 7957, 7960, 7961, 8343, 8344, 9242, 28175** as the same book, seven fragments/fourteen folios. All seven records exist in the downloaded export. Six carry **Codex 1104** and image pointers. **Fr 28175 has CCM Sequ 42, two leaves, but blank codex and image fields**. The initial report incorrectly called it absent after selecting only the exact codex label; direct identifier lookup corrected that error. This demonstrates a known-positive omission by an overly strict filter, not an unknown fragment. Do not call the catalogue's 62 associated leaves a verified downloadable inventory. [Six codex-labelled rows](research/mpo_codex1104.json); [direct identifier crosscheck](research/goal_identity_crosscheck.json).

**Images and existing work:** five Swedish records supplied the actual JPEGs in section 3.2; [7957 sample](https://lbiiif.riksarkivet.se/v3/arkis!R1007957_00001/full/800,/0/default.jpg) is visually usable. Helsinki's [listed first TIFF](https://fragmenta.kansalliskirjasto.fi/bitstream/handle/10024/1610/F_m_II_44-0001.tif?sequence=1&isAllowed=y) is approximately 61 MB and was not downloaded. Ilkka Taitto's **2002 *Graduale Aboense 1397–1406*** is an established partial reconstruction, not a result this project may claim. [Publisher](https://kirjat.finlit.fi/EN/page/product/graduale-aboense-1397-1406/21983?category=4949).

**Open question, AI role and value:** hide the documented associations and test whether metadata, chant sequence and visual evidence recover them. The export explicitly identifies continuity between **7960–7961** and **8343–8344**. Additional surviving leaves would be valuable, but none has been identified as an unresolved candidate in Phase 0. A future artifact could show the already known chant sequence, reuse notes and lacunae, clearly separating validated retrieval from any proposed extension. Risks are a mature prior reconstruction, differing capture quality, incomplete surviving coverage, and confusing the broad catalogue dating with the narrower scholarly date.

### 5.2 St Catherine / Åbo–Nådendal antiphonal neighbourhood — centred on F.m.IV.157

**Identity, date and origin:** F.m.IV.157 is one catalogued antiphonal, but its disputed neighbourhood is a **manuscript family and competing membership hypotheses**, not one safely merged codex. The heading gives **c.1460–1486**; an updated note citing Keskiaho gives **c.1460–1475**. Åbo liturgical connections and probable Nådendal production are scholarly attributions, not secure proof of origin. [Full record](https://fragmenta.kansalliskirjasto.fi/handle/10024/1300?show=full).

**Exact holdings and extent:** Helsinki lists **14 folios / 28 TIFF sides**. It records same-codex associations with **CCM Ant 99: Fr 20274–20278**, plus **MPO Fr 1385**: six further catalog-associated leaves at Swedish Riksarkivet. The export has all six records but image pointers for only **1385 and 20274**. Separately, **Turku Ms. c** and **MPO Codex 1505: Fr 8994, 10370, 10406, 10407, 10437** are qualified associations, with related suggestions under F.m.IV.156. All five Codex 1505 rows have manifest pointers; 8994's manifest/image and the two image-linked accepted comparators were actually retrieved in the continuation. [Crosslink extract](research/finnish_crosslinks_mpo.json); [image receipt](research/target_access_log.json).

**Identity caution:** IV.156's accumulated notes use both qualified association language and an equation involving Codex 1505/IV.157. The Swedish notes describe resemblance, already citing Taitto 2001, pp.161–168. Reconcile these statements before treating the shelfmarks as securely independent books or the links as unresolved binary labels. **Turku Ms. c** is described under both a provincial-museum name and *Turun maakunta-arkisto*, with a defective bifolium versus a one-folio extent; its present holder, shelfmark and physical identity remain unverified.

**Images and scholarship:** [listed Helsinki sample TIFF](https://fragmenta.kansalliskirjasto.fi/bitstream/handle/10024/1300/F_m_IV_157-0001.tif), 73 MB, remains untested. Swedish 1385/20274 and Codex 1505 leaf 8994 now have real retrieved sample images (section 3.6). [IV.173](https://fragmenta.kansalliskirjasto.fi/handle/10024/1314?show=full) supplied the actual Finnish PDF. Taitto 2001, notes citing Keskiaho 2010 and the unread 2018/2019 chapter are prior scholarship; existing associations are not discoveries.

**A narrower testable edge:** IV.173's updated note explicitly links it to **Ant 242 = Fr 29666** as the same codex, and suggests **Ant 99/IV.157** and **Hy 49 = Fr 25592**. The Fr 29666 export row independently repeats the known relation but has no image pointer. Fr 25592's row dates it to the twelfth/thirteenth century, with two columns/35 lines; its actual image confirms a different layout from the inspected large one-column chant-page views. Resolve the alias, catalogue dates and the possibility of a composite book before accepting or rejecting this suggestion. It is unsuitable as an automatic positive training label. [Exact rows](research/goal_identity_crosscheck.json).

**Uncertainty, proposed contribution and artifact:** determine whether the *catalogue-disputed* leaves fit IV.157, IV.156, another book, or merely the same production milieu. A specialist must establish which alternatives remain live in 2026. Eleven-line ruling, text/chant positions, hands, notation, decoration and quire clues offer multiple evidence channels. AI could rank comparisons or make contradictions easier to inspect. A supported exclusion or correction would count as useful evidence; rediscovering the listed links would not. A public artifact could display alternative reconstructions and explicitly uncertain leaves. Principal risks are shared-workshop similarity, damage, unfinished musical passages, poorly imaged known comparators, and an apparently unresolved catalogue note having already been resolved offline.

**Priority:** strongest provisional discovery/audit target, conditional on scholarly status and access checks. Its Dominican associations also require coordination with CODICUM's stated research, rather than treating a narrower date as protection from overlap.

### 5.3 F.m.IV.160 / CCM Ant 140 — a second cross-border control

**Identity, date and origin:** a single catalogued antiphonal, **second half of the fifteenth century**, Dominican–Åbo use, probably Nådendal/Åbo. [Full record](https://fragmenta.kansalliskirjasto.fi/handle/10024/1303?show=full).

**Exact holdings and extent:** Helsinki lists **10 folios / 20 TIFF sides**. A known same-book link is Swedish Riksarkivet **Fr 20340 = CCM Ant 140, Finska cameralia 88:3:3, Åbo 1615 Införingslängd**, one further leaf. The row exists in the export but has **no viewer or manifest URL**. Eleven associated leaves is a catalogue statement, not an eleven-leaf accessible benchmark.

**Images and existing work:** [listed first TIFF](https://fragmenta.kansalliskirjasto.fi/bitstream/handle/10024/1303/F_m_IV_160-0001.tif?sequence=1&isAllowed=y), approximately 136 MB, not downloaded. The catalogue cites Maliniemi and Taitto, including 1992 work. It describes one column and nine lines, which distinguish it from the eleven-line IV.157 neighbourhood. No book-specific image bytes were fetched here.

**Question, value and risks:** hide the existing Fr 20340 association if a usable image is obtained; ask whether retrieval distinguishes a known related book within the same production milieu. This is currently a **conditional control**, not an image-ready cross-border benchmark or independently justified novel target. A future artifact could explain the documented reunion and any separately supported addition. Few known positive objects, the missing Swedish image pointer, common chant text and related scribes limit its value. No specific additional surviving leaf was established.

### 5.4 F.m.IV.28 — bounded antiphonal comparison with a documented exclusion

**Identity, date and origin:** a single secular Nordic antiphonal, **fourteenth century, possibly its second half**. The record excludes Åbo and discusses other unlikely dioceses; its origin remains uncertain. Related shelfmarks are comparison sources, not automatically one manuscript family or codex. [Full record](https://fragmenta.kansalliskirjasto.fi/handle/10024/1232?show=full).

**Exact holdings and extent:** Helsinki lists **30 folios / 60 TIFF sides**, two columns and fifteen lines. Comparators include **F.m.IV.29, IV.30, IV.36, VII.85**. Stockholm Riksarkivet **Fr 10349**, catalogued `Ant 111?` in the export, is an explicitly rejected same-codex comparison because overlapping contents conflict with the suggested attribution. It has a [manifest pointer](https://lbiiif.riksarkivet.se/arkis!R1010349/manifest); no bytes were fetched from it here. The full comparison-family extent was not counted.

**Images and scholarship:** [listed Helsinki TIFF](https://fragmenta.kansalliskirjasto.fi/bitstream/handle/10024/1232/F_m_IV_28-0001.tif?sequence=1&isAllowed=y), approximately 55 MB, untested. Taitto's catalogue cites Toy 1981 and Nilsson 2000. Public Domain Mark is recorded for the Finnish images. Book-specific downloads are not verified.

**Purpose and possible contribution:** use the known exclusion to test whether a matcher incorrectly equates similar notation/appearance with book identity. This is primarily a **hard-negative control**. An evidence viewer could explain why a visually persuasive match fails textually. A new attribution would require a separately identified, still-open problem and stronger evidence; neither is supplied here. The main risk is counting related books as either established positives or independent discovery opportunities.

### 5.5 CCM Ant 49 / MPO Codex 1146 — a contested catalogue cluster

**Identity, date and origin:** at least two antiphonaries are implicated; **Ant 49 is not one authenticated lost codex**. The export dates 8201 and 8304 to the **fifteenth century**, 20106 to the **fourteenth**, and offers tentative German/Baltic/Swedish origins. Preserve this disagreement. [8201 viewer](https://sok.riksarkivet.se/bildvisning/R1008201); [8304 viewer](https://sok.riksarkivet.se/bildvisning/R1008304).

**Exact holdings and extent:** exact CCM Ant 49 gives **eight MPO records: 8066, 8072, 8073, 8201, 8304, 9620, 20106, 20107**, seven with manifest pointers. **8201 and 8304 now both have retrieved images**; the other five pointers were not image-tested here. **20106** is registered as **KB A 103** in the export but lacks an image link. Historical collection labels do not necessarily establish present physical location: Tahkokallio's [2023 study](https://doi.org/10.54334/mirator.v23i1.125301) notes that MPO items registered as KB are physically at Riksarkivet. Confirm the current shelfmark/location with the holder before requesting or publishing.

**Known published correction:** Czesław Grajewski's [study of St Catherine offices](https://doi.org/10.25167/ls.4818), p.293, supports continuity between **20106 and 8201**, while **8304 belongs to another book despite apparently sharing the hand**. The export still assigns 8201 and 8304 to Codex 1146. This is a valuable **published difficult negative**, not a new finding. A separate known Ant 205 pair, 20900/20902, has no image pointers and is not adopted as a ready benchmark.

**Open question, contribution and artifact:** audit the remaining Ant 49 members and establish the curator's current interpretation before asking whether an additional membership can be supported. AI could rank lookalikes, but text order and contradictory duplicated liturgical positions must control identity judgments. A useful result could be a supported membership correction/exclusion with an evidence graph and literature trail. Risks include the missing image for the key positive 20106, inconsistent dating, shared scribal features and a correction already published but not propagated into the export. This is an audit/comparison target rather than a clean late-fifteenth-century discovery book.

### 5.6 Explicit research-priority ranking

These are ordinal judgments, not numerical discovery probabilities or additive scores. The [maintained candidate file](CANDIDATES.md) expands the same six requested dimensions. **Rank 1 is the single recommended provisional opportunity; ranks 2–5 are audit/control leads, not four additional demonstrated discovery opportunities.**

| Rank / target | Digitized material | Unresolved relationships | Original-research potential | AI comparison | Historical significance | Interactive potential |
|---|---|---|---|---|---|---|
| **1 — IV.157-centred family / Codex 1505** | Exact family/comparator samples now verified; full view inventory incomplete | Qualified and ambiguous catalogue edges; later chapter still unread | Best in shortlist, **conditional** on a still-open attribution/exclusion | Constrained layout/chant comparisons; shared production is a major confound | Åbo-region liturgy, production and reuse | Competing leaf memberships with source-linked uncertainty |
| **2 — Ant 49 cluster** | Two actual hard-negative images; key positive lacks a pointer | Published correction versus retained codex label; other members need audit | Low–moderate; central correction already known | Excellent difficult-negative stress test; baseline demonstrably fails | St Catherine office transmission | Explain accepted/rejected connections |
| **3 — Graduale Aboense** | Strongest verified Nordic control coverage | No specific newly unrecognized leaf established | Low until a real extension candidate is found | Best known-book starting control | Named Åbo gradual with substantial scholarship | Chant sequence and reuse history, credited to prior reconstruction |
| **4 — IV.28 / Fr 10349** | Listed Finnish folios and a Swedish pointer; exact pair bytes untested | Rejection already documented | Low; method falsification rather than discovery | Useful lookalike/textual-contradiction control | Nordic antiphonal tradition | Show why resemblance fails |
| **5 — IV.160 / Fr 20340** | Key Swedish image absent from export | Known relation; no specific new leaf | Low at present | Conditional on obtaining comparator image | Related regional book production/use | Explain a documented reunion |

## 6. What evidence of unresolved relationships actually exists?

There is evidence of **documented uncertainty**, rather than evidence of an undiscovered join:

- Finnish catalogue notes distinguish secure and suggested same-codex associations and preserve conflicting interpretations around the late-fifteenth-century antiphonals. This is a bounded question that an expert could adjudicate; the present state of scholarship still needs checking.
- The Ant 49 catalogue grouping conflicts with a published same-hand/different-book assessment. The export still groups 8201 and 8304 as Codex 1146. Resolving the other members may be useful, but the published correction itself is already known.
- Known cross-border books, including Graduale Aboense, survive incompletely. Missing pages do not prove that additional recoverable leaves exist, and no searchable collection is guaranteed to contain them.

The evidence supports a **credible catalogue-level attribution and exclusion question** involving exact objects and competing explanations. It does not establish a previously unrecognized relationship. The unread Keskiaho 2018/2019 update is an explicit first gate: if it settles the proposed edges, the result becomes replication or catalogue harmonization and the next ranked lead must be reassessed. No candidate has passed comprehensive novelty clearance against current curatorial records, CODICUM/BOMPAC work and the full literature. There is **no basis for a new-discovery claim or an unconditional GO**.

## 7. Validation methodology

### 7.1 Reference data and distinct tasks

Use **Beauvais** for an accessible positive control, **Graduale Aboense** for Nordic same-book/sequence controls, and **Ant 49** for a documented difficult distinction. Expand to independently reviewed relationships from multiple books before claiming general performance.

Beauvais is dated **1270–1300**, from Beauvais, and contains square notation. Its existing reconstruction establishes membership and some sequence/quire evidence, although not all leaves are musical. It differs substantially from Nordic reused wrappers. Davis's [2015 reconstruction account](https://manuscriptroadtrip.wordpress.com/2015/03/24/manuscript-road-trip-reconstructing-the-beauvais-missal/) explains adjacency and gold-offset evidence. These are valuable positive labels after identifiers/certainty are checked; the complete quire structure was not independently harvested here. A second Ege control, [F-djs6](https://fragmentarium.ms/overview/F-djs6), a Paris-use Book of Hours, 1425–1450, has a documented reconstruction but still requires its own access/licence audit.

Maintain separate evaluation labels for **physical join**, **same codex**, **adjacency/quire location**, and **related text/hand/workshop**. Agreement on one is not a positive label for the others. Freeze an expert-reviewed association ledger with source citation, exact object IDs, physical units, certainty, adjudicator and date. Distinguish accepted, rejected and uncertain associations. Catalogue `codex` alone is insufficient.

### 7.2 Hidden-association experiment and separation

Proposed scale: **100–300 physical fragments**, preferably **5–10 or more independent codices**, including at least three unseen test codices if the actual reference evidence permits. These are design targets, not available verified counts. Keep a separate, unlabelled discovery set. If independent books cannot be secured, report a case study, not a validated general matcher.

1. Split **whole original books** into development, calibration and untouched test partitions. Keep related disputed groups together conservatively. No relationship from a test codex may guide training, feature selection or threshold tuning.
2. Within each test book, withhold selected **whole physical fragments** as queries and leave other fragments in the gallery. Both sides, alternate captures, crops and augmentations of a query object stay with it; a recto/verso duplicate must never count as a successful recovery.
3. Hide all association labels, reconstruction names, codex IDs, Ege portfolio numbers, sequence positions, revealing filenames, and notes that explicitly state relationships. Preserve a private evaluator crosswalk. The matcher may use independently described type/date/dimensions, but not a note saying that the pieces belong together. Check whether dates or measurements were copied from a reconstructed parent group: inherited attributes can leak membership indirectly and need exclusion or a separate ablation. Do not permit web lookup of test reconstruction pages during inference.
4. Compare metadata-only ranking, metadata plus chant/text sequence, layout/handwriting features, frozen visual retrieval, and transparent feature fusion on the **same gallery**. Measure candidate-filter losses. A metadata shortlist is useful only if its false exclusions are counted.
5. Freeze all choices before opening final labels. Test across institutions; mask rulers, watermarks and capture backgrounds in an ablation so provider appearance cannot substitute for manuscript identity. Disclose possible pretrained-model exposure to publicly reproduced test pages.

The test gallery deliberately contains other leaves from unseen books: that makes retrieval possible. Their labels remain evaluator-only and their relationships never enter fitting or tuning. This differs from training and testing on pairs from the same codex.

### 7.3 Difficult negatives and open-world evaluation

Include specialist-confirmed different books containing the same chant/text; visually similar hands; books from the same region and period; similar notation; and, where supported, different books copied by the same scribe. Ant 49 provides a published example of the last risk. Include damaged examples and query fragments with **no** correct gallery match, so rejection is tested.

Unlinked fragments are not automatically negatives. Explicitly uncertain pairs remain outside binary gold labels and get a separate review outcome. The reference set needs specialist confirmation of both positives and difficult negatives. A balanced sample of easy negatives would inflate practical precision.

| Measure | Definition and reporting rule |
|---|---|
| Suggested-match precision | Confirmed true same-codex suggestions / all adjudicated positive suggestions; show numerator, denominator and interval; report unresolved suggestions separately |
| Known-relationship recall | Recovered established positives / eligible established positives, including positives lost by filtering; this is not recall of all unknown surviving associations |
| Hit@1, @5, @10 | Fraction of queries **known to have a correct gallery item** with at least one such item in the top k, excluding duplicate/self views; report this denominator |
| Recall@k and MRR | Fraction of all known relevant gallery items retrieved; reciprocal rank of first correct item |
| False positives | Counts per 100 queries, per negative subtype, and FP/(FP+TN); specify the evaluated pair universe and negative sampling |
| Calibration | Separate-book reliability bins, Brier score and calibration error with bin counts; test abstention on unmatched queries |

Use codex-level macro averages and group-aware uncertainty intervals; hundreds of correlated pairs do not create hundreds of independent books. Report filtering recall, notation, damage and provider breakdowns. Score rejection/false acceptance of unmatched queries separately from Hit@k. Cosine similarity is not a probability. If too few independent calibration books exist, publish ranks/evidence and abstain from numerical confidence claims.

Proposed preregistered pilot targets are **Hit@5 ≥ 0.8**, **precision ≥ 0.9 in the expert-review queue**, and measurable improvement over metadata/text baselines without unacceptable filter losses. Freeze the queue-selection rule before revealing labels: for example, the top **30 distinct pairs**, deduplicated and with at most three pairs per query, selected by a frozen ranking/threshold. Adjudicate the entire queue, rather than selecting easy suggestions. Report adjudicated coverage and unresolved pairs alongside conditional precision; show conservative bounds treating unresolved suggestions as incorrect or correct. These are planning thresholds, not results or statistically established guarantees. Report uncertainty even if point targets are met; if visual features add no value, the negative result is an intended outcome. No blind AI-performance assessment has been completed; the narrower retrospective diagnostic below is a separate result.

### 7.4 Executed diagnostic: recovery is possible, but a difficult negative defeats the baseline

A deterministic metadata compatibility diagnostic was executed and independently rerun using the cached full export. Reproduce offline with:

```sh
python3 research/metadata_retrieval_diagnostic.py
```

For each query the gallery contains every other record of the exact manuscript type. Five raw categorical fields (script, notation, staff lines, columns and text/music lines) and four dimensional components receive equal weight, with 0.5 cm numeric tolerance. Complete descriptive fields are required deliberately to test that filter's failure. Codex/CCM, relationship prose, contents, institution and account provenance are excluded; IDs are evaluator-only and never break ties. Labels come from explicit catalogue continuity notes and Grajewski's published comparison. These labels remain scholarly interpretations needing review, not newly adjudicated ground truth.

| Evaluator comparison | Gallery before / after complete-case filter | Observed result |
|---|---:|---|
| 7960 → 7961, known same-codex continuity | 1,321 / 792 gradual records | 9/9 compatibility; leading tie positions **1–4** |
| 8343 → 8344, known same-codex continuity | 1,321 / 792 | 9/9; leading tie positions **1–7** |
| 8201 → 20106, published compatible same-book comparison | 2,099 / 1,221 antiphonal records | **Excluded** for missing script, columns and dimensions |
| 8201 → 8304, published different-book comparison | 2,099 / 1,221 | 9/9; **unique rank 1** despite the negative label |

This answers a narrow practical question: basic features can shortlist established positives, yet give the strongest suggestion to a published wrong-book pair and lose a documented positive. The 9/9 score is not a probability. Preserve ties; do not turn the seven-way leading tie into an arbitrary top-five success. No unlabelled gallery record is assumed negative, so population precision/recall cannot be computed from these four chosen comparisons.

This is **retrospective, selected after studying the labels, untrained and nonvisual**. It neither validates AI nor proves independent-book generalization. Descriptive catalogue fields may inherit group descriptions, an additional leakage risk. Its useful result is the demonstrated need for missing-data tolerance and text/codicological rejection checks. [Full method and source audit](research/goal_validation_audit.md); [script](research/metadata_retrieval_diagnostic.py); [results and hashes](research/metadata_retrieval_diagnostic.json).

For a prospective independent experiment, the detailed audit proposes at least **eight independently distinguished codices** divided into two development, three calibration and three untouched test books, if the actual labels permit. This is a planning minimum, not an achieved dataset or a guarantee of stable calibration. Freeze data/labels, features, tie handling and thresholds before evaluation; keep physical fragments/captures together. The broader multi-codex protocol in sections 7.1–7.3 remains required before any claim that adding visual evidence works.

## 8. Comparison of research directions

These are evidence-based qualitative judgments, not measured success probabilities.

| Criterion | A. Nordic musical manuscripts | B. Nordic legal manuscripts | C. Otto Ege dispersed leaves |
|---|---|---|---|
| Data accessibility | Strong Swedish export and tested IIIF; Finnish automation still conditional; quality varies | Working institutional IIIF demonstrated by B 193; uneven fragment coverage remains | Beauvais images demonstrably accessible; cross-holder rights and URLs vary |
| Chance of useful evidence | Good for known associations and a bounded disputed group; no promised new join | Plausible, but no stronger unresolved target verified here | Strongest for a quick known-book retrieval/ordering demonstration |
| Original contribution | Possible membership audit/addition or transparent negative result; direct CODICUM/BOMPAC overlap | Possible, with active NordicLaw and established textual scholarship; gap not yet secured | Many memberships already encoded in portfolio labels and handlists; novelty requires precise missing-leaf work |
| Technical difficulty | Highest: music, mixed notation, reuse damage, multi-hand books, orientation and low resolution | No OMR requirement, but gloss layouts and repeated legal texts complicate identity | Often cleaner whole leaves and foliation; still image/label leakage and same-text negatives |
| Specialist verification | Essential: codicology, Latin palaeography and medieval chant | Essential: codicology, legal textual traditions, relevant Latin/vernacular languages | Essential for attribution/order, historical handlists and ownership history |
| Narrative potential | Strong: shared Nordic book culture and administrative reuse | Strong: law, regional identity and reuse | Strong: modern dismemberment and dispersed cultural heritage |
| Interactive artifact | Evidence-linked lost-book/chant sequence with visible lacunae | Legal text/quire reconstruction and gloss comparison | Reunited pages, sequence and documented dispersal map |

[NordicLaw](https://www4.uib.no/en/research/research-projects/nordic-law-books-the-production-and-use-of-vernacular-law-manuscripts-in-the-north-from-1100-to-1600-nordiclaw) demonstrates active legal-manuscript research, rather than an untouched alternative. [Denison's Ege project](https://ege.denison.edu/) explains portfolio membership and [Stony Brook's institutional collection](https://exhibits.library.stonybrook.edu/s/ege/page/home) demonstrates existing digitization. Historical counts on these pages must not be treated as a current census.

**Choice:** A for the substantive research question; C for supplementary validation. B is a credible fallback only if a specialist identifies a better bounded unresolved legal relationship. Moving to law solely because one image works would not improve the evidence for originality.

## 9. Principal risks and practical mitigations

| Risk | Consequence | Smallest useful mitigation |
|---|---|---|
| Current work duplicates the question | Rediscovery mistaken for originality | Audit exact candidate IDs against current literature and curatorial/CODICUM knowledge before novel claims |
| Catalogue groups are fallible | Corrupted training/test truth | Expert evidence ledger; keep contested memberships out of positive gold labels |
| Mixed physical/counting units | Inflated corpus and biased evaluation | Object/leaf/capture crosswalk; group bifolia and repeated views |
| Sparse, uncertain metadata | False exclusions and distorted provenance | Soft filters, explicit missingness; retain alternate dates/origins and trimming markers |
| Different measurement conventions | False exclusion of a documented same-book comparator | Separate leaf size from written space, resolve width/height order and folding/trim before cross-collection filtering |
| Access failures or old scans | Unreproducible pipeline or inadequate letterform detail | Small endpoint/quality gate per selected object; preserve native dimensions; obtain institution guidance if needed |
| Same text/hand/notation in different books | Convincing false positives | Textual-position contradictions, same-scribe negatives, specialist rejection criteria |
| Dataset/provider leakage | Impressive but meaningless retrieval | Codex/object separation, hidden labels, background ablations, cross-institution tests |
| Few independent books | Unstable metrics and probabilities | Report group counts/intervals; use case-study language; avoid calibration claims |
| Unreconciled rights | Publication not justified for selected assets | Record per-image provider, statement, attribution and source; publish only supported assets |
| Expensive or unavailable expertise | No defensible adjudication | Secure limited specialist review before spending on model engineering |

Reuse-account geography is evidence of a fragment's later history, not automatically its medieval production place. Parchment hue/hair-flesh appearance depends on imaging and handling; it is weak photographic evidence, and cannot substitute for physical or biomolecular analysis. Do not infer provenance, ownership, or exact date from embeddings.

## 10. Proposed initial experiment — only after explicit Phase 1 approval

**Question:** does adding visual/layout/notation evidence improve recovery of expert-established same-codex relationships over metadata and textual evidence alone, and does it identify review-worthy uncertain memberships in a predefined antiphonal family?

**Exact first investigation, before the larger retrieval pilot:** examine Codex 1505's **Fr 8994, 10370, 10406, 10407, 10437** against selected representative sides under **F.m.IV.156 and IV.157**, documented comparators **Fr 1385/20274**, and the downloaded **IV.173** terminal leaf. Inspect **Fr 25592** as a proposed falsification case, not an accepted positive. **Fr 29666** is a documented IV.173 positive only if a usable image can be obtained. Start with roughly **10–20 representative sides**, not whole TIFF groups; some may be multiple views of the same physical object and must be grouped accordingly.

The first output is an association ledger and competing-hypothesis table, not a reconstructed book. Retain: (a) one Helsinki book contains a proposed leaf; (b) a third/different book shares production features; (c) a catalogue alias or inherited grouping explains the apparent disagreement; (d) later scholarship already settles it. Read the 2018/2019 update and Taitto's cited pages first. Then compare chant/text positions, opening signatures, ruling, original versus written-space dimensions and contrary evidence before visual ranking. If the source already settles the issue, log replication or rejection and reassess Ant 49 rather than rebranding the known conclusion as original.

One concrete harmonization check is essential: IV.157's prose dimensions **22–23 × 33.5–35.5 cm** cannot be directly compared with Swedish `format` leaf dimensions. Known-associated Fr 1385 has written space **34 × 23 cm**, close to a transposed version of those prose figures. Resolve category/orientation, trimming and folding before excluding a candidate; this observation itself does not establish compatibility.

**Step 1: resolve the gates.** Reconcile the combined-corpus IDs; establish reliable access to the required Finnish representative sides; read the later scholarship; resolve the Turku alias/measurement conventions; and assemble enough independent codex/negative labels. Graduale Aboense's seventh listed record, Fr 28175, is now found in the export but still lacks an image link. If essential gates fail, stop or rescope before building retrieval.

**Step 2: freeze a small reference set.** Select 100–300 physical fragments after access and expert review. Use the broad musical pool for hard negatives while keeping the discovery question narrow. A main late-fifteenth-century target does not exclude earlier books from separate validation controls. Label known/uncertain/rejected relationships and hide gold associations as above.

**Step 3: run cheap baselines.** Parse only defensible metadata, inspect dimensions and layouts, and manually identify a limited set of chant/text sequences. Add frozen image retrieval only after the baseline is meaningful. No large training run or paid service is necessary.

**Step 4: assess known associations before discovery.** Report end-to-end retrieval, false positives and uncertainty. Do not look for or announce new joins if the method cannot distinguish known difficult examples.

**Step 5: examine only a bounded review queue.** For each uncertain relationship, produce a dossier with exact IDs, source images/rights, measurements, supporting and contrary text/notation/hand evidence, alternative explanations, prior-literature search, remaining uncertainty and the specialist decision needed. A possible new association remains a hypothesis until independent scrutiny.

The next deliverable would be a small reproducible validation result and several evidence dossiers. A full website or complete lost-book reconstruction is outside this pilot. A later public artifact could show leaf locations, accepted/rejected/uncertain links, chant sequences, lacunae and provenance of each claim. Selected chant transcription/performance should only follow expert identification of notation and responsible representation of missing/uncertain passages; no musical realization is justified by Phase 0 alone.

## 11. Estimated resources and expected scholarly value

These are planning estimates, not quotations or commitments.

| Resource | Bounded pilot estimate |
|---|---|
| Research/data work | Approximately 40–80 hours for crosswalks, source checking, reference-set curation and reproducible analysis |
| Technical work | Approximately 30–60 hours for baselines, existing feature extraction, evaluation and dossiers |
| Specialist review | Approximately 15–30 hours across medieval chant and codicology/palaeography; availability is a prerequisite |
| Independent scrutiny | Approximately 5–10 additional hours if any proposed attribution survives initial review |
| Schedule | Roughly 3–6 elapsed weeks at part-time effort, subject to scholarly responses and access |
| Compute | An existing laptop for curation/baselines; optional existing local GPU for frozen features; no paid cloud dependency |
| Storage | Approximately 1–5 GB if derivatives average 5–10 MB per physical fragment including sides; native TIFF acquisition may be far larger and requires a separate decision |

The combined labour estimate is about **85–170 hours**, or **90–180 hours including independent scrutiny**. Costs depend primarily on access to specialist time; no monetary rate or free availability is assumed. Phase 0 incurred no paid API/cloud charges. If expertise or usable images cannot be secured, spending on models is not justified.

Useful outcomes include a supported additional attribution or exclusion, a corrected association ledger/crosswalk, a tested retrieval method with failure cases, or a well-supported negative result showing that visual similarity does not improve on textual/codicological evidence. A public-facing narrative should be built around those verified outcomes. A compelling story alone is not scholarly value.

## 12. Decision gates and stopping point

| Required GO criterion | Phase 0 result |
|---|---|
| Meaningful sample of real images | **PASS, bounded:** Swedish music, one two-sided Finnish leaf/PDF, Beauvais and one legal comparison retrieved; not a full coverage census |
| Metadata permits useful candidate filtering | **PASS with limits:** complete MPO export audited; geographic/detail sparsity and uncertain formats matter |
| Suitable validation dataset | **PARTIAL:** accessible positive controls exist; reconciled multi-codex Nordic truth and hard-negative set not secured |
| Credible unresolved question | **PARTIAL:** specific documented attribution uncertainties exist; present research status/novelty not confirmed |
| Distinguish documented from potentially original | **PARTIAL:** substantial prior work identified; no exhaustive candidate novelty clearance |
| Technically feasible small test | **CONDITIONAL:** no expensive engineering required; image access, quality and expert labels remain gates |

**CONDITIONAL GO** is the defensible decision. Approving Phase 1 should authorize a small access/reference-data/replication pilot with the explicit stop gates above, not a claim that new medieval relationships will be found. Do not expand to a large system, full-corpus downloading or a public site until these conditions and pilot evidence have been reviewed.

**Phase 0 ends here. Phase 1 requires the user's explicit approval.**

## Evidence package and reproducibility

- [Access audit script](research/access_audit.py): bounded probes only; offline mode profiles the cached CSV. `--probe` makes live requests and overwrites its primary access receipt; retain the delivered receipt when reproducing.
- [Executed metadata notebook](research/metadata_audit.ipynb), [profile](research/mpo_profile.json), [sample summary](research/mpo_sample_summary.json), [timestamped access log](research/access_log.json).
- [Original MPO deposit metadata](research/zenodo_record.json), [cached CC0 CSV](research/mpo.csv), [selected candidate rows](research/mpo_target_records.json), [combined-dataset deposit metadata](research/combined_record.json).
- [Finnish candidate research](research/finnish_candidates.md), [Swedish/CODICUM/legal research](research/sweden_codicum.md), [validation/Ege research](research/validation_ege.md).
- Maintained goal files: [research state](RESEARCH_STATE.md), [experiment log](EXPERIMENT_LOG.md), [ranked candidates](CANDIDATES.md), [findings and rejected hypotheses](FINDINGS.md), [open questions](OPEN_QUESTIONS.md).
- Continuation evidence: [novelty/source challenge](research/goal_novelty_audit.md), [independent candidate review](research/goal_candidate_review.md), [validation diagnostic audit](research/goal_validation_audit.md), [actual diagnostic results](research/metadata_retrieval_diagnostic.json), [target image receipt](research/target_access_log.json), [identity corrections](research/goal_identity_crosscheck.json).
- Sample manifests, image-info responses and a few actual JPEGs are in [research/evidence](research/evidence/); [Beauvais receipt](research/evidence/beauvais_access.json) and [legal receipt](research/legal_b193_probe.json) identify their sources/rights.

The receipts preserve failures as well as successes. The full image collections, a Finnish metadata harvest, the combined XLSX contents, current curator correspondence, the unread chapter's conclusions, a completed expert gold set, trained visual models and validated AI-matching results are **not** part of this deliverable. The small retrospective metadata diagnostic is included and explicitly limited.

**Delivery review, 21 October:** the cached CSV was recounted: 22,909 records, 37 fields and 15,788 manifest-bearing rows; its SHA-256 remains `f5d2825703be19fd1994bc0b91724c32c67c36535622d5554c37b4029592d00b`. The official Zenodo, CODICUM About and Beauvais overview pages were rechecked and remain consistent with the cited scope and catalogue claims. The Finnish IV.157 page did not load through the web-fetch tool in this review; its evidence remains the previously recorded official-browser inspection, not a newly verified automated route. A separate read-only review found the Phase 0 requirements covered. No pilot experiment was advanced during this delivery review.
