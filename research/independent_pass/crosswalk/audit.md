# Independent source-crosswalk pass

22 October 2026. This pass checked the pinned CC0 CSV, normalized working records and newly inspected **indexed institutional catalogue text**. No source image or PDF was downloaded; no person was contacted. Findings concern exact prior assertions and tests, not a new medieval attribution. Run `audit_crosswalk.py` in this folder to reproduce the CSV checks.

## Concrete result

**A specific published insertion has been flattened in our summary into generic similarity.** The older IV.157 description places a Swedish Mary Magdalene leaf, identified through Finska Cameralia48 / Christiern Philipssons1610, between Helsinki ff7 and8. The pinned CSV maps that account to **Fr10370, Finska cameralia48:7 1610**, and the later catalogue note supplies this complete crosswalk explicitly. Yet the later note qualifies the five-leaf Codex1505 association. Preserve the particular placement and the qualified group statement separately; neither is our discovery. [IV.157 institutional description](https://fragmenta.kansalliskirjasto.fi/handle/10024/1300)

**There is a conditional difference in side labels we can test.** Finnish descriptions specify a lowercase letter at the medieval verso head and a Roman numeral at the recto head. Fr10370's MPO note labels `k` as1r and `II` as1v. This warrants checking actual images and intrinsic text order before using catalogue r/v in a medieval sequence. It does not establish wrong-book identity. [IV.156 description](https://fragmenta.kansalliskirjasto.fi/handle/10024/1299), [IV.173 description](https://fragmenta.kansalliskirjasto.fi/handle/10024/1314)

A further catalogue-level falsifier is available: IV.156f2 and IV.157f5 share the opening interval **hVIII–hIX** but have different feast material (Peter/Paul versus John Baptist). They cannot occupy the same unrepeated signature address if both source readings are accurate. Repeated/reset numbering, composite structure and catalogue error remain alternatives. Images have not independently verified this exclusion. The next useful test is the actual opening signatures and overlapping words, not a global similarity score.

## Crosswalk and modality

The complete22,909-record pinned CSV, not a selected sample, gives these exact memberships:

| Source label | Exact fragment IDs | Assertion limit |
|---|---|---|
| Hy49 | 25592 only | Identifier is resolved in this deposit; a same-book association is only suggested. |
| Ant242 | 29666 only | Its note explicitly associates it with HelsinkiAnt173; second image is missing locally. |
| Ant99 | 20274–20278 | Five catalogue leaves; only20274has a local image pointer. |
| Codex1505 | 8994,10370,10406,10407,10437 | Five catalogue leaves; group identity is catalogue reference evidence. |

Fr29666's German note separates a comparison with Hy49 from an explicit same-codex claim for HelsinkiAnt173. The Finnish updated note makes the same distinction between accepted Ant242 and suggested Hy49/Ant99. Thus the Hy49 alias need not remain a generic unknown; the accuracy of the historical association does. Two-column, early-dated Fr25592 remains unsuitable as a validated late-fifteenth-century positive. Metadata conflict alone cannot exclude a composite book or a mistaken description.

The IV.156 updated note also has heterogeneous wording: Codex1505 is qualified in one passage and equated with IV.157 later in the field. This is a reason to preserve source layers and investigate, not to merge all catalogue units.

## Existing controls against false interpretation

Finnish prose dimensions are not labelled leaf size versus written space in the inspected metadata. MPO does distinguish these fields. Comparing the Finnish width/height figures directly to MPO leaf size would therefore be unjustified; a transposition/measurement-category hypothesis needs verification. Fr1385 and four Codex1505 entries have explicit margin-signature notes; Roman numerals alone are not unique addresses because letters distinguish different openings.

The local Finnish `raw` object is a compiled project summary, not a preserved original API body. The present indexed catalogue reading strengthens the traceable source record but is still not direct inspection of the printed Taitto volume, current physical manuscript, or later Keskiaho chapter. Index text contains OCR corruption. No current browser screenshot was obtained.

## Next tests within existing research scope

1. Inspect Fr10370 top margins and text direction. Record literal letter/numeral pixels without first assigning recto/verso. Test the apparent reversal against the Finnish convention.
2. Compare its actual words with IV.156f8 (catalogued kII–kIII, Mary Magdalene→James) and with the already documented IV.157 ff7/8 gap. This distinguishes a known placement from a newly inferred adjacency. Catalogue feast labels alone do not settle the comparison.
3. Verify the hVIII–hIX conflict from IV.156f2 and IV.157f5 images if legitimately obtainable. Test reset numbering and composite-book alternatives explicitly.
4. Inspect Fr1385 IX/D, Fr10407 IX/i and Fr8994 IIII/k. Pair full letter+numeral addresses and text; never deduplicate from IX alone.
5. For IV.173, test the catalogue's terminal-leaf premise against the actual last staff. Keep blank/incomplete notation elsewhere as an alternative to an automatic end-of-book inference.

Fr10370 is an already selected family comparator, not an eleventh frozen hypothesis. These tests support the existing H02/H03 attribution question without silently changing the queue. No confirmed relationship or originality claim is produced by this crosswalk pass.

## Executed conditional consistency check

`check_source_constraints.py` writes `source_constraints.json`. It evaluates the explicit joint premises for the hVIII–hIX comparison and separately checks Fr10370's side-label pattern. All16Boolean combinations of the four opening-premise assumptions were evaluated; unknown premises remain unresolved rather than receiving a book-identity verdict. This is a conditional argument check, not a measured attribution method or an independent historical observation.

**Actual result: unresolved.** The catalogue addresses agree and feast labels differ, but the retained comparison lacks complete corresponding chant/text readings. Thus mutually incompatible text is an unverified additional premise. If accurate identical addresses, unique unrepeated numbering, the same physical position and incompatible text all hold, their conjunction fails. Reset/composite numbering, transcription or side error, and incomplete content summaries remain explicit alternatives; different books is only another alternative.

**Fr10370 actual result: unresolved.** The literal k/II r/v pattern is reversed relative to the Finnish convention. The conditional side-label inconsistency applies only if both records describe the same medieval side convention and signature scheme accurately. It supplies no final recto/verso assignment or wrong-book verdict. The frozen queue SHA is unchanged.


## MPO/CCM side-convention qualification

The two bounded public searches did not locate an authoritative MPO/CCM rule assigning1r/1v to original medieval rather than present fragment/wrapper sides. This is not proof that such a rule is absent. The already-cached Duba article, printedp7/PDF9, explains why fragment-side numbering can follow present physical order rather than the original codex. That general observation does not establish the particular MPO convention. Consequently the10370token pattern remains conditional, and no catalogue error is asserted. Exact search limits, source URL/page and unresolved points are in `side_convention_note.json`.
