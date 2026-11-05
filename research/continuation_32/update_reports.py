"""Update current narrative documents after E32 evidence integration."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    if old in text:
        path.write_text(text.replace(old, new, 1), encoding="utf-8")
    elif new not in text:
        raise ValueError(f"Expected text absent from {path.relative_to(ROOT)}: {old[:100]}")


def insert_after_line(path: Path, prefix: str, new_line: str) -> None:
    text = path.read_text(encoding="utf-8")
    if new_line in text:
        return
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if line.startswith(prefix):
            lines.insert(i + 1, new_line)
            path.write_text("\n".join(lines) + "\n", encoding="utf-8")
            return
    raise ValueError(f"Line prefix absent from {path.relative_to(ROOT)}: {prefix}")


def append_section(path: Path, heading: str, content: str) -> None:
    text = path.read_text(encoding="utf-8")
    if heading not in text:
        path.write_text(text.rstrip() + "\n\n" + content.strip() + "\n", encoding="utf-8")


def main() -> None:
    state = ROOT / "PROJECT_STATE.md"
    replace_once(state, "E19–E31 are recorded", "E19–E32 are recorded")
    replace_once(state, "most recently [E31](RESEARCH_CONTINUATION_31.md)", "most recently [E32](RESEARCH_CONTINUATION_32.md)")
    insert_after_line(
        state,
        "- E31 checked the detailed official Fragmenta entries.",
        "- E32 directly inspected Fr 8994's first retained image and recorded a red four-stroke mark consistent with the catalogue's `IIII` foliation. The indexed IV.156 description says the opening-signature convention was not infrequent, so its format alone is not a unique fingerprint. H03 stays C; the exact Olavi sequence still needs paired source images and full prior-art review. The new region and limits are in [E32](RESEARCH_CONTINUATION_32.md)."
    )
    replace_once(state, "The current export contains 62 validated region annotations and twelve separate context checks", "The current export contains 63 validated region annotations and thirteen separate context checks")
    replace_once(state, "The current evidence export has 62 validated regions and twelve context checks", "The current evidence export has 63 validated regions and thirteen context checks")
    replace_once(state, "CTX12 the detailed catalogue wording and signature lead.", "CTX12 the detailed catalogue wording and signature lead, and CTX13 the image-linked four-stroke mark and common-signature caveat.")
    replace_once(state, "The H03 metadata calculation and E26/E27/E30/E31 source checks remain separate from image-region observations.", "H03's catalogue calculation and the E26/E27/E30/E31 prior-art checks remain distinct from image observations; E32 adds one image-linked Fr 8994 region.")
    replace_once(state, "See [E31 report](RESEARCH_CONTINUATION_31.md)", "See [E32 report](RESEARCH_CONTINUATION_32.md)")
    replace_once(state, "E31 refreshed the local review archive", "E32 refreshed the local review archive")
    replace_once(state, "E20–E31 add further source tests", "E20–E32 add further source tests")
    replace_once(state, "The next narrow test is the possible `k`/IV opening-signature correspondence among Fr 8994, Fr 20278 and F.m.IV.157, followed by text and chant-boundary comparison if official images are available.", "The next narrow test is still the paired `k`/IV and Olavi text comparison among Fr 8994, Fr 20278 and F.m.IV.157. E32 shows that the signature format itself was not infrequent, so it must be evaluated with text boundaries and sequence if official images are available.")

    readme = ROOT / "README.md"
    replace_once(readme, "[RESEARCH_CONTINUATION_30.md](RESEARCH_CONTINUATION_30.md)", "[RESEARCH_CONTINUATION_32.md](RESEARCH_CONTINUATION_32.md)")
    replace_once(readme, "observations.v8.json`, `review_bundle.json`: local screening, 62 source-linked pixel annotations", "observations.v9.json`, `review_bundle.json`: local screening, 63 source-linked pixel annotations")
    replace_once(readme, "`data/context_checks.v10.json`: twelve supporting family/source checks", "`data/context_checks.v11.json`: thirteen supporting family/source checks")
    replace_once(readme, "CTX12 the detailed catalogue wording and foliation test lead.", "CTX12 the detailed catalogue wording and foliation lead, and CTX13 the source-linked Fr 8994 mark plus the common-signature caveat.")
    replace_once(readme, "`research/continuation_31/`: official Fragmenta catalogue relationship labels and an unverified `k`/IV opening-signature lead for H03; no image or queue change.", "`research/continuation_31/` and `research/continuation_32/`: official Fragmenta relationship labels, an unverified `k`/IV lead, one region-linked Fr 8994 mark, and access outcomes; no queue change.")
    replace_once(readme, "./.venv/bin/python research/continuation_31/integrate.py", "./.venv/bin/python research/continuation_32/integrate.py")
    replace_once(readme, "CTX12 records the official Fragmenta relationship labels and the possible foliation test lead. It adds no source image, region annotation or frozen hypothesis; H03 remains C.", "CTX12 records official relationship labels and the foliation lead. CTX13 links the visible Fr 8994 mark to its pixels and records that the signature convention is common; H03 remains C.")

    final = ROOT / "FINAL_REPORT.md"
    replace_once(final, "The current export contains 62 validated regions, twelve context checks", "The current export contains 63 validated regions, thirteen context checks")
    replace_once(final, "The evidence export reports 62 regions and twelve context checks", "The evidence export reports 63 regions and thirteen context checks")
    replace_once(final, "E21/E22/E24/E26/E27/E28/E29/E30/E31 are supporting source checks", "E21/E22/E24/E26/E27/E28/E29/E30/E31/E32 are supporting source checks")
    replace_once(final, "E27/E28/E29/E30/E31 added no image or download", "E27/E28/E29/E30/E31/E32 added no image or download; E32 adds one annotation on an existing image")
    append_section(
        final,
        "E32 directly inspected Fr 8994",
        "E32 directly inspected a source-linked Fr 8994 image region and observed a four-stroke red mark consistent with the catalogue's `IIII` foliation note. The official indexed IV.156 description says the opening-signature convention was not infrequent in late-medieval codices and early printed books, so the format alone has limited specificity. This sharpened and weakened the H03 clue at the same time: an exact Olavi text and sequence comparison is still needed. The paired IV.157/Fr 20278 images and the full Taitto/Keskiaho texts remain unavailable in this pass. H03 remains C; no new attribution, physical join, or novelty claim is made."
    )

    questions = ROOT / "OPEN_QUESTIONS.md"
    replace_once(questions, "[E31](RESEARCH_CONTINUATION_31.md) checked", "[E32](RESEARCH_CONTINUATION_32.md) extends")
    replace_once(questions, "Fr 8994's recorded `IIII`/`k` foliation may align with IV.157's St Olaf folio-8 signature notation, but this is not image-checked. This is a promising narrow test, not a new attribution.", "A local Fr 8994 image shows four red strokes consistent with `IIII`; the official IV.156 description says the opening-signature convention was not infrequent. This is a narrower but less distinctive test, not a new attribution.")

    reviewer = ROOT / "REVIEWER_PACKET.md"
    replace_once(reviewer, "The signatures have not been compared on both source images.", "E32 now links a four-stroke Fr 8994 mark to exact pixels, but the paired IV.157 image is still missing. The official IV.156 catalogue says this signature convention was not infrequent, so the format alone is not diagnostic.")
    replace_once(reviewer, "The full ten-comparison queue is in", "E32 adds one image-linked Fr 8994 mark; the signature convention itself is not unique. The full ten-comparison queue is in")
    replace_once(reviewer, "The current export includes 62 source regions and twelve supporting checks", "The current export includes 63 source regions and thirteen supporting checks")
    replace_once(reviewer, "see [E28](RESEARCH_CONTINUATION_28.md), [E29](RESEARCH_CONTINUATION_29.md) and [E31](RESEARCH_CONTINUATION_31.md).", "see [E28](RESEARCH_CONTINUATION_28.md), [E29](RESEARCH_CONTINUATION_29.md), [E31](RESEARCH_CONTINUATION_31.md) and [E32](RESEARCH_CONTINUATION_32.md).")

    target = ROOT / "TARGET_MANUSCRIPT.md"
    append_section(
        target,
        "E32 source check",
        "E32 inspects a four-stroke red mark in Fr 8994's first retained capture, consistent with the catalogue's `IIII` note. The official IV.156 description says the opening-signature convention was not infrequent, so it is not a unique identifier by itself. No paired IV.157/Fr 20278 image comparison or exact Olavi text collation is complete; H03 remains C and novelty remains uncleared. See [E32](RESEARCH_CONTINUATION_32.md)."
    )

    ledger = ROOT / "research/PRIOR_ART_LEDGER.md"
    append_section(
        ledger,
        "E32 source-visible signature and convention context",
        "E32 directly inspects the four-stroke red mark in the first local Fr 8994 capture. It is consistent with the MPO catalogue's `IIII` foliation transcription, but the capture does not independently establish side orientation. The official indexed IV.156 description explains that this red-letter/Roman-numeral opening-signature convention was not infrequent and cites Antiphoners 34, 157, 170 and 173. The format is therefore not unique prior evidence for Codex 1505. Exact text/sequence comparison and full Taitto/Keskiaho reading remain pending. See [E32](../RESEARCH_CONTINUATION_32.md) and [the region annotation](../data/observations.v9.json)."
    )

    experiment = ROOT / "EXPERIMENT_LOG.md"
    append_section(
        experiment,
        "## E32 — source-linked Fr 8994 signature check (25 October)",
        "The first retained Fr 8994 capture contains a red upper-margin mark with four visible strokes, consistent with the catalogue's `IIII` foliation note. The observation is linked to a 38 × 20 pixel region and checked against the source hash. The official indexed F.m.IV.156 description says the paired opening-signature format was not infrequent in late-medieval codices and early printed books, so the format alone cannot identify a codex. Taitto 2001 pp.161–168 remains unread: the previous NLF page-viewer request returned Cache miss, while a normal Finna browser visit displayed Cloudflare verification; no challenge was interacted with or bypassed. Helsinki portal metadata confirms separate 2008 and 2019 Keskiaho works; neither full text was obtained. H03 remains C; no source image was downloaded, and the queue, model, predictors and thresholds are unchanged. See [E32](RESEARCH_CONTINUATION_32.md), [structured source result](research/continuation_32/results.json), and [region annotation](research/continuation_32/fr8994_signature_observation.json). Evidence export: 10 cases, 63 regions, 13 context checks, 2 E / 7 C / 1 D; zero new findings."
    )

    goal_audit = ROOT / "GOAL_AUDIT.md"
    replace_once(goal_audit, "E19](INDEPENDENT_RESEARCH_PASS.md) through [E31](RESEARCH_CONTINUATION_31.md)", "E19](INDEPENDENT_RESEARCH_PASS.md) through [E32](RESEARCH_CONTINUATION_32.md)")
    replace_once(goal_audit, "[62 versioned regions](data/observations.v8.json), reviews v1.13, [twelve context checks](data/context_checks.v10.json)", "[63 versioned regions](data/observations.v9.json), reviews v1.14, [thirteen context checks](data/context_checks.v11.json)")
    replace_once(goal_audit, "CTX12 preserves the detailed official catalogue labels and foliation lead. E31 updates H03's test lead", "CTX12 preserves the detailed official catalogue labels and foliation lead; CTX13 adds a source-linked Fr 8994 mark and records that the signature convention was not infrequent. E32 updates H03's test lead")
    replace_once(goal_audit, "62 validated regions, reviews, twelve context checks", "63 validated regions, reviews, thirteen context checks")
    replace_once(goal_audit, "E30/E31 update prior-art and source-test context", "E30/E31/E32 update prior-art and source-test context")
    replace_once(goal_audit, "E19–E31 progress added", "E19–E32 progress added")
    replace_once(goal_audit, "E31 refreshed the 551-file archive", "E32 refreshed the local review archive")

    print("Updated current state, final report, open questions, README, reviewer packet, target, prior-art ledger, experiment log and goal audit for E32.")


if __name__ == "__main__":
    main()
