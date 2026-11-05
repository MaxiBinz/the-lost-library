import csv
import json
import tempfile
import unittest
import shutil
from pathlib import Path

from lost_library.reconstruction import _relation, build_dossiers, reconstruct

ROOT = Path(__file__).resolve().parents[1]


class SourceBoundReconstructionTests(unittest.TestCase):
    def test_continuities_exist_in_independent_original_source(self):
        with (ROOT / "research/mpo.csv").open(encoding="utf-8-sig", newline="") as stream:
            records = {r["signatur"]: r for r in csv.DictReader(stream)}
        self.assertIn("Fr 7961", records["7960"]["inhalt"])
        self.assertIn("Fr 7960", records["7961"]["inhalt"])
        self.assertIn("Fr 8344", records["8343"]["inhalt"])
        self.assertIn("Fr 8343", records["8344"]["inhalt"])
        self.assertIn("innere Doppelbl", records["8344"]["anmerkungen"])

    def test_unknown_extent_is_not_a_fabricated_page_count(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            reconstruct(root)
            reconstruction = json.loads((root / "data/reconstruction.json").read_text())
            gaps = [x for c in reconstruction["components"] for x in c["items"] if x.get("missing")]
            self.assertTrue(gaps)
            self.assertTrue(all("count" not in x for x in gaps))
            self.assertFalse(reconstruction["music"]["available"])

    def source_passage_fixture(self, root):
        for path in ["data/fragments.json", "research/continuation_36/results.json"]:
            (root / path).parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / path, root / path)

    def test_text_boundaries_select_actual_capture_without_certifying_sides(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.source_passage_fixture(root)
            reconstruct(root)
            reconstruction = json.loads((root / "data/reconstruction.json").read_text())
            first, second, third = reconstruction["components"][:3]
            self.assertEqual(first["items"][1]["image_path"], "data/images/mpo-7960-capture-4.jpg")
            self.assertEqual(second["items"][2]["image_path"], "data/images/mpo-8344-capture-3.jpg")
            self.assertEqual(third["items"][1]["image_path"], "data/images/mpo-8344-capture-2.jpg")
            self.assertEqual(second["source_image_review"], "unresolved")
            self.assertEqual(third["source_image_review"], "supported")
            for component in [first, second, third]:
                self.assertEqual(component["status"], "documented")
                for item in component["items"][1:3]:
                    self.assertFalse(item["representative_image"])
                    self.assertEqual(item["mapping_status"], "provisional_content_based")
                    self.assertTrue(item["passage_evidence"])
                    self.assertIn("without independent confirmation", item["note"])

    def test_unregistered_passage_or_missing_review_cannot_select_an_image(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.source_passage_fixture(root)
            path = root / "research/continuation_36/results.json"
            data = json.loads(path.read_text())
            original = json.loads(path.read_text())
            data["edges"][0]["from_capture"] = "data/images/mpo-7961.jpg"
            path.write_text(json.dumps(data))
            with self.assertRaisesRegex(ValueError, "not a registered capture"):
                reconstruct(root)
            original["edges"].pop()
            path.write_text(json.dumps(original))
            with self.assertRaisesRegex(ValueError, "all three"):
                reconstruct(root)

    def test_published_negative_overrides_maximal_computational_score(self):
        with tempfile.TemporaryDirectory() as temporary:
            fragments = [{"id": f"mpo-{i}", "shelfmark": f"Fr {i}", "normalized": {}, "source_url": "https://example.test/source"} for i in (8201, 8304)]
            matches = [{"left_id": "mpo-8201", "right_id": "mpo-8304", "score": 1.0, "rank": 1, "evidence": [{"signal": "script", "compatibility": 1.0}]}]
            dossiers = build_dossiers(Path(temporary), fragments, matches)
            self.assertEqual(dossiers[0]["classification"], "D")
            self.assertFalse(dossiers[0]["discovery_claim"])
            self.assertTrue(all(isinstance(x, str) for x in dossiers[0]["supporting"]))

    def test_qualified_association_is_not_upgraded_to_proven_match(self):
        category, originality, _, _ = _relation("mpo-1385", "mpo-8994")
        self.assertEqual(category, "C")
        self.assertIn("suggested", originality)

    def test_existing_finnish_suggestion_is_not_rebranded_as_new(self):
        category, originality, _, sources = _relation("finn-iv173", "mpo-25592")
        self.assertEqual(category, "C")
        self.assertIn("Previously suggested", originality)
        self.assertTrue(any("1314" in s for s in sources))


if __name__ == "__main__":
    unittest.main()
