"""Record bounded E51 source-version identity and qualified margin readings.

No network requests. Private reading PDFs stay outside the review archive;
their original receipts remain inspectable when those PDFs are absent.
"""
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def read(path):
    return json.loads((ROOT / path).read_text())


def save(name, value):
    (HERE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def metadata_comparison():
    old = read('research/continuation_26/bompac/download_receipt.json')['files']
    records = [read('research/continuation_51/' + name) for name in
               ['combined-latest.json', 'raw-latest.json']]
    rows = []
    for label, receipt in old.items():
        record = records[0 if label.startswith('combined') else 1]
        published = next(f for f in record['files'] if f['key'] == receipt['filename'])
        folder = ROOT / 'research/continuation_26/bompac'
        if not label.startswith('combined'):
            folder /= 'raw_metadata'
        path = folder / receipt['filename']
        current_md5 = published['checksum'].removeprefix('md5:')
        assert current_md5 == receipt['md5'] == receipt['published_md5']
        assert published['size'] == receipt['bytes']
        if path.exists():
            raw = path.read_bytes()
            assert len(raw) == published['size']
            assert hashlib.md5(raw).hexdigest() == current_md5
            assert hashlib.sha256(raw).hexdigest() == receipt['sha256']
        rows.append({'label': label, 'path': str(path.relative_to(ROOT)),
                     'file': receipt['filename'], 'bytes': published['size'],
                     'published_current_md5': current_md5, 'sha256': receipt['sha256'],
                     'original_receipt_md5_matches': True,
                     'local_bytes_verified_in_this_execution': path.exists(),
                     'current_version_record': record['id'], 'doi': record['doi']})
    return {'checked_releases': [{'id': r['id'], 'conceptrecid': r['conceptrecid'],
                'doi': r['doi'], 'version': r['metadata']['version'],
                'publication_date': r['metadata']['publication_date'],
                'relations': r['metadata']['relations'],
                'description_html': r['metadata']['description']} for r in records],
            'file_comparisons': rows,
            'both_workbooks_identical_to_retained_bytes': True,
            'release_change_as_stated_by_publisher': 'v1.1 adds CSV with data unchanged.',
            'new_csv_bytes_downloaded_or_checked': False,
            'current_xlsx_assignment_scope': 'The latest public records returned on2026-10-30 distribute the identical two retained workbooks. E48 exact-cell findings, including4861 co-assignment of8201/8304, therefore apply to this current XLSX distribution. No CSV equivalence, historical correctness or novelty is independently established.',
            'independent_confirmation': False, 'novelty_cleared': False}


def main():
    p = read('research/continuation_51/primary_protocol.json')
    readings = read('research/continuation_51/manual_readings.json')
    comparison = metadata_comparison()
    save('metadata_comparison.json', comparison)
    sources = {c['path']: c for c in p['fixed_sources']}
    annotations = []
    for r in readings['regions']:
        src = sources[r['path']]
        raw = (ROOT / r['path']).read_bytes()
        assert hashlib.sha256(raw).hexdigest() == src['sha256']
        with Image.open(ROOT / r['path']) as im:
            dims = list(im.size)
        x, y, w, h = r['xywh']
        assert 0 <= x < x+w <= dims[0] and 0 <= y < y+h <= dims[1]
        annotations.append({'id': r['id'], 'type': 'Annotation', 'motivation': 'describing',
            'body': {'type': 'TextualBody', 'value': r['body'], 'language': 'en'},
            'target': {'source': r['path'], 'selector': {'type': 'FragmentSelector',
                'conformsTo': 'http://www.w3.org/TR/media-frags/',
                'value': 'xywh=' + ','.join(map(str, r['xywh']))}},
            'fragment_id': src['object_id'], 'source_url': src['url'],
            'sha256': src['sha256'], 'image_dimensions': dims,
            'rights_url': src['rights_url'], 'literal_candidate': r['literal'],
            'normalized_candidate': r['normalized'], 'observer': readings['observer'],
            'independent_confirmation': False, 'interpretation_limits': readings['limits']})
    save('observations.json', {'version': '1.0.0', 'date': '2026-10-30', 'annotations': annotations})
    # Labelled raw-pixel crops, with the previously recorded control readings.
    prior = read('data/observations.v9.json')['annotations']
    e33 = read('research/continuation_33/observations.json')['annotations']
    inherited = {a['id']: a for a in prior + e33}
    figure_rows = []
    for ident, label in [('V-10370-mark', '10370: prior ij / catalogue II'),
                         ('V-10370-kmark', '10370: prior k-like mark'),
                         ('I33-8994-roman', '8994: prior IIII control'),
                         ('I33-8994-k', '8994: prior k control')]:
        a = inherited[ident]
        xywh = list(map(int, a['target']['selector']['value'].split('=')[1].split(',')))
        figure_rows.append((label, a['target']['source'], xywh))
    figure_rows += [(r['id'], r['path'], r['xywh']) for r in readings['regions'][:2]]
    proof = Image.new('RGB', (1320, 800), 'white')
    draw = ImageDraw.Draw(proof)
    for i, (label, path, (x, y, w, h)) in enumerate(figure_rows):
        px, py = (i % 3) * 440, (i // 3) * 360
        draw.text((px+8, py+8), label, fill='black')
        with Image.open(ROOT / path) as im:
            crop = im.crop((x, y, x+w, y+h)).convert('RGB')
        scale = min(420 / crop.width, 305 / crop.height)
        crop = crop.resize((round(crop.width*scale), round(crop.height*scale)), Image.Resampling.NEAREST)
        proof.paste(crop, (px+8, py+30))
    draw.text((10, 735), 'Retained PDM source pixels; nearest-neighbour display. Four prior readings are reused, not new independent evidence.', fill='black')
    draw.text((10, 753), '20274 upper sign remains uncertain. Pencil KB / A103 k / CXVIII is a later identifier, not medieval folio118.', fill='black')
    draw.text((10, 771), 'No secure common/conflicting original address, medieval side assignment or historical book decision.', fill='black')
    proof.save(HERE / 'mark-review.png')
    saved_bytes = sum(r['bytes_received'] for r in read('research/continuation_51/metadata_receipts.json'))
    save('results.json', {'version': '1.0.0', 'date': '2026-10-30',
        'selected_lead': p['selected_lead'], 'pair': p['pair'],
        'metadata_audit': comparison,
        'metadata_response_bytes': saved_bytes,
        'source_regions': [a['id'] for a in annotations],
        'reused_source_regions': readings['reused_observations'] + readings['controls_reviewed'],
        'target_photo_views_inspected': 6, 'control_photo_views_inspected': 2,
        'new_source_files': 0, 'working_source_files_after': 194,
        'conservative_transfer_plan_after': 1671072950 + saved_bytes,
        'direct_result': readings['direct_result'], 'interpretation': readings['interpretation'],
        'primary_pair_test_executed': True, 'primary_pair_test_completed': True,
        'all_planned_target_views_inspected': True, 'initial_primary_comparison_recorded': True,
        'primary_pair_test_scope': 'The fixed six-view margin/address audit is completed; original side mapping and historical same-codex adjudication remain incomplete.',
        'historical_same_codex_adjudication_complete': False,
        'secure_comparable_original_address_recovered': False,
        'shared_original_address_established': False, 'conflicting_original_address_established': False,
        'new_historical_exclusion': False, 'new_20106_crosswalk': False,
        'decision_state': 'unresolved', 'primary_pair_tests_still_pending': 29,
        'next_test': readings['next_test'], 'new_discovery': False,
        'independent_confirmation': False, 'goal_complete': False, 'global_blocker_established': False})
    print(json.dumps({'metadata_response_bytes': saved_bytes, 'current_releases': [r['id'] for r in comparison['checked_releases']],
                     'current_workbook_identity': True, 'new_regions': len(annotations),
                     'primary_pairs_without_initial_comparison': 29, 'new_discovery': False}))


if __name__ == '__main__':
    main()
