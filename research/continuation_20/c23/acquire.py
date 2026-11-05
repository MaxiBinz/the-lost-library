"""Fetch one source image actually linked by Alvin; no URL enumeration.

The normal image viewer exposed this exact attachment but failed to render it.
No denial was bypassed. A single bounded original is used for a source comparison.
"""
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import urlopen

from PIL import Image

HERE = Path(__file__).resolve().parent
CAP = 40_000_000


def main():
    # These two exact links were exposed by the normal viewer controls. This is
    # not an enumerator over guessed attachment identifiers.
    attachment = sys.argv[1] if len(sys.argv) > 1 else '0144'
    assert attachment in ('0144', '0145'), 'Only the two observed comparison files are permitted.'
    url = f'https://www.alvin-portal.org/alvin/attachment/download/alvin-record:160517/ATTACHMENT-{attachment}.tiff'
    receipt_path = HERE / ('download_receipt.json' if attachment == '0144' else 'download_receipt-0145.json')
    if receipt_path.exists():
        raise SystemExit('Receipt exists: no automatic retry or duplicate transfer.')
    root = HERE.parents[2]
    audit = json.loads((root / 'data/resource_audit.json').read_text())
    assert audit['working_source_capture_files'] + 2 <= 300
    assert audit['conservative_planning_total_bytes'] + CAP < 3_000_000_000
    receipt = {'url': url, 'purpose': 'One exact C23 comparison image; folio identification initially unverified',
               'rights_url': 'https://creativecommons.org/publicdomain/mark/1.0/',
               'rights_source': 'https://www.alvin-portal.org/alvin/view.jsf?pid=alvin-record:160517',
               'requested_at_utc': datetime.now(timezone.utc).isoformat(), 'cap_bytes': CAP,
               'bytes_received': 0, 'saved': False}
    try:
        with urlopen(url, timeout=45) as response:
            receipt.update(status=response.status, final_url=response.url,
                           content_type=response.headers.get('Content-Type'))
            length = response.headers.get('Content-Length')
            if length and int(length) > CAP:
                raise ValueError('Declared file exceeds cap; no body read.')
            chunks = []
            while True:
                chunk = response.read(min(65536, CAP + 1 - receipt['bytes_received']))
                if not chunk:
                    break
                chunks.append(chunk)
                receipt['bytes_received'] += len(chunk)
                if receipt['bytes_received'] > CAP:
                    raise ValueError('Transfer cap exceeded; partial body discarded.')
        raw = b''.join(chunks)
        original = HERE / f'c23-attachment-{attachment}.tiff'
        original.write_bytes(raw)
        receipt.update(saved=True, local_path=str(original.relative_to(root)),
                       sha256=hashlib.sha256(raw).hexdigest())
        with Image.open(original) as source:
            receipt['dimensions'] = list(source.size)
            image = source.convert('RGB')
            if image.width > 2200:
                image = image.resize((2200, round(image.height * 2200 / image.width)))
            derivative = HERE / f'c23-attachment-{attachment}-2200px.jpg'
            image.save(derivative, quality=92)
            receipt['derivative'] = {'path': str(derivative.relative_to(root)),
                'sha256': hashlib.sha256(derivative.read_bytes()).hexdigest(),
                'dimensions': list(image.size), 'bytes': derivative.stat().st_size,
                'transformation': 'RGB conversion, resize to at most2200px width, JPEG quality92; no generated detail.'}
    except Exception as error:
        receipt['error'] = str(error)
    finally:
        receipt_path.write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()
