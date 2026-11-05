"""Expose saved correspondences as raw-pixel context, without refitting anything."""
import hashlib
import json
from pathlib import Path
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
WIDTH = 96


def crop_box(point, size):
    x = max(0, min(int(round(point[0])) - WIDTH//2, size[0] - WIDTH))
    y = max(0, min(int(round(point[1])) - WIDTH//2, size[1] - WIDTH))
    return [x, y, WIDTH, WIDTH]


def main():
    path = ROOT / 'research/continuation_35/feature_results.json'
    source = json.loads(path.read_text())
    selections = {}
    rows = {row['id']: row for row in source['results']}
    for ident in ['8994-1-2', '8994-3-4']:
        selections[ident] = list(range(len(rows[ident]['all_mutual_correspondences'])))
    count = len(rows['20274-overlap-positive']['all_mutual_correspondences'])
    selections['20274-overlap-positive'] = [round(i*(count-1)/5) for i in range(6)]
    selections['8994-1-3-nonrepeat'] = [i for i, row in enumerate(rows['8994-1-3-nonrepeat']['all_mutual_correspondences']) if row['ransac_inlier']]
    manifest = {'version': '1.0.0', 'date': '2026-10-28',
        'input': str(path.relative_to(ROOT)), 'input_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
        'method': 'Raw 96px source windows, clamped within the original image; no rotation, warp, rescaling or registration. Circles only locate stored keypoints.',
        'selections': {}, 'independent_review': False}
    for ident, indices in selections.items():
        row = rows[ident]
        originals = []
        for descriptor in row['sources']:
            actual = ROOT / descriptor['path']
            assert hashlib.sha256(actual.read_bytes()).hexdigest() == descriptor['sha256']
            originals.append(Image.open(actual).convert('RGB'))
        canvas = Image.new('RGB', (1390, ((len(indices)+4)//5)*170+45), 'white')
        draw = ImageDraw.Draw(canvas)
        draw.text((10, 6), ident+' / saved source pixels; no new fit; E35 gate unchanged', fill='black')
        items = []
        for ordinal, index in enumerate(indices):
            correspondence = row['all_mutual_correspondences'][index]
            px = (ordinal%5)*278+8;py = (ordinal//5)*170+40
            draw.text((px, py), f"point {index}; RANSAC inlier={correspondence['ransac_inlier']}", fill='black')
            item = {'index': index, 'ransac_inlier': correspondence['ransac_inlier'], 'sources': []}
            for side, (key, original) in enumerate(zip(['left_source_xy', 'right_source_xy'], originals)):
                point = correspondence[key];box = crop_box(point, original.size)
                x, y, w, h = box
                crop = original.crop((x, y, x+w, y+h))
                marker = ImageDraw.Draw(crop);cx, cy = point[0]-x, point[1]-y
                marker.ellipse((cx-4, cy-4, cx+4, cy+4), outline='#cc2440', width=1)
                canvas.paste(crop, (px+side*132, py+25))
                draw.text((px+side*132, py+126), f"{point[0]:.1f},{point[1]:.1f}", fill='black')
                descriptor = row['sources'][side]
                item['sources'].append({'path': descriptor['path'], 'sha256': descriptor['sha256'],
                    'point_xy': point, 'crop_xywh': box, 'image_dimensions': list(original.size)})
            items.append(item)
        filename = ident+'-raw-patches.png';canvas.save(HERE / filename)
        manifest['selections'][ident] = {'indices': indices, 'items': items,
            'review_figure': 'research/continuation_41/'+filename, 'original_screen_passed': row['screen_passed']}
    (HERE / 'review_manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
    print(json.dumps({key: len(value['indices']) for key, value in manifest['selections'].items()}))


if __name__ == '__main__':
    main()
