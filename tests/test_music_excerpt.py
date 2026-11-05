"""Ambiguity must survive an excerpt comparison rather than improve its score."""
import unittest
from research.continuation_39.compare_notes import compare_slot


class MusicExcerptTests(unittest.TestCase):
    def test_shared_alternative_stays_unresolved(self):
        self.assertEqual(compare_slot([3, 4], [3]), 'unresolved')

    def test_optional_event_is_not_a_matching_note_or_rest(self):
        self.assertEqual(compare_slot([3], [3, None]), 'unresolved')
        self.assertEqual(compare_slot([None], [None]), 'unresolved')

    def test_singleton_positions_can_agree_or_differ(self):
        self.assertEqual(compare_slot([0], [0]), 'agree')
        self.assertEqual(compare_slot([2], [3]), 'different')


if __name__ == '__main__':
    unittest.main()
