"""Independent literal-cell and state-transition checks; no historical verdict."""
import collections
import csv
import hashlib
import importlib.util
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]


def read(path):
    return json.loads((ROOT/path).read_text())


def main():
    protocol=read('research/continuation_48/protocol.json')
    for path,expected in {**protocol['source_inputs'],**protocol['frozen_inputs']}.items():
        assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==expected,path
    spec=importlib.util.spec_from_file_location('e47_xml',ROOT/'research/continuation_47/check_sources.py')
    xml=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(xml)
    source=read('research/continuation_48/source_rows.json')
    checked_units=0
    for name,unit_col,key in [('combined','M','Fr_reference'),('raw','F','fragment_id')]:
        src=source[name]
        columns={''.join(c for c in address if c.isalpha()):field
            for field,address in src['rows'][0]['cells'].items()}
        target_col='C' if name=='combined' else 'D'
        ids={r['values'][key] for r in src['rows']}
        actual,targets=xml.xml_unit_rows(src['path'],src['sheet'],set(src['units']),unit_col,
            set(columns),target_col,ids)
        headers=dict(actual)[2]
        assert all(headers[c]==field for c,field in columns.items())
        assert len(targets)==len(ids)==23
        by={n:v for n,v in targets}
        assert len(by)==23
        for row in src['rows']:
            values=by[row['excel_row']]
            assert {field:values.get(c) for c,field in columns.items()}==row['values']
        for unit,expected in src['units'].items():
            rows=[(n,r) for n,r in actual if n!=2 and r.get(unit_col)==unit]
            assert [{'excel_row':n,'identifier':r.get(target_col),
                'row_exclusion':r.get(next(c for c,k in columns.items() if k=='Row_exclusion'))} for n,r in rows]==expected
            checked_units+=len(rows)
    result=read('research/continuation_48/results.json')
    audit=result['pair_audit']
    before={l['id']:l for l in read('research/continuation_48/lead_register.before.json')['leads']}
    live_register=read('data/lead_register.v1.json')
    snapshot='research/continuation_50/lead_register.before.json'
    if (ROOT/snapshot).exists():
        pinned=read('research/continuation_50/primary_protocol.json')['register_before_overlay']
        assert hashlib.sha256((ROOT/snapshot).read_bytes()).hexdigest()==pinned['sha256']
        current=read(snapshot)
    else:
        current=live_register
    now={l['id']:l for l in current['leads']}
    assert before.keys()==now.keys() and len(now)==168
    ids={l['id'] for l in before.values() if l['test_execution']=='metadata and availability triage only'}
    assert ids=={a['lead_id'] for a in audit} and len(ids)==36
    repairs=set(result['repair_leads'])
    assert len(repairs)==5
    assert {k for k in before if before[k]['decision_state']!=now[k]['decision_state']}==repairs
    pending={a['lead_id'] for a in audit if a['primary_pair_test_pending']}
    assert len(pending)==31 and pending==set(result['pending_primary_leads'])
    assert {k for k,l in now.items() if l.get('primary_pair_test_pending')}==pending
    live_pending={l['id'] for l in live_register['leads'] if l.get('primary_pair_test_pending')}
    assert live_pending<=pending
    for ident in repairs:
        live=next(l for l in live_register['leads'] if l['id']==ident)
        assert live['decision_state']=='previously_documented' and not live['independent_confirmation']
    for a in audit:
        live=now[a['lead_id']]
        assert live['decision_state']==a['decision_state'] and not live['independent_confirmation']
        if a['category']=='contested_shared_unit':
            assert live['decision_state']=='unresolved' and a['combined_units']==['BOMPAC-4861']*2
    graph=read('data/knowledge.v1.json')
    members=[c for c in graph['claims'] if c['id'].startswith('assignment:mpo-') and c['id'].endswith(':E48-bompac')]
    assert len(members)==23
    assert all(c['basis']=='source_assertion' and c['predicate']=='assigned_to_reconstruction' and not c['independent_confirmation'] for c in members)
    contested=next(c for c in graph['claims'] if c['id']=='interpretation:E48-unit4861')
    assert contested['status']=='unresolved' and contested['source_stance']=='suggested'
    assert contested['basis']=='researcher_interpretation' and contested['derived_from_source_assignments']
    rejection=next(c for c in graph['claims'] if c['id']==contested['competing_source_claim'])
    assert rejection['source_stance']=='rejected' and rejection['predicate']=='same_codex'
    assert contested['subject']==rejection['subject'] and contested['object']==rejection['object']
    frozen=next(l for l in current['leads'] if l.get('frozen_hypothesis')=='H06')
    assert frozen['decision_state']=='contradicted'
    assert not any(result[k] for k in ['new_discovery','independent_confirmation','goal_complete','global_blocker_established'])
    with (ROOT/'research/mpo.csv').open(encoding='utf-8-sig') as handle:
        positive=[r for r in csv.DictReader(handle) if r['signatur']=='20106']
    assert len(positive)==1 and positive[0]['institution']=='KB'
    assert positive[0]['bestandsbezeichnung'].replace(' ','')=='A103'
    assert not positive[0]['iiif_manifest'] and not positive[0]['bildbetrachter']
    reading_sources=read('research/continuation_48/sources.json')['local_sources']
    missing=[]
    for src in reading_sources:
        path=ROOT/src['path']
        if path.exists():
            assert hashlib.sha256(path.read_bytes()).hexdigest()==src['sha256']
        else:
            missing.append(src['path'])
    print(json.dumps({'literal_target_rows_checked':46,'source_unit_rows_checked':checked_units,
        'audited_pairs':36,'documented_source_credit_repairs':5,'historical_primary_pair_tests_pending':31,
        'current_primary_pair_tests_pending':len(live_pending),
        'competing_unit_assertion_and_published_rejection_preserved':True,
        'private_reading_sources_absent_from_this_copy':missing,
        'scope':'Independent ZIP/XML extraction and state checks, not historical adjudication or novelty clearance.'}))


if __name__=='__main__':
    main()
