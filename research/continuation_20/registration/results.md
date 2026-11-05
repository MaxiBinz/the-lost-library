# Fixed-band capture-registration baseline

23 October 2026. No source acquisition, image restoration, predictor change or attribution decision. Project-environment OpenCV, scikit-image and SciPy were unavailable; NumPy and Pillow supplied a deliberately limited baseline. Any subsequent isolated feature-registration test must retain this result rather than replace it with a tuned positive.

The exact ROIs, source hashes, source endpoints and protocol are in [protocol.json](protocol.json) and [results.json](results.json). The 1/2 bands were copied from the existing complementary-initial annotations. The 3/4 test pairs the existing image-4 top ROI with a fixed image-3 bottom band of the same writing-area width. The different-surface 2/3 control uses the exact verse-prefix/suffix regions from the intrinsic text-order test.

The signal was binary dark ink with maximum RGB channel below125, excluding red ruling and pale parchment. Rulers and external image borders fall outside the declared ROIs. Translation was limited to ±50 horizontal pixels, with at least80% of the shorter band height and90% of its width overlapping. No rotation, scale, affine or perspective search occurred. These settings were written before execution and were not adjusted after the results.

| Pair | Role | Translations tested | Best dark-ink Pearson correlation | Result |
|---|---|---:|---:|---|
| 1/2 | Proposed same-surface partial views | 6,868 | 0.0682 | No strong correlation |
| 3/4 | Proposed same-surface partial views | 8,080 | 0.0567 | No strong correlation |
| 2/3 | Different-surface text-boundary control | 6,565 | 0.1361 | No strong correlation; higher than either candidate pair |

All FFT correlations at the selected maximum were checked against direct pixel calculations. The different-surface control is a useful warning against interpreting a low local correlation maximum as overlap. None passed the predeclared0.8 correlation screen, which would itself only trigger a visual check rather than prove same surface.

There are **zero accepted distinctive feature correspondences**, no inlier distribution, no affine/homography model and no geometric residual. The saved paired ROI sheets show tested pixels separately; they are not stitched images or matched-point overlays. No positive geometric overlap claim is made.

**Actual outcome: unresolved.** These limited translation tests supply no pixel evidence that 1/2 or3/4 overlap. They also cannot prove different surfaces: the views may be disjoint, perspective/scale may differ, lighting may change, or the chosen bands may contain too little shared matter. The independently observed text continuation between2and3 remains a separate kind of evidence. It does not turn a failure of pixel matching into proof that1/2 or3/4 are co-surface.

Run `.venv/bin/python research/continuation_20/registration/check_bands.py` from the project root. This uses only existing source files and does not modify the frozen queue or benchmark.
