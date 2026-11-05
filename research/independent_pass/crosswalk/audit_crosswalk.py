"""Reproduce the local source crosswalk; no network or attribution classifier."""
from pathlib import Path
import csv
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
TARGETS = {'1385', '8994', '10370', '10406', '10407', '10437', '20274', '20275', '20276', '20277', '20278', '25592', '29666'}
FIELDS = ['signatur', 'ccmsignum', 'codex', 'datierung', 'blattzahl', 'format', 'schriftraum1', 'spaltenzahl', 'zeilenzahl1', 'notation', 'lagenanmerkungen', 'anmerkungen', 'inhalt', 'bestandsbezeichnung', 'bestandssignatur', 'iiif_manifest']

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    source = ROOT / 'research/mpo.csv'
    rows = []
    selected = []
    with source.open(encoding='utf-8-sig', newline='') as stream:
        reader = csv.DictReader(stream)
        for ordinal, row in enumerate(reader, 1):
            rows.append(row)
            if row['signatur'] in TARGETS:
                selected.append({'data_record_ordinal': ordinal, 'csv_physical_end_line': reader.line_num,
                                 'fields': {k: row[k] for k in FIELDS}})
    records = {r['id']: r for r in json.loads((ROOT/'data/fragments.json').read_text())}
    queue_sha = sha(ROOT/'data/hypotheses.v1.json')
    assert queue_sha == 'b3e299a7c600584ce44518db1f5c30c3301edae0a07a8b009075498f64ccec47'
    assert len(selected) == 13
    assert all(records['mpo-'+r['fields']['signatur']]['raw'][k] == r['fields'][k]
               for r in selected for k in FIELDS)
    norm = lambda s: re.sub(r'\s+', '', s).casefold()
    aliases = {label: [r['signatur'] for r in rows if norm(r['ccmsignum']) == norm(label)]
               for label in ['Hy 49', 'Ant 99', 'Ant 242']}
    assert aliases == {'Hy 49':['25592'], 'Ant 99':['20274','20275','20276','20277','20278'], 'Ant 242':['29666']}
    codex = [r for r in rows if r['codex'] == 'Codex 1505']
    assert [r['signatur'] for r in codex] == ['8994','10370','10406','10407','10437']
    output = {
        'assessment_date': '2026-10-22',
        'scope': 'Pinned-source identity, assertion modality and falsifiable orientation/sequence audit; no new attribution',
        'csv': {'path': 'research/mpo.csv', 'sha256': sha(source), 'records':len(rows), 'licence':'CC0 deposit; images separately licensed'},
        'normalized_input_sha256':sha(ROOT/'data/fragments.json'),
        'frozen_queue_sha256':queue_sha,
        'checks': {'selected_raw_fields_match_pinned_csv':True, 'alias_mappings_unique_in_pinned_csv':True,
                   'same_codex_1505_member_list_exact':True, 'no_queue_mutation':True},
        'alias_to_fragment_ids': aliases,
        'codex_1505': {'fragment_ids':[r['signatur'] for r in codex], 'catalogued_leaves':sum(int(r['blattzahl']) for r in codex),
                       'interpretation':'A catalogue grouping, not an independently demonstrated codex identity.'},
        'raw_records': selected,
        'findings': [
            {'id':'X01','status':'verified identifier crosswalk',
             'claim':'Hy49 identifies Fr25592 uniquely in this version of MPO; Ant242 identifies29666; Ant99 has five records.',
             'consequence':'The Hy49/25592 identifier mapping is not an outstanding ambiguity within the pinned export. Accuracy of the historical association is a different question.'},
            {'id':'X02','status':'verified source assertion modality',
             'claim':'Fr29666 gives an explicit same-codex link to HelsinkiAnt173, while its Hy49 mention requests comparison only. The indexed Finnish updated note explicitly distinguishes accepted Ant242 from suggested Hy49 and Ant99.',
             'consequence':'H05 cannot be used as a known positive. Date/layout conflict challenges a previously suggested association; it does not overturn a proven positive or establish physical exclusion.'},
            {'id':'X03','status':'previously published specific placement recovered; not a discovery',
             'claim':'Older IV157 descriptive prose places a FinskaCameralia48/ChristiernPhilipssons1610 MaryMagdalene leaf between its ff7and8. Fr10370 is the exact matching account48:7/1610 leaf; the newer note itself supplies that full identifier under suggested Codex1505.',
             'consequence':'Preserve a specific testable insertion and the later qualified group assertion, instead of flattening both into generic resemblance. Neither chronology nor actual placement has been verified from both manuscripts.'},
            {'id':'X04','status':'conditional side-label difference, not resolved physical orientation',
             'claim':'Finnish IV156/157/173 descriptions place letter signatures on medieval verso and Roman numerals on recto. Fr10370 MPO note instead labels k as1r andII as1v.',
             'consequence':'No MPO-specific r/v convention is established. Do not transfer provider r/v or capture ordinals directly into a medieval sequence. Inspect actual top-margin tokens and text succession; different source-side convention, reversal or transcription error are alternatives. See side_convention_note.json.'},
            {'id':'X05','status':'conditional falsification from explicit catalogue positions',
             'claim':'IV156f2 andIV157f5 have the same catalogued opening interval hVIII–hIX but different feast contents: Peter/Paul versus JohnBaptist.',
             'consequence':'They cannot occupy one unrepeated opening address in a single uniform numbering system if both transcriptions are accurate. Repeated/reset numbering, composite structure or catalogue error remain alternatives. This is not an independent image-based exclusion.'},
            {'id':'X06','status':'exact comparator test identified',
             'claim':'IV156f8 is catalogued at kII–kIII and changes from MaryMagdalene toJames. Fr10370 contains MaryMagdalene and its k/II signatures need orientation resolution.',
             'consequence':'After orientation, compare overlapping text positions against IV156f8 and the documented IV157gap. Match precise chants and words, not merely feast names. Source descriptions alone do not settle it.'},
            {'id':'X07','status':'measurement semantics unresolved',
             'claim':'Finnish prose gives IV15722–23by33.5–35.5cm and IV15622.5–23by32–36cm; the indexed metadata does not identify these as leaf versus written-space fields. MPO distinguishes format from schriftraum1.',
             'consequence':'A direct dimension exclusion is unjustified. Transposition and measurement category must be established before comparing these values. The old dimensional caution remains valid.'},
            {'id':'X08','status':'catalogue assertion tension retained',
             'claim':'IV156 updated notes qualify Codex1505 as suggested in one passage but later equate it with IV157 in the same field.',
             'consequence':'This is evidence of heterogeneous catalogue assertion levels, not proof that the three catalogue units form one manuscript or that the historical question remains unresolved today.'},
            {'id':'X09','status':'provenance qualification',
             'claim':'The local Finnish record raw object holds a manually compiled association summary rather than the original catalogue text; normalize_mpo preserves the Swedish row verbatim.',
             'consequence':'Cite the indexed institutional wording and its access status directly. Do not present the hardcoded Finnish summary as a raw institutional API response.'}
        ],
        'catalogue_access': {
            'method':'Official institutional pages read through search-index full metadata; not direct HTML/PDF retrieval or a current browser screenshot',
            'direct_html_http_status':'not tested in this subtask', 'screenshot_obtained':False,
            'source_urls':['https://fragmenta.kansalliskirjasto.fi/handle/10024/1299', 'https://fragmenta.kansalliskirjasto.fi/handle/10024/1300', 'https://fragmenta.kansalliskirjasto.fi/handle/10024/1314'],
            'limits':'Indexed text has OCR/typographic corruption. Exact image readings, source edition chronology and the later Keskiaho chapter remain unverified.'},
        'next_source_images': [
            {'test':'Medieval-side orientation of Fr10370', 'available_local':['data/images/mpo-10370.jpg'],
             'source_manifest':records['mpo-10370']['manifest_url'], 'manifest_canvas_count':records['mpo-10370'].get('source_canvas_count'),
             'needed':'Top-margin views of both actual surfaces; source canvas ordinals must not be assumed to identify recto/verso.'},
            {'test':'Signature collision image check', 'needed':['IV156 folio2 recto and verso','IV157 folio5 recto and verso'],
             'record_urls':['https://fragmenta.kansalliskirjasto.fi/handle/10024/1299','https://fragmenta.kansalliskirjasto.fi/handle/10024/1300'],
             'condition':'Map source PDF/canvases to these actual folios before reading; do not infer PDFpage=2*folio.'},
            {'test':'10370 competing placement', 'needed':['IV156 folio8 recto and verso','IV157 folio7 verso','IV157 folio8 recto','Both medieval surfaces ofFr10370'],
             'condition':'Compare exact words and chant positions after intrinsic orientation; no direct boundary join inferred from an insertion between surviving leaves.'}
        ],
        'new_discovery':False, 'independent_expert_review':False,
        'source_images_or_pdfs_downloaded':0, 'external_messages_sent':0,
    }
    (OUT/'audit.json').write_text(json.dumps(output, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({'raw_rows':len(selected),'checks':output['checks'],'findings':len(output['findings']),'new_discovery':False},indent=2))

if __name__ == '__main__': main()
