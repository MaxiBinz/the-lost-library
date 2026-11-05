import hashlib
import tempfile
import unittest
from pathlib import Path

from PIL import Image
from lost_library.evidence import index_evidence_records, validate_context_checks, validate_observation


class EvidenceIntegrityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        Image.new('RGB', (100, 80), 'white').save(self.root / 'leaf.png')
        self.records = {'fragment': {'image_path': 'leaf.png'}}
        self.observation = {'fragment_id': 'fragment', 'sha256': hashlib.sha256((self.root / 'leaf.png').read_bytes()).hexdigest(),
                            'target': {'source': 'leaf.png', 'selector': {'value': 'xywh=10,20,30,40'}}}

    def test_region_preserves_source_coordinate_system(self):
        result = validate_observation(self.root, self.observation, self.records)
        self.assertEqual(result['region'], [10, 20, 30, 40])
        self.assertEqual(result['image_dimensions'], [100, 80])

    def test_altered_source_cannot_support_old_observation(self):
        Image.new('RGB', (100, 80), 'black').save(self.root / 'leaf.png')
        with self.assertRaisesRegex(ValueError, 'hash changed'):
            validate_observation(self.root, self.observation, self.records)

    def test_outside_image_is_not_valid_evidence(self):
        self.observation['target']['selector']['value'] = 'xywh=90,20,30,40'
        with self.assertRaisesRegex(ValueError, 'outside'):
            validate_observation(self.root, self.observation, self.records)

    def test_region_cannot_silently_move_to_another_fragment(self):
        self.records['fragment']['image_path'] = 'another.png'
        with self.assertRaisesRegex(ValueError, 'does not belong'):
            validate_observation(self.root, self.observation, self.records)

    def test_context_cannot_cite_missing_observation(self):
        check = {'id': 'context', 'record_ids': ['fragment'], 'observation_ids': ['absent']}
        with self.assertRaisesRegex(ValueError, 'Unknown context observation'):
            validate_context_checks([check], {}, self.records)

    def test_context_cannot_attach_another_records_region(self):
        observations = {'region': {'fragment_id': 'other'}}
        check = {'id': 'context', 'record_ids': ['fragment'], 'observation_ids': ['region']}
        with self.assertRaisesRegex(ValueError, 'another record'):
            validate_context_checks([check], observations, self.records)

    def test_comparison_source_cannot_replace_core_record(self):
        core = [{'id': 'fragment', 'image_path': 'leaf.png'}]
        comparator = [{'id': 'fragment', 'image_path': 'unrelated.png'}]
        with self.assertRaisesRegex(ValueError, 'colliding'):
            index_evidence_records(core, comparator)

    def test_comparison_region_uses_its_own_registered_capture(self):
        Image.new('RGB', (60, 70), 'grey').save(self.root / 'comparison.png')
        comparison = {'id': 'comparison-page', 'image_path': None,
                      'captures': [{'path': 'comparison.png'}]}
        records = index_evidence_records([{'id': 'fragment', **self.records['fragment']}], [comparison])
        observation = {'fragment_id': 'comparison-page',
                       'sha256': hashlib.sha256((self.root / 'comparison.png').read_bytes()).hexdigest(),
                       'target': {'source': 'comparison.png', 'selector': {'value': 'xywh=5,10,30,40'}}}
        result = validate_observation(self.root, observation, records)
        self.assertEqual(result['image_dimensions'], [60, 70])
        observation['target']['source'] = 'leaf.png'
        with self.assertRaisesRegex(ValueError, 'does not belong'):
            validate_observation(self.root, observation, records)


if __name__ == '__main__':
    unittest.main()
