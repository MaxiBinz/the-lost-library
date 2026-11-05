"""Extract existing Ant 49 catalogue rows without interpreting missing descriptions."""
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def main():
    source = ROOT / 'research/mpo.csv'
    with source.open(encoding='utf-8-sig', newline='') as f:
        rows = [r for r in csv.DictReader(f) if r.get('ccmsignum', '').strip() == 'Ant 49']
    rows.sort(key=lambda r: int(r['signatur']))
    result = {
        'source': 'research/mpo.csv',
        'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
        'selection': 'ccmsignum exactly Ant 49 after trimming',
        'rows': [{k: r.get(k, '') for k in ('signatur', 'ccmsignum', 'codex', 'inhalt', 'bildbetrachter')} for r in rows],
        'interpretation_limit': 'Catalogue descriptions are not full transcriptions; blank or different contents do not establish absence or a different book.'
    }
    (ROOT / 'research/continuation_76/candidate_rows.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'rows': len(rows), 'signatures': [r['signatur'] for r in rows]}))

if __name__ == '__main__':
    main()
