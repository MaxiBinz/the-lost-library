"""E49 source integrity, region bounds and inferential limits; no new access."""
import csv
import hashlib
import json
from pathlib import Path

from PIL import Image

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]


def read(path):
    return json.loads((ROOT/path).read_text())


def main():
    protocol=read('research/continuation_49/protocol.json')
    for path,expected in protocol['frozen_inputs'].items():
        assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==expected,path
    caps={c['path']:c for c in protocol['fixed_sources']}
    assert len(caps)==8 and {c['object_id'] for c in caps.values()}=={'mpo-8201','mpo-8304'}
    for path,c in caps.items():
        assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==c['sha256'],path
        with Image.open(ROOT/path) as im:
            assert im.size==(c['width'],c['height'])
        assert c['medieval_side'] is None
    readings=read('research/continuation_49/manual_readings.json')
    assert {r['path'] for r in readings['coverage']}==caps.keys()
    assert len(readings['coverage'])==8
    assert all(r['all_visible_pixels_inspected'] and r['medieval_side'] is None and not r['independent_witness'] for r in readings['coverage'])
    annotations=read('research/continuation_49/observations.json')['annotations']
    assert len(annotations)==len(readings['regions'])==4
    for a,r in zip(annotations,readings['regions']):
        assert a['id']==r['id'] and a['literal_candidate']==r['literal']
        assert a['normalized_candidate']==r['normalized'] and not a['independent_confirmation']
        c=caps[r['path']]
        x,y,w,h=r['xywh']
        assert 0<=x<x+w<=c['width'] and 0<=y<y+h<=c['height']
        assert a['target']['selector']['value']=='xywh='+','.join(map(str,r['xywh']))
        assert a['sha256']==c['sha256'] and a['rights_url']==c['rights_url']
    result=read('research/continuation_49/results.json')
    assert result['8304_local_opening_supported']
    for key in ['8201_second_complete_office_opening_established','published_duplicate_opening_argument_fully_replicated',
        'published_20106_8201_continuity_independently_verified','published_rejection_refuted',
        'new_historical_exclusion_established','new_discovery','independent_confirmation','goal_complete','global_blocker_established']:
        assert result[key] is False,key
    sources=read('research/continuation_49/sources.json')
    reference=sources['published_argument']
    reference_path=ROOT/reference['local_path']
    if reference_path.exists():
        assert hashlib.sha256(reference_path.read_bytes()).hexdigest()==reference['sha256']
    missing=sources['missing_positive_record']
    with (ROOT/missing['source']).open(encoding='utf-8-sig') as handle:
        rows={n:r for n,r in enumerate(csv.DictReader(handle),2)}
    actual=rows[missing['csv_line']]
    assert {k:actual[k] for k in missing['source_values']}==missing['source_values']
    assert not actual['iiif_manifest'] and not actual['bildbetrachter']
    assert sources['candidate_catalogue_record']['manifest_requested'] is False
    graph=read('data/knowledge.v1.json')
    overlay={e['id'] for e in graph['evidence']}
    assert all('evidence:'+a['id'] in overlay for a in annotations)
    recheck=next(c for c in graph['claims'] if c['id']=='interpretation:E48-unit4861')['primary_source_recheck']
    assert not recheck['full_published_argument_replicated'] and not recheck['new_historical_exclusion']
    live_register=read('data/lead_register.v1.json')
    snapshot='research/continuation_50/lead_register.before.json'
    if (ROOT/snapshot).exists():
        pinned=read('research/continuation_50/primary_protocol.json')['register_before_overlay']
        assert hashlib.sha256((ROOT/snapshot).read_bytes()).hexdigest()==pinned['sha256']
        current=read(snapshot)
    else:
        current=live_register
    assert len(current['leads'])==168
    assert sum(bool(l.get('primary_pair_test_pending')) for l in current['leads'])==31
    prior_pending={l['id'] for l in current['leads'] if l.get('primary_pair_test_pending')}
    live_pending={l['id'] for l in live_register['leads'] if l.get('primary_pair_test_pending')}
    assert live_pending<=prior_pending
    assert next(l for l in current['leads'] if l.get('frozen_hypothesis')=='H06')['decision_state']=='contradicted'
    record=next(e for e in graph['entities'] if e['id']=='record:manuscripta-101111')
    assert record['type']=='CatalogRecord' and record['physical_object'] is None
    assert record['crosswalk_status']=='unresolved'
    print(json.dumps({'retained_captures_checked':8,'source_regions_checked':4,
        'full_published_argument_replicated':False,'historical_primary_pair_tests_pending':31,
        'current_primary_pair_tests_pending':len(live_pending),
        'catalogue_record_not_merged_into_physical_fragment':True,
        'private_reference_present':reference_path.exists(),
        'scope':'Hashes, bounds, source-record fields and preserved inferential limits, not independent reading adjudication or novelty.'}))


if __name__=='__main__':
    main()
