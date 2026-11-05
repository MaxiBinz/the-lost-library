# Research continuation E20: source order, initials and actual witness readings

23 October 2026. The existing evidence-led discovery goal is active. This continuation follows the same objective, with the frozen ten-pair queue and original predictions preserved. **No original historical attribution, exclusion or independently confirmed finding is established.**

## What we learned

| Source test | Result | Consequence |
|---|---|---|
| Fr 10370 text at the end of photograph 2 and start of photograph 3 | Candidate *Ardore caritatis succensa quem* continues with *sepultum noverat…*, matching responsory verse Cantus 601029a after declared normalizations. | Text supports relative reading order 2→3. This adds evidence beyond photograph ordinal; it does not prove a seam, complete physical reconstruction or catalogue error. |
| H02 initials controlled for candidate letter A | Selected Fr 1385/10406 A forms retain the earlier specific ornamental resemblance; selected Ant 39 A forms differ. | A narrower descriptive comparison, with exact liturgical roles still incompletely matched. It does not establish rarity, one hand or one book. |
| Published wrong-book control, candidate D against D | Fr 8201/8304 repeat the broader red/pale/lozenge/scallop vocabulary despite the published different-book conclusion. | Broad ornamental vocabulary is insufficient even within one letter class. These are D initials, a separate auxiliary control rather than an A-specific counterexample. |
| Helsinki IV.157 source boundaries | Indexed institutional descriptions specify f.5 John Baptist, ff.6–7 Peter/Paul and f.8 Olaf boundaries. | More precise source assertions for comparison; no Finnish manuscript image or actual IV.156 text contradiction was obtained. |
| Actual Uppsala C23 pages versus Fr 20274 | Ten selected sites were retained: eight were evaluable at text/structure level, comprising seven current/standard word or cue agreements and one written-scope difference; two lacked target text. | The target does not establish a shared distinctive uncorrected C23 error. Corrected/standard agreement is insufficient for a unique transmission branch or copying direction. |
| Fixed Fr 10370 capture-boundary registration | Declared 1/2 and 3/4 regions failed both a translation screen and a fixed SIFT/mutual-ratio/RANSAC screen; the intentionally different 2/3 control also gave small low-inlier fits. | No physical overlap or seam is established. Failure does not show that two captures are different faces, but it prevents treating the visual resemblance as a registered join. |

The C23 counts describe selected word/cue sites. They are not seven independent evidence channels, an accuracy estimate or a measure of rarity.

## Fr 10370: a stronger relative-order argument

The literal candidate on photograph 2 ends `[A]rdore caritatis succensa quē`; photograph 3 begins `sepultum nouerat sublatum cred[ens?] de se pul chro`. Expanding the marked abbreviation to *quem*, normalizing u/v and joining divided syllables produces a candidate continuous verse. The less secure *credens* reading remains explicitly informed by the parallel. Five prefix words and eight suffix words match the cited verse; reversing the selected regions does not form it.

Publicly indexed [Cantus F-Pn Latin 12044 f.165r](https://cantusdatabase.org/chant/402240/), [Wrocław R 503 f.163r](https://cantusdatabase.org/chant/564421/) and [Cambrai 38 f.291v](https://cantusdatabase.org/chant/204152/) attest the verse in other books. These concordances identify a chant; they make no unique codex fingerprint. Direct comparator manuscript images were not inspected in this step.

With the prior proposed photograph 1/2 continuation and the catalogue's single-leaf assertion, 2→3 is consistent with a numeral-bearing surface preceding the k-bearing surface. It does not independently prove every physical premise, full 1/2 or 3/4 seams, medieval side labels or MPO's meaning of `1r`/`1v`. The already published insertion between IV.157 ff.7/8 remains credited prior evidence. The new local result is the explicit source-linked textual continuation, with no first-notice claim. [Protocol and source regions](research/continuation_20/intrinsic_10370/results.md).

### Fixed capture-boundary falsification

The declared 1/2 and 3/4 writing-area boundary regions were first screened with fixed dark-ink translations, then with OpenCV SIFT features, mutual 0.75-ratio matching and 3-pixel RANSAC. No new source image, region or parameter was added after seeing the output. The 1/2 candidate yielded 9 mutual feature matches and 4 RANSAC inliers; 3/4 yielded 28 and 5. The deliberately different 2/3 text-continuity control yielded 18 and 5. The predeclared screen required at least 8 distributed inliers, so none was accepted. Low-inlier homographies are retained for inspection rather than presented as joins. This cannot disprove adjacent but nonoverlapping captures; it means only that the available images do not supply a robust registered overlap. [Feature protocol and exact output](research/continuation_20/registration/feature_results.json).

## Ornament: matching letters improves the question

All four available captures for each of seven objects were screened, totalling 28 files. Selected large candidate A forms were compared after excluding uncertain, partial and other-letter forms. Fr 1385/10406 share pale body fields, a long red stem stripe, small lozenges and a toothed dark edge, while particular lozenge colours and body/crossbar construction differ. Selected Fr 4223/8311 A forms do not show that exact combination securely. Exact chant roles and the prevalence of those features remain unknown.

The auxiliary Fr 8201/8304 comparison uses D initials, correctly identified from their following *e*. Their shared vocabulary survives letter matching in a published same-hand/different-book example. Pooling those D forms as A evidence would be an error. The source checks keep these letter classes and functions separate. No A/B category promotion, hand attribution or validated discrimination rule follows. [Selection inventory and observations](research/continuation_20/ornament/results.md).

## C23: move from the editor's report to actual source pages

The normal institutional Alvin record for [Uppsala C23](https://www.alvin-portal.org/alvin/view.jsf?pid=alvin-record:160517) exposed exact original TIFF links. Two permitted Public Domain Mark attachments, [0144](https://www.alvin-portal.org/alvin/attachment/download/alvin-record:160517/ATTACHMENT-0144.tiff) and [0145](https://www.alvin-portal.org/alvin/attachment/download/alvin-record:160517/ATTACHMENT-0145.tiff), were successfully acquired, totalling 44,885,780 bytes. Local JPEG derivatives retain declared transforms and hashes. They are external comparison sources; they do not enter the core matching predictors, labels or ten frozen hypotheses. See [comparison-source registry](data/comparison_sources.v1.json).

The page correspondence is supported by text/layout with Hallqvist's C23 edition. Attachment 0144 corresponds to the office opening at 71v without an independently read folio numeral. Attachment 0145 has pencil 72 and continuing text supporting 72r. Attachment ordinal alone is not the foliation argument.

Actual C23 source regions show corrections: an interlinear *super* over cancelled pro-like text, a *patri parens* replacement, and a replacement candidate *dampnatur innoxius*. Fr 20274 has the current/standard equivalents in its continuous text rather than the reported earlier states. Other shared cues are ordinary words or incipits. The hymn entry in C23 is visible, while no intervening hymn entry appears in the inspected continuous target transition. This concerns written scope, not performance omission. The source's fragrantissa-like spelling has no target counterpart there and cannot become a shared variant.

Cancelled C23 words are only partly legible. The collation therefore separates direct readings from Hallqvist's report of the full earlier state, and leaves two unavailable target passages unevaluated. C435 original images remain uninspected, so its witness readings are still editorial reports. No common exemplar, copying direction, unique branch, melody or correcting-hand identity/date is established. The selected post-review sites are not a blind or preregistered test. [Complete ten-site collation](research/continuation_20/c23/collation.json).

## Helsinki: a precise access limit

The supported browser reached a Cloudflare check at the ordinary IV.157 institutional record. No refresh, CAPTCHA interaction, alternate-host bypass or guessed PDF download followed. Public search indexing still exposed selected factual boundaries: f.5 spans John Baptist material, ff.6–7 Peter/Paul, and f.8 begins within Olaf's *Regnante illustrissimo*. The catalogue's proposed interleaving of temporale/sanctorale units cautions against a simple global sequence. Its doubtful ff.6–7 address string remains unparsed.

These are indexed catalogue assertions with possible OCR noise, not direct manuscript readings. No matching IV.156 words or images were obtained, so the hVIII–hIX exclusion premise remains unverified. A one-time HEAD check of the catalogue's explicitly listed IV.157 TIFF also met a Cloudflare challenge without transferring image bytes; no bypass or follow-up was attempted. The access limit affects that comparison; other source work proceeded. [Assertions and access receipts](research/continuation_20/helsinki_access/README.md).

## Research inventory and replay

The resource inventory comprises 171 working source files: 167 core JPEGs, two C23 TIFF originals and two declared C23 JPEG derivatives. The core collection remains 120 imaged physical objects with 121 primary analysis images. The two C23 pages belong to one external comparison witness. Duplicated formats are not new medieval objects. Conservative download planning is approximately 1.146 GB including a 1 GB reserve; exact lifetime traffic remains incompletely logged. The 300-image/3 GB limits remain in force.

Reproduce the cached local source checks from the project root:

```sh
.venv/bin/python research/continuation_20/intrinsic_10370/check_order.py
.venv/bin/python research/continuation_20/ornament/analyze.py
```

The [ten-site JSON](research/continuation_20/c23/collation.json) and exact observation selectors preserve the direct textual comparison. Acquisition scripts are not required for replay and should not be rerun to repeat failed access. The frozen selection retains SHA-256 `b3e299a7c600584ce44518db1f5c30c3301edae0a07a8b009075498f64ccec47`, with 2 E / 7 C / 1 D outcomes. No predictor or threshold changed.

E20 integration exported 58 validated regions, four separate context checks and two external C23 pages. The registration script rechecks its source hashes and has no source downloads or mutations. All 167 core source hashes/dimensions passed; the frozen queue and core fragment data remain unchanged. These checks establish technical integrity rather than independent historical truth.

## What remains

The new text-order evidence should be tested against complete surrounding Swedish/Helsinki material when legitimately accessible. Ornamental comparison needs exact incipits/roles and repeated same-letter examples in known same-book and wrong-book material. The C23 result narrows an unsupported branch-fingerprint claim; it does not exhaust wider textual or melodic relationships. Relevant Keskiaho/Taitto material is still needed for definitive novelty clearance of affected questions.

The prior E19 package remains its own verified snapshot until a new manifest/replay receipt records an updated archive. No external contact, source upload, public release or claim of independent expert review occurred. The goal remains active and scientifically incomplete.
