"""Version the target-level BOMPAC prior-art finding into the evidence viewer."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "data/context_checks.v6.json"
DEST = ROOT / "data/context_checks.v7.json"
REVIEWS = ROOT / "data/hypothesis_reviews.v1.json"


def main() -> None:
    doc = json.loads(SOURCE.read_text(encoding="utf-8"))
    check = next(item for item in doc["checks"] if item["id"] == "CTX07")
    check["summary"] = (
        "The 2025 BOMPAC combined workbook assigns Fr 8994 and four other Codex 1505 "
        "fragments plus F.m.IV.156 folios 1–22 and 23–24 to BOMPAC-5324 (28 included "
        "rows). It assigns Fr 1385 and Fr 20274–20278 plus F.m.IV.157 folios 1–14 to "
        "BOMPAC-912 (20 rows). Its raw MPO workbook groups the five Codex 1505 fragments "
        "as M-1217, Fr 20274–20278 as C-35/Ant-99, and Fr 1385 as singleton F-1385. "
        "The raw Fr 8994 note calls it very similar to Ant 99 and the Helsinki Ant 156/157, "
        "citing Taitto 2001, pp. 161–168; the Fr 1385 note calls it the same manuscript as Ant 157."
    )
    check["outcome"] = (
        "The target-level published reconstructions are now known: BOMPAC separates "
        "Fr 8994/Codex 1505/F.m.IV.156 from Fr 20274/Ant 99/F.m.IV.157, while its "
        "combined unit 912 includes Fr 1385. Broad cross-collection integration and "
        "these row assignments are prior work, not a new discovery here. H03 remains "
        "category C; the workbook assignments are not fresh image proof and do not "
        "exclude a more complex historical relationship."
    )
    check["limits"] = [
        "BOMPAC describes its combined spreadsheet as research data prepared for the project, not institutional catalogue data; it defines units as reconstructions but cautions that inherited codex signa can overlap and need not cover every fragment thought to come from a codex.",
        "The raw-metadata readme says the underlying research metadata is incomplete and work-in-progress. Blank target-row ambiguity/correction cells are not proof of certainty.",
        "The inherited Fr 8994 note says 'very similar' to the listed groups, while the Fr 1385 note says 'same manuscript' as Ant 157; those are not equivalent claims. Taitto pp. 161–168, cited by Fr 8994, remain unread.",
        "The combined row assignments and raw MPO groups are related data products, not independent image examinations or expert judgments.",
        "A distinct reconstruction ID alone does not prove there can be no shared hand, workshop, textual relation, composite history, or later revision.",
    ]
    check["sources"] = [
        "RESEARCH_CONTINUATION_26.md",
        "research/continuation_26/bompac/target_crosswalk_results.json",
        "research/continuation_26/bompac/target_crosswalk.py",
        "research/continuation_26/bompac/Readme-Sto-Hel-Frs-Combined-BOMPAC.pdf",
        "research/continuation_26/bompac/raw_metadata/Readme-Raw-Metadata-BOMPAC.pdf",
        "research/continuation_26/bompac/raw_metadata/MPO_commentary_Holger_Kaasik.pdf",
        "https://doi.org/10.5281/zenodo.17511106",
        "https://doi.org/10.5281/zenodo.17701360",
        "https://doi.org/10.24446/no5r",
    ]
    doc["version"] = "1.1.0"
    doc["assessment_date"] = "2026-10-24"
    doc["scope"] = "Supporting source, layout-control and prior-art checks; no additional frozen attribution hypotheses."
    DEST.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    review_doc = json.loads(REVIEWS.read_text(encoding="utf-8"))
    review_doc["context_checks_path"] = "data/context_checks.v7.json"
    review_doc["version"] = "1.8.0"
    h03 = next(item for item in review_doc["reviews"] if item["id"] == "H03")
    h03["prior_status"] = (
        "Previously suggested Ant99/Codex1505 comparison; E26 finds that the published "
        "BOMPAC combined dataset assigns them to separate reconstructed units."
    )
    catalogue_note = (
        "The raw MPO note for Fr 8994 describes it as similar to Ant 99 and Helsinki Ant 156/157, "
        "cites Taitto 2001, pp. 161–168, and also points to Fr 1385. This is a prior catalogue "
        "similarity claim; it does not state that Fr 8994 and Fr 20274 are the same codex."
    )
    if catalogue_note not in h03["supporting"]:
        h03["supporting"].append(catalogue_note)
    published_split = (
        "E26's checksum-verified BOMPAC workbook assigns Fr 20274/Ant 99/IV.157 to "
        "BOMPAC-912 and Fr 8994/Codex 1505/IV.156 to BOMPAC-5324. This is a published "
        "separate reconstruction, but it is research metadata rather than a fresh direct "
        "image examination; it does not by itself rule out a more complex relationship."
    )
    if published_split not in h03["against"]:
        h03["against"].append(published_split)
    h03["outcome"] = (
        "H03 remains C / unresolved on the local image evidence. The target-level BOMPAC "
        "split is now an explicit, strong competing published reconstruction; any different "
        "conclusion requires direct source evidence and an explanation of why it revises that split."
    )
    h03["next_evidence_needed"] = (
        "Compare complete corresponding text, foliation/quire structure and diagnostic "
        "physical features against the published BOMPAC split. Keep the recorded 0.5 cm "
        "catalogue size similarity separate from direct image evidence; read the cited "
        "Taitto 2001 pp. 161–168 through a legitimate accessible route; retain uncertainty "
        "about capture geometry and medieval-side conventions."
    )
    h03_sources = [
        "RESEARCH_CONTINUATION_26.md",
        "research/continuation_26/bompac/target_crosswalk_results.json",
        "https://doi.org/10.5281/zenodo.17511106",
        "https://doi.org/10.5281/zenodo.17701360",
    ]
    for source in h03_sources:
        if source not in h03["sources"]:
            h03["sources"].append(source)
    h03["originality"] = (
        "No originality claim cleared; broad cross-collection reconstruction and the "
        "published target-unit split are prior work."
    )
    REVIEWS.write_text(json.dumps(review_doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"context_checks": len(doc["checks"]), "updated": "CTX07",
                      "path": "data/context_checks.v7.json",
                      "queue_sha256": review_doc["queue_sha256"]}, indent=2))


if __name__ == "__main__":
    main()
