"""Record E55's failed disambiguation without rewriting E39 source readings."""
import hashlib
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]


def main():
    c=json.loads((HERE/'staff_calibration.json').read_text())
    notes=c['notes']
    targets=[r for r in notes if r['source']=='target' and r['slot']==4]
    assert all(r['geometric_relative_alternatives']==[3,4] for r in targets)
    result=dict(version='1.0.0',date='2026-10-31',selected_existing_lead='E39-excerpt',
        retained_head_anchors=28,declared_alignment_slots=14,
        candidate_rule_models=12,valid_rule_models=sum(m['valid'] for w in c['windows'].values() for m in w['models']),
        source_regions_reused=['I39-target-opening-signs','I39-target-nobis','I39-C23-nobis','I39-target-petition','I39-C23-petition'],
        direct_result='Both E39 target upper events retain geometric relative alternatives3/4 under the declared source-pixel sensitivity. C23 nobis has no valid complete four-rule fit; its prior edition-assisted reading is not freshly certified by this algorithm. C23 petition has two valid threshold fits and one failed fit.',
        qualified_target_upper_events=targets,
        further_uncertainty='The same broad sensitivity also permits1/2 at the two target spem anchors. E39 twelve provisional concordances remain a historical selected reading, not twelve newly verified pitches or recognition accuracy.',
        opening_signs={'region':'I39-target-opening-signs','state':'unclassified','limit':'The exact source crop was re-viewed. This local geometric test does not supply a documented clef/guide/neume classification or absolute pitch.'},
        native_recheck='The already retained C23 original TIFF was visually rechecked at both windows after the JPEG fit failed. No new target pitch was read from it and no classifier thresholds were retuned.',
        prior_art_recheck={'source':'research/scholarship/urberg2016.pdf','url':'https://doi.org/10.6082/uchicago.1751','fresh_pages_visually_checked':[600,604,605],'pdf_pages':[626,630,631],
            'actual_scope':'Legend/opening and two selected six-witness score pages; not a fresh full-thesis or all AppendixF review.',
            'result':'The edition already compares six witnesses. These pages show broad shared internal contours and some other variation; no new target reading is established by matching the edition. The unresolved target events cannot be presented as an original variant.'},
        interpretation='Source-local geometry does not resolve either target ambiguity. Do not claim a robust melodic difference, exact excerpt identity, new tradition or codex attribution. A future documented sign/anchor reading or genuinely better primary detail is needed for this specific uncertainty.',
        decision_state='unresolved',new_source_files=0,new_download_bytes=0,new_source_regions=0,
        working_source_files_after=208,conservative_transfer_plan_after=1675854139,
        two_target_events_resolved=False,complete_rule_calibration_succeeded=False,
        exact_pitches_verified=False,robust_melodic_variant_established=False,
        melodic_identity_established=False,new_codex_attribution=False,new_discovery=False,
        novelty_cleared=False,independent_confirmation=False,goal_complete=False,global_blocker_established=False,
        next_test='Reconcile the existing Turku Ms.c holding/extent alias through exact legitimate institutional records, then perform the still-open Fr8311 work/verse identification check. Do not repeat E39 pixel rounding without genuinely new notation evidence.',
        future_note_test='The two target upper signs need a documented source-specific neume/anchor interpretation or genuinely better primary detail. Raw geometric rounding is insufficient; retain3/4 alternatives. Opening signs remain unclassified, and two spem controls also widen to1/2 under this sensitivity.')
    result['preserved_e39_reading_hash']=hashlib.sha256((ROOT/'research/continuation_39/readings.v3.json').read_bytes()).hexdigest()
    (HERE/'results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['valid_rule_models','candidate_rule_models','two_target_events_resolved','new_source_files','decision_state','new_discovery']}))


if __name__=='__main__':
    main()
