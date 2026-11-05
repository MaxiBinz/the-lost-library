"""Offline E37 provenance checks. Readings and historical claims need inspection."""
import argparse
import hashlib
import json
from pathlib import Path

from PIL import Image

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent


def sha(path):
    with path.open('rb') as stream:return hashlib.file_digest(stream,'sha256').hexdigest()


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--require-private',action='store_true',help='Require the two locally retained copyrighted reading PDFs; they are excluded from the review archive.')
    args=parser.parse_args()
    result=json.loads((HERE/'results.json').read_text())
    observations=json.loads((HERE/'observations.json').read_text())['annotations']
    expected=set(result['target_observations']+result['comparison_observations'])
    assert expected=={a['id'] for a in observations}
    for a in observations:
        path=ROOT/a['target']['source']
        assert sha(path)==a['sha256']
        with Image.open(path) as im:
            assert list(im.size)==a['image_dimensions']
            x,y,w,h=map(int,a['target']['selector']['value'][5:].split(','))
            assert 0<=x<x+w<=im.width and 0<=y<y+h<=im.height
    receipts=json.loads((HERE/'download_receipts.json').read_text())
    saved=[r for r in receipts if r.get('saved')]
    assert len(saved)==1 and saved[0]['bytes_received']==result['new_download_bytes']
    assert saved[0]['md5']==saved[0]['expected_md5']=='1f0193e4c997d3a94e060d804a38aeda'
    checked=[];missing=[]
    for source in result['previously_published'].values():
        path=ROOT/source['private_pdf']
        if path.exists():
            assert sha(path)==source['sha256'];checked.append(source['private_pdf'])
        else:missing.append(source['private_pdf'])
    if args.require_private:assert not missing,missing
    frozen=json.loads((ROOT/'research/continuation_33/results.json').read_text())['frozen_inputs']
    assert frozen=={p:sha(ROOT/p) for p in frozen}
    assert not result['whole_office_recension_established'] and not result['new_codex_attribution']
    assert not result['novelty_cleared'] and not result['independent_confirmation']
    assert sum(r['state']=='supported' for r in result['diagnostic_coverage'])==1
    print(json.dumps({'verified_regions':len(observations),'frozen_inputs_unchanged':True,
          'private_pdf_hashes_checked':checked,'private_pdfs_missing_in_this_copy':missing,
          'scope':result['scope'],'limits':'Verifies provenance and declared scope, not reading truth or novelty.'}))


if __name__=='__main__':main()
