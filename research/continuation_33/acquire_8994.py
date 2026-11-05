"""Acquire four native-width versions of already retained Fr 8994 photographs.

The IIIF services and PDM rights come from the cached institutional manifest.
Never replace the primary images, normalized metadata, predictors, or queue.
Each service is requested at most once by this script; failed attempts are kept.
"""
from __future__ import annotations

import hashlib
import io
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from lost_library.pipeline import build_database, parse_manifest, permitted_rights


def read(path):
    return json.loads(path.read_text())


def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def frozen(records):
    return [(r["id"], r["normalized"], (r.get("image") or {}).get("sha256")) for r in records]


def main():
    records_path = ROOT / "data/fragments.json"
    records = read(records_path)
    before = frozen(records)
    record = next(r for r in records if r["id"] == "mpo-8994")
    manifest = read(ROOT / "data/manifests/8994.json")
    assert len(manifest["items"]) == 4
    audit = read(ROOT / "data/resource_audit.json")
    assert audit["conservative_planning_total_bytes"] + 20_000_000 < 3_000_000_000
    assert audit["working_source_capture_files"] + 4 <= 300
    receipt_path = Path(__file__).with_name("download_receipts.json")
    receipts = read(receipt_path) if receipt_path.exists() else []
    downloads_path = ROOT / "data/downloads.json"
    downloads = read(downloads_path)
    retry_local_network = "--retry-local-network-error" in sys.argv
    for index, canvas in enumerate(manifest["items"]):
        prior = [x for x in receipts if x["capture_index"] == index]
        if prior:
            local_dns_failure = (not prior[-1].get("saved") and prior[-1].get("status") is None
                                 and "nodename nor servname" in prior[-1].get("error", ""))
            if not (retry_local_network and local_dns_failure):
                continue
        info = parse_manifest(dict(manifest, items=[canvas]))
        assert permitted_rights(info["rights"])
        width = int(info["native_width"])
        assert width <= 2000
        url = info["service"].rstrip("/") + f"/full/{width},/0/default.jpg"
        assert urlsplit(url).hostname == "lbiiif.riksarkivet.se"
        assert urlsplit(url).scheme == "https"
        name = f"data/images/mpo-8994-capture-{index+1}-{width}px.jpg"
        destination = ROOT / name
        assert not destination.exists()
        item = {
            "id": "8994", "capture_index": index, "url": url,
            "destination": name,
            "requested_at_utc": datetime.now(timezone.utc).isoformat(),
            "purpose": "Read signs and chant/text on an existing photograph; not another object or side",
            "bytes_received": 0,
        }
        data = b""
        try:
            with urlopen(Request(url, headers={"User-Agent": "LostLibraryResearch/0.1 bounded source reading"}), timeout=30) as response:
                item.update(status=response.status, content_type=response.headers.get("Content-Type"), final_url=response.url)
                data = response.read(5_000_001)
            assert len(data) <= 5_000_000
            with Image.open(io.BytesIO(data)) as im:
                w, h = im.size
                im.verify()
            assert w == width and h > 0
            digest = hashlib.sha256(data).hexdigest()
            destination.write_bytes(data)
            capture = {
                "path": name, "url": url, "sha256": digest,
                "width": w, "height": h, "bytes": len(data),
                "canvas_id": info["canvas_id"], "physical_object_id": "mpo-8994",
                "capture_index": index, "resolution_variant": True,
                "label": f"Manifest image {index+1}, native-width derivative (same photograph; not a new side)",
                "rights_url": info["rights"],
            }
            record["captures"].append(capture)
            item.update(saved=True, sha256=digest, capture=capture)
            write(records_path, records)
        except Exception as error:
            item.update(saved=False, error=str(error), status=getattr(error, "code", item.get("status")))
        item["bytes_received"] = len(data)
        receipts.append(item)
        downloads.append(item)
        write(receipt_path, receipts)
        write(downloads_path, downloads)
        print(json.dumps({k: item.get(k) for k in ("capture_index", "saved", "bytes_received", "error")}), flush=True)
        if not item["saved"]:
            break
    assert frozen(records) == before
    build_database(ROOT, records)
    summary_path = ROOT / "data/ingestion_summary.json"
    summary = read(summary_path)
    images = list((ROOT / "data/images").glob("*.jpg"))
    summary.update(source_image_files=len(images), stored_image_bytes=sum(p.stat().st_size for p in images),
                   new_download_bytes=sum(x.get("bytes_received", 0) for x in downloads))
    write(summary_path, summary)


if __name__ == "__main__":
    main()
