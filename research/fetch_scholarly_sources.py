"""One bounded public download per explicitly identified scholarly PDF.

No access-denial retries. Preserve receipts; originals are private research
copies, not implicitly licensed GitHub assets. Batch cap: 20 MB.
"""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
SOURCES = [
    ('hallqvist2020.pdf', 'https://lup.lub.lu.se/student-papers/record/9032430/file/9032431.pdf'),
    ('grajewski2022.pdf', 'https://czasopisma.uni.opole.pl/index.php/ls/article/download/4818/4236/13686'),
]


def main():
    folder = ROOT / 'research/scholarship'
    folder.mkdir(exist_ok=True)
    receipt_file = folder / 'receipts.json'
    receipts = json.loads(receipt_file.read_text()) if receipt_file.exists() else []
    spent = sum(r.get('bytes_received', 0) for r in receipts)
    for filename, url in SOURCES:
        if any(r['url'] == url for r in receipts):
            continue
        receipt = dict(url=url, checked_at_utc=datetime.now(timezone.utc).isoformat(),
                       local_path=str((folder / filename).relative_to(ROOT)),
                       purpose='Private scholarly reading; no redistribution permission inferred')
        received = bytearray()
        try:
            with urlopen(url, timeout=35) as response:
                receipt.update(status=response.status, content_type=response.headers.get('Content-Type'),
                               final_url=response.url)
                while True:
                    chunk = response.read(min(65536, 20000000 - spent - len(received) + 1))
                    if not chunk:
                        break
                    received.extend(chunk)
                    if spent + len(received) > 20000000:
                        raise ValueError('Scholarly batch download cap exceeded')
            if not received.startswith(b'%PDF-'):
                raise ValueError('Response is not a PDF; no challenge or error page accepted')
            (folder / filename).write_bytes(received)
            receipt.update(sha256=hashlib.sha256(received).hexdigest(), saved=True)
        except Exception as error:
            receipt.update(error=str(error), saved=False)
        receipt['bytes_received'] = len(received)
        spent += len(received)
        receipts.append(receipt)
        receipt_file.write_text(json.dumps(receipts, ensure_ascii=False, indent=2) + '\n')
        print(json.dumps(receipt, ensure_ascii=False))


if __name__ == '__main__':
    main()
