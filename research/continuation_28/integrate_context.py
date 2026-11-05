"""Integrate the E28 prior-art clarification without changing the frozen queue."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "data/context_checks.v8.json"
DEST = ROOT / "data/context_checks.v9.json"
REVIEWS = ROOT / "data/hypothesis_reviews.v1.json"
QUEUE_SHA256 = "b3e299a7c600584ce44518db1f5c30c3301edae0a07a8b009075498f64ccec47"
REPORT = "RESEARCH_CONTINUATION_28.md"
PORTAL = "https://researchportal.helsinki.fi/en/publications/birgittine-fragments-in-finland-reconstructing-naantali-abbeys-li/"
PDF = "https://www.diva-portal.org/smash/get/diva2%3A668618/FULLTEXT01.pdf"


def append_unique(items: list[str], value: str) -> None:
    if value not in items:
        items.append(value)


def main() -> None:
    checks_doc = json.loads(SOURCE.read_text(encoding="utf-8"))
    checks = checks_doc["checks"]
    check = {
        "id": "CTX10",
        "title": "Walta 2013 prior-art on the broader Naantali fragment group",
        "record_ids": ["finn-iv173", "mpo-29666", "mpo-25592"],
        "observation_ids": [],
        "summary": (
            "The University of Helsinki research portal identifies Ville Walta's 'Birgittine Fragments in Finland: "
            "Reconstructing Naantali Abbey's Library' as a peer-reviewed 2013 chapter (pp. 11–29). The indexed "
            "chapter excerpt for p. 20/footnote 35 describes a broader group of up to 19 manuscripts that includes "
            "F.m.IV.156, IV.157 and IV.173. It notes several hands and says only one or possibly two items are "
            "directly connected to Naantali, leaving the production site uncertain; it cites Keskiaho 2010 for "
            "additional members. Opening the full PDF timed out, so this is an indexed excerpt, not a full-chapter "
            "review."
        ),
        "outcome": (
            "The E27 catalogue/workbook difference should not be described as a proven scholarly contradiction. "
            "The sources may discuss narrower reconstructed same-codex units, suggested joins and a broad "
            "stylistic/production group at different levels. H03–H05 remain unresolved; no new historical finding "
            "or attribution is established."
        ),
        "limits": [
            "The chapter excerpt is search-indexed; the complete PDF did not open and is not retained locally.",
            "Walta's broad group does not imply that all its members came from one codex, one scribe or one production site.",
            "The exact Taitto 2001 pp. 161–168 and Keskiaho 2010 pp. 418–419 passages remain unread.",
            "No new manuscript images, direct physical inspection, side mapping or unique text/music variant were tested.",
            "This contextual prior-art check does not modify the frozen queue, baseline predictors or thresholds.",
        ],
        "sources": [REPORT, PORTAL, PDF],
    }
    checks[:] = [item for item in checks if item.get("id") != "CTX10"]
    checks.append(check)
    checks_doc["version"] = "1.3.0"
    checks_doc["assessment_date"] = "2026-10-24"
    checks_doc["scope"] = "Supporting source, layout-control and prior-art checks; no additional frozen attribution hypotheses."
    DEST.write_text(json.dumps(checks_doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    review_doc = json.loads(REVIEWS.read_text(encoding="utf-8"))
    if review_doc.get("queue_sha256") != QUEUE_SHA256:
        raise ValueError("Frozen hypothesis queue hash changed")
    review_doc["version"] = "1.10.0"
    review_doc["context_checks_path"] = "data/context_checks.v9.json"

    h03 = next(item for item in review_doc["reviews"] if item["id"] == "H03")
    h03["prior_status"] = (
        "E27 records the BOMPAC split between Ant 99/Codex 1505 and the IV.173 unit. E28 locates Walta 2013's "
        "broader group, which includes IV.156, IV.157 and IV.173 at a stylistic/production level; full text still pending."
    )
    append_unique(h03["against"], (
        "Walta 2013's indexed excerpt places IV.156, IV.157 and IV.173 in a larger stylistic/production group, "
        "but does not say these are one codex. Its categories therefore cannot be treated as a direct contradiction "
        "of the narrower BOMPAC reconstruction units."
    ))
    h03["outcome"] = (
        "Still C / unresolved. The published BOMPAC unit split and the broader Naantali-related production group "
        "use potentially different relationship levels; direct image and textual evidence is still needed to test "
        "the specific same-codex claim."
    )
    h04 = next(item for item in review_doc["reviews"] if item["id"] == "H04")
    h04["prior_status"] = (
        "E27 maps IV.173/Fr 29666/Fr 25592 to BOMPAC-9531 and Fr 1385/IV.157 to BOMPAC-912. E28 locates "
        "Walta 2013's broader stylistic/production group containing both IV.173 and IV.157."
    )
    h04["outcome"] = (
        "Still C / unresolved. Walta's broader group and BOMPAC's narrower units are not demonstrably competing "
        "claims. No new direct evidence establishes a same-codex relationship between IV.173 and IV.157/Fr 1385."
    )
    h04["next_evidence_needed"] = (
        "Read the complete Walta 2013 discussion and the cited Taitto/Keskiaho passages, then compare their "
        "relationship definitions. For a physical join, test corresponding text, page order/signatures and "
        "material features; do not equate a broader style group with a single codex."
    )
    h05 = next(item for item in review_doc["reviews"] if item["id"] == "H05")
    h05["prior_status"] = (
        "E27 finds Hy 49/Fr 25592 in BOMPAC-9531 with IV.173 and Fr 29666. E28 locates Walta 2013's broader "
        "Naantali-related group, which includes IV.173 and IV.157, while distinguishing several hands and uncertain origin."
    )
    h05["outcome"] = (
        "Still C / unresolved. BOMPAC's grouping and the earlier broad style/production group are useful prior art, "
        "not independent proof that the visually different leaves belonged to one codex. The E27 source difference "
        "is not established as a contradiction."
    )
    h05["next_evidence_needed"] = (
        "Read Walta 2013 in full and compare its group definitions with Fragmenta and BOMPAC. Then test diagnostic "
        "texts, openings/signatures and physical structure in IV.173 and Fr 25592, using the accepted Fr 29666/Ant 242 "
        "comparator if an authorized image is available."
    )
    for review in (h03, h04, h05):
        sources = review.setdefault("sources", [])
        for source in (REPORT, PORTAL, PDF):
            append_unique(sources, source)

    REVIEWS.write_text(json.dumps(review_doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "context_checks": len(checks),
        "updated_context": "CTX10",
        "context_path": "data/context_checks.v9.json",
        "queue_sha256": review_doc["queue_sha256"],
        "updated_reviews": ["H03", "H04", "H05"],
    }, indent=2))


if __name__ == "__main__":
    main()
