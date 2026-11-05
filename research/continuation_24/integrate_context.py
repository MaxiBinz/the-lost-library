#!/usr/bin/env python3
"""Add the H03 metadata screen as a separate, non-hypothesis context check."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE_CHECKS = ROOT / "data/context_checks.v5.json"
OUTPUT_CHECKS = ROOT / "data/context_checks.v6.json"
REVIEW_PATH = ROOT / "data/hypothesis_reviews.v1.json"
RESULT_PATH = ROOT / "research/continuation_24/h03_layout_results.json"
QUEUE_HASH = "b3e299a7c600584ce44518db1f5c30c3301edae0a07a8b009075498f64ccec47"


def main() -> None:
    checks_doc = json.loads(BASE_CHECKS.read_text())
    review = json.loads(REVIEW_PATH.read_text())
    result = json.loads(RESULT_PATH.read_text())
    if review["queue_sha256"] != QUEUE_HASH or result["frozen_queue_sha256"] != QUEUE_HASH:
        raise SystemExit("Frozen hypothesis queue changed; context integration stopped")
    if any(check["id"] == "CTX08" for check in checks_doc["checks"]):
        raise SystemExit("CTX08 already exists in the source context document")
    if result["hypothesis_id"] != "H03" or result["interpretation"]["new_discovery"]:
        raise SystemExit("Unexpected result: this source check must remain contextual")

    check = {
        "id": "CTX08",
        "title": "H03 matched catalogue layout screen",
        "record_ids": [
            "mpo-20274", "mpo-8994", "mpo-7292", "mpo-10370", "mpo-10406", "mpo-10407"
        ],
        "observation_ids": [],
        "summary": (
            "The pinned MPO metadata records Fr8994 at 35.5 x 22.5 cm and Fr20274 at "
            "36.0 x 22.5 cm written area. A post-inspection screen of 22,909 catalogue "
            "rows selected Quadr, four-staff records with a leading 11 main-text-row count; "
            "the parser intentionally includes Fr20274's literal '11 (33)' as well as '#11'. "
            "This yields 244 records, 154 with parseable area, including 97 Antiphonaria "
            "(52 dimensioned). The full machine-readable query is in the linked result."
        ),
        "outcome": (
            "The candidate pair has closely similar catalogue written-area dimensions, "
            "consistent with the already suggested relationship. At a 0.5 cm-expanded "
            "pair bounding box, seven matched Antiphonaria include the pair, two Codex 1306 "
            "records (Fr7292 and Fr9165), and three other Codex 1505 leaves. This supports "
            "layout compatibility but does not distinguish one codex from shared format or "
            "production. H03 remains category C; no identity or novelty claim follows."
        ),
        "limits": [
            "The compared dimensions are inherited catalogue values from the same MPO source, not direct image measurements or independent physical observations.",
            "The exact box is post hoc and defined by the candidate pair; the two-record exact result is not a rarity statistic.",
            "Only 52 of 97 Quadr/four-line/11-row Antiphonaria have parseable dimensions; missingness is unquantified and likely not random.",
            "Fr20274's catalogue record omits leaf format and script; source photographs do not document complete physical sides.",
            "No corresponding Olavi text or melody in Fr20274, shared distinctive error, physical join, same hand, or same-book identity is established by this check.",
        ],
        "sources": [
            "research/continuation_24/h03_layout_screen.py",
            "research/continuation_24/h03_layout_results.json",
            "research/mpo.csv",
            "https://zenodo.org/records/17287665",
        ],
    }
    checks_doc["version"] = "1.0.0"
    checks_doc["assessment_date"] = "2026-10-24"
    checks_doc["checks"].append(check)
    OUTPUT_CHECKS.write_text(json.dumps(checks_doc, ensure_ascii=False, indent=2) + "\n")

    review["version"] = "1.7.0"
    review["assessment_date"] = "2026-10-24"
    review["context_checks_path"] = "data/context_checks.v6.json"
    REVIEW_PATH.write_text(json.dumps(review, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({
        "context_checks": len(checks_doc["checks"]),
        "new_check": "CTX08",
        "queue_sha256_unchanged": QUEUE_HASH,
        "reviews_path": str(REVIEW_PATH.relative_to(ROOT)),
        "checks_path": str(OUTPUT_CHECKS.relative_to(ROOT)),
    }, indent=2))


if __name__ == "__main__":
    main()
