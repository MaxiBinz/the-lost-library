"""Check locators, all declared pairings and limits; never certify a reading."""
import hashlib
import json
from pathlib import Path
from PIL import Image

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]


def read(path):
    return json.loads(path.read_text())


def main():
    protocol=read(HERE/'protocol.json');result=read(HERE/'results.json')
    coverage=read(HERE/'row_coverage.json');observations=read(HERE/'observations.json')
    rows={}
    for capture in coverage['captures']:
        path=ROOT/capture['path']
        assert hashlib.sha256(path.read_bytes()).hexdigest()==capture['sha256']
        with Image.open(path) as image:
            assert list(image.size)==capture['dimensions']
            assert [r['row'] for r in capture['rows']]==list(range(1,len(capture['rows'])+1))
            assert all(0<=r['y_range'][0]<r['y_range'][1]<=image.height for r in capture['rows'])
        assert not capture['complete_medieval_surface_verified']
        rows[capture['capture']]=capture['visible_medieval_text_rows']
        assert rows[capture['capture']]==len(capture['rows'])
    assert [c['path'] for c in coverage['captures']]==protocol['fixed_sources']
    assert [c['pair'] for c in result['comparisons']]==protocol['comparisons']
    for comparison in result['comparisons']:
        left,right=comparison['pair']
        assert comparison['visible_row_sum']==rows[left]+rows[right]==11
        assert not comparison['physical_adjacency_established']
        assert not comparison['complete_surface_map_established']
    assert [a['id'] for a in observations['annotations']]==result['new_regions']
    existing={a['id'] for number in [34,40] for a in read(ROOT/f'research/continuation_{number}/observations.json')['annotations']}
    assert set(observations['reused_regions'])==set(result['reused_regions'])<=existing
    for annotation in observations['annotations']:
        p=ROOT/annotation['target']['source']
        assert hashlib.sha256(p.read_bytes()).hexdigest()==annotation['sha256']
        x,y,w,h=map(int,annotation['target']['selector']['value'][5:].split(','))
        with Image.open(p) as image:
            assert list(image.size)==annotation['image_dimensions']
            assert 0<=x<x+w<=image.width and 0<=y<y+h<=image.height
        assert not annotation['independent_confirmation']
    assert '?' in observations['annotations'][0]['literal_candidate']
    assert not any(result[k] for k in ['accepted_photographic_overlap','physical_adjacency_established',
        'complete_surface_map_established','physical_join_established','new_codex_attribution',
        'novelty_cleared','independent_confirmation','new_download_bytes_retained'])
    for path,expected in result['unchanged_inputs'].items():
        assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==expected,path
    sources=read(HERE/'sources.json')
    assert not sources['novelty_cleared'] and not sources['independent_confirmation']
    print(json.dumps({'new_regions_checked':len(observations['annotations']),
        'captures_checked':len(rows),'all_four_pairings_accounted_for':True,
        'frozen_core_e35_inputs_unchanged':True,
        'scope':'Source hashes/dimensions/locators, row-sum arithmetic and declared-limit consistency; no independent transcription, complete surface, historical attribution or novelty verification.'}))


if __name__=='__main__':
    main()
