"""Integrate the E27 prior-art crosswalk without changing the frozen queue."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "data/context_checks.v7.json"
DEST = ROOT / "data/context_checks.v8.json"
REVIEWS = ROOT / "data/hypothesis_reviews.v1.json"
QUEUE_SHA256 = "b3e299a7c600584ce44518db1f5c30c3301edae0a07a8b009075498f64ccec47"


def append_unique(items: list[str], value: str) -> None:
    if value not in items:
        items.append(value)


def main() -> None:
    checks_doc = json.loads(SOURCE.read_text(encoding="utf-8"))
    check = {
        "id": "CTX09",
        "title": "IV.173 related-group reconstruction crosswalk",
        "record_ids": ["finn-iv173", "mpo-29666", "mpo-25592", "mpo-20274", "mpo-8994", "mpo-1385"],
        "observation_ids": [],
        "summary": (
            "The updated National Library record for F.m.IV.173 identifies Ant 242/Fr 29666 as "
            "same codex, lists Hy 49/Fr 25592 and Ant 99 as suggestions, and describes a broader "
            "style/liturgical group. The deposited BOMPAC workbook assigns IV.173, Fr 29666 and "
            "Fr 25592 to BOMPAC-9531 (3 included rows); Ant 99/IV.157/Fr 1385 belong to BOMPAC-912, "
            "and Codex 1505/IV.156 to BOMPAC-5324. The raw Fr 29666 note also cites Taitto 2001 p.185 "
            "for the Ant 242–Ant 173 same-codex claim."
        ),
        "outcome": (
            "The published sources distinguish a broad stylistic group, suggested links and explicit "
            "same-codex assertions. BOMPAC's IV.173 unit agrees with the Ant 242 link and includes Hy 49, "
            "but separates it from Ant 99/IV.157. This is a source-level difference in group membership, "
            "not an independent image adjudication or a new attribution. H03, H04 and H05 remain unresolved."
        ),
        "limits": [
            "The official Fragmenta record says Ant 99 is suggested in connection with Keskiaho 2010; it does not label Ant 99 as a proven same-codex member of IV.173.",
            "The BOMPAC workbook records project reconstruction units, not a fresh image examination; its grouping does not prove that a more complex shared hand, workshop, production group or composite history is impossible.",
            "Fr 25592's two-column hymn layout and IV.173's one-column music layout are visible in existing images, but layout differences alone do not disprove a book with sections made for different functions.",
            "Fr 29666 has no verified local image. The ordinary Riksarkivet catalogue page displayed a human-verification challenge; no challenge was interacted with or bypassed, and no image was acquired.",
            "No independent specialist judgment, new manuscript-side mapping, physical join or unique text/music variant is established by this crosswalk.",
        ],
        "sources": [
            "RESEARCH_CONTINUATION_27.md",
            "research/continuation_27/related_unit_crosswalk.py",
            "research/continuation_27/related_unit_crosswalk_results.json",
            "https://fragmenta.kansalliskirjasto.fi/handle/10024/1314",
            "https://fragmenta.kansalliskirjasto.fi/handle/10024/1300",
            "https://doi.org/10.5281/zenodo.17511106",
            "https://doi.org/10.5281/zenodo.17701360",
        ],
    }
    checks = checks_doc["checks"]
    checks[:] = [item for item in checks if item.get("id") != "CTX09"]
    checks.append(check)
    checks_doc["version"] = "1.2.0"
    checks_doc["assessment_date"] = "2026-10-24"
    checks_doc["scope"] = "Supporting source, layout-control and prior-art checks; no additional frozen attribution hypotheses."
    DEST.write_text(json.dumps(checks_doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    review_doc = json.loads(REVIEWS.read_text(encoding="utf-8"))
    if review_doc.get("queue_sha256") != QUEUE_SHA256:
        raise ValueError("Frozen hypothesis queue hash changed; stop before integration")
    review_doc["context_checks_path"] = "data/context_checks.v8.json"
    review_doc["version"] = "1.9.0"
    review_doc["assessment_date"] = "2026-10-24"

    h03 = next(item for item in review_doc["reviews"] if item["id"] == "H03")
    h03["prior_status"] = (
        "Previously suggested Ant99/Codex1505 comparison; E26 finds BOMPAC assigns them to separate "
        "units, and E27 records a separate IV.173 unit alongside the official catalogue's broader "
        "suggested-group wording."
    )
    h03_support = (
        "The updated official F.m.IV.173 record lists Ant 99 as a suggested relationship within a broader "
        "stylistic/liturgical group; it does not call Ant 99 a proven same-codex member. This is published "
        "prior art for a possible wider production relationship, not direct identity evidence."
    )
    h03_against = (
        "E27's checksum-verified BOMPAC query puts F.m.IV.173, Ant 242/Fr 29666 and Hy 49/Fr 25592 in "
        "BOMPAC-9531, while Ant 99/IV.157 remain in BOMPAC-912. The different reconstruction units "
        "clarify the published disagreement but are not fresh image proof."
    )
    append_unique(h03["supporting"], h03_support)
    append_unique(h03["against"], h03_against)
    h03["sources"] = list(h03.get("sources", []))
    for source in ["RESEARCH_CONTINUATION_27.md", "research/continuation_27/related_unit_crosswalk_results.json"]:
        append_unique(h03["sources"], source)

    h04 = next(item for item in review_doc["reviews"] if item["id"] == "H04")
    h04["prior_status"] = (
        "Previously suggested IV.173/family association; E27 maps IV.173, Fr 29666 and Fr 25592 to "
        "BOMPAC-9531, separate from Fr 1385/IV.157 in BOMPAC-912."
    )
    append_unique(h04["supporting"], (
        "E27 verifies that BOMPAC-9531 contains F.m.IV.173, Ant 242/Fr 29666 and Hy 49/Fr 25592. "
        "The official IV.173 record explicitly identifies Ant 242/Fr 29666 as same codex."
    ))
    append_unique(h04["against"], (
        "BOMPAC places Fr 1385 with IV.157 in unit 912, separate from IV.173 in unit 9531; this is "
        "a published reconstruction distinction, not proof against a shared production group or hand."
    ))
    h04["outcome"] = (
        "Not promoted: the published sources distinguish the IV.173/Ant 242/Hy 49 reconstruction from "
        "the IV.157/Fr 1385 reconstruction, but no new direct evidence resolves their broader family relation."
    )
    h04["next_evidence_needed"] = (
        "Compare IV.173 directly with the accepted Ant 242/Fr 29666 image when a normal authorized source "
        "route is available; separately test the Fr 1385–IV.157 link with page order, text and physical "
        "evidence. Do not infer that separate BOMPAC units exclude common production or a shared hand."
    )
    h04["sources"] = list(h04.get("sources", []))
    for source in ["RESEARCH_CONTINUATION_27.md", "research/continuation_27/related_unit_crosswalk_results.json"]:
        append_unique(h04["sources"], source)

    h05 = next(item for item in review_doc["reviews"] if item["id"] == "H05")
    h05["prior_status"] = (
        "Previously suggested IV.173/Hy 49 association; E27 finds BOMPAC groups Fr 25592/Hy 49 with "
        "IV.173 and Ant 242/Fr 29666 in BOMPAC-9531."
    )
    append_unique(h05["supporting"], (
        "E27 verifies BOMPAC-9531 contains all three rows: Fr 25592/Hy 49, Fr 29666/Ant 242 and "
        "F.m.IV.173, fol. 1. The Fr 29666 note cites Taitto 2001 p.185 for its same-codex link to IV.173."
    ))
    append_unique(h05["against"], (
        "The actual captures still show a one-column music layout for IV.173 and a much denser two-column "
        "hymn layout for Fr 25592, and the catalogue dating for Fr 25592 conflicts with the proposed "
        "fifteenth-century group. BOMPAC's unit is a research reconstruction, not direct proof that these "
        "differences are compatible within one codex."
    ))
    h05["outcome"] = (
        "Still C / unresolved. BOMPAC now supplies a published grouping that supports the suggested "
        "IV.173–Hy 49 link, while the visible layout and dating differences remain untested explanations; "
        "neither side alone settles the identity."
    )
    h05["next_evidence_needed"] = (
        "Compare corresponding texts, openings/signatures and physical structure in IV.173 and Fr 25592; "
        "use the accepted Fr 29666/Ant 242 comparator if an authorized image becomes available; investigate "
        "the dating conflict without assuming a composite book or catalogue error."
    )
    h05["sources"] = list(h05.get("sources", []))
    for source in ["RESEARCH_CONTINUATION_27.md", "research/continuation_27/related_unit_crosswalk_results.json"]:
        append_unique(h05["sources"], source)

    REVIEWS.write_text(json.dumps(review_doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "context_checks": len(checks_doc["checks"]),
        "updated_context": "CTX09",
        "context_path": "data/context_checks.v8.json",
        "queue_sha256": review_doc["queue_sha256"],
        "updated_reviews": ["H03", "H04", "H05"],
    }, indent=2))


if __name__ == "__main__":
    main()
