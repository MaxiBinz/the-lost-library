"""Small Phase 0 access audit; no matching model or bulk image harvesting.

Run from project root: python3 research/access_audit.py [--probe]
Offline profiling uses the cached CC0 mpo.csv. --probe makes seven IIIF
manifest/info/image requests plus one full-size image request, and tests
three Finnish catalogue/API URLs. Results are observations, not a census.
"""
import collections
import csv
import datetime
import hashlib
import json
import pathlib
import struct
import sys
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent
EVIDENCE = ROOT / "evidence"
EVIDENCE.mkdir(exist_ok=True)


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def dimensions(data):
    """Read JPEG frame dimensions without installing imaging dependencies."""
    if data[:2] != b"\xff\xd8":
        return None
    pos = 2
    while pos < len(data):
        if data[pos] != 255:
            pos += 1
            continue
        marker = data[pos + 1]
        pos += 2
        if marker in (216, 217):
            continue
        size = struct.unpack(">H", data[pos:pos + 2])[0]
        if marker in (192, 193, 194):
            height, width = struct.unpack(">HH", data[pos + 3:pos + 7])
            return [width, height]
        pos += size
    return None


rows = list(csv.DictReader((ROOT / "mpo.csv").open(encoding="utf-8-sig", newline="")))
populated = {k: sum(bool(r[k].strip()) for r in rows) for k in rows[0]}
ids = collections.Counter(r["signatur"].strip() for r in rows)
profile = {
    "source": "https://zenodo.org/records/17287665",
    "csv_bytes": (ROOT / "mpo.csv").stat().st_size,
    "md5": hashlib.md5((ROOT / "mpo.csv").read_bytes()).hexdigest(),
    "rows": len(rows), "columns": len(rows[0]), "fields": list(rows[0]),
    "nonempty": populated,
    "duplicate_identifiers": {k: v for k, v in ids.items() if v > 1},
    "codex_distinct_nonempty": len({r["codex"].strip() for r in rows if r["codex"].strip()}),
    "manifest_unique": len({r["iiif_manifest"].strip() for r in rows if r["iiif_manifest"].strip()}),
    "exact_title_subsets": {},
    "notation": dict(collections.Counter(r["notation"].strip() for r in rows)),
}
for title in ("Antiphonarium", "Graduale", "Sequentiarium"):
    selected = [r for r in rows if r["sachtitel"].strip() == title]
    profile["exact_title_subsets"][title] = {
        "records": len(selected),
        "manifest_populated": sum(bool(r["iiif_manifest"].strip()) for r in selected),
        "codex_populated": sum(bool(r["codex"].strip()) for r in selected),
    }
write_json(ROOT / "mpo_profile.json", profile)
selected = [r for r in rows if r["codex"].strip() == "Codex 1104" or r["ccmsignum"].strip() == "Ant 49"]
write_json(ROOT / "mpo_target_records.json", selected)
print(json.dumps({k: profile[k] for k in ("rows", "columns", "md5", "exact_title_subsets")}))

if "--probe" not in sys.argv:
    sys.exit(0)

log = []


def fetch(url, filename=None, cap=3000000):
    observation = {"url": url, "checked_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat()}
    try:
        with urllib.request.urlopen(url, timeout=35) as response:
            data = response.read(cap + 1)
            if len(data) > cap:
                raise ValueError("response exceeds Phase 0 byte cap")
            observation.update(status=response.status, final_url=response.url,
                               content_type=response.headers.get("Content-Type"), bytes=len(data),
                               sha256=hashlib.sha256(data).hexdigest())
            if data[:2] == b"\xff\xd8":
                observation["jpeg_dimensions"] = dimensions(data)
            if filename:
                (EVIDENCE / filename).write_bytes(data)
                observation["saved"] = "research/evidence/" + filename
        log.append(observation)
        return data
    except Exception as exc:
        observation.update(status=getattr(exc, "code", None), error=str(exc))
        log.append(observation)
        return None


summaries = []
for identifier in ("7957", "7960", "7961", "8343", "8344", "8201", "8304"):
    record = next(r for r in rows if r["signatur"] == identifier)
    data = fetch(record["iiif_manifest"], f"mpo_{identifier}_manifest.json")
    if not data:
        continue
    manifest = json.loads(data)
    canvases = manifest.get("items", [])
    body = canvases[0]["items"][0]["items"][0]["body"]
    service = body["service"][0]["id"]
    info_data = fetch(service + "/info.json", f"mpo_{identifier}_info.json")
    info = json.loads(info_data) if info_data else {}
    image_url = service + "/full/800,/0/default.jpg"
    fetch(image_url, f"mpo_{identifier}_sample.jpg")
    if identifier == "7957":
        fetch(body["id"], f"mpo_{identifier}_full.jpg")
    summaries.append({"mpo": identifier, "manifest": record["iiif_manifest"],
                      "canvases": len(canvases), "catalogue_leaves": record["blattzahl"],
                      "first_canvas_dimensions": [canvases[0]["width"], canvases[0]["height"]],
                      "image_service_dimensions": [info.get("width"), info.get("height")],
                      "image_url": image_url,
                      "rights_metadata": [m for m in manifest.get("metadata", []) if "Rights" in str(m.get("label"))]})

for url in ("https://fragmenta.kansalliskirjasto.fi/",
            "https://fragmenta.kansalliskirjasto.fi/handle/10024/1610",
            "https://api.finna.fi/v1/search?lookfor=F.m.II.44&limit=1"):
    fetch(url, cap=1000000)
write_json(ROOT / "access_log.json", log)
write_json(ROOT / "mpo_sample_summary.json", summaries)
print(json.dumps(summaries, ensure_ascii=False, indent=2))
print("Requests:", len(log), "Downloaded bytes:", sum(x.get("bytes", 0) for x in log))
