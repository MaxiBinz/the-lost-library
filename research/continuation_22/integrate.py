"""Register E22's matched control and current prior-art checks.

The source remains an auxiliary comparator, outside the core collection,
baseline predictors and frozen ten-pair queue.
"""
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
QUEUE_SHA = "b3e299a7c600584ce44518db1f5c30c3301edae0a07a8b009075498f64ccec47"
PDM = "http://creativecommons.org/publicdomain/mark/1.0/"


def load(path):
    return json.loads((ROOT / path).read_text())


def write(path, value):
    (ROOT / path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def main():
    queue_path = ROOT / "data/hypotheses.v1.json"
    queue_hash = hashlib.sha256(queue_path.read_bytes()).hexdigest()
    if queue_hash != QUEUE_SHA:
        raise ValueError("The frozen ten-pair queue has changed")

    core = load("data/fragments.json")
    if "mpo-7292" in {r["id"] for r in core}:
        raise ValueError("The auxiliary control must not enter the core collection")

    result = load("research/continuation_22/matched_staff_results.json")
    receipt = load("research/continuation_22/image_receipt.json")
    manifest_path = ROOT / receipt["manifest_path"]
    manifest = json.loads(manifest_path.read_text())
    rights_values = []
    for item in manifest.get("metadata", []):
        if "Rights" in item.get("label", {}).get("en", []):
            rights_values.extend(item.get("value", {}).get("none", []))
    if PDM not in rights_values:
        raise ValueError("Official IIIF manifest does not give the expected Public Domain Mark")

    if receipt.get("higher_resolution_derivative", {}).get("sha256") != result["image"]["sha256"]:
        raise ValueError("E22 measurement image does not match the acquisition receipt")
    cap800 = {
        "path": receipt["saved_path"],
        "url": receipt["image_url"],
        "sha256": receipt["sha256"],
        "width": receipt["dimensions_px"][0],
        "height": receipt["dimensions_px"][1],
        "bytes": receipt["bytes_received"],
        "canvas_id": receipt["canvas_id"],
        "physical_object_id": "mpo-7292",
        "capture_index": 0,
        "resolution_variant": False,
        "label": "MPO manifest image 1, 800px derivative; capture order is not medieval side order",
        "rights_url": PDM,
    }
    hi = receipt["higher_resolution_derivative"]
    cap1600 = {
        "path": hi["saved_path"],
        "url": hi["image_url"],
        "sha256": hi["sha256"],
        "width": hi["dimensions_px"][0],
        "height": hi["dimensions_px"][1],
        "bytes": hi["bytes_received"],
        "canvas_id": receipt["canvas_id"],
        "physical_object_id": "mpo-7292",
        "capture_index": 0,
        "resolution_variant": True,
        "label": "MPO manifest image 1, 1600px derivative used for region coordinates; not a separate side",
        "rights_url": PDM,
    }
    metadata = {}
    with (ROOT / "research/mpo.csv").open(newline="", encoding="utf-8-sig") as f:
        row = next(r for r in csv.DictReader(f) if r["signatur"] == "7292")
    source_record = {
        "id": "mpo-7292",
        "physical_object_id": "mpo-7292",
        "shelfmark": "Fr 7292 (Swedish National Archives MPO)",
        "institution": "Swedish National Archives",
        "attribution": "Riksarkivet",
        "collection": "Medeltida pergamentomslag (MPO)",
        "role": "metadata-matched different-codex staff-pitch control; excluded from core predictors, benchmark and frozen attribution queue",
        "image_path": cap1600["path"],
        "image": cap1600,
        "captures": [cap800, cap1600],
        "source_url": "https://sok.riksarkivet.se/bildvisning/R1007292",
        "manifest_url": receipt["manifest_url"],
        "rights_url": PDM,
        "rights_label": "Public Domain Mark 1.0, recorded in the official Riksarkivet IIIF manifest",
        "normalized": {
            "type": row["sachtitel"],
            "date_text": row["datierung"],
            "material": row["beschreibstoff"],
            "contents": row["inhalt"],
            "notation": f"{row['notation']}, {row['notenlinien']} lines",
            "main_text_rows": row["zeilenzahl1"],
            "written_area": row["schriftraum1"],
            "catalogue_codex_label": row["codex"],
        },
        "warnings": [
            "Auxiliary comparison source only; not added to the 129-record core collection, matching gallery, predictors or frozen hypothesis queue.",
            "Codex 1306 is the MPO catalogue label, not independent expert adjudication.",
            "Selection was made from metadata before image retrieval; staff systems and line centers were selected after viewing the image.",
            "The single control matches broad layout metadata, not hand or workshop.",
            "Two JPEG files are resolution derivatives of one IIIF canvas and one physical fragment, not two witnesses.",
        ],
        "raw": {
            "record_id": "R1007292",
            "access_method": "Official IIIF v3 manifest and public Image API; both returned HTTP 200 after ordinary read-only retrieval.",
            "codex_label_origin": "Pinned MPO v1.0.0 CSV",
            "manifest_sha256": receipt["manifest_sha256"],
        },
    }
    comparisons = load("data/comparison_sources.v1.json")
    if any(x["id"] == source_record["id"] for x in comparisons):
        raise ValueError("Fr 7292 is already registered as a comparison source")
    comparisons.append(source_record)
    write("data/comparison_sources.v1.json", comparisons)

    # Keep each successful image transfer in the acquisition ledger. The 800px
    # and 1600px responses share one canvas and are not counted as two fragments.
    downloads = load("data/downloads.json")
    transfer_entries = [
        {
            "id": "7292", "capture_index": 0, "url": receipt["image_url"],
            "destination": cap800["path"], "requested_at_utc": receipt["requested_at_utc"],
            "purpose": "Metadata-selected different-codex layout control; first low-resolution view",
            "bytes_received": cap800["bytes"], "status": 200, "content_type": "image/jpeg",
            "final_url": receipt["final_url"], "saved": True, "sha256": cap800["sha256"],
            "capture": cap800,
        },
        {
            "id": "7292", "capture_index": 0, "url": hi["image_url"],
            "destination": cap1600["path"], "requested_at_utc": hi["requested_at_utc"],
            "purpose": "Higher-resolution derivative of the same control capture for staff/ruler measurement",
            "bytes_received": cap1600["bytes"], "status": 200, "content_type": "image/jpeg",
            "final_url": hi["final_url"], "saved": True, "sha256": cap1600["sha256"],
            "capture": cap1600,
        },
    ]
    old_hashes = {x.get("sha256") for x in downloads}
    for entry in transfer_entries:
        if entry["sha256"] not in old_hashes:
            downloads.append(entry)
    write("data/downloads.json", downloads)

    capture_log = load("data/evidence_capture_log.json")
    if not any(x.get("capture", {}).get("sha256") == cap1600["sha256"] for x in capture_log):
        capture_log.append({"id": "mpo-7292", "capture_index": 0, "status": "ok", "capture": cap1600})
    write("data/evidence_capture_log.json", capture_log)

    manifest_receipt = {
        "url": receipt["manifest_url"],
        "requested_on": "2026-10-24",
        "status": 200,
        "content_type": "application/ld+json",
        "bytes_received": manifest_path.stat().st_size,
        "sha256": hashlib.sha256(manifest_path.read_bytes()).hexdigest(),
        "saved": True,
        "destination": str(manifest_path.relative_to(ROOT)),
        "purpose": "Resolve official canvas, IIIF image service and per-item reproduction rights before acquiring the matched control image.",
    }
    write("research/continuation_22/manifest_receipt.json", manifest_receipt)

    new_observations = load("research/continuation_22/observations.json")["annotations"]
    previous_observations = load("data/observations.v7.json")
    annotations = previous_observations["annotations"] + new_observations
    if len({x["id"] for x in annotations}) != len(annotations):
        raise ValueError("Duplicate observation identifier")
    write("data/observations.v8.json", {
        **previous_observations,
        "version": "8.0.0",
        "assessment_date": "2026-10-24",
        "inputs": previous_observations["inputs"] + ["research/continuation_22/observations.json"],
        "scope": "Post-review source tests, calibrated Codex 1505 layout measurements and one metadata-matched different-codex staff-pitch control; no new attribution or predictor.",
        "annotations": annotations,
    })

    previous_contexts = load("data/context_checks.v4.json")
    checks = previous_contexts["checks"]
    if any(c["id"] in {"CTX06", "CTX07"} for c in checks):
        raise ValueError("E22 context IDs already exist")
    checks.extend([
        {
            "id": "CTX06",
            "title": "Exact-layout different-codex staff-pitch control",
            "record_ids": ["mpo-7292", "mpo-10370", "mpo-10406"],
            "observation_ids": ["I22-7292-staff-pitch", "I22-7292-ruler"],
            "summary": "The metadata-selected Fr 7292 (MPO Codex 1306) antiphonary matches the Codex 1505 sample on notation, line count, text rows and written-area range. Two ruler-calibrated systems measure a mean staff pitch of approximately 5.543 mm, versus 5.602 mm averaged across the two E21 target images.",
            "outcome": "The difference is about 0.059 mm, far below conservative manual measurement uncertainty. This shows the measured pitch is not unique to the catalogue-labelled Codex 1505 group. It does not establish any same-book or same-hand relation.",
            "limits": [
                "Only one different-codex leaf is measured; no sample distribution or classifier test is inferred.",
                "The different-codex label and match-selection metadata come from MPO, not independent adjudication.",
                "The control is matched on genre and layout metadata, not scribe/hand or workshop.",
                "Ruler and staff centers were selected manually after image inspection; page warp, ruler-plane offset and perspective remain uncorrected.",
                "No second reader, specialist review, historical attribution or physical join is claimed."
            ],
            "sources": [
                "research/continuation_22/matched_staff_results.json",
                "research/continuation_22/matched_staff_control.py",
                "research/continuation_22/image_receipt.json",
                "https://lbiiif.riksarkivet.se/arkis!R1007292/manifest",
                "https://zenodo.org/records/17287665",
                "research/continuation_21/ruling_pitch_results.json"
            ]
        },
        {
            "id": "CTX07",
            "title": "Current BOMPAC/CODICUM prior-art check",
            "record_ids": ["mpo-10370", "mpo-10406", "mpo-8994", "mpo-10407", "mpo-10437"],
            "observation_ids": [],
            "summary": "A 2025 BOMPAC research note describes a 29,230-record integrated Stockholm-Helsinki dataset and about 12,300 codices. CODICUM's living survey describes a Nordic overview and reports 5,435 Helsinki fragments grouped into 1,544 codices, citing Taitto 2001 and BOMPAC metadata. The BOMPAC article reports 5,434 Finnish records; the one-record difference is unresolved.",
            "outcome": "Cross-collection integration is established prior work, not a new contribution by this project. The published pages checked do not adjudicate the specific target relationships. The linked BOMPAC dataset payload was not inspected, so no target-level record result is claimed.",
            "limits": [
                "The research note was read but the linked Zenodo dataset payload was not retrievable through the connected web route at this audit.",
                "The Nordic Survey is a living collection-level overview, not a target-level codex attribution.",
                "The 5,434 versus 5,435 count difference is unresolved; source versions/scopes were not harmonized.",
                "No unpublished CODICUM finding, expert endorsement or institution-held information is inferred."
            ],
            "sources": [
                "research/continuation_22/bompac_codicum_audit.json",
                "https://doi.org/10.24446/no5r",
                "https://doi.org/10.5281/zenodo.17511106",
                "https://www.codicum.eu/resources/nordic-survey",
                "https://www.codicum.eu/news"
            ]
        }
    ])
    write("data/context_checks.v5.json", {
        **previous_contexts,
        "version": "5.0.0",
        "assessment_date": "2026-10-24",
        "scope": "Supporting source, layout-control and prior-art checks; no additional frozen attribution hypotheses.",
        "checks": checks,
    })

    reviews = load("data/hypothesis_reviews.v1.json")
    reviews["version"] = "1.6.0"
    reviews["assessment_date"] = "2026-10-24"
    reviews["observations_path"] = "data/observations.v8.json"
    reviews["context_checks_path"] = "data/context_checks.v5.json"
    write("data/hypothesis_reviews.v1.json", reviews)

    print(json.dumps({
        "queue_sha256": queue_hash,
        "core_records": len(core),
        "comparison_sources": len(comparisons),
        "observations": len(annotations),
        "context_checks": len(checks),
        "new_contexts": ["CTX06", "CTX07"],
        "frozen_hypotheses_changed": False,
    }, indent=2))


if __name__ == "__main__":
    main()
