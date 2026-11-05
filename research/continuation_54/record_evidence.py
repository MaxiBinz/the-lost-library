"""Record qualified E54 image readings and all eight initial comparisons.

The readings below are AI source observations after disclosed catalogue exposure,
not an independent transcription or a complete diplomatic/music edition.
"""
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def read(path):
    return json.loads((ROOT / path).read_text())


def save(name, value):
    (HERE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def main():
    p = read('research/continuation_54/protocol.json')
    caps = read('research/continuation_54/captures.json')['captures']
    sources = {r['path']: r for r in p['retained_sources']}
    sources.update({r['path']: dict(r, object_id=r['physical_object_id']) for r in caps})
    records = {r['id']: r for r in read('data/fragments.json')}
    for s in sources.values():
        s.setdefault('rights_url', records[s['object_id']]['rights_url'])
    regions = []

    def region(ident, path, xywh, literal, body):
        regions.append(dict(id=ident, path=path, xywh=xywh, literal=literal,
                            normalized=None, display_rotation_degrees=0, body=body))

    region('I54-10407-ix', caps[0]['path'], [650, 60, 450, 170], 'ix-like, flanked by points',
           'Red upper-margin sign, compatible with catalogue IX. The disclosed prior reading informs this qualified candidate; its historical numbering function and original side are not established.')
    region('I54-10407-i', caps[2]['path'], [800, 40, 400, 190], 'i-like, flanked by points',
           'Red upper-margin single-letter/stroke-like sign, compatible with catalogue i. Photograph ordinal is not medieval recto/verso; no unique compound address is established.')
    region('I54-10437-vj', caps[4]['path'], [650, 70, 450, 190], 'vj-like, flanked by points',
           'Red upper-margin sign, compatible with catalogue VI. Literal shape, normalized numeral and historical function remain separate; no original folio or quire number is assigned.')
    region('I54-10437-o', caps[6]['path'], [600, 40, 500, 200], 'O-like, flanked by points',
           'Angular rounded red upper-margin sign, compatible with catalogue O. It is not normalized to a number or assigned a medieval side.')
    region('I54-1385-first-edge', 'data/images/mpo-1385.jpg', [180, 0, 250, 70], None,
           'Red upper-edge strokes are clipped at the source boundary/fold. Catalogue IX is known, but this retained photograph does not independently yield a secure complete literal reading. Missing strokes are not reconstructed.')
    region('I54-1385-third-edge', 'data/images/mpo-1385-capture-3.jpg', [250, 0, 350, 100], None,
           'The red upper-edge mark is partly outside the visible surface. Catalogue D remains an attributed reading; this source does not securely establish the full sign or its function.')
    region('I54-10407-irregabat', caps[3]['path'], [390, 390, 1220, 260], 'Irregabat [...] lacrimis [...]',
           'Large I-initial notated opening and nearby lacrimis wording are visible. The provisional reading is compatible with the source-described Magdalene context; no exact complete chant ID, corresponding variant or new liturgical tradition is asserted.')
    region('I54-10437-reuse', caps[7]['path'], [80, 0, 1460, 380], None,
           'Two reinforced straps and sewing cross over medieval music/text in the reused binding. These later reuse features do not establish original medieval quire stitching, a physical join to another fragment or an original leaf-side map.')
    region('I54-10437-domum', caps[4]['path'], [230, 330, 1280, 300], 'Domum tuam domine [...]',
           'A broad-field notated D-initial opening is compatible with dedication material already reported by the catalogue. Different feast context from another fragment is not a book exclusion.')
    region('I54-10406-service', 'data/images/mpo-10406.jpg', [100, 140, 560, 245], None,
           'A short red service rubric and notated text occupy one broad writing field. The catalogue describes Magdalene, James and Olav material; the service cue is not independently read as an All-Saints feast or a complete calendar reconstruction.')
    region('I54-8311-adam', 'data/images/mpo-8311.jpg', [85, 205, 560, 225], 'Dum deambularet dominus in paradiso [...] / [...] Adam [...]',
           'The surviving music/text includes a paradise/Adam passage in one broad writing field. Different visible subject from10406 is compatible with separate sections in one book and also with different related books.')
    region('I54-365-hisunt', 'data/images/mpo-365.jpg', [115, 235, 565, 110], 'Hi sunt [...] sanguine [...]',
           'The one selected thumbnail has a broad-field notated H-initial passage with blood/martyr-related wording. The other three manifest photographs were not selected or inspected in E54; no complete text inventory or absence test is claimed.')

    objects = {
        'mpo-10406': dict(context='One broad notated field with red service cues; catalogue Magdalene, James and Olav material is attributed rather than silently expanded from the rubric. Four source photographs inspected.', regions=['I54-10406-service'], marks=[], full_manifest_photo_coverage=True),
        'mpo-10407': dict(context='One broad notated field; ix-like and i-like upper marks, plus provisional Irregabat/lacrimis context compatible with the already described Magdalene material.', regions=['I54-10407-ix', 'I54-10407-i', 'I54-10407-irregabat'], marks=['ix-like', 'i-like'], full_manifest_photo_coverage=True),
        'mpo-10437': dict(context='One broad notated field; vj-like and O-like upper signs and Domum-tuam dedication context. Later binding straps over text are reuse evidence.', regions=['I54-10437-vj', 'I54-10437-o', 'I54-10437-domum', 'I54-10437-reuse'], marks=['vj-like', 'O-like'], full_manifest_photo_coverage=True),
        'mpo-1385': dict(context='One broad notated field with service rubrics; catalogue Holy-Thursday context is credited. The two catalogue IX/D marks are clipped in retained first/third views; no secure fresh complete reading.', regions=['I54-1385-first-edge', 'I54-1385-third-edge'], marks=['unread: first clipped', 'unread: third clipped'], full_manifest_photo_coverage=True),
        'mpo-20274': dict(context='One broad notated field with Marian material already investigated. Its two retained photographs overlap one page area; they are not independent leaves. Upper red sign remains f/4-like and unnormalized; pencil KB/A103k/CXVIII is later library identification.', regions=['I51-20274-upper-sign', 'I51-20274-library-label'], marks=['f/4-like, uncertain'], full_manifest_photo_coverage=True),
        'mpo-365': dict(context='One selected broad-field thumbnail has a Hi-sunt/sanguine passage. Three other manifest photographs remain outside this phase; no secure original address from the selected view.', regions=['I54-365-hisunt'], marks=[], full_manifest_photo_coverage=False),
        'mpo-8311': dict(context='One broad notated field with Dum-deambularet/paradiso/Adam wording. Four source photographs inspected; rotated later account writing does not supply an original address.', regions=['I54-8311-adam'], marks=[], full_manifest_photo_coverage=True),
        'mpo-8994': dict(context='One broad notated field with already studied Stephen material. Previously recorded IIII-like and k-like red signs recur; no new side map or physical join.', regions=['I33-8994-roman', 'I33-8994-k', 'I33-8994-third-nocturn', 'I40-8994-contemplatur'], marks=['IIII-like', 'k-like'], full_manifest_photo_coverage=True),
    }
    for row in objects.values():
        row['columns_visible'] = 1
        row['original_address_function_established'] = False
        row['medieval_side'] = None
    limits = [
        '27 selected source photographs of eight existing objects were inspected; photographs are not independent leaves or witnesses. One Fr365 photograph of four is included.',
        'Catalogue mark readings were known in advance. Native photographs improve visibility of existing marks, not independent corroboration of their historical function.',
        'The Fr1385 IX/D catalogue readings are not securely readable in the retained clipped views. Equal Roman numerals alone can recur across sections or books and are not unique addresses.',
        'No complete corresponding diagnostic text/music work, original side/quire map, physical join or historical book adjudication is established. Different feasts and a common broad-field layout do not settle identity.',
        'All eight initial comparisons are recorded; a false first-comparison-pending flag means only that limited comparison took place, not that the historical question is exhausted.',
    ]
    readings = dict(version='1.0.0', date='2026-10-31',
                    observer='Codex AI; unblinded catalogue/prior-image exposure; no independent adjudication',
                    regions=regions, object_summaries=objects, limits=limits,
                    prior_regions_reused=list(dict.fromkeys(i for r in objects.values() for i in r['regions'] if not i.startswith('I54-'))),
                    coverage=[dict(object_id=s['object_id'], path=path,
                                   source_capture_index=s.get('source_capture_index', s.get('capture_index')),
                                   full_retained_photo_viewed=True, medieval_side=None,
                                   reading_scope='Whole selected source photograph inspected for context; not a complete text/music edition or original-side assignment.')
                              for path, s in sources.items()])
    save('readings.v1.json', readings)
    annotations = []
    for r in regions:
        s = sources[r['path']]
        assert hashlib.sha256((ROOT / r['path']).read_bytes()).hexdigest() == s['sha256']
        x, y, w, h = r['xywh']
        assert 0 <= x < x+w <= s['width'] and 0 <= y < y+h <= s['height']
        annotations.append(dict(id=r['id'], type='Annotation', motivation='describing',
            body=dict(type='TextualBody', value=r['body'], language='en'),
            target=dict(source=r['path'], selector=dict(type='FragmentSelector', conformsTo='http://www.w3.org/TR/media-frags/', value='xywh='+','.join(map(str, r['xywh'])))),
            fragment_id=s['object_id'], source_url=s['url'], sha256=s['sha256'],
            image_dimensions=[s['width'], s['height']], rights_url=s['rights_url'],
            attribution='Riksarkivet, Sweden; MPO/Fragmentarium source photograph',
            literal_candidate=r['literal'], normalized_candidate=None, display_rotation_degrees=0,
            observer=readings['observer'], independent_confirmation=False, interpretation_limits=limits))
    save('observations.json', dict(version='1.0.0', date='2026-10-31', annotations=annotations))
    matrix = []
    for lead in p['selected_existing_leads']:
        a, b = lead['pair']
        equal_ix = {a, b} == {'mpo-10407', 'mpo-1385'}
        matrix.append(dict(lead_id=lead['id'], pair=[a, b], contexts={x: objects[x] for x in [a, b]},
            source_regions=list(dict.fromkeys(i for x in [a, b] for i in objects[x]['regions'])),
            comparison_scope='Initial selected-source mark, service-context and writing-field comparison; incomplete historical identity test.',
            equal_ix_catalogue_suggestion_tested=equal_ix,
            equal_ix_source_result=('10407 ix-like sign is visible;1385 catalogue IX is clipped/unread in retained source. No securely shared unique address.' if equal_ix else None),
            selected_view_inspection_complete=True, initial_primary_comparison_recorded=True,
            complete_source_photo_coverage=all(objects[x]['full_manifest_photo_coverage'] for x in [a, b]),
            complete_corresponding_diagnostic_work_established=False, unique_shared_original_address_established=False,
            historical_same_codex_excluded=False, historical_adjudication_complete=False,
            decision_state='unresolved', independent_confirmation=False,
            limits='One broad field and different service/calendar material are compatibility only. Original mark function, resets, section copying and composite volumes remain alternatives. Reused bindings do not establish original quire structure.',
            next_test=('Obtain a genuinely new source view of the clipped1385 marks, if an exact lawful pointer is available, and establish the numeral/letter convention before an address argument. Otherwise this particular mark test remains access-limited.' if 'mpo-1385' in [a, b] else
                       'Identify a securely corresponding text/work or original physical feature; first establish source-photo/original-side mapping. Do not repeat a generic common-layout or different-feast screen.')))
    save('pair_comparisons.json', dict(version='1.0.0', date='2026-10-31', comparisons=matrix))
    total = sum(c['bytes'] for c in caps)
    save('results.json', dict(version='1.0.0', date='2026-10-31',
        pair_comparisons_recorded=8, initial_primary_comparisons_recorded=8,
        selected_existing_leads=[r['lead_id'] for r in matrix], new_source_regions=[r['id'] for r in regions],
        source_photo_views_inspected=27, new_source_files=len(caps), new_source_bytes=total,
        working_source_files_after=p['resources_before']['working_source_files']+len(caps),
        conservative_transfer_plan_after=p['resources_before']['conservative_transfer_plan_bytes']+total,
        direct_result='10407 ix-like/i-like and10437 vj-like/O-like signs are visible in eight exact native source photographs. Retained1385 edge marks remain clipped. The apparent catalogue IX agreement cannot be independently verified as a shared unique address. All eight objects show broad writing fields; selected contexts differ without excluding one historical book.',
        interpretation='No original-numbering convention, complete corresponding diagnostic work or physical join is established. Later10437 straps/sewing are reuse evidence. All eight historical decisions remain unresolved.',
        selected_view_inspection_complete=True, complete_group_source_photo_coverage=False,
        complete_diplomatic_or_music_collation=False, historical_adjudication_complete=False,
        primary_pair_tests_still_pending=0,
        pending_flag_scope='No stored pair awaits a FIRST limited source comparison; this is not historical adjudication or research completion.',
        decision_state='unresolved', new_codex_attribution=False, new_historical_exclusion=False,
        new_catalogue_correction=False, novelty_cleared=False, new_discovery=False,
        independent_confirmation=False, goal_complete=False, global_blocker_established=False,
        next_test='Audit all goal requirements and unresolved lead dependencies, distinguishing meaningful remaining public/local tests from completed generic screens and genuinely inaccessible decisive sources. Select a discriminating test before further acquisition or annotation; no new candidate family or threshold tuning.'))
    # PDM source crops only; unchanged pixels, no generated detail.
    proof = Image.new('RGB', (1000, 780), 'white')
    draw = ImageDraw.Draw(proof)
    for i, r in enumerate(regions[:6]):
        x, y, w, h = r['xywh']
        with Image.open(ROOT / r['path']) as im:
            crop = im.crop((x, y, x+w, y+h)).convert('RGB')
        crop.thumbnail((480, 205))
        col, row = (i % 2)*500, (i // 2)*260
        proof.paste(crop, (col+5, row+30))
        draw.text((col+5, row+5), r['id']+'; source crop', fill='black')
    proof.save(HERE / 'mark-review.png')
    print(json.dumps(dict(photo_views=27, initial_comparisons=8, new_regions=len(regions),
                          new_source_files=len(caps), source_bytes=total, historical_decisions='unchanged')))


if __name__ == '__main__':
    main()
