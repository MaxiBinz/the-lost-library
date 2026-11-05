# Dependencies and third-party components

## Current assessment — E54,31October2026

E54 uses the existing Python/Pillow/JSON stack to inspect exact institutional JPEGs and record source bounds. No new software, model, paid service or cloud dependency was added. Native-source variants are photographs of existing objects; the source-crop proof is not generated manuscript detail. See [E54](RESEARCH_CONTINUATION_54.md). Older dated sections below describe historical snapshots.

Tested environment: Python3.12.14, macOS arm64; exact package versions in `requirements.txt` and `data/environment.json`. The viewer uses browser-native HTML/CSS/JavaScript, with no external fonts, analytics or runtime CDN.

| Component | Use | Upstream |
|---|---|---|
| NumPy2.3.5 | descriptors, similarities, evaluation | https://numpy.org/ |
| Pillow12.3.0 | image decoding and layout analysis | https://python-pillow.org/ |
| PyTorch2.9.0 / torchvision0.24.0 | frozen CPU image encoder | https://pytorch.org/ |
| pypdfium2 4.30.0 / PDFium | local PDF decoding/inspection | https://pypdfium2.readthedocs.io/ |
| openpyxl 3.1.5 | read-only inspection of published BOMPAC workbooks | https://openpyxl.readthedocs.io/ |
| SQLite / Python standard library | local database, fetching, command line | https://www.sqlite.org/ and https://www.python.org/ |
| Node built-in test/assert modules | viewer verification only | https://nodejs.org/ |

ResNet18 uses torchvision IMAGENET1K_V1 official weights. Architecture, transform, weight URL/hash, byte size and versions are in `data/features.json`. No model was trained or fine-tuned. ImageNet pretraining is not evidence of manuscript suitability or of rights over the project's source images. Model weights are excluded from the review archive; obtain them from the documented official upstream route if recomputing features.

Preserve upstream notices when redistributing dependencies; this project does not bundle a Python environment or relicense those components. Specialized HTR/OMR services were considered but not installed or used for authoritative transcription. No paid service, external image upload or cloud model training was used in the experiments.

E50 adds six source-image files from Riksarkivet for two existing physical objects, with the same recorded PDM1.0 Rights-metadata scope preserved. The E50 capture ledger contains exact attribution/source locators; the layout figure uses only those source pixels. No new provider, private publication image or library code dependency is introduced.
