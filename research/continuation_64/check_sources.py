"""Check local inputs and claim boundaries, not live-source interpretation."""
import csv,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def read(p):return json.loads((ROOT/p).read_text())
def main():
 source=read('research/continuation_64/sources.json'); result=read('research/continuation_64/results.json')
 baseline=read('research/continuation_64/decisions.before.json')['states']
 register=read('data/lead_register.v1.json'); leads={l['id']:l for l in register['leads']}
 assert {k:v['decision_state'] for k,v in leads.items()}==baseline
 prior=read('research/continuation_49/sources.json')['missing_positive_record']
 raw=ROOT/prior['source']; assert hashlib.sha256(raw.read_bytes()).hexdigest()==prior['sha256']
 with raw.open(encoding='utf-8-sig',newline='') as f: rows=[r for r in csv.DictReader(f) if r['signatur']=='20106']
 assert len(rows)==1 and all(rows[0][k]==v for k,v in prior['source_values'].items())
 for key in ['exact_fr20106_crosswalk','current_holding_verified','image_pointer_verified','same_book_newly_proved','new_historical_discovery','independent_confirmation']:
  assert result[key] is False
 assert result['new_source_images']==result['new_download_bytes']==0
 assert len(source['failed_routes'])==3 and 'repeated' in source['failed_routes'][0]['outcome']
 graph=read('data/knowledge.v1.json'); claims={c['id']:c for c in graph['claims']}
 c=claims['source:E64-A103-deposit']; assert c['status']=='unresolved' and c['predicate']=='suggested_association'
 assert all(c[k] is False for k in ['direct_fr20106_collection_assertion','current_holding_verified','image_pointer_verified','new_discovery','independent_confirmation'])
 assert all('Fr 20106' in leads[i]['strongest_feasible_test'] for i in ['ant49-audit','pair-1b35a032653fb22b9e36','pair-bef99c0c6dd2ef1ff931'])
 entity=next(e for e in graph['entities'] if e['id']=='record:manuscripta-101111')
 assert entity['physical_object'] is None and entity['crosswalk_status']=='unresolved'
 print(json.dumps({'source_rows':1,'lead_decisions':'unchanged','current_holding':'unverified','crosswalk':'unresolved','failed_route_repeat_disclosed':True}))
if __name__=='__main__':main()
