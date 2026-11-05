"""Check saved audit coverage and provenance, not visual judgment or novelty."""
import collections
import hashlib
import json
from pathlib import Path
from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def read(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    protocol = read(HERE / 'protocol.json')
    manifest = read(HERE / 'review_manifest.json')
    review = read(HERE / 'manual_review.json')
    result = read(HERE / 'results.json')
    assert sha(ROOT / manifest['input']) == manifest['input_sha256']
    features = {r['id']: r for r in read(ROOT / manifest['input'])['results']}
    total = 0
    for ident, selection in manifest['selections'].items():
        source = features[ident]
        correspondences = source['all_mutual_correspondences']
        if ident in ['8994-1-2', '8994-3-4']:
            expected = list(range(len(correspondences)))
            assert len(expected) == 25
        elif ident == '20274-overlap-positive':
            expected = [round(i*(len(correspondences)-1)/5) for i in range(6)]
        else:
            expected = [i for i, r in enumerate(correspondences) if r['ransac_inlier']]
        assert selection['indices'] == expected == [r['index'] for r in selection['items']]
        observations = review['comparisons'][ident]
        assert [r['index'] for r in observations] == expected
        for item, observation in zip(selection['items'], observations):
            original = correspondences[item['index']]
            assert item['ransac_inlier'] == original['ransac_inlier'] == observation['ransac_inlier']
            assert observation['outcome'] in protocol['manual_outcomes'] and observation['observation']
            for side, key in enumerate(['left_source_xy', 'right_source_xy']):
                descriptor = item['sources'][side]
                assert descriptor['point_xy'] == original[key]
                assert descriptor['path'] == source['sources'][side]['path']
                assert descriptor['sha256'] == source['sources'][side]['sha256'] == sha(ROOT / descriptor['path'])
                with Image.open(ROOT / descriptor['path']) as image:
                    assert list(image.size) == descriptor['image_dimensions']
                    x, y, w, h = descriptor['crop_xywh']
                    px, py = descriptor['point_xy']
                    assert w == h == 96 and 0 <= x <= px < x+w <= image.width
                    assert 0 <= y <= py < y+h <= image.height
        summary = result['summaries'][ident]
        assert summary['manual_outcomes'] == dict(collections.Counter(r['outcome'] for r in observations))
        assert summary['inlier_outcomes'] == dict(collections.Counter(r['outcome'] for r in observations if r['ransac_inlier']))
        assert summary['reviewed_correspondences'] == len(expected)
        assert summary['original_screen_passed'] == source['screen_passed']
        assert (ROOT / selection['review_figure']).exists()
        total += len(expected)
    assert total == 63 and not review['independent_review'] and not review['blind']
    inliers = [r for r in manifest['selections']['8994-1-2']['items'] if r['ransac_inlier']]
    assert len(inliers) == 10
    assert all(r['sources'][1]['point_xy'][1] < 37 for r in inliers)
    assert all(r['sources'][0]['image_dimensions'][1] - r['sources'][0]['point_xy'][1] < 36 for r in inliers)
    for path, expected_sha in result['unchanged_inputs'].items():
        assert sha(ROOT / path) == expected_sha, path
    assert not any(result[k] for k in ['accepted_photographic_overlap', 'complete_surface_map_established',
        'physical_join_established', 'new_codex_attribution', 'novelty_cleared',
        'independent_confirmation', 'changed_e35_screen', 'new_download_bytes'])
    print(json.dumps({'reviewed_correspondences': total, 'all_selected_points_accounted_for': True,
        'frozen_core_and_e35_inputs_unchanged': True,
        'scope': 'Coverage, coordinate/bounds, source-hash and declared-limit checks only; not visual reading truth, medieval mapping or novelty.'}))


if __name__ == '__main__':
    main()
