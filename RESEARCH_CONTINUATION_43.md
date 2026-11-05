# E43: full-register source-credit and coverage audit

29 October 2026, Europe/Vienna. E42 was progress: its declared row/boundary tests, source locators, uncertainty and archive replay were completed. E43 returns to the full research population instead of repeating photograph-compatibility checks. It finds and repairs an internal source-credit defect. **This is not a new codex, a correction to scholarship, or a discovery.**

## Population and source test

The [protocol](research/continuation_43/protocol.json) preserves the pre-change register and its hashes. All **168 overlapping lead/question entries, 117 physical-pair leads, 170 directional ranking rows and ten frozen cases** are accounted for in [coverage_audit.json](research/continuation_43/coverage_audit.json). Topic entries and pairs are not independent manuscripts. This is a post hoc audit: the missing Beauvais credit was noticed before the protocol was saved.

The controlling source is the retained [F-4ihz virtual-reconstruction manifest](research/evidence/F-4ihz_manifest.json), identified as *Virtual Reconstruction* and *Beauvais Missal*. For each of the twelve local Beauvais records, we traced its exact working-image service into a canvas of that manifest. We normalized the default HTTPS port only; object paths remain case-sensitive. No similar-title or shared-use shortcut supplied membership. Each match retains the parent canvas ID, JSON locator, image URL/hash and individual source record in [memberships.json](research/continuation_43/memberships.json). This checks the pinned source, not the current live reconstruction or its historical conclusions independently.

**All twelve local control images have explicit source membership. Forty-three of their pair leads had been labelled merely as unestablished metadata suggestions without the reconstruction credit.** The import path handled MPO `codex`/`ccmsignum` fields, while these Fragmentarium records represented membership through another source structure. That omission could waste discovery effort and misstate prior art. It did not change the frozen matcher or its metrics.

## Repair and limits

Those43 lead entries now say **previously documented**, explicitly scoped to the published reconstruction. Twelve source-assertion claims connect the members to the source-defined Beauvais codex concept. The original computational suggestions remain separate, unresolved computational claims; their scores have not become source validation or confidence. No automatic identity closure occurs, and no new pair-level image transcription or physical examination is reported.

The pre-change93 metadata-only pairs break down as follows:

| Audit outcome | Pair leads | Meaning |
|---|---:|---|
| Explicit Beauvais reconstruction membership, now credited | 43 | Published controls; no new physical attribution |
| Still metadata/availability triage only | 50 | Both objects have retained local images; primary pair work is not complete |

Of the remaining50, five share the MPO Codex1505 label, thirteen share Codex1104 and fourteen share Codex1146. These32 shared labels were already recorded as catalogue assertions. We did not automatically promote them. In particular, Codex1146/Ant49 includes the published8201–8304 different-book control, so shared catalogue grouping cannot by itself validate physical identity. The remaining eighteen have other or differing assignments, which likewise do not automatically prove different books.

## Frozen queue and named questions

The frozen review remains **2E / 7C / 1D, zero A/B**, byte-identical. Its cases were all revisited against their current records:

| Case | Current evidence and limit | Remaining discriminating work |
|---|---|---|
| H01,1385/20274 | Previously documented control; actual text/structure comparisons do not supply a unique variant | Source-specific hand/ruling assessment; retain known-control status |
| H02,1385/10406 | Ornament/ruling compatibility also occurs across controls | Diagnostic hand/notation and securely mapped structure; no promotion from broad similarity |
| H03,20274/8994 | E33–E42 sharpen marks, words and local order; complete surface/address remains unresolved | Designated Finnish originals, Fr20278, actual numbering and unread prior art |
| H04,IV173/1385 | Known broad group and separated reconstruction units; different chant ranges | Local structural/script comparison can still be developed; exact scholarship remains claim-specific |
| H05,IV173/25592 | Alias resolved; strong visible layout/date discrepancy remains historically ambiguous | Distinguish composite/section/catalogue alternatives; accepted29666 comparator still lacks an image |
| H06,8201/8304 | Published rejection retained despite high machine compatibility | Preserve as hard negative; no new rejection claimed |
| H07,8201/20106 | Published positive; second image missing | Exact legitimate20106 original, not an invented endpoint |
| H08–H10,1385/4223/8311/8455 | Model lookalikes assigned to another published unit; shared decoration/chant not decisive | A source discriminator is needed to reopen physical identity; no blanket negative from workbook labels |

The full machine record retains the other named leads as well. Fr10370's relative text order is distinct from an unproved medieval-side map. The IV156/IV157 address conflict still has reset/composite/source-description alternatives. IV173's broader grouping remains distinct from its specific29666 relation. Fr8311's common chant identification is not identity evidence. Duba's reciprocal-ratio correction remains a separately reproduced methods observation with first notice uncleared. The C23/Fr20274 subcase has partial text/music compatibility and identified prior art; it supplies no new codex. No context check is relabelled independent expert review.

## Completion decision and next test

**The goal is not complete and no global blocker is established.** An indexed source or missing chapter cannot become novelty clearance, and a fully populated register cannot stand in for executed manuscript tests. Fifty retained pairs still have metadata-only work, and concrete local comparisons remain possible. This audit does not justify an exhausted-investigation negative conclusion.

The next selected test is the existing Ant49 pair **Fr8066/Fr9620**, both concerning Dedication in the catalogue, with9620 described as hymns. Inspect the actual visible sequences and their positions: do they duplicate a corresponding opening, or occupy different sections/genres? Test any conflict against book-function, abbreviation and composite alternatives. Keep the published8201–8304 rejection and8201–20106 positive separate. This is a specific existing audit lead, not another target family; source inspection is **pending**, not reported as performed by E43.

Reproduce the source/coverage audit and check with:

```sh
.venv/bin/python research/continuation_43/audit_register.py
.venv/bin/python -m lost_library knowledge build
.venv/bin/python research/continuation_43/check_sources.py
```

The preserved baseline makes the before/after counts reproducible. The checker verifies exact source-service membership, all lead/pair identifiers, repaired source credit, remaining triage counts and unchanged frozen/core inputs. It does not verify historical identity, an independent image reading, originality or the full goal's completion.

Knowledge version1.7.0 has **168 entries,117 pair leads,870 entities,594 claims and98 regions**. Its overlapping topic-state totals are90 unresolved,69 previously documented,3 contradicted,5 supported and1 not testable. These are not counts of independent scientific findings. No manuscript image, source catalogue, model, threshold or frozen review changed. The179-file inventory and1,666,761,179-byte conservative transfer plan remain unchanged; no download, contact, upload or publication occurred.
