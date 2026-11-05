# Phase 0 evidence: validation, Beauvais, Ege, and technical precedents

Research date: 19 October 2026. Evidence-only research; no matching system was built or run. Live access artifacts are in `research/evidence/`. Counts below distinguish catalog statements, manifest contents, and actual image retrieval.

## Beauvais Missal: suitable positive-control corpus, insufficient by itself

The authoritative [Fragmentarium reconstruction F-4ihz](https://fragmentarium.ms/overview/F-4ihz), described by Lisa Fagin Davis, catalogs a **single** late-thirteenth-century missal from Beauvais, dated 1270–1300, with **122 leaves of an original 309**. It includes music in square notation, but is neither a Nordic antiphonary nor a gradual. Its existing membership and ordering supply scholarly reference associations; reproducing them would be validation, not discovery. The reconstruction links exact holdings, including Harvard Houghton MS Typ 956 1/F-ag0v and Typ 956 2/F-g58m, Cleveland Museum of Art 1982.141/F-6zvk, and Lima Public Library Ege Set 29 no.15/F-qbrf. The catalog's 122 is not a current census of successfully accessible unique leaves.

A direct GET of the [IIIF Presentation 2 manifest](https://fragmentarium.ms/metadata/iiif/F-4ihz/manifest.json) returned HTTP 200, application/json, **220,065 bytes**, containing **240 canvases/image references**. This is not 240 fragments or proof that all 240 images function. There are 226 local Loris references and 14 external references. Four Boston image resource URLs are malformed: they collapse to `https://ark.digitalcommonwealth.org/full/full/0/default.jpg`; the service objects retain specific Digital Commonwealth IIIF identifiers. There are also repeated human-readable labels. Derive leaf/side identity from reviewed source records, not sequential canvas counts or image filenames. The 122-leaf/240-canvas discrepancy needs reconciliation before scoring a benchmark.

### Actual image requests

All four following small samples returned HTTP 200 and JPEG data; the first and fourth were decoded and visually inspected. This establishes retrieval, not full-dataset coverage. JSON logs record content types, bytes, and SHA256.

| Child record and holding | Actual image URL | Retrieved | Child-manifest rights |
|---|---|---:|---|
| [F-6zvk](https://fragmentarium.ms/overview/F-6zvk), Cleveland Museum of Art 1982.141 | [CMA recto, 400px](https://fragmentarium.ms:443/loris/F-6zvk/CMA_r.JPG/full/400,/0/default.jpg) | 70,627 bytes; 400 × 553 px | Public Domain Mark 1.0 |
| [F-qbrf](https://fragmentarium.ms/overview/F-qbrf), Lima Public Library Set 29 no.15 | [Lima recto, 400px](https://fragmentarium.ms:443/loris/F-qbrf/Lima_r.JPG/full/400,/0/default.jpg) | 61,829 bytes; 400 × 565 px | Public Domain Mark 1.0 |
| [F-g7p5](https://fragmentarium.ms/overview/F-g7p5), Waseda University | [Waseda recto, 400px](https://fragmentarium.ms:443/loris/F-g7p5/Waseda_r.jpg/full/400,/0/default.jpg) | 67,015 bytes; 400 × 589 px | No Known Copyright (NKC), **not** an explicit CC licence |
| [F-5uba](https://fragmentarium.ms/overview/F-5uba), Australian National University Library | [ANU music page, 1200px](https://fragmentarium.ms:443/loris/F-5uba/Chifley_005_cropped.jp2/full/1200,/0/default.jpg) | 527,097 bytes; 1200 × 1730 px | CC BY 4.0 |

The ANU sample visibly resolves square notes, red staff lines, words, initials, and margins; it also shows substantial bleed-through. The Cleveland sample is a text page. The variation in page contents means not every Beauvais leaf tests musical similarity. [ANU's own repository record](https://dspace-prod.anu.edu.au/items/64fae581-bf94-4811-8866-b371b00a4aee/full) independently identifies the liturgical contents and offers JPG and preservation TIFF files; those large originals were not downloaded.

The composite manifest asserts Public Domain Mark, but the sampled child manifests differ. [Fragmentarium's terms](https://fragmentarium.ms/pages/terms) explicitly direct users of multi-collection reconstructions to the individual fragments for collection-specific rights. Metadata and scholarly descriptions have separate terms. Preserve the institution, shelfmark, Fragmentarium identifier, creator attribution where required, and exact licence URL per asset. Do not use the aggregate's PDM as a blanket licence. The [Broken Books project site](https://brokenbooks2.omeka.net/) has a CC BY-NC-ND rights statement for its own content; that statement also must not be generalized to all provider images.

### Established sequence and physical evidence

[Davis's 2015 first-person reconstruction account](https://manuscriptroadtrip.wordpress.com/2015/03/24/manuscript-road-trip-reconstructing-the-beauvais-missal/) documents pairing consecutive leaves, reconstructing quires, and using mirror-image gold offsets as physical evidence. One illustrated established adjacency is Houghton MS Typ 956 2 and a leaf sold at Christie's on 4 September 2013, lot 262 no.1. This is a promising independently explained positive association, rather than a label inferred from visual similarity. Validate present identifiers and the curator's certainty before freezing it as an adjacency label. The linked [VCEditor project](https://vceditor.library.upenn.edu/project/61706e8942764a0001a3cbe7/viewOnly) timed out in web retrieval; its complete quire labels were **not** independently extracted. The 2015 handlist and missing-leaf statements are historical, not a current missing-leaf census.

**Judgment:** real images, established same-codex labels, and documented sequence evidence make Beauvais a credible small positive-control source. Its mostly complete detached leaves, French script, and modern dispersal are a domain shift from damaged Nordic binding fragments. One codex cannot establish general manuscript identity discrimination or confidence calibration. A Beauvais-only benchmark without difficult other-codex negatives is inadequate.

## Another concrete Ege control (outside Nordic discovery scope)

[Fragmentarium F-djs6](https://fragmentarium.ms/overview/F-djs6) is a **single Book of Hours (Use of Paris)**, north France, 1425–1450, with **28 of 189 leaves** in its published reconstruction; Ege FOL no.30. Linked exact identifiers include Morgan Library M.1021/F-77tw (reconstructed f.15), Ohio State Set 2 no.30/F-jk4x (f.120), and Stony Brook Z109.e4/F-nmq2 (f.157). Cataloging is credited to Lisa Fagin Davis's Simmons students in 2017. This could supply a different held-out codex, subject to its own image and rights audit, which was not done here. Missing sections and surviving foliation support reconstruction tasks, but this is established research and is not a Nordic musical target. A public artifact could compare a recovered ordering to the scholarly reconstruction while marking lacunae.

## Ege alternative: accessibility and originality

[Denison's institutional project](https://ege.denison.edu/) explains the portfolio structure: forty sets, with one leaf from each of fifty manuscripts in every set, so the portfolio item number provides a useful starting membership label. Its narrative and count of located sets were written in 2008 and are not a current census. Historic item labels require scholarly reconciliation, not automatic acceptance. [Stony Brook's institutional digital collection](https://exhibits.library.stonybrook.edu/s/ege/page/home) states that rectos, versos, context cards, and housings of Set 19 were photographed and described using Dublin Core/VRA. Many institutions thus supply excellent educational and benchmark material. There is no single verified uniform licence for the entire Ege corpus.

Assessment: Ege material gives the fastest route to an interpretable retrieval/ordering demonstration and a compelling public story. Its existing portfolio numbering and established reconstructions also make naive same-book retrieval trivial if labels leak. Existing work reduces the originality of rediscovering membership. Genuine additions would require tracing unrecorded leaves or correcting a specific documented uncertainty after comparison with specialist handlists, catalogues, auction histories, and the researchers' current records. Missing catalog fields do not establish novelty. Ege is strongest as validation, not a reason to abandon Nordic discovery research before its access and specialist gates are resolved.

## Relevant primary technical precedents

1. [Gogawale et al., Bag of Bags, CVPR Workshops 2026](https://openaccess.thecvf.com/content/CVPR2026W/SINT4CH/html/Gogawale_Bag_of_Bags_Adaptive_Visual_Vocabularies_for_Genizah_Join_Image_CVPRW_2026_paper.html) studies same-manuscript retrieval for Cairo Genizah fragments, reporting Hit@1 0.78/MRR 0.84 for its best variant. This supports the plausibility of handwriting-based retrieval, not transfer accuracy on Latin parchment or music. The [author repository](https://github.com/TAU-CH/midrash_bob) offers MIT-licensed code, but its advertised [data directory](https://github.com/TAU-CH/midrash_bob/tree/main/data) contained only `.gitkeep` in this audit. Thus the abstract's statement that dataset and code are available must **not** be repeated as verified downloadable image availability. No model was installed, trained, or run. The official webpage was search-index accessible but a subsequent direct web open returned 403; the author README independently describes the method and metrics.
2. [Reunion helper, Heritage Science 2024](https://www.nature.com/articles/s40494-024-01150-3) concerns fragments from the **same sheet**, using edge geometry and a Dunhuang evaluation corpus that includes generated curves. This is a different target from identifying nonadjacent leaves of the same codex. Its high classification scores are not an accuracy forecast here. A later direct article open redirected to an inaccessible identity endpoint; the primary article's indexed text was readable.
3. [Hock et al., Optical Medieval Music Recognition—A Complete Pipeline for Historic Chants, Applied Sciences 2024](https://www.mdpi.com/2076-3417/14/16/7355) evaluates text/music/layout transcription, including square notation, and links [OMMR4all datasets](https://github.com/OMMR4all/datasets). OMR may provide chant sequences as supporting features; successful transcription does not prove codex identity. Northern notational variation and damaged fragments require separate testing. No OMR training is justified in Phase 0.

## Proposed validation experiment (design only)

### Define separate claims

Use four labels: (1) same physical leaf/piece join, (2) same codex, (3) adjacent leaves or quire position, and (4) related text/notation/workshop. Score each separately. Repeated chants can support (4) while being a difficult negative for (2). Do not evaluate image embedding similarity as if it directly measured identity.

### Freeze scholarly ground truth before looking at suggestions

Build a versioned association ledger: exact institution IDs, physical leaf/recto-verso grouping, codex assignment, evidence citation, certainty, adjudicator, date, and explicit known/unknown status. Require a specialist-reviewed subset of strong same-codex relationships. Add Beauvais as positive control and at least several genuinely different books, including Nordic known memberships, for domain validation. A practical target is 100–300 physical fragments across at least 5–10 codices, including at least three unseen evaluation codices if the verified data permit. These are proposed design targets, not achieved data counts. If that minimum cannot be obtained, report the result as a feasibility case study rather than general validation.

### Prevent leakage

Split by **original codex**, not image pair. Recto and verso of one leaf, alternate photographs, crops, and augmented copies stay together. Development books are distinct from calibration books and final test books. Freeze feature choices, filters, and thresholds before opening test labels. For each held-out test book, separate leaves serve as queries and gallery members; gallery membership is needed to make retrieval possible, but the system receives no codex/association labels. This query-gallery arrangement is evaluation, not model training. Remove names such as “Beauvais,” Ege item numbers, reconstruction IDs, filenames, catalog relationship fields, and existing sequence positions from model/filter inputs; retain a hidden evaluator-only ID map. Do not let the system browse reconstruction pages while solving the test. Pretrained-data contamination cannot be ruled out, so compare interpretable nonlearned baselines and acknowledge this uncertainty.

### Candidate pool and negatives

Use the same gallery for all methods. Include identical chant/text in different books; similar regional/script hands; same-era and same-region books; similar musical notation; and, where separately established, different books written by one scribe. Include singleton queries with no correct gallery match so abstention is tested. Have a specialist verify negative book separation; absence of an existing association is **not** proof of a negative. Exclude genuinely uncertain pairs from binary ground truth and report them separately. Keep capture backgrounds, ruler styles, and institution watermarks from becoming proxies for identity; test across institutions and report performance by provider.

Compare: metadata-only baseline; metadata plus text/chant sequence; layout/handwriting features; frozen generic visual retrieval; and a transparent fusion/reranking. Use metadata to shortlist, but measure how many positives the filter loses. Compare visual retrieval both with and without standardized backgrounds. Do not train a large model; start with existing representations and measurements.

### Metrics and calibration

- Pair precision = verified true same-codex suggestions / all adjudicated positive suggestions; report counts and uncertainty intervals.
- Pair recall = recovered established same-codex relationships / all eligible established relationships, including true pairs lost by metadata filtering. This estimates recall on known labels, not all surviving unknown associations.
- Hit@k for k=1,5,10 = proportion of eligible queries with at least one known true match in the first k suggestions. Also report recall@k (fraction of all known relevant gallery items recovered) and MRR. Exclude self-images and grouped recto-verso matches.
- Report false positives per 100 queries, per negative subtype, and false-positive rate FP/(FP+TN). State how candidate sampling changes class prevalence: precision on an artificially balanced test is not production precision.
- Calibrate only on separate books: reliability bins, Brier score, and expected calibration error with sample counts. A cosine score or softmax over a shortlist is not a probability. If too few independent books/pairs support calibration, output ranked evidence with abstention, and explicitly decline numerical probability claims.
- Use codex-level macro averages and group-aware uncertainty estimates, not thousands of correlated leaf pairs as independent samples. Report denominator sizes and performance by damage, notation family, and institution.

A reasonable preregistered **target**, not a demonstrated result, is Hit@5 >=0.8 on the small held-out sample and >=0.9 precision among a small expert-review queue, plus improvement over metadata/text alone without catastrophic recall loss. With few held-out codices, intervals will be broad; meeting point targets does not establish a universal success rate. Release a negative result if visual information adds no useful retrieval value.

### What counts as original evidence

Only after passing known-association validation should unlabelled Nordic candidates be examined. Each proposed relationship needs an evidence dossier covering measurements, text/chant continuity, hand/notation, conflicting evidence, alternative explanations, scholarly search, and specialist review. A recovered known association is validation. A previously unindexed association is a catalog enhancement until broader novelty checking. A new same-book or physical-join claim needs independent scrutiny before public announcement. A future interactive artifact should display accepted, rejected, and uncertain links, missing leaves, source citations, and the reasons for each relationship.

## Recommendation to parent

Use Beauvais as a real, accessible positive-control corpus, with individual rights and identity auditing. It is not a complete standalone benchmark for Nordic music reconstruction. Ege is the easiest initial methodology demonstration; Nordic music remains the stronger discovery direction if exact target books, current scholarly novelty, multi-codex validation, and adequate images are secured. A **CONDITIONAL GO** is more defensible than unconditional GO on this evidence. No claim of a newly unknown medieval association is established here.
