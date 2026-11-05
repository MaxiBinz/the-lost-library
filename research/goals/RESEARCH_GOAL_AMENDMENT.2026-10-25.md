Continue work on The Lost Library in this workspace. Treat this as an amendment to the project’s existing research goal, informed by its current outcomes—not as a fresh project or a reason to discard earlier work.

## Primary objective

Conduct a sustained, systematic investigation aimed at identifying a previously unrecognized medieval music manuscript book (codex) from surviving fragments, or establishing a comparably significant new correction to the scholarly record.

The desired result should be important enough to invite serious scrutiny from leading researchers. Make that possible through a precise, falsifiable claim, strong primary-source evidence, transparent alternatives, and a reproducible argument. Do not optimize for a dramatic claim or assume that a new attribution exists.

“New to science” requires a meaningful check of relevant prior scholarship, catalogues, datasets, and known reconstruction projects. A failed search or an unread source does not establish novelty. Keep “new candidate,” “supported inference,” “independently confirmed attribution,” and “new discovery” distinct.

The matching system is a tool for finding comparisons to inspect. It is not an identity oracle. Existing results show important false positives and misses. Do not describe compatibility scores as probabilities or as proof of codex identity.

## Start from the project’s actual state

Before changing files or choosing a lead, read the current versions of:

- `RESEARCH_GOAL.md`, `PROJECT_STATE.md`, `OPEN_QUESTIONS.md`
- `CANDIDATES.md`, `EVIDENCE_DOSSIERS.md`, `MATCHING_RESULTS.md`
- `INDEPENDENT_RESEARCH_PASS.md` and all later continuation reports
- `data/hypotheses.v1.json`, the current review and observation data, matches, context checks, and their source documentation
- `DATA_RIGHTS.md`, `THIRD_PARTY.md`, `SCIENTIFIC_LIMITATIONS.md`, and the implementation documentation

Check for work newer than E32 before relying on the summary below. Treat source claims, catalogue assertions, model suggestions, and direct image observations as different kinds of evidence.

## Test the complete lead and candidate set

Build a versioned lead register from the project’s records. Include every existing candidate and hypothesis, not only the highest-ranked matches. Reconcile aliases and duplicate records before counting candidates. For each lead, record:

1. The exact claim being tested and the relationship type it would imply.
2. What is already published or catalogued, with sources.
3. Supporting and contradicting evidence, kept separate.
4. The strongest feasible test that could distinguish the candidate from alternatives.
5. Required images, passages, metadata, or expertise; what is available and what is missing.
6. A decision state: supported, contradicted, unresolved, previously documented, or not testable with current evidence.
7. What result would change that state.

At minimum, revisit the current leads, checking their status against the latest project data:

- Fr 10370’s intrinsic text order, marks, and previously documented placement between IV.157 ff.7 and 8, separately from the qualified Codex 1505 association.
- The IV.156/IV.157 hVIII–hIX address comparison, including reset numbering, composite structure, and source-description alternatives.
- The Fr 1385/Fr 10406 ornament and layout comparisons, with different-book controls.
- Fr 20274’s text and chant evidence, separating visible manuscript readings from edited text and reported witness readings.
- The Fr 8994 `IIII`/`k` opening-signature lead and the proposed comparison with Fr 20278 and F.m.IV.157.
- The Fr 4223/8311/8455 suggestions involving Fr 1385, in light of the published BOMPAC assignments.
- The IV.173, Hy 49/Fr 25592, Ant 242/Fr 29666, and Ant 99/IV.157 relationships, keeping “same codex,” “suggested association,” and broader stylistic or liturgical grouping distinct.
- The Fr 8311 chant identification and any other text, notation, ruling, decoration, foliation, quire, or physical-structure leads in the candidate set.
- The published different-book control and known-positive controls. Preserve them as controls; do not weaken or remove them to make a method look successful.
- The possible reciprocal-ratio error in Duba’s published image-scaling method. Track it as a separate methods lead unless it bears directly on a codex claim.

This list is a minimum, not a substitute for auditing the complete candidate data. Do not turn an inaccessible image, unread publication, or missing text into a negative result. Try legitimate, ordinary access routes where useful; record exact outcomes and stop at access restrictions rather than bypassing them.

## Research method

Prioritize primary evidence that can distinguish one book from a shared workshop, script, notation style, liturgical tradition, or capture artifact. Seek complete corresponding text sequences, diagnostic variants, physical joins, foliation or quire evidence, and reliable side/order information where available.

For any new test:

- State the claim, alternatives, and predicted observations before inspecting the decisive region where practical.
- Preserve source URLs, catalogue identifiers, licenses or rights statements, checksums, image dimensions, and exact image regions.
- Keep observations, interpretations, catalogue statements, published claims, and editorial reconstructions explicitly separate.
- Record counterevidence and plausible explanations, including composite books, reused material, shared production, catalogue errors, and incomplete captures.
- Use controls. Do not generalize from a single match or a selected post-inspection comparison.
- Keep the frozen ten-pair queue and its associated reviews intact. Any expanded or newly selected screening set must be versioned separately and must disclose how it was selected.
- Use models to prioritize review only. Do not claim improved recognition without defensible labels and an untouched, book-level evaluation.
- Search relevant scholarship and institutional sources before making a novelty claim. Cite exact sources and mark any passages that remain unread.

Respect the project’s existing acquisition and rights limits: no access-control bypass; no unapproved outreach, upload, public deployment, or publication; stay within the recorded image and download budgets unless I authorize a change. Do not contact researchers or institutions without my explicit authorization.

## Add a practical manuscript-knowledge ontology

Design and implement a small, usable ontology for the knowledge this investigation creates. Start from the project’s real cases and the questions researchers need to ask. Avoid an elaborate abstract model that cannot be populated from the evidence.

The model must distinguish at least:

- A manuscript/book or codex from its surviving physical fragments, leaves, and sides.
- A physical object from its catalogue records, identifiers, aliases, image captures, and image derivatives.
- A source assertion from a project observation, a computational suggestion, and a researcher’s interpretation.
- “Same codex,” “physical join,” “textual continuation,” “same hand,” “stylistic similarity,” “liturgical relationship,” and “suggested association.”
- A claim from the evidence supporting or challenging it. Claims must be attributable to a source or agent and record date, scope, status, and provenance where known.
- Unknown or missing information from a negative assertion.

Represent competing claims side by side. Do not force records into one definitive book assignment when evidence supports multiple alternatives. Do not use uncalibrated compatibility scores as confidence values.

First write competency questions, a concise data model, and examples drawn from the current project. Then implement a versioned, machine-readable MVP that can link to the existing source records without silently rewriting them. Prefer a simple format that the project can maintain and validate; keep a path open for standard semantic-web export if it proves useful. Document entity types, relationship types, claim status, identifier handling, provenance, and how evidence regions are referenced.

At minimum, show how the ontology represents:
- The qualified Codex 1505 and IV.157 relationships.
- The documented IV.157/Ant 99 relationship.
- IV.173’s broader grouping versus its specific same-codex relation to Ant 242/Fr 29666.
- An unresolved candidate such as Fr 8994’s opening-signature lead.
- A published rejection such as the 8201–8304 different-book control.

## Update the research goal and report honestly

Amend `RESEARCH_GOAL.md` to include the discovery objective and the ontology workstream while preserving the existing research history and constraints. Update the project state and open-questions documents to reflect actual findings, blocked tests, and next steps. Do not overwrite historical reports or frozen experimental data.

Work through the leads until each has a clear evidence-based status or a concrete, documented external dependency. When a new attribution appears promising, build a reviewable argument that identifies what would falsify it and what independent confirmation is still needed. Do not claim independent confirmation unless it has actually occurred.

Report:
- Which leads were tested and how.
- Which results materially changed the case.
- What remains unresolved, including missing sources and unread scholarship.
- Whether any claim meets the project’s stated novelty standard, and why.
- How to reproduce the tests and inspect the ontology.
- The next highest-value test.

The goal is a credible discovery or a rigorous account of why the available evidence cannot yet establish one. Continue as far as the available evidence and authorized actions allow; do not stop at a plan when the underlying tests can be carried out.