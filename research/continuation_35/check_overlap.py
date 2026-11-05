"""Fixed, exploratory E35 photograph-overlap test; no source writes or network.

Run with the already retained E20 OpenCV runtime:
  PYTHONPATH=/private/tmp/lost-library-cv20/isolated .venv/bin/python \
    research/continuation_35/check_overlap.py
Diagnostic PNGs contain labelled crops of existing source pixels and all matches.
They are analysis derivatives, never new manuscript captures or inferred stitches.
"""
from __future__ import annotations

import hashlib
import json
import platform
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
FROZEN = json.loads((ROOT / "research/continuation_33/results.json").read_text())["frozen_inputs"]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(spec, captures):
    path, box = spec
    cap = captures[path]
    assert sha(ROOT / path) == cap["sha256"]
    with Image.open(ROOT / path) as im:
        x, y, w, h = box
        assert list(im.size) == [cap["width"], cap["height"]]
        assert 0 <= x < x + w <= im.width and 0 <= y < y + h <= im.height
        rgb = np.asarray(im.convert("RGB").crop((x, y, x + w, y + h)))
    gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
    gray = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8)).apply(gray)
    return gray, rgb, {"path": path, "sha256": cap["sha256"], "roi_xywh": box,
                       "image_dimensions": [cap["width"], cap["height"]],
                       "canvas_id": cap.get("canvas_id"), "source_url": cap["url"],
                       "rights_url": cap["rights_url"], "attribution": cap["attribution"]}


def mutual_matches(a, b):
    if a is None or b is None or len(a) < 2 or len(b) < 2:
        return []
    matcher = cv2.BFMatcher(cv2.NORM_L2)
    f = {m.queryIdx: m.trainIdx for m, n in matcher.knnMatch(a, b, k=2)
         if m.distance < 0.75 * n.distance}
    r = {m.queryIdx: m.trainIdx for m, n in matcher.knnMatch(b, a, k=2)
         if m.distance < 0.75 * n.distance}
    return [(i, j) for i, j in f.items() if r.get(j) == i]


def distinct_count(points):
    kept = []
    for point in points:
        if all(np.linalg.norm(point - other) >= 2.0 for other in kept):
            kept.append(point)
    return len(kept)


def span(points, shape):
    return {"x": float(np.ptp(points[:, 0]) / shape[1]),
            "y": float(np.ptp(points[:, 1]) / shape[0])}


def run(spec, captures):
    cv2.setRNGSeed(35)
    ga, rgb_a, source_a = load(spec["left"], captures)
    gb, rgb_b, source_b = load(spec["right"], captures)
    sift = cv2.SIFT_create()
    ka, da = sift.detectAndCompute(ga, None)
    kb, db = sift.detectAndCompute(gb, None)
    matches = mutual_matches(da, db)
    output = {"id": spec["id"], "role": spec["role"], "sources": [source_a, source_b],
              "keypoints": [len(ka), len(kb)], "mutual_ratio_matches": len(matches),
              "inliers": 0, "distinct_inlier_positions": [0, 0], "inlier_spans": None,
              "homography_roi_coordinates": None, "median_inlier_error_px": None,
              "all_mutual_correspondences": []}
    inlier_mask = np.zeros(len(matches), dtype=bool)
    if len(matches) >= 4:
        a = np.float32([ka[i].pt for i, _ in matches])
        b = np.float32([kb[j].pt for _, j in matches])
        h, mask = cv2.findHomography(a, b, cv2.RANSAC, 3.0, maxIters=2000, confidence=0.995)
        if h is not None and mask is not None:
            inlier_mask = mask.ravel().astype(bool)
            ia, ib = a[inlier_mask], b[inlier_mask]
            prediction = cv2.perspectiveTransform(ia.reshape(-1, 1, 2), h).reshape(-1, 2)
            output.update({"inliers": int(inlier_mask.sum()),
                           "distinct_inlier_positions": [distinct_count(ia), distinct_count(ib)],
                           "inlier_spans": [span(ia, ga.shape), span(ib, gb.shape)],
                           "homography_roi_coordinates": h.tolist(),
                           "median_inlier_error_px": float(np.median(np.linalg.norm(prediction - ib, axis=1)))})
    spans = output["inlier_spans"]
    output["screen_passed"] = bool(len(matches) >= 8 and output["inliers"] >= 8
                                   and min(output["distinct_inlier_positions"]) >= 8
                                   and spans and all(v >= .20 for side in spans for v in side.values()))
    for (i, j), flag in zip(matches, inlier_mask):
        p, q = ka[i].pt, kb[j].pt
        output["all_mutual_correspondences"].append({
            "left_roi_xy": list(p), "right_roi_xy": list(q),
            "left_source_xy": [p[0] + source_a["roi_xywh"][0], p[1] + source_a["roi_xywh"][1]],
            "right_source_xy": [q[0] + source_b["roi_xywh"][0], q[1] + source_b["roi_xywh"][1]],
            "ransac_inlier": bool(flag)})
    # Preserve RGB correctly; PIL renders every match, including outliers.
    figure = Image.new("RGB", (rgb_a.shape[1] + rgb_b.shape[1], max(rgb_a.shape[0], rgb_b.shape[0]) + 60), "white")
    figure.paste(Image.fromarray(rgb_a), (0, 60))
    figure.paste(Image.fromarray(rgb_b), (rgb_a.shape[1], 60))
    draw = ImageDraw.Draw(figure)
    draw.text((10, 8), spec["id"] + " / " + spec["role"], fill="black")
    draw.text((10, 28), f"{len(matches)} mutual matches; {output['inliers']} inliers; screen={output['screen_passed']}; green=inlier, red=outlier", fill="black")
    for item in output["all_mutual_correspondences"]:
        a, b = item["left_roi_xy"], item["right_roi_xy"]
        color = "#00bb55" if item["ransac_inlier"] else "#dd2244"
        p, q = (a[0], a[1] + 60), (b[0] + rgb_a.shape[1], b[1] + 60)
        draw.line([p, q], fill=color, width=1)
        for x, y in [p, q]:
            draw.ellipse((x-3, y-3, x+3, y+3), outline=color, width=1)
    output["review_figure"] = "research/continuation_35/" + spec["id"] + "-matches.png"
    figure.save(ROOT / output["review_figure"])
    return output


def main():
    before = {p: sha(ROOT / p) for p in FROZEN}
    assert before == FROZEN
    protocol = json.loads((HERE / "protocol.json").read_text())
    captures = {}
    for record in json.loads((ROOT / "data/fragments.json").read_text()):
        for cap in record.get("captures", []):
            captures[cap["path"]] = {**cap, "rights_url": cap.get("rights_url") or record["rights_url"], "attribution": record["attribution"]}
    results = [run(spec, captures) for spec in protocol["pairs"]]
    # Post-fit review illustration only: source-pixel strips selected after
    # inspecting the 1/2 inliers. It changes neither test ROI nor decision gate.
    strips = [("data/images/mpo-8994-capture-1-1802px.jpg", (650,1180,1400,1246)),
              ("data/images/mpo-8994-capture-2-1835px.jpg", (595,0,1345,65))]
    strip_figure = Image.new("RGB", (1540,150), "white")
    draw = ImageDraw.Draw(strip_figure)
    for i,(path,box) in enumerate(strips):
        with Image.open(ROOT/path) as im:
            strip_figure.paste(im.convert("RGB").crop(box), (770*i,40))
        draw.text((770*i,8),Path(path).name+" "+str(box),fill="black")
    strip_figure.save(HERE/"thin-fold-original-pixels.png")
    assert before == {p: sha(ROOT / p) for p in FROZEN}
    output = {"version": "1.0.0", "date": "2026-10-27", "protocol_sha256": sha(HERE / "protocol.json"),
              "script_sha256": sha(Path(__file__)), "method": protocol["method"],
              "runtime": {"python": platform.python_version(), "opencv": cv2.__version__, "numpy": np.__version__,
                          "opencv_origin": cv2.__file__, "dependency_receipt": "research/continuation_20/registration/dependency_receipt.json"},
              "results": results, "frozen_inputs": before, "new_downloads": 0, "source_mutations": 0,
              "limits": "Feature-screen results require source inspection; no codex identification, side assignment, independent confirmation or novelty follows from registration alone."}
    (HERE / "feature_results.json").write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps([{k: row[k] for k in ["id", "mutual_ratio_matches", "inliers", "distinct_inlier_positions", "screen_passed"]} for row in results], indent=2))


if __name__ == "__main__":
    main()
