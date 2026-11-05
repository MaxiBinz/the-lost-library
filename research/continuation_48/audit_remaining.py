"""Exact published-source assignment audit of the fixed36 remaining pair leads."""
import collections
import hashlib
import json
from pathlib import Path

from openpyxl import load_workbook
from openpyxl.utils import get_column_letter

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
COMBINED = 'research/continuation_26/bompac/Stockholm-Helsinki-Frs-Combined-BOMPAC.xlsx'
RAW = 'research/continuation_26/bompac/raw_metadata/MPO_BOMPAC.xlsx'


def read(path):
    return json.loads((ROOT/path).read_text())


def save(name, value):
    (HERE/name).write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n')


def extract(path, sheet, key, targets, unit):
    wb = load_workbook(ROOT/path, read_only=True, data_only=True)
    ws = wb[sheet]
    rows = ws.iter_rows(values_only=True)
    next(rows)
    headers = list(next(rows))
    wanted = [key, unit, 'Row_exclusion', 'Exclusion_criteria']
    wanted += (['Database_or_institution', 'Frs_per_unit', 'Fr_in_unit', 'FM_signum_BOMPAC',
        'CCM_signum_BOMPAC', 'Codex_signum_BOMPAC', 'Identification_comment',
        'Dating_BOMPAC', 'Dating_BOMPAC_conflict', 'Origin_BOMPAC_conflict'] if sheet=='Sheet1'
        else ['unit_NB_HK', 'frs_per_unit_HK', 'fr_in_unit_IDX_HK', 'ccmsignum_HK', 'codex_HK',
        'ccmsignum_HK_ambivalence-MPO', 'codex_HK_ambivalence-MPO',
        'ccmsignum_HK_ambivalence-HK', 'codex_HK_ambivalence-HK',
        'ccmsignum_HK_correction_log', 'codex_HK_correction_log', 'signum_comments_HK', 'general_notes_HK'])
    assert all(headers.count(k)==1 for k in wanted)
    selected = []
    membership = collections.defaultdict(list)
    for n, row in enumerate(rows, 3):
        d = dict(zip(headers, row))
        if d.get(unit):
            membership[d[unit]].append({'excel_row':n, 'identifier':d.get(key),
                'row_exclusion':d.get('Row_exclusion')})
        if d.get(key) in targets:
            selected.append({'excel_row':n, 'values':{k:d.get(k) for k in wanted},
                'cells':{k:f'{get_column_letter(headers.index(k)+1)}{n}' for k in wanted}})
    counts = collections.Counter(r['values'][key] for r in selected)
    assert set(counts)==targets and all(v==1 for v in counts.values())
    selected_units = {r['values'][unit] for r in selected}
    assert None not in selected_units
    result = {'path':path, 'sheet':sheet, 'sha256':hashlib.sha256((ROOT/path).read_bytes()).hexdigest(),
        'headers_row':2, 'source_dimensions':[ws.max_row,ws.max_column], 'rows':selected,
        'target_match_counts':{str(k):v for k,v in sorted(counts.items())},
        'units':{k:membership[k] for k in sorted(selected_units)}}
    wb.close()
    return result


def main():
    protocol = read('research/continuation_48/protocol.json')
    for path, expected in {**protocol['source_inputs'],**protocol['frozen_inputs']}.items():
        assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==expected, path
    baseline = read('research/continuation_48/lead_register.before.json')
    leads = [r for r in baseline['leads'] if r['id'] in protocol['selection']['lead_ids']]
    ids = {int(s[4:]) for s in protocol['selection']['physical_objects'] if s.startswith('mpo-')}
    assert len(leads)==36 and len(ids)==23
    c = extract(COMBINED,'Sheet1','Fr_reference',{'Fr '+str(i) for i in ids},'BOMPAC-reconstruction')
    r = extract(RAW,'Blad1','fragment_id',ids,'unit_HK')
    combined = {'mpo-'+row['values']['Fr_reference'].removeprefix('Fr '):row for row in c['rows']}
    raw = {'mpo-'+str(row['values']['fragment_id']):row for row in r['rows']}
    assert all(row['values']['Row_exclusion']=='Include row' for row in c['rows'])
    negative_objects = ['mpo-8201','mpo-8304']
    contested_units = {combined[i]['values']['BOMPAC-reconstruction'] for i in negative_objects}
    assert len(contested_units)==1 and contested_units=={'BOMPAC-4861'}
    audit = []
    for lead in leads:
        objects = [s.removeprefix('object:') for s in lead['subjects']]
        rows = [combined.get(o) for o in objects]
        units = [row['values']['BOMPAC-reconstruction'] if row else None for row in rows]
        available = all(row is not None for row in rows)
        same = available and units[0]==units[1]
        contested = same and units[0] in contested_units
        category = ('contested_shared_unit' if contested else 'documented_shared_unit') if same else ('different_units' if available else 'outside_workbook_crosswalk')
        audit.append({'lead_id':lead['id'], 'objects':objects, 'combined_units':units,
            'raw_units':[raw[o]['values']['unit_HK'] if o in raw else None for o in objects],
            'category':category, 'source_credit_repair':same and not contested,
            'decision_state':'previously_documented' if same and not contested else 'unresolved',
            'primary_pair_test_pending':not (same and not contested),
            'scope':'Source assignment audit only; no new primary pair reading or physical identity proof.'})
    categories = dict(collections.Counter(row['category'] for row in audit))
    assert categories=={'outside_workbook_crosswalk':2,'different_units':16,
        'documented_shared_unit':5,'contested_shared_unit':13}, categories
    save('source_rows.json', {'version':'1.0.0','date':'2026-10-29','combined':c,'raw':r,
        'memberships':[{'object_id':o,'combined_row':combined[o],'raw_row':raw[o],
            'basis':'source_assertion','independent_confirmation':False} for o in sorted(combined)],
        'scope':'Exact source rows of23 existing objects. Other unit-member identifiers are source records only, not newly ingested physical objects or images.'})
    save('results.json', {'version':'1.0.0','date':'2026-10-29','completed_date':'2026-10-30','pair_audit':audit,
        'totals':{'audited_pair_leads':36,'source_objects':23,'outside_crosswalk_objects':2,
            'source_credit_repairs':5,'primary_pair_tests_pending':31,'categories':categories},
        'repair_leads':[row['lead_id'] for row in audit if row['source_credit_repair']],
        'pending_primary_leads':[row['lead_id'] for row in audit if row['primary_pair_test_pending']],
        'unit_conflict':{'unit':'BOMPAC-4861','raw_unit':'C-20','objects':negative_objects,
            'combined_excel_rows':[combined[o]['excel_row'] for o in negative_objects],
            'published_rejection':'https://doi.org/10.25167/ls.4818','published_rejection_locator':'Grajewski2022 p293, paragraph beside Table2; previously frozen H06, re-read from retained source page.',
            'result':'The pinned combined dataset places8201 and8304 in one reconstruction unit; the published study places8304 in a different manuscript despite the same hand. These are competing source assertions.',
            'scope':'Source/data reconciliation issue, not a newly discovered historical exclusion, a proved global dataset error or a cleared novelty claim.',
            'interpretation_scope':'Literal co-assignment is a source assertion. Its implied same-codex meaning is recorded as a separate unresolved project interpretation of the published unit definition, not a direct pair-level argument by the dataset authors.',
            'novelty_cleared':False,'independent_confirmation':False},
        'next_test':{'pair':['mpo-8201','mpo-8304'],
            'question':'Do the actual retained captures independently show both office-opening rubrics and their exact positions, as required by the published different-book argument? Preserve uncertain readings and composite/repeated-office alternatives.',
            'selection':'Existing frozen negative control and unit conflict, not a new target. Use all four retained captures per fragment; no invented missing positive-control image.',
            'dependency':'Fr20106 is catalogued at KB A103 but its retained MPO record has neither viewer nor IIIF pointer. Its missing image remains a separate explicit dependency.'},
        'independent_confirmation':False,'new_discovery':False,'goal_complete':False,
        'global_blocker_established':False,'new_source_image_files':0,
        'retained_file_acquisition_bytes':0,'web_reader_traffic':'Unmeasured; covered by existing planning reserve.'})
    print(json.dumps({'categories':categories,'source_credit_repairs':5,'primary_pair_tests_pending':31},indent=2))


if __name__=='__main__':
    main()
