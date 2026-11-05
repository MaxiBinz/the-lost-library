"""Offline integrity audit and frozen source-first research queue, version 1.

Run with the project Python. No downloads, fitting, or expert adjudication.
Existing queue files are verified rather than silently reselected.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path, obj):
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')


def main():
    records = json.loads((ROOT / 'data/fragments.json').read_text())
    by_id = {r['id']: r for r in records}
    matches = json.loads((ROOT / 'data/matches.json').read_text())
    validation = json.loads((ROOT / 'data/validation.json').read_text())
    images = {}
    failures = []
    for r in records:
        captures = list(r.get('captures', []))
        if r.get('image_path'):
            captures.append({'path': r['image_path'], **(r.get('image') or {})})
        for capture in captures:
            name = capture.get('path')
            if not name:
                continue
            previous = images.get(name)
            if previous and previous.get('sha256') != capture.get('sha256'):
                failures.append({'path': name, 'reason': 'conflicting recorded hashes'})
            images[name] = capture
    for name, capture in images.items():
        p = (ROOT / name).resolve()
        if not p.is_relative_to(ROOT) or not p.is_file():
            failures.append({'path': name, 'reason': 'missing or unsafe image path'})
            continue
        if not capture.get('sha256') or sha(p) != capture['sha256']:
            failures.append({'path': name, 'reason': 'missing or changed image hash'})
        with Image.open(p) as image:
            if list(image.size) != [capture.get('width'), capture.get('height')]:
                failures.append({'path': name, 'reason': 'image dimensions changed'})
    assert len(by_id) == len(records), 'Duplicate record identifiers'
    assert not failures, f'Missing or altered source images: {failures}'
    assert len(images) <= 300
    # Freeze top three unestablished suggestions for one preselected query.
    new_pairs = [m for m in matches if m['left_id'] == 'mpo-1385'
                 and m['originality'] == 'not established'][:3]
    assert len(new_pairs) == 3
    fixed = [
        ('mpo-1385', 'mpo-20274', 'accepted', 'E',
         'Known same-codex target-transfer control; low retrieval rank is a failure to explain.',
         'Catalogue contents concern different liturgical occasions: do not demand literal text identity.',
         'https://fragmenta.kansalliskirjasto.fi/handle/10024/1300?show=full'),
        ('mpo-1385', 'mpo-10406', 'suggested', 'C',
         'Same book versus shared production in the already published comparison.',
         'Compare distinctive script/ruling and chant positions; apparent resemblance is already known.',
         'https://zenodo.org/records/17287665'),
        ('mpo-20274', 'mpo-8994', 'suggested', 'C',
         'Ant 99 versus Codex 1505: test book identity rather than regional liturgical overlap.',
         'Check source sides and contradictions; sharing regional chant tradition is insufficient.',
         'https://zenodo.org/records/17287665'),
        ('finn-iv173', 'mpo-1385', 'suggested', 'C',
         'Does the terminal IV.173 leaf fit the already suggested IV.157 family?',
         'Require independent codicological evidence; terminal Te Deum is not a distinctive identity signal.',
         'https://fragmenta.kansalliskirjasto.fi/handle/10024/1314?show=full'),
        ('finn-iv173', 'mpo-25592', 'suggested', 'C',
         'Test the Hy 49 alias against the different observed layout and catalogue date.',
         'Resolve alias/date/composite-book alternatives before declaring physical incompatibility.',
         'https://fragmenta.kansalliskirjasto.fi/handle/10024/1314?show=full'),
        ('mpo-8201', 'mpo-8304', 'rejected', 'D',
         'Published same-hand/different-book falsification control.',
         'Reproduce rejection from scholarly/textual evidence, not a score adjusted to this known label.',
         'https://doi.org/10.25167/ls.4818'),
        ('mpo-8201', 'mpo-20106', 'accepted', 'E',
         'Published positive control whose second image is unavailable.',
         'No visual conclusion without the missing image; assess legitimate textual source evidence.',
         'https://doi.org/10.25167/ls.4818'),
    ]
    queue = []
    for a, b, prior, category, question, falsifier, source in fixed:
        queue.append(dict(left_id=a, right_id=b, prior_status=prior,
                          classification=category, question=question,
                          falsification_test=falsifier, source=source))
    for m in new_pairs:
        queue.append(dict(left_id=m['left_id'], right_id=m['right_id'],
                          prior_status='unestablished model suggestion; novelty not cleared',
                          classification='C', question='Can independent evidence support this model suggestion?',
                          falsification_test='Inspect source notes, chant positions, script and ruling; test different-book alternatives.',
                          source='data/matches.json', initial_rank_interval=m['rank_interval'],
                          initial_score=m['score']))
    for i, q in enumerate(queue, 1):
        q.update(id=f'H{i:02}', review_state='pending source/region investigation',
                 originality='not independently cleared', independent_expert_review=False,
                 observations=[], alternatives=['same codex', 'different books sharing production or liturgy',
                                                 'catalogue/capture identity error'])
        q['objects'] = [{
            'id': x, 'physical_object_id': by_id[x].get('physical_object_id', x),
            'image_path': by_id[x].get('image_path'),
            'image_sha256': (by_id[x].get('image') or {}).get('sha256'),
            'catalogue_contents_literal': by_id[x].get('normalized', {}).get('contents'),
            'reading_status': 'catalogue assertion; not an image transcription',
            'side_mapping': 'unverified source capture; no folio-side inferred',
        } for x in (q['left_id'], q['right_id'])]
    queue_file = ROOT / 'data/hypotheses.v1.json'
    selection = [(q['left_id'], q['right_id']) for q in queue]
    if queue_file.exists():
        prior = json.loads(queue_file.read_text())
        assert selection == [(q['left_id'], q['right_id']) for q in prior['hypotheses']], 'Frozen queue changed'
    else:
        write(queue_file, dict(version='1.0.0', frozen_date='2026-10-21',
                              selection_rule='Seven explicit controls/previous suggestions plus the first three unestablished suggestions in the saved Fr1385 ranking. Exploratory, not blind selection.',
                              matches_sha256=sha(ROOT / 'data/matches.json'),
                              hypotheses=queue))
    audit = dict(assessment_date=datetime.now(timezone.utc).date().isoformat(), records=len(records),
                 imaged_physical_objects=len({r.get('physical_object_id', r['id']) for r in records if r.get('image_path')}),
                 primary_analysis_images=sum(bool(r.get('image_path')) for r in records),
                 source_image_files=len(images), image_hash_failures=failures,
                 source_image_hashes_and_dimensions_checked=len(images),
                 feature_images=json.loads((ROOT / 'data/features.json').read_text())['images_processed'],
                 ranked_suggestions=len(matches), frozen_hypotheses=len(queue),
                 validation_scope=validation['scope'],
                 metadata_input_sha256=sha(ROOT / 'research/mpo.csv'),
                 fragments_sha256=sha(ROOT / 'data/fragments.json'),
                 hypotheses_sha256=sha(queue_file),
                 limitations=['Hash integrity is not attribution truth.',
                              'Previously inspected evaluation remains exploratory.',
                              'The inventory counts captures separately from physical objects.'])
    write(ROOT / 'data/evidence_audit.json', audit)
    print(json.dumps(audit, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
