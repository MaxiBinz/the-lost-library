"""Integrate the E29 catalogue qualifier check without changing the frozen queue."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "data/context_checks.v9.json"
DEST = ROOT / "data/context_checks.v10.json"
REVIEWS = ROOT / "data/hypothesis_reviews.v1.json"
QUEUE_SHA256 = "b3e299a7c600584ce44518db1f5c30c3301edae0a07a8b009075498f64ccec47"
REPORT = "RESEARCH_CONTINUATION_29.md"
IV156 = "https://fragmenta.kansalliskirjasto.fi/handle/10024/1299"
IV157 = "https://fragmenta.kansalliskirjasto.fi/handle/10024/1300"


def append_unique(items: list[str], value: str) -> None:
    if value not in items:
        items.append(value)


def main() -> None:
    checks_doc = json.loads(SOURCE.read_text(encoding="utf-8"))
    checks = checks_doc["checks"]
    check = {
        "id": "CTX11",
        "title": "Fragmenta catalogue relationship qualifiers for IV.156 and IV.157",
        "record_ids": ["finn-iv173", "mpo-1385", "mpo-25592"],
        "observation_ids": [],
        "summary": (
            "The National Library of Finland's indexed Fragmenta catalogue entries describe F.m.IV.156 and "
            "F.m.IV.157 as Dominican antiphonaries for the Diocese of Åbo, with one-column, 11-line layouts, "
            "similar square notation and overlapping dimensions. IV.156 is explicitly said to bear a strong "
            "stylistic resemblance to IV.157. The entries separately label specific links: IV.156 lists Turku "
            "Ms. c as from the same codex and Codex 1505 as suggested; IV.157 lists Ant 99 and Fr 1385 as from "
            "the same codex and lists Turku Ms. c and Codex 1505 as suggested. The IV.157 page returned 403 "
            "when directly opened, so the detailed text is recorded as search-indexed catalogue text."
        ),
        "outcome": (
            "A shared broad style group or Codex 1505 suggestion does not assert that IV.156 and IV.157 are "
            "one codex. This clarifies the relationship levels in E27/E28; it neither resolves the IV.173 joins "
            "nor establishes a new attribution. H03–H05 remain unresolved."
        ),
        "limits": [
            "Detailed catalogue wording was available through the search index; direct page access to IV.157 returned HTTP 403.",
            "No manuscript image, physical object, page-side mapping, or diagnostic textual/music variant was tested in E29.",
            "The cited Taitto 2001 pp. 161–168 and Keskiaho 2010 pp. 418–419 passages remain unread.",
            "Stylistic resemblance, shared liturgical use, or a suggested Codex 1505 association does not prove same-codex identity.",
            "The check does not modify the frozen queue, baseline predictors, or thresholds.",
        ],
        "sources": [REPORT, IV156, IV157],
    }
    checks[:] = [item for item in checks if item.get("id") != "CTX11"]
    checks.append(check)
    checks_doc["version"] = "1.4.0"
    checks_doc["assessment_date"] = "2026-10-25"
    checks_doc["scope"] = "Supporting source, layout-control and prior-art checks; no additional frozen attribution hypotheses."
    DEST.write_text(json.dumps(checks_doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    review_doc = json.loads(REVIEWS.read_text(encoding="utf-8"))
    if review_doc.get("queue_sha256") != QUEUE_SHA256:
        raise ValueError("Frozen hypothesis queue hash changed")
    review_doc["version"] = "1.11.0"
    review_doc["assessment_date"] = "2026-10-25"
    review_doc["context_checks_path"] = "data/context_checks.v10.json"

    for ident in ("H03", "H04", "H05"):
        review = next(item for item in review_doc["reviews"] if item["id"] == ident)
        review["prior_status"] = (
            review["prior_status"] + " E29 checked the indexed IV.156/IV.157 catalogue entries: the catalogue distinguishes "
            "stylistic resemblance and suggested Codex 1505 links from its specific same-codex labels."
        )
        append_unique(review["against"], (
            "The official Fragmenta catalogue describes IV.156 and IV.157 as stylistically similar but does not say they "
            "are the same codex; Codex 1505 is listed as a suggestion, while other links receive explicit same-codex labels."
        ))
        append_unique(review["sources"], REPORT)
        append_unique(review["sources"], IV156)
        append_unique(review["sources"], IV157)

    review_doc["reviews"][:] = review_doc["reviews"]
    REVIEWS.write_text(json.dumps(review_doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "context_checks": len(checks),
        "updated_context": "CTX11",
        "context_path": "data/context_checks.v10.json",
        "queue_sha256": review_doc["queue_sha256"],
        "updated_reviews": ["H03", "H04", "H05"],
    }, indent=2))


if __name__ == "__main__":
    main()
