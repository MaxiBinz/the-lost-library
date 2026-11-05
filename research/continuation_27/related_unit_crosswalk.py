"""Reproduce the BOMPAC crosswalk for the IV.173-related fragment group.

This is a read-only query against the deposited combined workbook. It checks
the workbook's published checksum before selecting included rows. It does not
use image similarity or claim to adjudicate the historical attributions.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BOMPAC_DIR = ROOT / "research/continuation_26/bompac"
sys.path.insert(0, str(BOMPAC_DIR))

from target_crosswalk import SOURCES, file_receipt, workbook_rows  # noqa: E402


def main() -> None:
    combined_source = SOURCES["combined_workbook"]
    raw_source = SOURCES["raw_mpo_workbook"]
    receipts = {
        "combined_workbook": file_receipt(
            combined_source["path"], combined_source["published_md5"]
        ),
        "raw_mpo_workbook": file_receipt(
            raw_source["path"], raw_source["published_md5"]
        ),
    }

    rows = list(workbook_rows(combined_source["path"], "Sheet1"))
    included = [r for r in rows if r.get("Row_exclusion") == "Include row"]
    targets = {
        "Fr 1385", "Fr 8994", "Fr 20274", "Fr 25592", "Fr 29666",
        "F.m.IV.156, fol. 1", "F.m.IV.157, fol. 1", "F.m.IV.173, fol. 1",
    }
    fields = [
        "Fr_reference", "BOMPAC-reconstruction", "Frs_per_unit", "Fr_in_unit",
        "CCM_signum_BOMPAC", "FM_signum_BOMPAC", "Dating_BOMPAC",
        "Dating_BOMPAC_conflict", "Dating_start", "Dating_end",
        "Origin_BOMPAC_BOMPAC", "Type_hierarchy_1", "Notation_type",
        "Notation_lines", "Rows", "Row_exclusion", "Exclusion_criteria",
    ]
    selected = [r for r in included if r.get("Fr_reference") in targets]
    selected.sort(key=lambda r: str(r.get("Fr_reference")))

    units: dict[str, dict] = {}
    for unit_id in ("BOMPAC-912", "BOMPAC-9531", "BOMPAC-5324"):
        members = [r for r in included if r.get("BOMPAC-reconstruction") == unit_id]
        units[unit_id] = {
            "included_row_count": len(members),
            "members": [r.get("Fr_reference") for r in members],
            "selected_records": [
                {key: r.get(key) for key in fields}
                for r in members if r.get("Fr_reference") in targets
            ],
        }

    membership = {
        str(r.get("Fr_reference")): r.get("BOMPAC-reconstruction")
        for r in selected
    }
    assert membership.get("Fr 25592") == "BOMPAC-9531"
    assert membership.get("Fr 29666") == "BOMPAC-9531"
    assert membership.get("F.m.IV.173, fol. 1") == "BOMPAC-9531"
    assert membership.get("Fr 20274") == "BOMPAC-912"
    assert membership.get("F.m.IV.157, fol. 1") == "BOMPAC-912"
    assert membership.get("Fr 8994") == "BOMPAC-5324"
    assert len(units["BOMPAC-9531"]["members"]) == 3

    result = {
        "date": "2026-10-24",
        "question": "How does BOMPAC assign the IV.173 / Ant 242 / Hy 49 / Ant 99 related group?",
        "sources": {
            "combined_dataset": "https://doi.org/10.5281/zenodo.17511106",
            "raw_metadata": "https://doi.org/10.5281/zenodo.17701360",
            "fragmenta_iv173_record": "https://fragmenta.kansalliskirjasto.fi/handle/10024/1314",
            "fragmenta_iv157_record": "https://fragmenta.kansalliskirjasto.fi/handle/10024/1300",
        },
        "verified_workbook_checksums": receipts,
        "method": {
            "parser": "openpyxl read_only=True, data_only=True; row-2 headers; rows from 3",
            "included_row_filter": "Row_exclusion == 'Include row'",
            "image_or_model_score_used": False,
            "source_record_access": "Official Fragmenta indexed record and BOMPAC deposited workbooks; no Riksarkivet image acquired.",
        },
        "selected_records": [{key: r.get(key) for key in fields} for r in selected],
        "units": units,
        "source_claims": {
            "fragmenta_iv173_record": "The National Library record identifies CCM Ant 242 / Fr 29666 as from the same codex as F.m.IV.173, lists Fr 25592 / Hy 49 as also suggested, and names Ant 99 as also suggested with reference to Keskiaho 2010 and F.m.IV.157. The same record describes a broader group by shared style and Åbo-Dominican liturgical use.",
            "raw_mpo_fr29666_note": "The deposited MPO note says to compare Hy 49 and identifies Ant 242 / Fr 29666 as the same codex as Helsinki Ant 173, citing Taitto 2001 p. 185.",
            "bompac_result": "BOMPAC-9531 contains Fr 25592 / Hy 49, Fr 29666 / Ant 242, and F.m.IV.173, fol. 1. BOMPAC-912 contains Fr 1385, Ant 99 / Fr 20274-20278, and F.m.IV.157. BOMPAC-5324 contains Fr 8994 / Codex 1505 and F.m.IV.156.",
        },
        "interpretation": {
            "supported": [
                "The BOMPAC unit for IV.173 agrees with the explicit IV.173–Ant 242 / Fr 29666 same-codex assertion and also groups the previously suggested Hy 49 / Fr 25592 with them.",
                "BOMPAC assigns Ant 99 / F.m.IV.157 and IV.173 to different reconstruction units, despite the updated Fragmenta record listing Ant 99 as a suggestion associated with the broader group.",
                "The sources distinguish a broad stylistic/liturgical group, suggested relationships, and explicit same-codex claims; they should not be collapsed into one identity assertion.",
            ],
            "not_established": [
                "The BOMPAC unit split does not explain why the Ant 99 suggestion is absent from unit 9531 or independently settle the historical relation.",
                "No new same-book, same-hand, workshop, or physical-join finding is established by this metadata crosswalk.",
                "The selected source records and workbook rows are not independent image examinations or expert adjudications.",
            ],
            "research_consequence": "Revise H04/H05/H03 prior-art context to account for the third BOMPAC unit and the unresolved difference between the updated Fragmenta suggestions and the BOMPAC reconstruction. Keep the image-based questions open.",
        },
        "access_attempt": {
            "route": "https://sok.riksarkivet.se/MPO?FragmentID=29666&page=1&postid=Mpo_29666&tab=post",
            "result": "The ordinary archive page displayed a human-verification CAPTCHA.",
            "challenge_interacted_with_or_bypassed": False,
            "image_acquired": False,
        },
    }
    out = HERE / "related_unit_crosswalk_results.json"
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(out.relative_to(ROOT)),
        "checksums_verified": len(receipts),
        "selected_rows": len(selected),
        "unit_sizes": {key: value["included_row_count"] for key, value in units.items()},
        "membership": membership,
        "challenge_interaction": False,
    }, indent=2))


if __name__ == "__main__":
    main()
