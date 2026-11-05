# The Lost Library — local viewer

## Current assessment — E55,31October2026

E55 tests the two E39 upper-note uncertainties against local staff geometry. Both retain3/4 alternatives; four of twelve complete rule fits fail, and two spem anchors also widen under the same sensitivity. No new pitch, melodic variant, book attribution or discovery is established. The same167 exact evidence regions remain. The E55 observation links back to existing E39 regions; no synthetic reading or new source-side assignment is displayed. Knowledge1.19.0 has959 entities,641 claims and167 regions across168 entries/117 pairs. Lead states and frozen2E/7C/1D are unchanged.208 source files and the conservative1,675,854,139-byte plan are unchanged. [E55](../RESEARCH_CONTINUATION_55.md). Earlier dated sections describe historical snapshots.

## Current assessment — E54,31October2026

The knowledge view exposes E54 source captures and12 exact regions with qualified literals, clipped-sign limits and later reuse context. All eight new comparisons remain historically unresolved. Zero first-comparison-pending flags must not be read as complete adjudication or scientific success. Version1.18.0 retains168 entries/117 pairs,958 entities,640 claims and167 regions.208 working source files; conservative transfer plan1,675,854,139bytes including the existing1GB reserve. Exact lifetime traffic remains unverified. See [E54](../RESEARCH_CONTINUATION_54.md). Older dated sections below describe historical snapshots.

Buildless HTML/CSS/JavaScript. Serve the project root and open `/viewer/`; the viewer fetches `../data/site.json`. Core operation uses no external fonts, libraries, analytics, credentials or hosted services. It never downloads additional archive images automatically.

## Supported data

Root-level `site.json` fields: `project`, `stats`, `fragments`, `matches`, `reconstruction`, `validation`, `dossiers`, `sources`, `limitations`. Only `fragments` needs to be a list; absent optional sections have visible empty states.

Fragments follow `IMPLEMENTATION_CONTRACT.md`. Source `raw` metadata is not modified. `image_path` is project-relative; external image URLs are accepted only when explicitly supplied. Detail views show catalogue date/type, contents, dimensions, script/notation, credit, rights, record/manifest/image endpoints and image SHA-256.

### Reconstruction

Preferred shape:

```json
{
  "title": "Graduale Aboense: documented components",
  "description": "Scope and limitations",
  "note": "Separate components have no asserted global relative position.",
  "components": [{
    "title": "A documented textual continuity",
    "classification": "E",
    "description": "What the source establishes",
    "link_label": "documented continuity",
    "source_url": "https://...",
    "items": [
      {"missing": true, "label": "Position unknown", "note": "Extent unestablished"},
      {"fragment_id": "mpo-7960", "side": "leaf 2 verso", "image_path": "data/images/verified-side.jpg", "representative_image": false, "note": "Source-backed side"},
      {"fragment_id": "mpo-7961", "side": "leaf 1 recto", "representative_image": true, "note": "Only a representative capture is currently available"}
    ]
  }],
  "music": {"status": "unavailable", "reason": "No independently checked transcription was established."}
}
```

`groups` and `sequence` are accepted aliases. Individual items may be fragment-ID strings. Separate components are never joined into a fabricated full-book order. An optional item `image_path` overrides the record capture; `representative_image:true` produces an explicit warning in the inspection view. Missing items are visible placeholders, not reconstructed pages.

Audio renders **only** if `music.verified:true` or `music.status:"verified"`, plus an `audio_url`/`url`. Otherwise only the stated unavailability reason is shown. A playback control is never fabricated.

### Matches and dossiers

Matches: `left_id`, `right_id`, `score`, `rank`, `scores` (signal→number), `evidence` and `cautions`. Dossiers enrich a matching pair with `classification` (A–E), `originality`, `title`, `summary`, `supporting`, `against`, `alternatives`, `expert_verification` and `sources:[{url,label}]`. Unknown classification is shown as **not adjudicated**, not an accepted relationship. Unknown originality remains **not assessed**. Compatibility is never displayed as probability. Reciprocal pair rows are deduplicated in this view only; the exported ranked dataset remains unchanged.

### Validation

Preferred: `{selected_method, test_queries, test_codices, description, label_source, limitations:[], methods:[{name, selected, metrics:{precision_at_1, precision_at_5, recall_at_5, hit_at_1, hit_at_5, mrr, queries}}]}`. Metrics are fractions. Missing metrics remain dashes, never zero-filled. An object keyed by method name is also accepted. The root exporter should pass the intended test partition's metrics explicitly rather than letting the UI choose a partition.

### Other fields

`sources` accepts `[{title,url,description}]`; `limitations` is a list of text statements. `project` optionally supplies `description`, `edition`, `hero_fragment_id`, `story` (paragraph list). Stats accept `imaged_fragments`, `images`, `ranked_pairs`/`candidate_pairs`, `sequence_components`; otherwise counts derive from loaded records. The first statistic counts distinct physical objects among image-supported records; the explorer reports record count separately. Labels say records/captures rather than assuming that every photograph is a distinct leaf.

## Interaction and accessibility

Search supports shelfmarks, contents, institution, origin, notation and script with accent-insensitive multiword matching. Filters cover collection/type/research role and image availability. The explorer paginates 24 records at a time. Two selections open a native modal comparison; each capture supports zoom, rotate and reset. When a record has multiple `captures`, a selector switches its source photograph and updates the displayed dimensions, hash, source URL and rights. Capture ordinals never become medieval folio-side labels. Escape closes the modal. All actions are buttons/links with keyboard focus styles. Reduced-motion preference is respected. Responsive navigation/grid and stacked mobile comparison are provided.

## Tests

`node tests/viewer.test.cjs` uses built-in Node assertions for data handling, escaping, filter behavior, missing images, reconstruction grouping and validation normalization. Browser QA should additionally verify actual image loading, navigation, filters, selections, modal zoom/rotation, evidence expansions and mobile layout once generated research data exists.

## Knowledge and complete lead register

Open `knowledge.html` on the same local server. It loads the versioned knowledge and lead JSON, supports text/state filtering, displays the work actually performed and remaining inputs, and overlays the cited regions on unchanged local images. Entity inspection keeps competing source/interpretation claims side by side. The atlas sidebar links this page; its 70 regions include seven E33/E34 overlays in addition to the preserved review's 63. No external upload or hosted dependency is used.

E36 (27 October 2026) selects six registered captures for the three documented Aboense boundaries, rather than displaying each object's first image. The notes preserve provisional side mapping and distinguish two exact phrase continuations from a generic Alleluia boundary. Two unplaced witnesses retain representative images. The knowledge page includes E35's unresolved photographic-overlap question and seven E36 regions; frozen reviews remain unchanged.

## E51 evidence — 30 October 2026

The1.15.0 overlay has923 entities,631 claims and139 regions across168 entries/117 pairs. Four added regions record an uncertain20274 upper sign, its later library reference and10370 reuse/edge features. Four prior mark regions are reused. Only the later-reference description receives a new supported claim; no book identity or folio assignment is created. Current release metadata enriches source provenance.29 source-only pairs still lack an initial direct comparison; no fresh live-browser UI validation is claimed. [E51](../RESEARCH_CONTINUATION_51.md).

## E52 evidence — 30 October 2026

The1.16.0 overlay has939 entities,636 claims and146 regions across168 entries/117 pairs. Six native files link to existing8072/8073 objects/canvases. Seven regions and separate candidate Chant claims preserve actual text/function uncertainty; supported local observations do not become book identities. All13 limited Ant49 edge comparisons are linked, while16 other first comparisons remain pending. Historical decisions/frozen outputs are unchanged; no fresh live-browser UI validation is claimed. [E52](../RESEARCH_CONTINUATION_52.md).

## E53 evidence — 30 October 2026

The1.17.0 overlay has943 entities,638 claims and155 regions across168 entries/117 pairs. Nine added regions link retained source context, with rights/attribution for the CC BY Beauvais images; the new figure uses PDM pixels only. Two hymn concepts have separate unresolved local candidate claims. Eight more selected-view comparisons do not resolve historical membership, and eight first comparisons remain pending. No fresh live-browser UI validation is claimed. [E53](../RESEARCH_CONTINUATION_53.md).
