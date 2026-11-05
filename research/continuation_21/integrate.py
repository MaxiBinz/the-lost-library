"""Add the E21 source measurement as an auxiliary, non-hypothesis context check."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
QUEUE_SHA = "b3e299a7c600584ce44518db1f5c30c3301edae0a07a8b009075498f64ccec47"


def load(path):
    return json.loads((ROOT / path).read_text())


def write(path, value):
    (ROOT / path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def main():
    queue_hash = hashlib.sha256((ROOT / "data/hypotheses.v1.json").read_bytes()).hexdigest()
    if queue_hash != QUEUE_SHA:
        raise ValueError("The frozen ten-pair queue has changed")

    previous_observations = load("data/observations.v6.json")
    new_observations = load("research/continuation_21/observations.json")["annotations"]
    annotations = previous_observations["annotations"] + new_observations
    if len({item["id"] for item in annotations}) != len(annotations):
        raise ValueError("Duplicate observation identifier")
    write("data/observations.v7.json", {
        **previous_observations,
        "version": "7.0.0",
        "assessment_date": "2026-10-24",
        "inputs": previous_observations["inputs"] + ["research/continuation_21/observations.json"],
        "scope": "Post-review source tests, fixed registration falsification and calibrated exploratory ruling-layout check; no new attribution or predictor.",
        "annotations": annotations,
    })

    previous_contexts = load("data/context_checks.v3.json")
    checks = previous_contexts["checks"]
    if any(item["id"] == "CTX05" for item in checks):
        raise ValueError("CTX05 already exists; refusing to append a duplicate")
    checks.append({
        "id": "CTX05",
        "title": "Codex 1505 ruling pitch and full-MPO layout screen",
        "record_ids": ["mpo-10370", "mpo-10406", "mpo-8994", "mpo-10407", "mpo-10437", "mpo-1385", "mpo-8201", "mpo-8304"],
        "observation_ids": ["I21-10370-staff-pitch", "I21-10406-staff-pitch"],
        "summary": "Manual ruler-calibrated image measurements put selected Fr10370 and Fr10406 red staff-rule intervals at approximately5.6mm. The full pinned MPO export has9196Quadr/four-line entries,197 with11 text rows and149 of those with parseable written-space sizes; three other entries fall inside the five Codex1505 target records' exact dimension box, and ten within the ±1cm sensitivity box.",
        "outcome": "The images and catalogue fields are consistent with a shared page layout in the pre-existing Codex1505 grouping. This does not independently validate that grouping or provide a unique fingerprint; 4-line Quadr notation is widespread and the matching database is the source of the existing grouping.",
        "limits": [
            "Image regions and coordinates were selected after viewing the sources; this was not blind, preregistered or independently repeated.",
            "Ruler endpoints and staff-line centers are manually selected; perspective, page waviness, local deformation and ruling curvature are not corrected.",
            "The full MPO metadata is incomplete and non-random; only149 of197 records in the specified notation/row subset have parseable written-area sizes. The 3 and10 comparison counts are descriptive, not rarity estimates.",
            "Fr1385, already a documented comparator, is one exact-range match. The known wrong-book control Fr8201/8304 is not like-for-like Quadr notation; its records describe Gothic notation with three black and one red staff line.",
            "The catalogue itself supplies the Codex1505 association, so this screen cannot independently confirm it. No hand, workshop or parchment-origin claim follows."
        ],
        "sources": [
            "research/continuation_21/ruling_pitch_results.md",
            "research/continuation_21/ruling_pitch_results.json",
            "research/continuation_21/ruling_pitch_check.py",
            "https://zenodo.org/records/17287665"
        ]
    })
    write("data/context_checks.v4.json", {
        **previous_contexts,
        "version": "4.0.0",
        "assessment_date": "2026-10-24",
        "scope": "Supporting source checks; no additional frozen attribution hypotheses.",
        "checks": checks,
    })

    reviews = load("data/hypothesis_reviews.v1.json")
    reviews["version"] = "1.5.0"
    reviews["assessment_date"] = "2026-10-24"
    reviews["observations_path"] = "data/observations.v7.json"
    reviews["context_checks_path"] = "data/context_checks.v4.json"
    write("data/hypothesis_reviews.v1.json", reviews)

    print(json.dumps({
        "queue_sha256": queue_hash,
        "observations": len(annotations),
        "context_checks": len(checks),
        "new_context": "CTX05",
        "frozen_hypotheses_changed": False,
    }, indent=2))


if __name__ == "__main__":
    main()
