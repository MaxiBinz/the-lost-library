"""Offline resource inventory; transfer receipts are incomplete, not a lifetime meter."""
from datetime import datetime, timezone
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECEIPTS = [
    'data/downloads.json', 'research/access_log.json', 'research/target_access_log.json',
    'research/evidence/finnish_access.json', 'research/evidence/beauvais_access.json',
    'research/evidence/goal_negative_image_access.json', 'research/legal_b193_probe.json',
    'research/scholarship/receipts.json',
    'research/independent_pass/methods/full_issue_receipt.json',
    'research/continuation_20/c23/download_receipt.json',
    'research/continuation_20/c23/download_receipt-0145.json',
    'research/continuation_20/registration/dependency_receipt.json',
    'research/continuation_22/manifest_receipt.json',
    'research/continuation_26/bompac/download_receipt.json',
    'research/continuation_37/download_receipts.json',
    'research/continuation_38/download_receipt.json',
    'research/continuation_39/method_receipt.json',
    'research/continuation_40/download_receipt.json',
    'research/continuation_44/download_receipts.json',
    'research/continuation_50/download_receipts.json',
    'research/continuation_51/metadata_receipts.json',
    'research/continuation_52/download_receipts.json',
    'research/continuation_54/download_receipts.json',
    'research/continuation_56/metadata_receipts.json',
    'research/continuation_56/download_receipts.json',
    'research/continuation_65/download_receipt.json',
    'research/continuation_88/supplement_receipt.json',
    'research/continuation_114/download_receipt.json',
]


def receipt_bytes(value):
    """Count each transfer receipt once, without recounting its capture metadata."""
    if isinstance(value, list):
        return sum(receipt_bytes(v) for v in value)
    if isinstance(value, dict):
        own = value.get('bytes_received', value.get('bytes', 0))
        nested = 0
        for key, child in value.items():
            if not isinstance(child, (dict, list)):
                continue
            # A high-resolution transfer carries the saved capture descriptor too.
            # That descriptor repeats this response's byte count; a nested sample
            # with its own URL, by contrast, is a separate transfer and must count.
            if (key == 'capture' and isinstance(child, dict)
                    and 'bytes_received' in value
                    and child.get('url') == value.get('url')
                    and child.get('sha256') == value.get('sha256')
                    and child.get('bytes') == own):
                continue
            if key == 'derivative' and 'bytes_received' in value:
                continue  # A local JPEG derivative is not another transfer.
            nested += receipt_bytes(child)
        return (own if isinstance(own, int) else 0) + nested
    return 0


def main():
    records = json.loads((ROOT / 'data/fragments.json').read_text())
    images = {r['image_path'] for r in records if r.get('image_path')}
    images.update(c['path'] for r in records for c in r.get('captures', []) if c.get('path'))
    core_images = set(images)
    comparison_path = ROOT / 'data/comparison_sources.v1.json'
    comparisons = json.loads(comparison_path.read_text()) if comparison_path.exists() else []
    for record in comparisons:
        images.add(record['image_path'])
        images.update(c['path'] for c in record.get('captures', []) if c.get('path'))
        if record.get('original_source', {}).get('path'):
            images.add(record['original_source']['path'])
    external_comparison_images = set(images) - core_images
    additional = json.loads((ROOT / 'research/continuation_44/captures.json').read_text())['captures']
    additional += json.loads((ROOT / 'research/continuation_50/captures.json').read_text())['captures']
    additional += json.loads((ROOT / 'research/continuation_52/captures.json').read_text())['captures']
    additional += json.loads((ROOT / 'research/continuation_54/captures.json').read_text())['captures']
    additional += json.loads((ROOT / 'research/continuation_65/captures.json').read_text())['captures']
    images.update(c['path'] for c in additional)
    assert len(images) <= 300, 'Working source-image bound exceeded'
    receipts = {p: receipt_bytes(json.loads((ROOT / p).read_text())) for p in RECEIPTS}
    retained = sum(p.stat().st_size for folder in ('data', 'research')
                   for p in (ROOT / folder).rglob('*') if p.is_file())
    historical = list((ROOT / 'research/evidence').glob('*.jpg'))
    model_weights = sum(p.stat().st_size for p in (ROOT / 'data/models').rglob('*.pth'))
    reserve = 1_000_000_000
    # Counting weights again is deliberately conservative if any logged fetch overlaps.
    planning_total = sum(receipts.values()) + model_weights + reserve
    assert planning_total < 3_000_000_000, 'Resource planning allowance exhausted'
    result = {
        'date': datetime.now(timezone.utc).date().isoformat(),
        'recorded_transfer_receipt_sum_including_possible_overlaps': sum(receipts.values()),
        'receipt_subtotals': receipts,
        'receipt_accounting_notes': [
            'Ten higher-resolution source-image transfers, including four E33 Fr 8994 images, '
            'are already included in data/downloads.json; their separate ledgers are not added again. Nested capture-byte '
            'metadata inside each transfer receipt is not another transfer.',
            'The Duba reference is one successful full-issue PDF transfer, counted once. '
            'Its private reading copy is not a working source-image file.',
            'The E37 Urberg dissertation is one successful 425,202,182-byte transfer. '
            'Earlier zero-body attempts add no bytes; the private PDF and local '
            'reading renders are not working manuscript source-image files.',
            'The E39 official Cantus guide is one 1,083,153-byte private method PDF '
            'transfer; its local reading renders add no transfer or manuscript-image count.',
            'The two E20 C23 TIFF transfers and the E38 69r transfer are counted once each; their local JPEG derivatives '
            'add image files but no network transfer bytes.',
            'The five BOMPAC workbooks/readmes/commentary files are counted once from their '
            'file-level receipts; they are data/document downloads, not manuscript images.',
            'The isolated OpenCV wheel is counted as a bounded local-compute dependency; '
            'it is excluded from the review release and is not a source image.',
            'E44 adds nine exact manifest-linked PDM photographs of existing8066/9620 objects, '
            '2,769,595 transfer bytes, counted once from their receipts; no extra physical object.',
            'E50 adds six saved exact manifest-linked source files of existing10349/2862 objects, '
            '1,542,176 confirmed successful bytes. A DNS failure was not retried; a timeout may have unmeasured traffic '
            'even with no saved body, so the historical reserve remains. No new physical object.',
            'E51 adds three saved public Zenodo API metadata responses,31,373 bytes, '
            'counted once. No new workbook or source-image transfer; web-reader/search traffic remains unmeasured.',
            'E52 adds six exact-manifest PDM photographs of existing8072/8073 objects, '
            '1,896,527 confirmed saved bytes. Two timed-out URLs were not retried; unmeasured timeout traffic remains covered by the historical reserve.',
            'E54 adds eight exact-manifest PDM photographs of existing10407/10437 objects, '
            '2,853,289 confirmed saved bytes. All eight single attempts succeeded; resolution variants are not new physical objects or witnesses.',
            'E65 adds one native-size derivative of an existing Fr 8201 photograph, 313,747 bytes; it is not a new physical object, side or witness.',
            'The E88 Cambridge supplement is one 2,782,409-byte DOCX transfer, not a manuscript source-image acquisition.',
            'E114 adds one 18,526,969-byte CC BY 4.0 BOMPAC metadata CSV transfer; the copy is not a manuscript image.',
        ],
        'retained_research_and_data_bytes': retained,
        'working_source_capture_files': len(images),
        'core_source_image_files': len(core_images),
        'external_comparison_page_records': len(comparisons),
        'external_source_and_derivative_files': len(external_comparison_images),
        'additional_existing_object_capture_files': len({c['path'] for c in additional}),
        'working_source_image_bytes': sum((ROOT / p).stat().st_size for p in images),
        'historical_probe_image_files_outside_working_set': len(historical),
        'local_rendering_derivatives_count_as_downloads': False,
        'model_weights_bytes': model_weights,
        'historical_unlogged_transfer_planning_reserve_bytes': reserve,
        'conservative_planning_total_bytes': planning_total,
        'download_limit_bytes': 3_000_000_000,
        'exact_lifetime_transfer_total_verified': False,
        'caution': 'Receipts incompletely cover earlier browser reads and dependency installs. '
                   'Overlapping receipts may overcount. The reserve is a planning allowance, '
                   'not measured traffic or proof of an exact lifetime total. No bulk expansion authorized.',
    }
    (ROOT / 'data/resource_audit.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
