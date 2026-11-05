"""Fixed-band dark-ink translation check; no acquisition or feature fitting.

OpenCV, scikit-image and SciPy are unavailable in the project environment.
This deliberately limited NumPy check is not a substitute for affine/SIFT
registration. Rulers/background are outside the fixed writing-area ROIs.
"""
import hashlib
import importlib.util
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
PAIRS = [
    {'id': 'capture1_2', 'role': 'candidate partial views of one surface',
     'left': (1, [234, 1290, 1179, 127]), 'right': (2, [232, 25, 1163, 100]),
     'roi_origin': 'Both ROIs copied from existing V-10370-overlap-upper/lower annotations.'},
    {'id': 'capture3_4', 'role': 'candidate partial views of one surface',
     'left': (3, [300, 1040, 1180, 193]), 'right': (4, [300, 0, 1180, 190]),
     'roi_origin': 'Right ROI is existing V-10370-no-seam-34 annotation; left is the native bottom193px band at the same writing-area x range, fixed before correlation.'},
    {'id': 'capture2_3_control', 'role': 'different-surface text-boundary control',
     'left': (2, [650, 490, 740, 115]), 'right': (3, [345, 330, 1155, 85]),
     'roi_origin': 'Exact existing I20-10370 verse-prefix/suffix text ROIs, not shared pixels by the source presentation.'},
]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dump(name, obj):
    (OUT / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')


def integral(a):
    return np.pad(a.cumsum(0).cumsum(1), ((1, 0), (1, 0)))


def rectangle(summed, x0, y0, x1, y1):
    return float(summed[y1, x1] - summed[y0, x1] - summed[y1, x0] + summed[y0, x0])


def pearson_at(a, b, dx, dy):
    x0, y0 = max(0, dx), max(0, dy)
    x1, y1 = min(a.shape[1], dx + b.shape[1]), min(a.shape[0], dy + b.shape[0])
    aa = a[y0:y1, x0:x1].reshape(-1)
    bb = b[y0-dy:y1-dy, x0-dx:x1-dx].reshape(-1)
    if len(aa) == 0 or aa.std() == 0 or bb.std() == 0:
        return None
    return float(np.corrcoef(aa, bb)[0, 1])


def compare(a, b):
    ha, wa = a.shape
    hb, wb = b.shape
    shape = (ha + hb - 1, wa + wb - 1)
    convolution = np.fft.irfftn(np.fft.rfftn(a, shape, axes=(0, 1)) *
                               np.fft.rfftn(b[::-1, ::-1], shape, axes=(0, 1)),
                               shape, axes=(0, 1))
    ia, ib = integral(a), integral(b)
    matches = []
    # Fixed +/-50px horizontal translation, no scale or rotation search.
    # At least80% of the shorter band's height and90% of width must overlap.
    for dy in range(-hb + 1, ha):
        y0, y1 = max(0, dy), min(ha, dy + hb)
        if y1 - y0 < .8 * min(ha, hb):
            continue
        for dx in range(-50, 51):
            x0, x1 = max(0, dx), min(wa, dx + wb)
            if x1 - x0 < .9 * min(wa, wb):
                continue
            n = (x1-x0) * (y1-y0)
            sa = rectangle(ia, x0, y0, x1, y1)
            sb = rectangle(ib, x0-dx, y0-dy, x1-dx, y1-dy)
            denom = ((sa-sa*sa/n) * (sb-sb*sb/n)) ** .5
            if denom <= 0:
                continue
            cross = float(convolution[dy+hb-1, dx+wb-1])
            rho = (cross - sa*sb/n) / denom
            matches.append({'dx': dx, 'dy': dy, 'pearson_dark_ink': rho,
                            'overlap_pixels': n, 'left_ink_pixels': sa, 'right_ink_pixels': sb,
                            'roi_overlap': [x0, y0, x1-x0, y1-y0]})
    matches.sort(key=lambda r: -r['pearson_dark_ink'])
    best = matches[0]
    direct = pearson_at(a, b, best['dx'], best['dy'])
    assert abs(direct - best['pearson_dark_ink']) < 1e-10
    other = next((r for r in matches if abs(r['dx']-best['dx']) > 8 or abs(r['dy']-best['dy']) > 8), None)
    return {'tested_translations': len(matches), 'best': best, 'separate_peak': other,
            'peak_gap': best['pearson_dark_ink'] - other['pearson_dark_ink'] if other else None,
            'direct_calculation_matches_fft': True,
            'strong_correlation_screen': best['pearson_dark_ink'] >= .8,
            'accepted_feature_correspondences': [],
            'inlier_distribution': 'Not available: this method does not detect independent features or fit an affine model.',
            'geometric_residual': None}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    deps = {n: importlib.util.find_spec(n) is not None for n in ['cv2', 'skimage', 'scipy', 'numpy', 'PIL']}
    protocol = {
        'version': '1.0.0', 'assessment_date': '2026-10-23', 'dependencies': deps,
        'fixed_before_execution': True,
        'pairs': PAIRS,
        'signal': 'Binary dark ink where max(R,G,B)<125. Red ruling and pale parchment do not count as ink.',
        'transforms': 'Translation only; dx=-50..50px; no fitted scale, rotation, affine or perspective search.',
        'overlap_gate': 'At least80% of shorter band height and90% of shorter band width.',
        'candidate_screen': 'Pearson correlation>=0.8 would trigger visual review, not automatically prove same surface.',
        'positive_evidence_requirement': 'A positive overlap claim additionally needs distributed distinctive non-ruler/non-staff photographic correspondences, residuals and visual point overlay. This limited correlation does not supply those.',
        'no_tuning_or_retry': 'ROIs, threshold and transforms are not adjusted after seeing outcomes.',
    }
    dump('protocol.json', protocol)
    records = json.loads((ROOT/'data/fragments.json').read_text())
    record = next(r for r in records if r['id'] == 'mpo-10370')
    sources = {c['capture_index']+1:c for c in record['captures'] if c.get('resolution_variant')}
    results = []
    for spec in PAIRS:
        masks, crops, provenance = [], [], []
        for side in ('left', 'right'):
            index, box = spec[side]
            c = sources[index]
            p = ROOT / c['path']
            assert sha(p) == c['sha256']
            with Image.open(p) as im:
                x,y,w,h = box
                assert x>=0 and y>=0 and x+w<=im.width and y+h<=im.height
                crop = im.crop((x,y,x+w,y+h)).convert('RGB')
                pixels = np.asarray(crop)
            mask = (pixels.max(2) < 125).astype(np.float64)
            masks.append(mask)
            crops.append(crop)
            provenance.append({'side': side, 'capture_index_one_based': index,
                'path': c['path'], 'sha256': c['sha256'], 'roi_xywh': box,
                'source_url': c['url']})
        result = compare(*masks)
        # Side-by-side ROIs show what was tested; they are not stitched imagery.
        canvas = Image.new('RGB', (max(c.width for c in crops), sum(c.height+28 for c in crops)), 'white')
        draw = ImageDraw.Draw(canvas)
        y = 0
        for side, crop in zip(('left', 'right'), crops):
            draw.text((3,y+4), f'{spec["id"]}: {side} fixed source ROI; not a stitch', fill='black')
            canvas.paste(crop, (0,y+28))
            y += crop.height+28
        canvas.save(OUT/f'{spec["id"]}-tested-rois.png')
        results.append({'id': spec['id'], 'role': spec['role'], 'sources': provenance,
                        **result, 'outcome': 'Unresolved: no accepted distinctive feature correspondences or affine registration.'})
    dump('results.json', {'assessment_date': '2026-10-23', 'method': protocol, 'results': results,
        'conclusion': 'This translation-only check does not establish a shared photographed surface for1/2 or3/4. Failure to match cannot demonstrate different faces.',
        'source_downloads': 0, 'source_mutations': 0, 'new_discovery': False})
    print(json.dumps([{k:r[k] for k in ('id','tested_translations','best','peak_gap','strong_correlation_screen','outcome')} for r in results], indent=2))


if __name__ == '__main__':
    main()
