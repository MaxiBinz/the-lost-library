"""Integrate the fixed Fr 10370 registration falsification without touching queue data."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
QUEUE_SHA = "b3e299a7c600584ce44518db1f5c30c3301edae0a07a8b009075498f64ccec47"


def load(path):
    return json.loads((ROOT / path).read_text())


def write(path, value):
    (ROOT / path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def add_once(values, value):
    if value not in values:
        values.append(value)


def main():
    assert hashlib.sha256((ROOT / "data/hypotheses.v1.json").read_bytes()).hexdigest() == QUEUE_SHA
    registration = load("research/continuation_20/registration/feature_results.json")
    baseline = load("research/continuation_20/registration/results.json")
    assert registration["source_downloads"] == baseline["source_downloads"] == 0
    assert not any(r["strong_registration_screen"] for r in registration["results"])

    obs = load("data/observations.v5.json")
    write("data/observations.v6.json", {
        **obs,
        "version": "6.0.0",
        "assessment_date": "2026-10-24",
        "inputs": obs["inputs"] + [
            "research/continuation_20/registration/results.json",
            "research/continuation_20/registration/feature_results.json",
        ],
        "scope": "Post-review source tests and fixed registration falsification; no new attribution or predictor.",
    })

    contexts = load("data/context_checks.v2.json")
    ctx = next(item for item in contexts["checks"] if item["id"] == "CTX01")
    ctx["summary"] += " A fixed translation-only screen and a fixed SIFT/mutual-ratio/RANSAC screen then tested the declared 1/2 and 3/4 boundary ROIs against the 2/3 different-surface control."
    ctx["outcome"] += " Neither proposed boundary passed the predeclared feature-registration screen (1/2: 4 RANSAC inliers from 9 mutual matches; 3/4: 5 from 28; 2/3 control: 5 from 18)."
    add_once(ctx["limits"], "Feature matching is a test for repeated photographed detail, not a test of adjacent-but-nonoverlapping page regions. Failed registration cannot prove different faces; low-inlier homographies are not joins.")
    add_once(ctx["sources"], "research/continuation_20/registration/results.json")
    add_once(ctx["sources"], "research/continuation_20/registration/feature_results.json")
    contexts["version"] = "3.0.0"
    contexts["assessment_date"] = "2026-10-24"
    write("data/context_checks.v3.json", contexts)

    reviews = load("data/hypothesis_reviews.v1.json")
    reviews["version"] = "1.4.0"
    reviews["assessment_date"] = "2026-10-24"
    reviews["observations_path"] = "data/observations.v6.json"
    reviews["context_checks_path"] = "data/context_checks.v3.json"
    h03 = next(item for item in reviews["reviews"] if item["id"] == "H03")
    add_once(h03["against"], "The predeclared Fr10370 boundary ROIs did not pass translation or SIFT/RANSAC registration; the same feature screen also produces small low-inlier fits for the deliberately different 2/3 control. These non-results do not prove different faces but remove no physical ambiguity.")
    add_once(h03["sources"], "research/continuation_20/registration/feature_results.json")
    write("data/hypothesis_reviews.v1.json", reviews)
    print(json.dumps({"annotations": len(obs["annotations"]), "contexts": len(contexts["checks"]), "queue_sha": QUEUE_SHA, "registration": "recorded as non-decisive"}))


if __name__ == "__main__":
    main()
