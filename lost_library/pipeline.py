"""Bounded, provenance-preserving manuscript ingestion for The Lost Library.

Uses only public IIIF metadata/images and the explicitly cached Finnish PDF.
No access restriction bypass, credentials, model fitting, or manuscript identity
inference occurs here. Benchmark labels are stored outside predictor metadata.
"""
from __future__ import annotations

import concurrent.futures
import csv
import datetime as dt
import hashlib
import io
import json
import re
import shutil
import sqlite3
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict
from pathlib import Path

from PIL import Image

MPO_URL = "https://zenodo.org/api/records/17287665/files/mpo.csv/content"
MPO_SOURCE = "https://zenodo.org/records/17287665"
MPO_MD5 = "bac851653aa9b0816208a13430154cfb"
PDM = "http://creativecommons.org/publicdomain/mark/1.0/"
MAX_IMAGES = 300
MAX_DOWNLOAD_BYTES = 3_000_000_000
GROUPS = [
    ("Codex 285", "development"), ("Codex 270", "development"),
    ("Codex 875", "development"), ("Codex 1200", "calibration"),
    ("Codex 609", "calibration"), ("Codex 276", "calibration"),
    ("Codex 1104", "test"), ("Codex 434", "test"),
    ("Codex 920", "test"), ("Codex 674", "test"),
]
TARGET_IDS = ["1385", "20274", "8994", "10370", "10406", "10407", "10437", "25592", "10349"]
ANT49_IDS = ["8066", "8072", "8073", "8201", "8304", "9620"]
MISSING_IDS = ["20106", "28175", "29666", "20340", "20275", "20276", "20277", "20278"]
ALLOWED_HOSTS = {"zenodo.org", "lbiiif.riksarkivet.se", "fragmentarium.ms"}


def _now():
    return dt.datetime.now(dt.timezone.utc).isoformat()


def _sha(data):
    return hashlib.sha256(data).hexdigest()


def _dump(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")
    temporary.replace(path)


def _text(value):
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return "; ".join(_text(v) for v in value)
    if isinstance(value, dict):
        if "@value" in value:
            return str(value["@value"])
        return "; ".join(_text(v) for v in value.values())
    return "" if value is None else str(value)


def _plain(value):
    return re.sub(r"<[^>]*>", "", _text(value)).strip()


def parse_dimension(value):
    """Parse observed dimensions only; preserve the original uncertainty outside."""
    match = re.fullmatch(r"[ *?]*(\d+(?:\.\d+)?)\s*x\s*[ *?]*(\d+(?:\.\d+)?)[ *?]*", (value or "").strip())
    return [float(x) for x in match.groups()] if match else None


def parse_integer(value):
    match = re.search(r"\d+", value or "")
    return int(match.group()) if match else None


def parse_date(value):
    value = value or ""
    years = [int(x) for x in re.findall(r"\b(?:1[0-9]{3})\b", value)]
    if years:
        return min(years), max(years)
    centuries = [int(x) for x in re.findall(r"\b(\d{1,2})\.", value.split("Jh", 1)[0])] if "Jh" in value else []
    if not centuries:
        return None, None
    start, end = 100 * (min(centuries) - 1), 100 * max(centuries) - 1
    if len(centuries) == 1:
        if re.search(r"1\.\s*Hälfte", value):
            end = start + 49
        elif re.search(r"2\.\s*Hälfte", value):
            start += 50
    return start, end


def normalize_mpo(row):
    lower, upper = parse_date(row.get("datierung"))
    return {
        "type": row.get("sachtitel", "").strip() or None,
        "date_min": lower, "date_max": upper,
        "date_raw": row.get("datierung", ""),
        "leaf_cm": parse_dimension(row.get("format")),
        "written_cm": parse_dimension(row.get("schriftraum1")),
        "columns": parse_integer(row.get("spaltenzahl")),
        "lines": parse_integer(row.get("zeilenzahl1")),
        "script": row.get("schrift", "").strip() or None,
        "notation": row.get("notation", "").strip() or None,
        "staff_lines": parse_integer(row.get("notenlinien")),
        "contents": row.get("inhalt", "").strip(),
        "origin": row.get("entstehungsort", "").strip() or None,
        "use_place": row.get("anwendungsort", "").strip() or None,
        "leaves": parse_integer(row.get("blattzahl")),
        "material": row.get("beschreibstoff", "").strip() or None,
    }


def _warnings(row):
    warnings = ["Representative capture is not a complete leaf-side inventory.",
                "Catalogue association fields are source assertions, not newly verified identities."]
    for field in ("format", "schriftraum1", "datierung", "notenlinien", "zeilenzahl1"):
        if any(marker in row.get(field, "") for marker in ("*", "?", "#", "(")):
            warnings.append(f"Uncertain or qualified source value retained: {field}={row[field]}")
    if row.get("institution") == "KB":
        warnings.append("KB is the catalogue holder label; present physical custody needs confirmation.")
    return warnings


def permitted_rights(value):
    """Conservative local working set: explicit PDM, CC0 or CC BY4 only."""
    value = _text(value).lower()
    return any(token in value for token in (
        "creativecommons.org/publicdomain/mark/1.0", "creativecommons.org/publicdomain/zero/1.0",
        "creativecommons.org/licenses/by/4.0"))


def parse_manifest(manifest):
    """Read Presentation2/3 first capture; never mistake canvas count for leaves."""
    metadata = {_plain(m.get("label")): _plain(m.get("value")) for m in manifest.get("metadata", [])}
    rights = manifest.get("rights") or manifest.get("license")
    if not rights:
        rights = next((v for k, v in metadata.items() if "Rights" in k or "Rättigheter" in k), "")
    if isinstance(rights, list):
        rights = rights[0] if rights else ""
    if manifest.get("items"):
        canvases = manifest["items"]
        canvas = canvases[0]
        body = canvas["items"][0]["items"][0]["body"]
    else:
        canvases = manifest["sequences"][0]["canvases"]
        canvas = canvases[0]
        body = canvas["images"][0]["resource"]
    service = body.get("service")
    if isinstance(service, list):
        service = service[0]
    service_id = service.get("id", service.get("@id")) if isinstance(service, dict) else service
    provider = _plain(manifest.get("provider", [{}])[0].get("label")) if manifest.get("provider") else None
    return {"rights": _text(rights), "metadata": metadata,
            "canvas_id": canvas.get("id", canvas.get("@id")), "canvas_count": len(canvases),
            "service": service_id, "image_resource": body.get("id", body.get("@id")),
            "native_width": body.get("width") or canvas.get("width"),
            "native_height": body.get("height") or canvas.get("height"),
            "label": _plain(manifest.get("label")),
            "attribution": _plain(manifest.get("attribution")) or provider,
            "provider": provider}


class Fetcher:
    """Small anonymous public fetches, cache first, no retry of denial responses."""
    def __init__(self, root, offline=False):
        self.root = Path(root)
        self.path = self.root / "data/downloads.json"
        self.entries = json.loads(self.path.read_text()) if self.path.exists() else []
        self.lock = threading.Lock()
        self.offline = offline
        self.inflight_cap = 0
        self.pending_images = set()

    def record(self, entry):
        with self.lock:
            self.entries.append(entry)
            _dump(self.path, self.entries)

    def get(self, url, destination, cap=4_000_000):
        destination = Path(destination)
        if destination.exists():
            return destination.read_bytes()
        if self.offline:
            raise FileNotFoundError(f"Offline cache miss: {destination}")
        parsed = urllib.parse.urlsplit(url)
        if parsed.scheme != "https" or parsed.hostname not in ALLOWED_HOSTS:
            raise ValueError(f"Unapproved public host or scheme: {url}")
        for attempt in range(2):
            entry = {"url": url, "requested_at_utc": _now(), "attempt": attempt + 1,
                     "destination": str(destination.relative_to(self.root))}
            data = b""
            reserved = False
            try:
                with self.lock:
                    total = sum(x.get("bytes_received", 0) for x in self.entries)
                    if total + self.inflight_cap + cap > MAX_DOWNLOAD_BYTES:
                        raise ValueError("3GB pipeline download budget would be exceeded")
                    self.inflight_cap += cap
                    reserved = True
                request = urllib.request.Request(url, headers={"User-Agent": "LostLibraryResearch/0.1 (bounded local research)"})
                with urllib.request.urlopen(request, timeout=20) as response:
                    data = response.read(cap + 1)
                    entry.update(status=response.status, content_type=response.headers.get("Content-Type"),
                                 bytes_received=len(data), sha256=_sha(data), final_url=response.url)
                if len(data) > cap:
                    raise ValueError(f"Response exceeds {cap}-byte cap")
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_bytes(data)
                entry["saved"] = True
                self.record(entry)
                return data
            except Exception as error:
                entry.update(status=getattr(error, "code", None), bytes_received=len(data), error=str(error))
                self.record(entry)
                if isinstance(error, urllib.error.HTTPError) and error.code in (400, 401, 403, 404, 410, 429):
                    raise
                if attempt:
                    raise
                time.sleep(.3)
            finally:
                if reserved:
                    with self.lock:
                        self.inflight_cap -= cap


def _metadata(root, fetcher):
    root = Path(root)
    cached = root / "research/mpo.csv"
    if not cached.exists():
        cached = root / "data/raw/mpo.csv"
        fetcher.get(MPO_URL, cached, cap=12_000_000)
    data = cached.read_bytes()
    if hashlib.md5(data).hexdigest() != MPO_MD5:
        raise ValueError("MPO CSV checksum differs from the pinned 2025v1 deposit")
    return list(csv.DictReader(io.StringIO(data.decode("utf-8-sig"))))


def make_sample_plan(root, limit=120, offline=False):
    """Deterministic explicit-codex sampling plus unlabelled lookalike distractors."""
    root = Path(root)
    if not 100 <= limit <= MAX_IMAGES - 2:
        raise ValueError("Choose100–298 representative records; two slots reserved for Finnish sides")
    rows = _metadata(root, Fetcher(root, offline=offline))
    by_id = {r["signatur"].strip(): r for r in rows}
    selected, assigned, groups = [], set(), []

    def add(identifier, role, group_id=None, split=None):
        if identifier not in assigned:
            if identifier not in by_id:
                raise ValueError(f"MPO identifier absent from source: {identifier}")
            selected.append({"source": "MPO", "identifier": identifier, "id": "mpo-" + identifier,
                             "role": role, "group_id": group_id, "split": split})
            assigned.add(identifier)

    for group, split in GROUPS:
        members = sorted((r for r in rows if r["codex"].strip() == group and r["iiif_manifest"].strip()
                          and r["sachtitel"].strip() in {"Antiphonarium", "Graduale"}), key=lambda r: int(r["signatur"]))[:6]
        if len(members) < 4:
            raise ValueError(f"Insufficient image-linked records for {group}")
        group_id = "mpo-" + group.lower().replace(" ", "-")
        for row in members:
            add(row["signatur"], "control" if group == "Codex 1104" else "benchmark", group_id, split)
        groups.append({"id": group_id, "split": split, "member_ids": ["mpo-" + r["signatur"] for r in members],
                       "label_source": "https://fragmenta.kansalliskirjasto.fi/handle/10024/1610?show=full" if group == "Codex 1104" else MPO_SOURCE,
                       "label_strength": "literature/catalogue-backed" if group == "Codex 1104" else "catalogue-derived",
                       "source_label": group,
                       "limitations": "A shared institutional codex label is not independent expert adjudication; separate labels may still need reconciliation."})
    for identifier in TARGET_IDS:
        add(identifier, "target")
    for identifier in ANT49_IDS:
        add(identifier, "control")
    # Reserve12 Beauvais leaf records and1 Finnish physical fragment.
    mpo_target = limit - 13
    distractors = [r for r in rows if r["signatur"] not in assigned and r["iiif_manifest"].strip()
                   and not r["codex"].strip() and r["sachtitel"].strip() in {"Antiphonarium", "Graduale"}
                   and "15." in r["datierung"]]
    distractors.sort(key=lambda r: _sha(("lost-library-v1:" + r["signatur"]).encode()))
    for row in distractors:
        if len(selected) >= mpo_target:
            break
        add(row["signatur"], "distractor")
    plan = {"version": "1.0", "selection_rule": "10 explicit codex groups, first6 numeric IDs with images; target/control IDs; deterministic SHA256 order15c ungrouped musical distractors",
            "requested_representative_records": limit, "mpo_records": selected,
            "beauvais_requested": 12, "finnish_physical_records": 1,
            "nonimage_record_ids": MISSING_IDS, "groups": groups,
            "selection_bias": "Access and existing labels drive this small nonrepresentative sample. Unknown distractor relationships are not negative labels.",
            "budget": {"max_source_images": MAX_IMAGES, "max_pipeline_download_bytes": MAX_DOWNLOAD_BYTES}}
    _dump(root / "data/sample_plan.json", plan)
    return plan


def _cached_manifest(root, identifier, source="MPO"):
    evidence = Path(root) / "research/evidence"
    names = [f"mpo_{identifier}_manifest.json", f"target_{identifier}_manifest.json"] if source == "MPO" else [f"{identifier}_manifest.json"]
    for name in names:
        if (evidence / name).exists():
            return evidence / name
    return None


def _cached_image(root, identifier, source="MPO"):
    evidence = Path(root) / "research/evidence"
    names = [f"mpo_{identifier}_sample.jpg", f"mpo_{identifier}_goal_sample.jpg", f"target_{identifier}_sample.jpg"] if source == "MPO" else [f"{identifier}_sample_1200.jpg", f"{identifier}_sample.jpg"]
    for name in names:
        if (evidence / name).exists():
            return evidence / name
    return None


def _load_manifest(root, fetcher, identifier, url, source="MPO"):
    destination = Path(root) / "data/manifests" / (identifier + ".json")
    cached = _cached_manifest(root, identifier, source)
    if not destination.exists() and cached:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(cached, destination)
    content = fetcher.get(url, destination, cap=2_000_000)
    return json.loads(content), _sha(content)


def _image(root, fetcher, identifier, info, source="MPO", width=800):
    if not permitted_rights(info["rights"]):
        raise ValueError("Image omitted: no explicit PDM/CC0/CCBY4 rights statement in child manifest")
    destination = Path(root) / "data/images" / (("mpo-" if source == "MPO" else "fragmentarium-") + identifier + ".jpg")
    if not destination.exists() and len(list(destination.parent.glob("*.jpg"))) >= MAX_IMAGES:
        raise ValueError("Working-image cap reached; do not download additional images")
    cached = _cached_image(root, identifier, source)
    reused = None
    if not destination.exists() and cached:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(cached, destination)
        reused = str(cached.relative_to(root))
    native_width = info.get("native_width")
    if isinstance(native_width, (int,float)) and native_width > 0:
        width = min(width, int(native_width))
    if info["service"]:
        image_url = info["service"].rstrip("/") + f"/full/{width},/0/default.jpg"
    else:
        image_url = info["image_resource"]
    content = fetcher.get(image_url, destination)
    try:
        with Image.open(io.BytesIO(content)) as decoded:
            actual_width, actual_height = decoded.size
            decoded.verify()
    except Exception:
        destination.unlink(missing_ok=True)
        raise
    if reused and info["service"]:
        image_url = info["service"].rstrip("/") + f"/full/{actual_width},/0/default.jpg"
    return str(destination.relative_to(root)), {
        "url": image_url, "sha256": _sha(content), "width": actual_width, "height": actual_height,
        "bytes": len(content), "canvas_id": info["canvas_id"], "role": "first_capture",
        "verified_at_utc": _now(), "reused_from": reused, "provider": info.get("provider"),
    }


def _mpo_record(root, row, spec, fetcher):
    identifier = row["signatur"].strip()
    holder = {"KA": "Swedish National Archives", "KB": "Kungliga biblioteket (catalogue label)", "HUB": "National Library of Finland (catalogue label)"}.get(row.get("institution"), row.get("institution") or "Holder unrecorded")
    record = {"id": "mpo-" + identifier, "shelfmark": "Riksarkivet Fr " + identifier,
              "institution": holder, "collection": "MPO", "source_url": row.get("bildbetrachter") or "https://sok.riksarkivet.se/en/mpo",
              "manifest_url": row.get("iiif_manifest") or None, "rights_url": None,
              "attribution": None, "image_path": None, "image": None,
              "raw": dict(row), "normalized": normalize_mpo(row), "role": spec.get("role", "control"),
              "physical_object_id": "mpo-" + identifier, "warnings": _warnings(row)}
    if not record["manifest_url"]:
        record["warnings"].append("No image pointer in pinned export; record retained but not counted as an image.")
        return record
    try:
        manifest, manifest_sha = _load_manifest(root, fetcher, identifier, record["manifest_url"])
        info = parse_manifest(manifest)
        record.update(rights_url=info["rights"], attribution=info["attribution"] or "National Archives of Sweden",
                      manifest_sha256=manifest_sha, source_canvas_count=info["canvas_count"])
        record["image_path"], record["image"] = _image(root, fetcher, identifier, info)
    except Exception as error:
        record["warnings"].append("Image access failed: " + str(error))
    return record


def _beauvais_candidates(root):
    d = json.loads((Path(root) / "research/evidence/F-4ihz_manifest.json").read_text())
    identifiers = list(dict.fromkeys(re.findall(r"/(F-[a-z0-9]+)/", json.dumps(d))))
    preferred = ["F-6zvk", "F-qbrf", "F-5uba"]
    return preferred + [x for x in identifiers if x not in preferred and x not in {"F-4ihz", "F-g7p5"}]


def _beauvais_record(root, identifier, fetcher):
    url = f"https://fragmentarium.ms/metadata/iiif/{identifier}/manifest.json"
    manifest, manifest_sha = _load_manifest(root, fetcher, identifier, url, "Fragmentarium")
    info = parse_manifest(manifest)
    metadata = info["metadata"]
    if not permitted_rights(info["rights"]):
        raise ValueError("Child rights not within explicit permitted working-set statements")
    extent = metadata.get("Number of Fragment Items", "")
    if extent and not re.search(r"^1\s+lea[fv]", extent, re.I):
        raise ValueError("Child is not explicitly one leaf; skip ambiguous physical unit")
    image_path, image = _image(root, fetcher, identifier, info, "Fragmentarium")
    dim = re.search(r"(\d+(?:\.\d+)?)\s*x\s*(\d+(?:\.\d+)?)\s*mm", metadata.get("Current Dimensions (in mm)", ""))
    date = re.findall(r"\b(1\d{3})\b", metadata.get("Date of origin", ""))
    shelfmark = metadata.get("Shelfmark") or identifier
    holder = metadata.get("Collection Name") or info["label"]
    return {"id": "fragmentarium-" + identifier, "shelfmark": holder + ", " + shelfmark,
            "institution": holder, "collection": "Fragmentarium / Beauvais Missal",
            "source_url": f"https://fragmentarium.ms/overview/{identifier}", "manifest_url": url,
            "rights_url": info["rights"], "attribution": holder + "; " + (info["attribution"] or "Fragmentarium"),
            "manifest_sha256": manifest_sha, "image_path": image_path, "image": image,
            "source_canvas_count": info["canvas_count"], "physical_object_id": "fragmentarium-" + identifier,
            "raw": metadata,
            "normalized": {"type": "Missal", "date_min": min(map(int, date)) if date else None,
                           "date_max": max(map(int, date)) if date else None,
                           "date_raw": metadata.get("Date of origin"),
                           "leaf_cm": [float(x) / 10 for x in dim.groups()] if dim else None,
                           "written_cm": None, "columns": None, "lines": None,
                           "script": metadata.get("Script Type"), "notation": metadata.get("Musical Notation"),
                           "staff_lines": None, "contents": "Liturgical missal fragment; text not independently transcribed for matching.",
                           "origin": metadata.get("Place of origin"), "use_place": "Beauvais", "leaves": 1, "material": metadata.get("Material")},
            "role": "control", "warnings": ["Published Beauvais reconstruction membership; positive control, not a new identification.",
                                                "One source capture per leaf; this book is a domain-shifted control, not a standalone discrimination benchmark."]}


def _finnish_record(root):
    root = Path(root)
    pdf = root / "research/evidence/F_m_IV_173.pdf"
    receipt = json.loads((root / "research/evidence/finnish_access.json").read_text())
    if _sha(pdf.read_bytes()) != receipt["sha256"]:
        raise ValueError("Finnish source PDF checksum mismatch")
    import pypdfium2 as pdfium
    document = pdfium.PdfDocument(str(pdf))
    captures = []
    for index in range(min(2, len(document))):
        destination = root / "data/images" / f"fm-IV173-{index + 1}.jpg"
        if not destination.exists():
            page = document[index]
            picture = page.render(scale=1.5).to_pil().convert("RGB")
            picture.thumbnail((1200, 1600))
            picture.save(destination, "JPEG", quality=90)
            page.close()
        content = destination.read_bytes()
        with Image.open(destination) as picture:
            width, height = picture.size
        captures.append({"path": str(destination.relative_to(root)), "label": f"PDF page {index + 1}",
                         "physical_object_id": "finn-iv173", "sha256": _sha(content), "width": width, "height": height,
                         "url": receipt["download_url"], "bytes": len(content), "role": "pdf_page_derivative"})
    document.close()
    return {"id": "finn-iv173", "shelfmark": "Helsinki F.m.IV.173", "institution": "National Library of Finland",
            "collection": "Fragmenta membranea", "source_url": receipt["record"], "manifest_url": None,
            "rights_url": receipt["rights_from_catalogue"], "attribution": "National Library of Finland",
            "image_path": captures[0]["path"], "image": {k: v for k, v in captures[0].items() if k != "path"},
            "captures": captures, "physical_object_id": "finn-iv173", "raw": {"source_pdf": str(pdf.relative_to(root)),
                 "source_pdf_sha256": receipt["sha256"], "shelfmark": "F.m.IV.173", "catalogue_associations": "Same codex Ant242/Fr29666; suggested Hy49/Fr25592 and Ant99; not newly adjudicated"},
            "normalized": {"type": "Antiphonal / Gradual?", "date_min":1450, "date_max":1499,
                           "date_raw":"15th century, second half (catalogue note)", "leaf_cm": None, "written_cm":None,
                           "columns":None,"lines":None,"script":None,"notation":"Quadr", "staff_lines":4,
                           "contents":"Terminal Te Deum leaf (catalogue description)","origin":"Åbo/Nådendal?", "use_place":"Åbo?", "leaves":1,"material":"Parchment"},
            "role":"target", "warnings":["Two PDF pages are two captures of one physical leaf, not two fragments.",
                "PDF obtained earlier through the official public browser viewer; no automated access bypass used.",
                "Approximate dating/notation/content transcribed from prior live catalogue inspection; no new attribution inferred.",
                "Finnish measurement convention and suggested associations remain unresolved."]}


def build_database(root, fragments):
    root = Path(root)
    path = root / "data/fragments.sqlite"
    with sqlite3.connect(path) as db:
        db.execute("DROP TABLE IF EXISTS fragments")
        db.execute("DROP TABLE IF EXISTS fragments_fts")
        db.execute("CREATE TABLE fragments(id TEXT PRIMARY KEY,shelfmark TEXT,institution TEXT,collection TEXT,role TEXT,has_image INTEGER,json TEXT NOT NULL)")
        db.executemany("INSERT INTO fragments VALUES(?,?,?,?,?,?,?)", [(r["id"],r["shelfmark"],r["institution"],r["collection"],r["role"],int(bool(r.get("image_path"))),json.dumps(r,ensure_ascii=False)) for r in fragments])
        db.execute("CREATE VIRTUAL TABLE fragments_fts USING fts5(id UNINDEXED,shelfmark,institution,contents,metadata)")
        db.executemany("INSERT INTO fragments_fts VALUES(?,?,?,?,?)", [(r["id"],r["shelfmark"],r["institution"],r["normalized"].get("contents", ""),json.dumps(r.get("raw",{}),ensure_ascii=False)) for r in fragments])
    return path


def search(root, query, limit=20):
    # Quote every term: user text cannot introduce FTS operators or SQL syntax.
    terms = re.findall(r"[\w]+", query, re.UNICODE)
    if not terms:
        return []
    fts = " AND ".join('"' + term.replace('"','""') + '"' for term in terms)
    with sqlite3.connect(Path(root) / "data/fragments.sqlite") as db:
        rows = db.execute("SELECT f.json FROM fragments f JOIN fragments_fts s ON f.id=s.id WHERE fragments_fts MATCH ? ORDER BY bm25(fragments_fts) LIMIT ?", (fts, int(limit))).fetchall()
    return [json.loads(r[0]) for r in rows]


def fetch_capture(root, fragment_id, canvas_index=0, width=800, offline=False):
    """Add one permitted source view for a documented reconstruction component.

    Alternate captures are kept under the same record and physical-object ID;
    this never turns recto/verso or a folded view into another benchmark object.
    The index is a manifest capture index, not an inferred medieval leaf order.
    """
    root = Path(root).resolve()
    fragments = json.loads((root / "data/fragments.json").read_text())
    record = next((r for r in fragments if r["id"] == fragment_id), None)
    if record is None:
        raise KeyError(fragment_id)
    if not record.get("manifest_url"):
        raise ValueError("Record has no verified IIIF manifest")
    fetcher = Fetcher(root,offline=offline)
    identifier = fragment_id.removeprefix("mpo-").removeprefix("fragmentarium-")
    source = "MPO" if fragment_id.startswith("mpo-") else "Fragmentarium"
    manifest, _ = _load_manifest(root,fetcher,identifier,record['manifest_url'],source)
    canvases = manifest.get("items") or manifest.get("sequences",[{}])[0].get("canvases",[])
    if not 0 <= canvas_index < len(canvases):
        raise IndexError("Manifest capture index out of range")
    subset = dict(manifest)
    if manifest.get("items"):
        subset["items"] = [canvases[canvas_index]]
    else:
        subset["sequences"] = [dict(manifest['sequences'][0],canvases=[canvases[canvas_index]])]
    info = parse_manifest(subset)
    if not permitted_rights(info['rights']):
        raise ValueError("Image rights outside permitted working-set policy")
    if canvas_index == 0:
        return {"path":record['image_path'],**record['image'],"physical_object_id":record['physical_object_id'],"capture_index":0}
    destination = root / "data/images" / f"{fragment_id}-capture-{canvas_index+1}.jpg"
    if not destination.exists() and len(list(destination.parent.glob('*.jpg'))) >= MAX_IMAGES:
        raise ValueError("300-image working limit reached")
    actual_width = min(width,int(info['native_width'])) if info.get('native_width') else width
    url = info['service'].rstrip('/') + f"/full/{actual_width},/0/default.jpg" if info['service'] else info['image_resource']
    data = fetcher.get(url,destination)
    with Image.open(io.BytesIO(data)) as image:
        w,h=image.size
        image.verify()
    capture = {"path":str(destination.relative_to(root)),"url":url,"sha256":_sha(data),
               "width":w,"height":h,"bytes":len(data),"canvas_id":info['canvas_id'],
               "physical_object_id":record['physical_object_id'],"capture_index":canvas_index,
               "label":f"Manifest image{canvas_index+1} (capture order; not an inferred medieval sequence)",
               "rights_url":info['rights']}
    initial={"path":record['image_path'],**record['image'],"physical_object_id":record['physical_object_id'],"capture_index":0}
    captures=record.setdefault('captures',[initial])
    captures[:]=[c for c in captures if c.get('capture_index')!=canvas_index]
    captures.append(capture)
    captures.sort(key=lambda c:c.get('capture_index',0))
    _dump(root/'data/fragments.json',fragments)
    build_database(root,fragments)
    summary_path=root/'data/ingestion_summary.json'
    if summary_path.exists():
        summary=json.loads(summary_path.read_text())
        files=list((root/'data/images').glob('*.jpg'))
        summary.update(source_image_files=len(files),stored_image_bytes=sum(p.stat().st_size for p in files),
                       new_download_bytes=sum(x.get('bytes_received',0) for x in fetcher.entries))
        _dump(summary_path,summary)
    return capture


def ingest(root, limit=120, offline=False, workers=2):
    """Retrieve/validate120 representative records by default, idempotently."""
    root = Path(root).resolve()
    (root / "data/images").mkdir(parents=True, exist_ok=True)
    plan = make_sample_plan(root, limit, offline=offline)
    fetcher = Fetcher(root, offline=offline)
    rows = _metadata(root, fetcher)
    by_id = {r["signatur"].strip():r for r in rows}
    fragments = []
    def get(spec):
        return _mpo_record(root, by_id[spec["identifier"]], spec, fetcher)
    with concurrent.futures.ThreadPoolExecutor(max_workers=min(2,max(1,workers))) as pool:
        for record in pool.map(get, plan["mpo_records"]):
            fragments.append(record)
            _dump(root / "data/fragments.partial.json", fragments)
            print(f"MPO {record['id']}: {'image' if record['image_path'] else 'metadata only'}", flush=True)
    # Preserve useful known records excluded by missing image fields.
    for identifier in MISSING_IDS:
        if "mpo-" + identifier not in {r["id"] for r in fragments}:
            fragments.append(_mpo_record(root,by_id[identifier],{"role":"control"},fetcher))
    beauvais = []
    failures = []
    for identifier in _beauvais_candidates(root):
        if len(beauvais) >= plan["beauvais_requested"]:
            break
        try:
            record = _beauvais_record(root,identifier,fetcher)
            beauvais.append(record)
            print(f"Beauvais {identifier}: image", flush=True)
        except Exception as error:
            failures.append({"id":identifier,"error":str(error)})
            print(f"Beauvais {identifier}: skipped ({error})",flush=True)
        if len(failures) >= 20:
            break
    fragments.extend(beauvais)
    try:
        finnish = _finnish_record(root)
        fragments.append(finnish)
        if len(finnish["captures"]) > 1:
            alternate = dict(finnish)
            alternate.update(id="finn-iv173-verso", shelfmark="Helsinki F.m.IV.173 (PDF page2)",
                             image_path=finnish["captures"][1]["path"],
                             image={k:v for k,v in finnish["captures"][1].items() if k!="path"},
                             warnings=finnish["warnings"]+["Alternate capture of the same physical leaf; never a separate benchmark object."])
            fragments.append(alternate)
    except Exception as error:
        failures.append({"id":"fm-IV173","error":str(error)})
    fragments.sort(key=lambda r:r["id"])
    # Extra source views added for reconstruction remain provenance-linked on
    # ingestion replay; cache replay must not orphan already downloaded sides.
    existing_path = root / "data/fragments.json"
    previous = {r['id']:r for r in json.loads(existing_path.read_text())} if existing_path.exists() else {}
    for record in fragments:
        earlier = previous.get(record['id'],{})
        if not record.get('captures') and earlier.get('captures'):
            valid=[]
            for capture in earlier['captures']:
                path=root/capture.get('path','')
                if path.is_file() and (not capture.get('sha256') or _sha(path.read_bytes())==capture['sha256']):
                    valid.append(capture)
            if valid:
                record['captures']=valid
    usable = {r["id"] for r in fragments if r.get("image_path")}
    benchmark = {"version":"1.0", "source":MPO_SOURCE,"groups":plan["groups"],
                 "hard_pairs":[
                     {"left_id":"mpo-7960","right_id":"mpo-7961","label":"positive","source":MPO_SOURCE,"subtype":"documented textual continuity"},
                     {"left_id":"mpo-8343","right_id":"mpo-8344","label":"positive","source":MPO_SOURCE,"subtype":"documented textual continuity"},
                     {"left_id":"mpo-8201","right_id":"mpo-8304","label":"negative","source":"https://doi.org/10.25167/ls.4818","subtype":"published same-hand different-book"},
                     {"left_id":"mpo-8201","right_id":"mpo-20106","label":"positive","source":"https://doi.org/10.25167/ls.4818","subtype":"published compatible same-book; image missing"}],
                 "limitations":["Different catalogue labels are a closed-world benchmark assumption, not independently proved negative book identities.",
                                 "Catalogue-derived groups may contain errors; Ant49/Codex1146 is deliberately excluded from positive groups.",
                                 "Discovery targets and unlabelled distractors are never treated as negative labels."]}
    for group in benchmark["groups"]:
        group["planned_member_ids"] = list(group["member_ids"])
        group["member_ids"] = [x for x in group["member_ids"] if x in usable]
    benchmark["groups"].append({"id":"beauvais-missal","split":"control","member_ids":[r["id"] for r in beauvais],
        "label_source":"https://fragmentarium.ms/overview/F-4ihz","label_strength":"published reconstructed same-codex control",
        "limitations":"Single French missal, domain shift; only child records explicitly describing one leaf and permitted rights were used."})
    _dump(root / "data/fragments.json",fragments)
    _dump(root / "data/benchmark.json",benchmark)
    database = build_database(root,fragments)
    image_files = list((root / "data/images").glob("*.jpg"))
    if len(image_files)>MAX_IMAGES:
        raise ValueError("Working-image count exceeds300")
    summary={"completed_at_utc":_now(),"metadata_source":MPO_SOURCE,"metadata_version":"1.0.0 (9October2025)",
             "metadata_sha256":_sha(((root / "research/mpo.csv") if (root / "research/mpo.csv").exists() else (root / "data/raw/mpo.csv")).read_bytes()),
             "records":len(fragments),"records_with_images":len(usable),"source_image_files":len(image_files),
             "physical_objects_with_images":len({r['physical_object_id'] for r in fragments if r.get('image_path')}),
             "collections":dict(__import__('collections').Counter(r['collection'] for r in fragments)),
             "new_download_bytes":sum(x.get('bytes_received',0) for x in fetcher.entries),
             "stored_image_bytes":sum(p.stat().st_size for p in image_files),
             "benchmark_groups":len(benchmark['groups']),"beauvais_records":len(beauvais),
             "metadata_only_records":[r['id'] for r in fragments if not r.get('image_path')],
             "failures":failures,"database":str(database.relative_to(root)),
             "rights_policy":"Explicit child-levelPDM/CC0/CCBY4; no blanket aggregate-rights assumption",
             "restrictions":"No paid API, public hosting, external contact, access-denial bypass, or large original-TIFF harvest."}
    _dump(root / "data/ingestion_summary.json",summary)
    (root / "data/fragments.partial.json").unlink(missing_ok=True)
    return summary


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root",type=Path,default=Path(__file__).resolve().parents[1])
    parser.add_argument("--limit",type=int,default=120)
    parser.add_argument("--offline",action="store_true")
    args=parser.parse_args()
    print(json.dumps(ingest(args.root,args.limit,offline=args.offline),ensure_ascii=False,indent=2))
