"""Check E46 source locators and declared arithmetic; not music adjudication."""
import hashlib
import json
import sys
from pathlib import Path
from PIL import Image
from compare_notes import compare

ROOT=Path(__file__).resolve().parents[2]


def read(path):
    return json.loads((ROOT/path).read_text())


def sha(path):
    return hashlib.sha256((ROOT/path).read_bytes()).hexdigest()


def main():
    protocol=read('research/continuation_46/protocol.json')
    readings=read('research/continuation_46/readings.v2.json')
    prior=readings['previous_reading'];assert sha(prior['path'])==prior['sha256']
    previous=read(prior['path']);assert readings['sources']==previous['sources']
    comparison=read('research/continuation_46/comparison.json')
    assert comparison==compare(readings)
    assert comparison['candidate_celos_head_counts']=={'8066':5,'9620':2}
    assert comparison['candidate_primary_centres']==15 and comparison['optional_uncertain_centres']==1
    assert not comparison['robust_direction_contrast']
    for s in readings['sources'].values():
        assert sha(s['path'])==s['sha256']
        with Image.open(ROOT/s['path']) as image:
            x,y,w,h=s['window_xywh'];assert 0<=x<x+w<=image.width and 0<=y<y+h<=image.height
            for e in s['events']+s['optional_events']:
                px,py=e['pixel'];assert x<=px<x+w and y<=py<y+h
        assert s['absolute_pitch'] is None and s['diatonic_staff_steps'] is None
    annotations=read('research/continuation_46/observations.json')['annotations']
    result=read('research/continuation_46/results.json')
    assert len(annotations)==6 and [a['id'] for a in annotations]==result['observations']
    for a in annotations:
        path=a['target']['source'];assert sha(path)==a['sha256']
        with Image.open(ROOT/path) as image:
            assert list(image.size)==a['image_dimensions']
            x,y,w,h=map(int,a['target']['selector']['value'][5:].split(','))
            assert 0<=x<x+w<=image.width and 0<=y<y+h<=image.height
        assert not a['independent_confirmation']
    for key in ['same_complete_chant_identification_established','diagnostic_melodic_variant_established',
                'robust_direction_contrast','melodic_identity_established','absolute_pitches_verified',
                'same_codex_established','different_codex_established','physical_join_established',
                'catalogue_correction_confirmed','novelty_cleared','independent_confirmation','new_discovery',
                'new_working_source_files','new_recorded_file_download_bytes']:
        assert not result[key]
    assert result['pair_state']=='unresolved'
    for path,expected in protocol['frozen_inputs'].items():assert sha(path)==expected
    guide=protocol['method_source'];present=(ROOT/guide['path']).is_file()
    if '--require-private' in sys.argv:assert present
    if present:assert sha(guide['path'])==guide['sha256']
    print(json.dumps({'source_images_checked':2,'regions_checked':6,'primary_centres_checked':15,
        'uncertain_centres_retained':1,'private_method_copy_present':present,'frozen_core_inputs_unchanged':True,
        'scope':'Hashes, coordinates, preserved readings and arithmetic only; no independent musical/genre/identity or novelty validation.'}))


if __name__=='__main__':
    main()
