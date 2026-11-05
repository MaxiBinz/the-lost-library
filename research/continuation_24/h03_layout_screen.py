#!/usr/bin/env python3
"""Reproducible metadata-layout sensitivity screen for frozen hypothesis H03."""
from __future__ import annotations

import csv
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CSV_PATH = ROOT / "research/mpo.csv"
EXPECTED_CSV_SHA256 = "f5d2825703be19fd1994bc0b91724c32c67c36535622d5554c37b4029592d00b"
CANDIDATE_IDS = {"8994", "20274"}


def parse_area(value: str | None) -> tuple[float, float] | None:
    match = re.search(r"(\d+(?:[.,]\d+)?)\s*[x×]\s*(\d+(?:[.,]\d+)?)", value or "", re.I)
    if not match:
        return None
    return tuple(float(part.replace(",", ".")) for part in match.groups())


def first_row_count(value: str | None) -> int | None:
    match = re.match(r"\s*#?\s*(\d+)", value or "")
    return int(match.group(1)) if match else None


def record_stub(row: dict[str, str], area: tuple[float, float]) -> dict:
    return {
        "signatur": row["signatur"],
        "codex": row.get("codex", ""),
        "type": row.get("sachtitel", ""),
        "written_area_cm": list(area),
        "main_text_rows_literal": row.get("zeilenzahl1", ""),
        "script": row.get("schrift", ""),
        "content_excerpt": (row.get("inhalt", "") or "")[:120],
    }


def main() -> dict:
    csv_sha256 = hashlib.sha256(CSV_PATH.read_bytes()).hexdigest()
    if csv_sha256 != EXPECTED_CSV_SHA256:
        raise SystemExit(f"Pinned MPO CSV hash mismatch: {csv_sha256}")
    with CSV_PATH.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))

    by_id = {row["signatur"]: row for row in rows}
    if not CANDIDATE_IDS <= by_id.keys():
        raise SystemExit("H03 candidate records missing from pinned MPO export")
    candidate = {key: parse_area(by_id[key].get("schriftraum1")) for key in sorted(CANDIDATE_IDS)}
    if candidate != {"20274": (36.0, 22.5), "8994": (35.5, 22.5)}:
        raise SystemExit(f"H03 catalogue dimensions changed: {candidate}")

    cohort = []
    for row in rows:
        if not (row.get("notation", "").strip().lower().startswith("quadr") and
                row.get("notenlinien", "").strip() == "4" and
                first_row_count(row.get("zeilenzahl1")) == 11):
            continue
        area = parse_area(row.get("schriftraum1"))
        cohort.append((row, area))

    dimensioned = [(row, area) for row, area in cohort if area is not None]
    antiphonaria = [(row, area) for row, area in cohort
                    if row.get("sachtitel", "").strip().lower() == "antiphonarium"]
    antiphonaria_dimensioned = [(row, area) for row, area in antiphonaria if area is not None]
    pair_areas = list(candidate.values())
    low = [min(area[axis] for area in pair_areas) for axis in range(2)]
    high = [max(area[axis] for area in pair_areas) for axis in range(2)]

    def get_sensitivities(selected):
        results = []
        for tolerance in (0.0, 0.5, 1.0):
            matches = []
            for row, area in selected:
                if all(low[axis] - tolerance <= area[axis] <= high[axis] + tolerance
                       for axis in range(2)):
                    matches.append(record_stub(row, area))
            results.append({
                "tolerance_cm_beyond_candidate_pair_bbox": tolerance,
                "bbox_cm": {
                    "written_width": [low[0] - tolerance, high[0] + tolerance],
                    "written_height": [low[1] - tolerance, high[1] + tolerance],
                },
                "match_count": len(matches),
                "candidate_pair_included": sorted(CANDIDATE_IDS & {m["signatur"] for m in matches}),
                "matches": matches,
            })
        return results

    sensitivities = get_sensitivities(dimensioned)
    antiphonaria_sensitivities = get_sensitivities(antiphonaria_dimensioned)

    fragments = json.loads((ROOT / "data/fragments.json").read_text())
    fragment_by_signatur = {item["raw"]["signatur"]: item for item in fragments
                            if item.get("raw", {}).get("signatur")}
    records = {key: fragment_by_signatur[key] for key in CANDIDATE_IDS}
    pair_details = {}
    for signature, record in records.items():
        pair_details[signature] = {
            "catalogue_record": {key: record["raw"].get(key) for key in (
                "sachtitel", "datierung", "format", "schriftraum1", "zeilenzahl1",
                "notation", "notenlinien", "schrift", "codex", "inhalt")},
            "record_sha256": hashlib.sha256(json.dumps(record, sort_keys=True,
                                                         ensure_ascii=False).encode()).hexdigest(),
        }

    review = json.loads((ROOT / "data/hypothesis_reviews.v1.json").read_text())
    result = {
        "version": "1.0.0",
        "date": "2026-10-24",
        "question": "How unusual are H03's nearly equal catalogued written-area dimensions among four-line Quadr records with 11 text rows?",
        "hypothesis_id": "H03",
        "frozen_queue_sha256": review["queue_sha256"],
        "source": {
            "path": "research/mpo.csv",
            "record_count": len(rows),
            "sha256": csv_sha256,
            "source_version": "MPO dataset 1.0.0",
            "source_url": "https://zenodo.org/records/17287665",
        },
        "selection": {
            "status": "post-inspection descriptive screen; not preregistered, blind, or an image measurement",
            "cohort_rule": "notation starts Quadr; notenlinien exactly 4; leading integer in zeilenzahl1 equals 11 (therefore includes both '#11' and '11 (33)')",
            "candidate_pair": ["mpo-8994", "mpo-20274"],
            "dimensions_source": "pinned MPO catalogue schriftraum1 field; recorded centimetre values, not remeasured pixels",
            "pair_record_details": pair_details,
        },
        "denominators": {
            "quadr4_11_row_cohort_records": len(cohort),
            "quadr4_11_row_cohort_records_with_parseable_written_area": len(dimensioned),
            "antiphonarium_subset_records": len(antiphonaria),
            "antiphonarium_subset_records_with_parseable_written_area": len(antiphonaria_dimensioned),
        },
        "candidate_bbox_cm": {
            "width": [low[0], high[0]],
            "height": [low[1], high[1]],
            "pair_width_difference_cm": high[0] - low[0],
            "pair_height_difference_cm": high[1] - low[1],
        },
        "sensitivity_results": sensitivities,
        "antiphonarium_sensitivity_results": antiphonaria_sensitivities,
        "interpretation": {
            "supports": "The pinned catalogue records closely similar written-area sizes for this already proposed H03 pair, consistent with a shared page-design tradition or possible common codex.",
            "limits": [
                "The metadata itself records Fr 8994 as Codex 1505 and supplies the existing comparison context; it is not independent physical evidence.",
                "The pair-defined exact box is post hoc and mechanically contains both candidates, so its two-record count is not a rarity statistic.",
                "Within the genre-matched Antiphonarium subset, the ±0.5 cm box also includes two Fragments labelled Codex 1306 and three other Codex 1505 leaves; close dimensions do not identify one codex.",
                "Only 154 of 244 catalogue records in the notation/row-count cohort have parseable written areas; within the Antiphonarium subset, only 52 of 97 do. Missingness is not random or quantified.",
                "Fr 20274 has no catalogue leaf format value and no script value, limiting direct codicological comparison.",
                "Catalogue dimensions are inherited descriptions, not independent ruler measurements of the displayed source images.",
                "This result does not establish or refute same-book, same-hand, workshop, or historical transmission claims.",
            ],
            "classification": "supportive compatibility only; H03 remains C/unresolved",
            "new_discovery": False,
            "new_source_downloads": False,
        },
    }
    output = ROOT / "research/continuation_24/h03_layout_results.json"
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({
        "hypothesis": "H03",
        "queue_sha256_unchanged": review["queue_sha256"],
        "cohort": len(cohort),
        "with_dimensions": len(dimensioned),
        "candidate_bbox_cm": result["candidate_bbox_cm"],
        "sensitivity_match_counts": [x["match_count"] for x in sensitivities],
        "antiphonarium_match_counts": [x["match_count"] for x in antiphonaria_sensitivities],
        "result": str(output.relative_to(ROOT)),
    }, indent=2))
    return result


if __name__ == "__main__":
    main()
