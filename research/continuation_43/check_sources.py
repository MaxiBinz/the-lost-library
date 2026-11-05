"""Check the source join and full-population accounting without new access."""
import hashlib
import json
from pathlib import Path
from urllib.parse import urlsplit

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]


def read(path):
    return json.loads((ROOT/path).read_text())


def main():
    protocol=read('research/continuation_43/protocol.json')
    for path,expected in protocol['inputs'].items():
        assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==expected,path
    audit=read('research/continuation_43/coverage_audit.json')
    baseline=read('research/continuation_43/lead_register.before.json')
    memberships=read('research/continuation_43/memberships.json')['memberships']
    manifest=read('research/evidence/F-4ihz_manifest.json')
    records={r['id']:r for r in read('data/fragments.json')}
    assert {r['id'] for r in audit['all_leads']}=={r['id'] for r in baseline['leads']}
    assert {r['lead_id'] for r in audit['pair_audit']}=={r['id'] for r in baseline['leads'] if r['id'].startswith('pair-')}
    assert len(audit['all_leads'])==168 and len(audit['pair_audit'])==117
    for member in memberships:
        r=records[member['record_id']]
        assert member['object_id']==r['physical_object_id']
        assert hashlib.sha256((ROOT/member['working_image']).read_bytes()).hexdigest()==member['working_image_sha256']
        assert member['working_image_url']==r['image']['url']
        for match in member['matches']:
            value=manifest
            for key in match['locator'].split('/'):
                value=value[int(key)] if isinstance(value,list) else value[key]
            assert value==match['resource_service']
            source=urlsplit(value);working=urlsplit(member['working_image_url'])
            assert source.scheme==working.scheme and source.hostname==working.hostname
            assert working.path.startswith(source.path.rstrip('/')+'/full/')
        assert not member['independent_confirmation']
    result=read('research/continuation_43/results.json')
    assert len(result['repair_leads'])==43 and len(set(result['repair_leads']))==43
    assert result['totals']['baseline_metadata_only_pairs']==93
    assert result['totals']['remaining_metadata_only_pairs']==50
    assert len(audit['frozen_queue'])==10
    assert {r['classification'] for r in audit['frozen_queue']}=={'C','D','E'}
    assert not any(result[k] for k in ['goal_complete','global_blocker_established','new_discovery','independent_confirmation'])
    current=read('data/lead_register.v1.json')
    by={r['id']:r for r in current['leads']}
    for ident in result['repair_leads']:
        row=by[ident]
        assert row['decision_state']=='previously_documented'
        assert row['test_execution']=='published reconstruction source audit; no new pair-level image transcription'
        assert not row['independent_confirmation']
    # E43's historical remainder is50. Later source tests can legitimately
    # reduce it, so never freeze the live register at an unfinished state.
    expected_remainder={r['lead_id'] for r in audit['pair_audit'] if r['local_source_work_pending']}
    current_remainder={r['id'] for r in current['leads'] if r['test_execution']=='metadata and availability triage only'}
    assert len(expected_remainder)==50 and current_remainder<=expected_remainder
    negative=next(r for r in current['leads'] if r.get('frozen_hypothesis')=='H06')
    assert negative['decision_state']=='contradicted'
    print(json.dumps({'all_leads_accounted_for':168,'pair_leads_accounted_for':117,
        'source_memberships_checked':len(memberships),'source_credit_repairs_checked':43,
        'e43_remaining_metadata_only_pairs':50,'current_metadata_only_pairs':len(current_remainder),'frozen_core_inputs_unchanged':True,
        'scope':'Exact source-service membership and register accounting only; no new historical attribution, primary pair reading, independent confirmation or full goal-completion proof.'}))


if __name__=='__main__':
    main()
