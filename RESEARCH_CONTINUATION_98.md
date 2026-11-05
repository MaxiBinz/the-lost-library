# E98: opposite-face check and review-package refresh

**3 November 2026.** The previous E97 pass recorded faint marks after the last clearly read words on Fr 8994. This pass compared the retained lower views of captures 2 and 4 after mirroring capture 4 horizontally for visual inspection. Both were already known and the selection was post-exposure. The source images were not changed.

## Result

The photographs show different writing and different folds or obstructions. This inspection did **not** find sufficient distinctive, reliably paired physical landmarks to register the two photographed surfaces at the faint mark. Thus it does not show whether the mark is ink from the other face, and the failure to establish a correspondence is not proof that it is not show-through. No independent reader, authenticated surface map, Finnish image, reading, physical join or historical attribution was obtained. The original [E97 annotation](research/continuation_97/observations.json), candidate reading and alternatives remain unchanged.

A bounded search for exact shelfmark/folio phrases did not locate a labelled reproduction of the relevant Finnish f.8 or f.9 surfaces. This is not proof no reproduction exists; do not retry previously failed access routes. A peer-reviewed radiocarbon article illustrates another fragment, VII.67, rather than the desired Finnish leaves. Its sample references are already documented in [E88](RESEARCH_CONTINUATION_88.md).

## Local review package

The previously verified archive was from 2 November and could not contain the latest research or the E97 graph. The local packaging script now writes a staging archive and replaces the previous archive only after checksum, extracted source and replay checks pass. It also verifies the E85, E96 and E97 source checks in the extracted package. These checks assess provenance, coordinates and arithmetic, **not** manuscript readings or historical identity. No external publication or communication is authorized or performed.

Use `.venv/bin/python research/package_research.py` to build and verify the review archive. Its result and timestamp are in `output/research/package_verification.json`; check that receipt rather than treating an older verification as current. No new manuscript file, upload or paid service was used. The goal remains active.
