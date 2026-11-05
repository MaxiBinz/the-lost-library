"""Validate traceable observations and export the complete frozen review queue.

This is evidence bookkeeping, not a learned attribution classifier. Existing
scholarly decisions remain reference evidence, never independent AI discoveries.
"""
from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path

from PIL import Image


def _load(root, name):
    return json.loads((root / name).read_text())


def _sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def index_evidence_records(core_records, comparison_sources):
    """Index inspectable sources without letting comparators replace core data."""
    if not isinstance(core_records, list) or not isinstance(comparison_sources, list):
        raise ValueError('Evidence source collections must be lists')
    records = {}
    for collection in (core_records, comparison_sources):
        for record in collection:
            ident = record['id']
            if ident in records:
                raise ValueError('Duplicate or colliding evidence source identifier')
            records[ident] = record
    return records


def validate_observation(root, observation, records):
    """Reject altered, unrelated, missing or out-of-image evidence regions."""
    ident = observation['fragment_id']
    if ident not in records:
        raise ValueError('Observation fragment is absent')
    target = observation['target']
    source = target['source']
    record = records[ident]
    permitted = {record.get('image_path')} | {c.get('path') for c in record.get('captures', [])}
    if source not in permitted:
        raise ValueError('Observation source does not belong to this fragment')
    path = (root / source).resolve()
    if not path.is_relative_to(root.resolve()) or not path.is_file():
        raise ValueError('Missing or unsafe observation source')
    if _sha(path) != observation['sha256']:
        raise ValueError('Observation source hash changed')
    selector = target['selector']['value']
    if not selector.startswith('xywh='):
        raise ValueError('Unsupported selector')
    box = [int(x) for x in selector[5:].split(',')]
    if len(box) != 4:
        raise ValueError('Region must have four coordinates')
    x, y, width, height = box
    with Image.open(path) as image:
        iw, ih = image.size
    if min(x, y) < 0 or min(width, height) <= 0 or x + width > iw or y + height > ih:
        raise ValueError('Observation region is outside its source image')
    return {**observation, 'region': box, 'image_dimensions': [iw, ih]}


def validate_context_checks(checks, observations, records):
    """Keep auxiliary evidence traceable without adding attribution hypotheses."""
    if len({c['id'] for c in checks}) != len(checks):
        raise ValueError('Duplicate context identifiers')
    result = []
    for check in checks:
        if any(i not in records for i in check['record_ids']):
            raise ValueError('Unknown context record')
        if any(i not in observations for i in check['observation_ids']):
            raise ValueError('Unknown context observation')
        selected = [observations[i] for i in check['observation_ids']]
        if any(o['fragment_id'] not in check['record_ids'] for o in selected):
            raise ValueError('Context observation belongs to another record')
        result.append({**check, 'observations': selected})
    return result


def export_evidence(root: Path):
    root = Path(root).resolve()
    queue_path = root / 'data/hypotheses.v1.json'
    queue = _load(root, 'data/hypotheses.v1.json')
    document = _load(root, 'data/hypothesis_reviews.v1.json')
    if document['queue_sha256'] != _sha(queue_path):
        raise ValueError('Reviews do not refer to the frozen hypothesis queue')
    hypotheses = queue['hypotheses']
    reviews = document['reviews']
    if len(hypotheses) > 10 or len({r['id'] for r in reviews}) != len(reviews):
        raise ValueError('Queue limit or duplicate review violation')
    if {r['id'] for r in reviews} != {r['id'] for r in hypotheses}:
        raise ValueError('Every frozen hypothesis must have exactly one review')
    core_records = _load(root, 'data/fragments.json')
    comparison_path = root / 'data/comparison_sources.v1.json'
    comparison_sources = _load(root, 'data/comparison_sources.v1.json') if comparison_path.exists() else []
    records = index_evidence_records(core_records, comparison_sources)
    core_ids = {r['id'] for r in core_records}
    if any(h[k] not in core_ids for h in hypotheses for k in ('left_id', 'right_id')):
        raise ValueError('Frozen hypothesis refers to a comparison source or unknown record')
    annotations = _load(root, document['observations_path'])['annotations']
    observations = [validate_observation(root, o, records) for o in annotations]
    if len({o['id'] for o in observations}) != len(observations):
        raise ValueError('Duplicate observation identifiers')
    by_id = {o['id']: o for o in observations}
    context_path = document.get('context_checks_path')
    context_checks = validate_context_checks(
        _load(root, context_path)['checks'] if context_path else [], by_id, records)
    validation = _load(root, 'data/validation.json')
    from .matching import metadata_score
    threshold = validation['thresholds']['metadata']['threshold']
    results, dossiers, markdown = [], [], [
        '# Evidence dossiers — frozen review queue', '',
        f"Assessment updated: {document['assessment_date']}. All ten comparisons received a local AI-assisted screen. "
        'No independent expert has adjudicated them. No original attribution is confirmed.', '',
        'Category and originality are separate. A source-supported reference decision is not '
        'a new model prediction. A C outcome is unresolved, not a demonstrated different book.', '',
    ]
    for h in hypotheses:
        review = next(r for r in reviews if r['id'] == h['id'])
        if (review['left_id'], review['right_id']) != (h['left_id'], h['right_id']):
            raise ValueError('Review pair or orientation changed')
        if review['new_discovery'] and not review['independent_expert_review']:
            raise ValueError('Unreviewed finding cannot be called independently confirmed')
        if any(i not in by_id for i in review['observation_ids']):
            raise ValueError('Unknown observation reference')
        if any(by_id[i]['fragment_id'] not in (h['left_id'], h['right_id']) for i in review['observation_ids']):
            raise ValueError('Observation refers to another pair')
        a, b = records[h['left_id']], records[h['right_id']]
        evaluable = bool(a.get('image_path') and b.get('image_path'))
        score = metadata_score(a, b)[0] if evaluable else None
        decision = 'reference-supported acceptance' if review['classification'] == 'E' else 'published rejection' if review['classification'] == 'D' else 'abstain: insufficient evidence'
        row = {'id': h['id'], 'left_id': h['left_id'], 'right_id': h['right_id'],
               'image_evaluable': evaluable, 'metadata_score': score,
               'baseline_threshold_accepts': score >= threshold if evaluable else None,
               'evidence_screen_decision': decision, 'classification': review['classification'],
               'new_discovery': review['new_discovery']}
        results.append(row)
        dossier = {**h, **review, 'baseline': row,
                   'observations': [by_id[i] for i in review['observation_ids']]}
        dossiers.append(dossier)
        markdown += [f"## {h['id']} — {a['shelfmark']} / {b['shelfmark']}", '',
                     f"**Category {review['classification']}.** {review['prior_status']}. "
                     f"{review['review_state']}.", '', f"**Question:** {h['question']}", '',
                     '**Supporting observations:** ' + ' '.join(review['supporting']), '',
                     '**Contrary evidence / alternatives:** ' + ' '.join(review['against']), '',
                     '**Falsification test:** ' + h['falsification_test'], '',
                     '**Outcome:** ' + review['outcome'], '',
                     '**Next evidence:** ' + review['next_evidence_needed'], '',
                     '**Originality:** ' + review['originality'] + '. No discovery claim.', '',
                     '**Images/regions:** ' + ', '.join(review['observation_ids']) +
                     '. Exact pixel selectors, source endpoints and SHA-256 hashes are in '
                     '`data/review_bundle.json` and the local viewer.', '',
                     '**Sources:** ' + ' · '.join(f'[source {i+1}]({u})' for i, u in enumerate(review['sources'])), '']
    if context_checks:
        markdown += ['# Supporting source checks', '',
                     'These checks provide context; they are not additional frozen attribution hypotheses. '
                     'No independent expert confirmation is claimed.', '']
        for check in context_checks:
            markdown += [f"## {check['id']} — {check['title']}", '', check['summary'], '',
                         '**Outcome:** ' + check['outcome'], '',
                         '**Limits:** ' + ' '.join(check['limits']), '',
                         '**Images/regions:** ' + (', '.join(check['observation_ids']) or 'No image-region observation attached; see cited source assertions and calculations.'), '',
                         '**Sources:** ' + ' · '.join(f'[source {i+1}]({u})' for i, u in enumerate(check['sources'])), '']
    categories = dict(Counter(r['classification'] for r in reviews))
    experiment = {
        'version': '1.0.0', 'queue_sha256': _sha(queue_path),
        'scope': 'Post-review descriptive case study; source-supported abstention, not a blind improved-method evaluation.',
        'baseline_method': 'unchanged metadata score and existing calibration threshold',
        'threshold': threshold, 'cases': results, 'categories': categories,
        'known_reference_acceptances': categories.get('E', 0),
        'published_rejections': categories.get('D', 0),
        'unresolved': categories.get('C', 0),
        'new_findings_confirmed': 0,
        'limits': [
            'Prior scholarly decisions are inputs to the screen, so agreement is not independent accuracy.',
            'Fr1385 lookalikes belong to one catalogue group: cases are correlated.',
            'Chant identifications are provisional AI readings with external concordances, not expert validation.',
            'No population precision, recall, calibrated identity probability or advanced-method gain inferred.',
        ],
    }
    bundle = {'version': '1.2.0', 'queue': queue, 'reviews': dossiers,
              'observations': observations, 'experiment': experiment,
              'context_checks': context_checks,
              'comparison_sources': comparison_sources,
              'source_document': document['observations_path']}
    for path, value in [('data/evidence_experiment.json', experiment), ('data/review_bundle.json', bundle)]:
        (root / path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
    (root / 'EVIDENCE_DOSSIERS.md').write_text('\n'.join(markdown))
    return {'cases': len(reviews), 'regions': len(observations), 'context_checks': len(context_checks), 'categories': categories,
            'new_findings_confirmed': 0, 'path': 'data/review_bundle.json'}
