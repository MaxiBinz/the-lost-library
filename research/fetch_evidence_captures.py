"""Bounded alternate views of the ten Swedish objects in the frozen queue.

Serial writes preserve the shared catalogue. Source ordinal is not a folio side.
Uses existing image-rights, host and download safeguards; no denied retry.
"""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from lost_library.pipeline import fetch_capture


def predictor_hash():
    records = json.loads((ROOT / 'data/fragments.json').read_text())
    payload = [(r['id'], r['normalized'], (r.get('image') or {}).get('sha256')) for r in records]
    return hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()


def main():
    hypotheses = json.loads((ROOT / 'data/hypotheses.v1.json').read_text())['hypotheses']
    records = {r['id']: r for r in json.loads((ROOT / 'data/fragments.json').read_text())}
    ids = sorted({q[k] for q in hypotheses for k in ('left_id', 'right_id')
                  if q[k].startswith('mpo-') and records[q[k]].get('image_path')})
    before = predictor_hash()
    log_file = ROOT / 'data/evidence_capture_log.json'
    log = json.loads(log_file.read_text()) if log_file.exists() else []
    for ident in ids:
        for index in (1, 2, 3):
            if any(x['id'] == ident and x['capture_index'] == index for x in log):
                continue
            item = {'id': ident, 'capture_index': index}
            try:
                item.update(status='ok', capture=fetch_capture(ROOT, ident, index, width=1000))
            except Exception as error:
                item.update(status='failed; do not automatically retry', error=str(error))
            log.append(item)
            log_file.write_text(json.dumps(log, ensure_ascii=False, indent=2) + '\n')
            print(ident, index, item['status'], flush=True)
    assert predictor_hash() == before, 'Predictor inputs unexpectedly changed'
    print(json.dumps({'normalized_metadata_and_primary_image_hash_unchanged': before,
                      'source_views': len(log), 'failures': sum(x['status'] != 'ok' for x in log)}))


if __name__ == '__main__':
    main()
