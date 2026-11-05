"""Inventory explicit Finnish shelfmarks in the pinned BOMPAC workbook.

The workbook is research metadata, not a complete institutional catalogue.
This test is case-insensitive and matches shelfmark syntax only in three named
fields. It does not equate rows, folios, and medieval books.
"""
from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from pathlib import Path

from openpyxl import load_workbook

ROOT = Path(__file__).resolve().parents[2]
BOOK = ROOT / "research/continuation_26/bompac/Stockholm-Helsinki-Frs-Combined-BOMPAC.xlsx"
OUT = ROOT / "research/continuation_82/workbook_inventory.json"
FIELDS = ("Fr_reference", "FM_signum", "FM_signum_BOMPAC")
# Capture optional b explicitly: IIb is distinct from the II gradual series.
MARK = re.compile(r"(?<![A-Za-z0-9])F\.?M\.?\s*\.?\s*(IIb|II|IV)\.?\s*(\d+)(?!\d)", re.I)


def main() -> None:
    payload = BOOK.read_bytes()
    md5 = hashlib.md5(payload).hexdigest()
    if md5 != "ae9572cd4df5e5bccc241e8423ddf0c1":
        raise ValueError("Published BOMPAC workbook checksum mismatch")
    book = load_workbook(BOOK, read_only=True, data_only=True)
    sheet = book["Sheet1"]
    headers = next(sheet.iter_rows(min_row=2, max_row=2, values_only=True))
    if any(field not in headers for field in FIELDS):
        raise ValueError("Expected shelfmark columns missing")
    counts: dict[str, Counter[int]] = {x: Counter() for x in ("ii", "iib", "iv")}
    per_field: dict[str, Counter[str]] = {field: Counter() for field in FIELDS}
    numbers_by_field: dict[str, dict[str, set[int]]] = {
        field: {series: set() for series in counts} for field in FIELDS
    }
    hits = []
    rows_total = 0
    for line, values in enumerate(sheet.iter_rows(min_row=3, values_only=True), 3):
        row = dict(zip(headers, values))
        rows_total += 1
        for field in FIELDS:
            value = str(row.get(field) or "")
            for m in MARK.finditer(value):
                series, number = m.group(1).lower(), int(m.group(2))
                counts[series][number] += 1
                per_field[field][series] += 1
                numbers_by_field[field][series].add(number)
                if (series, number) in (("ii", 129), ("ii", 157), ("iib", 7), ("iv", 157)):
                    hits.append({"sheet_row": line, "field": field, "literal": m.group(0),
                                 "cell_value": value, "fragment_reference": row.get("Fr_reference"),
                                 "row_exclusion": row.get("Row_exclusion")})
    book.close()
    ii = set(counts["ii"])
    result = {
        "source": "research/continuation_26/bompac/Stockholm-Helsinki-Frs-Combined-BOMPAC.xlsx",
        "doi": "https://doi.org/10.5281/zenodo.17511106",
        "published_md5_verified": md5,
        "sha256": hashlib.sha256(payload).hexdigest(),
        "sheet": "Sheet1", "header_row": 2, "data_rows_scanned": rows_total,
        "row_filter": "none; included and excluded rows scanned separately from their exclusion status",
        "fields_scanned": list(FIELDS), "pattern": MARK.pattern,
        "matching_cell_occurrences_by_field": {k: dict(v) for k, v in per_field.items()},
        "distinct_numbers_by_field": {
            field: {series: sorted(numbers) for series, numbers in groups.items()}
            for field, groups in numbers_by_field.items()
        },
        "distinct_numbers": {series: sorted(counter) for series, counter in counts.items()},
        "ii_missing_from_1_to_129": sorted(set(range(1, 130)) - ii),
        "ii_numbers_above_129": sorted(n for n in ii if n > 129),
        "target_control_hits": hits,
        "interpretation_limit": "A three-column research-workbook scan is not an exhaustive current or historical catalogue. Variants outside the pattern or columns can be missed; a missing row does not prove nonexistence.",
    }
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"rows": rows_total, "ii_distinct": len(ii), "ii_min": min(ii),
                      "ii_max": max(ii), "missing_1_to_129": result["ii_missing_from_1_to_129"],
                      "ii157_matches": counts["ii"].get(157, 0),
                      "iib_numbers": sorted(counts["iib"]),
                      "iv157_matches": counts["iv"].get(157, 0), "output": str(OUT.relative_to(ROOT))}))


if __name__ == "__main__":
    main()
