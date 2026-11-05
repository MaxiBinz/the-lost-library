"""Check annotation bounds and provenance, not the validity of the reading."""
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def read(path):
    return json.loads((ROOT / path).read_text())

def main():
    result = read('research/continuation_73/results.json')
    observations = read('research/continuation_73/observations.json')['annotations']
    caps = {c['path']:c for c in read('research/continuation_52/captures.json')['captures']}
    assert {a['id'] for a in observations} == set(result['source_regions'])
    for a in observations:
        path = a['target']['source']
        assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest() == a['sha256'] == caps[path]['sha256']
        assert a['source_url'] == caps[path]['url']
        x,y,w,h = map(int, a['target']['selector']['value'].removeprefix('xywh=').split(','))
        width,height = a['image_dimensions']
        assert min(x,y) >= 0 and min(w,h) > 0 and x+w <= width and y+h <= height
        assert not a['independent_confirmation']
    with (ROOT/'research/mpo.csv').open(encoding='utf-8-sig',newline='') as f:
        row = next(r for r in csv.DictReader(f) if r['signatur'] == '8073')
    assert '104' in row['inhalt'] and 'Felix terra' not in row['inhalt']
    for key in ('independent_confirmation','source_side_mapping_established','external_medieval_original_inspected',
                'novel_wording_established','historical_book_decision','new_discovery'):
        assert not result[key]
    assert result['new_source_images'] == result['new_download_bytes'] == 0
    states = {x['id']:x['decision_state'] for x in read('data/lead_register.v1.json')['leads']}
    assert states == read('research/continuation_69/decisions.before.json')['states']
    graph = read('data/knowledge.v1.json')
    for ident in ('interpretation:E73-8073-antiphon','interpretation:E73-8073-hymn'):
        claim = next(c for c in graph['claims'] if c['id'] == ident)
        assert claim['status'] == 'unresolved' and not claim['independent_confirmation']
    print(json.dumps({'image_hashes_and_regions_valid':True,'catalogue_hymn_previously_listed':True,
                      'historical_reading_independently_verified':False,'decisions_unchanged':True}))

if __name__ == '__main__':
    main()
