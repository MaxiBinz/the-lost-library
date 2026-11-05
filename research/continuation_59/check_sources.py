"""Verify recorded source scope and state integrity, not the Finnish translation."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[2]
def read(p):return json.loads((ROOT/p).read_text())
def main():
    result=read('research/continuation_59/results.json'); sources=read(result['source'])
    ch=sources['chapter']
    assert ch['year']==2025 and ch['pages']=='183–221' and ch['doi']=='10.21435/ht.294'
    for k in ['primary_f9_inspected','published_figure_visually_inspected','scholarship_independently_verified','new_book_attribution','new_discovery']:assert result[k] is False
    assert result['new_source_images']==result['new_download_bytes']==0
    before=read('research/continuation_59/decisions.before.json')['decision_states']
    after={x['id']:x['decision_state'] for x in read('data/lead_register.v1.json')['leads']}
    assert before==after and after['iv156-1505']=='unresolved' and after['E40-boundary']=='unresolved'
    g=read('data/knowledge.v1.json')
    assert any(c['id']=='published:E59-iv156-use' and c['basis']=='source_assertion' and c['status']=='previously_documented' for c in g['claims'])
    for p,sha in g['frozen_inputs'].items(): assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==sha
    assert '10.21435/ht.294' in (ROOT/'research/bibliography.ris').read_text()
    print(json.dumps({'chapter':'2025 prior art','decisions':'unchanged','f9_inspected':False,'new_discovery':False}))
if __name__=='__main__':main()
