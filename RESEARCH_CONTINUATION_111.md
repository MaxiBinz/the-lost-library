# E111 — apparent column counts where the original field is blank

**4 November 2026.** This extends the probable BOMPAC data-quality issue in [E108](RESEARCH_CONTINUATION_108.md); it is not a medieval manuscript attribution.

The [predeclared check](research/continuation_111/protocol.json) matched the pinned combined and raw workbooks by exact fragment number and reference, requiring an included row on both sides and a unique raw ID. All **22,553** included Swedish MPO rows met those conditions. Of those, **6,872** have a blank original `spaltenzahl` cell. For **6,543** of these 6,872, the combined `Columns` cell contains numeric 1 or 2: 2,323 and 4,220 records respectively. The other 329 blank-source cases have a blank, another number or other content in that combined field. These are fragment records, not reconstructed books.

For all 6,543 cases, the separately retained MPO CSV also has a unique matching ID and a blank column-count field. The CSV and raw BOMPAC workbook are related representations of the same catalogue data, not independent physical evidence. As reported in E108, the combined Swedish numeric `Columns` values equal `No_of_leaves` throughout the tested rows; this new check demonstrates that the problem also affects cases where the original layout field is missing. A blank field does **not** prove that the historical layout is unknowable, that no other source exists, or that every combined value is incorrect. The compilers' intent, any additional source, current release and first notice remain unverified.

This matters when a researcher treats nonblank `Columns` as observed layout data: a completeness filter can select thousands of records without an original MPO column count in these retained sources. In the matched population, the 6,543 blank-source cases are disjoint from E108's 5,598 raw-versus-combined 1/2 disagreements; together they total 12,141 records, **53.8% of 22,553**. This is a count of specified data discrepancies and missing-source cases, **not** an estimate of individually verified errors, historical layouts, affected scholarly publications, or all versions of the dataset.

The checksum-pinned [results](research/continuation_111/results.json) retain the complete category matrix and exact cell references, including Fr 52 (raw `EI54` blank, combined `AS54` = 2, combined leaf count `H54` = 2). To reproduce:

```sh
.venv/bin/python research/continuation_111/check_missingness.py
```

The calculation is exploratory and has no independent reviewer. It does not update published data, alter the frozen model or imply that all original catalogue entries are correct. No source images were acquired and no external contact or publication occurred.
