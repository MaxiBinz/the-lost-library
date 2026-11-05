"""Extend the published BOMPAC crosswalk to the H08–H10 model suggestions.

This read-only query uses the already downloaded CC BY 4.0 workbooks. It does
not treat workbook reconstruction IDs as fresh image evidence or ground truth.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from openpyxl import load_workbook


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "research/continuation_26/bompac"
OUT = Path(__file__).resolve().parent / "bompac_suggestion_crosswalk_results.json"
QUEUE_SHA256 = "b3e299a7c600584ce44518db1f5c30c3301edae0a07a8b009075498f64ccec47"
EXPECTED_MD5 = {
    "Stockholm-Helsinki-Frs-Combined-BOMPAC.xlsx": "ae9572cd4df5e5bccc241e8423ddf0c1",
    "MPO_BOMPAC.xlsx": "6aaea1e3ba1a60355dfb6c649fc7baff",
}
TARGETS = {
    "Fr 1385": "mpo-1385",
    "Fr 4223": "mpo-4223",
    "Fr 8311": "mpo-8311",
    "Fr 8455": "mpo-8455",
}
PAIRS = {
    "H08": ("mpo-1385", "mpo-4223"),
    "H09": ("mpo-1385", "mpo-8311"),
    "H10": ("mpo-1385", "mpo-8455"),
}


def workbook_rows(path: Path, sheet_name: str) -> list[dict]:
    wb = load_workbook(path, read_only=True, data_only=True)
    try:
        sheet = wb[sheet_name]
        headers = [sheet.cell(2, col).value for col in range(1, sheet.max_column + 1)]
        return [dict(zip(headers, values)) for values in sheet.iter_rows(min_row=3, values_only=True)]
    finally:
        wb.close()


def receipt(path: Path, expected_md5: str) -> dict:
    data = path.read_bytes()
    md5 = hashlib.md5(data).hexdigest()
    if md5 != expected_md5:
        raise ValueError(f"Published MD5 mismatch for {path.name}: {md5}")
    return {"filename": path.name, "bytes": len(data), "md5": md5,
            "sha256": hashlib.sha256(data).hexdigest()}


def main() -> None:
    queue_path = ROOT / "data/hypotheses.v1.json"
    queue_sha = hashlib.sha256(queue_path.read_bytes()).hexdigest()
    if queue_sha != QUEUE_SHA256:
        raise ValueError("Frozen hypothesis queue changed")

    combined_path = SOURCE / "Stockholm-Helsinki-Frs-Combined-BOMPAC.xlsx"
    raw_path = SOURCE / "raw_metadata/MPO_BOMPAC.xlsx"
    receipts = {
        "combined_workbook": receipt(combined_path, EXPECTED_MD5[combined_path.name]),
        "raw_mpo_workbook": receipt(raw_path, EXPECTED_MD5[raw_path.name]),
    }

    combined_rows = workbook_rows(combined_path, "Sheet1")
    included = [row for row in combined_rows if row.get("Row_exclusion") == "Include row"]
    selected = [row for row in included if row.get("Fr_reference") in TARGETS]
    if {row.get("Fr_reference") for row in selected} != set(TARGETS):
        raise ValueError("Expected target references missing from combined BOMPAC workbook")
    combined_fields = [
        "Fr_reference", "BOMPAC-reconstruction", "Frs_per_unit", "Fr_in_unit",
        "CCM_signum_BOMPAC", "Codex_signum_BOMPAC", "FM_signum_BOMPAC",
        "Category", "Genre", "Rows", "Notation_type", "Notation_lines", "Row_exclusion",
    ]
    combined_records = [{key: row.get(key) for key in combined_fields} for row in selected]
    combined_units = {}
    for unit in sorted({row.get("BOMPAC-reconstruction") for row in selected}):
        members = [row for row in included if row.get("BOMPAC-reconstruction") == unit]
        combined_units[unit] = {
            "included_row_count": len(members),
            "target_members": sorted(row.get("Fr_reference") for row in members
                                      if row.get("Fr_reference") in TARGETS),
        }

    raw_rows = workbook_rows(raw_path, "Blad1")
    raw_ids = {reference.removeprefix("Fr ") for reference in TARGETS}
    raw_selected = [row for row in raw_rows if str(row.get("fragment_id")) in raw_ids]
    if {str(row.get("fragment_id")) for row in raw_selected} != raw_ids:
        raise ValueError("Expected target references missing from raw MPO workbook")
    raw_fields = ["fragment_id", "unit_HK", "frs_per_unit_HK", "fr_in_unit_IDX_HK",
                  "ccmsignum_HK", "codex_HK", "sachtitel", "datierung", "entstehungsort",
                  "inhalt", "Row_exclusion"]
    raw_records = [{key: row.get(key) for key in raw_fields if key in row} for row in raw_selected]
    raw_units = {}
    for unit in sorted({row.get("unit_HK") for row in raw_selected if row.get("unit_HK")}):
        members = [row for row in raw_rows if row.get("unit_HK") == unit]
        raw_units[unit] = {
            "row_count": len(members),
            "fragment_ids": [row.get("fragment_id") for row in members],
        }

    queue = json.loads(queue_path.read_text(encoding="utf-8"))["hypotheses"]
    queue_pairs = {row["id"]: (row["left_id"], row["right_id"]) for row in queue}
    for ident, pair in PAIRS.items():
        if queue_pairs.get(ident) != pair:
            raise ValueError(f"Frozen pair changed: {ident}")
    match_rows = json.loads((ROOT / "data/matches.json").read_text(encoding="utf-8"))
    scores = {}
    for ident, pair in PAIRS.items():
        row = next((item for item in match_rows
                    if (item.get("left_id"), item.get("right_id")) == pair), None)
        if row is None:
            raise ValueError(f"Missing baseline candidate: {ident}")
        scores[ident] = {key: row.get(key) for key in ("rank", "method", "score", "scores")}

    result = {
        "date": "2026-10-25",
        "question": "Do published BOMPAC reconstruction assignments already separate the H08–H10 Fr 1385 model suggestions from their anchor?",
        "source_records": [
            {"doi": "10.5281/zenodo.17511106", "license": "CC BY 4.0", "workbook": receipts["combined_workbook"]},
            {"doi": "10.5281/zenodo.17701360", "license": "CC BY 4.0", "workbook": receipts["raw_mpo_workbook"]},
        ],
        "queue_sha256": queue_sha,
        "method": {
            "parser": "openpyxl read_only=True, data_only=True; headers on row 2; records from row 3",
            "combined_sheet": "Sheet1; included rows only where Row_exclusion == 'Include row'",
            "raw_sheet": "Blad1; exact numeric fragment_id values",
            "query_references": sorted(TARGETS),
            "images_downloaded": 0,
            "queue_or_model_changed": False,
        },
        "combined_dataset": {"records": combined_records, "units": combined_units},
        "raw_mpo_dataset": {"records": raw_records, "units": raw_units},
        "existing_model_candidates": scores,
        "interpretation": {
            "supported": [
                "The combined workbook places Fr 4223, Fr 8311 and Fr 8455 in BOMPAC-258 (Ant-39/Codex-1200/FM.IV.159), with Fr 1385 in BOMPAC-912 (Ant-99/FM.IV.157).",
                "The raw MPO workbook groups Fr 4223, Fr 8311 and Fr 8455 in C-17/Codex-1200 and lists Fr 1385 as singleton F-1385.",
                "All three model suggestions are high-scoring, correlated lookalikes whose published reconstruction assignments differ from the anchor's assignment.",
            ],
            "not_established": [
                "Workbook unit assignments are prior reconstruction data, not fresh image-based proof or independent expert adjudication.",
                "Separate reconstruction units do not prove physical incompatibility, different hand, or absence of a broader production relationship.",
                "The workbook sources are related BOMPAC datasets, not independent corroborating studies.",
                "No case is rejected, no hypothesis category changes, and no novel attribution or method is established by this crosswalk.",
            ],
        },
    }
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(OUT.relative_to(ROOT)), "checksums_verified": len(receipts),
                      "candidate_rows": len(combined_records), "combined_units": combined_units,
                      "raw_units": {key: value["row_count"] for key, value in raw_units.items()},
                      "queue_sha256": queue_sha}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
