"""Retrospective Phase 0 diagnostic, NOT a validated manuscript matcher.

Run from any directory: python3 research/metadata_retrieval_diagnostic.py
Uses the cached CC0 MPO export only. No model is trained, no images are
classified, and no unlabelled catalogue pair is assumed to be a negative.
All judgement labels are evaluator-only and never enter feature extraction.
"""
import csv
import hashlib
import json
import pathlib
import re
from fractions import Fraction

ROOT = pathlib.Path(__file__).resolve().parent
CSV = ROOT / "mpo.csv"
OUT = ROOT / "metadata_retrieval_diagnostic.json"
FIELDS = ("schrift", "notation", "notenlinien", "spaltenzahl", "zeilenzahl1")
DIM_FIELDS = ("format", "schriftraum1")
ALLOWED = {"sachtitel", *FIELDS, *DIM_FIELDS}
FORBIDDEN = {"codex", "ccmsignum", "anmerkungen", "inhalt", "literatur", "entstehungsort", "institution", "bildbetrachter", "iiif_manifest"}
assert not ALLOWED & FORBIDDEN


def features(row):
    # Only independently catalogued descriptive attributes are used. These
    # may themselves inherit parent-group descriptions; no blindness claim
    # is possible without an expert source audit.
    selected = {field: row[field].strip() for field in ALLOWED}
    dims = {}
    for field in DIM_FIELDS:
        match = re.fullmatch(r"[ *?]*(\d+(?:\.\d+)?)\s*x\s*[ *?]*(\d+(?:\.\d+)?)[ *?]*", selected[field])
        dims[field] = tuple(float(x) for x in match.groups()) if match else None
    return {"type": selected["sachtitel"],
            "categorical": {field: selected[field] for field in FIELDS},
            "dimensions": dims,
            "dimension_raw": {field: selected[field] for field in DIM_FIELDS}}


def score(a, b):
    agreements = []
    for field in FIELDS:
        x, y = a["categorical"][field], b["categorical"][field]
        if not x or not y:
            return None
        agreements.append({"field": field, "match": x == y, "query": x, "candidate": y})
    for field in DIM_FIELDS:
        x, y = a["dimensions"][field], b["dimensions"][field]
        if x is None or y is None:
            return None
        for index in (0, 1):
            agreements.append({"field": field + ("_height" if index == 0 else "_width"),
                               "match": abs(x[index] - y[index]) <= .50000001,
                               "query": x[index], "candidate": y[index]})
    return Fraction(sum(x["match"] for x in agreements), 9), agreements


rows = list(csv.DictReader(CSV.open(encoding="utf-8-sig", newline="")))
by_id = {row["signatur"]: row for row in rows}
feature_map = {identifier: features(row) for identifier, row in by_id.items()}

# This diagnostic was deliberately selected after known relationships had
# already been researched. It is not a preregistered or blind benchmark.
reference_pairs = [
    {"query": "7960", "candidate": "7961", "relationship": "documented same-codex textual continuity",
     "source": "https://zenodo.org/records/17287665", "label": "positive"},
    {"query": "8343", "candidate": "8344", "relationship": "documented same-codex textual continuity",
     "source": "https://zenodo.org/records/17287665", "label": "positive"},
    {"query": "8201", "candidate": "20106", "relationship": "published same-codex text continuity",
     "source": "https://doi.org/10.25167/ls.4818", "page": 293, "label": "positive"},
    {"query": "8201", "candidate": "8304", "relationship": "published same-hand, different-book comparison",
     "source": "https://doi.org/10.25167/ls.4818", "page": 293, "label": "negative"},
]

results = []
for reference in reference_pairs:
    qid, cid = reference["query"], reference["candidate"]
    query, candidate = feature_map[qid], feature_map[cid]
    # Gallery selection uses exact manuscript type and complete descriptive
    # features, never CCM/codex assignments, account sequences or identifiers.
    gallery = []
    population = 0
    for identifier, f in feature_map.items():
        if identifier == qid or f["type"] != query["type"]:
            continue
        population += 1
        comparison = score(query, f)
        if comparison is not None:
            gallery.append((identifier, comparison[0]))
    pair_score = score(query, candidate)
    result = dict(reference)
    result.update(genre=query["type"], query_features=query, candidate_features=candidate,
                  gallery_before_complete_case_filter=population,
                  gallery_after_complete_case_filter=len(gallery),
                  candidate_eligible=pair_score is not None)
    if pair_score is not None:
        value, detail = pair_score
        better = sum(s > value for _, s in gallery)
        equal = sum(s == value for _, s in gallery)
        result.update(score_fraction=str(value), score=float(value), feature_agreements=detail,
                      best_possible_tie_rank=better + 1, worst_possible_tie_rank=better + equal,
                      tied_candidates=equal)
    else:
        result["missing_candidate_fields"] = [field for field in FIELDS if not candidate["categorical"][field]] + [field for field in DIM_FIELDS if candidate["dimensions"][field] is None]
    results.append(result)

output = {
    "purpose": "Retrospective diagnostic of metadata retrieval and complete-case filtering failure; not AI performance validation",
    "source": "https://zenodo.org/records/17287665",
    "csv_sha256": hashlib.sha256(CSV.read_bytes()).hexdigest(),
    "script_sha256": hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),
    "feature_whitelist": sorted(ALLOWED),
    "scoring": "Five exact categorical agreements and four observed-dimension component agreements, each weight1; numeric tolerance0.5cm; all9 required; same genre gallery; no identifier tie-break",
    "dimension_caution": "Asterisks/questionmarks remain in recorded raw values; numerical comparison of damaged sizes is deliberately weak compatibility evidence, not original-size inference",
    "complete_case_filter_is_intentionally_tested_not_recommended": True,
    "results": results,
    "claims_not_supported": ["population precision or recall", "image or AI performance", "book-independent generalization", "new fragment identity", "calibrated confidence"],
}
OUT.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n")
for result in results:
    print(json.dumps({key: result[key] for key in ("query", "candidate", "label", "candidate_eligible", "gallery_before_complete_case_filter", "gallery_after_complete_case_filter", "score", "best_possible_tie_rank", "worst_possible_tie_rank", "missing_candidate_fields") if key in result}))
