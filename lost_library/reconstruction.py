"""Source-backed partial reconstruction and an explicitly uncertain evidence layer."""
from __future__ import annotations

import json
from pathlib import Path

MPO_SOURCE = "https://zenodo.org/records/17287665"
FINN_SOURCE = "https://fragmenta.kansalliskirjasto.fi/handle/10024/1300?show=full"
GRAD_SOURCE = "https://fragmenta.kansalliskirjasto.fi/handle/10024/1610?show=full"
PUBLISHED_NEGATIVE = "https://doi.org/10.25167/ls.4818"
TARGET_IDS = {"mpo-1385", "mpo-20274", "mpo-8994", "mpo-10370", "mpo-10406", "mpo-10407", "mpo-10437", "mpo-25592", "finn-iv173"}
KNOWN_IV157 = {"mpo-1385", "mpo-20274", "mpo-20275", "mpo-20276", "mpo-20277", "mpo-20278"}
SUGGESTED_1505 = {"mpo-8994", "mpo-10370", "mpo-10406", "mpo-10407", "mpo-10437"}
GRAD_IDS = {"mpo-7957", "mpo-7960", "mpo-7961", "mpo-8343", "mpo-8344", "mpo-9242", "mpo-28175"}


def _load(path: Path, default):
    return json.loads(path.read_text()) if path.exists() else default


def _write(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def reconstruct(root: Path) -> dict:
    """Retain catalogue continuities with separately attributed source passages."""
    root = Path(root)
    fragments = _load(root / "data/fragments.json", [])
    available = {r["id"] for r in fragments if r.get("image_path")}
    def item(identifier, label, note):
        return {"fragment_id": identifier, "label": label, "status": "documented",
                "representative_image": True,
                "note": note + " The displayed image is a representative source capture; its ordinal is not an independently verified folio-side mapping.",
                "image_available": identifier in available, "source_url": MPO_SOURCE}
    gap = {"missing": True, "status": "unknown", "label": "Unknown original position / extent",
           "note": "Other leaves and their number are not reconstructed. This placeholder does not assert that exactly one leaf is missing."}
    reconstruction = {
        "title": "Graduale Aboense: a documented surviving subset",
        "status": "Previously documented reconstruction demonstration",
        "description": "An Åbo-use gradual dated 1397–1406. These are separate source-backed continuity components, not a newly discovered codex or an inferred global page order.",
        "historical_origin": "Åbo/Turku liturgical use; production attribution and date derive from the Finnish catalogue and prior scholarship.",
        "dimensions": "Surviving Swedish catalogue dimensions around 33 × 23 cm, sometimes trimmed; original untrimmed size is not inferred.",
        "liturgical_function": "Gradual: chants for the Mass, including the temporal cycle and saints' feasts.",
        "credits": "National Library of Finland; National Archives of Sweden; Toivo Haapanen; Ilkka Taitto's published Graduale Aboense (2002).",
        "sources": [GRAD_SOURCE, MPO_SOURCE, "https://kirjat.finlit.fi/EN/page/product/graduale-aboense-1397-1406/21983?category=4949"],
        "components": [
            {"title": "Continuity I · Pre-Lent", "status": "documented", "description": "The catalogue explicitly continues Fr 7960 leaf 2v into Fr 7961 leaf 1r. The two physical fragments each contain multiple leaves; this does not order their complete contents.", "items": [gap,
             item("mpo-7960", "Fr 7960 · catalogue leaf 2v", "Source position: pre-Lenten material at the end of this catalogue leaf."),
             item("mpo-7961", "Fr 7961 · catalogue leaf 1r", "Source position: continuation of the same pre-Lenten section."), gap]},
            {"title": "Continuity II · After Easter", "status": "documented", "description": "Fr 8343 leaf 1v continues in Fr 8344 leaf 1r, according to the catalogue. Fr 8344 is described as an inner bifolium.", "items": [gap,
             item("mpo-8343", "Fr 8343 · catalogue leaf 1v", "Second Sunday after Easter: the catalogue states that the text continues in Fr 8344."),
             item("mpo-8344", "Fr 8344 · catalogue leaf 1r", "Continuation from Fr 8343; the source contains the intervening post-Easter material."), gap]},
            {"title": "Continuity III · Returning to the outer leaf", "status": "documented", "description": "The catalogue also continues Fr 8344 leaf 2v into Fr 8343 leaf 2r. This interleaving is why fragments must not be displayed as a simple whole-record linear book.", "items": [gap,
             item("mpo-8344", "Fr 8344 · catalogue leaf 2v", "Fifth Sunday after Easter: source-backed continuation to Fr 8343."),
             item("mpo-8343", "Fr 8343 · catalogue leaf 2r", "Continuation from Fr 8344, followed by Rogation material."), gap]},
            {"title": "Other surviving witnesses · position unplaced", "status": "unknown", "description": "These belong to the published book grouping, but no physical adjacency to the components above is asserted here.", "items": [
             item("mpo-7957", "Fr 7957 · Advent", "Catalogue contents: Advent temporal cycle."), gap,
             item("mpo-9242", "Fr 9242 · Christmas / Epiphany", "Catalogue contents: Christmas season, Circumcision and Epiphany."), gap]}
        ],
        "music": {"status": "Audio withheld: no verified note-level transcription", "available": False,
                  "explanation": "Square notation and chant texts are visible, but cropped/folded captures and uncertain page-side mapping do not supply an expert-checked melodic transcription. No notes, recordings or missing pages have been invented. Catalogue chant/feast identifications remain available in each fragment record."},
        "limits": ["This is a documented subset demonstration, not a novel reconstruction.",
                   "Local continuities do not establish global foliation or a complete quire structure.",
                   "First captures may show only part of a folded fragment; source page positions are distinguished from image ordinals.",
                   "The Finnish collection's other leaves and Fr 28175 have not all been acquired."]
    }
    # E36 locates visible passages. This selects the photograph to inspect,
    # without promoting a catalogue side label to independently verified fact.
    passage_path = "research/continuation_36/results.json"
    passages = _load(root / passage_path, {}).get("edges", [])
    if (root / passage_path).exists() and len(passages) != 3:
        raise ValueError("E36 must retain all three source-image continuity reviews")
    record_index = {r["id"]: r for r in fragments}
    for component, edge in zip(reconstruction["components"][:3], passages):
        component["source_image_review"] = edge["local_observation_state"]
        component["link_label"] = ("catalogued continuation; exact text support" if edge["local_observation_state"] == "supported"
                                   else "catalogued continuation; generic boundary only")
        component["source_url"] = "../" + passage_path
        component["source_label"] = "E36 source-image review and limits"
        for position, side in [(1,"from"),(2,"to")]:
            target = component["items"][position]
            if target["fragment_id"] != edge[side]:
                raise ValueError("E36 passage does not match reconstruction component")
            path = edge[side + "_capture"]
            captures = record_index.get(target["fragment_id"], {}).get("captures", [])
            capture = next((c for c in captures if c.get("path") == path), None)
            if capture is None:
                raise ValueError("E36 passage image is not a registered capture")
            target.update(image_path=path, image_sha256=capture["sha256"], representative_image=False,
                          passage_evidence=edge[side + "_regions"], source_image_review=passage_path,
                          mapping_status="provisional_content_based",
                          note="E36 selects this capture for its visible boundary passage. " + edge["result"] +
                               " The named catalogue side is mapped provisionally from contents; this is an AI reading without independent confirmation.")
    _write(root / "data/reconstruction.json", reconstruction)
    return {"components": len(reconstruction["components"]), "global_order_inferred": False, "path": "data/reconstruction.json"}


def _relation(left: str, right: str) -> tuple[str, str, str, list[str]]:
    pair = {left, right}
    if pair == {"finn-iv173", "mpo-29666"}:
        return "E", "Previously documented", "Catalogue links IV.173 with Ant 242 / Fr 29666; no Swedish image is currently verified", ["https://fragmenta.kansalliskirjasto.fi/handle/10024/1314?show=full", MPO_SOURCE]
    if "finn-iv173" in pair and pair & (KNOWN_IV157 | {"mpo-25592"}):
        return "C", "Previously suggested; not a new hypothesis", "A suggested IV.173 catalogue association; source reconciliation remains necessary", ["https://fragmenta.kansalliskirjasto.fi/handle/10024/1314?show=full", FINN_SOURCE, MPO_SOURCE]
    if pair == {"mpo-8201", "mpo-8304"}:
        return "D", "Previously documented rejection", "A published same-hand, different-book comparison", [PUBLISHED_NEGATIVE]
    if pair <= GRAD_IDS:
        return "E", "Previously documented", "Two members of the published Graduale Aboense grouping", [GRAD_SOURCE, MPO_SOURCE]
    if pair <= KNOWN_IV157:
        return "E", "Previously documented", "Catalogue associates in the IV.157 / Ant 99 group", [FINN_SOURCE, MPO_SOURCE]
    if (left in KNOWN_IV157 and right in SUGGESTED_1505) or (right in KNOWN_IV157 and left in SUGGESTED_1505):
        return "C", "Previously suggested; not a new hypothesis", "A qualified catalogue association needing source and physical review", [FINN_SOURCE, MPO_SOURCE]
    if pair <= SUGGESTED_1505:
        return "E", "Previously catalogued group", "Two members of Swedish MPO Codex 1505; broader Helsinki assignment remains qualified", [MPO_SOURCE, FINN_SOURCE]
    return "C", "Scholarly novelty unverified", "A retrieval suggestion, not a demonstrated same-book relationship", [MPO_SOURCE]


def build_dossiers(root: Path, fragments: list[dict], matches: list[dict]) -> list[dict]:
    index = {r["id"]: r for r in fragments}
    selected = []
    seen = set()
    # Include the documented hard negative even if the selected method ranks it low.
    hard = next((m for m in matches if {m.get("left_id"), m.get("right_id")} == {"mpo-8201", "mpo-8304"}), None)
    if not hard and "mpo-8201" in index and "mpo-8304" in index:
        hard = {"left_id": "mpo-8201", "right_id": "mpo-8304", "score": None, "scores": {}, "rank": None,
                "evidence": ["Published rejection retained independently of retrieval rank."]}
    controls = []
    for a, b in (("mpo-7960", "mpo-7961"), ("mpo-8343", "mpo-8344"), ("finn-iv173", "mpo-29666")):
        control = next((m for m in matches if {m.get("left_id"), m.get("right_id")} == {a, b}), None)
        controls.append(control or {"left_id": a, "right_id": b, "score": None, "scores": {}, "rank": None,
                                    "evidence": ["Catalogue documents this association; retained as a reference case independently of retrieval rank. A missing image is not a validated image match."]})
    candidates = ([hard] if hard else []) + controls + [m for m in matches if m.get("left_id") in TARGET_IDS] + [m for m in matches if m.get("left_id") in GRAD_IDS]
    unknown_count = 0
    for match in candidates:
        left, right = match.get("left_id"), match.get("right_id")
        if left not in index or right not in index or left == right:
            continue
        key = tuple(sorted((left, right)))
        if key in seen:
            continue
        seen.add(key)
        category, originality, title, sources = _relation(left, right)
        # Bound the review queue; retain multiple roles rather than a gallery of easy positives.
        if category == "C" and originality == "Scholarly novelty unverified":
            unknown_count += 1
            if unknown_count > 5:
                continue
        if len(selected) >= 16:
            break
        a, b = index[left], index[right]
        na, nb = a.get("normalized", {}), b.get("normalized", {})
        supporting = []
        for evidence in match.get("evidence") or []:
            if isinstance(evidence, dict):
                name = str(evidence.get("signal", "Recorded signal"))
                if "terms" in evidence:
                    supporting.append(name + ": " + ", ".join(map(str, evidence["terms"])))
                elif isinstance(evidence.get("compatibility"), (int, float)):
                    supporting.append(f"{name}: compatibility {evidence['compatibility']:.3f}; this is not an identity probability.")
                else:
                    supporting.append(name)
            else:
                supporting.append(str(evidence))
        if not supporting:
            supporting.append("Ranked by the recorded computational compatibility method; see separate component scores.")
        supporting += [f"Catalogue type: {na.get('type') or 'missing'} / {nb.get('type') or 'missing'}.",
                       f"Notation: {na.get('notation') or 'missing'} / {nb.get('notation') or 'missing'}."]
        against = list(match.get("cautions") or [])
        against += ["Image similarity can reflect shared script, notation, damage, capture background or workshop rather than one codex.",
                    "Source metadata may inherit reconstructed-group descriptions; it is not independent physical evidence.",
                    "No external specialist has adjudicated this computational suggestion."]
        if not a.get("image_path") or not b.get("image_path"):
            against.append("At least one source object lacks a verified local image; this is a catalogue reference case, not an evaluated visual match.")
        if category == "D":
            against.insert(0, "Grajewski's published analysis distinguishes these books despite the hand; this overrides computational resemblance.")
        if category == "C":
            against.append("Keskiaho's 2018/2019 update remains unread, so a claim of present scholarly novelty is unavailable.")
        dossier = {"id": f"case-{len(selected)+1:02d}", "left_id": left, "right_id": right,
                   "classification": category, "originality": originality, "title": title,
                   "summary": f"{a['shelfmark']} compared with {b['shelfmark']}. Category {category}; compatibility is not identity.",
                   "score": match.get("score"), "scores": match.get("scores", {}), "rank": match.get("rank"),
                   "rank_interval": match.get("rank_interval"),
                   "supporting": supporting, "against": against,
                   "textual_musical_evidence": {"left": na.get("contents"), "right": nb.get("contents"),
                       "interpretation": "Catalogue contents are provided for inspection. Similar feast/chant texts do not prove book identity; no automatic note-level transcription is asserted."},
                   "physical_evidence": {"left_leaf_cm": na.get("leaf_cm"), "right_leaf_cm": nb.get("leaf_cm"),
                       "left_written_cm": na.get("written_cm"), "right_written_cm": nb.get("written_cm")},
                   "alternatives": ["Same liturgical tradition or workshop, different books.", "A previously catalogued relationship or alias.", "Capture/metadata similarity without a historical relationship."],
                   "expert_verification_needed": "Check source identities and later bibliography; compare chants, scribal/notation details, opening signatures and original ruling on all relevant sides.",
                   "sources": list(dict.fromkeys(sources + [a.get("source_url", ""), b.get("source_url", "")])),
                   "discovery_claim": False}
        selected.append(dossier)
    _write(root / "data/dossiers.json", selected)
    return selected


def export_site(root: Path) -> dict:
    root = Path(root)
    fragments = _load(root / "data/fragments.json", [])
    if not fragments:
        raise RuntimeError("No fragments available. Run ingest first.")
    comparison_sources = _load(root / 'data/comparison_sources.v1.json', [])
    from .evidence import index_evidence_records
    index_evidence_records(fragments, comparison_sources)
    matches = _load(root / "data/matches.json", [])
    if isinstance(matches, dict):
        matches = matches.get("matches", matches.get("candidates", []))
    validation = _load(root / "data/validation.json", {})
    if not (root / "data/reconstruction.json").exists():
        reconstruct(root)
    reconstruction = _load(root / "data/reconstruction.json", {})
    dossiers = build_dossiers(root, fragments, matches)
    capture_paths = {r["image_path"] for r in fragments if r.get("image_path")}
    for record in fragments:
        capture_paths.update(c["path"] for c in record.get("captures", []) if c.get("path"))
    site = {"project": {"title": "THE LOST LIBRARY", "subtitle": "An evidence-led investigation into a scattered medieval book",
                        "status": "Local research demonstration · no new discovery claimed", "research_target": "The IV.157-centred Åbo/Nådendal antiphonal family",
                        "reconstruction_target": "A documented Graduale Aboense subset", "date": "21 October 2026"},
            "stats": {"fragments": len({f.get("physical_object_id", f["id"]) for f in fragments if f.get("image_path")}),
                      "total_catalogued_objects": len({f.get("physical_object_id", f["id"]) for f in fragments}),
                      "records": len(fragments), "images": len(capture_paths),
                      "analysis_images": sum(bool(f.get("image_path")) for f in fragments),
                      "imaged_fragments": len({f.get("physical_object_id", f["id"]) for f in fragments if f.get("image_path")}),
                      "candidate_pairs": len(matches), "dossiers": len(dossiers), "new_discoveries": 0},
            "fragments": fragments, "comparison_sources": comparison_sources,
            "matches": matches, "reconstruction": reconstruction,
            "validation": validation, "dossiers": dossiers,
            "sources": [{"title": "Swedish MPO metadata, version 1.0.0 (CC0)", "url": MPO_SOURCE},
                        {"title": "National Library of Finland: IV.157", "url": FINN_SOURCE},
                        {"title": "Graduale Aboense: published grouping", "url": GRAD_SOURCE},
                        {"title": "CODICUM: ongoing Nordic reconstruction research", "url": "https://www.codicum.eu/about"},
                        {"title": "BOMPAC: existing Stockholm–Helsinki corpus", "url": "https://doi.org/10.5281/zenodo.17511106"},
                        {"title": "Grajewski: a published different-book comparison", "url": PUBLISHED_NEGATIVE},
                        {"title": "Beauvais Missal reconstruction", "url": "https://fragmentarium.ms/overview/F-4ihz"}],
            "limitations": ["No new scholarly discovery is claimed; known and previously suggested associations are labelled separately.",
                            "Catalogue-derived benchmark labels have not been independently adjudicated by manuscript specialists.",
                            "The pretrained encoder was trained on general images, not medieval music manuscripts.",
                            "The sample is selected and small; retrieval metrics do not measure the archive-wide probability of discovery.",
                            "The later Keskiaho 2018/2019 chapter remains unread, preventing novelty clearance.",
                            "No verified note-level chant transcription was obtained; no invented musical audio is presented."],
            "story": [{"title": "A book becomes a wrapper", "text": "After the Reformation, parchment leaves from medieval books were reused around administrative accounts. Later archival division placed related material in different Nordic collections. Surviving notes tell both medieval and early modern histories."},
                      {"title": "A convincing wrong answer", "text": "The first metadata check ranked a published different-book pair uniquely first. Matching script, notation and dimensions were insufficient. That failure became a test case rather than a discovery."},
                      {"title": "What the machine can offer", "text": "The pipeline ranks inspectable comparisons using metadata, image layout and a frozen visual encoder. Known associations test retrieval. Uncertain suggestions remain hypotheses requiring textual, codicological and scholarly scrutiny."},
                      {"title": "A reconstruction with limits", "text": "The reading sequence shows only catalogue-supported continuities in an already studied gradual. Separate components, unplaced leaves and unknown gaps remain visible. The result demonstrates a method, not the recovery of an unknown complete book."}]}
    site['evidence_review'] = _load(root / 'data/review_bundle.json', {})
    _write(root / "data/site.json", site)
    return {"fragments": len(fragments), "matches": len(matches), "dossiers": len(dossiers), "path": "data/site.json"}
