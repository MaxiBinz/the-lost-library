# The Lost Library — evidence-led discovery goal

Created 21 October 2026, Europe/Vienna.

## Objective

Use the existing Lost Library prototype to investigate previously unestablished relationships among Nordic medieval music-manuscript fragments. Seek an original, reproducible historical finding supported by independently checkable textual, musical and codicological evidence. AI should help find, read, compare and challenge evidence; it must not manufacture certainty, scholarly novelty or expert endorsement.

The desired result is a defensible new attribution, exclusion, sequence, catalogue correction, or historically meaningful observation. A known catalogue suggestion can be resolved with new evidence, but the suggestion itself must be credited. A new finding and a useful new method are separate claims and require separate validation.

## Starting point: preserve what we actually know

Audit and reuse existing code, images, receipts, bibliography, tests and experiment outputs. Reconcile outdated project notes before extending the system. The current inventory records 129 catalogue/image records, 120 imaged physical objects and 133 source images; repeated views are not additional fragments. A local viewer, matching experiments and a documented Graduale Aboense reconstruction demonstration exist.

Current experiments do not establish a novel manuscript relationship. Advanced visual methods have not demonstrated improvement over the simpler baseline. A published same-hand/different-book pair defeats the matching methods. Closed-gallery retrieval scores are not identity probabilities or proof of usefulness on unknown books. Do not relabel these results as a discovery.

## Initial research question and novelty gate

Start with the attribution boundaries around Helsinki F.m.IV.157, IV.156 and IV.173, Swedish Codex 1505 (Fr 8994, 10370, 10406, 10407, 10437), and documented IV.157 comparators Fr 1385 and Ant 99. Keep same book, same scribe, shared workshop, shared liturgical tradition and catalogue alias as distinct explanations.

Before pursuing originality, seek and read legitimately available relevant scholarship, especially Jesse Keskiaho's “En grupp handskrifter från Nådendal: nya rön,” pp. 51–67 (volume dated 2018; author bibliography 2019), and relevant Taitto passages. Record inaccessible sources precisely. Check current public CODICUM/BOMPAC outputs. An inaccessible decisive source leaves novelty uncleared; it does not demonstrate a gap. Do not repeat failed access attempts or bypass restrictions.

If this question is already settled, document that result and assess the existing Ant 49 audit lead or at most one additional specific music-manuscript target. Select a new target only with exact identifiers, legitimate access and a source-backed question. Do not expand indefinitely to seek an exciting result.

## Suitable research stack

- Keep Python, SQLite, original metadata/IIIF manifests, JSON/CSV exports and the existing local viewer where they already serve the research. Use local Git history for reproducibility when appropriate; do not publish remotely without approval.
- Use IIIF-compatible comparison and region annotations. Adopt Mirador only if its capabilities materially improve the existing viewer; replacing working software is not a research result.
- Use Fragmentarium and institutional catalogues for source descriptions, documented reconstructions and references. Keep local proposals distinct from institutional records; no external edits without authorization.
- Use Cantus Database/Cantus Index for chant identification and concordances where coverage permits. Preserve the manuscript's literal reading separately from normalized text and chant identifiers. Record unsuccessful searches and avoid treating database absence as rarity.
- Maintain a source-linked bibliography in an interoperable format suitable for Zotero. Do not require a Zotero installation or account to reproduce the work.
- Evaluate specialized handwriting or medieval music recognition only against manually checked representative passages. Transkribus or an equivalent HTR tool and OMMR4all or an equivalent music-recognition tool are optional, not mandatory dependencies. Use existing permitted local capabilities first. Do not upload images, pay for services or acquire accounts without applicable authorization.
- Prefer interoperable annotations and exports over bespoke locked formats. Use TEI/MEI only where an actual transcription or musical edition warrants them; no unnecessary infrastructure.

## AI-native evidence workflow

1. Create a versioned hypothesis ledger. Each claim has exact fragment/leaf/side identifiers, source citations, image region coordinates, literal observations, proposed interpretation, contrary evidence, alternative explanations and review state.
2. Keep machine proposals, human corrections, catalogue assertions and independent expert judgments separate. Log model/tool versions, inputs and transformations. Mark illegible and uncertain readings instead of silently completing them.
3. Let AI propose readings, chant IDs, visual comparisons and contradictions. Verify decisive evidence against the source image and cited reference. Never use agreement between AI outputs as independent corroboration.
4. Study a small number of informative passages before general image similarity: chant/text succession, distinctive variants, corrections, liturgical positions, ruling, written-space conventions, distinctive letterforms, opening/quire marks and physical damage where observable. A generic text match, common notation or shared catalogue description cannot establish identity.
5. Give each promising hypothesis an explicit falsification test. Consider different books copied by the same hand, duplicated text, inherited metadata, folded/cropped captures, date errors and composite volumes. Retain rejected cases and reasons.
6. Update the local viewer so a reviewer can follow a claim directly to the precise image region, source and objection, then export the complete dossier without needing the AI session.

## Bounded experiments and validation

Freeze an initial queue of no more than 10 distinct candidate relationships, distinguishing previously accepted, previously suggested and genuinely new proposals. Review the whole queue and report unresolved cases; do not cherry-pick survivors. Changing the queue requires a recorded reason and a new version.

Use established positive controls and literature-backed difficult negatives. Resolve physical object/capture grouping and source page-side mapping. Preserve whole-book separation in development, calibration and evaluation; mask association labels and revealing prose. Disclose inherited catalogue attributes and other leakage risks. Report retrieval, filtering losses, tie handling, false acceptance, sample denominators and uncertainty. Previously inspected tests remain exploratory; any improved-method confirmation needs a genuinely untouched evaluation set when feasible.

Evaluate whether chant/text/region evidence helps distinguish the existing convincing false match and recover documented target associations that metadata missed. Test each added signal against the same simpler baseline. Do not fine-tune indefinitely on these examples or claim population accuracy from a few selected cases. If independent labels or adequate texts cannot be secured, publish case-study limits rather than calibrated identity probabilities.

## Evidence standard and expert review

A finding is ready for specialist review when its novelty audit is explicit, decisive observations are traceable, serious alternatives have been tested, and no unresolved contradiction is hidden. Seek converging evidence from meaningfully independent channels; two measurements copied from one catalogue description do not qualify. Evidence quality matters more than an arbitrary count of agreeing features.

Classify dossiers A (strong), B (plausible), C (ambiguous), D (rejected), or E (previously documented), while recording originality and review status separately. An A label is an internal assessment, not expert confirmation. No score alone promotes a hypothesis to a confirmed attribution.

Prepare a concise specialist-review packet identifying the strongest claim, competing explanations, precise questions and relevant images. Contact or send material to manuscript/chant specialists, holding institutions or CODICUM only after explicit user authorization. Do not claim independent verification until an actual qualified reviewer has supplied it. Physical examination or institution-led imaging may remain necessary.

## Deliverables

1. Updated PROJECT_STATE.md, TARGET_MANUSCRIPT.md, EXPERIMENT_LOG.md and OPEN_QUESTIONS.md, consistent with actual outputs.
2. A source and prior-art ledger that separates read sources from bibliographic leads and inaccessible material.
3. A structured hypothesis/evidence dataset with region-linked observations, uncertainty and provenance.
4. Reproducible bounded experiments, comparisons with baselines and a VALIDATION_REPORT.md.
5. EVIDENCE_DOSSIERS.md and machine-readable dossiers, including contrary evidence and rejected hypotheses.
6. An updated local viewer that supports inspection of the actual evidence without overstating reconstruction or novelty.
7. FINAL_REPORT.md distinguishing technical achievements, new observations, previously known relationships and unverified hypotheses.
8. A reviewer packet, setup/reproduction README, dependency and data-rights documentation, and a draft research narrative. Prepare for GitHub release locally; public release remains a separate approved action.

## Resource and action boundaries

Keep the total working source-image inventory at or below 300 and total project downloads below 3 GB, counting existing acquisitions and additional derivatives. Audit existing usage before fetching more. Use existing local compute; no paid API/cloud service or large-model training. Respect per-item rights and archive restrictions. Do not contact others, upload manuscript material to external services, edit external catalogues, or publicly publish/deploy without explicit authorization. Ask before expanding these limits. No autonomous recurring task or multi-agent delegation is implied by this goal.

## Completion and honest stopping rules

The desired scientific success is at least one source-backed, plausibly original finding that survives adversarial review and, before being called independently confirmed, actual qualified specialist scrutiny. Expert surprise is not an acceptance criterion.

Do not promise or require that nature will supply a new discovery. The bounded investigation can also finish with a fully documented negative or replication result after the defined candidate queue and justified limited pivot have been exhausted. In that outcome, deliver the reproducible evidence package, explain why no unique finding was established, and explicitly state that the discovery ambition was not achieved. This does not by itself establish a novel methodological publication.

If decisive progress requires inaccessible scholarship, expert judgment, original-object access or an external action, finish all independent local work, record the exact dependency and prepare a concrete request for the user. Do not substitute speculation or manufacture a finding to close the goal. Observe the goal tool's blocking rules when reporting blocked status.

## First execution priorities

Reconcile saved scientific outputs and current status; complete the prior-art/novelty audit; identify the smallest source passages that could distinguish the competing hypotheses; then implement evidence annotations and run the bounded comparisons. Spend engineering effort only where it makes a historical claim more testable.
