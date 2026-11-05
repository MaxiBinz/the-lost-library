"""Verify retained source provenance and inference bounds; not paleography."""
import hashlib
import json
from pathlib import Path
from PIL import Image

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]


def read(path):
    return json.loads((ROOT/path).read_text())


def sha(path):
    return hashlib.sha256((ROOT/path).read_bytes()).hexdigest()


def main():
    protocol=read('research/continuation_44/protocol.json')
    result=read('research/continuation_44/results.json')
    receipts=read('research/continuation_44/download_receipts.json')
    captures=read('research/continuation_44/captures.json')['captures']
    observations=read('research/continuation_44/observations.json')['annotations']
    assert len(captures)==len(receipts)==9
    assert len({r['url'] for r in receipts})==9
    for receipt,cap in zip(receipts,captures):
        assert receipt['status']==200 and receipt['saved']
        assert receipt['path']==cap['path'] and receipt['sha256']==cap['sha256']==sha(cap['path'])
        assert receipt['bytes_received']==cap['bytes']==(ROOT/cap['path']).stat().st_size
        assert receipt['manifest_sha256']==sha(cap['manifest'])
        manifest=read(cap['manifest']);value=manifest
        for key in cap['manifest_locator'].split('/'):
            value=value[int(key)] if isinstance(value,list) else value[key]
        assert value==cap['url']==receipt['url']
        rights=next(m['value']['none'][0] for m in manifest['metadata'] if 'Rights' in m['label'].get('en',[]))
        assert rights==cap['rights_url']=='http://creativecommons.org/publicdomain/mark/1.0/'
        with Image.open(ROOT/cap['path']) as image:
            assert image.size==(cap['width'],cap['height'])
        assert cap['side_assignment'] is None
    for path,expected in protocol['fixed_images'].items():
        assert sha(path)==expected
    for path,expected in result['unchanged_inputs'].items():
        assert sha(path)==expected,path
    assert [a['id'] for a in observations]==result['observations']
    assert len(observations)==11
    inspection=read('research/continuation_44/inspection.v2.json')
    assert inspection['previous_version']=='research/continuation_44/inspection.v1.json'
    revision=inspection['reference_assisted_revision']
    original=read(inspection['previous_version'])
    assert next(r for r in original['source_observations'] if r['id']=='9620-rubric')['literal_candidate']==revision['previous_literal_candidate']
    assert next(a for a in observations if a['id']==revision['site'])['literal_candidate']==revision['revised_literal_candidate']
    assert result['reference_assisted_revision']==revision
    for a in observations:
        path=a['target']['source'];assert sha(path)==a['sha256']
        x,y,w,h=map(int,a['target']['selector']['value'][5:].split(','))
        with Image.open(ROOT/path) as image:
            assert list(image.size)==a['image_dimensions']
            assert 0<=x<x+w<=image.width and 0<=y<y+h<=image.height
        assert not a['independent_confirmation']
    assert result['new_download_bytes']==sum(r['bytes_received'] for r in receipts)==2769595
    assert result['pair_state']=='unresolved'
    assert not any(result[k] for k in ['four_vs_five_split_supported','different_book_genres_established',
        'duplicated_complete_opening_established','same_codex_established','physical_join_established',
        'catalogue_correction_confirmed','novelty_cleared','independent_confirmation','new_discovery','new_physical_objects'])
    print(json.dumps({'native_photographs_checked':9,'source_regions_checked':11,
        'transfer_bytes':result['new_download_bytes'],'frozen_core_inputs_unchanged':True,
        'scope':'Manifest URL/rights/hash/dimensions/bounds and declared-limit checks; no independent text/rule reading, complete liturgical position, historical attribution, catalogue correction or novelty proof.'}))


if __name__=='__main__':
    main()
