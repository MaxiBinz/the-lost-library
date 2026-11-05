# E61: testing a non-adjacent explanation for Fr 10370

1 November 2026. The preceding E60 turn produced a conditional opening-text comparison and completed package verification. This follow-up tests an alternative, without assuming that Fr 10370 and IV.156 belonged to the same book.

## The Swedish passage

In Fr 10370's fourth retained photograph, the final surviving written area provisionally fits the responsory **Gloriosa diei**, Cantus 006779. The visible text includes the beginning of the chant and, lower down, words consistent with *celos meruit a…*. The end is partly erased; the unwritten-looking portion must not be treated as proof of what was originally absent. The candidate identification is supported by [indexed Cantus text](https://cantusindex.org/feast/14072200?cid=&field_full_text_value=&genre=All&order=title&page=8&sort=desc&string=), but our image reading is incomplete, unblinded and reference-assisted. It needs independent checking. The [source region](research/continuation_61/observations.json) records the original Swedish image and coordinates.

## A different witness tests the ordering assumption

The [search-indexed inventory of Barcelona Ms. 2322, f. 097v](https://musicahispanica.eu/source/20244?antibot_key=&page=9&sort_by=title&sort_order=ASC) lists *Gloriosa* and its verse, then a versicle and a first lauds antiphon, followed by **Haec corde compuncta** as a second lauds antiphon. Its direct page open returned a cache miss, so this is an indexed listing, not a visual inspection of the reference manuscript. It supplies a concrete example in which the two works occur in that order **with intervening material**.

The previously indexed IV.156 f.8 description begins within *Haec corde compuncta*. If our Swedish identification, the Finnish description and the presumed ordering are all correct, a broad progression from earlier Matins material toward later lauds is plausible. The Barcelona sequence does **not** show what intervening material, if any, existed in either of the target fragments. Shared liturgical order occurs in different books and does not establish their identity, immediate adjacency, a physical join or a unique textual variant.

This also does not remove E60's specific concern. If the two reported *k II* addresses really designate the **same unique page**, the differing opening texts remain a conditional conflict. A proposal that Fr 10370 instead stood on an earlier page must explain the apparent address through side mapping, a different mark, repeated numbering, a source error or another mechanism. The Finnish original is needed to evaluate those premises.

## State and next test

This work adds one source-linked Swedish observation and an explicit non-adjacent alternative; it does not resolve the historical relationship or claim a discovery. The [post-exposure protocol](research/continuation_61/protocol.json), [results](research/continuation_61/results.json) and [source/access notes](research/continuation_61/sources.json) retain the assumptions and limitations. No original f.8 image was inspected and no independent reviewer participated. The earlier institutional access restriction and the new failed reference-page open were not retried or bypassed.

The useful next test is the original IV.156 f.8 opening and signature alongside a reliable map of the Swedish surfaces and numbering. The Fr 8994/f.9 question remains a separate test. No new source image was downloaded; the 208-file image inventory and 1,675,860,841-byte conservative transfer plan are unchanged, with web-reader traffic unmeasured. Frozen metrics and historical decision states are unchanged; no outreach or publication occurred.

```sh
.venv/bin/python research/continuation_61/check_sources.py
.venv/bin/python -m lost_library knowledge validate
```

These checks validate source hashes, region bounds and recorded state, not the manuscript reading or historical attribution.
