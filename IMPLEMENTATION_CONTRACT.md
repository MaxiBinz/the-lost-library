# Lost Library implementation contract

## Current assessment — E55,31October2026

Knowledge1.19.0 has959 entities,641 claims and167 regions across168 entries/117 pairs. Lead states and frozen2E/7C/1D are unchanged.208 source files and the conservative1,675,854,139-byte plan are unchanged. E55 adds no image regions or physical objects. It retains historical E39 source anchors, failed model outcomes and exact input hashes; one scoped calibration observation is distinct from the unresolved musical interpretation. All historical lead states remain unchanged. [E55](RESEARCH_CONTINUATION_55.md). Earlier dated sections describe historical snapshots.

## Current assessment — E54,31October2026

Knowledge1.18.0 includes12 E54 regions, eight existing-object source variants and two scoped observation claims. Frozen core records/reviews/features/scores remain byte-identical. The eight initial-pending flags are cleared only for recorded limited source comparisons; no historical decision state changes. Version1.18.0 retains168 entries/117 pairs,958 entities,640 claims and167 regions.208 working source files; conservative transfer plan1,675,854,139bytes including the existing1GB reserve. Exact lifetime traffic remains unverified. See [E54](RESEARCH_CONTINUATION_54.md). Older dated sections below describe historical snapshots.

New implementation goal authorized on 20 October 2026 by attachment `5895cdf6-3f2f-4f65-b339-1d38f7dcb5d7/goal-objective.md`. This supersedes the earlier stop-before-implementation instruction. Local implementation and bounded experiments are authorized; public deployment, external contact, paid compute, >300 source images or >3 GB downloads are not.

## Shared paths and interfaces

- Python package: `lost_library/`; root owns `__main__.py`, CLI/integration, reconstruction/export and final documentation.
- Data agent owns `lost_library/pipeline.py`, `data/sample_plan.json`, data ingestion/download/database tests.
- Matching agent owns `lost_library/matching.py`, `lost_library/vision.py`, benchmark/evaluation tests and corresponding generated results.
- Viewer agent owns `viewer/index.html`, `viewer/app.js`, `viewer/style.css`, viewer-specific tests/docs.
- Runtime: project `.venv/bin/python`, created from bundled Python3.12 with system-site packages (NumPy/Pillow already available). Root handles dependency installation.
- Raw historical research files remain in `research/`. New data/images/analysis live in `data/`. Do not overwrite Phase0 results.

## Fragment JSON contract

`data/fragments.json` is a JSON **list**. Every record has:

```json
{
  "id": "mpo-7957",
  "shelfmark": "Riksarkivet Fr 7957",
  "institution": "Swedish National Archives",
  "collection": "MPO",
  "source_url": "https://sok.riksarkivet.se/bildvisning/R1007957",
  "manifest_url": "https://lbiiif.riksarkivet.se/arkis!R1007957/manifest",
  "rights_url": "http://creativecommons.org/publicdomain/mark/1.0/",
  "attribution": "National Archives of Sweden",
  "image_path": "data/images/mpo-7957.jpg",
  "image": {"url":"...", "sha256":"...", "width":800, "height":1143, "canvas_id":"..."},
  "raw": {"signatur":"7957", "codex":"Codex 1104"},
  "normalized": {"type":"Graduale", "date_min":1400, "date_max":1499, "leaf_cm":[33,23], "written_cm":[22.5,15.5], "columns":1, "lines":10, "script":"Textualis", "notation":"Quadr", "staff_lines":4, "contents":"...", "origin":"..."},
  "role": "target|benchmark|distractor|control",
  "warnings": []
}
```

Missing values are null. Raw fields and uncertainty markers are retained. `image_path` is project-relative. Missing-image records may remain searchable with null image_path, but must not count as processed images or benchmark queries. One representative capture per physical record for the main benchmark; alternate sides must not leak across query/gallery. No relationship labels enter visual/descriptive feature extraction.

## Matching and evaluation

`python -m lost_library` will dispatch ingestion, features, evaluate, match, reconstruct/export, search, serve and reproduce commands. Agents expose plain functions callable by root CLI and may provide their own temporary runners for real execution.

Matching outputs `data/matches.json` as a list of records with left_id/right_id, score, per-signal scores, evidence/cautions and rank. A score is compatibility, not probability. Benchmark inputs and group/source labels are recorded separately from feature inputs. Known catalogue groups must be labelled **catalogue-derived**, with exclusions for the published Ant49 false grouping. Report literature-backed controls separately. Keep whole books disjoint for method selection versus test. Compare metadata, layout, pretrained embeddings, and fusion on identical galleries. Unknown pairs are not automatic negatives.

Root will install a real pretrained ResNet18 encoder for frozen features (44.7MB official weights), with no training. It is an ImageNet general-image model and carries a domain-transfer limitation. Its added value must be measured, and a simpler method retained if it performs better. Use deterministic CPU inference and record model/package/weights hashes.

## Viewer contract

Viewer fetches `../data/site.json` while served at `/viewer/`. Root writes that assembled file from generated artifacts. Top-level keys: `project`, `stats`, `fragments` (above schema), `matches`, `reconstruction`, `validation`, `dossiers`, `sources`, `limitations`. Viewer must tolerate missing optional keys and show honest empty/loading/error states. Use actual local images via `../` + image_path. No remote fonts/assets required for core behavior. Local-only static serving; no hosting registration or deployment.

Reconstruction will be a **documented Graduale Aboense subset demonstration** if no new grouping survives validation, while the IV.157 family remains a comparison research target. Do not invent global leaf order: show separate established continuity components, original recto/verso within a record where known, and explicit lacuna/unknown-position placeholders. Musical audio only if a reliable transcription is supported; otherwise explain why it is unavailable.

## Manuscript-knowledge overlay — amendment of 25 October 2026

`lost_library/knowledge.py` and `python -m lost_library knowledge build|validate|export` create a separate versioned knowledge/lead overlay. They preserve the existing records and frozen hypothesis/review/ranking/feature/validation files. `data/knowledge.schema.v1.json` documents the vocabulary; the validator checks coverage, references, source hashes and image regions. `viewer/knowledge.html` inspects the overlay independently of the historical review. Existing object identifiers, explicit physical identity mappings and image coordinate systems remain authoritative for linking; no automatic codex identity closure or model-confidence promotion is permitted.
