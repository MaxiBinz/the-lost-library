# Research continuation E30: BOMPAC assignments for three Fr 1385 model suggestions

**Date:** 25 October 2026. **Question:** do published target-level reconstruction datasets already place the H08–H10 candidate fragments with Fr 1385?

## Result

The checksum-verified BOMPAC combined workbook places Fr 4223, Fr 8311 and Fr 8455 together in BOMPAC-258, identified there as Ant-39/Codex-1200/FM.IV.159. The same workbook places Fr 1385 in BOMPAC-912 with Ant-99/FM.IV.157. The included units have 39 and 20 rows, respectively. Thus all three H08–H10 suggestions are grouped together by this prior reconstruction dataset, while their Fr 1385 anchor is assigned to another unit.

The raw MPO workbook has a parallel assignment: the candidates belong to unit C-17 (27 rows), while Fr 1385 is a one-record singleton, F-1385. The three candidate records identify the Ant-39/Codex-1200 group and Västerås; Fr 1385's source record describes an *Antiphonarium OP* and separately says it is the same manuscript as Taitto Ant 157. The raw MPO and combined workbook are related BOMPAC datasets, not two independent expert judgments.

The existing local metadata matcher ranked the three candidate pairs at 1–3 for the Fr 1385 anchor, with metadata scores about 0.936–0.943 and embedding scores about 0.903–0.918. These are uncalibrated retrieval scores, not identity probabilities. The crosswalk provides a clear explanation for why high similarity is not a new same-book finding: the published reconstruction data assigns the candidate fragments to another reconstructed unit.

## Interpretation and limits

This strengthens the prior-art and difficult-negative interpretation of H08–H10. It does **not** prove that the physical leaves cannot share a scribe, workshop, liturgical tradition, or a more complicated historical relationship; workbook units are source-backed reconstructions, not fresh image examination. No H08–H10 case changes category C, and no new attribution, exclusion, or method claim is established.

The queue, model, predictors, thresholds, images and source-image inventory are unchanged. No public data was newly downloaded. The source workbooks were rechecked against their published MD5 values: combined workbook `ae9572cd4df5e5bccc241e8423ddf0c1`; raw MPO workbook `6aaea1e3ba1a60355dfb6c649fc7baff`. The query and exact records are reproduced in [the script](research/continuation_30/bompac_suggestion_crosswalk.py) and [machine result](research/continuation_30/bompac_suggestion_crosswalk_results.json), using the published [combined dataset](https://doi.org/10.5281/zenodo.17511106) and [raw MPO dataset](https://doi.org/10.5281/zenodo.17701360), both CC BY 4.0.

## Strategy consequence

Do not spend the next discovery pass promoting H08–H10 from image resemblance. Keep them in the frozen review queue as unresolved model lookalikes, and prioritize source-level evidence for the central IV.157/Codex 1505 questions or other untested cases. Reopen these three only if exact text, physical structure, or diagnostic script/notation evidence can test the published unit separation. This is a narrowing of candidate priorities within the original goal, not a new goal.

## Reproduction

```sh
./.venv/bin/python research/continuation_30/bompac_suggestion_crosswalk.py
./.venv/bin/python research/continuation_30/integrate.py
./.venv/bin/python -m lost_library evidence
./.venv/bin/python -m lost_library export
```

The integration preserves the frozen queue hash `b3e299a7c600584ce44518db1f5c30c3301edae0a07a8b009075498f64ccec47` and retains categories 2 E / 7 C / 1 D.

The query's two source workbook MD5 values passed; evidence and site export, all 35 Python tests, the Node viewer test, the 167-image integrity check and the 173-file resource audit passed. The local review archive includes both workbook inputs and passed checksum verification plus extracted offline replay. These package checks do not independently verify the manuscript reconstruction.
