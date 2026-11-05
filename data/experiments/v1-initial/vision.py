"""Deterministic image descriptors and frozen pretrained visual retrieval.

The descriptors do not transcribe a chant or identify a scribe. ImageNet
ResNet18 features are generic visual similarity, never manuscript identity.
"""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
from typing import Any

import numpy as np
from PIL import Image, ImageOps

VISION_VERSION = "1.0.0"
WEIGHTS_URL = "https://download.pytorch.org/models/resnet18-f37072fd.pth"
WEIGHTS_FILENAME = "resnet18-f37072fd.pth"


def unit(vector: np.ndarray) -> np.ndarray:
    vector = np.asarray(vector, dtype=np.float32)
    norm = float(np.linalg.norm(vector))
    return vector / norm if norm > 1e-10 else np.zeros_like(vector)


def _resample(vector: np.ndarray, length: int) -> np.ndarray:
    result = np.interp(np.linspace(0, len(vector) - 1, length), np.arange(len(vector)), vector)
    return unit(result - result.mean())


def crop_paper(image: Image.Image) -> tuple[Image.Image, dict[str, Any]]:
    """Suppress dark capture borders, using one fixed rule for every source.

    This is a processing crop, not an original-leaf boundary estimate. It
    can retain rulers and lose damaged edges; the raw-image ablation tests
    the dependence of retrieval on this rule.
    """
    image = ImageOps.exif_transpose(image.convert("RGB"))
    width, height = image.size
    margin_x, margin_y = max(1, round(width * .055)), max(1, round(height * .055))
    base = image.crop((margin_x, margin_y, width - margin_x, height - margin_y))
    small = np.asarray(base.resize((160, 160)), dtype=np.float32)
    brightness = small.mean(axis=2)
    paper = (brightness > 85) & (small[:, :, 0] > 60)
    ys, xs = np.where(paper)
    if len(xs) > 160 * 160 * .15:
        # Quantiles suppress isolated ruler labels without fitting to a book.
        x0, x1 = np.quantile(xs, [.015, .985])
        y0, y1 = np.quantile(ys, [.015, .985])
        box = (int(x0 / 160 * base.width), int(y0 / 160 * base.height),
               max(1, int((x1 + 1) / 160 * base.width)),
               max(1, int((y1 + 1) / 160 * base.height)))
        if box[2] - box[0] > base.width * .4 and box[3] - box[1] > base.height * .4:
            base = base.crop(box)
    else:
        box = (0, 0, base.width, base.height)
    return base, {"fixed_border_fraction": .055, "source_size": [width, height],
                  "processing_crop_size": list(base.size), "paper_quantile_box": list(box),
                  "is_original_leaf_measurement": False}


def layout_descriptor(image: Image.Image) -> tuple[np.ndarray, dict[str, Any]]:
    """Projection profiles, gradients and colour fractions, without OCR/OMR."""
    pixels = np.asarray(image.resize((256, 256)), dtype=np.float32) / 255.0
    gray = pixels.mean(axis=2)
    # Relative local darkness is less sensitive to parchment exposure.
    background = np.asarray(Image.fromarray((gray * 255).astype("uint8")).filter(
        __import__("PIL.ImageFilter", fromlist=["GaussianBlur"]).GaussianBlur(9)), dtype=np.float32) / 255
    ink = np.clip(background - gray - .025, 0, 1)
    red = np.clip(pixels[:, :, 0] - np.maximum(pixels[:, :, 1], pixels[:, :, 2]) - .045, 0, 1)
    row, column = ink.mean(axis=1), ink.mean(axis=0)
    red_row, red_column = red.mean(axis=1), red.mean(axis=0)

    gy, gx = np.gradient(gray)
    magnitude = np.hypot(gx, gy)
    orientation = (np.arctan2(gy, gx) + np.pi) % np.pi
    hog = []
    for yy in range(4):
        for xx in range(4):
            sl = (slice(yy * 64, (yy + 1) * 64), slice(xx * 64, (xx + 1) * 64))
            bins = np.floor(orientation[sl] / np.pi * 8).astype(int).clip(0, 7)
            hist = np.bincount(bins.ravel(), weights=magnitude[sl].ravel(), minlength=8)
            hog.extend(unit(hist))
    components = [_resample(row, 64), _resample(column, 64),
                  _resample(red_row, 32), _resample(red_column, 32),
                  unit(np.asarray(hog))]
    vector = unit(np.concatenate(components))

    centered = red_row - red_row.mean()
    autocorrelation = np.correlate(centered, centered, mode="full")[255:]
    if autocorrelation[0] > 1e-8:
        autocorrelation /= autocorrelation[0]
        lag = int(np.argmax(autocorrelation[3:51]) + 3)
        periodicity = float(autocorrelation[lag])
    else:
        lag, periodicity = 0, 0.0
    stats = {"ink_density": float(np.mean(ink > .035)),
             "red_density": float(np.mean(red > .04)),
             "blue_density": float(np.mean((pixels[:, :, 2] - pixels[:, :, 0] > .07) & (pixels[:, :, 2] > pixels[:, :, 1]))),
             "horizontal_red_period_px_at_256": lag or None,
             "horizontal_red_periodicity": periodicity,
             "gradient_energy": float(magnitude.mean()),
             "descriptor_dimension": int(len(vector)),
             "interpretation": "Image-pattern proxies only; not measured physical staff spacing, script identity or music transcription."}
    return vector, stats


def load_encoder(root: Path):
    import torch
    import torchvision
    from torchvision.models import ResNet18_Weights, resnet18

    model_dir = root / "data" / "models"
    model_dir.mkdir(parents=True, exist_ok=True)
    torch.hub.set_dir(str(model_dir))
    torch.set_num_threads(2)
    torch.manual_seed(0)
    torch.use_deterministic_algorithms(True)
    weights = ResNet18_Weights.IMAGENET1K_V1
    model = resnet18(weights=weights, progress=True)
    model.fc = torch.nn.Identity()
    model.eval()
    checkpoint = model_dir / "checkpoints" / WEIGHTS_FILENAME
    metadata = {"architecture": "torchvision.resnet18", "weights": "IMAGENET1K_V1",
                "weights_url": WEIGHTS_URL, "weights_path": str(checkpoint.relative_to(root)),
                "weights_sha256": hashlib.sha256(checkpoint.read_bytes()).hexdigest(),
                "weights_bytes": checkpoint.stat().st_size,
                "torch_version": torch.__version__, "torchvision_version": torchvision.__version__,
                "device": "cpu", "training": False, "embedding_dimension": 512,
                "preprocessing": "Official weights.transforms(): resize256, center224, ImageNet normalization; once raw and once fixed paper crop.",
                "model_scope": "Frozen ImageNet generic-image encoder; no handwriting/notation identity validation and no training here.",
                "source": "https://docs.pytorch.org/vision/stable/models/generated/torchvision.models.resnet18.html"}
    return model, weights.transforms(), metadata


def extract_features(root: str | Path, use_ai: bool = True, force: bool = False) -> dict[str, Any]:
    root = Path(root).resolve()
    records = json.loads((root / "data" / "fragments.json").read_text())
    selected = [r for r in records if r.get("image_path") and (root / r["image_path"]).is_file()]
    if not selected:
        raise ValueError("No actual local fragment images are available")
    if len(selected) > 300:
        raise ValueError("Working sample exceeds the authorized 300-image bound")
    fingerprint = hashlib.sha256(json.dumps([(r["id"], hashlib.sha256((root / r["image_path"]).read_bytes()).hexdigest()) for r in selected], sort_keys=True).encode()).hexdigest()
    output_path = root / "data" / "features.json"
    arrays_path = root / "data" / "features.npz"
    if not force and output_path.exists() and arrays_path.exists():
        existing = json.loads(output_path.read_text())
        if existing.get("image_fingerprint") == fingerprint and existing.get("vision_version") == VISION_VERSION and bool(existing.get("encoder")) == bool(use_ai):
            return existing

    encoder, transform, encoder_info = (None, None, None)
    if use_ai:
        encoder, transform, encoder_info = load_encoder(root)
    ids, layouts, embeddings, raw_embeddings, items, failed = [], [], [], [], {}, []
    for index, record in enumerate(selected):
        try:
            with Image.open(root / record["image_path"]) as source:
                raw = ImageOps.exif_transpose(source).convert("RGB")
                crop, crop_info = crop_paper(raw)
                layout, stats = layout_descriptor(crop)
                if encoder is not None:
                    import torch
                    with torch.inference_mode():
                        batch = torch.stack([transform(crop), transform(raw)])
                        encoded = encoder(batch).cpu().numpy()
                    embedding, raw_embedding = unit(encoded[0]), unit(encoded[1])
                else:
                    embedding = raw_embedding = np.zeros(512, dtype=np.float32)
                ids.append(record["id"])
                layouts.append(layout)
                embeddings.append(embedding)
                raw_embeddings.append(raw_embedding)
                items[record["id"]] = {"image_sha256": hashlib.sha256((root / record["image_path"]).read_bytes()).hexdigest(),
                                        "crop": crop_info, "layout": stats}
                print(f"features {index + 1}/{len(selected)} {record['id']}", flush=True)
        except Exception as error:
            failed.append({"id": record["id"], "error": str(error)})
    if not ids:
        raise ValueError("Every image failed decoding/feature extraction")
    np.savez_compressed(arrays_path, ids=np.asarray(ids), layout=np.stack(layouts),
                        embedding=np.stack(embeddings), raw_embedding=np.stack(raw_embeddings))
    summary = {"vision_version": VISION_VERSION, "image_fingerprint": fingerprint,
               "images_requested": len(selected), "images_processed": len(ids), "failed": failed,
               "encoder": encoder_info, "arrays_path": "data/features.npz", "items": items,
               "forbidden_inputs": ["codex", "CCM", "shelfmark", "filename semantics", "institution", "relationship notes", "account provenance"],
               "limitations": ["Processing crop is not an original-leaf boundary.",
                               "Layout/gradient features do not identify letterforms, abbreviations or a scribe.",
                               "Red periodicity is a pixel-pattern proxy, not physical staff-line spacing.",
                               "The encoder can retain imaging/provider shortcuts; raw/cropped ablations are evaluated."]}
    output_path.write_text(json.dumps(summary, indent=2) + "\n")
    return summary


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--no-ai", action="store_true")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    extract_features(args.root, use_ai=not args.no_ai, force=args.force)
