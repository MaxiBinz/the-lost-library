import copy
import math
import unittest

import numpy as np
from PIL import Image, ImageDraw

from lost_library.matching import (METHOD_ORDER, _association, _evaluate_split, _groups, _threshold,
                                   expected_metrics, metadata_score, representative_indices,
                                   sanitize_contents, text_score, validate_reference_objects)
from lost_library.vision import crop_paper, layout_descriptor


class MatchingMethodTests(unittest.TestCase):
    def test_metrics_average_ties_instead_of_using_identifier_order(self):
        result = expected_metrics([1, 1], [True, False], ks=(1, 2))
        self.assertAlmostEqual(result["precision@1"], .5)
        self.assertAlmostEqual(result["hit@1"], .5)
        self.assertAlmostEqual(result["recall@1"], .5)
        self.assertAlmostEqual(result["mrr"], .75)
        self.assertAlmostEqual(result["recall@2"], 1)

    def test_two_positives_in_three_way_tie(self):
        result = expected_metrics([.8, .8, .8], [True, False, True], ks=(1, 2))
        self.assertAlmostEqual(result["hit@1"], 2 / 3)
        self.assertAlmostEqual(result["hit@2"], 1)
        self.assertAlmostEqual(result["precision@2"], 2 / 3)
        self.assertAlmostEqual(result["mrr"], 5 / 6)

    def test_no_positive_query_cannot_be_silently_scored(self):
        with self.assertRaises(ValueError):
            expected_metrics([.9], [False])

    def test_missing_metadata_neutral_and_not_excluded(self):
        score, coverage, evidence = metadata_score({"normalized": {}}, {"normalized": {}})
        self.assertEqual(score, .5)
        self.assertEqual(coverage, 0)
        self.assertEqual(evidence, [])
        partial = {"normalized": {"type": "Antiphonarium", "notation": "Quadr"}}
        score, coverage, _ = metadata_score(partial, partial)
        self.assertGreater(score, .5)
        self.assertLess(score, 1)
        self.assertLess(coverage, 1)

    def test_raw_group_labels_do_not_enter_metadata_predictor(self):
        a = {"collection": "MPO", "normalized": {"type": "Graduale", "lines": 10}, "raw": {"codex": "Codex 1"}}
        b = copy.deepcopy(a)
        baseline = metadata_score(a, b)
        b["raw"] = {"codex": "Codex 999", "ccmsignum": "Secret label", "anmerkungen": "Same codex"}
        b["institution"] = "Different provider"
        b["id"] = "revealing-book-name"
        self.assertEqual(metadata_score(a, b), baseline)

    def test_explicit_relationship_content_is_removed(self):
        text = "Dom. in L (Beginn in Fr 7960, 2v); Fer.VI."
        tokens = sanitize_contents(text)
        self.assertNotIn("beginn", tokens)
        self.assertNotIn("fr", tokens)
        self.assertFalse(any(any(c.isdigit() for c in token) for token in tokens))

    def test_cross_collection_dimension_conventions_are_not_equated(self):
        a = {"collection": "MPO", "normalized": {"leaf_cm": [49, 34]}}
        b = {"collection": "Fragmenta", "normalized": {"leaf_cm": [34, 23]}}
        self.assertEqual(metadata_score(a, b)[:2], (.5, 0))

    def test_physical_record_cannot_cross_book_splits(self):
        benchmark = {"groups": [{"id": "one", "split": "development", "member_ids": ["a", "b"]},
                                 {"id": "two", "split": "test", "member_ids": ["a", "c"]}]}
        with self.assertRaises(ValueError):
            _groups(benchmark, {"a", "b", "c"})

    def test_empty_calibration_conservatively_rejects(self):
        self.assertGreater(_threshold([])["threshold"], 1)

    def test_alternate_captures_have_one_physical_representative(self):
        records = [{"id": "leaf-verso", "physical_object_id": "leaf"},
                   {"id": "leaf", "physical_object_id": "leaf"}, {"id": "other"}]
        self.assertEqual(representative_indices(records), [1, 2])

    def test_exact_capture_aliases_cannot_enter_reference_benchmark(self):
        records = [{"id": "a", "image": {"sha256": "same"}},
                   {"id": "b", "image": {"sha256": "same"}}]
        with self.assertRaises(ValueError):
            validate_reference_objects(records, [{"member_ids": ["a", "b"]}])

    def test_single_book_genre_is_excluded_from_retrieval_accuracy(self):
        records = [{"id": x, "normalized": {"type": "Antiphonarium" if x in "ab" else "Graduale"}}
                   for x in "abcdef"]
        groups = [{"id": name, "split": "development", "member_ids": list(ids)}
                  for name, ids in [("one", "ab"), ("two", "cd"), ("three", "ef")]]
        matrices = {method: np.eye(6) for method in METHOD_ORDER}
        result = _evaluate_split(records, matrices, groups, "development", True)
        self.assertEqual(result["reference_book_count"], 3)
        self.assertEqual(result["book_count"], 2)
        self.assertEqual(len(result["excluded_queries"]), 2)
        self.assertEqual(result["methods"]["metadata"]["query_count"], 4)

    def test_transcription_placeholder_is_not_text_evidence(self):
        record = {"normalized": {"contents": "Liturgical missal fragment; text not independently transcribed for matching"}}
        self.assertEqual(text_score(record, record), .5)

    def test_conflicted_catalogue_group_is_documented_not_new(self):
        a = {"id": "mpo-8201", "raw": {"codex": "Codex 1146"}}
        b = {"id": "mpo-8072", "raw": {"codex": "Codex 1146"}}
        self.assertEqual(_association(a, b)[0], "E")
        b["id"] = "mpo-8304"
        self.assertEqual(_association(a, b)[0], "D")

    def test_visual_descriptor_is_deterministic_and_not_a_staff_count(self):
        image = Image.new("RGB", (320, 400), "black")
        draw = ImageDraw.Draw(image)
        draw.rectangle((25, 25, 295, 375), fill=(220, 210, 180))
        for y in range(60, 330, 20):
            draw.line((45, y, 270, y), fill=(150, 40, 40), width=2)
        cropped, info = crop_paper(image)
        a, stats = layout_descriptor(cropped)
        b, _ = layout_descriptor(cropped)
        self.assertTrue(np.array_equal(a, b))
        self.assertTrue(np.isfinite(a).all())
        self.assertGreater(stats["red_density"], 0)
        self.assertFalse(info["is_original_leaf_measurement"])
        self.assertIn("not measured physical", stats["interpretation"])


if __name__ == "__main__":
    unittest.main()
