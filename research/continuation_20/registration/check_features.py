"""Fixed SIFT/RANSAC check of declared Fr 10370 capture-boundary ROIs.

This is a falsification-oriented follow-up to ``check_bands.py``.  It does
not search other regions, alter the declared ROIs, or identify manuscripts.
The same procedure is applied to the two proposed surface continuations and
to a text-continuity/different-surface control.

Run with the isolated OpenCV wheel recorded in dependency_receipt.json:
  PYTHONPATH=/private/tmp/lost-library-cv20/isolated .venv/bin/python \
    research/continuation_20/registration/check_features.py
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent

# Copied verbatim from the fixed translation protocol before this feature test.
PAIRS = [
    {"id": "capture1_2", "role": "candidate partial views of one surface",
     "left": (1, [234, 1290, 1179, 127]), "right": (2, [232, 25, 1163, 100])},
    {"id": "capture3_4", "role": "candidate partial views of one surface",
     "left": (3, [300, 1040, 1180, 193]), "right": (4, [300, 0, 1180, 190])},
    {"id": "capture2_3_control", "role": "different-surface text-boundary control",
     "left": (2, [650, 490, 740, 115]), "right": (3, [345, 330, 1155, 85])},
]

# Fixed conventional screen, chosen before execution.  Passing it means only
# that the output deserves manual inspection; it cannot by itself prove a seam.
RATIO = 0.75
RANSAC_REPROJECTION_THRESHOLD = 3.0
MIN_MUTUAL_RATIO_MATCHES = 8
MIN_RANSAC_INLIERS = 8
MIN_INLIER_AXIS_SPAN_FRACTION = 0.20


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_capture(record, index, box):
    capture = next(c for c in record["captures"]
                   if c.get("resolution_variant") and c["capture_index"] + 1 == index)
    path = ROOT / capture["path"]
    assert sha(path) == capture["sha256"]
    with Image.open(path) as im:
        x, y, w, h = box
        assert x >= 0 and y >= 0 and x + w <= im.width and y + h <= im.height
        rgb = np.asarray(im.crop((x, y, x + w, y + h)).convert("RGB"))
    # CLAHE is a fixed local-contrast transform; no colour/ruling segmentation
    # is used to manufacture correspondences.
    gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
    gray = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8)).apply(gray)
    return gray, rgb, {"capture_index_one_based": index, "path": capture["path"],
                       "sha256": capture["sha256"], "roi_xywh": box,
                       "source_url": capture["url"]}


def ratio_matches(desc_a, desc_b):
    if desc_a is None or desc_b is None or len(desc_a) < 2 or len(desc_b) < 2:
        return []
    matcher = cv2.BFMatcher(cv2.NORM_L2)
    forward = matcher.knnMatch(desc_a, desc_b, k=2)
    reverse = matcher.knnMatch(desc_b, desc_a, k=2)
    accepted_forward = {m.queryIdx: m.trainIdx for m, n in forward if m.distance < RATIO * n.distance}
    accepted_reverse = {m.queryIdx: m.trainIdx for m, n in reverse if m.distance < RATIO * n.distance}
    return [(a, b) for a, b in accepted_forward.items() if accepted_reverse.get(b) == a]


def axis_span(points, shape):
    if len(points) < 2:
        return {"x": 0.0, "y": 0.0}
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    height, width = shape[:2]
    return {"x": float((max(xs) - min(xs)) / width),
            "y": float((max(ys) - min(ys)) / height)}


def run_pair(spec, record):
    left_index, left_box = spec["left"]
    right_index, right_box = spec["right"]
    left_gray, left_rgb, left_source = load_capture(record, left_index, left_box)
    right_gray, right_rgb, right_source = load_capture(record, right_index, right_box)
    sift = cv2.SIFT_create()  # OpenCV defaults, recorded in output.
    kp_l, d_l = sift.detectAndCompute(left_gray, None)
    kp_r, d_r = sift.detectAndCompute(right_gray, None)
    mutual = ratio_matches(d_l, d_r)
    record_out = {
        "id": spec["id"], "role": spec["role"],
        "sources": [{"side": "left", **left_source}, {"side": "right", **right_source}],
        "keypoints": {"left": len(kp_l), "right": len(kp_r)},
        "mutual_ratio_matches": len(mutual), "ratio": RATIO,
        "ransac_reprojection_threshold_px": RANSAC_REPROJECTION_THRESHOLD,
        "inliers": 0, "inlier_spans": None, "homography": None,
        "median_inlier_reprojection_error_px": None,
        "candidate_ransac_inlier_correspondences": [],
    }
    if len(mutual) >= 4:
        src = np.float32([kp_l[a].pt for a, _ in mutual]).reshape(-1, 1, 2)
        dst = np.float32([kp_r[b].pt for _, b in mutual]).reshape(-1, 1, 2)
        homography, mask = cv2.findHomography(src, dst, cv2.RANSAC, RANSAC_REPROJECTION_THRESHOLD)
        if homography is not None and mask is not None:
            which = mask.ravel().astype(bool)
            in_src = src.reshape(-1, 2)[which]
            in_dst = dst.reshape(-1, 2)[which]
            predicted = cv2.perspectiveTransform(in_src.reshape(-1, 1, 2), homography).reshape(-1, 2)
            errors = np.linalg.norm(predicted - in_dst, axis=1)
            record_out.update({
                "inliers": int(which.sum()),
                "inlier_spans": {"left": axis_span(in_src, left_gray.shape),
                                 "right": axis_span(in_dst, right_gray.shape)},
                "homography": homography.round(8).tolist(),
                "median_inlier_reprojection_error_px": float(np.median(errors)),
                "candidate_ransac_inlier_correspondences": [
                    {"left_xy": [round(float(x), 2), round(float(y), 2)],
                     "right_xy": [round(float(u), 2), round(float(v), 2)]}
                    for (x, y), (u, v) in zip(in_src, in_dst)
                ],
            })
    spans = record_out["inlier_spans"]
    distributed = bool(spans and all(
        value >= MIN_INLIER_AXIS_SPAN_FRACTION
        for side in spans.values() for value in side.values()))
    record_out["strong_registration_screen"] = bool(
        record_out["mutual_ratio_matches"] >= MIN_MUTUAL_RATIO_MATCHES and
        record_out["inliers"] >= MIN_RANSAC_INLIERS and distributed)
    record_out["outcome"] = (
        "Manual-review candidate only: fixed feature screen passed; no physical join is claimed."
        if record_out["strong_registration_screen"] else
        "No accepted registration: fixed feature screen did not produce enough distributed RANSAC inliers."
    )
    # A review visual shows all mutual matches; it never hides non-inliers.
    draw_matches = [cv2.DMatch(_queryIdx=a, _trainIdx=b, _imgIdx=0, _distance=0) for a, b in mutual]
    image = cv2.drawMatches(left_rgb, kp_l, right_rgb, kp_r, draw_matches, None,
                            flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
    Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB)).save(OUT / f"{spec['id']}-sift-matches.png")
    return record_out


def main():
    records = json.loads((ROOT / "data/fragments.json").read_text())
    record = next(r for r in records if r["id"] == "mpo-10370")
    output = {
        "assessment_date": "2026-10-24", "method": {
            "library": "opencv-python-headless", "opencv_version": cv2.__version__,
            "sift": "OpenCV SIFT_create defaults", "clahe": {"clip_limit": 2.0, "tile_grid": [8, 8]},
            "ratio_test": RATIO, "mutual": True,
            "ransac": {"model": "homography", "reprojection_threshold_px": RANSAC_REPROJECTION_THRESHOLD},
            "screen": {"minimum_mutual_ratio_matches": MIN_MUTUAL_RATIO_MATCHES,
                       "minimum_inliers": MIN_RANSAC_INLIERS,
                       "minimum_axis_span_fraction_each_axis": MIN_INLIER_AXIS_SPAN_FRACTION},
            "scope": "Only the three predeclared ROIs; no new images, ROI changes, or parameter tuning."},
        "results": [run_pair(spec, record) for spec in PAIRS],
        "limits": "A passed feature screen would require independent visual review and cannot establish a medieval leaf, side, sequence or manuscript relationship. A failed screen cannot prove different faces.",
        "source_downloads": 0, "source_mutations": 0, "new_discovery": False,
    }
    (OUT / "feature_results.json").write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps([{k: item[k] for k in ("id", "keypoints", "mutual_ratio_matches", "inliers", "strong_registration_screen", "outcome")} for item in output["results"]], indent=2))


if __name__ == "__main__":
    main()
