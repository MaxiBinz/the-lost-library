"""Acquire three exact public Zenodo v1.1 files once, with publisher checksums."""
import hashlib
import json
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).parent
META = json.loads((ROOT / 'research/continuation_51/raw-latest.json').read_text())
NAMES = {'FM_Frs_BOMPAC.csv', 'Readme-FM-frs-BOMPAC.pdf', 'Bailiffs_Records_and_Covers.csv'}


def main():
    if (HERE / 'download_receipts.json').exists():
        raise SystemExit('Refusing to repeat an acquisition with an existing receipt')
    files = [f for f in META['files'] if f['key'] in NAMES]
    assert len(files) == len(NAMES)
    receipts = []
    for f in files:
        target = HERE / f['key']
        if target.exists():
            raise SystemExit(f'Refusing to reacquire existing file: {target.name}')
        entry = {'key': f['key'], 'url': f['links']['self'], 'expected_size': f['size'],
                 'expected_checksum': f['checksum'], 'saved': None, 'error': None}
        try:
            req = Request(f['links']['self'], headers={'User-Agent': 'LostLibrary-research/1.0'})
            with urlopen(req, timeout=35) as response:
                payload = response.read(f['size'] + 1)
                entry['http_status'] = response.status
            entry['bytes'] = len(payload)
            entry['md5'] = hashlib.md5(payload).hexdigest()
            entry['sha256'] = hashlib.sha256(payload).hexdigest()
            if len(payload) != f['size'] or 'md5:' + entry['md5'] != f['checksum']:
                raise ValueError('Publisher size/checksum mismatch; content not saved')
            target.write_bytes(payload)
            entry['saved'] = str(target.relative_to(ROOT))
        except Exception as exc:
            entry['error'] = f'{type(exc).__name__}: {exc}'
        receipts.append(entry)
        (HERE / 'download_receipts.json').write_text(json.dumps(receipts, indent=2) + '\n')
        print(json.dumps(entry, ensure_ascii=False))


if __name__ == '__main__':
    main()
