"""Reproduce the ruler-calibrated Fr 7292 matched-control check.

This is a source-linked descriptive measurement, not a classifier or identity test.
The page was chosen from the pinned MPO metadata query before its image was fetched.
Staff-line centers were manually selected after visual inspection.
"""
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
CONTROL_ID = "7292"
IMAGE_RELATIVE = "data/images/mpo-7292-capture-1-1600px.jpg"
IMAGE_SHA256 = "a864bec13a29a315a7df8e910b23118ef76fc631be8e10f97b60ec3b732285f2"
RULER_Y_CM = {0: 70, 20: 948}
STAFF_GROUPS = {
    "system_1": [242, 263, 289, 314],
    "system_2": [375, 398, 424, 449],
}


def read_json(path: str):
    return json.loads((ROOT / path).read_text())


def main():
    image_path = ROOT / IMAGE_RELATIVE
    raw = image_path.read_bytes()
    image_hash = hashlib.sha256(raw).hexdigest()
    if image_hash != IMAGE_SHA256:
        raise ValueError("The registered Fr 7292 image hash changed")
    with Image.open(image_path) as image:
        width, height = image.size

    with (ROOT / "research/mpo.csv").open(newline="", encoding="utf-8-sig") as source:
        row = next(r for r in csv.DictReader(source) if r["signatur"] == CONTROL_ID)
    expected = {
        "sachtitel": "Antiphonarium",
        "notation": "Quadr",
        "notenlinien": "4",
        "zeilenzahl1": "#11",
        "codex": "Codex 1306",
    }
    for key, value in expected.items():
        if row.get(key) != value:
            raise ValueError(f"Fr 7292 no longer matches metadata selection: {key}")

    e21 = read_json("research/continuation_21/ruling_pitch_results.json")
    screen = e21["catalogue_layout_screen"]
    if CONTROL_ID not in {item["signatur"] for item in screen["other_records_inside_exact_box"]}:
        raise ValueError("Fr 7292 is no longer an exact-box control in the pinned query")

    scale_px_per_cm = (RULER_Y_CM[20] - RULER_Y_CM[0]) / 20
    systems = {}
    intervals = []
    for name, centers in STAFF_GROUPS.items():
        adjacent = [b - a for a, b in zip(centers, centers[1:])]
        mean_px = sum(adjacent) / len(adjacent)
        pitch_mm = mean_px / scale_px_per_cm * 10
        systems[name] = {
            "line_center_rows_px": centers,
            "adjacent_intervals_px": adjacent,
            "mean_interval_px": mean_px,
            "approx_pitch_mm": round(pitch_mm, 3),
        }
        intervals.extend(adjacent)

    control_mean_px = sum(intervals) / len(intervals)
    control_pitch_mm = control_mean_px / scale_px_per_cm * 10
    target_measurements = [x["aggregate_approx_pitch_mm"] for x in e21["staff_pitch_measurements"]]
    target_mean = sum(target_measurements) / len(target_measurements)
    result = {
        "version": "1.0.0",
        "assessment_date": "2026-10-24",
        "question": "Does the approximately 5.6 mm staff pitch distinguish the existing Codex 1505 grouping from a catalogue-matched different codex?",
        "selection_protocol": {
            "status": "Fr 7292 selected from pinned MPO metadata before its image was retrieved; staff systems selected after image inspection, so measurement is not blind.",
            "metadata_filter": "Quadr notation; four music lines; 11 main-text rows; Antiphonarium; exact Codex 1505 written-area range; a distinct recorded MPO codex group.",
            "candidate_source": "E21 full-MPO exact-box screen; Fr 1385 was already a documented group comparator and Fr 10096 is a Graduale, so Fr 7292 was the closest different-codex antiphonary control.",
        },
        "control": {
            "fragment_id": "mpo-7292",
            "codex_label": row["codex"],
            "genre": row["sachtitel"],
            "notation": row["notation"],
            "staff_lines": row["notenlinien"],
            "main_text_rows": row["zeilenzahl1"],
            "written_area": row["schriftraum1"],
            "dating": row["datierung"],
            "content_excerpt": row["inhalt"],
            "metadata_source": "Pinned MPO v1.0.0 CSV; catalogue codex label is not independent adjudication.",
        },
        "image": {
            "path": IMAGE_RELATIVE,
            "url": "https://lbiiif.riksarkivet.se/v3/arkis!R1007292_00001/full/1600,/0/default.jpg",
            "canvas_id": "https://lbiiif.riksarkivet.se/arkis!R1007292_00001/canvas",
            "sha256": image_hash,
            "dimensions_px": [width, height],
            "rights_url": "http://creativecommons.org/publicdomain/mark/1.0/",
            "manifest_path": "research/continuation_22/mpo-7292-manifest.json",
            "receipt_path": "research/continuation_22/image_receipt.json",
        },
        "ruler_calibration": {
            "axis": "vertical image axis; photographed metric ruler at left edge",
            "label_span_cm": 20,
            "endpoint_centers_px": [RULER_Y_CM[0], RULER_Y_CM[20]],
            "label_order": [0, 20],
            "pixels_per_cm": round(scale_px_per_cm, 3),
            "coordinate_origin": "top-left of 1600px JPEG",
        },
        "staff_groups": systems,
        "aggregate": {
            "adjacent_interval_count": len(intervals),
            "mean_interval_px": round(control_mean_px, 3),
            "approx_pitch_mm": round(control_pitch_mm, 3),
        },
        "comparison": {
            "e21_codex1505_fragment_means_mm": [round(v, 3) for v in target_measurements],
            "e21_target_mean_mm": round(target_mean, 3),
            "control_minus_target_mean_mm": round(control_pitch_mm - target_mean, 3),
            "interpretation": "The matched control's estimated pitch is effectively the same as the two E21 Codex 1505 estimates at this measurement resolution. Staff pitch alone is therefore not unique to the catalogued group.",
        },
        "limits": [
            "Only one different-codex leaf was measured; this is not a distribution or classifier test.",
            "The matching Codex 1306 label and all selection metadata come from MPO, the same cataloguing system used for the Codex 1505 group.",
            "Fr 7292 is matched on genre, notation, staff count, main-text rows and written-area range, not on hand or workshop.",
            "Line centers and ruler endpoints are manual; approximately ±1 px per line center and ±2 px per ruler endpoint, before perspective, page curvature, ruling waviness and ruler-to-writing-plane effects.",
            "The measured image areas were selected after inspection; no blind or independent repeated measurement was made.",
            "No same-book, same-hand, workshop, provenance or historical attribution follows.",
        ],
    }
    output = ROOT / "research/continuation_22/matched_staff_results.json"
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"output": str(output.relative_to(ROOT)), "control_pitch_mm": result["aggregate"]["approx_pitch_mm"], "target_mean_mm": round(target_mean, 3), "difference_mm": result["comparison"]["control_minus_target_mean_mm"], "image_sha256": image_hash}, indent=2))


if __name__ == "__main__":
    main()
