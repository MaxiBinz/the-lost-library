"""Offline integrity and scope checks across the active source investigation."""
import hashlib
import json
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]


def load(name):
    return json.loads((ROOT / name).read_text())


def main():
    comparisons = load('data/comparison_sources.v1.json')
    registration = load('research/continuation_20/registration/feature_results.json')
    assert registration['source_downloads'] == registration['source_mutations'] == 0
    assert not any(r['strong_registration_screen'] for r in registration['results'])
    checked = []
    for record in comparisons:
        sources = [record['image']]
        if record.get('original_source'):
            sources.append(record['original_source'])
        sources.extend(record.get('captures', []))
        seen = set()
        for source in sources:
            if source['path'] in seen:
                continue
            seen.add(source['path'])
            path = ROOT / source['path']
            assert path.is_relative_to(ROOT) and path.is_file()
            assert hashlib.sha256(path.read_bytes()).hexdigest() == source['sha256']
            with Image.open(path) as image:
                assert image.size == (source['width'], source['height'])
            checked.append(source['path'])
    from lost_library.evidence import export_evidence
    export = export_evidence(ROOT)
    bundle = load('data/review_bundle.json')
    ids = {o['id'] for o in bundle['observations']}
    for site in load('research/continuation_20/c23/collation.json')['sites']:
        assert set(site['source_observations']) <= ids
    validation = load('data/validation.json')
    archived = load('data/experiments/v1-initial/validation.json')
    assert validation['results'] == archived['results']
    assert validation['thresholds'] == archived['thresholds']
    core = load('data/fragments.json')
    assert hashlib.sha256((ROOT / 'data/fragments.json').read_bytes()).hexdigest() == '1243131507c1f72652cbb36507d2c9f0f6a24ea99fe9cfafd7c4387d33864080'
    assert len(core) == 129
    assert len(load('data/site.json')['fragments']) == 129
    assert len(bundle['queue']['hypotheses']) == 10
    assert len(bundle['comparison_sources']) == len(comparisons) == 3
    assert {x['id'] for x in comparisons} == {'uub-c23-0144', 'uub-c23-0145', 'mpo-7292'}
    auxiliary = next(x for x in comparisons if x['id'] == 'mpo-7292')
    assert 'excluded from core' in auxiliary['role']
    assert not any(x['new_discovery'] or x['independent_expert_review'] for x in bundle['reviews'])
    result = {'assessment_date': '2026-10-25', 'previous_goal_turn': 'progress: E29 indexed Fragmenta IV.156/IV.157 entries clarify same-codex versus suggested relation labels; integrated into CTX11',
              'current_goal_turn': 'progress: E30 checksum-verified BOMPAC crosswalk separates H08-H10 model suggestions from Fr1385; integrated into dossier review without queue changes',
              'consecutive_no_progress_turns': 0, 'goal_status': 'active, verified by get_goal at turn start',
              'comparison_source_files_hashes_and_dimensions_checked': checked,
              'evidence_export': export, 'core_fragments_unchanged': True,
              'benchmark_results_and_thresholds_unchanged': True,
              'external_pages_excluded_from_core_gallery_and_frozen_queue': True,
              'registration_screen_non_decisive': True,
              'completion_proven': False,
              'limits': ['Integrity checks do not establish historical truth or originality.',
                         'The source sites were inspected post-review; no blind improved-method test.']}
    (ROOT / 'research/continuation_20/check_results.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    import sys
    sys.path.insert(0, str(ROOT))
    main()
