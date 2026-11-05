"""Reproduce the bounded Codex 1505 ruling-pitch and MPO layout screen.

This is an exploratory source check, not a blind or preregistered test. Image
coordinates were selected after viewing the photographs. No source image is
modified and the ten-pair attribution queue is not read or changed.
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
from pathlib import Path
from statistics import mean

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
CSV_PATH = ROOT / "research/mpo.csv"
EXPECTED_CSV_MD5 = "bac851653aa9b0816208a13430154cfb"
EXPECTED_CSV_SHA256 = "f5d2825703be19fd1994bc0b91724c32c67c36535622d5554c37b4029592d00b"


def digest(path: Path, algorithm: str) -> str:
    h = hashlib.new(algorithm)
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def parse_dimensions(value: str) -> tuple[float, float] | None:
    match = re.search(r"(\d+(?:\.\d+)?)\s*x\s*(\d+(?:\.\d+)?)", value or "")
    return tuple(map(float, match.groups())) if match else None


def measure_staff_pitch(item: dict) -> dict:
    path = ROOT / item["path"]
    sha = digest(path, "sha256")
    if sha != item["sha256"]:
        raise ValueError(f"Source hash changed: {item['path']}")
    with Image.open(path) as image:
        dimensions = list(image.size)
    if dimensions != item["image_dimensions"]:
        raise ValueError(f"Source dimensions changed: {item['path']}")

    groups = []
    interval_values = []
    for center_rows in item["staff_line_center_rows_px"]:
        gaps = [b - a for a, b in zip(center_rows, center_rows[1:])]
        pitch_px = mean(gaps)
        pitch_mm = pitch_px / item["ruler_px_per_cm"] * 10
        groups.append({
            "line_center_rows_px": center_rows,
            "adjacent_intervals_px": gaps,
            "mean_interval_px": pitch_px,
            "approx_pitch_mm": round(pitch_mm, 3),
        })
        interval_values.extend(gaps)

    return {
        "fragment_id": item["fragment_id"],
        "path": item["path"],
        "source_url": item["source_url"],
        "sha256": sha,
        "image_dimensions": dimensions,
        "region_xywh": item["region_xywh"],
        "ruler_calibration": item["ruler_calibration"],
        "ruler_px_per_cm": item["ruler_px_per_cm"],
        "staff_groups": groups,
        "aggregate_adjacent_interval_px": round(mean(interval_values), 3),
        "aggregate_approx_pitch_mm": round(mean(interval_values) / item["ruler_px_per_cm"] * 10, 3),
        "measurement_uncertainty": "Approximate manual center selection (about ±1 px per line); ruler endpoints are manual readings from the numbered 20 cm marks (about ±2 px). Perspective, local parchment deformation, red-rule waviness and image capture geometry are not corrected.",
    }


def main() -> None:
    md5 = digest(CSV_PATH, "md5")
    sha256 = digest(CSV_PATH, "sha256")
    if md5 != EXPECTED_CSV_MD5 or sha256 != EXPECTED_CSV_SHA256:
        raise ValueError("Pinned MPO CSV checksum differs from the research receipt")

    with CSV_PATH.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    q4 = [r for r in rows if r.get("notation", "").strip().lower().startswith("quad")
          and r.get("notenlinien", "").strip() == "4"]
    q4_11 = [r for r in q4 if r.get("zeilenzahl1", "").strip() == "#11"]
    q4_11_dimensioned = [r for r in q4_11 if parse_dimensions(r.get("schriftraum1", ""))]
    target_signatures = {"8994", "10370", "10406", "10407", "10437"}
    targets = [r for r in rows if r.get("codex") == "Codex 1505"
               and r.get("signatur") in target_signatures]
    if {r["signatur"] for r in targets} != target_signatures:
        raise ValueError("Expected Codex 1505 target records missing from the pinned CSV")

    target_dimensions = [parse_dimensions(r["schriftraum1"]) for r in targets]
    target_widths = [d[0] for d in target_dimensions if d]
    target_heights = [d[1] for d in target_dimensions if d]
    exact_box = (min(target_widths), max(target_widths), min(target_heights), max(target_heights))

    def other_matches(box: tuple[float, float, float, float]) -> list[dict]:
        w0, w1, h0, h1 = box
        matches = []
        for r in q4_11_dimensioned:
            if r.get("codex") == "Codex 1505":
                continue
            dims = parse_dimensions(r.get("schriftraum1", ""))
            if dims and w0 <= dims[0] <= w1 and h0 <= dims[1] <= h1:
                matches.append({
                    "signatur": r["signatur"],
                    "codex": r.get("codex", ""),
                    "written_area_cm": list(dims),
                    "content_excerpt": r.get("inhalt", "")[:180],
                })
        return matches

    exact_matches = other_matches(exact_box)
    relaxed_box = (exact_box[0] - 1.0, exact_box[1] + 1.0,
                   exact_box[2] - 1.0, exact_box[3] + 1.0)
    relaxed_matches = other_matches(relaxed_box)

    image_inputs = [
        {
            "fragment_id": "mpo-10370",
            "path": "data/images/mpo-10370-capture-3-1728px.jpg",
            "source_url": "https://lbiiif.riksarkivet.se/v3/arkis!R1010370_00003/full/1728,/0/default.jpg",
            "sha256": "b1258668d90ca011960ab4ff85f25fb79c0c3c636ad626ceb4fa90af8f6de28b",
            "image_dimensions": [1728, 1233],
            "region_xywh": [350, 400, 1155, 260],
            "ruler_calibration": {
                "axis": "vertical image axis; left-hand photographic ruler",
                "label_span_cm": 20,
                "endpoint_centers_px": [86, 1077],
                "label_order": [0, 20],
                "coordinate_origin": "top-left of source JPEG",
            },
            "ruler_px_per_cm": abs(1077 - 86) / 20,
            "staff_line_center_rows_px": [[407, 434, 462, 490], [566, 594, 622, 650]],
        },
        {
            "fragment_id": "mpo-10406",
            "path": "data/images/mpo-10406-capture-4.jpg",
            "source_url": "https://lbiiif.riksarkivet.se/v3/arkis!R1010406_00004/full/1000,/0/default.jpg",
            "sha256": "eb77ec83d785842e929432be99d99b579fce102d062d0ecdebe280dbdf9f6677",
            "image_dimensions": [1000, 647],
            "region_xywh": [225, 145, 650, 255],
            "ruler_calibration": {
                "axis": "vertical image axis; right-hand photographic ruler",
                "label_span_cm": 20,
                "endpoint_centers_px": [51, 600],
                "label_order": [20, 0],
                "coordinate_origin": "top-left of source JPEG",
            },
            "ruler_px_per_cm": abs(600 - 51) / 20,
            "staff_line_center_rows_px": [[153, 168, 184, 199], [244, 258, 274, 290], [337, 353, 368, 383]],
        },
    ]
    measured = [measure_staff_pitch(item) for item in image_inputs]

    result = {
        "version": "1.0.0",
        "assessment_date": "2026-10-24",
        "purpose": "Exploratory same-layout consistency check for the existing Codex 1505 Fr10370/Fr10406 association, with a whole-MPO metadata screen for how exclusive that layout description is.",
        "dataset": {
            "source": "https://zenodo.org/records/17287665",
            "version": "1.0.0",
            "path": "research/mpo.csv",
            "md5": md5,
            "sha256": sha256,
            "rows": len(rows),
            "independent_source_note": "This is the source catalogue that already supplies the Codex 1505 grouping; its metadata screen is not independent confirmation of that grouping.",
        },
        "selection_protocol": {
            "status": "post-inspection exploratory; not preregistered or blind",
            "image_measure": "Mean vertical interval between manually selected centers of four visible red staff rules in two clear Fr10370 systems and three Fr10406 systems, scaled by the vertical metric ruler photographed in the same image.",
            "catalogue_screen": "Exact case-insensitive Quadr prefix, notenlinien exactly '4', zeilenzahl1 exactly '#11'. Parse the first numeric written-area width x height from schriftraum1. Compare the full-record min-max dimensions across the five recorded Codex1505 items (and a ±1 cm sensitivity box). Exclude records labelled Codex1505 from comparison counts.",
            "image_centers_and_ruler_endpoints": "Coordinates were selected after visual inspection. The script records all exact coordinates and source hashes; it reproduces arithmetic, not the human coordinate judgment.",
        },
        "staff_pitch_measurements": measured,
        "catalogue_layout_screen": {
            "exact_rule": "notation starts with 'Quadr'; notenlinien='4'",
            "quadrature_four_line_records": len(q4),
            "with_main_text_rows_11": len(q4_11),
            "of_those_with_parseable_written_area": len(q4_11_dimensioned),
            "codex1505_signatures": sorted(target_signatures),
            "codex1505_dimensions_cm": [
                {"signatur": r["signatur"], "written_area": list(parse_dimensions(r["schriftraum1"])),
                 "fragment_size": r.get("format", ""), "text_rows": r.get("zeilenzahl1", ""),
                 "notation": r.get("notation", ""), "staff_lines": r.get("notenlinien", "")}
                for r in sorted(targets, key=lambda r: int(r["signatur"]))
            ],
            "exact_target_written_area_box_cm": list(exact_box),
            "other_records_inside_exact_box": exact_matches,
            "exact_box_other_record_count": len(exact_matches),
            "relaxed_target_box_cm_plus_minus_1": list(relaxed_box),
            "other_records_inside_relaxed_box": relaxed_matches,
            "relaxed_box_other_record_count": len(relaxed_matches),
            "published_different_book_control": {
                "signatures": ["8201", "8304"],
                "catalogue_fields": "Both are Codex1146, #12 main-text rows, written area 32.0 x 21.0 cm, notation 'Got', and uncertain four-line count; source notes describe three black and one red staff line.",
                "role": "A published same-hand/different-book comparison from the existing ornament dossier; it is not a like-for-like Quadr / four-red-rule control and is not counted in the Quadr metadata screen.",
            },
        },
        "interpretation": {
            "observed": "The measured Fr10370 and Fr10406 staff pitches are both approximately 5.6 mm in these selected systems, a strong descriptive consistency between two fragments already catalogued as Codex1505. The catalogue also gives them 11 main-text rows, four-line Quadr notation and very similar written-area dimensions.",
            "counterevidence": "Four-line Quadr notation is widespread in the full MPO export. Among the 197 records with that notation and 11 main-text rows, 149 have a parseable written-area dimension; three other records fall inside the exact target group's dimensional bounding box, and ten fall inside a ±1 cm sensitivity box. Fr1385, already a documented comparator, is one exact-box match.",
            "conclusion": "Consistent with the pre-existing Codex1505 association; not a new attribution, not proof of a shared codex, and not a unique layout fingerprint. A better-matched image control and broader measurement sampling would be needed to claim this signal discriminates books.",
        },
        "limits": [
            "The selected image systems were chosen after viewing the sources; no blind selection or measurement repeatability study was done.",
            "The pixel-to-millimeter values are approximate and assume the photographic ruler and parchment share the local scale; perspective, waviness and parchment deformation are uncorrected.",
            "The full MPO metadata is incomplete and its records are not a random sample. Dimensions are catalogue fields, not remeasured in this screen.",
            "The written-area range was derived from the five already grouped Codex1505 records; this is a descriptive retrieval screen, not a preregistered rarity test.",
            "No technical or catalogue result independently verifies the existing Codex1505 grouping."
        ],
    }
    out = OUT / "ruling_pitch_results.json"
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({
        "output": str(out.relative_to(ROOT)),
        "rows": len(rows),
        "quadrature_four_line": len(q4),
        "quadrature_four_line_11_rows": len(q4_11),
        "dimensioned_subset": len(q4_11_dimensioned),
        "exact_box_other_records": len(exact_matches),
        "relaxed_box_other_records": len(relaxed_matches),
        "measured_pitch_mm": {m["fragment_id"]: m["aggregate_approx_pitch_mm"] for m in measured},
    }, indent=2))


if __name__ == "__main__":
    main()
