# Manuscript knowledge model, version 1

## Current assessment — E55,31October2026

Knowledge1.19.0 has959 entities,641 claims and167 regions across168 entries/117 pairs. Lead states and frozen2E/7C/1D are unchanged.208 source files and the conservative1,675,854,139-byte plan are unchanged. E55 source-geometry outcomes are project observations; they do not assert sounding pitches or identify a codex. The E39 interpretation retains its original provenance alongside the failed follow-up and explicit uncertainty. [E55](RESEARCH_CONTINUATION_55.md). Earlier dated sections describe historical snapshots.

## Current assessment — E54,31October2026

Version1.18.0 adds exact E54 capture/region provenance and two scoped observations. A supported observation about mark visibility or later reuse is distinct from an unresolved same-codex interpretation. No identity closure, calibrated probability or medieval-side assignment is introduced. Version1.18.0 retains168 entries/117 pairs,958 entities,640 claims and167 regions.208 working source files; conservative transfer plan1,675,854,139bytes including the existing1GB reserve. Exact lifetime traffic remains unverified. See [E54](RESEARCH_CONTINUATION_54.md). Older dated sections below describe historical snapshots.

Design written 25 October 2026 before implementing the MVP. This is a provenance-preserving research overlay. It does not replace institutional records or the frozen ten-case review.

## Competency questions

1. Which source says that two items share a codex, and does it assert, suggest or reject that relation?
2. Which items merely belong to a broad stylistic/liturgical group, rather than one reconstructed book?
3. Can the Codex 1505/IV.157 suggestion coexist with BOMPAC's separate assignments without merging their objects?
4. What exact pixels support a reading, at which resolution, and from which institutional photograph?
5. Are two records two objects, two sides, or duplicate descriptions of one physical object?
6. Which aliases are catalogue unit labels shared by several fragments, and which are actual object identifiers?
7. What supports or challenges each claim, who made it, and what remains missing?
8. Why does 8201–8304 remain a rejected same-book control despite catalogue co-assignment and high similarity?
9. Which suggestions have had only a metadata/availability screen, and which received a direct source test?
10. What observation would change an unresolved lead, and can the next test be run locally now?
11. Which current proposals derive from the same source and therefore do not provide independent corroboration?
12. Is a methodological correction a separate lead from a medieval attribution?

## Small data model

| Entity | Meaning and boundary |
|---|---|
| Codex | A proposed once-intact book, kept distinct from its catalogue label and surviving pieces. Competing reconstructions remain separate entities. |
| Chant | A textual/musical work, distinct from the physical manuscripts transmitting it. Identifying a surviving ending does not identify a whole office or book. |
| PhysicalFragment / FragmentSet | An archival object, potentially containing more than one leaf, or an explicitly described aggregate. A photograph is never counted as a fragment. |
| Leaf / Side | A leaf and one of its surfaces. Create only source-described or directly supported examples; ordinal capture numbers do not create recto/verso assignments. |
| CatalogRecord / Identifier | A source record and its scoped identifiers. Ant 99 is a reconstruction-unit label covering several objects; it is not an alias making those objects identical. |
| Capture / ImageDerivative | An institutional photograph/canvas and a retained file at a particular resolution. Multiple resolutions share a capture. Identical bytes alone do not merge physical objects. |
| Source / Agent | The publication, dataset, record or local file and the person, institution or software responsible for a statement. Unknown authors/dates stay null. |
| EvidenceRegion | An observation linked to a file, SHA-256, dimensions and pixel selector. Its literal reading is separate from expansion and interpretation. |
| Claim | Subject, relationship, object, polarity, source stance, project status, attributed agent, date, scope, provenance, support, challenge and limits. |
| MissingInformation | A missing image, unread passage, unverified side map or absent adjudication. This creates no negative historical claim. |

Relationships include `same_codex`, `physical_join`, `textual_continuation`, `same_hand`, `stylistic_similarity`, `liturgical_relationship`, `suggested_association`, `assigned_to_reconstruction`, `member_of_group`, `part_of`, `describes`, `capture_of`, `derivative_of`, and `method_correction`. An assignment or a suggested association never automatically becomes a same-codex fact. No transitive identity closure is performed.

Claim basis is one of `source_assertion`, `project_observation`, `computational_suggestion`, or `researcher_interpretation`. Source stance (`asserted`, `suggested`, `rejected`, `unknown`) is separate from project decision state (`supported`, `contradicted`, `unresolved`, `previously_documented`, `not_testable`). A published rejection can therefore be represented as a documented negative same-codex claim, alongside the positive catalogue co-assignment. No compatibility score is stored as confidence.

## Populated examples required of the MVP

| Example | Representation |
|---|---|
| Codex 1505 versus IV.157 | A qualified source `suggested_association`, a separate project same-codex question, and BOMPAC reconstruction assignments. No entity merge. |
| IV.157 and Ant 99 | A source-attributed, previously documented same-codex claim; individual Fr 20274–20278 objects remain distinct. |
| IV.173 and Ant 242/Fr 29666 | A specific documented same-codex claim distinct from the broad Naantali stylistic group's membership claims. Hy 49/Fr 25592 and Ant 99 suggestions remain qualified. |
| Fr 8994 opening signs | Source-linked `IIII` and `k` observations and a separately conditional interpretation comparing the third-nocturn text with the Finnish catalogue's first-nocturn description. No unconditional exclusion. |
| Fr 8201–8304 | Positive MPO Codex 1146 co-assignments, a published same-hand assertion, a published negative same-codex assertion, and the retained computational suggestion. |

## Identifier, provenance and uncertainty rules

Only the existing explicit `physical_object_id` mapping merges local record representations. Bare catalogue numbers, same reconstructed-book labels and similar images do not. `finn-iv173` and `finn-iv173-verso` refer to one physical object; they retain distinct record/capture provenance. Turku Ms. c stays an unresolved scoped identifier rather than being silently equated with another holder's manuscript.

The JSON MVP stores entities, claims, evidence, dependencies and a separate lead register. Each imported statement points to its source file and JSON selector or publication URL; input checksums make the extraction reproducible. Imported historical dates remain source dates where known, and the extraction date is recorded separately. Evidence regions retain their original coordinates and source-image hashes. Current source records and the ten frozen reviews remain unchanged by knowledge extraction.

Lead coverage must account for every ranking row, frozen hypothesis, dossier, named feasibility family, explicit cross-collection source link and required auxiliary lead. Reciprocal rankings resolve to one physical-pair lead while retaining every original rank and score as retrieval provenance. Metadata triage is labelled as such; it is not called a full manuscript test. An internal transcription task is not disguised as an external access dependency.

The standard-library validator checks IDs, types, relationship targets, claim provenance, evidence and dependency links, image regions/hashes, source snapshots, full pair coverage and frozen-input preservation. JSON-LD export keeps claims reified; it does not emit `owl:sameAs` or flatten uncertain assertions into facts. Semantic-web vocabulary mappings can be refined later without changing the source overlay.

## Working MVP and commands

The current version 1.17.0 overlay has 168 lead/question entries (117 pair leads), 943 entities, 638 claims and 155 evidence regions. Every stored ranking row is covered; 8 pair leads have source-assignment review only and explicitly pending primary pair tests. E44 registers nine source photographs on existing physical objects and canvases, preserves unknown medieval sides, and records an unresolved text/ruling comparison; five-rule compatibility and a hymn cue create no book identity or confirmed catalogue correction. E43 credits43 previously uncredited Beauvais pairings through exact image services in the parent reconstruction manifest; this is a source-membership audit, not new pair-level image validation. E45 adds eight service/text regions and provenance to the same unresolved interpretation, without a new claim or lead. It preserves partial corresponding passages, uncertain word order and a paper-specific scope clarification; service labels do not become codex identity. E46 adds two external Chant concepts (005415/007763zd), separate unresolved local identification claims, and one scoped head-group observation. Related words and differing notation do not establish a same-work melodic variant or book exclusion. E47 credits13 Aboense pairings through exact included BOMPAC-4795 workbook rows and adds seven source-assignment claims. The related raw C-1481 unit is not independent corroboration, and the31 mixed-grain source records do not generate new physical leaves or captures. E48 audits all36 remaining source-only comparisons, credits five published BOMPAC-5324 pairings, and preserves an unresolved BOMPAC-4861 co-assignment beside the published8201/8304 rejection. Its31 remaining primary pair tests carry an explicit pending flag; shared/different unit labels do not resolve them. E49 adds four image regions and a partial-primary-recheck payload to that interpretation. It preserves the missing20106 premise and an A103 CatalogRecord with `physical_object: null` and unresolved crosswalk, rather than creating a physical identity from shelfmark agreement. E50 adds eight source regions and a supported negative `stylistic_similarity` observation scoped to visible copying-field layout. Exactly one primary-test flag changes after an initial direct source comparison; this counts first primary review, not full photo coverage or completed historical adjudication. The missing view and same-codex decision remain unresolved. Six added image files link to existing objects/canvases, with no new physical object or medieval-side assignment. E51 adds four regions and a supported description of a later20274 library reference; its completed six-view margin audit recovers no secure comparable original address. Four prior mark regions are reused, not independent new evidence. Current v1.1 release provenance shows identical workbook distribution without creating new codices, CSV validation or novelty. Exactly one additional first-comparison flag clears, with all historical decisions unchanged. E52 adds seven regions, three candidate work identifications and two scoped observations for8072/8073. All13 pending Ant49 edges receive limited group-context comparisons; generic layout fails the known wrong-pair control, and no historical decision changes. Full-photo scope remains incomplete. Three external Chant concepts and local candidates remain distinct from book identity. E53 adds nine regions and two unresolved local hymn-identification claims, with known external Chant concepts kept separate from physical book identity. Eight selected-view context comparisons leave all historical decisions unchanged and preserve coverage/section/composite limits. Source assertions, repeated topic views and computational proposals are not independent scientific evidence. The historical review retains its 63 annotations and ten cases; E33/E34/E36/E37/E38/E39/E40/E42/E44/E45/E46/E49/E50/E51/E52/E53 regions are separate. E35 adds a `photographic_overlap` relationship between image derivatives, distinct from physical joining or codex identity. Both failed boundary screens remain unresolved, including the narrow folded-strip clue. E41 adds manual context-audit provenance and scoped summaries to these existing imaging claims; its 63 descriptor pairs are not new independent leads or source regions. E36 preserves two exact phrase controls and one weaker generic boundary without converting prior continuities into discoveries.

```sh
.venv/bin/python research/continuation_33/check_sources.py
.venv/bin/python research/continuation_34/check_sources.py
.venv/bin/python -m lost_library knowledge build
.venv/bin/python -m lost_library knowledge validate
.venv/bin/python -m lost_library knowledge export
```

Build writes `data/knowledge.v1.json`, `data/lead_register.v1.json` and `LEAD_REGISTER.md`; export writes `data/knowledge.v1.jsonld`. The published JSON Schema documents shapes/vocabulary; the shipped validator additionally checks referential integrity, input freshness, coverage and image regions. Serve the project locally and open `viewer/knowledge.html` to filter leads, inspect regions and compare attributed claims. The JSON-LD MVP reifies claims and preserves complete payloads in details; it makes no full CIDOC-CRM/TEI interoperability claim.

Input hashes deliberately become stale when source reports change: rebuild the overlay, then validate/export again. These commands do not rerank, retrain, reacquire or modify the frozen experiment. Manual readings remain fallible and are not independently confirmed by successful validation.

E37 adds `Chant` as a textual/musical work entity, distinct from any physical manuscript. Its selected Fr 20274 ending claim has explicit `claim_extent=surviving_ending` and `whole_office_recension_established=false`. The older C23 71v evidence and missing replacement 69r remain distinct. Urberg’s published replacement account is a separate attributed claim. A source-specific C435 image dependency is not a global project block.

E38 resolves the specific replacement-69r image dependency after a labelled public-viewer acquisition. The historical dependency remains with `state=resolved`, while current leads cease listing it as missing. The new claim supports only selected text identification; `melodic_identity_established=false` prevents a lexical match from silently becoming a musical result.

E39 adds `melodic_excerpt_comparison` to preserve a partial musical reading as a separate relationship. Twelve provisional relative staff-position concordances coexist with two unresolved events; the claim remains unresolved, with `absolute_pitch_verified=false` and `melodic_identity_established=false`. Overlapping alternatives are never counted as verified matches. The retained readings distinguish an editorially assisted C23 event and corrected image anchors from independent confirmation.

E40 represents the source-described IV.156 folio9 as a leaf with an unverified image/signature mapping. Its proposed textual continuation remains unresolved, with explicit false fields for physical adjacency, physical join, complete edge and signature succession. The numeral V is retained as a conditional prediction, never substituted for the unclear source reading.

E42 keeps two local `textual_continuation` claims between the retained image derivatives. The N[o?]+uo split remains unresolved; the adversus+xpistum eius phrase fit is supported only in its local reading scope. Both deny verified physical adjacency, physical joining, complete surface mapping, accepted photographed overlap, new attribution and novelty. All four proposed/wrong groupings have the same11-row total. The count and common reference wording cannot turn either claim into codex identity.

E43 adds a source-defined Beauvais codex concept and twelve `assigned_to_reconstruction` source assertions, retaining exact matched parent-canvas locators. Its43 repaired lead statuses say previously documented, but the corresponding machine suggestions remain unresolved computational claims. No title matching or transitive identity closure supplies physical membership. Shared MPO labels, including the disputed Codex1146 group, are not automatically promoted. The preserved before-register and whole-population audit distinguish source credit from primary-image execution coverage.
