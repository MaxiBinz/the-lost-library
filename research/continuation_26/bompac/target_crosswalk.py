"""Reproduce the target-row BOMPAC crosswalk from the deposited workbooks.

Read-only analysis. Uses openpyxl in read-only mode and writes only the local
machine-readable result beside the source files.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from openpyxl import load_workbook


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SOURCES = {
    "combined_workbook": {
        "path": HERE / "Stockholm-Helsinki-Frs-Combined-BOMPAC.xlsx",
        "published_md5": "ae9572cd4df5e5bccc241e8423ddf0c1",
        "doi": "10.5281/zenodo.17511106",
    },
    "combined_readme": {
        "path": HERE / "Readme-Sto-Hel-Frs-Combined-BOMPAC.pdf",
        "published_md5": "277c9e39fa987139607f76ed2f3168e6",
        "doi": "10.5281/zenodo.17511106",
    },
    "raw_mpo_workbook": {
        "path": HERE / "raw_metadata/MPO_BOMPAC.xlsx",
        "published_md5": "6aaea1e3ba1a60355dfb6c649fc7baff",
        "doi": "10.5281/zenodo.17701360",
    },
    "raw_readme": {
        "path": HERE / "raw_metadata/Readme-Raw-Metadata-BOMPAC.pdf",
        "published_md5": "cbde32835ab0acc379117354cdf06c4b",
        "doi": "10.5281/zenodo.17701360",
    },
    "kaasik_commentary": {
        "path": HERE / "raw_metadata/MPO_commentary_Holger_Kaasik.pdf",
        "published_md5": "38cd079e03c0030cbccfefe5dd2436a5",
        "doi": "10.5281/zenodo.17701360",
    },
}
TARGETS = {
    "Fr 1385", "Fr 8994", "Fr 10370", "Fr 10406", "Fr 10407",
    "Fr 10437", "Fr 20274", "Fr 20275", "Fr 20276", "Fr 20277",
    "Fr 20278",
}


def file_receipt(path: Path, expected_md5: str) -> dict:
    raw = path.read_bytes()
    md5 = hashlib.md5(raw).hexdigest()
    if md5 != expected_md5:
        raise ValueError(f"Published MD5 mismatch for {path.name}: {md5}")
    return {
        "filename": path.name,
        "bytes": len(raw),
        "md5": md5,
        "sha256": hashlib.sha256(raw).hexdigest(),
    }


def workbook_rows(path: Path, sheet_name: str):
    book = load_workbook(path, read_only=True, data_only=True)
    sheet = book[sheet_name]
    headers = [sheet.cell(2, col).value for col in range(1, sheet.max_column + 1)]
    for values in sheet.iter_rows(min_row=3, values_only=True):
        yield dict(zip(headers, values))
    book.close()


def main() -> None:
    receipts = {
        key: {**{k: v for k, v in item.items() if k != "path"},
              **file_receipt(item["path"], item["published_md5"])}
        for key, item in SOURCES.items()
    }

    combined_rows = list(workbook_rows(SOURCES["combined_workbook"]["path"], "Sheet1"))
    included = [r for r in combined_rows if r.get("Row_exclusion") == "Include row"]
    selected = [r for r in included if r.get("Fr_reference") in TARGETS]
    selected.sort(key=lambda r: r["Fr_reference"])
    combined_fields = [
        "Fr_reference", "Database_or_institution", "BOMPAC-reconstruction",
        "Frs_per_unit", "Fr_in_unit", "CCM_signum_BOMPAC",
        "Codex_signum_BOMPAC", "FM_signum_BOMPAC", "Category",
        "Genre", "Type_hierarchy_1", "Dating_BOMPAC", "Written_area_height_1",
        "Written_area_width_1", "Rows", "Notation_type", "Notation_lines",
        "Identification_comment", "Row_exclusion", "Exclusion_criteria",
    ]
    selected_records = [{k: r.get(k) for k in combined_fields} for r in selected]
    combined_unit_ids = sorted({r["BOMPAC-reconstruction"] for r in selected})
    combined_units = {}
    for unit_id in combined_unit_ids:
        members = [r for r in included if r.get("BOMPAC-reconstruction") == unit_id]
        combined_units[unit_id] = {
            "included_row_count": len(members),
            "members": [r.get("Fr_reference") for r in members],
            "target_member_rows": [r["Fr_reference"] for r in members
                                   if r.get("Fr_reference") in TARGETS],
        }

    raw_rows = list(workbook_rows(SOURCES["raw_mpo_workbook"]["path"], "Blad1"))
    raw_target_rows = [r for r in raw_rows
                       if str(r.get("fragment_id")) in {"1385", "8994", "10370",
                                                       "10406", "10407", "10437",
                                                       "20274", "20275", "20276",
                                                       "20277", "20278"}]
    raw_target_rows.sort(key=lambda r: int(r["fragment_id"]))
    raw_fields = [
        "fragment_id", "unit_HK", "unit_NB_HK", "frs_per_unit_HK",
        "fr_in_unit_IDX_HK", "ccmsignum_HK", "codex_HK",
        "ccmsignum_HK_ambivalence-MPO", "codex_HK_ambivalence-MPO",
        "ccmsignum_HK_ambivalence-HK", "codex_HK_ambivalence-HK",
        "ccmsignum_HK_correction_log", "codex_HK_correction_log",
        "signum_comments_HK", "general_notes_HK", "schrift", "notation",
        "notenlinien", "zeilenzahl1", "schriftraum1", "inhalt", "anmerkungen",
        "literatur", "Row_exclusion",
    ]
    raw_units = sorted({r.get("unit_HK") for r in raw_target_rows if r.get("unit_HK")})
    raw_groups = {}
    for unit_id in raw_units:
        members = [r for r in raw_rows if r.get("unit_HK") == unit_id]
        raw_groups[unit_id] = {
            "row_count": len(members),
            "fragment_ids": [r.get("fragment_id") for r in members],
        }

    result = {
        "date": "2026-10-24",
        "question": "What do the published BOMPAC datasets assign to the target MPO/FM fragments?",
        "source_records": [
            {"doi": "10.5281/zenodo.17511106", "license": "CC BY 4.0"},
            {"doi": "10.5281/zenodo.17701360", "license": "CC BY 4.0"},
        ],
        "sources": receipts,
        "method": {
            "parser": "openpyxl read_only=True, data_only=True; headers read from row 2; data begins row 3",
            "combined_sheet": "Sheet1",
            "combined_row_filter": "Row_exclusion == 'Include row'",
            "raw_sheet": "Blad1",
            "raw_query": "exact numeric fragment_id values for the listed MPO records",
            "no_images_or_model_scores_used": True,
        },
        "combined_dataset": {
            "sheet_dimensions_including_header_rows": [29588, 69],
            "target_records": selected_records,
            "target_reconstruction_units": combined_units,
        },
        "raw_mpo_dataset": {
            "target_records": [{k: r.get(k) for k in raw_fields} for r in raw_target_rows],
            "target_unit_membership": raw_groups,
        },
        "interpretation": {
            "supported": [
                "The combined BOMPAC workbook assigns Fr 8994 and the other listed Codex 1505 fragments plus FM.IV.156 records to BOMPAC-5324.",
                "The combined BOMPAC workbook assigns Fr 1385 and Fr 20274-20278 plus FM.IV.157 records to BOMPAC-912.",
                "The raw MPO workbook groups Fr 8994, 10370, 10406, 10407 and 10437 together as M-1217/Codex 1505; it groups Fr 20274-20278 as C-35/Ant-99 and keeps Fr 1385 in singleton unit F-1385.",
            ],
            "not_established": [
                "The spreadsheet rows are not fresh image-based proof or independent expert review.",
                "Separate reconstruction IDs do not by themselves prove that the physical fragments cannot have a more complex historical relationship.",
                "No new attribution, exclusion, hand identification, catalogue error, or scientific novelty is established by this query alone.",
            ],
            "research_consequence": "Target-level dataset assignments are now established prior work. Any new claim must specify and test evidence beyond reproducing these row groupings.",
        },
    }
    out = HERE / "target_crosswalk_results.json"
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    receipt = {
        "date": "2026-10-24",
        "source": "Official Zenodo records 17511106 and 17701360; five deposited files fetched and checked against their published MD5 values.",
        "license": "CC BY 4.0 as recorded in Zenodo metadata",
        "files": receipts,
        "downloaded_bytes": sum(item["bytes"] for item in receipts.values()),
        "working_source_image_files_added": 0,
    }
    (HERE / "download_receipt.json").write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(out.relative_to(ROOT)),
        "receipt": str((HERE / "download_receipt.json").relative_to(ROOT)),
        "checksums_verified": len(receipts),
        "selected_target_rows": len(selected_records),
        "combined_units": {k: v["included_row_count"] for k, v in combined_units.items()},
        "raw_target_units": {k: v["row_count"] for k, v in raw_groups.items()},
    }, indent=2))


if __name__ == "__main__":
    main()
