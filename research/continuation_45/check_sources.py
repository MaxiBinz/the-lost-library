"""Check exact E45 provenance and scope, not independent rubric readings."""
import hashlib
import json
import sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]


def read(path):
    return json.loads((ROOT/path).read_text())


def main():
    protocol=read('research/continuation_45/protocol.json')
    manual=read('research/continuation_45/manual_readings.json')
    result=read('research/continuation_45/results.json')
    annotations=read('research/continuation_45/observations.json')['annotations']
    expected={r['path']:r for r in protocol['fixed_sources']}
    assert len(expected)==9
    assert {r['path'] for r in manual['capture_coverage']}==set(expected)
    for path,source in expected.items():
        assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==source['sha256']
        with Image.open(ROOT/path) as image:
            assert image.size==(source['width'],source['height'])
    assert len(annotations)==8 and [a['id'] for a in annotations]==result['observations']
    for region,a in zip(manual['regions'],annotations):
        assert a['target']['source']==region['path'] and a['literal_candidate']==region['literal_candidate']
        x,y,w,h=region['xywh']; assert a['target']['selector']['value']=='xywh='+','.join(map(str,region['xywh']))
        assert a['sha256']==expected[region['path']]['sha256']
        assert 0<=x<x+w<=a['image_dimensions'][0] and 0<=y<y+h<=a['image_dimensions'][1]
        assert not a['independent_confirmation']
    assert result['pair_state']=='unresolved'
    for key in ['same_codex_established','different_codex_established','physical_join_established',
                'complete_side_map_established','complete_duplicate_opening_established',
                'catalogue_correction_confirmed','novelty_cleared','independent_confirmation','new_discovery',
                'new_download_bytes','new_source_files']:
        assert not result[key]
    for path,sha in protocol['frozen_inputs'].items():
        assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==sha
    article=next(s for s in read('research/continuation_45/sources.json')['sources'] if s.get('local_private_path'))
    private=ROOT/article['local_private_path']
    if '--require-private' in sys.argv:
        assert private.is_file(), 'Private reading PDF required'
    if private.is_file():
        assert hashlib.sha256(private.read_bytes()).hexdigest()==article['sha256']
    print(json.dumps({'source_photographs_checked':9,'regions_checked':8,'frozen_core_inputs_unchanged':True,
        'private_reading_copy_present':private.is_file(),
        'scope':'Hashes, source coverage, selectors and declared limits only; no independent reading, full office/side map, attribution or novelty validation.'}))


if __name__=='__main__':
    main()
