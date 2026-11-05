"""Build and verify a local review archive with an explicit asset allowlist.

No GitHub, hosting, uploads or external messages. Private scholarly PDFs,
environments, model weights and historical image probes are excluded. The
Finnish source PDF is included under its recorded Public Domain Mark statement
because cached ingestion verifies it even when derivatives already exist.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import zipfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def selected_files():
    files = set(ROOT.glob('*.md'))
    files.update(ROOT / x for x in ['.gitignore', 'requirements.txt', 'pyproject.toml'])
    for folder, suffixes in [('lost_library', {'.py'}), ('tests', {'.py', '.cjs'}),
                             ('viewer', {'.html', '.js', '.css', '.md'}),
                             ('data', {'.json', '.jsonld', '.npz', '.sqlite', '.py'}),
                             ('research', {'.py', '.md', '.json', '.csv', '.ipynb', '.ris'})]:
        files.update(p for p in (ROOT / folder).rglob('*') if p.is_file() and p.suffix in suffixes
                     and '__pycache__' not in p.parts and 'models' not in p.parts)
    records = json.loads((ROOT / 'data/fragments.json').read_text())
    comparison_path = ROOT / 'data/comparison_sources.v1.json'
    if comparison_path.exists():
        records += json.loads(comparison_path.read_text())
    images = {r['image_path']: r for r in records if r.get('image_path')}
    for r in records:
        images.update({c['path']: r for c in r.get('captures', []) if c.get('path')})
    from lost_library.pipeline import permitted_rights
    for path, record in images.items():
        if not permitted_rights(record.get('rights_url', '')):
            raise ValueError(f'Working image has unsupported release rights: {path}')
        files.add(ROOT / path)
    for record in records:
        original = record.get('original_source', {}).get('path')
        if original:
            if not permitted_rights(record.get('rights_url', '')):
                raise ValueError(f'Comparison original has unsupported rights: {original}')
            files.add(ROOT / original)
    comparison_rights_receipt = ROOT / 'research/continuation_20/c23/institutional-record.ax.txt'
    if comparison_rights_receipt.exists():
        files.add(comparison_rights_receipt)
    files.add(ROOT / 'research/evidence/F_m_IV_173.pdf')
    # These two CC BY 4.0 workbooks are the exact inputs to E26/E27/E30
    # crosswalks. Include them so the prior-art queries reproduce offline;
    # underlying manuscript-image rights are not implied by this dataset licence.
    files.add(ROOT / 'research/continuation_26/bompac/Stockholm-Helsinki-Frs-Combined-BOMPAC.xlsx')
    files.add(ROOT / 'research/continuation_26/bompac/raw_metadata/MPO_BOMPAC.xlsx')
    # A retained browser proof contains only our local interface and the PDM
    # Swedish source image. Private article renderings remain excluded.
    proof = ROOT / 'research/independent_pass/viewer/latin-region.png'
    if proof.exists():
        files.add(proof)
    # E35/E36 diagnostics contain only labelled regions of the existing PDM
    # Swedish captures. They document the source tests and add no new source.
    for folder in ['continuation_35', 'continuation_36']:
        files.update((ROOT / 'research' / folder).glob('*.png'))
    # Only this E37 figure contains PDM source pixels. Its private scholarly
    # PDF/page renders and complete extracted text must remain excluded.
    files.add(ROOT / 'research/continuation_37/magnificat-comparison.png')
    files.add(ROOT / 'research/continuation_38/replacement-comparison.png')
    files.add(ROOT / 'research/continuation_38/c23-record.ax.txt')
    files.add(ROOT / 'research/continuation_38/c23-69r-viewer.ax.txt')
    # Keep E39's public-domain manuscript proof; never glob its private
    # method/dissertation page renders into the review archive.
    files.add(ROOT / 'research/continuation_39/note-review.png')
    files.add(ROOT / 'research/continuation_40/boundary-review.png')
    # E41 figures expose only raw pixels from the already permitted PDM set.
    for name in ['8994-1-2-raw-patches.png', '8994-3-4-raw-patches.png',
                 '20274-overlap-positive-raw-patches.png', '8994-1-3-nonrepeat-raw-patches.png']:
        files.add(ROOT / 'research/continuation_41' / name)
    for name in ['row-coverage-overview.png', 'boundary-text-review.png']:
        files.add(ROOT / 'research/continuation_42' / name)
    for capture in json.loads((ROOT / 'research/continuation_44/captures.json').read_text())['captures']:
        if not permitted_rights(capture['rights_url']):
            raise ValueError('Unsupported E44 capture rights')
        files.add(ROOT / capture['path'])
    for name in ['ruling-review.png','text-review.png']:
        files.add(ROOT / 'research/continuation_44' / name)
    # Local interface and PDM manuscript pixels only; no outside webpage text.
    for name in ['e44-rubric-region.png','e44-source-box.png']:
        files.add(ROOT / 'output/research' / name)
    for name in ['service-review.png','parallel-text-review.png']:
        files.add(ROOT / 'research/continuation_45' / name)
    for name in ['note-review.png','context-review.png']:
        files.add(ROOT / 'research/continuation_46' / name)
    files.add(ROOT / 'research/continuation_49/rubric-review.png')
    files.add(ROOT / 'research/continuation_58/seam-review.png')
    files.add(ROOT / 'research/continuation_60/swedish-head.png')
    for capture in json.loads((ROOT / 'research/continuation_50/captures.json').read_text())['captures']:
        if not permitted_rights(capture['rights_url']):
            raise ValueError('Unsupported E50 source rights')
        files.add(ROOT / capture['path'])
    files.add(ROOT / 'research/continuation_50/layout-review.png')
    files.add(ROOT / 'research/continuation_51/mark-review.png')
    for capture in json.loads((ROOT / 'research/continuation_52/captures.json').read_text())['captures']:
        if not permitted_rights(capture['rights_url']):
            raise ValueError('Unsupported E52 source rights')
        files.add(ROOT / capture['path'])
    files.add(ROOT / 'research/continuation_52/text-review.png')
    files.add(ROOT / 'research/continuation_53/hymn-review.png')
    for capture in json.loads((ROOT / 'research/continuation_54/captures.json').read_text())['captures']:
        if not permitted_rights(capture['rights_url']):
            raise ValueError('Unsupported E54 source rights')
        files.add(ROOT / capture['path'])
    for capture in json.loads((ROOT / 'research/continuation_65/captures.json').read_text())['captures']:
        if not permitted_rights(capture['rights_url']):
            raise ValueError('Unsupported E65 source rights')
        files.add(ROOT / capture['path'])
    files.add(ROOT / 'research/continuation_54/mark-review.png')
    files.add(ROOT / 'research/continuation_55/staff-review.png')
    files.add(ROOT / 'research/continuation_56/TMMA_fragC.xml')
    return sorted(files)


def main():
    # Permit direct execution without installing the project as a package.
    sys.path.insert(0, str(ROOT))
    output = ROOT / 'output/research'
    output.mkdir(parents=True, exist_ok=True)
    archive = output / 'lost-library-review.zip'
    staged_archive = output / 'lost-library-review.staged.zip'
    files = selected_files()
    entries = [{'path': str(p.relative_to(ROOT)), 'bytes': p.stat().st_size,
                'sha256': sha(p.read_bytes())} for p in files]
    manifest = {'created_at_utc': datetime.now(timezone.utc).isoformat(),
                'audience': 'Research review snapshot; source rights are tracked per item',
                'files': entries,
                'exclusions': ['Python environment', 'model weights', 'private scholarly PDFs',
                               'historical image probes outside the permitted working set',
                               'temporary rendering previews'],
                'code_licence': 'Owner selection pending; third-party rights remain separate'}
    raw_manifest = (json.dumps(manifest, ensure_ascii=False, indent=2) + '\n').encode()
    with zipfile.ZipFile(staged_archive, 'w', zipfile.ZIP_DEFLATED) as zipped:
        for p in files:
            zipped.write(p, str(p.relative_to(ROOT)))
        zipped.writestr('PACKAGE_MANIFEST.json', raw_manifest)
    with zipfile.ZipFile(staged_archive) as zipped:
        if zipped.testzip() is not None:
            raise ValueError('Archive integrity test failed')
        for item in entries:
            if sha(zipped.read(item['path'])) != item['sha256']:
                raise ValueError(f"Archive checksum mismatch: {item['path']}")
        forbidden = [p for p in zipped.namelist() if p.endswith('.pth') or
                     (p.endswith('.pdf') and p != 'research/evidence/F_m_IV_173.pdf') or '.venv/' in p]
        if forbidden:
            raise ValueError(f'Forbidden private/runtime assets in archive: {forbidden}')
        with tempfile.TemporaryDirectory(prefix='lost-library-replay-') as temp:
            target = Path(temp)
            zipped.extractall(target)
            knowledge = subprocess.run([sys.executable, '-m', 'lost_library', 'knowledge', 'validate'],
                                       cwd=target, capture_output=True, text=True, timeout=30)
            (output / 'archive_knowledge_validation.log').write_text(knowledge.stdout + knowledge.stderr)
            if knowledge.returncode:
                raise RuntimeError('Extracted knowledge validation failed; see saved log')
            # Private reading PDFs are intentionally absent. E37's default
            # mode reports that absence while checking the shareable evidence;
            # E38 must also reproduce using only the included source assets.
            source_logs = []
            for script in ['research/continuation_37/check_sources.py',
                           'research/continuation_38/check_sources.py',
                           'research/continuation_39/check_sources.py',
                           'research/continuation_40/check_sources.py',
                           'research/continuation_41/check_sources.py',
                           'research/continuation_42/check_sources.py',
                           'research/continuation_43/check_sources.py',
                           'research/continuation_44/check_sources.py',
                           'research/continuation_45/check_sources.py',
                           'research/continuation_46/check_sources.py',
                           'research/continuation_47/check_sources.py',
                           'research/continuation_48/check_sources.py',
                           'research/continuation_49/check_sources.py',
                           'research/continuation_50/check_sources.py',
                           'research/continuation_51/check_sources.py',
                           'research/continuation_52/check_sources.py',
                           'research/continuation_53/check_sources.py',
                           'research/continuation_54/check_sources.py',
                           'research/continuation_55/check_sources.py',
                           'research/continuation_56/check_sources.py',
                           'research/continuation_57/check_sources.py',
                           'research/continuation_58/check_sources.py',
                           'research/continuation_59/check_sources.py',
                           'research/continuation_60/check_sources.py',
                           'research/continuation_61/check_sources.py',
                           'research/continuation_62/check_sources.py',
                           'research/continuation_63/check_sources.py',
                           'research/continuation_64/check_sources.py',
                           'research/continuation_65/check_sources.py',
                           'research/continuation_66/check_sources.py',
                           'research/continuation_67/check_sources.py',
                           'research/continuation_69/check_sources.py',
                           'research/continuation_70/check_sources.py',
                           'research/continuation_71/check_sources.py',
                           'research/continuation_72/check_sources.py',
                           'research/continuation_73/check_sources.py',
                           'research/continuation_74/check_sources.py',
                           'research/continuation_75/check_sources.py',
                           'research/continuation_76/check_sources.py',
                           'research/continuation_77/check_sources.py',
                           'research/continuation_78/check_sources.py',
                           'research/continuation_79/check_sources.py',
                           'research/continuation_80/check_sources.py',
                           'research/continuation_85/check_sources.py',
                           'research/continuation_96/check.py',
                           'research/continuation_97/check.py',
                           'research/continuation_99/audit.py',
                           'research/continuation_108/audit.py',
                           'research/continuation_111/check_missingness.py',
                           'research/continuation_112/check.py',
                           'research/continuation_113/audit.py',
                           'research/continuation_114/audit.py']:
                checked = subprocess.run([sys.executable, script], cwd=target,
                                         capture_output=True, text=True, timeout=30)
                source_logs.append(script + '\n' + checked.stdout + checked.stderr)
                (output / 'archive_source_checks.log').write_text('\n'.join(source_logs))
                if checked.returncode:
                    raise RuntimeError('Extracted source checks failed; see saved log')
            for result_path in ['research/continuation_108/results.json',
                                'research/continuation_111/results.json',
                                'research/continuation_113/results.json',
                                'research/continuation_114/results.json']:
                if json.loads((target / result_path).read_text()) != json.loads((ROOT / result_path).read_text()):
                    raise ValueError(f'Extracted calculation changed saved findings: {result_path}')
            process = subprocess.run([sys.executable, '-m', 'lost_library', 'run', '--offline'],
                                     cwd=target, capture_output=True, text=True, timeout=90)
            (output / 'archive_offline_replay.log').write_text(process.stdout + process.stderr)
            if process.returncode:
                raise RuntimeError('Extracted archive replay failed; see saved log')
            original = json.loads((ROOT / 'data/validation.json').read_text())
            replay = json.loads((target / 'data/validation.json').read_text())
            if original['results'] != replay['results'] or original['thresholds'] != replay['thresholds']:
                raise ValueError('Archive replay changed scientific metrics')
            if json.loads((target / 'data/evidence_experiment.json').read_text()) != json.loads((ROOT / 'data/evidence_experiment.json').read_text()):
                raise ValueError('Archive replay changed frozen case-screen results')
    staged_archive.replace(archive)
    (output / 'package_manifest.json').write_bytes(raw_manifest)
    result = {'archive': str(archive.relative_to(ROOT)), 'files': len(files),
              'bytes': archive.stat().st_size, 'sha256': sha(archive.read_bytes()),
              'archive_checksums_verified': True, 'extracted_offline_replay': 'passed',
              'extracted_knowledge_validation': 'passed',
              'extracted_e108_e111_e113_results_reproduced': 'passed',
              'extracted_e112_image_selectors_checked': 'passed',
              'extracted_e114_csv_field_comparison_reproduced': 'passed',
              'extracted_e37_e38_source_checks': 'passed',
              'extracted_e39_source_checks': 'passed',
              'extracted_e40_source_checks': 'passed',
              'extracted_e41_source_checks': 'passed',
              'extracted_e42_source_checks': 'passed',
              'extracted_e43_source_checks': 'passed',
              'extracted_e44_source_checks': 'passed',
              'extracted_e45_source_checks': 'passed',
              'extracted_e46_source_checks': 'passed',
              'extracted_e47_source_checks': 'passed',
              'extracted_e48_source_checks': 'passed',
              'extracted_e49_source_checks': 'passed',
              'extracted_e50_source_checks': 'passed',
              'extracted_e51_source_checks': 'passed',
              'extracted_e52_source_checks': 'passed',
              'extracted_e53_source_checks': 'passed',
              'extracted_e54_source_checks': 'passed',
              'extracted_e55_source_checks': 'passed',
              'extracted_e56_source_checks': 'passed',
              'extracted_e57_source_checks': 'passed',
              'extracted_e58_source_checks': 'passed',
              'extracted_e59_source_checks': 'passed',
              'extracted_e60_source_checks': 'passed',
              'extracted_e61_source_checks': 'passed',
              'extracted_e62_source_checks': 'passed',
              'extracted_e63_source_checks': 'passed',
              'extracted_e64_source_checks': 'passed',
              'extracted_e65_source_checks': 'passed',
              'extracted_e66_source_checks': 'passed',
              'extracted_e67_source_checks': 'passed',
              'extracted_e69_source_checks': 'passed',
              'extracted_e70_source_checks': 'passed',
              'extracted_e71_source_checks': 'passed',
              'extracted_e72_source_checks': 'passed',
              'extracted_e73_source_checks': 'passed',
              'extracted_e74_source_checks': 'passed',
              'extracted_e75_source_checks': 'passed',
              'extracted_e76_source_checks': 'passed',
              'extracted_e77_source_checks': 'passed',
              'extracted_e78_source_checks': 'passed',
              'extracted_e79_source_checks': 'passed',
              'extracted_e80_source_checks': 'passed',
              'extracted_e85_source_checks': 'passed',
              'extracted_e96_source_checks': 'passed',
              'extracted_e97_source_checks': 'passed',
              'extracted_e99_source_audit': 'passed',
              'scientific_metrics_unchanged': True, 'frozen_screen_results_unchanged': True}
    (output / 'package_verification.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
