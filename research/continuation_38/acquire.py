"""Acquire the single original linked by the public, labelled C23 69r view."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
import urllib.request

from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
URL = 'https://www.alvin-portal.org/alvin/attachment/download/alvin-record:160517/ATTACHMENT-0139.tiff'
LIMIT = 50_000_000


def main():
    destination = HERE / 'c23-69r-0139.tiff'
    derivative = HERE / 'c23-69r-0139-2200px.jpg'
    assert not destination.exists(), 'Do not reacquire a retained source'
    receipt = {
        'requested_at_utc': datetime.now(timezone.utc).isoformat(),
        'url': URL, 'source_record': 'https://www.alvin-portal.org/alvin/view.jsf?pid=alvin-record:160517',
        'folio_label': 'Folio 69r',
        'identification': 'Selected the explicitly named thumbnail; viewer then labelled Folio 69r and exposed this download URL. Not inferred from ordinal.',
        'rights_url': 'https://creativecommons.org/publicdomain/mark/1.0/',
        'rights_receipt': 'research/continuation_38/c23-record.ax.txt',
        'cap_bytes': LIMIT, 'bytes_received': 0, 'saved': False,
    }
    try:
        request = urllib.request.Request(URL, headers={'User-Agent': 'Lost-Library-research/1.0'})
        with urllib.request.urlopen(request, timeout=30) as response:
            receipt.update(status=response.status, final_url=response.url,
                           content_type=response.headers.get('Content-Type'))
            assert response.status == 200
            assert 'image/tiff' in receipt['content_type'].lower(), 'Stop on a non-image response; do not bypass verification'
            declared = response.headers.get('Content-Length')
            if declared:
                assert int(declared) <= LIMIT
            chunks = []
            while True:
                part = response.read(1024 * 1024)
                if not part:
                    break
                receipt['bytes_received'] += len(part)
                assert receipt['bytes_received'] <= LIMIT
                chunks.append(part)
            content = b''.join(chunks)
        assert content[:4] in (b'II*\x00', b'MM\x00*')
        destination.write_bytes(content)
        receipt.update(saved=True, local_path=str(destination.relative_to(ROOT)),
                       sha256=hashlib.sha256(content).hexdigest())
        with Image.open(destination) as source:
            receipt['source_dimensions'] = list(source.size)
            preview = source.convert('RGB')
            preview.thumbnail((2200, 10000))
            preview.save(derivative, quality=95)
        receipt['derivative'] = {'path': str(derivative.relative_to(ROOT)),
                                 'dimensions': list(preview.size),
                                 'sha256': hashlib.sha256(derivative.read_bytes()).hexdigest(),
                                 'transform': 'Pillow RGB, thumbnail width 2200, JPEG quality 95; no generated pixels or restoration'}
    except Exception as exc:
        receipt['error'] = f'{type(exc).__name__}: {exc}'
        raise
    finally:
        (HERE / 'download_receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
        print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()
