"""Verify retained TEI, access receipts and the scoped catalogue crosswalk."""
import hashlib
import json
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
def read(path):return json.loads((ROOT/path).read_text())

def main():
    p=read('research/continuation_56/protocol.json')
    for path,sha in p['frozen_inputs'].items():assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==sha,path
    snap=p['register_before_overlay'];assert hashlib.sha256((ROOT/snap['path']).read_bytes()).hexdigest()==snap['sha256']
    r=read('research/continuation_56/results.json');tei=ROOT/r['metadata_file']
    assert tei.stat().st_size==r['metadata_bytes']==6702
    assert hashlib.sha256(tei.read_bytes()).hexdigest()==r['metadata_sha256']
    root=ET.parse(tei).getroot();txt=' '.join(' '.join(root.itertext()).split())
    assert '2 folios.' in txt and 'F.m. II.157' in txt and 'Keskiaho' in txt
    meta=read('research/continuation_56/metadata_receipts.json');assert len(meta)==1 and meta[0]['sha256']==r['metadata_sha256'] and meta[0]['bytes_received']==6702
    attempts=read('research/continuation_56/download_receipts.json');assert len(attempts)==2
    assert all(not x['saved'] and not x['retry'] and x['bytes_received']==0 and 'CERTIFICATE_VERIFY_FAILED' in x['error'] for x in attempts)
    assert not read('research/continuation_56/captures.json')['captures']
    assert all(not r[k] for k in ['new_codex_attribution','historical_placement_verified','catalogue_emendation_confirmed','new_discovery','independent_confirmation','goal_complete'])
    old={x['id']:x for x in read(snap['path'])['leads']};live={x['id']:x for x in read('data/lead_register.v1.json')['leads']}
    assert old.keys()==live.keys() and all(old[k]['decision_state']==live[k]['decision_state'] for k in old)
    assert live['turku-ms-c']['decision_state']=='unresolved' and live['turku-ms-c']['test_execution'].startswith('E56')
    claims={x['id']:x for x in read('data/knowledge.v1.json')['claims']}
    assert claims['assertion:E56-printed-reference']['basis']=='source_assertion'
    assert not claims['interpretation:E56-reference']['catalogue_emendation_confirmed']
    a=read('data/resource_audit.json'); later=read('research/continuation_65/captures.json')['captures']; assert a['working_source_capture_files']==208+len(later) and a['conservative_planning_total_bytes']==1675860841+a['receipt_subtotals']['research/continuation_65/download_receipt.json']+a['receipt_subtotals']['research/continuation_88/supplement_receipt.json']+a['receipt_subtotals']['research/continuation_114/download_receipt.json']
    print(json.dumps({'tei_verified':True,'metadata_bytes':6702,'failed_tiff_attempts':2,'new_images':0,'historical_decisions':'unchanged','new_discovery':False}))

if __name__=='__main__':main()
