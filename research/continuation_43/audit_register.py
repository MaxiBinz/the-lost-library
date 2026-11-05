"""Audit the entire saved register against explicit, pinned source membership."""
import collections
import hashlib
import json
from pathlib import Path
from urllib.parse import urlsplit

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]


def read(path):
    return json.loads((ROOT/path).read_text())


def save(path,value):
    (HERE/path).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')


def service_key(url):
    parts=urlsplit(url)
    # Normalize only the default HTTPS port, never case-fold object paths.
    port='' if parts.port in [None,443] and parts.scheme=='https' else (':'+str(parts.port) if parts.port else '')
    return parts.scheme+'://'+parts.hostname+port+parts.path.rstrip('/')


def main():
    protocol=read('research/continuation_43/protocol.json')
    for path,expected in protocol['inputs'].items():
        assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==expected,path
    baseline=read('research/continuation_43/lead_register.before.json')
    records=read('data/fragments.json')
    # Keep aliases explicit; do not let a duplicate catalogue record silently
    # overwrite the physical-object lookup.
    object_records=collections.defaultdict(list)
    for record in records:
        object_records[record['physical_object_id']].append(record)
    manifest_path='research/evidence/F-4ihz_manifest.json'
    manifest=read(manifest_path)
    metadata={r['label']:r['value'] for r in manifest['metadata']}
    assert metadata['Document Type']=='Virtual Reconstruction'
    services=collections.defaultdict(list)
    for sequence_index,sequence in enumerate(manifest['sequences']):
        for canvas_index,canvas in enumerate(sequence['canvases']):
            for image_index,annotation in enumerate(canvas.get('images',[])):
                resource=annotation['resource'];service=resource.get('service',{})
                if not isinstance(service,dict) or not service.get('@id'):
                    continue
                services[service_key(service['@id'])].append({
                    'canvas_id':canvas['@id'],'canvas_label':canvas.get('label'),
                    'resource_service':service['@id'],
                    'locator':f'sequences/{sequence_index}/canvases/{canvas_index}/images/{image_index}/resource/service/@id'})
    memberships=[];unmatched=[]
    for record in records:
        if record.get('collection')!='Fragmentarium / Beauvais Missal':
            continue
        image=record.get('image',{});url=image.get('url','')
        source_service=url.rsplit('/full/',1)[0]
        matches=services.get(service_key(source_service),[]) if source_service else []
        if not matches:
            unmatched.append(record['id']);continue
        memberships.append({'object_id':record['physical_object_id'],'record_id':record['id'],
            'source_record':record['source_url'],'working_image':record['image_path'],
            'working_image_sha256':image['sha256'],'working_image_url':url,
            'manifest':manifest_path,'manifest_sha256':protocol['inputs'][manifest_path],
            'reconstruction_url':'https://fragmentarium.ms/overview/F-4ihz',
            'reconstruction_id':manifest['@id'],'reconstruction_title':metadata['Title'],
            'matches':matches,'basis':'source_assertion','scope':'Membership of the source-defined virtual reconstruction; not a new independent physical attribution.',
            'independent_confirmation':False})
    member_ids={r['object_id'] for r in memberships}
    pair_rows=[];all_leads=[]
    prior_only='metadata and availability triage only'
    for lead in baseline['leads']:
        all_leads.append({'id':lead['id'],'subjects':lead['subjects'],
            'relationship_type':lead['relationship_type'],'retained_state':lead['decision_state'],
            'retained_execution':lead['test_execution'],
            'external_dependencies':lead['required_inputs'].get('dependencies',[]),
            'local_tasks':lead['required_inputs'].get('local_tasks',[]),
            'origins':lead['origins']})
        if not lead['id'].startswith('pair-'):
            continue
        ids=[s.removeprefix('object:') for s in lead['subjects']]
        source_rows=[object_records[i][0] for i in ids]
        labels=[r.get('raw',{}).get('codex') for r in source_rows]
        member=all(i in member_ids for i in ids)
        shared=labels[0] if labels[0] and labels[0]==labels[1] else None
        triage=lead['test_execution']==prior_only
        pair_rows.append({'lead_id':lead['id'],'objects':ids,
            'baseline_state':lead['decision_state'],'baseline_execution':lead['test_execution'],
            'baseline_metadata_only':triage,'both_in_published_beauvais_reconstruction':member,
            'source_credit_repair':triage and member,
            'shared_mpo_codex_label':shared,
            'shared_label_has_published_counterexample':shared=='Codex 1146',
            'available_images':lead['required_inputs']['available_primary_images'],
            'local_source_work_pending':triage and not member,
            'source_limit':'A common label does not independently prove same codex. Ant49/1146 has an explicit published different-book control.',
            'frozen_hypothesis':lead.get('frozen_hypothesis')})
    queue=read('data/hypotheses.v1.json')['hypotheses']
    reviews={r['id']:r for r in read('data/hypothesis_reviews.v1.json')['reviews']}
    frozen=[]
    for case in queue:
        review=reviews[case['id']]
        frozen.append({'id':case['id'],'objects':[case['left_id'],case['right_id']],
            'classification':review['classification'],'outcome':review['outcome'],
            'next_evidence_needed':review['next_evidence_needed'],
            'no_new_discovery':not review['new_discovery'],
            'sources':review['sources']})
    totals={'all_leads':len(all_leads),'pair_leads':len(pair_rows),
        'ranking_rows':baseline['coverage']['ranking_rows'],
        'frozen_cases':len(frozen),'verified_reconstruction_members':len(memberships),
        'unmatched_control_records':unmatched,
        'baseline_metadata_only_pairs':sum(r['baseline_metadata_only'] for r in pair_rows),
        'source_credit_repairs':sum(r['source_credit_repair'] for r in pair_rows),
        'remaining_metadata_only_pairs':sum(r['local_source_work_pending'] for r in pair_rows),
        'remaining_shared_mpo_labels':dict(collections.Counter(r['shared_mpo_codex_label'] for r in pair_rows if r['local_source_work_pending'] and r['shared_mpo_codex_label']))}
    save('memberships.json',{'version':'1.0.0','date':'2026-10-29','memberships':memberships,'unmatched':unmatched})
    save('coverage_audit.json',{'version':'1.0.0','date':'2026-10-29','grain':'One row per retained lead; pair entries are overlapping comparisons, not independent manuscripts.',
        'baseline':'research/continuation_43/lead_register.before.json','totals':totals,
        'all_leads':all_leads,'pair_audit':pair_rows,'frozen_queue':frozen,
        'coverage_limit':'This audits source-credit and retained execution metadata across the whole population. It does not turn metadata rows into primary-image tests.'})
    save('results.json',{'version':'1.0.0','date':'2026-10-29','totals':totals,
        'repair_leads':[r['lead_id'] for r in pair_rows if r['source_credit_repair']],
        'direct_result':'The register omitted published Beauvais reconstruction credit on43 metadata-only pair leads. All12 local member-image services occur in canvases of the pinned Virtual Reconstruction manifest. These43 pairs are already source-defined controls, not new discoveries.',
        'scope':'Internal source/provenance correction, not a correction to the scholarly record, a new codex attribution, image validation or improved matcher.',
        'ant49_limit':'Fourteen remaining metadata-only pairs share Codex1146. They remain unresolved: the8201–8304 rejection demonstrates why the common catalogue label cannot be promoted to physical identity.',
        'completion_audit':'Not complete. Fifty pair leads still have metadata/availability triage only and have local images. The frozen cases remain2E/7C/1D; original scholarship and specific Finnish comparators remain missing. No rigorous exhausted-queue negative conclusion or discovery success is established.',
        'next_test':{'target':['mpo-8066','mpo-9620'],
            'reason':'Existing Ant49 audit lead and retained pair; both catalogue records concern Dedication, but9620 is described as hymns. No new target family is introduced.',
            'question':'Do their original visible sequences occupy the same liturgical opening/address, or different sections/genres? Test any proposed conflict against book-function/composite alternatives and preserve the8201–8304 negative control.',
            'execution':'Pending source inspection, not counted as completed research.'},
        'goal_complete':False,'global_blocker_established':False,
        'new_discovery':False,'independent_confirmation':False,
        'frozen_core_inputs_unchanged':True})
    print(json.dumps(totals,indent=2))


if __name__=='__main__':
    main()
