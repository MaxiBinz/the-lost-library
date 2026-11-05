"""Index every existing lead's recorded status and actual local source inputs.

This inventory does not infer that an unresolved historical test is exhausted.
It exposes repeated/general tasks and concrete source gaps for the next test.
"""
from collections import Counter
import hashlib
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]


def read(path):
    return json.loads((ROOT/path).read_text())


def main():
    before=read('research/continuation_55/lead_register.before.json')
    records=read('data/fragments.json')+read('data/comparison_sources.v1.json')
    available={}
    for r in records:
        ident=r.get('physical_object_id',r['id'])
        paths=[r.get('image_path')]+[c.get('path') for c in r.get('captures',[])]
        if r.get('original_source'):paths.append(r['original_source']['path'])
        available.setdefault(ident,set()).update(p for p in paths if p and (ROOT/p).is_file())
        available.setdefault(r['id'],set()).update(available[ident])
    for n in [44,50,52,54]:
        for c in read(f'research/continuation_{n}/captures.json')['captures']:
            assert (ROOT/c['path']).is_file()
            available.setdefault(c['physical_object_id'],set()).add(c['path'])
    ant49={'mpo-'+i for i in ['8066','8072','8073','8201','8304','9620']}
    objects={r['id']:r for r in records}
    rows=[]
    for lead in before['leads']:
        ids=[s.removeprefix('object:') for s in lead['subjects']]
        if lead['id'].startswith('pair-'):
            if len(ids)==2 and set(ids)<=ant49:
                family='Ant49'
                requirement='A securely corresponding complete work/variant or original physical discriminator; generic five-rule/broad-field similarity is already non-specific. Full published negative-control replication separately needs20106.'
            elif any(i.startswith('finn-') or i.startswith('fm-') for i in ids):
                family='Finnish attribution comparisons'
                requirement='Exact source-described relationship and appropriate original source/side correspondence. Existing Finnish173 images do not replace missing156/157 originals or the cited scholarship.'
            elif any(i in {'mpo-25592','mpo-10349'} for i in ids):
                family='Hy49 /10349 comparisons'
                requirement='A demonstrably corresponding diagnostic work or physical feature. E53 selected Jesu openings probably concern different known hymns; layout/section differences alone leave composite-volume alternatives.'
            else:
                family='Other stored pair comparisons'
                requirement='A source-specific diagnostic text/physical feature and original-side/address convention. E54 clipped1385 marks cannot be recovered through another scaling of the same photograph.'
        else:
            family='Context / auxiliary / named association'
            requirement=lead['strongest_feasible_test']
        current_inputs={i:sorted(available.get(i,set())) for i in ids if i in available or i in objects}
        rows.append(dict(id=lead['id'],title=lead['title'],family=family,
            decision_state=lead['decision_state'],relationship_type=lead['relationship_type'],
            first_comparison_pending=bool(lead.get('primary_pair_test_pending')),
            existing_test=lead.get('test_execution'),recorded_next_test=lead['strongest_feasible_test'],
            remaining_requirement=requirement,
            recorded_dependencies=lead['required_inputs'].get('dependencies',[]),
            recorded_local_tasks=lead['required_inputs'].get('local_tasks',[]),
            available_local_sources=current_inputs,
            input_inventory_scope='File presence only; not a diplomatic edition, source-photo completeness, side map or availability beyond the checked local store.',
            historical_test_exhaustion_established=False if lead['decision_state']=='unresolved' else None))
    out=dict(version='1.0.0',date='2026-10-31',source_register='research/continuation_55/lead_register.before.json',
        total_existing_entries=len(rows),decision_states=dict(Counter(r['decision_state'] for r in rows)),
        unresolved_by_family=dict(Counter(r['family'] for r in rows if r['decision_state']=='unresolved')),
        first_comparisons_pending=sum(r['first_comparison_pending'] for r in rows),leads=rows,
        priorities=[
            dict(id='turku-ms-c',action='Reconcile the museum/archive holder and defective-bifolium/one-folio descriptions through exact public institutional/catalogue evidence. No existing image pointer or physical identity has been verified.',feasibility='Public-source identity investigation remains meaningful; do not retry failed Finnish page routes.'),
            dict(id='fr8311-chant',action='Compare the retained literal paradise/Adam responsory and following verse with exact primary Cantus concordances006537/006537a. Keep the known chant identification separate from a codex discriminator.',feasibility='Four local photos available; the exact full chant/melody is not already established by an opening-word match.'),
            dict(id='E39-excerpt',action='E55 completes the bounded local staff-calibration test without resolving the two target upper events. Reopen only on a documented sign/anchor interpretation or genuinely better primary detail; no threshold search to force agreement.',feasibility='Current local geometric test is complete; this does not exhaust all palaeographic research or establish a melody.'),
        ],
        completion_assessment='Discovery and exhausted-negative outcomes remain unproven. The inventory identifies meaningful named tasks and specific missing inputs; it is not a source-based adjudication of every historical relation.',
        global_blocker_established=False)
    (HERE/'remaining_leads.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k in ['total_existing_entries','decision_states','unresolved_by_family','first_comparisons_pending','completion_assessment']}))


if __name__=='__main__':
    main()
