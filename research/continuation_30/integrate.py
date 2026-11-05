"""Integrate the H08–H10 BOMPAC crosswalk without changing queue labels."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RESULT = Path(__file__).resolve().parent / "bompac_suggestion_crosswalk_results.json"
REVIEWS = ROOT / "data/hypothesis_reviews.v1.json"
QUEUE = ROOT / "data/hypotheses.v1.json"
QUEUE_SHA256 = "b3e299a7c600584ce44518db1f5c30c3301edae0a07a8b009075498f64ccec47"
REPORT = "RESEARCH_CONTINUATION_30.md"
MACHINE_RESULT = "research/continuation_30/bompac_suggestion_crosswalk_results.json"
SOURCES = [
    MACHINE_RESULT,
    "https://doi.org/10.5281/zenodo.17511106",
    "https://doi.org/10.5281/zenodo.17701360",
]


def append_unique(items: list[str], value: str) -> None:
    if value not in items:
        items.append(value)


def main() -> None:
    queue_hash = hashlib.sha256(QUEUE.read_bytes()).hexdigest()
    if queue_hash != QUEUE_SHA256:
        raise ValueError("Frozen hypothesis queue changed")
    result = json.loads(RESULT.read_text(encoding="utf-8"))
    if result["queue_sha256"] != QUEUE_SHA256:
        raise ValueError("Crosswalk result was generated for another queue")

    document = json.loads(REVIEWS.read_text(encoding="utf-8"))
    if document.get("queue_sha256") != QUEUE_SHA256:
        raise ValueError("Reviews refer to a different queue")
    by_id = {review["id"]: review for review in document["reviews"]}
    ref_by_id = {
        "Fr 1385": "mpo-1385", "Fr 4223": "mpo-4223",
        "Fr 8311": "mpo-8311", "Fr 8455": "mpo-8455",
    }
    candidate_ref = {"H08": "Fr 4223", "H09": "Fr 8311", "H10": "Fr 8455"}
    for ident, candidate in candidate_ref.items():
        review = by_id[ident]
        if review["classification"] != "C" or review["new_discovery"]:
            raise ValueError(f"Unexpected review state for {ident}")
        pair = (review["left_id"], review["right_id"])
        if pair != (ref_by_id["Fr 1385"], ref_by_id[candidate]):
            raise ValueError(f"Pair changed for {ident}")

        prior = (
            f" E30's checksum-verified BOMPAC crosswalk assigns {candidate} to BOMPAC-258/Ant-39/Codex-1200/FM.IV.159, "
            "while assigning Fr 1385 to BOMPAC-912/Ant-99/FM.IV.157. The raw MPO workbook likewise groups the candidate "
            "in C-17/Codex-1200 and lists Fr 1385 as singleton F-1385."
        )
        if "E30's checksum-verified BOMPAC crosswalk" not in review["prior_status"]:
            review["prior_status"] += prior
        contrary = (
            f"The BOMPAC combined reconstruction workbook assigns {candidate} to BOMPAC-258 (Ant-39/Codex-1200/FM.IV.159) "
            "and Fr 1385 to BOMPAC-912 (Ant-99/FM.IV.157); its raw MPO workbook similarly places the candidate in C-17 "
            "and Fr 1385 in singleton F-1385. These are published reconstruction assignments, not fresh image proof or "
            "independent adjudication. They weigh against treating the model suggestion as a new same-codex match but do "
            "not by themselves disprove physical connection, a shared hand, or broader production context."
        )
        append_unique(review["against"], contrary)
        review["outcome"] = (
            "The checksum-verified BOMPAC datasets place the suggested pair in different reconstruction units and group all "
            "three suggestions with Ant 39/Codex 1200. The high model compatibility is therefore not new same-book evidence. "
            "Because workbook labels are not a fresh physical examination, retain category C rather than claim rejection."
        )
        review["next_evidence_needed"] = (
            "Only reopen the same-codex proposal if source-level text, foliation/quire evidence, or diagnostic hand/notation "
            "features can test the BOMPAC separation; otherwise treat this as an unresolved model lookalike, not a new discovery."
        )
        for source in SOURCES:
            append_unique(review["sources"], source)

    document["version"] = "1.12.0"
    document["assessment_date"] = "2026-10-25"
    REVIEWS.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"updated_reviews": sorted(candidate_ref),
                      "classifications_unchanged": True,
                      "queue_sha256": queue_hash,
                      "review_version": document["version"]}, indent=2))


if __name__ == "__main__":
    main()
