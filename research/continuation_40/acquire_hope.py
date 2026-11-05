"""One official, bounded scholarly reading copy; no manuscript acquisition."""
import hashlib
import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
URL = 'https://findresearcher.sdu.dk/ws/portalfiles/portal/281648358/phd_thesis_sdu_cml_steffen_hope_constructing_institutional_identity_through_the_cult_of_royal_saint.pdf'


def main():
    path = ROOT / 'research/scholarship/hope2018.pdf'
    assert not path.exists(), 'Use the retained source instead of reacquiring it'
    receipt = {'url': URL, 'requested_at_utc': datetime.now(timezone.utc).isoformat(),
               'cap_bytes': 30_000_000, 'bytes_received': 0, 'saved': False,
               'role': 'Private scholarly concordance reading copy, not a manuscript source image'}
    try:
        with urllib.request.urlopen(URL, timeout=30) as response:
            receipt.update(status=response.status, content_type=response.headers.get('Content-Type'), final_url=response.url)
            assert response.status == 200 and 'application/pdf' in receipt['content_type'].lower()
            if response.headers.get('Content-Length'):
                assert int(response.headers['Content-Length']) <= receipt['cap_bytes']
            chunks = []
            while True:
                part = response.read(65536)
                if not part:
                    break
                receipt['bytes_received'] += len(part)
                assert receipt['bytes_received'] <= receipt['cap_bytes']
                chunks.append(part)
        data = b''.join(chunks)
        assert data.startswith(b'%PDF')
        path.write_bytes(data)
        receipt.update(saved=True, path=str(path.relative_to(ROOT)), sha256=hashlib.sha256(data).hexdigest())
    except Exception as exc:
        receipt['status'] = getattr(exc, 'code', None)
        receipt['error'] = f'{type(exc).__name__}: {exc}'
        raise
    finally:
        (HERE / 'download_receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
        print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()
