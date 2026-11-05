"""Scientific/provenance invariants for the real manuscript data pipeline."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from lost_library.pipeline import (
    Fetcher, build_database, make_sample_plan, normalize_mpo, parse_date,
    parse_dimension, parse_manifest, permitted_rights, search,
)


class NormalizationTests(unittest.TestCase):
    def test_century_half_is_not_misread_as_first_or_second_century(self):
        self.assertEqual(parse_date("14. Jh. 1. Hälfte"),(1300,1349))
        self.assertEqual(parse_date("15. Jh. 2. Hälfte"),(1450,1499))
        self.assertEqual(parse_date("12.-13. Jh."),(1100,1299))
        self.assertEqual(parse_date("1397-1406"),(1397,1406))
        self.assertEqual(parse_date(""),(None,None))

    def test_qualified_observed_measurements_do_not_replace_raw_source(self):
        row={"format":"*43.5 x 32.0","schriftraum1":"34.0 x 23.0", "datierung":"15. Jh.","zeilenzahl1":"#11"}
        normalized=normalize_mpo(row)
        self.assertEqual(normalized['leaf_cm'],[43.5,32.0])
        self.assertEqual(normalized['written_cm'],[34.0,23.0])
        self.assertEqual(row['format'],'*43.5 x 32.0')
        self.assertEqual(row['zeilenzahl1'],'#11')
        self.assertIsNone(parse_dimension("unrecorded"))
        self.assertIsNone(normalized['columns'])


class ManifestAndRightsTests(unittest.TestCase):
    def test_real_v3_manifest_retains_capture_count_not_leaf_count(self):
        path=Path(__file__).resolve().parents[1]/'research/evidence/mpo_8201_manifest.json'
        info=parse_manifest(json.loads(path.read_text()))
        self.assertEqual(info['canvas_count'],4)
        self.assertTrue(info['canvas_id'].endswith('R1008201_00001/canvas'))
        self.assertTrue(permitted_rights(info['rights']))

    def test_real_child_v2_rights_are_not_inherited_from_composite(self):
        root=Path(__file__).resolve().parents[1]/'research/evidence'
        pdm=parse_manifest(json.loads((root/'F-6zvk_manifest.json').read_text()))
        nkc=parse_manifest(json.loads((root/'F-g7p5_manifest.json').read_text()))
        self.assertTrue(permitted_rights(pdm['rights']))
        self.assertFalse(permitted_rights(nkc['rights']))
        self.assertFalse(permitted_rights('https://creativecommons.org/licenses/by-nc/4.0/'))

    def test_offline_and_host_allowlist_prevent_unintended_fetches(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            with mock.patch('urllib.request.urlopen') as network:
                with self.assertRaises(FileNotFoundError):
                    Fetcher(root,offline=True).get('https://lbiiif.riksarkivet.se/a',root/'a')
                with self.assertRaises(ValueError):
                    Fetcher(root).get('http://127.0.0.1/private',root/'b')
                network.assert_not_called()


class DataSelectionAndSearchTests(unittest.TestCase):
    def test_false_catalogue_group_is_never_a_benchmark_positive(self):
        root=Path(__file__).resolve().parents[1]
        plan=make_sample_plan(root,120,offline=True)
        labels={g['source_label'] for g in plan['groups']}
        self.assertNotIn('Codex 1146',labels)
        self.assertNotIn('Codex 1505',labels)
        identifiers=[r['id'] for r in plan['mpo_records']]
        self.assertEqual(len(identifiers),len(set(identifiers)))
        self.assertEqual(len(plan['groups']),10)
        self.assertTrue(all(len(g['member_ids'])==6 for g in plan['groups']))
        split_members={split:{x for g in plan['groups'] if g['split']==split for x in g['member_ids']}
                       for split in ('development','calibration','test')}
        self.assertFalse(split_members['development'] & split_members['test'])
        self.assertFalse(split_members['calibration'] & split_members['test'])

    def test_sqlite_unicode_search_retains_original_json(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);(root/'data').mkdir()
            record={'id':'sample-1','shelfmark':'Verified source identifier','institution':'Library',
                    'collection':'Source','role':'control','image_path':None,
                    'normalized':{'contents':'Åbo antiphonal'},'raw':{'qualified':'original?'}}
            build_database(root,[record])
            hits=search(root,'Åbo')
            self.assertEqual(hits,[record])
            self.assertEqual(search(root,'unrepresented'),[])


if __name__=='__main__':
    unittest.main()
