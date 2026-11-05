"""Interpretable, label-separated retrieval and a catalogue-derived benchmark.

Ranking compatibility is not manuscript identity or a calibrated probability.
All numerical validation is explicitly conditional on catalogue labels.
"""
from __future__ import annotations

import difflib
import hashlib
import json
import math
import re
from collections import defaultdict
from pathlib import Path
from typing import Any

import numpy as np

EXPERIMENT_VERSION = "1.0.0"
SEED = 20261020
KS = (1, 3, 5, 10)
METHOD_WEIGHTS = {
    "metadata": {"metadata": 1.0},
    "layout": {"layout": 1.0},
    "embedding": {"embedding": 1.0},
    "embedding_raw": {"embedding_raw": 1.0},
    "metadata_layout": {"metadata": .65, "layout": .35},
    "metadata_embedding": {"metadata": .65, "embedding": .35},
    "metadata_text": {"metadata": .80, "text": .20},
    "fusion": {"metadata": .45, "layout": .20, "embedding": .35},
    "fusion_text": {"metadata": .40, "layout": .20, "embedding": .30, "text": .10},
}
# Ordered tie preference penalizes unnecessary complexity. Fixed before test.
METHOD_ORDER = tuple(METHOD_WEIGHTS)
CONFIG = {"version": EXPERIMENT_VERSION, "seed": SEED, "methods": METHOD_WEIGHTS,
          "method_selection": "On development books, maximize same-genre book-macro MRR; require at least0.02 improvement over metadata on development AND calibration before adopting a more complex method. No test-book tuning.",
          "threshold_selection": "Maximize F1 on catalogue-label calibration pairs only; ties prefer fewer false positives then higher threshold. Not probability calibration.",
          "evaluation": "Whole-codex split; leave one physical record out as query; identical within-split galleries; separate same-genre ablation; expected tie-aware metrics; book-macro bootstrap.",
          "feature_whitelist": ["type", "date_min", "date_max", "leaf_cm", "written_cm", "columns", "lines", "script", "notation", "staff_lines", "sanitized catalogue contents"],
          "forbidden_predictors": ["codex", "CCM", "institution", "source/filename semantics", "relationship notes", "account provenance"],
          "model_training": False, "score_is_probability": False}


def _normal(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "").strip().lower())


def genre(record: dict) -> str:
    value = _normal(record.get("normalized", {}).get("type"))
    if "antiph" in value:
        return "antiphonal"
    if "grad" in value or "sequent" in value:
        return "gradual/sequence"
    if "miss" in value:
        return "missal"
    return value or "unknown"


def sanitize_contents(text: Any) -> list[str]:
    """Remove explicit cross-reference clauses/IDs before content comparison.

    This is catalogue-summary overlap, not OCR or a chant transcription.
    """
    text = str(text or "")
    text = re.sub(r"\([^)]*(?:Fr\s*\d|fortsetzung|beginn|vgl|codex|taitto)[^)]*\)", " ", text, flags=re.I)
    text = re.sub(r"(?:Fr(?:agment)?\.?\s*\d+|Codex\s*\d+|CCM\s*\w+\s*\d+|HUB\s*\w+\s*\d+)", " ", text, flags=re.I)
    text = re.sub(r"\b(?:fortsetzung|beginn|derselbe|siehe|vgl)\b.*", " ", text, flags=re.I)
    stop = {"proprium", "sanctis", "tempore", "de", "et", "in", "ad", "rv", "fer", "dom", "ah", "nr", "fol", "hy", "ro", "off", "commem", "beauvais", "missal", "graduale", "aboense", "fragmentarium"}
    return [x for x in re.findall(r"[^\W\d_]{3,}", text.lower(), flags=re.UNICODE) if x not in stop]


def metadata_score(a: dict, b: dict) -> tuple[float, float, list[dict]]:
    aa, bb = a.get("normalized", {}), b.get("normalized", {})
    observed: list[tuple[float, float, str]] = []
    if genre(a) != "unknown" and genre(b) != "unknown":
        observed.append((1.0 if genre(a) == genre(b) else 0.0, .7, "manuscript type"))
    for field, weight in (("script", 1), ("notation", 1), ("staff_lines", .8), ("columns", 1), ("lines", 1)):
        x, y = aa.get(field), bb.get(field)
        if x is None or y is None or not str(x).strip() or not str(y).strip():
            continue
        if field == "lines":
            try:
                value = math.exp(-abs(float(x) - float(y)) / 3)
            except (TypeError, ValueError):
                value = float(_normal(x) == _normal(y))
        else:
            value = float(_normal(x).replace("?", "") == _normal(y).replace("?", ""))
        observed.append((value, weight, field))
    for field in ("leaf_cm", "written_cm"):
        x, y = aa.get(field), bb.get(field)
        if isinstance(x, list) and isinstance(y, list) and len(x) == len(y) == 2 and all(isinstance(v, (int, float)) and v > 0 for v in x + y):
            # Same source convention only. Finnish prose dimensions are not
            # assumed equivalent to Swedish structured leaf measurements.
            if a.get("collection") == b.get("collection"):
                delta = sum(abs(math.log(float(u) / float(v))) for u, v in zip(x, y)) / 2
                observed.append((math.exp(-delta / .13), 1.5, field))
    if all(isinstance(aa.get(k), (int, float)) and isinstance(bb.get(k), (int, float)) for k in ("date_min", "date_max")):
        distance = max(0, max(aa["date_min"], bb["date_min"]) - min(aa["date_max"], bb["date_max"]))
        observed.append((math.exp(-distance / 100), .5, "catalogue date range"))
    weight = sum(w for _, w, _ in observed)
    if not weight:
        return .5, 0.0, []
    value = sum(v * w for v, w, _ in observed) / weight
    coverage = min(1.0, weight / 9.0)
    # Missing values are not exclusions or positive agreements. Low observed
    # coverage shrinks compatibility toward neutral, not toward false truth.
    value = .5 + (value - .5) * coverage
    return float(value), coverage, [{"signal": name, "compatibility": round(v, 5), "weight": w} for v, w, name in observed]


def text_score(a: dict, b: dict) -> float:
    ta = sanitize_contents(a.get("normalized", {}).get("contents"))
    tb = sanitize_contents(b.get("normalized", {}).get("contents"))
    if not ta or not tb:
        return .5
    sa, sb = set(ta), set(tb)
    jaccard = len(sa & sb) / len(sa | sb)
    ordered = difflib.SequenceMatcher(None, ta, tb, autojunk=False).ratio()
    return (jaccard + ordered) / 2


def load_inputs(root: str | Path) -> tuple[Path, list[dict], dict, dict]:
    root = Path(root).resolve()
    records = json.loads((root / "data" / "fragments.json").read_text())
    features = np.load(root / "data" / "features.npz", allow_pickle=False)
    feature_ids = list(features["ids"].astype(str))
    by_id = {r["id"]: r for r in records}
    missing = [x for x in feature_ids if x not in by_id]
    if missing:
        raise ValueError(f"Feature IDs absent from source records: {missing}")
    return root, [by_id[x] for x in feature_ids], {k: features[k] for k in features.files}, json.loads((root / "data" / "features.json").read_text())


def build_matrices(records: list[dict], arrays: dict) -> dict[str, np.ndarray]:
    n = len(records)
    meta, text = np.full((n, n), .5), np.full((n, n), .5)
    for i in range(n):
        for j in range(i, n):
            meta[i, j] = meta[j, i] = metadata_score(records[i], records[j])[0]
            text[i, j] = text[j, i] = text_score(records[i], records[j])
    base = {"metadata": meta, "text": text,
            "layout": np.clip((arrays["layout"] @ arrays["layout"].T + 1) / 2, 0, 1),
            "embedding": np.clip(arrays["embedding"] @ arrays["embedding"].T, 0, 1),
            "embedding_raw": np.clip(arrays["raw_embedding"] @ arrays["raw_embedding"].T, 0, 1)}
    result = {name: sum(base[k] * w for k, w in weights.items()) for name, weights in METHOD_WEIGHTS.items()}
    result.update({"_metadata": meta, "_text": text, "_layout": base["layout"], "_embedding": base["embedding"], "_embedding_raw": base["embedding_raw"]})
    return result


def expected_metrics(scores: list[float], relevant: list[bool], ks=KS) -> dict[str, float]:
    """Exact expectation over random orders within equal-score ties."""
    if len(scores) != len(relevant) or not any(relevant):
        raise ValueError("Metrics require a nonempty known-positive gallery")
    buckets: dict[float, list[bool]] = defaultdict(list)
    for value, label in zip(scores, relevant):
        buckets[round(float(value), 10)].append(bool(label))
    groups = [(v, buckets[v]) for v in sorted(buckets, reverse=True)]
    positives = sum(relevant)
    result = {}
    for k in ks:
        effective_k = min(k, len(scores))
        remaining, expected_hits, no_hit_probability = effective_k, 0.0, 1.0
        for _, labels in groups:
            if remaining <= 0:
                break
            take = min(remaining, len(labels))
            hits = sum(labels)
            expected_hits += take * hits / len(labels)
            if hits:
                no_hit_probability *= 0.0 if take > len(labels) - hits else math.comb(len(labels) - hits, take) / math.comb(len(labels), take)
            remaining -= take
        result[f"precision@{k}"] = expected_hits / effective_k if effective_k else 0
        result[f"recall@{k}"] = expected_hits / positives
        result[f"hit@{k}"] = 1 - no_hit_probability
    before, reciprocal = 0, 0.0
    for _, labels in groups:
        m, n = sum(labels), len(labels)
        if m:
            denominator = math.comb(n, m)
            reciprocal = sum(math.comb(n - t, m - 1) / denominator / (before + t) for t in range(1, n - m + 2))
            break
        before += n
    result["mrr"] = reciprocal
    return result


def _mean(rows: list[dict]) -> dict[str, float]:
    return {key: float(np.mean([r[key] for r in rows])) for key in rows[0]} if rows else {}


def _bootstrap(group_metrics: list[dict]) -> dict[str, list[float]]:
    if not group_metrics:
        return {}
    rng = np.random.default_rng(SEED)
    result = {}
    for key in group_metrics[0]:
        values = np.asarray([x[key] for x in group_metrics])
        draws = values[rng.integers(0, len(values), size=(1000, len(values)))].mean(axis=1)
        result[key] = [float(x) for x in np.quantile(draws, [.025, .975])]
    return result


def _groups(benchmark: dict, present: set[str]) -> list[dict]:
    groups = []
    seen = {}
    for group in benchmark.get("groups", []):
        copied = dict(group)
        members = group.get("member_ids", group.get("members", []))
        members = [x if isinstance(x, str) else x.get("id") for x in members]
        copied["member_ids"] = [x for x in members if x in present]
        copied["missing_members"] = [x for x in members if x not in present]
        for x in copied["member_ids"]:
            if x in seen:
                raise ValueError(f"Physical record {x} belongs to multiple benchmark groups: {seen[x]}, {group['id']}")
            seen[x] = group["id"]
        groups.append(copied)
    return groups


def representative_indices(records: list[dict]) -> list[int]:
    """One gallery/query representative per physical object, not per view."""
    choices = {}
    for index, record in enumerate(records):
        physical = record.get("physical_object_id") or record["id"]
        if physical not in choices or record["id"] == physical:
            choices[physical] = index
    return sorted(choices.values())


def _evaluate_split(records, matrices, groups, split, same_genre=False):
    index = {r["id"]: i for i, r in enumerate(records)}
    by_id = {r["id"]: r for r in records}
    chosen = [g for g in groups if g.get("split") == split and len(g["member_ids"]) >= 2]
    pool = [x for g in chosen for x in g["member_ids"]]
    by_method = {}
    excluded_queries = []
    for method in METHOD_ORDER:
        group_results = []
        queries = []
        for group in chosen:
            qmetrics = []
            for query in group["member_ids"]:
                gallery = [x for x in pool if x != query and (not same_genre or genre(by_id[x]) == genre(by_id[query]))]
                truth = [x in group["member_ids"] for x in gallery]
                if not any(truth):
                    continue
                if not any(not x for x in truth):
                    if method == METHOD_ORDER[0]:
                        excluded_queries.append({"query_id": query, "group_id": group["id"], "reason": "No other reference book supplies a negative in this gallery; all-positive retrieval is trivial."})
                    continue
                values = [float(matrices[method][index[query], index[x]]) for x in gallery]
                metrics = expected_metrics(values, truth)
                qmetrics.append(metrics)
                queries.append({"query_id": query, "group_id": group["id"], "gallery_size": len(gallery), "known_relevant": sum(truth), "metrics": metrics})
            if qmetrics:
                group_results.append({"group_id": group["id"], "queries": len(qmetrics), "metrics": _mean(qmetrics)})
        macro = _mean([g["metrics"] for g in group_results])
        by_method[method] = {"book_macro": macro,
                             "book_bootstrap_95_interval": _bootstrap([g["metrics"] for g in group_results]),
                             "book_count": len(group_results), "query_count": len(queries),
                             "groups": group_results, "queries": queries}
    evaluated_books = by_method[METHOD_ORDER[0]]["book_count"]
    return {"split": split, "same_genre_gallery": same_genre, "reference_book_count": len(chosen),
            "book_count": evaluated_books, "gallery_records": len(pool), "excluded_queries": excluded_queries, "methods": by_method}


def _pair_outcomes(records, matrix, groups, split):
    index = {r["id"]: i for i, r in enumerate(records)}
    chosen = [g for g in groups if g.get("split") == split and len(g["member_ids"]) >= 2]
    labels = {x: g["id"] for g in chosen for x in g["member_ids"]}
    ids = sorted(labels)
    by_id = {r["id"]: r for r in records}
    genre_books = defaultdict(set)
    for identifier in ids:
        genre_books[genre(by_id[identifier])].add(labels[identifier])
    return [(float(matrix[index[a], index[b]]), labels[a] == labels[b])
            for i, a in enumerate(ids) for b in ids[i + 1:]
            if genre(by_id[a]) == genre(by_id[b]) and len(genre_books[genre(by_id[a])]) >= 2]


def _threshold(pairs):
    if not pairs:
        return {"threshold": 1.000001, "reason": "No calibration pairs; reject all rather than invent calibration."}
    candidates = sorted({x[0] for x in pairs} | {1.000001})
    best = None
    for threshold in candidates:
        tp = sum(label and score >= threshold for score, label in pairs)
        fp = sum(not label and score >= threshold for score, label in pairs)
        fn = sum(label and score < threshold for score, label in pairs)
        f1 = 2 * tp / (2 * tp + fp + fn) if 2 * tp + fp + fn else 0.0
        key = (f1, -fp, threshold)
        if best is None or key > best[0]:
            best = (key, {"threshold": threshold, "calibration_f1": f1, "calibration_tp": tp, "calibration_fp": fp, "calibration_fn": fn})
    return best[1]


def _confusion(pairs, threshold):
    tp = sum(label and score >= threshold for score, label in pairs)
    fp = sum(not label and score >= threshold for score, label in pairs)
    fn = sum(label and score < threshold for score, label in pairs)
    tn = sum(not label and score < threshold for score, label in pairs)
    return {"tp": tp, "fp": fp, "fn": fn, "tn": tn,
            "precision": tp / (tp + fp) if tp + fp else None,
            "recall": tp / (tp + fn) if tp + fn else None,
            "false_positive_rate": fp / (fp + tn) if fp + tn else None}


def evaluate(root: str | Path) -> dict:
    root, records, arrays, feature_summary = load_inputs(root)
    benchmark = json.loads((root / "data" / "benchmark.json").read_text())
    groups = _groups(benchmark, {r["id"] for r in records})
    # Detect exact capture aliases, including differently named source rows.
    reference_ids = {x for g in groups for x in g["member_ids"]}
    physical_seen, capture_seen = {}, {}
    for record in records:
        if record["id"] not in reference_ids:
            continue
        physical = record.get("physical_object_id") or record["id"]
        capture = record.get("image", {}).get("sha256")
        if physical in physical_seen:
            raise ValueError(f"Reference records share physical object {physical}: {physical_seen[physical]}, {record['id']}")
        if capture and capture in capture_seen:
            raise ValueError(f"Reference records share exact image bytes: {capture_seen[capture]}, {record['id']}")
        physical_seen[physical] = record["id"]
        if capture:
            capture_seen[capture] = record["id"]
    matrices = build_matrices(records, arrays)
    (root / "data" / "experiment_config.json").write_text(json.dumps(CONFIG, indent=2) + "\n")
    results = {split: {"all_genres": _evaluate_split(records, matrices, groups, split),
                       "same_genre": _evaluate_split(records, matrices, groups, split, True)}
               for split in ("development", "calibration", "test")}
    for split in results:
        if results[split]["same_genre"]["book_count"] < 2:
            raise ValueError(f"Need at least two independently labelled reference groups in {split}")
    dev = results["development"]["same_genre"]["methods"]
    cal = results["calibration"]["same_genre"]["methods"]
    baseline_dev = dev["metadata"]["book_macro"].get("mrr", 0)
    baseline_cal = cal["metadata"]["book_macro"].get("mrr", 0)
    ranked = sorted(METHOD_ORDER, key=lambda m: (-dev[m]["book_macro"].get("mrr", 0), METHOD_ORDER.index(m)))
    eligible = [m for m in ranked if m == "metadata" or (dev[m]["book_macro"].get("mrr", 0) - baseline_dev >= .02 and cal[m]["book_macro"].get("mrr", 0) - baseline_cal >= .02)]
    selected = eligible[0] if eligible else "metadata"
    thresholds = {}
    for method in METHOD_ORDER:
        threshold = _threshold(_pair_outcomes(records, matrices[method], groups, "calibration"))
        threshold["test_confusion_catalogue_labels"] = _confusion(_pair_outcomes(records, matrices[method], groups, "test"), threshold["threshold"])
        thresholds[method] = threshold

    # Hard pairs are external diagnostic controls, never tuning inputs.
    index = {r["id"]: i for i, r in enumerate(records)}
    hard_pairs = benchmark.get("hard_pairs", [])
    if not hard_pairs:
        hard_pairs = [{"left_id": "mpo-8201", "right_id": "mpo-8304", "label": "negative", "subtype": "published same-hand/different-book", "source": "https://doi.org/10.25167/ls.4818"},
                      {"left_id": "mpo-7960", "right_id": "mpo-7961", "label": "positive", "subtype": "published continuity", "source": "https://zenodo.org/records/17287665"},
                      {"left_id": "mpo-8343", "right_id": "mpo-8344", "label": "positive", "subtype": "published continuity", "source": "https://zenodo.org/records/17287665"}]
    controls = []
    representatives = representative_indices(records)
    for pair in hard_pairs:
        a, b = pair.get("left_id"), pair.get("right_id")
        entry = dict(pair)
        if a not in index or b not in index:
            entry.update(evaluable=False, reason="A source object lacks usable image features.")
        else:
            entry.update(evaluable=True, methods={})
            i, j = index[a], index[b]
            for method in METHOD_ORDER:
                value = float(matrices[method][i, j])
                physical = records[i].get("physical_object_id") or records[i]["id"]
                gallery = [float(matrices[method][i, k]) for k in representatives if (records[k].get("physical_object_id") or records[k]["id"]) != physical]
                entry["methods"][method] = {"score": value,
                    "rank_interval_all_imaged_records": [1 + sum(s > value + 1e-10 for s in gallery), sum(s >= value - 1e-10 for s in gallery)],
                    "accepted_at_catalogue_calibration_threshold": value >= thresholds[method]["threshold"]}
        controls.append(entry)

    positive_controls = []
    for group in groups:
        if group.get("split") != "control" or len(group["member_ids"]) < 2:
            continue
        output = {"group_id": group["id"], "source": group.get("label_source"),
                  "known_members": len(group["member_ids"]), "gallery_physical_objects": len(representatives),
                  "scope": "Known-membership retrieval among the whole sample. Other objects are not adjudicated negatives; no precision or false-positive rate is claimed. Beauvais differs in geography, genre and capture from Nordic wrappers, so metadata/domain shortcuts can make this easy.",
                  "methods": {}}
        for method in METHOD_ORDER:
            rows = []
            for query in group["member_ids"]:
                i = index[query]
                physical = records[i].get("physical_object_id") or query
                gallery = [k for k in representatives if (records[k].get("physical_object_id") or records[k]["id"]) != physical]
                metrics = expected_metrics([float(matrices[method][i, k]) for k in gallery], [records[k]["id"] in group["member_ids"] for k in gallery])
                rows.append({key: value for key, value in metrics.items() if not key.startswith("precision")})
            output["methods"][method] = _mean(rows)
        positive_controls.append(output)

    # Similarity strata are catalogue-derived stress tests, not independent
    # proof of different scribes or exact identical chant transcriptions.
    by_id = {r["id"]: r for r in records}
    test_groups = [g for g in groups if g.get("split") == "test"]
    book = {x: g["id"] for g in test_groups for x in g["member_ids"]}
    strata = defaultdict(list)
    tids = sorted(book)
    for at, a in enumerate(tids):
        for b in tids[at + 1:]:
            if book[a] == book[b]:
                continue
            na, nb = by_id[a].get("normalized", {}), by_id[b].get("normalized", {})
            kinds = []
            if genre(by_id[a]) == genre(by_id[b]):
                kinds.append("same_manuscript_genre_distinct_catalogue_books")
            if na.get("notation") and na.get("notation") == nb.get("notation"):
                kinds.append("same_notation_distinct_catalogue_books")
            if na.get("origin") and _normal(na.get("origin")) == _normal(nb.get("origin")):
                kinds.append("same_catalogued_origin_distinct_catalogue_books")
            shared = sorted(set(sanitize_contents(na.get("contents"))) & set(sanitize_contents(nb.get("contents"))))
            if len(shared) >= 2:
                kinds.append("overlapping_catalogue_content_terms_distinct_books")
            if matrices["embedding"][index[a], index[b]] >= .9:
                kinds.append("high_generic_visual_similarity_distinct_catalogue_books")
            for kind in kinds:
                strata[kind].append({"left_id": a, "right_id": b, "score": float(matrices[selected][index[a], index[b]]), "shared_content_terms": shared[:8]})
    strata_report = {kind: {"pairs": len(pairs), "false_acceptances_at_selected_threshold": sum(p["score"] >= thresholds[selected]["threshold"] for p in pairs), "examples": pairs[:5], "label_strength": "different catalogue book IDs, not independently adjudicated manuscript/scribe separation"} for kind, pairs in strata.items()}
    test = results["test"]["same_genre"]["methods"]
    selected_test = test[selected]["book_macro"]
    meta_test = test["metadata"]["book_macro"]
    # A failed held-out improvement is not a license to tune on this test.
    generalizes = selected == "metadata" or selected_test.get("mrr", 0) > meta_test.get("mrr", 0)
    recommended = selected if generalizes else "metadata"
    summary = {"experiment_version": EXPERIMENT_VERSION,
        "scope": "Closed-world retrieval against provisional catalogue-derived book labels, with separate literature controls; not expert-validated attribution accuracy.",
        "sample_images": len(records), "sample_physical_objects": len(representatives), "groups": groups, "results": results,
        "selection": {"chosen_on_development_and_calibration": selected, "recommended_retrieval_method": recommended,
                      "preselection_used_test_labels": False,
                      "held_out_improvement_survived": generalizes,
                      "conservative_fallback_after_failed_holdout": not generalizes,
                      "deployment_fallback_uses_test_outcome": not generalizes,
                      "reason": "Complex methods require >=0.02 MRR gain on both development and calibration; no new tuning on test. If a preselected complex method fails held-out improvement, retain metadata rather than claim useful advanced evidence. That conservative deployment fallback uses the test outcome and is not an unbiased new method-selection estimate.",
                      "development_mrr": {m: dev[m]["book_macro"].get("mrr") for m in METHOD_ORDER},
                      "calibration_mrr": {m: cal[m]["book_macro"].get("mrr") for m in METHOD_ORDER},
                      "test_mrr_delta_over_metadata": {m: test[m]["book_macro"].get("mrr", 0) - meta_test.get("mrr", 0) for m in METHOD_ORDER}},
        "thresholds": thresholds, "literature_controls": controls, "positive_reconstruction_controls": positive_controls, "hard_negative_strata": strata_report,
        "model": feature_summary.get("encoder"), "config": CONFIG,
        "reproducibility": {"fragments_sha256": hashlib.sha256((root / "data" / "fragments.json").read_bytes()).hexdigest(),
                            "benchmark_sha256": hashlib.sha256((root / "data" / "benchmark.json").read_bytes()).hexdigest(),
                            "features_sha256": hashlib.sha256((root / "data" / "features.npz").read_bytes()).hexdigest(),
                            "matching_code_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},
        "limitations": ["Distinct catalogue codex labels can still contain errors or cross-label identities; these are provisional reference labels, not expert gold.",
                        "Only four test book groups are expected; book-bootstrap intervals are descriptive and unstable with few groups.",
                        "Physical record separation removes self/capture duplicates, but each source row may contain more than one leaf.",
                        "Catalogue attributes may be copied from prior grouping, so metadata can leak identity indirectly despite the feature whitelist.",
                        "Generic ImageNet features may learn capture/provider/colour shortcuts; raw/cropped and same-genre ablations do not eliminate all confounding.",
                        "Overlap of catalogue content terms is not proof of identical chant text, melody or textual continuity.",
                        "No independently adjudicated different-scribe handwriting dataset or reliable probability calibration was secured.",
                        "Pretrained data exposure cannot be audited fully. No model was trained or fine-tuned here.",
                        "Strong discovery claims are prohibited by these limitations and the unread target-specific later scholarship."]}
    (root / "data" / "validation.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n")
    return summary


def _association(a: dict, b: dict) -> tuple[str, str]:
    ids = {a["id"], b["id"]}
    if ids == {"mpo-8201", "mpo-8304"}:
        return "D", "Published different-book interpretation despite the shared hand/catalogue label; DOI10.25167/ls.4818 p293."
    known_157 = {"mpo-1385", "mpo-20274", "mpo-20275", "mpo-20276", "mpo-20277", "mpo-20278"}
    codex1505 = {"mpo-8994", "mpo-10370", "mpo-10406", "mpo-10407", "mpo-10437"}
    raw_a, raw_b = a.get("raw", {}), b.get("raw", {})
    if a["id"].startswith("fragmentarium-") and b["id"].startswith("fragmentarium-") and raw_a.get("Title") == raw_b.get("Title") == "Beauvais Missal":
        return "E", "Published members of the Beauvais Missal reconstruction; this is a known positive control, not a new attribution."
    ca, cb = raw_a.get("codex", "").strip(), raw_b.get("codex", "").strip()
    if ids <= known_157:
        return "E", "Already linked to IV.157 in the Finnish catalogue; retrieval is replication, not discovery."
    if (ids & known_157 and ids & codex1505) or ("finn-iv173" in ids and ids & (known_157 | {"mpo-25592", "mpo-29666"})):
        return "E", "A related/suggested association already appears in the target catalogues; its strength and later scholarship need review."
    if ca and ca == cb and ca != "Codex 1146":
        return "E", "Same existing catalogue codex label; provisional documented grouping, not a new attribution."
    return "C", "Retrieval candidate only: visual/descriptive compatibility is ambiguous and originality is unverified."


def rank_candidates(root: str | Path, top_k: int = 5) -> list[dict]:
    root, records, arrays, _ = load_inputs(root)
    matrices = build_matrices(records, arrays)
    validation_path = root / "data" / "validation.json"
    if not validation_path.exists():
        raise ValueError("Run the known-relationship evaluation before searching target candidates")
    validation = json.loads(validation_path.read_text())
    method = validation["selection"]["recommended_retrieval_method"]
    output = []
    representatives = representative_indices(records)
    for i, left in enumerate(records):
        # Broad images remain in the searchable database, but candidate search
        # focuses on the selected research target and known controls.
        if i not in representatives or left.get("role") not in ("target", "control"):
            continue
        physical = left.get("physical_object_id") or left["id"]
        ranked = sorted((j for j in representatives if (records[j].get("physical_object_id") or records[j]["id"]) != physical), key=lambda j: (-float(matrices[method][i, j]), records[j]["id"]))
        for ordinal, j in enumerate(ranked[:top_k], 1):
            right = records[j]
            score = float(matrices[method][i, j])
            equivalent = [k for k in ranked if abs(float(matrices[method][i, k]) - score) < 1e-10]
            better = sum(float(matrices[method][i, k]) > score + 1e-10 for k in ranked)
            meta, coverage, evidence = metadata_score(left, right)
            classification, known_reason = _association(left, right)
            shared = sorted(set(sanitize_contents(left.get("normalized", {}).get("contents"))) & set(sanitize_contents(right.get("normalized", {}).get("contents"))))
            output.append({"left_id": left["id"], "right_id": right["id"], "rank": ordinal,
                           "rank_interval": [better + 1, better + len(equivalent)], "method": method, "score": score,
                           "scores": {"metadata": meta, "metadata_coverage": coverage,
                                      "layout": float(matrices["_layout"][i, j]), "embedding": float(matrices["_embedding"][i, j]),
                                      "embedding_raw": float(matrices["_embedding_raw"][i, j]), "catalogue_text": float(matrices["_text"][i, j])},
                           "evidence": evidence + ([{"signal": "shared catalogue content terms", "terms": shared[:10]}] if shared else []),
                           "classification": classification, "classification_reason": known_reason,
                           "originality": "previously documented association or suggestion" if classification == "E" else "not established",
                           "cautions": ["Compatibility score is not an identity probability.", "Text/chant continuity, individual letterforms and physical joins have not been independently verified.", "Current target-specific novelty is uncleared until later scholarship and expert review."]})
    (root / "data" / "matches.json").write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n")
    return output


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("evaluate", "match", "all"))
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--top-k", type=int, default=5)
    args = parser.parse_args()
    if args.command in ("evaluate", "all"):
        result = evaluate(args.root)
        print(json.dumps(result["selection"], indent=2))
    if args.command in ("match", "all"):
        print(f"Ranked {len(rank_candidates(args.root, args.top_k))} target/control suggestions")
