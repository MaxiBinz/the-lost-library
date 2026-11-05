"""One bounded official Cantus reading PDF; no manuscript acquisition."""
import hashlib
import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
URL = 'https://cantusdatabase.org/static/documents/2.%20Volpiano%20Protocols.pdf'


def main():
    path = HERE / 'private-volpiano-protocols.pdf'
    assert not path.exists(), 'Use the retained copy'
    receipt = {'url': URL, 'requested_at_utc': datetime.now(timezone.utc).isoformat(),
               'cap_bytes': 3_000_000, 'bytes_received': 0, 'saved': False,
               'role': 'Private method reading copy, not a working manuscript image'}
    try:
        with urllib.request.urlopen(URL, timeout=30) as response:
            receipt.update(status=response.status, content_type=response.headers.get('Content-Type'), final_url=response.url)
            assert response.status == 200 and 'application/pdf' in receipt['content_type'].lower()
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
        receipt['error'] = f'{type(exc).__name__}: {exc}'
        raise
    finally:
        (HERE / 'method_receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
        print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()
