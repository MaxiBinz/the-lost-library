"""Provenance-preserving manuscript knowledge and complete lead-register overlay.

No identity closure, score calibration, network access or source-record writes.
"""
from __future__ import annotations

import collections
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import quote

DATE = "2026-11-02"
VERSION = "1.48.0"
STATES = {"supported", "contradicted", "unresolved", "previously_documented", "not_testable"}
BASES = {"source_assertion", "project_observation", "computational_suggestion", "researcher_interpretation"}
RELATIONS = {"same_codex", "physical_join", "photographic_overlap", "textual_continuation", "same_hand", "stylistic_similarity", "liturgical_relationship", "suggested_association", "assigned_to_reconstruction", "member_of_group", "part_of", "describes", "capture_of", "derivative_of", "method_correction", "chant_identification", "numbering_conflict", "melodic_excerpt_comparison"}
TYPES = {"Codex", "PhysicalFragment", "FragmentSet", "Leaf", "Side", "CatalogRecord", "Identifier", "Capture", "ImageDerivative", "Source", "Agent", "StylisticGroup", "ResearchQuestion", "Method", "Chant"}
FROZEN = ["data/hypotheses.v1.json", "data/hypothesis_reviews.v1.json", "data/matches.json", "data/validation.json", "data/features.json"]
REQUIRED = ["RESEARCH_GOAL.md", "PROJECT_STATE.md", "OPEN_QUESTIONS.md", "CANDIDATES.md", "EVIDENCE_DOSSIERS.md", "MATCHING_RESULTS.md", "INDEPENDENT_RESEARCH_PASS.md", "DATA_RIGHTS.md", "THIRD_PARTY.md", "SCIENTIFIC_LIMITATIONS.md", "IMPLEMENTATION_CONTRACT.md", "viewer/README.md"]


def digest(data):
    return hashlib.sha256(data).hexdigest()


def read(root, path):
    return json.loads((root / path).read_text())


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def pair_key(a, b):
    return tuple(sorted((a, b)))


def pair_id(pair):
    return "pair-" + digest("|".join(pair).encode())[:20]


def catalogue_comparison(left, right):
    """Descriptive comparison only; missing and differing fields are not negatives."""
    fields = ["type", "date_raw", "leaf_cm", "written_cm", "columns", "lines", "script", "notation", "staff_lines", "contents", "origin", "use_place", "material"]
    a, b = left.get("normalized", {}), right.get("normalized", {})
    rows = []
    for field in fields:
        av, bv = a.get(field), b.get(field)
        outcome = "missing" if av is None or bv is None else ("equal" if av == bv else "different")
        rows.append({"field": field, "left_value": av, "right_value": bv, "comparison": outcome})
    dates = [a.get("date_min"), a.get("date_max"), b.get("date_min"), b.get("date_max")]
    date_overlap = None if any(x is None for x in dates) else max(dates[0], dates[2]) <= min(dates[1], dates[3])
    units = {key: {"left": left.get("raw", {}).get(key) or None, "right": right.get("raw", {}).get(key) or None} for key in ["codex", "ccmsignum"]}
    return {"basis": "source_assertion", "source": "data/fragments.json", "records": [left["id"], right["id"]], "fields": rows,
            "recorded_date_intervals_overlap": date_overlap, "catalogue_reconstruction_labels": units,
            "limits": ["Normalized inherited catalogue descriptions, not new pixel measurements or independent labels.", "Different contents can occupy different leaves of one book. Trimming, mixed sections, composite structure and catalogue errors remain possible.", "Equal fields and overlapping dates are compatibility only; missing fields are unknown. No score, exclusion or same-codex status is inferred."]}


def build_knowledge(root: Path):
    before = {p: digest((root / p).read_bytes()) for p in FROZEN}
    records = read(root, "data/fragments.json")
    comparisons = read(root, "data/comparison_sources.v1.json")
    matches = read(root, "data/matches.json")
    hypotheses = read(root, "data/hypotheses.v1.json")["hypotheses"]
    review_doc = read(root, "data/hypothesis_reviews.v1.json")
    reviews = {r["id"]: r for r in review_doc["reviews"]}
    annotations = read(root, review_doc["observations_path"])["annotations"]
    annotations += read(root, "research/continuation_33/observations.json")["annotations"]
    annotations += read(root, "research/continuation_34/observations.json")["annotations"]
    annotations += read(root, "research/continuation_36/observations.json")["annotations"]
    annotations += read(root, "research/continuation_37/observations.json")["annotations"]
    annotations += read(root, "research/continuation_38/observations.json")["annotations"]
    annotations += read(root, "research/continuation_39/observations.json")["annotations"]
    annotations += read(root, "research/continuation_40/observations.json")["annotations"]
    annotations += read(root, "research/continuation_42/observations.json")["annotations"]
    annotations += read(root, "research/continuation_44/observations.json")["annotations"]
    annotations += read(root, "research/continuation_45/observations.json")["annotations"]
    annotations += read(root, "research/continuation_46/observations.json")["annotations"]
    annotations += read(root, "research/continuation_49/observations.json")["annotations"]
    annotations += read(root, "research/continuation_50/observations.json")["annotations"]
    annotations += read(root, "research/continuation_51/observations.json")["annotations"]
    annotations += read(root, "research/continuation_52/observations.json")["annotations"]
    annotations += read(root, "research/continuation_53/observations.json")["annotations"]
    annotations += read(root, "research/continuation_54/observations.json")["annotations"]
    annotations += read(root, "research/continuation_57/observations.json")["annotations"]
    annotations += read(root, "research/continuation_58/observations.json")["annotations"]
    annotations += read(root, "research/continuation_60/observations.json")["annotations"]
    annotations += read(root, "research/continuation_61/observations.json")["annotations"]
    annotations += read(root, "research/continuation_92/observations.json")["annotations"]
    annotations += read(root, "research/continuation_93/observations.json")["annotations"]
    annotations += read(root, "research/continuation_97/observations.json")["annotations"]
    annotations += read(root, "research/continuation_112/observations.json")["annotations"]
    annotations += read(root, "research/continuation_113/observations.json")["annotations"]
    annotations += read(root, "research/continuation_63/observations.json")["annotations"]
    annotations += read(root, "research/continuation_65/observations.json")["annotations"]
    annotations += read(root, "research/continuation_66/observations.json")["annotations"]
    annotations += read(root, "research/continuation_69/observations.json")["annotations"]
    annotations += read(root, "research/continuation_73/observations.json")["annotations"]
    annotations += read(root, "research/continuation_74/observations.json")["annotations"]
    annotations += read(root, "research/continuation_75/observations.json")["annotations"]
    annotations += read(root, "research/continuation_77/observations.json")["annotations"]
    annotations += read(root, "research/continuation_78/observations.json")["annotations"]
    annotations += read(root, "research/continuation_79/observations.json")["annotations"]
    annotations += read(root, "research/continuation_80/observations.json")["annotations"]
    contexts = read(root, review_doc["context_checks_path"])["checks"]
    dossiers = read(root, "data/dossiers.json")
    crosslinks = read(root, "research/finnish_crosslinks_mpo.json")
    diagnostic = read(root, "research/metadata_retrieval_diagnostic.json")
    e33 = read(root, "research/continuation_33/results.json")
    e34 = read(root, "research/continuation_34/results.json")
    e35 = read(root, "research/continuation_35/results.json")
    e36 = read(root, "research/continuation_36/results.json")
    e37 = read(root, "research/continuation_37/results.json")
    e38 = read(root, "research/continuation_38/results.json")
    e39 = read(root, "research/continuation_39/results.json")
    e40 = read(root, "research/continuation_40/results.json")
    e41 = read(root, "research/continuation_41/results.json")
    e42 = read(root, "research/continuation_42/results.json")
    e43 = read(root, "research/continuation_43/results.json")
    e43_memberships = read(root, "research/continuation_43/memberships.json")["memberships"]
    e44 = read(root, "research/continuation_44/results.json")
    e44_captures = read(root, "research/continuation_44/captures.json")["captures"]
    e45 = read(root, "research/continuation_45/results.json")
    e46 = read(root, "research/continuation_46/results.json")
    e47 = read(root, "research/continuation_47/results.json")
    e47_memberships = read(root, "research/continuation_47/memberships.json")
    e48 = read(root, "research/continuation_48/results.json")
    e48_sources = read(root, "research/continuation_48/source_rows.json")
    e49 = read(root, "research/continuation_49/results.json")
    e49_sources = read(root, "research/continuation_49/sources.json")
    e50 = read(root, "research/continuation_50/results.json")
    e50_captures = read(root, "research/continuation_50/captures.json")["captures"]
    e51 = read(root, "research/continuation_51/results.json")
    e52 = read(root, "research/continuation_52/results.json")
    e52_captures = read(root, "research/continuation_52/captures.json")["captures"]
    e52_pairs = read(root, "research/continuation_52/pair_comparisons.json")["comparisons"]
    e53 = read(root, "research/continuation_53/results.json")
    e53_pairs = read(root, "research/continuation_53/pair_comparisons.json")["comparisons"]
    e54 = read(root, "research/continuation_54/results.json")
    e54_captures = read(root, "research/continuation_54/captures.json")["captures"]
    e54_pairs = read(root, "research/continuation_54/pair_comparisons.json")["comparisons"]
    e55 = read(root, "research/continuation_55/results.json")
    e56 = read(root, "research/continuation_56/results.json")
    e57 = read(root, "research/continuation_57/results.json")
    e58 = read(root, "research/continuation_58/results.json")
    e59 = read(root, "research/continuation_59/results.json")
    e60 = read(root, "research/continuation_60/results.json")
    e61 = read(root, "research/continuation_61/results.json")
    e63 = read(root, "research/continuation_63/results.json")
    e64 = read(root, "research/continuation_64/results.json")
    e65 = read(root, "research/continuation_65/results.json")
    e65_captures = read(root, "research/continuation_65/captures.json")["captures"]
    e66 = read(root, "research/continuation_66/results.json")
    e67 = read(root, "research/continuation_67/results.json")
    e68 = read(root, "research/continuation_68/results.json")
    e69 = read(root, "research/continuation_69/results.json")
    e70 = read(root, "research/continuation_70/results.json")
    e71 = read(root, "research/continuation_71/results.json")
    e72 = read(root, "research/continuation_72/results.json")
    e73 = read(root, "research/continuation_73/results.json")
    e74 = read(root, "research/continuation_74/results.json")
    e75 = read(root, "research/continuation_75/results.json")
    e76 = read(root, "research/continuation_76/results.json")
    e77 = read(root, "research/continuation_77/results.json")
    e78 = read(root, "research/continuation_78/results.json")
    e79 = read(root, "research/continuation_79/results.json")
    e80 = read(root, "research/continuation_80/results.json")
    e83 = read(root, "research/continuation_83/results.json")
    e84 = read(root, "research/continuation_84/results.json")
    e85 = read(root, "research/continuation_85/results.json")
    e86 = read(root, "research/continuation_86/results.json")
    e90 = read(root, "research/continuation_90/results.json")
    e92 = read(root, "research/continuation_92/results.json")
    e93 = read(root, "research/continuation_93/results.json")
    e97 = read(root, "research/continuation_97/results.json")
    e99 = read(root, "research/continuation_99/results.json")
    input_paths = list(dict.fromkeys(FROZEN + REQUIRED + [
        "data/fragments.json", "data/comparison_sources.v1.json", "data/dossiers.json",
        review_doc["observations_path"], review_doc["context_checks_path"],
        "research/finnish_crosslinks_mpo.json", "research/metadata_retrieval_diagnostic.json",
        "research/continuation_33/observations.json", "research/continuation_33/results.json",
        "research/continuation_33/download_receipts.json",
        "research/continuation_34/protocol.json", "research/continuation_34/observations.json", "research/continuation_34/results.json",
        "research/continuation_35/protocol.json", "research/continuation_35/check_overlap.py", "research/continuation_35/feature_results.json", "research/continuation_35/results.json",
        "research/continuation_36/protocol.json", "research/continuation_36/record_evidence.py", "research/continuation_36/observations.json", "research/continuation_36/results.json", "research/continuation_36/inventory.json", "research/continuation_36/checks.json",
        "research/continuation_37/protocol.json", "research/continuation_37/magnificat-test.json", "research/continuation_37/record_evidence.py", "research/continuation_37/check_sources.py", "research/continuation_37/observations.json", "research/continuation_37/results.json", "research/continuation_37/checks.json", "research/continuation_37/access_and_reading.json", "research/continuation_37/download_receipts.json", "research/continuation_37/text-search-index.json",
        "research/continuation_38/protocol.json", "research/continuation_38/record_evidence.py", "research/continuation_38/check_sources.py", "research/continuation_38/observations.json", "research/continuation_38/results.json", "research/continuation_38/download_receipt.json", "research/continuation_38/c23-record.ax.txt", "research/continuation_38/c23-69r-viewer.ax.txt",
        "research/continuation_39/protocol.json", "research/continuation_39/compare_notes.py", "research/continuation_39/record_evidence.py", "research/continuation_39/check_sources.py", "research/continuation_39/readings.v1.json", "research/continuation_39/readings.v2.json", "research/continuation_39/readings.v3.json", "research/continuation_39/comparison.json", "research/continuation_39/observations.json", "research/continuation_39/results.json", "research/continuation_39/method_receipt.json",
        "research/continuation_40/protocol.json", "research/continuation_40/record_evidence.py", "research/continuation_40/check_sources.py", "research/continuation_40/observations.json", "research/continuation_40/results.json", "research/continuation_40/sources.json", "research/continuation_40/download_receipt.json",
        "research/continuation_41/protocol.json", "research/continuation_41/make_review.py", "research/continuation_41/record_review.py", "research/continuation_41/check_sources.py", "research/continuation_41/review_manifest.json", "research/continuation_41/manual_review.json", "research/continuation_41/results.json",
        "research/continuation_42/protocol.json", "research/continuation_42/record_evidence.py", "research/continuation_42/check_sources.py", "research/continuation_42/row_coverage.json", "research/continuation_42/observations.json", "research/continuation_42/results.json", "research/continuation_42/sources.json",
        "research/continuation_43/protocol.json", "research/continuation_43/audit_register.py", "research/continuation_43/check_sources.py", "research/continuation_43/lead_register.before.json", "research/continuation_43/memberships.json", "research/continuation_43/coverage_audit.json", "research/continuation_43/results.json", "research/evidence/F-4ihz_manifest.json",
        "research/continuation_44/protocol.json", "research/continuation_44/resumption.json", "research/continuation_44/acquire.py", "research/continuation_44/record_evidence.py", "research/continuation_44/check_sources.py", "research/continuation_44/inspection.v1.json", "research/continuation_44/inspection.v2.json", "research/continuation_44/captures.json", "research/continuation_44/download_receipts.json", "research/continuation_44/observations.json", "research/continuation_44/results.json", "research/continuation_44/sources.json", "data/manifests/8066.json", "data/manifests/9620.json",
        "research/continuation_45/protocol.json", "research/continuation_45/manual_readings.json", "research/continuation_45/record_evidence.py", "research/continuation_45/check_sources.py", "research/continuation_45/observations.json", "research/continuation_45/results.json", "research/continuation_45/sources.json",
        "research/continuation_46/protocol.json", "research/continuation_46/readings.v1.json", "research/continuation_46/readings.v2.json", "research/continuation_46/compare_notes.py", "research/continuation_46/record_evidence.py", "research/continuation_46/check_sources.py", "research/continuation_46/comparison.json", "research/continuation_46/observations.json", "research/continuation_46/results.json", "research/continuation_46/sources.json",
        "research/continuation_47/protocol.json", "research/continuation_47/lead_register.before.json", "research/continuation_47/audit_membership.py", "research/continuation_47/check_sources.py", "research/continuation_47/memberships.json", "research/continuation_47/results.json",
        "research/continuation_47/lead_register.after.json", "research/continuation_48/protocol.json", "research/continuation_48/lead_register.before.json", "research/continuation_48/audit_remaining.py", "research/continuation_48/source_rows.json", "research/continuation_48/results.json", "research/continuation_48/check_sources.py", "research/continuation_48/sources.json",
        "research/continuation_49/protocol.json", "research/continuation_49/manual_readings.json", "research/continuation_49/record_evidence.py", "research/continuation_49/check_sources.py", "research/continuation_49/observations.json", "research/continuation_49/results.json", "research/continuation_49/sources.json",
        "research/continuation_50/access_protocol.json", "research/continuation_50/access_results.json", "research/continuation_50/primary_protocol.json", "research/continuation_50/lead_register.before.json", "research/continuation_50/acquire.py", "research/continuation_50/download_receipts.json", "research/continuation_50/captures.json", "research/continuation_50/manual_readings.json", "research/continuation_50/measure_fields.py", "research/continuation_50/field_comparison.json", "research/continuation_50/record_evidence.py", "research/continuation_50/check_sources.py", "research/continuation_50/results.json", "research/continuation_50/observations.json",
        "research/continuation_51/protocol.json", "research/continuation_51/primary_protocol.json", "research/continuation_51/lead_register.before.json", "research/continuation_51/fetch_metadata.py", "research/continuation_51/metadata_receipts.json", "research/continuation_51/records-query.json", "research/continuation_51/combined-latest.json", "research/continuation_51/raw-latest.json", "research/continuation_51/manual_readings.json", "research/continuation_51/sources.json", "research/continuation_51/record_evidence.py", "research/continuation_51/metadata_comparison.json", "research/continuation_51/results.json", "research/continuation_51/observations.json", "research/continuation_51/check_sources.py",
        "research/continuation_52/protocol.json", "research/continuation_52/lead_register.before.json", "research/continuation_52/acquire.py", "research/continuation_52/download_receipts.json", "research/continuation_52/captures.json", "research/continuation_52/readings.v1.json", "research/continuation_52/readings.v2.json", "research/continuation_52/readings.v3.json", "research/continuation_52/sources.json", "research/continuation_52/record_evidence.py", "research/continuation_52/pair_comparisons.json", "research/continuation_52/results.json", "research/continuation_52/observations.json", "research/continuation_52/check_sources.py",
        "research/continuation_53/protocol.json", "research/continuation_53/lead_register.before.json", "research/continuation_53/readings.v1.json", "research/continuation_53/readings.v2.json", "research/continuation_53/sources.json", "research/continuation_53/record_evidence.py", "research/continuation_53/pair_comparisons.json", "research/continuation_53/results.json", "research/continuation_53/observations.json", "research/continuation_53/check_sources.py",
        "research/continuation_54/protocol.json", "research/continuation_54/lead_register.before.json", "research/continuation_54/acquire.py", "research/continuation_54/download_receipts.json", "research/continuation_54/captures.json", "research/continuation_54/readings.v1.json", "research/continuation_54/record_evidence.py", "research/continuation_54/pair_comparisons.json", "research/continuation_54/results.json", "research/continuation_54/observations.json", "research/continuation_54/check_sources.py",
        "research/continuation_55/protocol.json", "research/continuation_55/lead_register.before.json", "research/continuation_55/calibrate_staff.py", "research/continuation_55/staff_calibration.json", "research/continuation_55/audit_remaining.py", "research/continuation_55/remaining_leads.json", "research/continuation_55/record_result.py", "research/continuation_55/results.json", "research/continuation_55/check_sources.py",
        "research/continuation_56/protocol.json", "research/continuation_56/lead_register.before.json", "research/continuation_56/TMMA_fragC.xml", "research/continuation_56/metadata_receipts.json", "research/continuation_56/source_files.json", "research/continuation_56/download_receipts.json", "research/continuation_56/captures.json", "research/continuation_56/results.json", "research/continuation_56/check_sources.py",
        "research/continuation_57/protocol.json", "research/continuation_57/lead_register.before.json", "research/continuation_57/record_evidence.py", "research/continuation_57/observations.json", "research/continuation_57/results.json", "research/continuation_57/check_sources.py",
        "research/continuation_58/protocol.json", "research/continuation_58/make_review.py", "research/continuation_58/review_sources.json", "research/continuation_58/record_evidence.py", "research/continuation_58/observations.json", "research/continuation_58/results.json", "research/continuation_58/sources.json", "research/continuation_58/check_sources.py",
        "research/continuation_59/protocol.json", "research/continuation_59/decisions.before.json", "research/continuation_59/results.json", "research/continuation_59/sources.json", "research/continuation_59/check_sources.py", "research/bibliography.ris",
        "research/continuation_60/protocol.json", "research/continuation_60/decisions.before.json", "research/continuation_60/record_evidence.py", "research/continuation_60/observations.json", "research/continuation_60/results.json", "research/continuation_60/sources.json", "research/continuation_60/make_review.py", "research/continuation_60/check_sources.py",
        "research/continuation_61/protocol.json", "research/continuation_61/decisions.before.json", "research/continuation_61/record_evidence.py", "research/continuation_61/observations.json", "research/continuation_61/results.json", "research/continuation_61/sources.json", "research/continuation_61/check_sources.py",
        "research/continuation_62/register.before.json", "research/continuation_62/results.json", "research/continuation_62/check_sources.py",
        "research/continuation_63/protocol.json", "research/continuation_63/acquire.py", "research/continuation_63/download_receipt.json", "research/continuation_63/record_evidence.py", "research/continuation_63/observations.json", "research/continuation_63/results.json", "research/continuation_63/decisions.before.json", "research/continuation_63/check_sources.py",
        "research/continuation_64/sources.json", "research/continuation_64/results.json", "research/continuation_64/decisions.before.json", "research/continuation_64/check_sources.py",
        "research/continuation_65/protocol.json", "research/continuation_65/acquire.py", "research/continuation_65/download_receipt.json", "research/continuation_65/captures.json", "research/continuation_65/record_evidence.py", "research/continuation_65/observations.json", "research/continuation_65/sources.json", "research/continuation_65/results.json", "research/continuation_65/decisions.before.json", "research/continuation_65/check_sources.py",
        "research/continuation_66/protocol.json", "research/continuation_66/record_evidence.py", "research/continuation_66/observations.json", "research/continuation_66/sources.json", "research/continuation_66/results.json", "research/continuation_66/decisions.before.json", "research/continuation_66/check_sources.py",
        "research/continuation_67/protocol.json", "research/continuation_67/sources.json", "research/continuation_67/results.json", "research/continuation_67/decisions.before.json", "research/continuation_67/check_sources.py",
        "research/continuation_68/sources.json", "research/continuation_68/results.json",
        "research/continuation_69/results.json", "research/continuation_69/sources.json", "research/continuation_69/observations.json", "research/continuation_69/decisions.before.json", "research/continuation_69/download_receipt.json", "research/continuation_69/check_sources.py",
        "research/continuation_70/results.json", "research/continuation_70/sources.json", "research/continuation_70/check_sources.py",
        "research/continuation_71/results.json", "research/continuation_71/check_sources.py",
        "research/continuation_72/results.json", "research/continuation_72/sources.json", "research/continuation_72/check_sources.py",
        "research/continuation_73/results.json", "research/continuation_73/sources.json", "research/continuation_73/observations.json", "research/continuation_73/check_sources.py",
        "research/continuation_74/results.json", "research/continuation_74/sources.json", "research/continuation_74/observations.json", "research/continuation_74/check_sources.py",
        "research/continuation_75/results.json", "research/continuation_75/sources.json", "research/continuation_75/observations.json", "research/continuation_75/check_sources.py",
        "research/continuation_76/results.json", "research/continuation_76/sources.json", "research/continuation_76/candidate_rows.json", "research/continuation_76/extract_candidates.py", "research/continuation_76/check_sources.py",
        "research/continuation_77/results.json", "research/continuation_77/sources.json", "research/continuation_77/observations.json", "research/continuation_77/record_observations.py", "research/continuation_77/check_sources.py",
        "research/continuation_78/results.json", "research/continuation_78/sources.json", "research/continuation_78/observations.json", "research/continuation_78/record_observations.py", "research/continuation_78/check_sources.py",
        "research/continuation_79/results.json", "research/continuation_79/sources.json", "research/continuation_79/observations.json", "research/continuation_79/readings.json", "research/continuation_79/comparison.json", "research/continuation_79/compare_notes.py", "research/continuation_79/record_observations.py", "research/continuation_79/check_sources.py",
        "research/continuation_80/results.json", "research/continuation_80/sources.json", "research/continuation_80/observations.json", "research/continuation_80/readings.json", "research/continuation_80/comparison.json", "research/continuation_80/compare_notes.py", "research/continuation_80/record_observations.py", "research/continuation_80/check_sources.py",
        "research/continuation_83/results.json", "RESEARCH_CONTINUATION_83.md",
        "research/continuation_84/results.json", "RESEARCH_CONTINUATION_84.md",
        "research/continuation_85/results.json", "research/continuation_85/check_sources.py", "RESEARCH_CONTINUATION_85.md",
        "research/continuation_86/protocol.json", "research/continuation_86/results.json", "RESEARCH_CONTINUATION_86.md",
        "research/continuation_90/record_evidence.py", "research/continuation_90/results.json", "RESEARCH_CONTINUATION_90.md",
        "research/continuation_92/protocol.json", "research/continuation_92/measure.py", "research/continuation_92/observations.json", "research/continuation_92/results.json", "RESEARCH_CONTINUATION_92.md",
        "research/continuation_93/protocol.json", "research/continuation_93/record.py", "research/continuation_93/observations.json", "research/continuation_93/results.json", "RESEARCH_CONTINUATION_93.md",
        "research/continuation_97/protocol.json", "research/continuation_97/observations.json", "research/continuation_97/results.json", "research/continuation_97/check.py", "RESEARCH_CONTINUATION_97.md",
        "research/continuation_99/audit.py", "research/continuation_99/results.json", "RESEARCH_CONTINUATION_99.md",
        "research/continuation_112/observations.json", "research/continuation_112/control_beban.json", "research/continuation_112/check.py", "RESEARCH_CONTINUATION_112.md",
        "research/continuation_113/observations.json", "research/continuation_113/results.json", "research/continuation_113/audit.py", "RESEARCH_CONTINUATION_113.md",
        "research/continuation_26/bompac/target_crosswalk_results.json",
        "research/continuation_27/related_unit_crosswalk_results.json",
        "research/continuation_30/bompac_suggestion_crosswalk_results.json",
        "data/reconstruction.json", "data/sample_plan.json", "MANUSCRIPT_KNOWLEDGE.md", "data/knowledge.schema.v1.json",
    ] + [str(p.relative_to(root)) for p in sorted(root.glob("RESEARCH_CONTINUATION_*.md"))]))
    entities, claims, evidence, dependencies, leads = {}, [], {}, {}, {}

    def entity(ident, kind, label, **attrs):
        if ident not in entities:
            entities[ident] = {"id": ident, "type": kind, "label": label, **attrs}
        return ident

    def source(location):
        ident = "source:" + digest(location.encode())[:20]
        entity(ident, "Source", location, location=location,
               sha256=digest((root / location).read_bytes()) if (root / location).is_file() else None)
        return ident

    entity("agent:project-ai", "Agent", "Codex AI-assisted project reading; no independent expert endorsement")
    entity("agent:institutional-source", "Agent", "Author/institution identified by the cited source; original statement date may be unknown")
    entity("agent:matcher", "Agent", "Frozen local compatibility retrieval; scores are not confidence")

    def claim(ident, subject, predicate, obj, basis, provenance, status="unresolved", stance="unknown", polarity="positive", scope="book relationship", **extra):
        claims.append({"id": ident, "subject": subject, "predicate": predicate, "object": obj,
                       "basis": basis, "status": status, "source_stance": stance, "polarity": polarity,
                       "attributed_to": "agent:matcher" if basis == "computational_suggestion" else ("agent:institutional-source" if basis == "source_assertion" else "agent:project-ai"),
                       "recorded_at": DATE, "source_statement_date": None, "scope": scope,
                       "provenance": [{"source": source(provenance), "locator": extra.pop("locator", None)}],
                       "supports": extra.pop("supports", []), "challenges": extra.pop("challenges", []), **extra})
        return ident

    by_id = {r["id"]: r for r in records}
    canonical = {r["id"]: r.get("physical_object_id", r["id"]) for r in records}
    object_records = collections.defaultdict(list)
    image_by_path = {}
    for record in records + comparisons:
        rid = record["id"]
        physical = record.get("physical_object_id", rid)
        canonical[rid] = physical
        object_records[physical].append(rid)
        oid = entity("object:" + physical, "PhysicalFragment", record.get("shelfmark", rid),
                     extent_statement=record.get("raw", {}).get("blattzahl"),
                     extent_status="catalogue assertion; no automatic leaf expansion")
        record_id = entity("record:" + rid, "CatalogRecord", record.get("shelfmark", rid),
                           physical_object=oid, source_url=record.get("source_url"),
                           existing_record={"path": "data/fragments.json" if rid in by_id else "data/comparison_sources.v1.json", "record_id": rid},
                           identifiers=[])
        claim("record-describes:" + rid, record_id, "describes", oid, "source_assertion", "data/fragments.json" if rid in by_id else "data/comparison_sources.v1.json", "previously_documented", "asserted", scope="record-to-object mapping")
        raw = record.get("raw", {})
        for scheme, field, target in [("MPO-Fr", "signatur", oid), ("MPO-Codex", "codex", None), ("CCM-unit", "ccmsignum", None)]:
            value = raw.get(field)
            if not value:
                continue
            iid = entity("identifier:" + scheme + ":" + quote(value, safe=""), "Identifier", value, scheme=scheme,
                         value=value, scope="Swedish National Archives/MPO", qualified=bool(re.search(r"[?*]", value)))
            entities[record_id]["identifiers"].append(iid)
            if target is None:
                target = entity("codex:" + scheme + ":" + quote(value, safe=""), "Codex", value,
                                identity_status="source reconstruction concept; not an independently verified book assignment", identifier=iid)
                claim(f"assignment:{rid}:{field}", oid, "assigned_to_reconstruction", target,
                      "source_assertion", "data/fragments.json", "previously_documented", "asserted",
                      scope="catalogue grouping, potentially disputed", locator=f"record {rid}/raw/{field}")
        captures = record.get("captures") or ([{"path": record["image_path"], **(record.get("image") or {})}] if record.get("image_path") else [])
        for index, cap in enumerate(captures):
            path = cap.get("path")
            if not path:
                continue
            canvas = cap.get("canvas_id") or f"{rid}:unmapped-capture:{cap.get('capture_index', index)}"
            cid = entity("capture:" + digest(canvas.encode())[:24], "Capture", canvas, physical_object=oid, canvas_id=cap.get("canvas_id"), side_assignment=None)
            image_id = entity("image:" + path, "ImageDerivative", path, path=path, sha256=cap.get("sha256"),
                              width=cap.get("width"), height=cap.get("height"), rights_url=cap.get("rights_url") or record.get("rights_url"),
                              source_url=cap.get("url"), capture=cid)
            image_by_path[path] = image_id
    # Additional source photographs are an overlay on existing objects and
    # captures. They do not manufacture catalogue records or alter core inputs.
    for cap in e44_captures + e50_captures + e52_captures + e54_captures + e65_captures:
        oid="object:"+cap["physical_object_id"]
        assert oid in entities
        cid=entity("capture:"+digest(cap["canvas_id"].encode())[:24],"Capture",cap["canvas_id"],
            physical_object=oid,canvas_id=cap["canvas_id"],side_assignment=None)
        path=cap["path"]
        image_by_path[path]=entity("image:"+path,"ImageDerivative",path,path=path,
            sha256=cap["sha256"],width=cap["width"],height=cap["height"],rights_url=cap["rights_url"],
            source_url=cap["url"],capture=cid,provenance_manifest=cap["manifest"],
            provenance_locator=cap["manifest_locator"],role=cap["role"])

    # E43 credits explicit membership of the retained virtual reconstruction.
    # Exact image-service/canvas links, rather than similar titles, supply the
    # source assertion. This is neither identity closure nor new attribution.
    beauvais = entity("codex:fragmentarium:BeauvaisMissal", "Codex", "Beauvais Missal / Fragmentarium F-4ihz",
                      identity_status="Published virtual reconstruction; source assertion, not independent project confirmation")
    e43_member_ids = {m["object_id"] for m in e43_memberships}
    for membership in e43_memberships:
        claim("assignment:"+membership["record_id"]+":beauvais", "object:"+membership["object_id"],
              "assigned_to_reconstruction", beauvais, "source_assertion", membership["manifest"],
              "previously_documented", "asserted", scope=membership["scope"],
              locator=[m["locator"] for m in membership["matches"]],
              source_record=membership["source_record"], reconstruction_url=membership["reconstruction_url"],
              matched_canvas_ids=[m["canvas_id"] for m in membership["matches"]],
              working_image=membership["working_image"], independent_confirmation=False, new_discovery=False)

    # Source-described Finnish leaves are distinct from their proposed codex.
    for label, count in [("IV.156",24),("IV.157",14),("IV.173",1),("IV.160",10),("IV.28",30),("II.44",48)]:
        entity("codex:fm-" + label, "Codex", "Codex represented by F.m." + label, identity_status="catalogue reconstruction concept")
        if label != "IV.173":
            entity("object:fm-" + label, "FragmentSet", "Surviving F.m." + label + " aggregate", extent_folios=count, extent_status="source assertion; not a physical census")
    for n in [8,9,10]:
        leaf = entity(f"leaf:fm-IV.157-{n}", "Leaf", f"F.m.IV.157 catalogue folio {n}", physical_parent="object:fm-IV.157", mapping_basis="catalogue; local scan missing")
        for side in ["r","v"]:
            entity(f"side:fm-IV.157-{n}{side}", "Side", f"F.m.IV.157 f.{n}{side}", leaf=leaf, designation_basis="catalogue; not independently image-verified")
    entity("identifier:Turku-Ms-c", "Identifier", "Turku Ms. c", scheme="historic holder and manuscript label", value="Ms. c", scope="Turku, holder unresolved", resolution_status="unresolved; no entity merge")
    for annotation in annotations:
        eid = "evidence:" + annotation["id"]
        path = annotation["target"]["source"]
        evidence[eid] = {"id": eid, "type": "EvidenceRegion", "basis": "project_observation",
                         "attributed_to": "agent:project-ai", "recorded_at": DATE,
                         "annotation_id": annotation["id"], "image": image_by_path.get(path),
                         "target": annotation["target"], "sha256": annotation["sha256"],
                         "observation": annotation["body"]["value"],
                         "literal_candidate": annotation.get("literal_candidate"),
                         "normalized_candidate": annotation.get("normalized_candidate"),
                         "source_url": annotation.get("source_url"),
                         "import_date": DATE, "original_annotation": annotation,
                         "independent_confirmation": False}

    # Keep the original E49 annotation verbatim in original_annotation while
    # making its later, uncertain word correction visible in the live viewer.
    older = evidence['evidence:I49-8304-opening']
    older['observation'] = 'E69 supersedes E49 sollempnitas with provisional sollempni[a?]; consult I69-8304-opening-corrected. ' + older['observation']
    older['superseded_by'] = 'evidence:I69-8304-opening-corrected'
    older['literal_candidate'] = 'Inclita sancte uirginis / katherine sollempni[a?] [...] (E69 re-reading)'
    older['normalized_candidate'] = 'Inclita sanctae virginis Katherinae sollemnia [...] (provisional E69 re-reading)'

    def dependency(ident, kind, value, external=True):
        dependencies[ident] = {"id": ident, "kind": kind, "description": value, "state": "missing", "external": external}
        return ident

    for rid, record in by_id.items():
        if not record.get("image_path"):
            dependency("missing-image:" + canonical[rid], "image", f"No verified local source image for {record['shelfmark']}.")
    dependency("missing-finnish-scans", "image", "F.m.IV.156/IV.157 corresponding source pages are listed publicly but not locally acquired; ordinary routes met verification pages.")
    dependency("unread-taitto", "scholarship", "Taitto 2001 pp.161–168 and other claim-specific cited passages remain unread in full.")
    dependency("unread-keskiaho", "scholarship", "Relevant Keskiaho 2008, 2010 pp.418–419 and 2019 discussions remain unread in full.")
    dependency("unread-walta", "scholarship", "Walta 2013 full chapter unread; only indexed excerpt reviewed.")
    dependency("side-map", "interpretation", "Intrinsic medieval-side mapping and source capture grouping require further source checks.", False)

    def lead(ident, title, subject_ids, relation, exact_claim, prior, support, challenge, test, inputs, state="unresolved", changes=None, origins=None, execution="source-context review", **extra):
        leads[ident] = {"id": ident, "title": title, "subjects": subject_ids, "relationship_type": relation,
                        "exact_claim": exact_claim, "already_published": prior, "supporting": support,
                        "contradicting": challenge, "strongest_feasible_test": test, "required_inputs": inputs,
                        "decision_state": state, "what_changes_state": changes or "Source-visible discriminating evidence, explicit alternatives and a meaningful prior-art check; similarity alone is insufficient.",
                        "origins": origins or [], "test_execution": execution,
                        "originality": "uncleared; no new discovery claim", **extra}

    pair_rows = collections.defaultdict(list)
    for i, m in enumerate(matches):
        pair_rows[pair_key(canonical[m["left_id"]], canonical[m["right_id"]])].append({"path": "data/matches.json", "row": i, "left_id": m["left_id"], "right_id": m["right_id"], "rank": m["rank"], "rank_interval": m.get("rank_interval"), "retrieval_score": m["score"], "method": m["method"]})
    pair_hypotheses = {}
    for h in hypotheses:
        pair = pair_key(canonical[h["left_id"]], canonical[h["right_id"]])
        pair_hypotheses[pair] = h
        pair_rows[pair].append({"path": "data/hypotheses.v1.json", "id": h["id"]})
    pair_dossiers = collections.defaultdict(list)
    for d in dossiers:
        pair = pair_key(canonical[d["left_id"]], canonical[d["right_id"]])
        pair_dossiers[pair].append(d)
        pair_rows[pair].append({"path": "data/dossiers.json", "id": d["id"]})
    for i, d in enumerate(diagnostic["results"]):
        a,b = "mpo-" + d["query"], "mpo-" + d["candidate"]
        pair_rows[pair_key(canonical.get(a,a),canonical.get(b,b))].append({"path": "research/metadata_retrieval_diagnostic.json", "row": i})
    for pair, origins in sorted(pair_rows.items()):
        ident = pair_id(pair)
        h = pair_hypotheses.get(pair)
        r = reviews[h["id"]] if h else None
        ds = pair_dossiers[pair]
        category = r["classification"] if r else (ds[0]["classification"] if ds else None)
        state = "previously_documented" if category == "E" else ("contradicted" if category == "D" else "unresolved")
        support = list(r["supporting"]) if r else [s for d in ds for s in d.get("supporting", [])]
        against = list(r["against"]) if r else [s for d in ds for s in d.get("against", [])]
        prior = [{"statement": r["prior_status"], "sources": r.get("sources", [])}] if r else [{"statement": d.get("originality"), "sources": d.get("sources", [])} for d in ds]
        local = {p: [by_id[x]["image_path"] for x in object_records[p] if x in by_id and by_id[x].get("image_path")] for p in pair}
        descriptive = catalogue_comparison(by_id[object_records[pair[0]][0]], by_id[object_records[pair[1]][0]])
        missing = ["missing-image:"+p for p in pair if not local[p]]
        published_beauvais = all(p in e43_member_ids for p in pair)
        published_aboense = all(p in {m['object_id'] for m in e47_memberships['memberships']} for p in pair)
        published_control = published_beauvais or published_aboense
        if not r and not ds:
            for p in pair:
                raw = by_id[object_records[p][0]].get("raw", {})
                if raw.get("codex") or raw.get("ccmsignum"):
                    prior.append({"statement": f"{p}: recorded codex={raw.get('codex') or None}, CCM unit={raw.get('ccmsignum') or None}", "sources": ["data/fragments.json", "https://zenodo.org/records/17287665"], "kind": "catalogue assignment, not image proof"})
            support.append("Saved compatibility ranking only; no new direct pair-level source interpretation was performed by this triage.")
            against.append("Shared style, liturgy, inherited metadata and capture appearance remain explanations; differing catalogue assignments are not automatic negatives.")
        test = r["next_evidence_needed"] if r else "Inspect complete corresponding text and foliation/quire or physical structure; compare with published same-book and same-hand/different-book controls. Establish side mapping before proposing a join."
        if published_beauvais:
            prior.append({"statement":"Both exact retained image services are included in the source-defined Beauvais Missal virtual reconstruction. This is a published control, not a new candidate identification.",
                          "sources":["research/evidence/F-4ihz_manifest.json","research/continuation_43/memberships.json","https://fragmentarium.ms/overview/F-4ihz"],
                          "kind":"source reconstruction membership; not fresh pair-level image validation"})
            if not r and not ds:
                state="previously_documented"
                support.append("E43 verified both working-image services against explicit canvases of the pinned published reconstruction manifest; no new pair-level transcription or physical examination.")
                test="Retain as a published reconstruction control. Any new physical-adjacency or improved-method claim needs its own source/holdout test; this recorded membership is not a new discovery."
        if published_aboense:
            prior.append({"statement":"Both exact identifiers have unique included rows explicitly assigned to published BOMPAC-4795 / FM.II.44. The related raw C-1481 unit is not independent corroboration.",
                          "sources":["research/continuation_47/memberships.json","https://doi.org/10.5281/zenodo.17511106","https://doi.org/10.5281/zenodo.17701360"],
                          "kind":"published source assignment; not fresh physical or image validation"})
            if not r and not ds:
                assert ident in e47['repair_leads']
                state="previously_documented"
                support.append("E47 checked exact workbook rows, inclusion flags, identifiers and reconstruction membership. This is a credited known Aboense control, with no new pair-level image transcription.")
                test="Retain as a previously documented reconstruction control. Any new adjacency, physical identity or method-performance claim needs a separate discriminating test; source credit is not a discovery."
        if h and h["id"] == "H03":
            against.append(e33["interpretation"]["changed_case"] + " The exclusion remains conditional on unverified numbering/section/source premises.")
            test = e33["next_test"]
        lead(ident, " / ".join(pair), ["object:"+p for p in pair], "same_codex", f"Do {pair[0]} and {pair[1]} belong to one codex?", prior, support, against, test,
             {"available_primary_images": local, "dependencies": missing, "local_tasks": ["Direct transcription and book-discriminating comparison remain pending for metadata-only rows."] if not r and not ds and not published_control else []}, state,
             origins=origins+([{"path":"research/continuation_43/memberships.json"}] if published_beauvais else [])+([{"path":"research/continuation_47/memberships.json"}] if published_aboense else []), execution=("frozen source review with dated E33 overlay" if h["id"] == "H03" else "frozen source review") if r else ("existing dossier review" if ds else ("published reconstruction source audit; no new pair-level image transcription" if published_beauvais else ("published BOMPAC membership audit; no new pair-level image transcription" if published_aboense else "metadata and availability triage only"))),
             frozen_hypothesis=h["id"] if h else None, frozen_category=category, independent_confirmation=False,
             catalogue_comparison=descriptive)
        claim("claim:"+ident, "object:"+pair[0], "same_codex" if r or ds else "suggested_association", "object:"+pair[1],
              "source_assertion" if category == "D" else ("researcher_interpretation" if r or ds else "computational_suggestion"), "https://doi.org/10.25167/ls.4818" if category == "D" else ("data/hypothesis_reviews.v1.json" if r else ("data/dossiers.json" if ds else "data/matches.json")), "previously_documented" if category == "D" else ("unresolved" if published_control and not r and not ds else state),
              "rejected" if category == "D" else ("asserted" if category == "E" else "suggested"),
              polarity="negative" if category == "D" else "positive", locator=h["id"] if h else ident,
              support_notes=support, challenge_notes=against,
              source_statement_date="2022" if category == "D" else None,
              source_locator="p.293; exact textual/liturgical rejection retained in frozen H06" if category == "D" else None,
              contextual_evidence=["evidence:"+x for x in (r.get("observation_ids",[]) if r else [])],
              lead_id=ident)
    # Preserve all 170 directional computational suggestions, even where rejected by a source.
    for i,m in enumerate(matches):
        claim(f"ranking:{i}", "object:"+canonical[m["left_id"]], "suggested_association", "object:"+canonical[m["right_id"]],
              "computational_suggestion", "data/matches.json", "unresolved", "suggested", scope="retrieval compatibility only",
              locator=f"/{i}", retrieval_score=m["score"], rank=m["rank"], method=m["method"])

    # Every current auxiliary check is retained as a separately scoped research lead.
    context_tests = {
        "CTX01": "Verify complete verse boundaries, shared photographed detail and the original catalogue side convention; keep published placement separate from the qualified Codex 1505 association.",
        "CTX02": "Inspect both hVIII–hIX source addresses and complete corresponding text; establish unique numbering, same section, accurate description and incompatibility before exclusion.",
        "CTX03": "Recheck the printed equation/prose and later errata or implementations; distinguish the demonstrated reciprocal correction from an unverified first-notice claim.",
        "CTX04": "Collate distinctive visible uncorrected readings at evaluable target sites against original C23/C435 witnesses; do not import cancelled or missing text from the edition.",
        "CTX05": "Measure additional comparable primary-image controls with independent calibration and explicit deformation uncertainty; require text or physical structure to distinguish one book.",
        "CTX06": "Check whether additional metadata-matched different-book controls reproduce the same pitch, retaining the existing contrary control and its catalogue-label limitation.",
        "CTX07": "Read Taitto pp.161–168 and relevant Keskiaho discussion, then adjudicate the separated BOMPAC units using primary text/structure rather than reconstruction IDs.",
        "CTX08": "Test complete corresponding Olavi text and reliable opening signatures; equal catalogue dimensions alone cannot distinguish H03 from same-format alternatives.",
        "CTX09": "Inspect a legitimate Fr 29666 image and Taitto p.185; compare same-codex evidence separately from the Hy 49 suggestion and broader style group.",
        "CTX10": "Read Walta's full chapter, especially p.20/footnote35, and its cited membership discussion; do not infer one codex or production site from the broad group.",
        "CTX11": "Check qualified relationship wording against full Taitto/Keskiaho passages and original images; preserve stylistic resemblance separately from same-codex assertions.",
        "CTX12": "Compare Fr 8994/Fr 20278 with Finnish f.8 and ff.9–10, establish actual address units and test reset/composite/description alternatives.",
        "CTX13": "Use the visible IIII mark together with full source text and unique address mapping; a common signature convention is not a unique codex fingerprint.",
    }
    for c in contexts:
        qid = entity("question:"+c["id"], "ResearchQuestion", c["title"])
        relation = "method_correction" if c["id"] == "CTX03" else ("textual_continuation" if c["id"] == "CTX01" else "suggested_association")
        state = "supported" if c["id"] in {"CTX01","CTX03"} else "unresolved"
        lead(c["id"], c["title"], [qid], relation, c["summary"], [{"statement": "Source assertions and earlier results remain attributed in the linked context check.", "sources": c.get("sources",[])}], [c["outcome"]], c.get("limits",[]),
             context_tests[c["id"]],
             {"dependencies": ["unread-taitto","unread-keskiaho"] if c["id"] in {"CTX02","CTX07","CTX09","CTX10","CTX11","CTX12","CTX13"} else [], "local_tasks": ["Follow the source-specific next test; consult linked exact regions."]}, state,
             origins=[{"path": review_doc["context_checks_path"], "id": c["id"]}])
    leads["CTX01"]["already_published"].append({"statement":"The earlier IV.157 catalogue places the Finska Cameralia 48 / Christiern Philipssons 1610 Mary Magdalene leaf, crosswalked to Fr 10370, between Helsinki ff.7 and 8. This is a prior specific placement, distinct from the later qualified Codex 1505 group association.","sources":["https://fragmenta.kansalliskirjasto.fi/handle/10024/1300","research/independent_pass/crosswalk/catalogue_excerpt_manifest.json","research/independent_pass/crosswalk/audit.json"]})
    for cid, execution in {"CTX01":"existing direct verse/mark inspection and fixed translation/SIFT registration tests; no accepted seam", "CTX03":"existing dimensional derivation and three analytic controls", "CTX04":"existing ten-site collation against actual C23 pages and editorial apparatus", "CTX05":"existing ruler-calibrated manual measurements and full-MPO layout query", "CTX06":"existing metadata-selected different-codex ruler-calibrated image control", "CTX08":"existing full-MPO descriptive dimension screen"}.items():
        leads[cid]["test_execution"] = execution
    method = entity("method:duba-scaling", "Method", "Duba 2023 image rescaling to a common pixels/mm value")
    claim("interpretation:duba-ratio", method, "method_correction", method, "researcher_interpretation", "RESEARCH_CONTINUATION_20.md", "supported", "asserted", scope="Dimensional correction of the displayed ratio; no claim of first notice or new historical finding", locator="CTX03 / full issue printed p.64, PDF p.66", source_statement_date="2023", support_notes=["Width × Smin/Sn agrees with the prose and preserves physical size in the saved analytic controls."], challenge_notes=["Synthetic controls only; no independent author confirmation or originality check."])

    group = entity("group:naantali-style", "StylisticGroup", "Broad Åbo/Naantali-related stylistic/liturgical group", identity_status="several books; not one codex")
    for label in ["IV.156","IV.157","IV.173"]:
        claim("broad-group:"+label,"codex:fm-"+label,"member_of_group",group,"source_assertion","RESEARCH_CONTINUATION_28.md","previously_documented","asserted",scope="stylistic/liturgical grouping; not codex identity")
    # Explicit catalogue assertions, kept beside narrower BOMPAC reconstructions.
    cc99 = entity("codex:CCM-unit:Ant%2099", "Codex", "CCM Ant 99", identity_status="source reconstruction concept")
    c1505 = "codex:MPO-Codex:Codex%201505"
    statements = [
        ("iv157-ant99","codex:fm-IV.157","same_codex",cc99,"asserted","previously_documented"),
        ("iv157-1385","codex:fm-IV.157","same_codex","object:mpo-1385","asserted","previously_documented"),
        ("iv157-1505","codex:fm-IV.157","suggested_association",c1505,"suggested","unresolved"),
        ("iv156-1505","codex:fm-IV.156","suggested_association",c1505,"suggested","unresolved"),
        ("iv156-iv157","codex:fm-IV.156","stylistic_similarity","codex:fm-IV.157","asserted","previously_documented"),
        ("iv173-29666","object:finn-iv173","same_codex","object:mpo-29666","asserted","previously_documented"),
        ("iv173-25592","object:finn-iv173","suggested_association","object:mpo-25592","suggested","unresolved"),
        ("iv173-ant99","codex:fm-IV.173","suggested_association",cc99,"suggested","unresolved"),
    ]
    for ident,a,p,b,stance,status in statements:
        url="https://fragmenta.kansalliskirjasto.fi/handle/10024/"+("1314" if ident.startswith("iv173") else ("1299" if ident.startswith("iv156") else "1300"))
        claim("catalogue:"+ident,a,p,b,"source_assertion",url,status,stance,locator="Other notes / relationship wording; indexed text in E29/E31")
        lead(ident,ident,[a,b],p,"Assess the precise catalogue relation without conflating identity and broader grouping.",[{"statement":stance+" catalogue relation", "sources":[url,"RESEARCH_CONTINUATION_31.md"]}], ["Published source assertion"], ["No new independent physical adjudication; competing reconstructions and composite-volume explanations remain possible."],
             "Read the cited scholarship and compare exact corresponding source evidence for this relation.", {"dependencies":["unread-taitto","unread-keskiaho"]}, status,origins=[{"path":"RESEARCH_CONTINUATION_31.md","relationship":ident}])
    for unit,members in [("5324",[c1505,"codex:fm-IV.156"]),("912",[cc99,"codex:fm-IV.157","object:mpo-1385"]),("9531",["codex:fm-IV.173","object:mpo-29666","object:mpo-25592"]),("258",["object:mpo-4223","object:mpo-8311","object:mpo-8455"])]:
        cid=entity("codex:BOMPAC-"+unit,"Codex","BOMPAC-"+unit,identity_status="published research reconstruction; not fresh image proof")
        for j,member in enumerate(members):
            claim(f"bompac:{unit}:{j}",member,"assigned_to_reconstruction",cid,"source_assertion","research/continuation_30/bompac_suggestion_crosswalk_results.json" if unit=="258" else ("research/continuation_27/related_unit_crosswalk_results.json" if unit=="9531" else "research/continuation_26/bompac/target_crosswalk_results.json"),"previously_documented","asserted",scope="BOMPAC research-data assignment; related datasets are not independent votes")
    claim("published:same-hand-8201-8304","object:mpo-8201","same_hand","object:mpo-8304","source_assertion","https://doi.org/10.25167/ls.4818","previously_documented","asserted",locator="p.293; project reading in H06",scope="published scribal assessment, not project expert review")

    # Exact source membership of the already known Aboense reconstruction.
    # Preserve reconstruction concepts and the six physical objects separately.
    aboense = entity('codex:BOMPAC-4795', 'Codex', 'BOMPAC-4795 / Graduale Aboense',
                     identity_status='published research reconstruction; not independent project confirmation')
    combined_path = e47_memberships['combined']['path']
    for member in e47_memberships['memberships']:
        claim('assignment:'+member['record_id']+':bompac4795', 'object:'+member['object_id'],
              'assigned_to_reconstruction', aboense, 'source_assertion', combined_path,
              'previously_documented', 'asserted', scope=member['scope'],
              locator={'sheet':'Sheet1', 'excel_row':member['combined_row']['excel_row'],
                       'cells':member['combined_row']['cells']},
              source_record='https://doi.org/10.5281/zenodo.17511106',
              related_raw_assignment={'path':e47_memberships['raw']['path'], 'sheet':'Blad1',
                  'row':member['raw_row']['excel_row'], 'unit':'C-1481',
                  'independent_confirmation':False},
              independent_confirmation=False, new_discovery=False)
    claim('bompac:4795:fmII44', 'codex:fm-II.44', 'assigned_to_reconstruction', aboense,
          'source_assertion', combined_path, 'previously_documented', 'asserted',
          locator={'sheet':'Sheet1', 'rows':[r['excel_row'] for r in e47_memberships['combined']['unit_rows'] if r['values']['Database_or_institution']=='FM']},
          scope='Published reconstruction membership through24 paired-folio dataset records; no automatic leaf, capture or identity expansion.',
          independent_confirmation=False, new_discovery=False)

    for member in e48_sources['memberships']:
        row=member['combined_row']
        unit=row['values']['BOMPAC-reconstruction']
        cid=entity('codex:'+unit,'Codex',unit,
            identity_status='published research reconstruction; assignment may be disputed')
        claim('assignment:'+member['object_id']+':E48-bompac','object:'+member['object_id'],
            'assigned_to_reconstruction',cid,'source_assertion',e48_sources['combined']['path'],
            'previously_documented','asserted',locator={'sheet':'Sheet1','excel_row':row['excel_row'],'cells':row['cells']},
            scope='Published source-unit assignment only; not independent codex identity or a physical join.',
            known_unit_counterexample=(unit=='BOMPAC-4861'),
            related_raw_unit=member['raw_row']['values']['unit_HK'],
            independent_confirmation=False,new_discovery=False)
    claim('interpretation:E48-unit4861','object:mpo-8201','same_codex','object:mpo-8304',
          'researcher_interpretation',e48_sources['combined']['path'],'unresolved','suggested',
          locator={'sheet':'Sheet1','cells':['M8203','M8306']},
          scope='Implicit once-intact-manuscript claim of shared BOMPAC-4861 assignment, per dataset readme. Competing published rejection retained; no project identity acceptance.',
          reconstruction_unit='codex:BOMPAC-4861',
          derived_from_source_assignments=True,
          projection_limit='Project projection of two literal assignments and the published unit definition; not an explicit pair-level argument by the dataset authors.',
          competing_source_claim='claim:'+pair_id(pair_key('mpo-8201','mpo-8304')),
          new_discovery=False,independent_confirmation=False)
    claims[-1]['provenance'].append({'source':source('research/continuation_26/bompac/Readme-Sto-Hel-Frs-Combined-BOMPAC.pdf'),
                                   'locator':'PDF p2, Codex identification; p3, harmonisation continuation'})

    for audited in e48['pair_audit']:
        current=leads[audited['lead_id']]
        current['already_published'].append({'statement':f"E48 exact source assignment category: {audited['category']}; combined units={audited['combined_units']}; related raw units={audited['raw_units']}.",
            'sources':['research/continuation_48/source_rows.json','https://doi.org/10.5281/zenodo.17511106'],
            'kind':'source assignment only; related deposits are not independent corroboration'})
        current['origins'].append({'path':'research/continuation_48/results.json','lead_id':audited['lead_id']})
        current['primary_pair_test_pending']=audited['primary_pair_test_pending']
        if audited['source_credit_repair']:
            current['decision_state']='previously_documented'
            current['test_execution']='E48 published reconstruction source audit; no new primary pair reading'
            current['supporting'].append('Both exact included identifiers are assigned to the already published BOMPAC-5324 reconstruction. No independent physical attribution follows.')
            current['required_inputs']['local_tasks']=[]
            current['strongest_feasible_test']='Retain this documented reconstruction control. A new adjacency, physical attribution or recognition-performance claim requires a separate discriminating test.'
        else:
            current['test_execution']='E48 published-assignment review only; primary pair test pending'
            current['required_inputs']['local_tasks']=['Direct corresponding primary-source evidence remains untested for this pair. Source assignments alone cannot decide physical identity.']
            if audited['category']=='contested_shared_unit':
                current['contradicting'].append('BOMPAC-4861 includes the published8201/8304 different-book control. The unit cannot serve as independent same-codex ground truth for its other member pairs.')
            elif audited['category']=='different_units':
                current['contradicting'].append('The published data assigns the objects to different reconstruction units; this is contextual counterevidence, not automatic proof of different books.')

    # Cross-collection candidate families from the earlier feasibility register.
    for bucket,rows in crosslinks.items():
        fm = "IV.157" if bucket.startswith("IV157") else ("IV.160" if bucket=="IV160" else "IV.28")
        for row in rows:
            rid="mpo-"+row["signatur"]
            oid="object:"+canonical.get(rid,rid)
            state="contradicted" if bucket=="IV28_negative" else ("previously_documented" if bucket in {"IV157_known","IV160"} else "unresolved")
            lid="crosslink:"+bucket+":"+rid
            lead(lid,f"{rid} / F.m.{fm}",[oid,"codex:fm-"+fm],"same_codex","Evaluate the explicitly recorded cross-collection relation.",[{"statement":row.get("anmerkungen") or "Association reported in the crosslink registry", "sources":["research/finnish_crosslinks_mpo.json","CANDIDATES.md"]}], ["Source catalogue/crosslink assertion"], ["No fresh image validation is implied by this crosswalk."],"Verify the exact cited publication and corresponding source text/structure, retaining the qualified source wording.",{"dependencies":["missing-finnish-scans"]+(["missing-image:"+canonical.get(rid,rid)] if not by_id.get(rid,{}).get("image_path") and "missing-image:"+canonical.get(rid,rid) in dependencies else [])},state,origins=[{"path":"research/finnish_crosslinks_mpo.json","bucket":bucket,"record":rid}])
    for ident,title,relation,description,src,deps in [
        ("fr8311-chant","Fr 8311 chant identification","chant_identification","Recheck the provisional Cantus 006537/006537a identification against literal pixels; chant identity is not codex identity.","SCIENTIFIC_LIMITATIONS.md",[]),
        ("ant49-audit","Ant 49 / Codex 1146 membership audit","same_codex","Audit remaining Ant 49 membership while preserving 8201–8304 as a published rejection and 8201–20106 as a positive control.","CANDIDATES.md",["missing-image:mpo-20106"]),
        ("aboense-control","Graduale Aboense documented reconstruction control","textual_continuation","Check the documented continuity components separately from global foliation and the missing Fr 28175 image.","data/reconstruction.json",["missing-image:mpo-28175"]),
        ("iv160-control","IV.160 / Fr 20340 control","same_codex","Retain the documented relation; a missing image prevents independent visual validation.","CANDIDATES.md",["missing-image:mpo-20340"]),
        ("iv28-control","IV.28 / Fr 10349 exclusion control","same_codex","Preserve the source-reported exclusion; inspect the actual corresponding source if access permits.","CANDIDATES.md",["missing-finnish-scans"]),
        ("turku-ms-c","Turku Ms. c identity and holding","suggested_association","Reconcile conflicting historic holder/extent descriptions before equating the identifier with a physical object.","CANDIDATES.md",[]),
    ]:
        qid=entity("question:"+ident,"ResearchQuestion",title)
        state="previously_documented" if ident in {"aboense-control","iv160-control"} else ("contradicted" if ident=="iv28-control" else "unresolved")
        lead(ident,title,[qid],relation,description,[{"statement":"Prior source and scope are in the cited project record.","sources":[src]}],[],[],description,{"dependencies":[x for x in deps if x in dependencies],"local_tasks":["Source-specific review remains open; no negative inferred from missing material."]},state,origins=[{"path":src}])
    leads['aboense-control']['already_published'].append({'statement':e47['result'],
        'sources':['research/continuation_47/memberships.json','https://doi.org/10.5281/zenodo.17511106']})
    leads['aboense-control']['origins'].append({'path':'research/continuation_47/results.json'})
    leads['aboense-control']['test_execution'] += '; E47 exact published membership/cell audit, not new pair-level image validation'
    leads['aboense-control']['required_inputs']['local_tasks'] = ['E36 continuity observations and E47 published membership are completed and separate. A global foliation/side map or missing Fr28175-image claim still needs its own original source.']
    lead("E33-numbering-conflict","Fr 8994 IIII/k content conflict",["object:mpo-8994","leaf:fm-IV.157-8"],"numbering_conflict",e33["question"], [{"statement":"Codex 1505 link was already suggested; BOMPAC assigns separate units.","sources":["RESEARCH_CONTINUATION_31.md","RESEARCH_CONTINUATION_26.md"]}], [e33["direct_result"]], e33["interpretation"]["alternatives"],e33["next_test"],{"dependencies":["missing-finnish-scans","unread-taitto","unread-keskiaho","side-map"]},"unresolved",changes="A unique same complete address plus verified incompatible text in the same service would support an exclusion; resets, a different address or source correction would remove that inference.",origins=[{"path":"research/continuation_33/results.json"}],execution="new direct source-image test; conditional catalogue comparison")
    claim("interpretation:E33","object:mpo-8994","numbering_conflict","leaf:fm-IV.157-8","researcher_interpretation","research/continuation_33/results.json","unresolved","suggested",scope="conditional same-address conflict, not unconditional codex exclusion", supports=["evidence:I33-8994-roman","evidence:I33-8994-k","evidence:I33-8994-third-nocturn"],limits=e33["interpretation"]["alternatives"],unverified_premises=e33["interpretation"]["unverified_premises"])
    lead("E34-local-order", "Fr 8994 local chant sequence and unresolved surface map", ["object:mpo-8994"], "textual_continuation", e34["supported_narrow_result"], [{"statement":"Concordance aids identification; this is not an independent manuscript transcription.","sources":[e34["concordance"]["url"]]}], e34["observations"], e34["not_established"], e34["next_test"], {"dependencies":["side-map"],"local_tasks":["Complete boundary transcription or overlapping-detail test remains possible; no failed registration is claimed."]}, "supported", changes="A different literal reading or corrected chant identification would change the narrow order result; same-surface mapping needs a separate test.", origins=[{"path":"research/continuation_34/results.json"}],execution=e34["test_execution"])

    # A photograph overlap is an imaging relation, never a physical join or
    # transitive book identity. Preserve failed screens and the thin-strip clue.
    leads["E34-local-order"]["required_inputs"]["local_tasks"] = ["E35 completed the fixed overlap screen; neither boundary passed. The 1/2 thin folded-strip clue remains unresolved, without retuning the gate."]
    lead("E35-overlap", "Fr 8994 controlled photograph-overlap test", ["object:mpo-8994"], "photographic_overlap", e35["question"],
         [{"statement":"Follow-up to E34's unresolved photograph mapping, not a new codex proposal.","sources":["RESEARCH_CONTINUATION_34.md"]}],
         [e35["thin_strip_scope"],e35["control_result"]],e35["not_established"],e35["next_test"],
         {"dependencies":["side-map"],"local_tasks":["Review the retained thin-strip correspondences against source fold/ink detail; the fixed distribution gate remains failed."]},
         "unresolved",changes="Distributed distinctive repeated photographed detail could support an overlap; failure alone cannot establish different surfaces.",
         origins=[{"path":"research/continuation_35/results.json"},{"path":"research/continuation_35/feature_results.json"}],execution="Fixed six-pair SIFT/RANSAC experiment and original-pixel inspection; two positive controls pass, both candidate boundaries fail the declared distribution gate.")
    e35_feature_rows = {row["id"]:row for row in read(root,"research/continuation_35/feature_results.json")["results"]}
    for row in e35["screen_results"][:2]:
        paths = [s["path"] for s in e35_feature_rows[row["id"]]["sources"]]
        claim("interpretation:E35:"+row["id"],image_by_path[paths[0]],"photographic_overlap",image_by_path[paths[1]],
              "researcher_interpretation","research/continuation_35/results.json","unresolved","suggested",scope="photograph overlap only; no physical seam or medieval side assignment",limits=e35["not_established"],numerical_result=row,independent_confirmation=False)

    # Enrich the existing imaging question; a descriptor audit is not another
    # independent lead, source region or historical relationship.
    leads["E35-overlap"]["supporting"] += [e41["direct_result"], e41["control_result"]]
    leads["E35-overlap"]["origins"].append({"path":"research/continuation_41/results.json"})
    leads["E35-overlap"]["required_inputs"]["local_tasks"] = [e41["next_test"]]
    leads["E35-overlap"]["strongest_feasible_test"] = e41["next_test"]
    leads["E35-overlap"]["test_execution"] += " E41 audits all 50 candidate correspondences plus 13 control correspondences without refitting; no distinctive candidate context is accepted."
    for interpretation in claims:
        if interpretation["id"] in {"interpretation:E35:8994-1-2", "interpretation:E35:8994-3-4"}:
            ident = interpretation["id"].split(":", 2)[-1]
            interpretation["manual_context_audit"] = {"source":"research/continuation_41/results.json",
                "summary":e41["summaries"][ident], "independent_confirmation":False,
                "accepted_photographic_overlap":False, "complete_surface_map_established":False,
                "limits":[e41["interpretation"], e41["prior_exposure"]]}

    leads["E34-local-order"]["supporting"] += [e42["row_count_result"],e42["text_result"]]
    leads["E34-local-order"]["origins"].append({"path":"research/continuation_42/results.json"})
    leads["E34-local-order"]["test_execution"] += " E42 now records exact boundary fragments and all four predeclared row-count/text comparisons, including both wrong-grouping controls; no complete diplomatic transcription or surface map."
    leads["E34-local-order"]["required_inputs"]["local_tasks"] = [e42["next_action"]]
    leads["E34-local-order"]["strongest_feasible_test"] = e42["next_action"]
    leads["E35-overlap"]["origins"].append({"path":"research/continuation_42/results.json"})
    leads["E35-overlap"]["required_inputs"]["local_tasks"] = [e42["next_action"]]
    leads["E35-overlap"]["strongest_feasible_test"] = e42["next_action"]
    leads["E35-overlap"]["test_execution"] += " E42 row-count and boundary-text follow-up completed; all proposed and wrong groupings sum to11, so the count does not discriminate."
    for row in e54_pairs:
        current=leads[row['lead_id']]
        current['primary_pair_test_pending']=False
        current['primary_pair_test_execution_state']='Initial selected-view mark/context comparison recorded; historical adjudication and diagnostic collation incomplete'
        current['test_execution']='E54 direct selected-source comparison: original-mark candidates, service context and broad writing fields; no historical book decision.'
        current['origins'].append({'path':'research/continuation_54/pair_comparisons.json','id':row['lead_id']})
        current['supporting'].append(' / '.join(row['contexts'][obj]['context'] for obj in row['pair']))
        current['contradicting'].append(row['limits'])
        if row['equal_ix_source_result']:
            current['contradicting'].append(row['equal_ix_source_result'])
        current['required_inputs']['local_tasks']=[row['next_test']]
        current['strongest_feasible_test']=row['next_test']
        current['retained_primary_comparison']={'path':'research/continuation_54/pair_comparisons.json',
            'selected_view_inspection_complete':True,'complete_source_photo_coverage':row['complete_source_photo_coverage'],
            'historical_adjudication_complete':False,'complete_corresponding_diagnostic_work_established':False,
            'unique_shared_original_address_established':False,
            'regions':['evidence:'+i for i in row['source_regions']]}
    claim('observation:E54-marks','object:mpo-10407','describes','object:mpo-1385',
        'project_observation','research/continuation_54/results.json','supported','asserted',
        scope='Visibility limits of the proposed shared IX catalogue clue, not shared historical address or codex identity',
        supports=['evidence:I54-10407-ix','evidence:I54-10407-i','evidence:I54-1385-first-edge','evidence:I54-1385-third-edge'],
        source_readings_unblinded=True,shared_ix_independently_read=False,
        unique_shared_original_address_established=False,original_side_mapping_complete=False,
        historical_book_decision=False,independent_confirmation=False,new_discovery=False)
    claim('observation:E54-reuse','image:'+e54_captures[7]['path'],'describes','object:mpo-10437',
        'project_observation','research/continuation_54/results.json','supported','asserted',
        scope='Binding straps/sewing laid over medieval text, observed as later reuse rather than original quire construction',
        supports=['evidence:I54-10437-reuse'],original_quire_structure_established=False,
        physical_join_established=False,independent_confirmation=False,new_discovery=False)
    leads['ant49-audit']['origins'].append({'path':'research/continuation_54/results.json'})
    leads['ant49-audit']['test_execution'] += ' E54 closes the remaining initial-comparison flags outside Ant49; this does not complete historical tests.'
    leads['ant49-audit']['strongest_feasible_test']='For Ant49, collate an exact corresponding work/variant if available; the full published wrong-book argument still needs20106. Generic broad-field/five-rule screens are exhausted as identity discriminators.'
    leads['ant49-audit']['required_inputs']['local_tasks']=[leads['ant49-audit']['strongest_feasible_test']]
    for ident in ["E34-local-order","E35-overlap"]:
        leads[ident]["origins"].append({"path":"research/continuation_43/coverage_audit.json"})
        leads[ident]["required_inputs"]["local_tasks"] = ["E43 completed the full register/source-credit audit. "+e43["next_test"]["question"]]
        leads[ident]["strongest_feasible_test"] = "E43 audit completed; next existing Ant49 comparison: Fr8066/Fr9620. "+e43["next_test"]["question"]

    e44_pair=pair_id(pair_key(*e44["pair"]))
    local_lead=leads[e44_pair]
    local_lead["supporting"] = [e44["direct_result"],e44["text_result"]]
    local_lead["contradicting"] = [
        "The selected five-rule feature also occurs in the published different-book control, so it cannot uniquely identify one book.",
        "Shared liturgical tradition and composite or abbreviated sections remain alternatives. No new source-visible same-book exclusion is established."]
    local_lead["origins"].append({"path":"research/continuation_44/results.json"})
    local_lead["test_execution"]="E44 direct exploratory text/ruling comparison of nine native source photographs and four fixed first-capture controls; no verified complete office position, codex identity or independent notation review."
    local_lead["required_inputs"]["local_tasks"]=[e44["next_test"]]
    for cap in e44_captures:
        local_lead["required_inputs"]["available_primary_images"][cap["physical_object_id"]].append(cap["path"])
    local_lead["strongest_feasible_test"]=e44["next_test"]
    claim("interpretation:E44-8066-9620","object:mpo-8066","same_codex","object:mpo-9620",
        "researcher_interpretation","research/continuation_44/results.json","unresolved","suggested",
        scope=e44["scope"],supports=["evidence:"+i for i in e44["observations"]],limits=e44["not_established"],
        four_vs_five_split_supported=False,different_book_genres_established=False,
        duplicated_complete_opening_established=False,same_codex_established=False,
        physical_join_established=False,catalogue_correction_confirmed=False,
        novelty_cleared=False,independent_confirmation=False,new_discovery=False)
    leads["ant49-audit"]["supporting"] += [e44["direct_result"],e44["text_result"]]
    leads["ant49-audit"]["origins"].append({"path":"research/continuation_44/results.json"})
    leads["ant49-audit"]["test_execution"]="E44 source test of the existing8066/9620 pair; published8201/8304 negative preserved and20106 image still missing."
    leads["ant49-audit"]["strongest_feasible_test"]=e44["next_test"]
    leads["ant49-audit"]["required_inputs"]["local_tasks"]=[e44["next_test"]]
    for current in [local_lead,leads["ant49-audit"]]:
        current["supporting"].append(e45["result"])
        current["origins"].append({"path":"research/continuation_45/results.json"})
        current["already_published"].append({"statement":e45["literature_scope_result"],
            "sources":["research/continuation_45/sources.json","https://doi.org/10.25167/ls.4818"],
            "kind":"published study scope, not a source adjudication of this pair"})
        current["test_execution"] += " E45 checks all nine retained photographs for service labels and partial corresponding verse material; no full same-position duplicate or secure diagnostic variant."
        current["strongest_feasible_test"]=e45["next_action"]
        current["required_inputs"]["local_tasks"]=[e45["next_action"]]
    interpretation=next(c for c in claims if c["id"]=="interpretation:E44-8066-9620")
    interpretation["provenance"].append({"source":source("research/continuation_45/results.json"),"locator":None})
    interpretation["supports"] += ["evidence:"+i for i in e45["observations"]]
    interpretation["service_recheck"]={"source":"research/continuation_45/results.json","result":e45["result"],
        "complete_duplicate_opening_established":False,"different_codex_established":False,
        "distinctive_variant_established":False,"independent_confirmation":False}
    for current in [local_lead,leads["ant49-audit"]]:
        current["contradicting"].append(e46["result"])
        current["origins"].append({"path":"research/continuation_46/results.json"})
        current["test_execution"] += " E46 compares the actual head groups and explores ordinal positions; full interval transcription remains incomplete and related work IDs remain provisional."
        current["strongest_feasible_test"]=e46["pair_next_test"]
        current["required_inputs"]["local_tasks"]=[e46["pair_next_test"]]
    interpretation["provenance"].append({"source":source("research/continuation_46/results.json"),"locator":None})
    interpretation["music_recheck"]={"source":"research/continuation_46/results.json","result":e46["result"],
        "same_complete_chant_identification_established":False,"diagnostic_melodic_variant_established":False,
        "different_codex_established":False,"independent_confirmation":False}
    for item in e46["candidate_identifications"]:
        ident=item["candidate_cantus_id"]
        chant_id=entity("chant:cantus-"+ident,"Chant",item["external_title"]+" ("+ident+")",
            cantus_id=ident,reference_url=item["reference"],
            identification_scope="Known external chant concept; its local fragment occurrence remains a qualified candidate.")
        regions=["I45-9620-Vidi","I46-9620-ending"] if item["object_id"]=="mpo-9620" else ["I45-8066-Vidi","I45-8066-Vidi-cont","I46-8066-verse-end"]
        claim("interpretation:E46:"+item["object_id"],"object:"+item["object_id"],"chant_identification",chant_id,
            "researcher_interpretation","research/continuation_46/results.json","unresolved","suggested",
            scope="Selected partial Jacob passage; reference-assisted candidate work identification only",
            supports=["evidence:"+r for r in regions],candidate_only=True,
            exact_local_work_confirmed=False,service_position_confirmed=False,
            whole_book_genre_assigned=False,independent_confirmation=False,
            limits=[item["state"],item["source_fit"]])
    claim("observation:E46-headgroups",image_by_path[next(c["path"] for c in e44_captures if c["path"].endswith("Fr8066-capture-2-native.jpg"))],"melodic_excerpt_comparison",
        image_by_path[next(c["path"] for c in e44_captures if c["path"].endswith("Fr9620-capture-4-native.jpg"))],
        "project_observation","research/continuation_46/results.json","supported","asserted",
        scope="Visible celos head grouping only, with provisional sounded-event interpretation; no same-work melodic variant or book exclusion",
        supports=["evidence:I46-8066-music-window","evidence:I46-9620-music-window"],
        visible_candidate_head_counts={"8066":5,"9620":2},exact_diatonic_intervals_verified=False,
        diagnostic_melodic_variant_established=False,different_codex_established=False,
        independent_confirmation=False,limits=e46["limits"])
    leads['ant49-audit']['supporting'].append(e48['unit_conflict']['result'])
    leads['ant49-audit']['origins'].append({'path':'research/continuation_48/results.json'})
    leads['ant49-audit']['test_execution'] += ' E48 compares exact BOMPAC-4861 membership with the published8201/8304 rejection; no new primary transcription.'
    leads['ant49-audit']['strongest_feasible_test']=e48['next_test']['question']
    leads['ant49-audit']['required_inputs']['local_tasks']=[e48['next_test']['question']]
    # A source recheck can support one part of a published argument without
    # claiming the unavailable second opening or merging a shelfmark lookalike.
    e49_primary=next(c for c in claims if c['id']=='interpretation:E48-unit4861')
    e49_primary['provenance'].append({'source':source('research/continuation_49/results.json'),'locator':None})
    e49_primary['primary_source_recheck']={'source':'research/continuation_49/results.json',
        'result':e49['direct_result'],'full_published_argument_replicated':False,
        'new_historical_exclusion':False,'missing_20106_source':True,
        'related_primary_regions':['evidence:'+i for i in e49['source_regions']],
        'scope':e49['interpretation'],'independent_confirmation':False}
    for current in [leads['ant49-audit'],leads[pair_id(pair_key(*e49['pair']))]]:
        current['origins'].append({'path':'research/continuation_49/results.json'})
        current['supporting'].append(e49['direct_result'])
        current['contradicting'].append(e49['interpretation'])
        current['test_execution'] += ' E49 inspects all eight retained8201/8304 photos; one local Catherine opening is supported, not a complete local replication of the published argument.'
        current['required_inputs']['local_tasks']=[e49['next_test']]
        current['strongest_feasible_test']=e49['next_test']
    candidate=e49_sources['candidate_catalogue_record']
    entity('record:manuscripta-101111','CatalogRecord','KB A103 / Manuscripta101111',
        physical_object=None,source_url=candidate['canonical_url'],crosswalk_status='unresolved',
        candidate_mpo_reference='Fr20106; reference coincidence only, no accepted physical crosswalk',
        source_record_scope=candidate['summary'],
        provenance=[{'source':source(candidate['canonical_url']),'locator':'Complete catalogue description; contents and binding/endleaves'}])
    entities['record:manuscripta-101111']['provenance'].append({'source':source('research/continuation_50/access_results.json'),
        'locator':'Bounded exact source-record lookup; crosswalk remains unresolved'})
    current=leads[e50['selected_lead']]
    current['primary_pair_test_pending']=False
    current['primary_pair_test_execution_state']='Partial; initial direct comparison recorded, planned full photo coverage and historical adjudication incomplete'
    current['test_execution']='E50 direct visible-layout test: seven target photo views and two retained control views; partial source coverage, no historical same-codex decision.'
    current['origins'].append({'path':'research/continuation_50/results.json'})
    current['contradicting'].append(e50['direct_result']+' '+e50['interpretation'])
    current['required_inputs']['local_tasks']=[e50['next_test']]
    missing_view=dependency('missing-source-view:mpo-2862:3','image','E50 exact native2862 capture3 request timed out and was stopped without retry; no retained third view was inspected.')
    current['required_inputs']['dependencies'].append(missing_view)
    current['strongest_feasible_test']=e50['next_test']
    for capture in e50_captures:
        current['required_inputs']['available_primary_images'][capture['physical_object_id']].append(capture['path'])
    claim('observation:E50-layout','object:mpo-10349','stylistic_similarity','object:mpo-2862',
        'project_observation','research/continuation_50/results.json','supported','asserted',polarity='negative',
        scope='Selected visible copying-field layout differs; not a historical same-codex exclusion or a complete original leaf/fold map.',
        supports=['evidence:'+i for i in e50['source_regions']],
        nominal_field_widths_cm=e50['measurement_summary'],
        post_inspection_measurements=True,wider_scale_sensitivity_overlaps=e50['wider_scale_sensitivity_overlaps'],
        original_leaf_fold_map_established=False,historical_same_codex_excluded=False,
        uniform_layout_unconditionally_excluded=False,independent_confirmation=False,new_discovery=False)
    claims[-1]['provenance'].append({'source':source('research/continuation_50/field_comparison.json'),
                                   'locator':'All post-inspection10–50px and additional-scale sensitivity outcomes'})
    # Latest-release metadata establishes distribution identity, not another
    # independent manuscript reconstruction or a novelty judgment.
    for release, filename in zip(e51['metadata_audit']['checked_releases'],
                                 ['combined-latest.json', 'raw-latest.json']):
        sid = source('research/continuation_51/' + filename)
        entities[sid].update(publisher_release_doi=release['doi'],
            publisher_version=release['version'], publication_date=release['publication_date'],
            latest_status_scope='Exact returned public latest-version API response on2026-10-30; not a permanent currentness claim')
    for row in e51['metadata_audit']['file_comparisons']:
        sid = source(row['path'])
        entities[sid]['distribution_recheck'] = {'source':source('research/continuation_51/metadata_comparison.json'),
            'current_release_doi':row['doi'], 'published_md5':row['published_current_md5'],
            'same_bytes_as_original_receipt':True, 'csv_bytes_checked':False,
            'independent_historical_confirmation':False}
    e49_primary['provenance'].append({'source':source('research/continuation_51/results.json'),
        'locator':'Latest XLSX distribution identity, not historical adjudication or independent reconstruction'})
    e49_primary['current_distribution_recheck'] = e51['metadata_audit']['current_xlsx_assignment_scope']
    leads['ant49-audit']['origins'].append({'path':'research/continuation_51/results.json'})
    leads['ant49-audit']['supporting'].append(e51['metadata_audit']['current_xlsx_assignment_scope'])
    entities['record:manuscripta-101111']['provenance'].append({'source':source('research/continuation_51/sources.json'),
        'locator':'Full k-series reference matters;20106 physical crosswalk remains unresolved'})
    current = leads[e51['selected_lead']]
    current['primary_pair_test_pending'] = False
    current['primary_pair_test_execution_state'] = 'Fixed six-view address audit completed; historical same-codex adjudication incomplete'
    current['test_execution'] = 'E51 direct margin/address audit: six target photographs and two retained8994 controls; no secure comparable original address or book decision.'
    current['origins'].append({'path':'research/continuation_51/results.json'})
    current['supporting'].append(e51['direct_result'])
    current['contradicting'].append(e51['interpretation'])
    current['required_inputs']['local_tasks'] = [e51['next_test']]
    current['strongest_feasible_test'] = e51['next_test']
    claim('observation:E51-library-reference', 'image:data/images/mpo-20274-capture-2-1835px.jpg',
        'describes', 'record:mpo-20274', 'project_observation', 'research/continuation_51/results.json',
        'supported', 'asserted', scope='Later pencil library reference corresponds to this pinned catalogue identifier; no original medieval foliation or shared codex',
        supports=['evidence:I51-20274-library-label'],
        candidate_reading='KB / A103 k / CXVIII', medieval_folio_assigned=False,
        new_20106_crosswalk=False, independent_confirmation=False, new_discovery=False)
    # The complete pending Ant49 subgraph receives scoped primary comparisons;
    # a first inspection flag never supplies a historical attribution.
    missing_8072 = dependency('missing-source-view:mpo-8072:3','image',
        'E52 exact8072 capture3 request timed out and was stopped without retry; this photograph remains unseen.')
    for row in e52_pairs:
        current = leads[row['lead_id']]
        current['primary_pair_test_pending'] = False
        current['primary_pair_test_execution_state'] = 'Initial limited group comparison recorded; historical adjudication incomplete' + (';8072 photo coverage partial' if not row['all_planned_photo_views_inspected'] else '')
        current['test_execution'] = 'E52 direct Ant49 group-context comparison: actual text/rubric boundaries and copying layout; general features fail the known wrong-pair control, no complete diagnostic work/physical comparison.'
        current['origins'].append({'path':'research/continuation_52/pair_comparisons.json','id':row['lead_id']})
        current['supporting'].append(' / '.join(row['contexts'][obj]['context'] for obj in row['pair']))
        current['contradicting'].append('The known8201/8304 different-book pair also shares the observed general ruling/layout; this feature cannot establish the candidate identity. '+row['text_result'])
        current['required_inputs']['local_tasks'] = [row['next_test']]
        current['strongest_feasible_test'] = row['next_test']
        current['group_primary_comparison'] = {'path':'research/continuation_52/pair_comparisons.json',
            'all_planned_photo_views_inspected':row['all_planned_photo_views_inspected'],
            'requested_native_coverage_complete':row['requested_native_coverage_complete'],
            'historical_adjudication_complete':False,'complete_corresponding_diagnostic_passage_established':False,
            'regions':['evidence:'+i for i in row['primary_regions']]}
        if 'mpo-8072' in row['pair']:
            current['required_inputs']['dependencies'].append(missing_8072)
        for cap in e52_captures:
            if cap['physical_object_id'] in row['pair']:
                current['required_inputs']['available_primary_images'][cap['physical_object_id']].append(cap['path'])
    leads['ant49-audit']['origins'].append({'path':'research/continuation_52/results.json'})
    leads['ant49-audit']['contradicting'].append(e52['interpretation'])
    leads['ant49-audit']['test_execution'] += ' E52 records all13 previously source-only group-context comparisons; no historical book decision.'
    leads['ant49-audit']['strongest_feasible_test'] = e52['next_test']
    leads['ant49-audit']['required_inputs']['local_tasks'] = [e52['next_test']]
    for item in e52['candidate_chant_identifications']:
        ident = item['cantus_id']
        titles = {'001151':'Regem virginum (invitatory candidate)',
                  '005328':'Veni sponsa Christi (antiphon)', '007828':'Veni sponsa Christi (responsory)'}
        chant = entity('chant:cantus-'+ident,'Chant',titles[ident],cantus_id=ident,
            identification_scope='Known external work concept; local occurrence remains a qualified candidate, not book identity')
        claim('interpretation:E52:'+ident,'object:mpo-8072','chant_identification',chant,
            'researcher_interpretation','research/continuation_52/sources.json','unresolved','suggested',
            scope='Selected8072 local work/function candidate only; no transferred reference melody or service position',
            supports=['evidence:'+item['region']],candidate_only=True,
            local_liturgical_position_verified=False,exact_melody_verified=False,
            different_book_inferred=False,independent_confirmation=False,limits=[item['limit']])
    claim('observation:E52-two-occurrences','image:research/continuation_52/images/Fr8072-capture-1-native.jpg',
        'melodic_excerpt_comparison','image:research/continuation_52/images/Fr8072-capture-2-native.jpg',
        'project_observation','research/continuation_52/results.json','supported','asserted',
        scope='Same Veni sponsa incipit with different visible text continuations and notational elaboration within the catalogue object; no exact same-work melody/interval claim',
        supports=['evidence:I52-8072-veni','evidence:I52-8072-veni-response'],
        exact_pitch_intervals_transcribed=False,same_chant_item_established=False,
        whole_surface_mapping_complete=False,historical_book_decision=False,
        independent_confirmation=False,new_discovery=False)
    claim('observation:E52-mixed-blocks','image:research/continuation_52/images/Fr8073-capture-3-native.jpg',
        'describes','object:mpo-8073','project_observation','research/continuation_52/results.json','supported','asserted',
        scope='Visible Magnificat antiphon rubric alongside continuous verse blocks; not a separate whole-book genre or codex attribution',
        supports=['evidence:I52-8073-magnificat-rubric','evidence:I52-8073-unnotated-verses'],
        whole_book_genre_assigned=False,historical_book_decision=False,
        independent_confirmation=False,new_discovery=False)
    for row in e53_pairs:
        current=leads[row['lead_id']]
        current['primary_pair_test_pending']=False
        current['primary_pair_test_execution_state']='Selected retained-view context comparison completed; historical adjudication and complete diagnostic text/music collation incomplete'
        current['test_execution']='E53 direct retained-source comparison: actual service/hymn context and copying fields; selected views inspected, no historical book decision.'
        current['origins'].append({'path':'research/continuation_53/pair_comparisons.json','id':row['lead_id']})
        current['supporting'].append(' / '.join(row['contexts'][obj]['context'] for obj in row['pair']))
        current['contradicting'].append(row['limits'])
        if row['hymn_comparison']:
            current['contradicting'].append(row['hymn_comparison'])
        if row['local_field_design_difference']:
            current['contradicting'].append('Observed writing-field design differs. This challenges an unchanged uniform copying template, not all section/composite same-volume alternatives.')
        current['required_inputs']['local_tasks']=[row['next_test']]
        current['strongest_feasible_test']=row['next_test']
        current['retained_primary_comparison']={'path':'research/continuation_53/pair_comparisons.json',
            'selected_view_inspection_complete':True,'complete_source_photo_coverage':row['complete_source_photo_coverage'],
            'historical_adjudication_complete':False,'complete_corresponding_diagnostic_work_established':False,
            'regions':['evidence:'+i for i in row['source_regions']]}
    for item in e53['candidate_chant_identifications']:
        ident=item['candidate_cantus_id']
        title='Jesu salvator saeculi / redemptis ope' if ident=='008333' else 'Jesu redemptor saeculi / verbum patris'
        chant=entity('chant:cantus-'+ident,'Chant',title,cantus_id=ident,reference_url=item['reference'],
            identification_scope='Known external hymn concept; the selected local reading remains a qualified candidate')
        claim('interpretation:E53:'+ident,'object:'+item['object_id'],'chant_identification',chant,
            'researcher_interpretation','research/continuation_53/sources.json','unresolved','suggested',
            scope='Selected hymn opening and partial continuation; no complete local text/music edition or book identity',
            supports=['evidence:'+item['region']],candidate_only=True,
            exact_complete_local_work_confirmed=False,exact_melody_verified=False,
            local_liturgical_position_verified=False,independent_confirmation=False,
            limits=[item['state'],'The Tu-fabricator stanza is already indexed in other witnesses; omission from one selected full-text listing does not establish novelty.'])
    layout_claim=next(c for c in claims if c['id']=='observation:E50-layout')
    layout_claim['provenance'].append({'source':source('research/continuation_53/results.json'),
        'locator':'Additional retained2863/2864/2872/2873 broad-field context; no expansion of the original pair claim to book identity'})
    for ident in ["E34-local-order","E35-overlap"]:
        leads[ident]["required_inputs"]["local_tasks"]=["E43 whole-register audit and the separate E44 Ant49 comparison are completed. Fr8994's fold/surface mapping remains unresolved; repeat image fitting only if genuinely new discriminating source information warrants it."]
        leads[ident]["strongest_feasible_test"]="Establish a defensible original capture/medieval-side convention or distinctive shared source detail and compare the designated Finnish original; the completed row-count and feature screens cannot supply that mapping."
    e42_sources=read(root,"research/continuation_42/protocol.json")["fixed_sources"]
    for left,right,state,regions in [(1,2,"unresolved",["I42-8994-c1-last-two","I34-8994-novo","I42-8994-c2-second-row"]),
                                     (3,4,"supported",["I42-8994-c3-last-two","I42-8994-c4-first-row","I40-8994-nocte"])]:
        comparison=next(r for r in e42["comparisons"] if r["pair"]==[left,right])
        claim(f"interpretation:E42:{left}-{right}",image_by_path[e42_sources[left-1]],"textual_continuation",image_by_path[e42_sources[right-1]],
            "researcher_interpretation","research/continuation_42/results.json",state,"suggested",
            scope="Local provisional word/phrase continuation only; not repeated ink, immediate physical adjacency or a complete medieval surface",
            supports=["evidence:"+r for r in regions],comparison=comparison,
            physical_adjacency_established=False,physical_join_established=False,
            complete_surface_map_established=False,accepted_photographic_overlap=False,
            new_codex_attribution=False,novelty_cleared=False,independent_confirmation=False,
            limits=[e42["scope"],"All four pairings total11 visible text rows; the count cannot choose a grouping.","Uncertain o and abbreviation expansions remain explicit; modern reference assistance is not another manuscript witness."])

    for edge in e36["edges"]:
        evidence_ids = ["evidence:"+x for x in edge["from_regions"]+edge["to_regions"]]
        lead("E36-"+edge["id"],"Aboense "+edge["id"].split("-")[-1]+" source-image continuation control",
             ["object:"+edge["from"],"object:"+edge["to"]],"textual_continuation",edge["result"],
             [{"statement":"This exact continuation was already stated in the MPO catalogue; E36 adds image-linked inspection, not a discovery.","sources":["data/reconstruction.json","https://zenodo.org/records/17287665"]}],edge["from_regions"]+edge["to_regions"],edge["limits"],
             "Review literal readings and the provisional catalogue-side mapping; seek physical or distinctive textual evidence for any new same-codex claim.",
             {"dependencies":[],"local_tasks":["Independent source reading remains possible; no outreach has been authorized or performed."]},"previously_documented",
             changes="A corrected reading or secure conflicting side mapping would change the new image interpretation; the prior assertion remains attributed separately.",
             origins=[{"path":"research/continuation_36/results.json","id":edge["id"]}],execution=e36["execution"],local_observation_state=edge["local_observation_state"],independent_confirmation=False)
        claim("interpretation:E36:"+edge["id"],"object:"+edge["from"],"textual_continuation","object:"+edge["to"],
              "researcher_interpretation","research/continuation_36/results.json",edge["local_observation_state"],"suggested",
              scope="Previously catalogued local text boundary only; no newly established book identity",supports=evidence_ids,
              limits=edge["limits"],catalogue_from=edge["catalogue_from"],catalogue_to=edge["catalogue_to"],independent_confirmation=False)
        pair_lead = leads[pair_id(pair_key(edge["from"],edge["to"]))]
        pair_lead["test_execution"] = "Existing dossier plus E36 direct boundary inspection; narrow text support is distinct from new codex identity."
        pair_lead["supporting"].append(edge["result"])
        pair_lead["contradicting"].extend(edge["limits"])
        pair_lead["origins"].append({"path":"research/continuation_36/results.json","id":edge["id"]})

    # Textual works are distinct from physical books. Identifying one surviving
    # ending neither creates a codex assignment nor classifies an entire office.
    standard = entity("chant:o-maria-stans-sub-cruce", "Chant", "O Maria stans sub cruce",
                      identification_scope="Published text; Fr 20274 identification is based on its surviving ending, with incipit missing", cantus_id=None)
    older = entity("chant:o-maria-dolorosa", "Chant", "O Maria dolorosa",
                   identification_scope="Published older C23 antiphon text; retained 71v ending inspected", cantus_id=None)
    c435 = entity("codex:uub-C435", "Codex", "Uppsala University Library C435",
                   identity_status="Extant manuscript reported in scholarship; no local source image or merger with fragments")
    dependency("missing-c435-original", "image", "C435's relevant original pages remain uninspected. Hallqvist 2020 reports author-held photographs; a current ordinary Alvin search met verification and was stopped. No current universal unavailability is inferred.")
    dependency("missing-c23-replacement-69r", "image", "The specific C23 added/replacement page 69r is not locally imaged; the retained older 71v ending must not stand in for it.")
    supports = ["evidence:"+x for x in e37["target_observations"]]
    comparison = ["evidence:"+x for x in e37["comparison_observations"]]
    claim("interpretation:E37-ending", "object:mpo-20274", "chant_identification", standard,
          "researcher_interpretation", "research/continuation_37/results.json", "supported", "suggested",
          scope=e37["scope"], supports=supports, contextual_evidence=comparison, limits=e37["limits"],
          claim_extent="surviving_ending", whole_office_recension_established=False, independent_confirmation=False)
    claim("interpretation:E37-C23-old-ending", "object:uub-c23", "chant_identification", older,
          "researcher_interpretation", "research/continuation_37/results.json", "supported", "suggested",
          scope="Selected retained C23 71v older ending only; not the added replacement on 69r", supports=comparison,independent_confirmation=False)
    claim("publication:E37-antiphon-replacement", standard, "liturgical_relationship", older,
          "source_assertion", "https://doi.org/10.6082/uchicago.1751", "previously_documented", "asserted",
          scope="Urberg's published C23 antiphon replacement account; not a claim of target descent or same codex",
          locator="Printed pp.254–257 / PDF280–283", source_statement_date="2016", retained_pdf_sha256=e37["previously_published"]["Urberg2016"]["sha256"])
    prior = [{"statement":value["statement"],"sources":[value["url"]],"locator":value["locator"]} for value in e37["previously_published"].values()]
    lead("E37-ending", "Fr 20274 identifies the shorter Magnificat-antiphon ending", ["object:mpo-20274",standard,older],
         "chant_identification", e37["new_source_observation"],prior,e37["target_observations"]+e37["comparison_observations"],e37["limits"],e37["next_test"],
         {"dependencies":["missing-c23-replacement-69r","missing-c435-original"],"local_tasks":["Review all four original source regions; manuscript-pitch comparison remains a separate unperformed test."]},
         "supported",changes="A corrected reading of the differentiating phrases would change the selected-ending identification. A different passage or shared common words alone cannot establish a whole-office version or codex identity.",
         origins=[{"path":"research/continuation_37/results.json"},{"path":"research/continuation_37/observations.json"}],
         execution="Relevant Urberg/Hallqvist passages read and checked; four exact manuscript regions inspected; exploratory literature-assisted reading, not independent confirmation.",
         independent_confirmation=False,whole_office_recension_established=False)
    lead("E37-C435-access", "C435 original-image dependency", [c435], "chant_identification",
         "Can the reported C435 word readings be verified on original pages?",prior,[],[e37["access_dependency"]],
         "Obtain a specifically identified lawful C435 original view for the antiphon and following invitatory; no outreach is authorized.",
         {"dependencies":["missing-c435-original"]},"not_testable",changes="Legitimate original images and exact page mapping would make this particular source verification testable; no global project blocker follows.",
         origins=[{"path":"research/continuation_37/access_and_reading.json"}],execution="2020 access statement checked on the complete PDF page; current ordinary catalogue search stopped at verification, with no scan obtained.")

    # The previously missing comparator is now present. Retain the historical
    # dependency record, but do not continue presenting it as a current blocker.
    dependencies["missing-c23-replacement-69r"].update(
        state="resolved", external=False,
        description="E38 obtained and inspected the explicitly labelled C23 69r page through its public viewer. The retained older 71v remains a different comparison page.",
        resolution_source="research/continuation_38/results.json")
    leads["E37-ending"]["required_inputs"] = {
        "dependencies":["missing-c435-original"],
        "local_tasks":[e38["next_test"]]}
    leads["E37-ending"]["strongest_feasible_test"] = e38["next_test"]
    leads["E37-ending"]["contradicting"] = [
        "C435 original pages remain uninspected; E38 has now inspected the formerly missing C23 69r comparator." if "specific C23 added/replacement" in item else item
        for item in leads["E37-ending"]["contradicting"]]
    leads["E37-ending"]["test_execution"] += " E38 subsequently verified the selected text on actual C23 69r."
    leads["E37-ending"]["origins"].append({"path":"research/continuation_38/results.json"})
    claim("interpretation:E38-replacement-text", "object:mpo-20274", "chant_identification", standard,
          "researcher_interpretation", "research/continuation_38/results.json", "supported", "suggested",
          scope=e38["scope"], supports=["evidence:"+x for x in e38["target_regions"]+e38["observations"]],
          limits=e38["limits"], claim_extent="surviving_ending", whole_office_recension_established=False,
          melodic_identity_established=False, independent_confirmation=False)
    lead("E38-replacement-text", "Fr 20274 ending checked against actual C23 69r", ["object:mpo-20274","object:uub-c23",standard],
         "chant_identification", e38["new_result"],
         [{"statement":e38["prior_art"],"sources":["RESEARCH_CONTINUATION_37.md"]}],
         e38["target_regions"]+e38["observations"],e38["limits"],e38["next_test"],
         {"dependencies":[],"local_tasks":[e38["music_test"]["remaining_work"]]},"supported",
         changes="A corrected reading of the differentiating words would change the selected-text comparison. Verified musical differences would change a future melodic claim, not establish a different book by themselves.",
         origins=[{"path":"research/continuation_38/results.json"},{"path":"research/continuation_38/observations.json"}],
         execution="Explicit folio label and PDM rights verified in the public browser; one exact TIFF acquired; selected incipit and ending compared directly. Pitch collation remains unperformed.",
         independent_confirmation=False,whole_office_recension_established=False,melodic_identity_established=False)

    # A partial staff-position comparison cannot become full melodic identity,
    # especially when overlapping alternatives remain unresolved.
    for ident in ["E37-ending", "E38-replacement-text"]:
        leads[ident]["strongest_feasible_test"] = e39["next_test"]
        leads[ident]["required_inputs"]["local_tasks"] = [e39["next_test"]]
        leads[ident]["test_execution"] = leads[ident]["test_execution"].replace("Pitch collation remains unperformed.", "") + " E39 now records a bounded relative-position comparison with two unresolved upper events; complete pitch transcription remains unverified."
        leads[ident]["origins"].append({"path":"research/continuation_39/results.json"})
    claim("interpretation:E39-excerpt", "object:mpo-20274", "melodic_excerpt_comparison", "object:uub-c23",
          "researcher_interpretation", "research/continuation_39/results.json", "unresolved", "suggested",
          scope=e39["scope"], supports=["evidence:"+x for x in e39["observations"]], limits=e39["limits"],
          provisional_concordant_positions=12, unresolved_positions=2, absolute_pitch_verified=False,
          melodic_identity_established=False, independent_confirmation=False)
    lead("E39-excerpt", "Partial chant-note comparison with two unresolved groups", ["object:mpo-20274","object:uub-c23",standard],
         "melodic_excerpt_comparison", e39["new_result"],
         [{"statement":e39["prior_art"]["statement"],"sources":["https://doi.org/10.6082/uchicago.1751"],"locator":e39["prior_art"]["locator"]}],
         e39["observations"],e39["limits"],e39["next_test"],
         {"dependencies":[],"local_tasks":[e39["next_test"]]},"unresolved",
         changes="A source-grounded correction of the two upper events and opening signs could resolve the bounded reading. Even exact common-melody agreement would not establish a parent codex or unique transmission branch.",
         origins=[{"path":"research/continuation_39/results.json"},{"path":"research/continuation_39/readings.v3.json"}],
         execution=e39["execution"], independent_confirmation=False, melodic_identity_established=False)

    for ident in ['E37-ending','E38-replacement-text','E39-excerpt']:
        current=leads[ident]
        current['test_execution'] += ' E55 performs a fixed local staff-calibration sensitivity test: both target upper events remain3/4, four of twelve complete rule models fail, and two spem anchors widen under the same sensitivity. No newly certified pitches.'
        current['origins'].append({'path':'research/continuation_55/results.json'})
        current['contradicting'].append(e55['direct_result']+' '+e55['further_uncertainty'])
        current['strongest_feasible_test']=e55['future_note_test']
        current['required_inputs']['local_tasks']=[e55['future_note_test']]
        current['staff_calibration_followup']={'path':'research/continuation_55/staff_calibration.json',
            'two_target_events_resolved':False,'complete_rule_calibration_succeeded':False,
            'robust_melodic_variant_established':False,'historical_book_decision':False}
    claim('observation:E55-calibration','object:mpo-20274','describes','object:uub-c23',
        'project_observation','research/continuation_55/results.json','supported','asserted',
        scope='Outcome of an unblinded geometric sensitivity diagnostic on fixed E39 anchors, not established musical pitches',
        supports=['evidence:'+i for i in e55['source_regions_reused']],
        valid_complete_rule_models=8,candidate_rule_models=12,two_target_events_resolved=False,
        exact_pitches_verified=False,robust_melodic_variant_established=False,
        melodic_identity_established=False,historical_book_decision=False,
        independent_confirmation=False,new_discovery=False)
    excerpt_claim=next(c for c in claims if c['id']=='interpretation:E39-excerpt')
    excerpt_claim['provenance'].append({'source':source('research/continuation_55/results.json'),
        'locator':'Bounded local staff calibration fails to resolve both upper events; two additional spem controls widen. The twelve E39 agreements are historical provisional readings.'})
    excerpt_claim['e55_geometric_diagnostic_resolved_events']=False

    museum_record=entity('record:turku-TKM23245-3','CatalogRecord','Turku City Museum TKM23245:3',source_url=e56['sources']['museum'],physical_object=None)
    cf_record=entity('record:codicesfennici-249','CatalogRecord','Codices Fennici fragment C',source_url=e56['sources']['codices'],physical_object=None)
    literal_ref=entity('identifier:literal-fm-II-157','Identifier','F.m. II.157 as printed',canonical_referent=None)
    claim('interpretation:E56-record-crosswalk',museum_record,'suggested_association',cf_record,
        'researcher_interpretation','research/continuation_56/results.json','supported','suggested',
        scope='Matching catalogue descriptions; source text is shared, not independent corroboration',
        physical_identity_independently_verified=False,new_discovery=False)
    claim('assertion:E56-printed-reference',cf_record,'describes',literal_ref,
        'source_assertion','research/continuation_56/TMMA_fragC.xml','previously_documented','suggested',
        scope='Published possible sewing-hole relationship and placement; literal II.157 retained',
        original_holes_inspected=False,historical_placement_verified=False,new_discovery=False)
    claim('interpretation:E56-reference',literal_ref,'suggested_association','codex:fm-IV.157',
        'researcher_interpretation','research/continuation_56/results.json','unresolved','suggested',
        scope='Possible intended IV.157 reference, not a confirmed emendation or physical join',
        catalogue_emendation_confirmed=False,independent_confirmation=False,new_discovery=False)
    current=leads['turku-ms-c']
    current['subjects'] += [museum_record,cf_record]
    current['supporting'] += e56['findings'][:1]
    current['contradicting'] += e56['findings'][1:3]
    current['origins'].append({'path':'research/continuation_56/results.json'})
    current['test_execution']='E56 compared exact museum/CF descriptions with the older Helsinki catalogue and indexed updated catalogue; no new source photographs inspected.'
    current['strongest_feasible_test']='Verify the historical archive alias and intended II.157/IV.157 reference using an authoritative record or original-object evidence; preserve the one-folio discrepancy.'
    current['required_inputs']['local_tasks']=[current['strongest_feasible_test']]
    handlist_record=entity('record:handlist-turku-c','CatalogRecord','Attributed handlist item 19: Turku museum fragment C',
        source_url=e83['source']['accessed_reproduction'], physical_object=None,
        source_scope='Third-party reproduction; exact publisher version and Finnish translation unverified')
    handlist_claim=claim('assertion:E83-handlist-iv156',handlist_record,'same_codex','codex:fm-IV.156',
        'source_assertion','research/continuation_83/results.json','previously_documented','asserted',
        scope='Attributed handlist assertion concerning museum C; not an independent project book attribution',
        locator=e83['source']['locator'], physical_identity_independently_verified=False,
        original_2008_page_read=False, independent_confirmation=False, new_discovery=False)
    ref_claim=next(c for c in claims if c['id']=='interpretation:E56-reference')
    ref_claim['provenance'].append({'source':source('research/continuation_83/results.json'),
        'locator':'Attributed handlist names IV.156 for matching museum fragment; IV.157 preference withdrawn'})
    ref_claim['contrary_source_claim_id']=handlist_claim
    ref_claim['scope']='Possible IV.157 referent, no longer preferred; an attributed handlist names IV.156 for matching museum C; both remain unresolved'
    current['subjects'].append(handlist_record)
    current['contradicting'].append(e83['consequence'])
    current['origins'].append({'path':'research/continuation_83/results.json'})
    current['test_execution'] += ' E83 found an attributed handlist naming IV.156 for the matching museum C; source reproduction and original 2008 page remain unverified.'
    current['strongest_feasible_test']='Authenticate the handlist and Keskiaho 2008 p.326; reconcile IV.156 against the TEI literal II.157 and its folio placement, independently of the museum/archive crosswalk.'
    current['required_inputs']['local_tasks']=[current['strongest_feasible_test']]
    crosswalk_claim=next(c for c in claims if c['id']=='interpretation:E56-record-crosswalk')
    crosswalk_claim['provenance'].append({'source':source('research/continuation_84/results.json'),
        'locator':'Public museum thumbnail versus CF viewer first face; visual comparison is likely shared photography'})
    crosswalk_claim['scope']='Strong record crosswalk from matching descriptions and public images; shared photography, not independent physical identity verification'
    claim('observation:E84-record-images',museum_record,'suggested_association',cf_record,
        'project_observation','research/continuation_84/results.json','supported','suggested',
        scope='Viewed public images share red O, uneven edge, fold and text layout; image may be shared, not independently photographed',
        locator='Museum overview thumbnail and CF viewer first face; full institutional viewer URLs in source record',
        shared_photography_possible=True,physical_identity_independently_verified=False,
        helsinki_join_established=False,independent_confirmation=False,new_discovery=False)
    current['supporting'].append(e84['record_crosswalk'])
    current['origins'].append({'path':'research/continuation_84/results.json'})
    current['test_execution'] += ' E84 directly compared public museum and CF displays; matching images strengthen the record crosswalk but do not resolve archive Ms. c or the Helsinki join.'
    transcription_question=entity('question:E85-transcription','ResearchQuestion',
        'Turku Sicut mirra: redisti or dedisti?',
        source_url=e85['source']['record_url'],
        source_location=e85['source']['viewer_location'],
        viewer_fragment=e85['source']['observed_viewer_fragment'],
        navigation_warning=e85['source']['navigation_warning'])
    claim('observation:E85-word',cf_record,'method_correction',transcription_question,
        'project_observation','research/continuation_85/results.json','unresolved','suggested',
        scope='Plausible correction to modern catalogue text after reference-assisted viewing; not a codex attribution or new medieval text variant',
        locator=e85['source']['viewer_location'], literal_catalogue=e85['catalogue']['literal'],
        provisional_reading=e85['image_reading']['literal_candidate'],
        independent_confirmation=False, novelty_cleared=False, catalogue_correction_confirmed=False,
        new_discovery=False)
    current['origins'].append({'path':'research/continuation_85/results.json'})
    current['test_execution'] += ' E85 found a tentative text-only catalogue correction on the Turku viewer; it is unrelated to deciding the physical book association.'
    word_claim=next(c for c in claims if c['id']=='observation:E85-word')
    word_claim['provenance'].append({'source':source('research/continuation_86/results.json'),
        'locator':'Same-page d and r controls; same AI and image, with positional differences and a faded ending'})
    word_claim['local_control_conclusion']=e86['conclusion']
    word_claim['local_controls_independent']=False
    current['origins'].append({'path':'research/continuation_86/results.json'})
    current['test_execution'] += ' E86 rechecked that text-only candidate using same-page d/r controls; the same AI reading remains unverified.'
    current=leads['fr8311-chant']
    current['test_execution']='E57 unblinded comparison of four retained photos with selected published chant inventories; complete transcription and original-side map remain incomplete.'
    current['supporting'].append(e57['local_reading'])
    current['contradicting'].append(e57['prior_art']['comparison'])
    current['origins'].append({'path':'research/continuation_57/results.json'})
    current['strongest_feasible_test']=e57['next_test']
    current['required_inputs']['local_tasks']=[e57['next_test']]
    claim('observation:E57-8311-repertory','object:mpo-8311','describes','question:fr8311-chant',
        'project_observation','research/continuation_57/results.json','supported','asserted',
        scope='Selected provisional text windows and known-work candidates; not a complete musical edition or book identification',
        supports=['evidence:'+i for i in e57['source_regions']+e57['prior_regions']],
        complete_side_map=False,physical_join_established=False,exact_melody_verified=False,
        independent_confirmation=False,new_discovery=False)
    current['test_execution'] += ' E58 additionally checked text-edge continuity and selected indexed prior-art examples; no matching ink or full side map verified.'
    current['supporting'].append(e58['comparison'])
    current['contradicting'].append(e58['counterexample'])
    current['origins'].append({'path':'research/continuation_58/results.json'})
    current['strongest_feasible_test']=e58['next_test']
    current['required_inputs']['local_tasks']=[e58['next_test']]
    claim('observation:E58-8311-surface-scope','object:mpo-8311','describes','question:fr8311-chant',
        'project_observation','research/continuation_58/results.json','supported','asserted',
        scope='Text-edge assessment and indexed six-identifier counterexamples; partial unblinded reading',
        supports=['evidence:'+i for i in e58['regions']], physical_overlap_demonstrated=False,
        complete_side_map=False, new_discovery=False, independent_confirmation=False)

    # A catalogue-defined text boundary is not an inspected Finnish page or a
    # verified physical seam. Keep the proposed placement conditional.
    iv156_f9 = entity("leaf:fm-IV.156-9", "Leaf", "F.m.IV.156 catalogue folio 9",
        physical_parent="object:fm-IV.156", mapping_basis="Catalogue-described range opening; original image and complete signature not inspected")
    dependency("missing-iv156-f9", "image", "Exact original IV156 f9 opening, signature, notation and physical edge remain uninspected; the indexed catalogue description is not a replacement scan.")
    claim("interpretation:E40-boundary", "object:mpo-8994", "textual_continuation", iv156_f9,
          "researcher_interpretation", "research/continuation_40/results.json", "unresolved", "suggested",
          scope=e40["scope"], supports=["evidence:"+x for x in e40["observations"]], limits=e40["limits"],
          local_observation_state="supported", physical_adjacency_established=False,
          physical_join_established=False, complete_leaf_edge_verified=False,
          signature_successor_verified=False, test_prediction=e40["signature_prediction"], independent_confirmation=False)
    lead("E40-boundary", "Fr 8994 terminal words and the IV156 opening test", ["object:mpo-8994",iv156_f9],
         "textual_continuation", e40["new_result"],
         [{"statement":e40["already_published"],"sources":["RESEARCH_CONTINUATION_26.md","https://fragmenta.kansalliskirjasto.fi/handle/10024/1299"]}],
         e40["observations"],e40["limits"],e40["next_test"],
         {"dependencies":["missing-iv156-f9","side-map","unread-taitto","unread-keskiaho"],"local_tasks":["Review the five source regions and capture coverage; no claim of a Finnish image comparison or accepted photographic seam."]},"unresolved",
         changes="A verified incompatible original opening or side/numbering map would challenge the proposed placement. Compatible text alone would still require physical and source-specific evidence for codex identity.",
         origins=[{"path":"research/continuation_40/results.json"},{"path":"research/continuation_40/sources.json"}],
         execution="Read the selected Swedish terminal and preceding words directly; compared them with indexed Finnish catalogue boundaries and known-office concordance text. No Finnish original or complete side map obtained.",
         physical_adjacency_established=False,physical_join_established=False,independent_confirmation=False)
    leads["E40-boundary"]["contradicting"].append(e97["result"] + " " + e97["interpretation"])
    leads["E40-boundary"]["origins"].append({"path":"research/continuation_97/results.json"})
    leads["E40-boundary"]["test_execution"] += " E97 records faint marks after the last clearly read word; their status and function are unknown."
    mark97 = entity('question:E97-8994-faint-marks', 'ResearchQuestion',
                    'Fr 8994 faint marks after the last clearly transcribed word')
    claim('observation:E97-8994-marks','object:mpo-8994','describes',mark97,
          'project_observation','research/continuation_97/results.json','supported','asserted',
          scope='Faint marks are visible; their reading, origin and function are unverified and reference-exposed',
          supports=['evidence:'+i for i in e97['source_regions']+e97['reused_regions']],
          candidate_ut_verified=False,catchword_proved=False,finnish_image_inspected=False,
          physical_join_established=False,independent_confirmation=False,new_discovery=False)
    leads["E33-numbering-conflict"]["required_inputs"]["local_tasks"] = ["E40 adds a precise IV156 boundary test while preserving this conditional IV157 f8 conflict; original Finnish pages and Swedish surface mapping remain missing."]
    leads["E33-numbering-conflict"]["origins"].append({"path":"research/continuation_40/results.json"})

    use_question=entity('question:iv156-use-context','ResearchQuestion','F.m.IV.156 production and use: distinct historical questions')
    claim('published:E59-iv156-use','codex:fm-IV.156','describes',use_question,
          'source_assertion','research/continuation_59/sources.json','previously_documented','suggested',
          scope='Vuori and Räsänen 2025 discuss liturgy and propose a possible Turku Cathedral side-altar use; the proposal is attributed, not established',
          locator='pp. 208–209, 211–218, 220–221 (web-reader text; selected sections)',
          production_place_verified=False,use_place_verified=False,fr8994_identity_verified=False,independent_confirmation=False)
    for lead_id in ['iv156-1505','E40-boundary']:
        current=leads[lead_id]
        current['already_published'].append({'statement':e59['prior_study']+' '+e59['production_vs_use'],
                                             'sources':['research/continuation_59/sources.json']})
        current['contradicting'].append(e59['boundary_effect'])
        current['origins'].append({'path':'research/continuation_59/results.json'})
        current['required_inputs']['local_tasks']=[e59['claim_specific_next_test']]
        current['strongest_feasible_test']=e59['claim_specific_next_test']
    current=leads['iv156-1505']
    current['contradicting'].append(e60['conditional_result'])
    current['already_published'].append({'statement':e60['known_prior_art'],'sources':['research/continuation_60/sources.json']})
    current['origins'].append({'path':'research/continuation_60/results.json'})
    current['test_execution'] += ' E60 compares a Swedish numbered-image opening with indexed IV156 f.8 under explicit address/side assumptions.'
    current['strongest_feasible_test']=e60['next_test']
    current['required_inputs']['local_tasks']=[e60['next_test']]
    claim('interpretation:E60-10370-iv156','object:mpo-10370','suggested_association','codex:fm-IV.156',
          'researcher_interpretation','research/continuation_60/results.json','unresolved','suggested',
          scope='Conditional opening-text conflict if the compared address, side and completeness premises hold; not a historical exclusion',
          supports=['evidence:'+i for i in e60['source_regions']+e60['reused_regions']],
          finnish_image_inspected=False,same_address_verified=False,physical_identity_rejected=False,
          catalogue_error_proved=False,new_discovery=False,independent_confirmation=False)
    current['supporting'].append(e61['local_observation'])
    current['contradicting'].append(e61['comparison']+' '+e61['e60_effect'])
    current['origins'].append({'path':'research/continuation_61/results.json'})
    current['test_execution'] += ' E61 checked a damaged final-photo chant candidate and an indexed alternative liturgical order.'
    current['strongest_feasible_test']=e61['next_test']
    current['required_inputs']['local_tasks']=[e61['next_test']]
    context61=entity('question:E61-10370-context','ResearchQuestion','Fr 10370 chant context and incomplete ending')
    claim('observation:E61-10370-context','object:mpo-10370','describes',context61,
          'project_observation','research/continuation_61/results.json','supported','asserted',
          scope='Provisional selected Swedish text and reference order, not book identity',
          supports=['evidence:'+i for i in e61['source_regions']],
          finnish_image_inspected=False,adjacent_pages_proved=False,same_book_proved=False,
          e60_conflict_resolved=False,new_discovery=False,independent_confirmation=False)
    reuse90 = entity('question:E90-10370-reuse', 'ResearchQuestion',
                     'Fr 10370 account heading and the II.64 catalogue description')
    claim('observation:E90-10370-reuse','object:mpo-10370','describes',reuse90,
          'project_observation','research/continuation_90/results.json','supported','asserted',
          scope='Provisional reuse-heading reading, not an established same account, physical crosswalk or medieval book identification',
          supports=['evidence:'+e90['reused_annotation']],
          same_account_proved=False,same_object_proved=False,independent_confirmation=False,new_discovery=False)
    width92 = entity('question:E92-10370-width', 'ResearchQuestion',
                     'Fr 10370 image span and II.64 catalogue width')
    claim('observation:E92-10370-width','object:mpo-10370','describes',width92,
          'project_observation','research/continuation_92/results.json','supported','asserted',
          scope='Approximate Swedish image span under stated geometric assumptions; Finnish value is unverified catalogue metadata',
          supports=['evidence:'+i for i in e92['source_regions']],
          finnish_image_inspected=False,physical_exclusion_proved=False,
          same_book_proved=False,independent_confirmation=False,new_discovery=False)
    sequence93 = entity('question:E93-chant-context', 'ResearchQuestion',
                        'Fr 10407, Fr 10370 and a known Mary Magdalene sequence')
    claim('observation:E93-10407-sequence','object:mpo-10407','describes',sequence93,
          'project_observation','research/continuation_93/results.json','supported','asserted',
          scope='Provisional selected chant readings and published separate-manuscript control; neither adjacency nor a new codex',
          supports=['evidence:'+i for i in e93['source_regions']+e93['reused_regions']],
          paris_original_inspected=False,adjacency_proved=False,
          new_attribution=False,independent_confirmation=False,new_discovery=False)

    overlap112 = entity('question:E112-10406-iv156-f8', 'ResearchQuestion',
                        'Fr 10406 and IV.156 f.8: provisional shared St James passage')
    claim('observation:E112-10406-james','object:mpo-10406','describes',overlap112,
          'project_observation','research/continuation_112/observations.json','unresolved','suggested',
          scope='Reference-exposed Swedish reading and indexed Finnish catalogue wording with an unexplained bracket; extent of Finnish surviving ink unknown; no Finnish image, physical overlap, exclusion, or independent review',
          supports=['evidence:'+i for i in ['I112-10406-iacobi','I112-10406-postolos',
                   'I112-10406-final-om','I112-10406-niumpopulorum','I112-10406-laudande']],
          external_control='research/continuation_112/control_beban.json',
          finnish_image_inspected=False,physical_overlap_proved=False,
          same_book_proved=False,independent_confirmation=False,new_discovery=False)
    claim('observation:E113-10406-reuse','object:mpo-10406','describes',overlap112,
          'project_observation','research/continuation_113/results.json','unresolved','suggested',
          scope='A visible 1608-like mark and distinct reported account descriptions; not a binding date, physical exclusion or medieval book decision',
          supports=['evidence:I113-10406-date-mark'],finnish_image_inspected=False,
          physical_overlap_proved=False,same_book_proved=False,independent_confirmation=False,new_discovery=False)

    current=leads[pair_id(pair_key('finn-iv173','mpo-1385'))]
    current['supporting'].append(e63['target_observation'])
    current['contradicting'].extend([e63['control_result'],e63['positive_control_limitation'],e63['selection_limit']])
    current['origins'].append({'path':'research/continuation_63/results.json'})
    current['test_execution'] += ' E63 compares selected D initials against a different-book control; role-matched positive images are unavailable.'
    current['strongest_feasible_test']=e63['next_test']
    current['required_inputs']['local_tasks']=[e63['next_test']]
    claim('observation:E63-selected-D','object:finn-iv173','stylistic_similarity','object:mpo-1385',
          'project_observation','research/continuation_63/results.json','supported','asserted',
          scope='Selected red upright and pale field only; not same-codex or same-hand evidence',
          supports=['evidence:'+i for i in e63['source_regions']+e63['reused_control_regions']],
          role_matched_positive_available=False,unblinded=True,same_book_proved=False,
          different_book_proved=False,feature_uniqueness_proved=False,new_discovery=False,independent_confirmation=False)

    a103 = entity('identifier:historic-kb-A103-deposit','Identifier','Historic KB A 103 deposited fragment collection',
                  scheme='historic collection designation',value='A 103',
                  scope='National Library fragment deposit reported at the National Archives during 2003–2006; current custody not verified')
    claim('source:E64-A103-deposit','record:mpo-20106','suggested_association',a103,
          'researcher_interpretation','research/continuation_64/results.json','unresolved','suggested',
          scope='Collection-level inference from historic collection description and full catalogue reference; no physical object or image crosswalk',
          direct_fr20106_collection_assertion=False,current_holding_verified=False,image_pointer_verified=False,
          new_discovery=False,independent_confirmation=False)
    for ident in ['ant49-audit',pair_id(pair_key('mpo-20106','mpo-8201')),
                  pair_id(pair_key('mpo-8201','mpo-8304'))]:
        current=leads[ident]
        current['supporting'].append(e64['interpretation'])
        current['contradicting'].append(e64['limits'])
        current['origins'].append({'path':'research/continuation_64/results.json'})
        current['test_execution'] += ' E64 distinguishes the historical A 103 fragment deposit from the similarly named psalter; exact Fr20106 custody and image remain unverified.'
        current['strongest_feasible_test']=e64['next_test']
        current['required_inputs']['local_tasks']=[e64['next_test']]
    entities['record:manuscripta-101111']['provenance'].append({'source':source('research/continuation_64/sources.json'),
        'locator':'Distinct historic A 103 fragment collection; similar short shelfmark is not a physical crosswalk'})

    for ident in ['ant49-audit',pair_id(pair_key('mpo-20106','mpo-8201')),
                  pair_id(pair_key('mpo-8201','mpo-8304'))]:
        current=leads[ident]
        current['supporting'].append(e65['local_observation'])
        current['contradicting'].extend([e65['reference_observation'],e65['interpretation']])
        current['origins'].append({'path':'research/continuation_65/results.json'})
        current['test_execution'] += ' E65 adds a native-resolution Fr8201 text reading and a distinct indexed chant witness; Fr20106 remains uninspected.'
        current['strongest_feasible_test']=e65['next_test']
        current['required_inputs']['local_tasks']=[e65['next_test']]
    chant65=entity('chant:cantus-204720','Chant','Specie corporis decora nimis enituit',cantus_id='204720')
    claim('interpretation:E65-8201-ending','object:mpo-8201','chant_identification',chant65,
          'researcher_interpretation','research/continuation_65/results.json','unresolved','suggested',
          scope='Candidate surviving ending; beginning is missing locally and prior identification is credited',
          supports=['evidence:'+i for i in e65['source_regions']+e65['reused_regions']],
          local_full_chant_verified=False,fr20106_image_inspected=False,exact_melody_verified=False,
          physical_adjacency_proved=False,new_discovery=False,independent_confirmation=False)

    for ident in ['ant49-audit',pair_id(pair_key('mpo-20106','mpo-8201')),
                  pair_id(pair_key('mpo-8201','mpo-8304'))]:
        current=leads[ident]
        current['supporting'].append(e66['local_reading'])
        current['contradicting'].extend([e66['museum_comparison'],e66['prior_art'],e66['boundary_limit']])
        current['origins'].append({'path':'research/continuation_66/results.json'})
        current['test_execution'] += ' E66 compares a local responsory wording with attributed external transcriptions; no book identity conclusion.'
        current['strongest_feasible_test']=e66['next_test']
        current['required_inputs']['local_tasks']=[e66['next_test']]
    chant66=entity('chant:cantus-601492','Chant','Nobilis et pulchra',cantus_id='601492')
    claim('interpretation:E66-8201-nobilis','object:mpo-8201','chant_identification',chant66,
          'researcher_interpretation','research/continuation_66/results.json','unresolved','suggested',
          scope='Provisional selected responsory opening and wording; published comparison and prior occurrence do not establish book or lineage',
          supports=['evidence:'+i for i in e66['source_regions']+e66['reused_regions']],
          exact_fr20106_boundary_matched=False,external_originals_inspected=False,melodic_match_verified=False,
          historical_same_codex_proved=False,new_discovery=False,independent_confirmation=False)

    sziget1855 = entity('record:sziget-toldy-1855', 'CatalogRecord',
        'Sziget breviary as described by Toldy in 1855', record_kind='historical printed description',
        physical_object_verified=False, provenance=[{'source': source('research/continuation_67/sources.json'), 'locator': 'toldy_1855'}])
    debrecen1942 = entity('record:debrecen-167-1942', 'CatalogRecord',
        'Historic Debrecen breviary no. 167 as described in 1942', record_kind='historical printed description',
        current_shelfmark_verified=False, provenance=[{'source': source('research/continuation_67/sources.json'), 'locator': 'gabriel_1942'}])
    claim('interpretation:E67-sziget-candidate', sziget1855, 'suggested_association', debrecen1942,
        'researcher_interpretation', 'research/continuation_67/results.json', 'unresolved', 'suggested',
        scope='Possible crosswalk between historical descriptions; shared reported 1399 date, genre and Sziget association',
        same_book_proved=False, current_holding_verified=False, original_inspected=False,
        independent_confirmation=False, new_discovery=False)
    for ident in ['ant49-audit', pair_id(pair_key('mpo-20106','mpo-8201')),
                  pair_id(pair_key('mpo-8201','mpo-8304'))]:
        current = leads[ident]
        current['supporting'].append(e67['interpretation'])
        current['contradicting'].append(e67['limits'])
        current['origins'].append({'path':'research/continuation_67/results.json'})
        current['test_execution'] += ' E67 traces an older quotation to a possible historic manuscript record; the crosswalk and modern custody remain unverified.'
        current['strongest_feasible_test'] = e67['next_test']
        current['required_inputs']['local_tasks'] = [e67['next_test']]

    for ident in ['ant49-audit', pair_id(pair_key('mpo-20106','mpo-8201')),
                  pair_id(pair_key('mpo-8201','mpo-8304'))]:
        current = leads[ident]
        current['supporting'].append(e68['interpretation'])
        current['contradicting'].append(e68['limits'])
        current['origins'].append({'path':'research/continuation_68/results.json'})
        current['test_execution'] += ' E68 identifies the earlier article bibliographically and records a possible institutional connection; the article text and manuscript remain unread.'
        current['strongest_feasible_test'] = e68['next_test']
        current['required_inputs']['local_tasks'] = [e68['next_test']]
    entities[sziget1855]['provenance'].append({'source':source('research/continuation_68/sources.json'),
        'locator':'academy_record and biographical_entry; bibliographic and institutional context, no manuscript identity'})

    chant69 = entity('chant:cantus-202513', 'Chant', 'Inclita sanctae virginis Catharinae sollemnia', cantus_id='202513')
    claim('interpretation:E69-8304-opening', 'object:mpo-8304', 'chant_identification', chant69,
        'researcher_interpretation', 'research/continuation_69/results.json', 'unresolved', 'suggested',
        scope='Reference-exposed selected opening; uncertain word ending and no original-comparator inspection',
        supports=['evidence:'+i for i in e69['source_regions']],
        original_comparator_inspected=False, independent_confirmation=False, new_discovery=False)
    for ident in ['ant49-audit', pair_id(pair_key('mpo-20106','mpo-8201')),
                  pair_id(pair_key('mpo-8201','mpo-8304'))]:
        current = leads[ident]
        current['supporting'].append(e69['transcription_correction'])
        current['contradicting'].extend([e69['published_counterexample'], e69['interpretation'], e69['limits']])
        current['origins'].append({'path':'research/continuation_69/results.json'})
        current['test_execution'] += ' E69 adds published prior art on repeated Catherine openings and corrects an earlier provisional transcription; it does not replicate or refute the published target exclusion.'
        current['strongest_feasible_test'] = e69['next_test']
        current['required_inputs']['local_tasks'] = [e69['next_test']]

    pal527 = entity('codex:pal-lat-527', 'Codex', 'Vatican, Pal. lat. 527',
        identity_status='Named institutional breviary; separate comparative witness, not merged with Swedish fragments',
        viewer='https://digi.vatlib.it/view/MSS_Pal.lat.527')
    claim('interpretation:E70-pal527-opening', pal527, 'chant_identification', chant69,
        'project_observation', 'research/continuation_70/results.json', 'unresolved', 'suggested',
        scope='Selected reference-exposed Vatican viewer readings at folios 122r and 125v; second incipit abbreviated',
        locator='Vatican viewer, f.122r lower-middle and f.125v middle',
        independent_confirmation=False, exact_duplicate_rubric_verified=False,
        full_office_collated=False, original_images_saved=False, new_discovery=False)
    for ident in ['ant49-audit', pair_id(pair_key('mpo-20106','mpo-8201')),
                  pair_id(pair_key('mpo-8201','mpo-8304'))]:
        current = leads[ident]
        current['contradicting'] = [item.replace('Pal. lat. 527 was not examined directly',
            'At E69 Pal. lat. 527 had not been examined directly; E70 subsequently viewed selected folios') for item in current['contradicting']]
        current['supporting'].append(e70['published_comparison'])
        current['contradicting'].extend([e70['interpretation'], e70['limits']])
        current['origins'].append({'path':'research/continuation_70/results.json'})
        current['test_execution'] += ' E70 views selected labelled Vatican folios; duplicate full headings and the target Fr 20106 remain unverified.'
        current['strongest_feasible_test'] = e70['next_test']
        current['required_inputs']['local_tasks'] = [e70['next_test']]

    for ident in ['ant49-audit', pair_id(pair_key('mpo-20106','mpo-8201'))]:
        current = leads[ident]
        current['supporting'].append(e71['source_description'])
        current['contradicting'].extend([e71['conditional_test'], e71['limits']])
        current['origins'].append({'path':'research/continuation_71/results.json'})
        current['test_execution'] += ' E71 specifies a conditional physical-order test; no Fr 20106 sides were inspected and no contradiction was established.'
        current['strongest_feasible_test'] = e71['next_test']
        current['required_inputs']['local_tasks'] = [e71['next_test']]

    for ident in ['ant49-audit', pair_id(pair_key('mpo-20106','mpo-8201'))]:
        current = leads[ident]
        current['contradicting'].extend([e72['comparison'], e72['interpretation'], e72['limits']])
        current['origins'].append({'path':'research/continuation_72/results.json'})
        current['test_execution'] += ' E72 records a different published Barbara-office text sharing the Fr 8201 ending; the fuller wording and following sequence differ.'
        current['strongest_feasible_test'] = e72['next_test']
        current['required_inputs']['local_tasks'] = [e72['next_test']]

    chant73 = entity('chant:cantus-201813', 'Chant', 'Felix terra pariens caelum trinitatis', cantus_id='201813',
        identification_scope='Indexed work concept; local occurrence is a provisional reference-assisted identification')
    hymn73 = entity('chant:AH52-104', 'Chant', 'De stella sol oriturus', analytic_hymnica='52:104',
        identification_scope='Work already listed in the MPO catalogue; stanza reading is provisional')
    for ident, obj, region in [('antiphon', chant73, 'I73-8073-felix-terra'), ('hymn', hymn73, 'I73-8073-annam-hymn')]:
        claim('interpretation:E73-8073-'+ident, 'object:mpo-8073', 'chant_identification', obj,
            'researcher_interpretation', 'research/continuation_73/results.json', 'unresolved', 'suggested',
            scope='Selected Fr 8073 photograph, reference-exposed reading; no independently checked full transcription',
            supports=['evidence:'+region], independent_confirmation=False, new_discovery=False,
            original_side_order_verified=False, book_membership_inferred=False, exact_melody_verified=False)
    for current in leads.values():
        if current['id'] == 'ant49-audit' or ('object:mpo-8073' in current.get('subjects', []) and current['relationship_type'] == 'same_codex'):
            current['supporting'].extend([e73['local_antiphon'], e73['local_hymn']])
            current['contradicting'].extend([e73['comparison'], e73['limits']])
            current['origins'].append({'path':'research/continuation_73/results.json'})
            current['test_execution'] += ' E73 identifies a provisional Felix terra antiphon and checks a catalogued hymn against editions; no historical book decision.'

    claim('interpretation:E74-8073-text-boundary',
        'image:research/continuation_52/images/Fr8073-capture-2-native.jpg', 'textual_continuation',
        'image:research/continuation_52/images/Fr8073-capture-3-native.jpg',
        'researcher_interpretation', 'research/continuation_74/results.json', 'unresolved', 'suggested',
        scope='Provisional within-object text order car- / nis; original side identity and absence of intervening material are not established',
        supports=['evidence:'+i for i in e74['source_regions']],
        recto_verso_verified=False, immediate_physical_adjacency_verified=False,
        independent_confirmation=False, new_discovery=False)
    for current in leads.values():
        if current['id'] == 'ant49-audit' or ('object:mpo-8073' in current.get('subjects', []) and current['relationship_type'] == 'same_codex'):
            current['supporting'].append(e74['local_boundary'])
            current['contradicting'].extend([e74['published_controls'], e74['limits']])
            current['origins'].append({'path':'research/continuation_74/results.json'})
            current['test_execution'] += ' E74 records a provisional Fr 8073 intra-object car- / nis text boundary; original sides and book relationships remain unresolved.'

    claim('interpretation:E75-8073-responsory-context',
        'image:data/images/mpo-8073.jpg', 'textual_continuation',
        'image:research/continuation_52/images/Fr8073-capture-2-native.jpg',
        'researcher_interpretation', 'research/continuation_75/results.json', 'unresolved', 'suggested',
        scope='Possible successive responsory contexts; repeat cues do not establish common ink, physical adjacency or original side identity',
        supports=['evidence:'+i for i in e75['source_regions']],
        same_ink_verified=False, recto_verso_verified=False, immediate_physical_adjacency_verified=False,
        independent_confirmation=False, new_discovery=False)
    for current in leads.values():
        if current['id'] == 'ant49-audit' or ('object:mpo-8073' in current.get('subjects', []) and current['relationship_type'] == 'same_codex'):
            current['supporting'].append(e75['local_boundary'])
            current['contradicting'].extend([e75['published_controls'], e75['limits']])
            current['origins'].append({'path':'research/continuation_75/results.json'})
            current['test_execution'] += ' E75 records a possible responsory context across Fr 8073 views; common ink and physical adjacency are not verified.'

    luebeck76 = entity('codex:luebeck-theol-lat-2f-48a', 'Codex', 'Lübeck, Stadtbibliothek, Ms. theol. lat. 2° 48a',
        identity_status='Separate surviving collectar described by Schnabel; no link or merge with Swedish fragments',
        catalogue='https://diglib.hab.de/?catalog=Schnabel&db=mss&id=hl-sb-theol-lat-2f-48a&list=ms')
    claim('interpretation:E76-8073-luebeck-control', 'object:mpo-8073', 'liturgical_relationship', luebeck76,
        'researcher_interpretation', 'research/continuation_76/results.json', 'unresolved', 'suggested',
        scope='Similar provisional chant-work order vs catalogue description; no claim of book identity, direct transmission or identical melody',
        locator='Schnabel catalogue, ff. 69va–72ra; AH 5 no.34, second nocturn responsory 3 and verse',
        supports=['evidence:'+i for i in e76['source_regions']],
        comparator_original_inspected=False, exact_adjacency_verified=False, melody_compared=False,
        independent_confirmation=False, new_discovery=False)
    for current in leads.values():
        if current['id'] == 'ant49-audit' or ('object:mpo-8073' in current.get('subjects', []) and current['relationship_type'] == 'same_codex'):
            current['contradicting'].extend([e76['published_comparison'], e76['interpretation'], e76['limits']])
            current['origins'].append({'path':'research/continuation_76/results.json'})
            current['test_execution'] += ' E76 records a catalogued different-book control for the tentative Anne work sequence; no original comparator image or melody was inspected.'

    claim('interpretation:E77-dedication-order-comparison', 'object:mpo-8066', 'liturgical_relationship', 'object:mpo-10437',
        'researcher_interpretation', 'research/continuation_77/results.json', 'unresolved', 'suggested',
        scope='Conditional local antiphon-order difference across existing fragments; not a candidate same-book or different-book decision',
        supports=['evidence:'+i for i in e77['source_regions']],
        same_service_occurrence_verified=False, physical_seam_verified=False, full_office_omission_verified=False,
        melody_compared=False, independent_confirmation=False, new_discovery=False)
    for current in leads.values():
        if current['id'] == 'ant49-audit' or ('object:mpo-8066' in current.get('subjects', []) and 'object:mpo-9620' in current.get('subjects', [])):
            current['contradicting'].extend([e77['conditional_difference'], e77['limits']])
            current['origins'].append({'path':'research/continuation_77/results.json'})
            current['test_execution'] += ' E77 compares existing 8066/10437 dedication contexts as a cross-family control; comparable service and book identity are not established.'

    verse78 = entity('chant:cantus-008036', 'Chant', 'Domus mea — verse and response', cantus_id='008036',
        identification_scope='Published work concept; Fr 10437 local identification remains tentative')
    claim('interpretation:E78-10437-verse', 'object:mpo-10437', 'chant_identification', verse78,
        'researcher_interpretation', 'research/continuation_78/results.json', 'unresolved', 'suggested',
        scope='Selected abbreviated source cue; work ID and markers not independently confirmed',
        supports=['evidence:I78-10437-lapides-verse-mane'],
        full_antiphon_omission_proven=False, comparator_original_inspected=False,
        independent_confirmation=False, new_discovery=False)
    previous77 = next(item for item in claims if item['id'] == 'interpretation:E77-dedication-order-comparison')
    previous77['later_qualification'] = e78['consequence']
    previous77['provenance'].append({'source': source('research/continuation_78/results.json'),
                                     'locator': 'Published Krakow and Utrecht controls; selected Fr 10437 cue'})
    for current in leads.values():
        if current['id'] == 'ant49-audit' or ('object:mpo-8066' in current.get('subjects', []) and 'object:mpo-9620' in current.get('subjects', [])):
            current['contradicting'].extend([e78['published_control'], e78['consequence'], e78['limits']])
            current['origins'].append({'path':'research/continuation_78/results.json'})
            current['test_execution'] += ' E78 identifies a tentative 10437 verse cue and published examples containing both verse and full antiphon; no whole-office omission is established.'

    claim('interpretation:E79-dedication-opening-notes', 'object:mpo-10437', 'melodic_excerpt_comparison', 'object:mpo-8066',
        'researcher_interpretation', 'research/continuation_79/results.json', 'unresolved', 'suggested',
        scope='Post-selection first four candidate Hec est do-mus noteheads; no complete melody, source attribution or robust interval contrast',
        supports=['evidence:'+i for i in e79['source_regions']],
        exact_pitch_transcribed=False, robust_between_source_contrast_established=False,
        independent_confirmation=False, new_discovery=False)
    for current in leads.values():
        if current['id'] == 'ant49-audit' or ('object:mpo-8066' in current.get('subjects', []) and 'object:mpo-9620' in current.get('subjects', [])):
            current['contradicting'].extend([e79['published_controls'], e79['limits']])
            current['origins'].append({'path':'research/continuation_79/results.json'})
            current['test_execution'] += ' E79 examines a tentative 10437/8066 same-antiphon opening as cross-family context, not a direct 8066/9620 conclusion.'

    claim('interpretation:E80-dedication-domini-notes', 'object:mpo-10437', 'melodic_excerpt_comparison', 'object:mpo-8066',
        'researcher_interpretation', 'research/continuation_80/results.json', 'unresolved', 'suggested',
        scope='Two candidate noteheads over do-mi of domini; local direction uncertain for 8066 at wider tolerances; no complete melody or book relationship',
        supports=['evidence:'+i for i in e80['source_regions']],
        equal_interval_proven=False, absolute_pitches_transcribed=False, compound_sign_adjudicated=False,
        independent_confirmation=False, new_discovery=False)
    previous79 = next(item for item in claims if item['id'] == 'interpretation:E79-dedication-opening-notes')
    previous79['later_context'] = e80['interpretation']
    previous79['provenance'].append({'source':source('research/continuation_80/results.json'), 'locator':'Following do-mi syllables; sensitivity and caveats'})
    for current in leads.values():
        if current['id'] == 'ant49-audit' or ('object:mpo-8066' in current.get('subjects', []) and 'object:mpo-9620' in current.get('subjects', [])):
            current['contradicting'].extend([e80['published_controls'], e80['limits']])
            current['origins'].append({'path':'research/continuation_80/results.json'})
            current['test_execution'] += ' E80 adds two tentative 10437/8066 following noteheads as cross-family context; it does not adjudicate 8066/9620.'

    # Group-level harmonization is a source transformation, not an
    # independent date measurement for each fragment in the unit.
    date99 = entity('question:E99-ant49-date-conflict', 'ResearchQuestion',
                    'Ant 49 catalogue dates and BOMPAC harmonization')
    claim('observation:E99-ant49-dating-conflict','object:mpo-8201','describes',date99,
          'project_observation','research/continuation_99/results.json','supported','asserted',
          scope='Eight pinned unit rows: six source 15th-century dates, two source 14th-century dates; all share the harmonized 14th-century value and conflict flag',
          source_row_count=len(e99['rows']),independent_dating=False,attribution_proved=False,
          independent_confirmation=False,new_discovery=False)
    for current in leads.values():
        subjects = set(current.get('subjects', []))
        if current['id'] == 'ant49-audit' or subjects in ({'object:mpo-8201','object:mpo-8304'}, {'object:mpo-8201','object:mpo-20106'}):
            current['contradicting'].append('E99: BOMPAC-4861 preserves six original 15th-century and two 14th-century source dates; all eight rows have a harmonized 1301–1400 value and the dataset\'s Conflict flag. The group value is not an independent date for each object.')
            current['origins'].append({'path':'research/continuation_99/results.json'})

    # The pair triage initially lists only representative images. Add all
    # explicitly recorded derivatives of the same physical object, without
    # implying that different captures or resolutions are different leaves.
    # Preserve prior overlays and their ordering; do not infer associations
    # from filenames, catalogue group labels, or visual similarity.
    object_images = collections.defaultdict(set)
    for record in records + comparisons:
        physical = record.get('physical_object_id', record['id'])
        if record.get('image_path'):
            object_images[physical].add(record['image_path'])
        for capture in record.get('captures', []):
            if capture.get('path') and capture.get('physical_object_id', physical) == physical:
                object_images[physical].add(capture['path'])
    for capture in e65_captures:
        object_images[capture['physical_object_id']].add(capture['path'])
    for current in leads.values():
        for physical, listed in current.get('required_inputs', {}).get('available_primary_images', {}).items():
            listed.extend(sorted(object_images[physical] - set(listed)))

    graph={"version":VERSION,"assessment_date":DATE,"design":"MANUSCRIPT_KNOWLEDGE.md","entities":list(entities.values()),"claims":claims,"evidence":list(evidence.values()),"dependencies":list(dependencies.values()),
           "input_snapshots":[{"path":p,"sha256":digest((root/p).read_bytes())} for p in input_paths],"frozen_inputs":before,
           "semantics":{"open_world":True,"identity_closure":False,"scores_are_confidence":False,"independent_confirmation_claimed":False}}
    register={"version":VERSION,"assessment_date":DATE,"selection":"Complete current stored ranking, hypotheses, dossiers, diagnostic controls, crosslinks, context checks and named feasibility/auxiliary leads; no new model screening.",
              "coverage":{"ranking_rows":len(matches),"ranking_unique_physical_pairs":len({pair_key(canonical[m['left_id']],canonical[m['right_id']]) for m in matches}),"all_pair_leads":len(pair_rows),"hypotheses":len(hypotheses),"dossiers":len(dossiers),"crosslink_rows":sum(map(len,crosslinks.values())),"context_checks":len(contexts),"catalogue_records":len(records),"distinct_physical_object_ids":len(set(canonical[r['id']] for r in records))},
              "alias_reconciliation":{"merged_record_representations":{k:v for k,v in object_records.items() if len(v)>1},"rule":"Use explicit physical_object_id only; reconstructed-unit labels do not merge objects.","unresolved":["Turku Ms. c holder/extent"]},
              "leads":list(leads.values()),"frozen_inputs":before}
    validate_knowledge(root,graph,register)
    write(root/"data/knowledge.v1.json",graph)
    write(root/"data/lead_register.v1.json",register)
    render_register(root,register)
    assert before=={p:digest((root/p).read_bytes()) for p in FROZEN},"Knowledge extraction changed frozen inputs"
    return {**register["coverage"],"leads":len(leads),"entities":len(entities),"claims":len(claims),"regions":len(evidence),"decision_states":dict(collections.Counter(x['decision_state'] for x in leads.values()))}


def validate_knowledge(root, graph=None, register=None):
    graph=graph or read(root,"data/knowledge.v1.json")
    register=register or read(root,"data/lead_register.v1.json")
    entities={x['id']:x for x in graph['entities']}
    evidence={x['id']:x for x in graph['evidence']}
    dependencies={x['id']:x for x in graph['dependencies']}
    for collection in ['entities','claims','evidence','dependencies']:
        ids=[x['id'] for x in graph[collection]]
        if len(ids)!=len(set(ids)):raise ValueError('Duplicate '+collection+' ID')
    if not all(x['type'] in TYPES for x in entities.values()):raise ValueError('Unknown entity type')
    for c in graph['claims']:
        if c['predicate'] not in RELATIONS or c['basis'] not in BASES or c['status'] not in STATES:raise ValueError('Invalid claim vocabulary')
        if c['subject'] not in entities or c['object'] not in entities or c['attributed_to'] not in entities:raise ValueError('Dangling claim entity')
        if not c['scope'] or not c['recorded_at'] or not c['provenance']:raise ValueError('Missing claim provenance')
        if c['source_stance'] not in {'asserted','suggested','rejected','unknown'} or c['polarity'] not in {'positive','negative','unknown'}:raise ValueError('Invalid assertion stance')
        if 'confidence' in c:raise ValueError('Uncalibrated confidence forbidden')
        if c['basis']=='computational_suggestion' and c['predicate']!='suggested_association':raise ValueError('Model proposal promoted to identity')
        for ref in c['supports']+c['challenges']+c.get('contextual_evidence',[]):
            if ref not in evidence:raise ValueError('Dangling evidence')
        for p in c['provenance']:
            if p['source'] not in entities or entities[p['source']]['type']!='Source':raise ValueError('Invalid source reference')
    for e in evidence.values():
        path=root/e['target']['source']
        if e['image'] not in entities:raise ValueError('Evidence image not registered')
        if entities[e['image']].get('path')!=e['target']['source']:raise ValueError('Evidence linked to a different image')
        if digest(path.read_bytes())!=e['sha256']:raise ValueError('Evidence image hash mismatch')
        nums=re.fullmatch(r'xywh=(\d+),(\d+),(\d+),(\d+)',e['target']['selector']['value'])
        if not nums:raise ValueError('Invalid region')
        from PIL import Image
        with Image.open(path) as im:w,h=im.size
        x,y,rw,rh=map(int,nums.groups())
        if rw<=0 or rh<=0 or x+rw>w or y+rh>h:raise ValueError('Region outside image')
    for snap in graph['input_snapshots']:
        if digest((root/snap['path']).read_bytes())!=snap['sha256']:raise ValueError('Stale knowledge input: '+snap['path'])
    for p,h in graph['frozen_inputs'].items():
        if digest((root/p).read_bytes())!=h:raise ValueError('Frozen input changed')
    lead_ids=set()
    covered_rows=set(); covered_h=set(); covered_d=set(); covered_crosslinks=set(); covered_contexts=set(); covered_diagnostic=set()
    for lead in register['leads']:
        if lead['id'] in lead_ids:raise ValueError('Duplicate lead')
        lead_ids.add(lead['id'])
        if lead['decision_state'] not in STATES:raise ValueError('Invalid lead state')
        if lead['relationship_type'] not in RELATIONS:raise ValueError('Invalid lead relation')
        for key in ['exact_claim','already_published','supporting','contradicting','strongest_feasible_test','required_inputs','what_changes_state','origins','test_execution']:
            if key not in lead:raise ValueError('Incomplete lead')
        if any(s not in entities for s in lead['subjects']):raise ValueError('Dangling lead entity')
        if any(d not in dependencies for d in lead['required_inputs'].get('dependencies',[])):raise ValueError('Dangling dependency')
        for origin in lead['origins']:
            if origin['path']=='data/matches.json':covered_rows.add(origin['row'])
            if origin['path']=='data/hypotheses.v1.json':covered_h.add(origin['id'])
            if origin['path']=='data/dossiers.json':covered_d.add(origin['id'])
            if origin['path']=='research/finnish_crosslinks_mpo.json':covered_crosslinks.add((origin['bucket'],origin['record']))
            if origin['path']==read(root,'data/hypothesis_reviews.v1.json')['context_checks_path']:covered_contexts.add(origin['id'])
            if origin['path']=='research/metadata_retrieval_diagnostic.json':covered_diagnostic.add(origin['row'])
    if covered_rows!=set(range(len(read(root,'data/matches.json')))):raise ValueError('Ranking row coverage incomplete')
    if covered_h!={h['id'] for h in read(root,'data/hypotheses.v1.json')['hypotheses']}:raise ValueError('Hypothesis coverage incomplete')
    if covered_d!={d['id'] for d in read(root,'data/dossiers.json')}:raise ValueError('Dossier coverage incomplete')
    expected_crosslinks={(bucket,'mpo-'+row['signatur']) for bucket,rows in read(root,'research/finnish_crosslinks_mpo.json').items() for row in rows}
    if covered_crosslinks!=expected_crosslinks:raise ValueError('Crosslink coverage incomplete')
    context_path=read(root,'data/hypothesis_reviews.v1.json')['context_checks_path']
    if covered_contexts!={c['id'] for c in read(root,context_path)['checks']}:raise ValueError('Context coverage incomplete')
    if covered_diagnostic!=set(range(len(read(root,'research/metadata_retrieval_diagnostic.json')['results']))):raise ValueError('Diagnostic coverage incomplete')
    required_leads={'fr8311-chant','ant49-audit','aboense-control','iv160-control','iv28-control','turku-ms-c','E33-numbering-conflict','iv157-1505','iv157-ant99','iv173-29666','E35-overlap','E36-aboense-I','E36-aboense-II','E36-aboense-III','E37-ending','E37-C435-access','E38-replacement-text','E39-excerpt','E40-boundary'}
    if not required_leads<=lead_ids:raise ValueError('Required topic coverage incomplete')
    return {'valid':True,'entities':len(entities),'claims':len(graph['claims']),'regions':len(evidence),'leads':len(lead_ids),'frozen_inputs_unchanged':True}


def render_register(root, register):
    lines=['# Complete lead register — version 1','',f"Assessment: {DATE}. This overlay preserves all frozen reviews. A metadata triage is not a manuscript test. All existing ranking rows are covered; unresolved local source work is recorded as pending, not as an external blocker.",'','Coverage: '+json.dumps(register['coverage'],ensure_ascii=False),'','| Lead | Claim/type | State | Work actually performed | Next discriminating test |','|---|---|---|---|---|']
    def cell(x):return str(x).replace('|',' / ').replace('\n',' ')
    for lead in register['leads']:
        lines.append('| '+ ' | '.join(cell(x) for x in [lead['id']+' · '+lead['title'],lead['relationship_type'],lead['decision_state'],lead['test_execution'],lead['strongest_feasible_test']])+' |')
    lines += ['','Each machine-readable row in `data/lead_register.v1.json` also retains prior sources, support, counterevidence, required/missing inputs, origins and a state-change criterion. The register does not claim the full underlying manuscript investigation is complete.']
    (root/'LEAD_REGISTER.md').write_text('\n'.join(lines)+'\n')


def export_jsonld(root):
    graph=read(root,'data/knowledge.v1.json')
    validate_knowledge(root,graph)
    base='urn:lost-library:'
    iri=lambda x:base+quote(x,safe='')
    nodes=[]
    for e in graph['entities']:
        nodes.append({'@id':iri(e['id']),'@type':'ll:'+e['type'],'label':e['label'],'details':json.dumps(e,ensure_ascii=False)})
    for c in graph['claims']:
        nodes.append({'@id':iri(c['id']),'@type':'ll:Claim','subject':{'@id':iri(c['subject'])},'relationship':'ll:'+c['predicate'],'object':{'@id':iri(c['object'])},'status':c['status'],'basis':c['basis'],'polarity':c['polarity'],'attributedTo':{'@id':iri(c['attributed_to'])},'details':json.dumps(c,ensure_ascii=False)})
    # Keep the complete evidence/dependency and extraction metadata, not just edges.
    nodes.append({'@id':base+'dataset:v1','@type':'ll:KnowledgeDataset','details':json.dumps({k:v for k,v in graph.items() if k not in {'entities','claims'}},ensure_ascii=False)})
    result={'@context':{'ll':'urn:lost-library:vocab:','label':'http://www.w3.org/2000/01/rdf-schema#label','subject':{'@id':'http://www.w3.org/1999/02/22-rdf-syntax-ns#subject','@type':'@id'},'object':{'@id':'http://www.w3.org/1999/02/22-rdf-syntax-ns#object','@type':'@id'},'relationship':{'@id':'http://www.w3.org/1999/02/22-rdf-syntax-ns#predicate','@type':'@id'},'status':'ll:status','basis':'ll:basis','polarity':'ll:polarity','attributedTo':{'@id':'http://www.w3.org/ns/prov#wasAttributedTo','@type':'@id'},'details':'ll:details'},'@graph':nodes}
    write(root/'data/knowledge.v1.jsonld',result)
    return {'path':'data/knowledge.v1.jsonld','nodes':len(nodes),'claims_reified':True,'identity_closure':False}
