# I Asked AI to Reassemble a Medieval Book That Was Torn Apart 500 Years Ago

*Draft investigation,25October2026. No new manuscript attribution is confirmed. Sources and results are linked below; no expert conversations have been invented.*

The first convincing answer was wrong.

Two medieval music fragments had the sort of similarities that make a computer comparison look persuasive: related handwriting descriptions, notation, dimensions and layout. The simple matching system put them together. The image methods also accepted them at their chosen thresholds.

But a scholar had already explained why they came from different books.

That failure became the most useful object in our small investigation. It showed how far a machine could travel toward a confident-looking answer while missing the evidence that actually distinguished the books. It also changed the project from a search for attractive matches into a test of what a match would have to prove.

## A book survives as something else

The fragments preserve an unusual kind of survival. Medieval parchment books were dismantled, and their leaves became durable wrappers for administrative accounts. A book could disappear as a book while some of its pages remained useful enough to keep.

Today, photographs and catalogue descriptions let us compare material held in different collections. That makes an AI-assisted search conceivable. It does not make the underlying scholarship new. Researchers have been reconnecting Nordic fragments for generations, and CODICUM now explicitly pursues cross-collection reconstruction. An independent project has to establish what it adds, not merely make existing connections easier to display.

Our provisional target was a closely related group of late-medieval antiphonals around Helsinki F.m.IV.157. The records already name accepted and suggested associations with Swedish fragments. They also leave room for different explanations: perhaps leaves belong to one book; perhaps different books share a scribe, workshop or liturgical tradition; perhaps accumulated catalogue notes conceal an alias or a resolved scholarly disagreement.

We kept those alternatives separate. Calling the whole neighbourhood one lost book would have made a tidier story and a worse investigation.

## Looking is easier than identifying

The local system acquired images, preserved original descriptions and rights statements, normalized a limited set of attributes, and built a searchable database. It extracted layout descriptors and frozen visual embeddings from an existing general-image model. There was no large training run, paid cloud service or claim that the model had learned medieval palaeography.

The resulting collection has120imaged physical objects and167source image files, including six higher-resolution derivatives of existing photographs. That distinction matters. Some pieces are photographed in sections; two captures can show overlapping parts of the same surface. A photograph is not automatically a leaf, a side, or another independent example.

One target fragment, Fr20274, made that problem particularly visible. Its two source photographs overlap in their writing areas. Simply placing photograph one before photograph two as recto and verso would manufacture evidence of a sequence. The viewer now warns against that shortcut and shows the actual inspected regions.

## The impressive number and the difficult question

We tested nine retrieval methods using separate catalogue-defined books for development, calibration and evaluation. Within the selected same-genre test gallery, the simple metadata baseline performed strongly: precision at five was0.95 and mean reciprocal rank was1.0. The more complicated image methods did not improve the selected baseline.

Those numbers answer a narrow question about ranking objects under provisional reference labels. They do not tell us the probability that an unknown pair belongs to the same medieval manuscript.

The threshold test made that difference plain. Against different-book catalogue labels, the selected threshold falsely accepted40of72same-genre negative pairs. It also accepted the published wrong-book example. Meanwhile, a documented same-book target association ranked26and was rejected. The method could perform well inside its small reference gallery and fail a relationship relevant to the actual investigation.

We kept the failures in the results. Removing them would have improved the presentation while hiding the reason the project needed further evidence.

## A song is not a fingerprint

The next step was to read smaller, more informative pieces of the images. On Fr8311, a provisional reading identifies a responsory beginning with a scene in paradise and a following verse. Cantus references provide candidate identities006537and006537a. The identification agrees with the catalogue's liturgical occasion.

It does not connect that leaf to our target. The same chant appears in other books. A recognizable song helps locate a passage; a common passage cannot serve as a unique fingerprint for a codex.

We also obtained a scholarly text-and-music edition relevant to the office named in another target description. Two short candidate antiphon openings agree with its sequence. Higher-resolution invitatory readings exposed another necessary distinction: the editor's corrected text and the manuscript states reported in the apparatus. A comparison with the edited text could hide differences from the reported manuscript. We now record apparent wording, phrase order and a written transition without a visible hymn entry separately. These provisional observations do not supply a unique book fingerprint, its missing melody or evidence about what singers performed.

The project's image notes therefore separate what is visible, the candidate reading, the normalized search text and the proposed database identity. Every observation points to a bounded region of a specific source photograph. Each remains marked as an AI observation awaiting qualified review.

## Why the wrong answer matters

The published StCatherine comparison distinguishes textual continuity from a repeated office opening. That is a different kind of evidence from overall resemblance. It can explain why pages attributed to a similar hand need not come from the same book.

We re-read that passage and its table. Using the scholar's decision to reject the pair is a replication of existing reasoning, not proof that our model has independently learned the distinction. Nor is duplicated text a universal automatic rule: composite books and repeated offices require contextual judgment.

The more useful role for AI here is to organize an argument that can be challenged. A reviewer should be able to see the proposed connection, the exact image region, the source claim, the objection and the alternative explanation. The interface now supports that chain of inspection.

## Ten comparisons, seven unresolved

To prevent a succession of cherry-picked successes, we froze ten comparisons. The set included documented positives, a published rejection, existing suggestions and three unexplained model suggestions. The published BOMPAC reconstruction files place those three suggestions in one Codex 1200 unit, while assigning their Fr 1385 anchor to a different Ant 99/IV.157 unit. That makes the high-scoring suggestions known reconstruction-level lookalikes, not three independent discoveries. The workbook assignments are prior research, not fresh image proof, and they do not rule out shared production or a more complex history.

After local source and image screening, two cases remain documented positives, one retains its published rejection, and seven remain ambiguous. We found no basis to promote an unknown connection to a confirmed attribution. A full-deposit crosswalk resolves Hy49 as Fr25592. Its conspicuous layout conflict with a suggested comparator remains historically unresolved; a unique identifier does not decide whether the proposed association is correct.

The updated Fragmenta record identifies Ant242/Fr29666 as the same codex as IV.173 and lists Hy49/Fr25592 and Ant99 as suggestions within a broader stylistic/liturgical group. The 2025 BOMPAC workbook assigns IV.173, Fr29666 and Fr25592 to one reconstruction unit, while placing Ant99/IV.157 in another. Walta's peer-reviewed 2013 chapter had already discussed a wider Naantali-related group that includes IV.156, IV.157 and IV.173, and cautions that its members show several hands and may not have been produced at Naantali. These sources may describe different relationship levels; they do not establish a contradiction or a new attribution. The full Walta chapter, the exact Taitto pages cited by Fr8994, and Keskiaho's 2010 pp.418–419 remain to be read, and Fr29666 has no verified local image.

A later chapter directly concerning the target group remains unread. It may resolve what looks uncertain in an online catalogue, limiting originality claims for these associations. The amended research goal continues professional source tests ourselves. We compared decorated initials and approximate ruler-normalized ruling: the ruling did not show a gross incompatibility, while ornamental traits were shared across controls. The older catalogue already places another Swedish leaf between specified Helsinki leaves; we credited that placement. Its margin marks are visible, but side conventions remain unresolved. Matching catalogue opening addresses with different feast labels also remains conditional until the corresponding text and numbering are verified.

Reading a published reconstruction guide produced a separate technical observation. Duba's image-scaling prose and displayed equation use reciprocal ratios. Three analytic controls support the prose operation for preserving physical size. We documented this as an implementation correction and possible typographical erratum, without a first-notice or historical-discovery claim.

## What we can put back together

The viewer includes a partial reconstruction demonstration from the already studied Graduale Aboense. Catalogue-supported local continuities are shown separately, with earlier scholarship credited. Unknown positions remain unknown; placeholders do not pretend to know how many leaves are missing.

There is no generated medieval performance. The photographs contain music, but we have not independently checked a note-level transcription. Adding an attractive soundtrack would create an impression of recovery beyond the evidence.

The result is a functioning research tool and an unfinished historical investigation. The latest export records 62 inspectable image regions and eleven supporting source checks separate from the frozen attribution queue. E30 checked the three Fr 1385 model suggestions against published BOMPAC reconstruction units; it weakened their novelty as same-book claims but did not establish a physical exclusion. Further progress calls for corresponding Helsinki text and signature images, stronger side mapping and wider variant comparison. Missing scholarship constrains novelty claims, and outside scrutiny would be needed before claiming independent confirmation. A review packet is prepared; no one has been contacted.

The book has not been newly recovered. What we have recovered is a clearer account of what the evidence would have to do before we could say so.

## Sources and reproducible evidence

[Research report](FINAL_REPORT.md), [independent pass](INDEPENDENT_RESEARCH_PASS.md), [validation](VALIDATION_REPORT.md), [all ten dossiers](EVIDENCE_DOSSIERS.md), [source ledger](research/PRIOR_ART_LEDGER.md), [reviewer questions](REVIEWER_PACKET.md), [E30 crosswalk](RESEARCH_CONTINUATION_30.md), [MPO deposit](https://zenodo.org/records/17287665), [CODICUM objectives](https://www.codicum.eu/about), [Grajewski's study](https://doi.org/10.25167/ls.4818), [Hallqvist's edition](https://lup.lub.lu.se/student-papers/record/9032430), [Duba's method](https://www.fragmentology.ms/article/view/4499), [Cantus reference](https://cantusdatabase.org/chant/150324/).
