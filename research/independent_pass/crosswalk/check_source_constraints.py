"""Conditional source consistency checks; not a manuscript-identity classifier.

No network, source acquisition, model fitting or queue mutation. The assertions
below test implications under explicit assumptions, not the historical truth of
those assumptions. Distinct feast labels are weaker than conflicting full text.
"""
from itertools import product
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
ASSUMPTIONS = ('unique_unrepeated_signature_scheme', 'identical_addresses_accurately_transcribed',
               'addresses_identify_same_physical_position', 'text_at_position_mutually_incompatible')


def source_collision(assumptions, addresses_equal, catalogue_feasts_differ):
    if any(assumptions[k] is None for k in ASSUMPTIONS):
        return 'unresolved: necessary premises not established'
    if all(assumptions[k] for k in ASSUMPTIONS) and addresses_equal and catalogue_feasts_differ:
        return 'conditional contradiction of joint premises'
    return 'no contradiction forced by this check; identity not established'


def orientation_check(same_rv_convention, same_signature_scheme, literal_tokens_accurate):
    if None in (same_rv_convention, same_signature_scheme, literal_tokens_accurate):
        return 'unresolved: side and scheme correspondence not established'
    if same_rv_convention and same_signature_scheme and literal_tokens_accurate:
        return 'conditional side-label inconsistency; no book-identity verdict'
    return 'no inconsistency forced by this check; orientation not established'


def main():
    audit_path = OUT/'audit.json'
    manifest_path = OUT/'catalogue_excerpt_manifest.json'
    audit = json.loads(audit_path.read_text())
    manifest = json.loads(manifest_path.read_text())
    by_id = {r['fields']['signatur']:r for r in audit['raw_records']}
    assert by_id['10370']['fields']['lagenanmerkungen'] == 'Am oberen Rand alte Foliierung 1r: k; 1v: II'
    rows = []
    for values in product((False, True), repeat=4):
        premises = dict(zip(ASSUMPTIONS, values))
        rows.append({'premises':premises, 'result':source_collision(premises, True, True)})
    assert sum(r['result'].startswith('conditional contradiction') for r in rows) == 1
    unresolved = {key:None for key in ASSUMPTIONS}
    assert source_collision(unresolved, True, True).startswith('unresolved')
    assert orientation_check(None, None, True).startswith('unresolved')
    assert orientation_check(True, True, True).startswith('conditional side-label inconsistency')
    assert orientation_check(False, True, True).startswith('no inconsistency forced')
    queue_sha = hashlib.sha256((ROOT/'data/hypotheses.v1.json').read_bytes()).hexdigest()
    assert queue_sha == audit['frozen_queue_sha256']
    result = {
        'version':'1.0.0', 'assessment_date':'2026-10-22',
        'scope':'Explicit conditional consistency checks on catalogue assertions; no attribution or independent physical adjudication',
        'input_provenance':{
            'audit_json_sha256':hashlib.sha256(audit_path.read_bytes()).hexdigest(),
            'catalogue_excerpt_manifest_sha256':hashlib.sha256(manifest_path.read_bytes()).hexdigest(),
            'frozen_queue_sha256_unchanged':queue_sha,
            'access_method':manifest['access_method'],
            'new_web_requests':0, 'source_images_inspected_in_this_check':0,
        },
        'opening_collision':{
            'source_assertions':[
                {'record':'Helsinki F.m.IV.156','folio':'2', 'opening_interval':{'letter':'h','start_roman':'VIII','end_roman':'IX'},
                 'catalogue_feast':'Peter and Paul','url':'https://fragmenta.kansalliskirjasto.fi/handle/10024/1299',
                 'location':'Older additionalInformation, per-folio contents list, folio2',
                 'epistemic_status':'Institutional catalogue assertion read through public index; exact image text not verified'},
                {'record':'Helsinki F.m.IV.157','folio':'5', 'opening_interval':{'letter':'h','start_roman':'VIII','end_roman':'IX'},
                 'catalogue_feast':'John Baptist','url':'https://fragmenta.kansalliskirjasto.fi/handle/10024/1300',
                 'location':'Older additionalInformation, per-folio contents list, folio5',
                 'epistemic_status':'Institutional catalogue assertion read through public index; exact image text not verified'},
            ],
            'facts_from_source_descriptions':{'identical_catalogued_opening_interval':True,'different_catalogue_feast_labels':True},
            'joint_premises_required_for_contradiction':list(ASSUMPTIONS),
            'actual_premise_status':{
                'unique_unrepeated_signature_scheme':'unverified across the alleged combined book',
                'identical_addresses_accurately_transcribed':'unverified against images; indexed text can contain OCR errors',
                'addresses_identify_same_physical_position':'conditional on common scheme/context; no physical placement verified',
                'text_at_position_mutually_incompatible':'unverified: only different feast labels used; complete corresponding text not retained here',
            },
            'actual_result':source_collision(unresolved,True,True),
            'conditional_result':'The conjunction of accurate identical addresses, unique unrepeated signatures, same physical position and mutually incompatible text is inconsistent. At least one premise must fail.',
            'not_a_result':'Does not by itself reject same codex, establish separate scribes or clear originality.',
            'weakness':'Different feast labels alone do not prove mutually incompatible full text. Partial descriptions, combined offices or different passage boundaries could explain labels.',
            'minimal_alternatives':[
                'Repeated or reset numbering, or multiple signature contexts in a composite volume',
                'Catalogue transcription/OCR error or wrong side/folio assignment',
                'Different labels are incomplete summaries of compatible contents',
                'The fragments belong to different books',
            ],
            'truth_table_under_catalogue_facts':rows,
            'next_observations':['Actual signatures on IV156f2 andIV157f5','Full overlapping chant/text at corresponding sides','Evidence for or against repeated/reset signature contexts'],
        },
        'fr10370_orientation':{
            'literal_cc0_mpo_note':by_id['10370']['fields']['lagenanmerkungen'],
            'csv_location':{'path':'research/mpo.csv','record_ordinal':by_id['10370']['data_record_ordinal'],'physical_end_line':by_id['10370']['csv_physical_end_line'],'field':'lagenanmerkungen'},
            'institutional_signature_convention':{'letter_side':'verso','roman_numeral_side':'recto','source_urls':['https://fragmenta.kansalliskirjasto.fi/handle/10024/1299','https://fragmenta.kansalliskirjasto.fi/handle/10024/1300','https://fragmenta.kansalliskirjasto.fi/handle/10024/1314']},
            'recorded_literal_token_pattern_reversed_relative_to_convention':True,
            'actual_medieval_side_orientation_verified':False,
            'actual_result':orientation_check(None,None,True),
            'conditional_result':orientation_check(True,True,True),
            'minimal_alternatives':['MPO r/v is a different descriptive or capture convention','Literal signature or side assignment is erroneous','The signature scheme differs or resets','The expected convention applies and the record labels require reversal'],
            'next_observations':['Top-margin tokens on both actual surfaces','Intrinsic direction and sequence of the Latin text','Whether MPO labels refer to medieval sides or source photographs'],
            'not_a_result':'No wrong-book conclusion, final recto/verso assignment or new sequence follows from the label pattern alone.',
        },
        'independent_expert_review':False,'new_discovery':False,'frozen_queue_changed':False,
        'checks_passed':['All16Boolean opening-premise combinations evaluated','Only the full joint premise set forces contradiction','Unknown premises remain unresolved','10370scheme/convention uncertainty remains unresolved','Source note literal and frozen queue hashes verified'],
    }
    (OUT/'source_constraints.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'opening_actual_result':result['opening_collision']['actual_result'],
                      'orientation_actual_result':result['fr10370_orientation']['actual_result'],
                      'opening_premise_combinations':len(rows),'checks':'passed','new_discovery':False},indent=2))

if __name__=='__main__':main()
