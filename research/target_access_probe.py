"""Fetch four bounded public IIIF sample images for the Phase 0 hypothesis audit.

No corpus harvest or matching is performed. Run from any directory with
python3 research/target_access_probe.py. Responses above 750 kB are rejected.
The original access receipt is preserved; this writes target_access_log.json.
"""
import datetime
import hashlib
import json
import pathlib
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent
EVIDENCE = ROOT / "evidence"
LOG = ROOT / "target_access_log.json"
observations = []


def fetch(url, name):
    item = {"url": url, "checked_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat()}
    try:
        with urllib.request.urlopen(url, timeout=20) as response:
            data = response.read(750001)
            if len(data) > 750000:
                raise ValueError("750000-byte per-response cap exceeded")
            item.update(status=response.status, content_type=response.headers.get("Content-Type"),
                        bytes=len(data), sha256=hashlib.sha256(data).hexdigest(),
                        saved="research/evidence/" + name)
            (EVIDENCE / name).write_bytes(data)
        observations.append(item)
        LOG.write_text(json.dumps(observations, ensure_ascii=False, indent=2) + "\n")
        return data
    except Exception as error:
        item.update(status=getattr(error, "code", None), error=str(error))
        observations.append(item)
        LOG.write_text(json.dumps(observations, ensure_ascii=False, indent=2) + "\n")
        return None


summary = []
for identifier in ("1385", "20274", "8994", "25592"):
    # Identifiers and URLs come from the cached institutional MPO export.
    code = "R1" + identifier.zfill(6)
    manifest_url = "https://lbiiif.riksarkivet.se/arkis!" + code + "/manifest"
    data = fetch(manifest_url, "target_" + identifier + "_manifest.json")
    if not data:
        continue
    manifest = json.loads(data)
    canvas = manifest["items"][0]
    body = canvas["items"][0]["items"][0]["body"]
    service = body["service"][0]["id"]
    image_url = service + "/full/600,/0/default.jpg"
    image = fetch(image_url, "target_" + identifier + "_sample.jpg")
    summary.append({"mpo": identifier, "manifest": manifest_url,
                    "canvases": len(manifest["items"]), "image_url": image_url,
                    "jpeg_magic_verified": bool(image and image.startswith(b"\xff\xd8")),
                    "first_canvas_dimensions": [canvas["width"], canvas["height"]],
                    "rights_metadata": [m for m in manifest.get("metadata", []) if "Rights" in str(m.get("label"))]})
    print(json.dumps(summary[-1], ensure_ascii=False), flush=True)
(ROOT / "target_access_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n")
