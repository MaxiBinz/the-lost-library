"""Record E31's official Fragmenta relationship labels without changing the frozen queue."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RESULT = Path(__file__).resolve().parent / "fragmenta_relationship_results.json"
CONTEXT = ROOT / "data/context_checks.v10.json"
REVIEWS = ROOT / "data/hypothesis_reviews.v1.json"
QUEUE_SHA256 = "b3e299a7c600584ce44518db1f5c30c3301edae0a07a8b009075498f64ccec47"
REPORT = "RESEARCH_CONTINUATION_31.md"
RESULT_PATH = "research/continuation_31/fragmenta_relationship_results.json"
SOURCES = [
    "https://fragmenta.kansalliskirjasto.fi/handle/10024/1299",
    "https://fragmenta.kansalliskirjasto.fi/handle/10024/1300",
    "https://fragmenta.kansalliskirjasto.fi/handle/10024/1314",
]


def append_unique(items: list[str], value: str) -> None:
    if value not in items:
        items.append(value)


def main() -> None:
    result = json.loads(RESULT.read_text(encoding="utf-8"))
    if result["queue_sha256"] != QUEUE_SHA256:
        raise ValueError("E31 result refers to another frozen queue")

    context_doc = json.loads(CONTEXT.read_text(encoding="utf-8"))
    checks = context_doc["checks"]
    checks[:] = [item for item in checks if item.get("id") != "CTX12"]
    checks.append({
        "id": "CTX12",
        "title": "Official Fragmenta relationship labels and a foliation test lead",
        "record_ids": ["mpo-8994", "mpo-20278", "finn-iv173"],
        "observation_ids": [],
        "summary": (
            "E31 records the National Library of Finland's detailed official catalogue wording. F.m.IV.157 labels Ant 99 "
            "and Fr 1385 as from the same codex, while Codex 1505 is suggested; F.m.IV.156 describes strong stylistic "
            "resemblance to IV.157 and also lists Codex 1505 as suggested. F.m.IV.173 describes a broader group of at "
            "least 18 stylistically uniform Åbo-use sources, identifies Ant 242/Fr 29666 as same codex, and lists Hy 49 "
            "and Ant 99 as suggestions. The IV.157 catalogue's St Olaf folio-8 signature notation '[k] iiijr - k [v]' "
            "may align with Fr 8994's catalogue foliation '1r IIII; 1v k'; that possible alignment has not been checked "
            "against both source images."
        ),
        "outcome": (
            "The catalogue distinguishes specific same-codex claims from suggested links and broad stylistic/production "
            "groups. These distinctions clarify prior art but establish no new attribution. The possible k/IV signature "
            "alignment is a narrow source-image test lead; H03 remains unresolved."
        ),
        "limits": [
            "The direct IV.156 and IV.157 pages returned HTTP 403 in this route; their detailed wording was available from official-page search indexing. The IV.173 page opened directly.",
            "Taitto 2001 pp. 161-168 and the relevant Keskiaho 2019 chapter have not been read in full.",
            "No local Fr 20278 or F.m.IV.157 image was available for an exact Olavi text, notation, or foliation comparison.",
            "The k/IV correspondence is a hypothesis to check; it establishes no physical join, shared hand, or same-codex identity.",
            "The frozen queue, predictors, thresholds, and manuscript image inventory are unchanged."
        ],
        "sources": [REPORT, RESULT_PATH, *SOURCES],
    })
    context_doc["version"] = "1.5.0"
    context_doc["assessment_date"] = "2026-10-25"
    CONTEXT.write_text(json.dumps(context_doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    review_doc = json.loads(REVIEWS.read_text(encoding="utf-8"))
    if review_doc.get("queue_sha256") != QUEUE_SHA256:
        raise ValueError("Review file does not preserve the frozen queue")
    by_id = {item["id"]: item for item in review_doc["reviews"]}
    h03 = by_id["H03"]
    note = (
        " E31 checked the official Fragmenta catalogue wording: IV.157 identifies Ant 99/Fr 1385 as same codex, "
        "while Codex 1505 is suggested; the broader IV.173 group likewise distinguishes same-codex from suggested links. "
        "Fr 8994's recorded IIII/k foliation may align with IV.157's St Olaf folio-8 k/IV signature, but that is an "
        "untested lead, not a join."
    )
    if "E31 checked the official Fragmenta catalogue wording" not in h03["prior_status"]:
        h03["prior_status"] += note
    append_unique(h03["supporting"], (
        "The official F.m.IV.157 entry places the St Olaf office at fol. 8 and records opening-signature notation '[k] iiijr - k [v]'; "
        "Fr 8994's catalogue foliation is '1r IIII; 1v k'. This is a possible correspondence to test against images, not an established link."
    ))
    append_unique(h03["against"], (
        "The official Fragmenta entry calls Codex 1505 a suggested relation to IV.157, not a demonstrated same-codex member; "
        "the possible k/IV signature alignment has not been checked against F.m.IV.157 and Fr 20278 images."
    ))
    h03["outcome"] = (
        "Still C / unresolved. The official catalogue's relationship labels distinguish the confirmed Ant 99/IV.157 same-codex "
        "relation from Codex 1505's suggested relation. A possible k/IV signature correspondence is a promising exact test lead, "
        "but without both source images it does not establish a join or new attribution."
    )
    h03["next_evidence_needed"] = (
        "If the official source provides usable images, compare the complete opening-signature sequence and Olavi chant boundaries "
        "on F.m.IV.157 fols. 8-10, Fr 20278, and Fr 8994; first resolve side orientation and the catalogue's signature notation. "
        "If an exact source comparison cannot be made, retain the C classification and do not promote the foliation resemblance."
    )
    for ident in ("H03", "H04", "H05"):
        review = by_id[ident]
        append_unique(review["sources"], REPORT)
        append_unique(review["sources"], RESULT_PATH)
        for source in SOURCES:
            append_unique(review["sources"], source)
    review_doc["version"] = "1.13.0"
    review_doc["assessment_date"] = "2026-10-25"
    REVIEWS.write_text(json.dumps(review_doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "context_checks": len(checks),
        "updated_context": "CTX12",
        "updated_reviews": ["H03", "H04", "H05"],
        "classifications": {key: by_id[key]["classification"] for key in ("H03", "H04", "H05")},
        "queue_sha256": review_doc["queue_sha256"],
    }, indent=2))


if __name__ == "__main__":
    main()
