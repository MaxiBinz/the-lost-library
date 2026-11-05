"""Integrate the E32 source-linked Fr 8994 mark without changing the queue."""
from __future__ import annotations

import copy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RESULT = Path(__file__).resolve().parent / "results.json"
OBSERVATION = Path(__file__).resolve().parent / "fr8994_signature_observation.json"
QUEUE_SHA256 = "b3e299a7c600584ce44518db1f5c30c3301edae0a07a8b009075498f64ccec47"


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def append_unique(items: list, value):
    if value not in items:
        items.append(value)


def main():
    result = read(RESULT)
    observation = read(OBSERVATION)
    if result["queue_sha256"] != QUEUE_SHA256:
        raise ValueError("E32 result refers to a different frozen queue")

    observations_path = ROOT / "data/observations.v9.json"
    observations = read(ROOT / "data/observations.v8.json")
    observations["version"] = "9.0.0"
    observations["assessment_date"] = "2026-10-25"
    observations["inputs"] = list(observations["inputs"])
    append_unique(observations["inputs"], "research/continuation_32/fr8994_signature_observation.json")
    annotations = observations["annotations"]
    annotations[:] = [x for x in annotations if x.get("id") != observation["id"]]
    annotations.append(observation)
    write(observations_path, observations)

    context_path = ROOT / "data/context_checks.v11.json"
    context = copy.deepcopy(read(ROOT / "data/context_checks.v10.json"))
    context["version"] = "1.6.0"
    context["assessment_date"] = "2026-10-25"
    checks = context["checks"]
    checks[:] = [x for x in checks if x.get("id") != "CTX13"]
    checks.append({
        "id": "CTX13",
        "title": "Fr 8994 opening-signature image check and convention specificity",
        "record_ids": ["mpo-8994"],
        "observation_ids": [observation["id"]],
        "summary": (
            "E32 directly inspected a region of the local first Fr 8994 capture and observed four red vertical strokes, "
            "consistent with the MPO catalogue's IIII foliation transcription. The official indexed F.m.IV.156 catalogue "
            "description explains the red-letter/Roman-numeral opening-signature system and says it was not infrequent "
            "in late-medieval codices and early printed books, citing Antiphoners 34, 157, 170 and 173. Thus the format "
            "alone is not a unique identity signal."
        ),
        "outcome": (
            "The visible mark improves traceability of the local IIII observation, while the catalogue context reduces the "
            "specificity of the signature format. Fr 8994's Olavi contents and the IV.157 folio-8 description still merit a "
            "text-and-sequence comparison, but H03 remains C and no new join is established."
        ),
        "limits": [
            "The retained image is a 600 x 415 JPEG; the manual reading has not been checked by a second reader or specialist.",
            "The capture is not independently assigned to medieval recto or verso; the paired k mark was not securely read from pixels in this observation.",
            "The IV.156 wording was available through official-page search indexing; its direct page was not opened in this pass.",
            "No local F.m.IV.157 or Fr 20278 scan is available for paired foliation, chant-boundary, or text comparison.",
            "Taitto 2001 pp. 161-168 and both relevant Keskiaho works remain unread in full; originality is uncleared.",
            "The frozen queue, predictor inputs, thresholds, source-image inventory, and case classifications are unchanged."
        ],
        "sources": [
            "RESEARCH_CONTINUATION_32.md",
            "research/continuation_32/results.json",
            "research/continuation_32/fr8994_signature_observation.json",
            "https://fragmenta.kansalliskirjasto.fi/handle/10024/1299",
            "https://fragmenta.kansalliskirjasto.fi/handle/10024/1300",
            "https://www.finna.fi/Record/fikka.3965551?lng=en-gb"
        ]
    })
    write(context_path, context)

    reviews_path = ROOT / "data/hypothesis_reviews.v1.json"
    review_doc = read(reviews_path)
    if review_doc.get("queue_sha256") != QUEUE_SHA256:
        raise ValueError("Review file does not preserve the frozen queue")
    if review_doc.get("observations_path") != "data/observations.v8.json":
        raise ValueError("Unexpected observations source; review integration needs inspection")
    by_id = {x["id"]: x for x in review_doc["reviews"]}
    h03 = by_id["H03"]
    h03["observation_ids"] = list(h03["observation_ids"])
    append_unique(h03["observation_ids"], observation["id"])
    append_unique(h03["supporting"], (
        "E32 inspected the local first Fr 8994 capture: a source-linked red four-stroke upper-margin mark is consistent "
        "with the catalogue's IIII transcription. This checks one visible mark only; side orientation and the paired k are not independently established."
    ))
    append_unique(h03["against"], (
        "The official F.m.IV.156 catalogue says the opening-signature convention was not infrequent in late-medieval codices "
        "and early printed books. The format alone therefore has limited specificity and is not a unique Codex 1505 fingerprint."
    ))
    h03["prior_status"] += (
        " E32 directly observed the four-stroke red mark on one local Fr 8994 capture, consistent with the catalogue's IIII note. "
        "The official indexed IV.156 description says the broader opening-signature convention was not infrequent, so the format "
        "alone cannot identify a codex."
    )
    h03["outcome"] = (
        "Still C / unresolved. One local Fr 8994 capture shows a four-stroke red mark consistent with IIII, but the image does not "
        "independently establish side mapping, the paired k, or a match with IV.157. The signature format is described as not uncommon; "
        "only paired textual and sequence evidence could make this a specific attribution test. No new attribution is established."
    )
    h03["next_evidence_needed"] = (
        "Obtain and compare usable official images of F.m.IV.157 fol. 8 and Fr 20278, if legitimately available; resolve side mapping; "
        "compare the full k/IIII opening-signature sequence and exact Olavi text/chant boundaries. Read Taitto 2001 pp. 161-168 and "
        "Keskiaho 2008 and 2019 discussions through legitimate access. Keep C if these sources remain unavailable or nondiagnostic."
    )
    review_doc["observations_path"] = "data/observations.v9.json"
    review_doc["context_checks_path"] = "data/context_checks.v11.json"
    review_doc["version"] = "1.14.0"
    review_doc["assessment_date"] = "2026-10-25"
    for ident in ("H03",):
        for source in [
            "RESEARCH_CONTINUATION_32.md",
            "research/continuation_32/results.json",
            "research/continuation_32/fr8994_signature_observation.json",
            "https://fragmenta.kansalliskirjasto.fi/handle/10024/1299",
            "https://fragmenta.kansalliskirjasto.fi/handle/10024/1300"
        ]:
            append_unique(by_id[ident]["sources"], source)
    write(reviews_path, review_doc)
    print(json.dumps({
        "observations": len(annotations),
        "context_checks": len(checks),
        "classification_H03": h03["classification"],
        "queue_sha256": review_doc["queue_sha256"],
        "observations_path": review_doc["observations_path"],
        "context_checks_path": review_doc["context_checks_path"]
    }, indent=2))


if __name__ == "__main__":
    main()
