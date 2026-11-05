"""Check E47 source cells with an independent stdlib XLSX/XML reader.

Checks attribution/join integrity and preservation, not historical codex identity.
No spreadsheet engine, external access, workbook mutation or private PDFs needed.
"""
from __future__ import annotations

import collections
import hashlib
import json
import posixpath
from pathlib import Path
import xml.etree.ElementTree as ET
import zipfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
NS = {'x': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
REL = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'


def read(path):
    return json.loads((ROOT / path).read_text())


def xml_unit_rows(path, sheet_name, unit, unit_column, wanted_columns, target_column, target_identifiers):
    """Resolve worksheet by name and read source values, without cached formulas."""
    with zipfile.ZipFile(ROOT / path) as z:
        strings = []
        if 'xl/sharedStrings.xml' in z.namelist():
            for item in ET.fromstring(z.read('xl/sharedStrings.xml')).findall('x:si', NS):
                strings.append(''.join(t.text or '' for t in item.iter('{'+NS['x']+'}t')))
        sheets = ET.fromstring(z.read('xl/workbook.xml')).findall('x:sheets/x:sheet', NS)
        matches = [s for s in sheets if s.attrib['name'] == sheet_name]
        assert len(matches) == 1
        relid = matches[0].attrib['{'+REL+'}id']
        relations = ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))
        targets = [r.attrib['Target'] for r in relations if r.attrib['Id'] == relid]
        assert len(targets) == 1
        target = targets[0]
        entry = target.lstrip('/') if target.startswith('/') else posixpath.normpath('xl/'+target)
        selected = []
        target_rows = []
        for _, element in ET.iterparse(z.open(entry), events=('end',)):
            if element.tag != '{'+NS['x']+'}row':
                continue
            rowno = int(element.attrib['r'])
            data = {}
            for cell in element.findall('x:c', NS):
                address = cell.attrib['r']
                col = ''.join(c for c in address if c.isalpha())
                if col not in wanted_columns:
                    continue
                assert cell.find('x:f', NS) is None, 'Formula cannot be treated as a source literal: '+address
                v = cell.find('x:v', NS)
                if cell.attrib.get('t') == 's':
                    value = strings[int(v.text)]
                elif cell.attrib.get('t') == 'inlineStr':
                    value = ''.join(t.text or '' for t in cell.findall('x:is//x:t', NS))
                elif v is None or v.text is None:
                    value = None
                elif cell.attrib.get('t') in ['str', 'e']:
                    value = v.text
                elif cell.attrib.get('t') == 'b':
                    value = bool(int(v.text))
                else:
                    value = float(v.text)
                    if value.is_integer():
                        value = int(value)
                data[col] = value
            unit_match = data.get(unit_column) in unit if isinstance(unit, set) else data.get(unit_column) == unit
            if rowno == 2 or unit_match:
                selected.append((rowno, data))
            if rowno > 2 and data.get(target_column) in target_identifiers:
                target_rows.append((rowno, data))
            element.clear()
    return selected, target_rows


def main():
    protocol = read('research/continuation_47/protocol.json')
    for path, expected in {**protocol['source_inputs'], **protocol['frozen_inputs']}.items():
        assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest() == expected, path
    doc = read('research/continuation_47/memberships.json')
    for key, unit_col in [('combined', 'M'), ('raw', 'F')]:
        source = doc[key]
        expected_rows = {r['excel_row']: r for r in source['unit_rows']}
        columns = {''.join(c for c in address if c.isalpha()): name
                   for name, address in source['unit_rows'][0]['cells'].items()}
        target_col = 'C' if key == 'combined' else 'D'
        target_name = 'Fr_reference' if key == 'combined' else 'fragment_id'
        target_identifiers = {r['values'][target_name] for r in source['target_rows']}
        actual, target_rows = xml_unit_rows(source['path'], source['sheet'], source['unit'], unit_col,
                                            set(columns), target_col, target_identifiers)
        assert len(target_rows) == 6
        assert len({r[target_col] for _, r in target_rows}) == 6
        assert {n for n, _ in target_rows} == {r['excel_row'] for r in source['target_rows']}
        assert len(actual) == len(expected_rows)+1
        header = dict(actual)[2]
        assert all(header[col] == name for col, name in columns.items())
        for n, values in actual:
            if n == 2:
                continue
            row = expected_rows[n]
            assert {name: values.get(col) for col, name in columns.items()} == row['values'], n
            assert all(address == col+str(n) for col, name in columns.items() for address in [row['cells'][name]])
    assert len(doc['memberships']) == 6
    assert {r['values']['Database_or_institution'] for r in doc['combined']['unit_rows']} == {'KA', 'FM'}
    assert sum(r['values']['Database_or_institution']=='FM' for r in doc['combined']['unit_rows']) == 24
    assert all(r['values']['Row_exclusion']=='Include row' for r in doc['combined']['unit_rows'])
    assert not doc['combined']['unit_identifier_duplicates'] and not doc['raw']['unit_identifier_duplicates']
    baseline = read('research/continuation_47/lead_register.before.json')
    # Preserve the exact historical transition when later source audits make
    # further legitimate changes. Still require all E47 repairs in the live data.
    after_path = 'research/continuation_47/lead_register.after.json'
    current = read(after_path) if (ROOT/after_path).exists() else read('data/lead_register.v1.json')
    if (ROOT/after_path).exists():
        assert current['version'] == '1.11.0'
        expected = read('research/continuation_48/protocol.json')['source_inputs'][after_path]
        assert hashlib.sha256((ROOT/after_path).read_bytes()).hexdigest() == expected
    old = {r['id']:r for r in baseline['leads']}
    now = {r['id']:r for r in current['leads']}
    result = read('research/continuation_47/results.json')
    repairs = set(result['repair_leads'])
    assert len(old) == len(now) == 168 and old.keys() == now.keys()
    assert len(repairs) == 13
    changed = {key for key in old if old[key]['decision_state'] != now[key]['decision_state']}
    assert changed == repairs
    for key in repairs:
        assert old[key]['test_execution'] == 'metadata and availability triage only'
        assert old[key]['decision_state'] == 'unresolved'
        assert now[key]['decision_state'] == 'previously_documented'
        assert now[key]['test_execution'] == 'published BOMPAC membership audit; no new pair-level image transcription'
        assert not now[key]['independent_confirmation']
        assert now[key]['subjects'] == old[key]['subjects']
        live = next(r for r in read('data/lead_register.v1.json')['leads'] if r['id']==key)
        assert live['decision_state']=='previously_documented' and not live['independent_confirmation']
    before_only = {k for k in old if old[k]['test_execution']=='metadata and availability triage only'}
    after_only = {k for k in now if now[k]['test_execution']=='metadata and availability triage only'}
    assert len(before_only) == 49 and len(after_only) == 36 and after_only == before_only-repairs
    assert now[next(k for k in now if now[k].get('frozen_hypothesis')=='H06')]['decision_state']=='contradicted'
    graph = read('data/knowledge.v1.json')
    claims = [c for c in graph['claims'] if c['id'].startswith('assignment:mpo-') and c['id'].endswith(':bompac4795')]
    assert len(claims) == 6
    for c in claims:
        assert c['basis'] == 'source_assertion' and c['predicate'] == 'assigned_to_reconstruction'
        assert c['status'] == 'previously_documented' and not c['independent_confirmation'] and not c['new_discovery']
        assert c['object'] == 'codex:BOMPAC-4795'
    finnish = next(c for c in graph['claims'] if c['id'] == 'bompac:4795:fmII44')
    assert finnish['subject'] == 'codex:fm-II.44' and finnish['object'] == 'codex:BOMPAC-4795'
    assert finnish['basis'] == 'source_assertion' and finnish['predicate'] == 'assigned_to_reconstruction'
    assert finnish['status'] == 'previously_documented' and not finnish['independent_confirmation']
    assert finnish['provenance'][0]['locator']['rows'] == [r['excel_row'] for r in doc['combined']['unit_rows'] if r['values']['Database_or_institution']=='FM']
    assert not any(result[k] for k in ['new_discovery','independent_confirmation','goal_complete','global_blocker_established'])
    print(json.dumps({'source_reader':'Independent Python stdlib ZIP/XML reader; no openpyxl import',
        'checked_source_unit_rows':38, 'retained_member_assignments':6,
        'source_credit_repairs':13, 'remaining_metadata_only_pairs':36,
        'scope':'Source-cell/join and register preservation checks only; not new historical attribution or independent confirmation.'}))


if __name__ == '__main__':
    main()
