"""Regression checks for manuscript identity, uncertainty and complete coverage."""
import copy
import json
import unittest
from pathlib import Path

from lost_library.knowledge import validate_knowledge

ROOT = Path(__file__).resolve().parents[1]


class ManuscriptKnowledgeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.graph = json.loads((ROOT / 'data/knowledge.v1.json').read_text())
        cls.register = json.loads((ROOT / 'data/lead_register.v1.json').read_text())

    def test_complete_source_linked_register_validates(self):
        result = validate_knowledge(ROOT, self.graph, self.register)
        self.assertTrue(result['frozen_inputs_unchanged'])
        self.assertEqual(self.register['coverage']['ranking_rows'], 170)
        self.assertEqual(self.register['coverage']['distinct_physical_object_ids'], 128)

    def test_shared_codex_labels_do_not_merge_physical_objects(self):
        entities = {e['id']: e for e in self.graph['entities']}
        self.assertIn('object:mpo-8201', entities)
        self.assertIn('object:mpo-8304', entities)
        self.assertEqual(entities['record:finn-iv173']['physical_object'],
                         entities['record:finn-iv173-verso']['physical_object'])

    def test_qualified_association_is_not_same_codex(self):
        claim = next(c for c in self.graph['claims'] if c['id'] == 'catalogue:iv157-1505')
        self.assertEqual(claim['predicate'], 'suggested_association')
        self.assertEqual(claim['status'], 'unresolved')
        self.assertEqual(claim['source_stance'], 'suggested')

    def test_same_hand_and_published_rejection_coexist(self):
        claims = [c for c in self.graph['claims'] if {c['subject'], c['object']} == {'object:mpo-8201', 'object:mpo-8304'}]
        self.assertTrue(any(c['predicate'] == 'same_hand' and c['polarity'] == 'positive' for c in claims))
        self.assertTrue(any(c['predicate'] == 'same_codex' and c['polarity'] == 'negative' and c['status'] == 'previously_documented' and c['basis'] == 'source_assertion' for c in claims))
        self.assertTrue(any(c['basis'] == 'computational_suggestion' for c in claims))

    def test_resolution_variants_share_capture_without_side_assignment(self):
        native = next(e for e in self.graph['entities'] if e['id'] == 'image:data/images/mpo-8994-capture-1-1802px.jpg')
        images = [e for e in self.graph['entities'] if e['type'] == 'ImageDerivative' and e['capture'] == native['capture']]
        self.assertGreaterEqual(len(images), 2)
        self.assertEqual(len({e['capture'] for e in images}), 1)
        capture = next(e for e in self.graph['entities'] if e['id'] == images[0]['capture'])
        self.assertIsNone(capture['side_assignment'])

    def test_missing_image_is_dependency_not_negative_assertion(self):
        self.assertTrue(any(d['id'] == 'missing-image:mpo-20278' for d in self.graph['dependencies']))
        self.assertFalse(any(c['polarity'] == 'negative' and 'missing-image' in c['id'] for c in self.graph['claims']))
        conflict = next(c for c in self.graph['claims'] if c['id'] == 'interpretation:E33')
        self.assertEqual(conflict['status'], 'unresolved')
        self.assertTrue(all(v is None for v in conflict['unverified_premises'].values()))

    def test_failed_registration_is_not_a_negative_codex_or_side_assertion(self):
        claims = [c for c in self.graph['claims'] if c['id'].startswith('interpretation:E35:')]
        self.assertEqual(len(claims), 2)
        for claim in claims:
            self.assertEqual(claim['predicate'], 'photographic_overlap')
            self.assertEqual(claim['status'], 'unresolved')
            self.assertEqual(claim['polarity'], 'positive')
            self.assertFalse(claim['numerical_result']['screen_passed'])
            self.assertFalse(claim['independent_confirmation'])
            self.assertTrue(claim['subject'].startswith('image:'))

    def test_generic_alleluia_boundary_stays_weaker_than_exact_phrase_controls(self):
        claims = {c['id']: c for c in self.graph['claims']}
        self.assertEqual(claims['interpretation:E36:aboense-I']['status'], 'supported')
        self.assertEqual(claims['interpretation:E36:aboense-II']['status'], 'unresolved')
        self.assertEqual(claims['interpretation:E36:aboense-III']['status'], 'supported')
        for lead in self.register['leads']:
            if lead['id'].startswith('E36-'):
                self.assertEqual(lead['decision_state'], 'previously_documented')
                self.assertFalse(lead['independent_confirmation'])

    def test_partial_chant_ending_does_not_become_codex_or_whole_office_identity(self):
        claim = next(c for c in self.graph['claims'] if c['id'] == 'interpretation:E37-ending')
        self.assertEqual(claim['predicate'], 'chant_identification')
        self.assertEqual(claim['claim_extent'], 'surviving_ending')
        self.assertFalse(claim['whole_office_recension_established'])
        self.assertFalse(claim['independent_confirmation'])
        entities = {e['id']: e for e in self.graph['entities']}
        self.assertEqual(entities[claim['object']]['type'], 'Chant')
        publication = next(c for c in self.graph['claims'] if c['id'] == 'publication:E37-antiphon-replacement')
        self.assertEqual(publication['basis'], 'source_assertion')
        self.assertEqual(publication['status'], 'previously_documented')

    def test_old_comparison_page_cannot_silently_supply_the_missing_replacement(self):
        observation = next(e for e in self.graph['evidence'] if e['id'] == 'evidence:I37-C23-older-ending')
        self.assertIn('attachment-0144', observation['target']['source'])
        self.assertIn('not the added/replacement', observation['observation'])
        self.assertTrue(any(d['id'] == 'missing-c23-replacement-69r' for d in self.graph['dependencies']))
        lead = next(l for l in self.register['leads'] if l['id'] == 'E37-C435-access')
        self.assertEqual(lead['decision_state'], 'not_testable')
        self.assertIn('missing-c435-original', lead['required_inputs']['dependencies'])

    def test_model_identity_promotion_rejected(self):
        graph = copy.deepcopy(self.graph)
        claim = next(c for c in graph['claims'] if c['basis'] == 'computational_suggestion')
        claim['predicate'] = 'same_codex'
        with self.assertRaisesRegex(ValueError, 'promoted to identity'):
            validate_knowledge(ROOT, graph, self.register)

    def test_received_replacement_page_resolves_only_its_own_dependency(self):
        dependency = next(d for d in self.graph['dependencies'] if d['id'] == 'missing-c23-replacement-69r')
        self.assertEqual(dependency['state'], 'resolved')
        lead = next(l for l in self.register['leads'] if l['id'] == 'E37-ending')
        self.assertNotIn(dependency['id'], lead['required_inputs']['dependencies'])
        self.assertIn('missing-c435-original', lead['required_inputs']['dependencies'])
        regions = [e for e in self.graph['evidence'] if e['annotation_id'].startswith('I38-')]
        self.assertEqual(len(regions), 3)
        self.assertTrue(all('0139' in e['target']['source'] for e in regions))
        claim = next(c for c in self.graph['claims'] if c['id'] == 'interpretation:E38-replacement-text')
        self.assertEqual(claim['predicate'], 'chant_identification')
        self.assertFalse(claim['melodic_identity_established'])
        self.assertFalse(claim['whole_office_recension_established'])

    def test_partial_music_agreement_does_not_establish_melodic_identity(self):
        claim = next(c for c in self.graph['claims'] if c['id'] == 'interpretation:E39-excerpt')
        self.assertEqual(claim['status'], 'unresolved')
        self.assertEqual(claim['provisional_concordant_positions'], 12)
        self.assertEqual(claim['unresolved_positions'], 2)
        self.assertFalse(claim['absolute_pitch_verified'])
        self.assertFalse(claim['melodic_identity_established'])
        lead = next(l for l in self.register['leads'] if l['id'] == 'E39-excerpt')
        self.assertEqual(lead['decision_state'], 'unresolved')
        self.assertFalse(lead['independent_confirmation'])

    def test_catalogue_boundary_fit_does_not_become_a_physical_join(self):
        claim = next(c for c in self.graph['claims'] if c['id'] == 'interpretation:E40-boundary')
        self.assertEqual(claim['predicate'], 'textual_continuation')
        self.assertEqual(claim['status'], 'unresolved')
        for key in ['physical_adjacency_established', 'physical_join_established',
                    'complete_leaf_edge_verified', 'signature_successor_verified']:
            self.assertFalse(claim[key])
        lead = next(l for l in self.register['leads'] if l['id'] == 'E40-boundary')
        self.assertIn('missing-iv156-f9', lead['required_inputs']['dependencies'])
        self.assertFalse(lead['independent_confirmation'])

    def test_local_text_fit_and_row_totals_do_not_assign_a_medieval_surface(self):
        rows = [c for c in self.graph['claims'] if c['id'].startswith('interpretation:E42:')]
        self.assertEqual(len(rows), 2)
        self.assertEqual({c['id']:c['status'] for c in rows},
                         {'interpretation:E42:1-2':'unresolved', 'interpretation:E42:3-4':'supported'})
        for claim in rows:
            self.assertEqual(claim['predicate'], 'textual_continuation')
            self.assertEqual(claim['comparison']['visible_row_sum'], 11)
            for key in ['physical_adjacency_established', 'physical_join_established',
                        'complete_surface_map_established', 'accepted_photographic_overlap',
                        'new_codex_attribution', 'novelty_cleared', 'independent_confirmation']:
                self.assertFalse(claim[key])

    def test_published_reconstruction_credit_does_not_validate_machine_proposals(self):
        repairs = [l for l in self.register['leads'] if
                   l['test_execution'] == 'published reconstruction source audit; no new pair-level image transcription']
        self.assertEqual(len(repairs), 43)
        claims = {c['id']:c for c in self.graph['claims']}
        for lead in repairs:
            self.assertEqual(lead['decision_state'], 'previously_documented')
            self.assertFalse(lead['independent_confirmation'])
            proposal = claims['claim:'+lead['id']]
            self.assertEqual(proposal['basis'], 'computational_suggestion')
            self.assertEqual(proposal['status'], 'unresolved')
        assignments = [c for c in self.graph['claims'] if c['id'].endswith(':beauvais')]
        self.assertEqual(len(assignments), 12)
        for claim in assignments:
            self.assertEqual(claim['basis'], 'source_assertion')
            self.assertEqual(claim['predicate'], 'assigned_to_reconstruction')
            self.assertTrue(claim['matched_canvas_ids'])
            self.assertFalse(claim['independent_confirmation'])
            self.assertFalse(claim['new_discovery'])

    def test_shared_catalogue_unit_does_not_override_published_rejection(self):
        negative = next(l for l in self.register['leads'] if l.get('frozen_hypothesis') == 'H06')
        self.assertEqual(negative['decision_state'], 'contradicted')
        self.assertEqual(negative['frozen_category'], 'D')
        audit = json.loads((ROOT/'research/continuation_43/coverage_audit.json').read_text())
        ids = {r['lead_id'] for r in audit['pair_audit'] if r['local_source_work_pending']
               and r['shared_mpo_codex_label']=='Codex 1146'}
        shared = [l for l in self.register['leads'] if l['id'] in ids]
        self.assertEqual(len(shared), 14)
        self.assertTrue(all(l['decision_state'] == 'unresolved' for l in shared))

    def test_ant49_ruling_and_text_compatibility_do_not_create_a_book_or_erratum(self):
        claim = next(c for c in self.graph['claims'] if c['id']=='interpretation:E44-8066-9620')
        self.assertEqual(claim['status'], 'unresolved')
        for key in ['four_vs_five_split_supported','different_book_genres_established',
                    'duplicated_complete_opening_established','same_codex_established',
                    'physical_join_established','catalogue_correction_confirmed',
                    'novelty_cleared','independent_confirmation','new_discovery']:
            self.assertFalse(claim[key])
        lead = next(l for l in self.register['leads'] if l['subjects']==['object:mpo-8066','object:mpo-9620'])
        self.assertEqual(lead['decision_state'], 'unresolved')
        self.assertTrue(lead['test_execution'].startswith('E44 direct exploratory'))
        self.assertEqual(sum(len(v) for v in lead['required_inputs']['available_primary_images'].values()),11)
        self.assertFalse(claim['service_recheck']['complete_duplicate_opening_established'])
        self.assertFalse(claim['service_recheck']['different_codex_established'])
        self.assertFalse(claim['service_recheck']['distinctive_variant_established'])

    def test_related_chant_candidates_do_not_create_a_same_work_variant_or_book_exclusion(self):
        candidates=[c for c in self.graph['claims'] if c['id'].startswith('interpretation:E46:')]
        self.assertEqual(len(candidates),2)
        self.assertEqual(len({c['object'] for c in candidates}),2)
        for c in candidates:
            self.assertEqual(c['status'],'unresolved')
            self.assertTrue(c['candidate_only'])
            self.assertFalse(c['exact_local_work_confirmed'])
            self.assertFalse(c['service_position_confirmed'])
        count=next(c for c in self.graph['claims'] if c['id']=='observation:E46-headgroups')
        self.assertEqual(count['visible_candidate_head_counts'],{'8066':5,'9620':2})
        self.assertFalse(count['diagnostic_melodic_variant_established'])
        self.assertFalse(count['different_codex_established'])

    def test_confidence_and_dangling_evidence_rejected(self):
        graph = copy.deepcopy(self.graph)
        graph['claims'][0]['confidence'] = 0.99
        with self.assertRaisesRegex(ValueError, 'confidence forbidden'):
            validate_knowledge(ROOT, graph, self.register)
        del graph['claims'][0]['confidence']
        graph['claims'][0]['supports'] = ['evidence:invented']
        with self.assertRaisesRegex(ValueError, 'Dangling evidence'):
            validate_knowledge(ROOT, graph, self.register)

    def test_dropped_crosslink_cannot_pass_complete_audit(self):
        register = copy.deepcopy(self.register)
        register['leads'] = [l for l in register['leads'] if not l['id'].startswith('crosslink:IV160:')]
        with self.assertRaisesRegex(ValueError, 'Crosslink coverage incomplete'):
            validate_knowledge(ROOT, self.graph, register)

    def test_changed_source_region_rejected(self):
        graph = copy.deepcopy(self.graph)
        graph['evidence'][0]['target']['selector']['value'] = 'xywh=0,0,99999,1'
        with self.assertRaisesRegex(ValueError, 'outside image'):
            validate_knowledge(ROOT, graph, self.register)


if __name__ == '__main__':
    unittest.main()
