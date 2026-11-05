"""Check E55 provenance, deterministic geometry and limits; no pitch authority."""
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile

from PIL import Image

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]


def read(path):
    return json.loads((ROOT/path).read_text())


def main():
    p=read('research/continuation_55/protocol.json')
    for path,sha in p['frozen_inputs'].items():
        assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==sha,path
    snap=p['register_before_overlay']
    assert hashlib.sha256((ROOT/snap['path']).read_bytes()).hexdigest()==snap['sha256']
    for s in p['sources']+[p['supplementary_native_recheck']]:
        assert hashlib.sha256((ROOT/s['path']).read_bytes()).hexdigest()==s['sha256']
        with Image.open(ROOT/s['path']) as im:assert im.size==(s['width'],s['height'])
    for s in p['sources']:
        assert s['url'] and s['attribution']
        assert s['rights_url'].removeprefix('https://').removeprefix('http://')=='creativecommons.org/publicdomain/mark/1.0/'
    private=ROOT/p['reference_pdf']['path']
    if private.exists():
        assert hashlib.sha256(private.read_bytes()).hexdigest()==p['reference_pdf']['sha256']
    # Recompute in scratch space. Do not mutate the retained output or core data.
    spec=importlib.util.spec_from_file_location('e55_calibration',HERE/'calibrate_staff.py')
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    retained=read('research/continuation_55/staff_calibration.json')
    with tempfile.TemporaryDirectory(prefix='e55-check-') as temp:
        mod.main(Path(temp))
        assert json.loads((Path(temp)/'staff_calibration.json').read_text())==retained
        assert hashlib.sha256((Path(temp)/'staff-review.png').read_bytes()).hexdigest()==hashlib.sha256((HERE/'staff-review.png').read_bytes()).hexdigest()
    prior=read('research/continuation_39/readings.v3.json')
    assert len(retained['notes'])==28
    for n in retained['notes']:
        old=prior['sources'][n['source']]['phrases'][n['phrase']][n['slot']-1]
        assert n['original_anchor']==old['pixel'] and n['e39_relative_alternatives']==old['relative_staff_steps']
        assert not n['sounding_pitch_adjudicated']
    assert sum(m['valid'] for w in retained['windows'].values() for m in w['models'])==8
    target_upper=[n for n in retained['notes'] if n['source']=='target' and n['slot']==4]
    assert len(target_upper)==2 and all(n['geometric_relative_alternatives']==[3,4] for n in target_upper)
    assert all(not m['valid'] for m in retained['windows']['c23:nobis-vite-spem']['models'])
    spem=[n for n in retained['notes'] if n['source']=='target' and n['phrase']=='nobis-vite-spem' and n['slot'] in [6,7]]
    assert all(n['geometric_relative_alternatives']==[1,2] for n in spem)
    result=read('research/continuation_55/results.json')
    assert result['valid_rule_models']==8 and result['candidate_rule_models']==12
    assert result['retained_head_anchors']==28 and result['declared_alignment_slots']==14
    for key in ['two_target_events_resolved','complete_rule_calibration_succeeded','exact_pitches_verified',
                'robust_melodic_variant_established','melodic_identity_established','new_codex_attribution',
                'new_discovery','novelty_cleared','independent_confirmation','goal_complete','global_blocker_established']:
        assert result[key] is False,key
    assert result['new_source_files']==result['new_source_regions']==result['new_download_bytes']==0
    before={r['id']:r for r in read(snap['path'])['leads']}
    live={r['id']:r for r in read('data/lead_register.v1.json')['leads']}
    audit=read('research/continuation_55/remaining_leads.json')
    assert len(before)==len(live)==len(audit['leads'])==168
    assert set(before)==set(live)=={r['id'] for r in audit['leads']}
    assert all(before[i]['decision_state']==live[i]['decision_state'] for i in before)
    assert audit['decision_states']['unresolved']==sum(r['decision_state']=='unresolved' for r in audit['leads'])==72
    assert audit['first_comparisons_pending']==0 and not any(r.get('primary_pair_test_pending') for r in live.values())
    for r in audit['leads']:
        for paths in r['available_local_sources'].values():
            assert all((ROOT/path).is_file() for path in paths)
        if r['decision_state']=='unresolved':assert r['historical_test_exhaustion_established'] is False
    graph=read('data/knowledge.v1.json')
    evidence={r['annotation_id'] for r in graph['evidence']}
    assert set(result['source_regions_reused'])<=evidence
    c=next(c for c in graph['claims'] if c['id']=='observation:E55-calibration')
    assert c['basis']=='project_observation' and c['scope'].endswith('not established musical pitches')
    assert not c['two_target_events_resolved'] and not c['exact_pitches_verified']
    for ident in ['E37-ending','E38-replacement-text','E39-excerpt']:
        assert 'E55 performs' in live[ident]['test_execution']
        assert not live[ident]['staff_calibration_followup']['two_target_events_resolved']
    resource=read('data/resource_audit.json')
    assert result['working_source_files_after']==208
    assert resource['working_source_capture_files']==208+len(read('research/continuation_65/captures.json')['captures'])
    assert result['conservative_transfer_plan_after']==1675854139
    assert resource['conservative_planning_total_bytes']==1675854139+resource['receipt_subtotals']['research/continuation_56/metadata_receipts.json']+resource['receipt_subtotals']['research/continuation_56/download_receipts.json']+resource['receipt_subtotals']['research/continuation_65/download_receipt.json']+resource['receipt_subtotals']['research/continuation_88/supplement_receipt.json']+resource['receipt_subtotals']['research/continuation_114/download_receipt.json']
    print(json.dumps(dict(geometry_recomputed=True,fixed_anchors_checked=28,unresolved_target_upper_events=2,
        audited_entries=168,unresolved_entries=72,new_source_files=0,historical_decisions='unchanged',
        private_reference_pdf_included_in_this_copy=private.exists(),independent_pitch_verification=False)))


if __name__=='__main__':
    main()
