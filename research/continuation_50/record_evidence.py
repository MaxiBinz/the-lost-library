"""Record E50 source regions and a PDM-only layout comparison from retained pixels."""
import hashlib
import json
from pathlib import Path

from PIL import Image,ImageDraw

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]


def read(path):
    return json.loads((ROOT/path).read_text())


def save(name,value):
    (HERE/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')


def main():
    protocol=read('research/continuation_50/primary_protocol.json')
    readings=read('research/continuation_50/manual_readings.json')
    measured=read('research/continuation_50/field_comparison.json')
    captures=read('research/continuation_50/captures.json')['captures']
    records={r['id']:r for r in read('data/fragments.json')}
    sources={c['path']:c for c in captures}
    for c in protocol['retained_controls']:
        sources[c['path']]={**c,'sha256':c['sha256']}
    annotations=[]
    for r in readings['regions']:
        source=sources[r['path']]
        with Image.open(ROOT/r['path']) as im:
            width,height=im.size
        x,y,w,h=r['xywh']
        assert 0<=x<x+w<=width and 0<=y<y+h<=height
        digest=hashlib.sha256((ROOT/r['path']).read_bytes()).hexdigest()
        assert digest==source['sha256']
        annotations.append({'id':r['id'],'type':'Annotation','motivation':'describing',
            'body':{'type':'TextualBody','value':r['body'],'language':'en'},
            'target':{'source':r['path'],'selector':{'type':'FragmentSelector',
                'conformsTo':'http://www.w3.org/TR/media-frags/','value':'xywh='+','.join(map(str,r['xywh']))}},
            'fragment_id':source['physical_object_id'],'source_url':source['url'],
            'sha256':digest,'image_dimensions':[width,height],'rights_url':source['rights_url'],
            'literal_candidate':None,'normalized_candidate':None,
            'observer':readings['observer'],'independent_confirmation':False,
            'interpretation_limits':readings['limits']})
    save('observations.json',{'version':'1.0.0','date':'2026-10-30','annotations':annotations})
    # Full retained page views preserve edges/rulers; this is an analysis
    # derivative, not another source capture or a manuscript reconstruction.
    page_paths=[readings['regions'][0]['path'],readings['regions'][2]['path']]
    proof=Image.new('RGB',(1640,1280),'white')
    draw=ImageDraw.Draw(proof)
    for i,path in enumerate(page_paths):
        with Image.open(ROOT/path) as im:
            im=im.convert('RGB')
            scale=min(790/im.width,1190/im.height)
            resized=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.NEAREST)
        x=10+i*820
        draw.text((x,6),('Fr10349: two narrow fields' if i==0 else 'Fr2862: one broad field'),fill='black')
        draw.text((x,23),'Retained source pixels; nearest-neighbour fit; side unassigned',fill='black')
        proof.paste(resized,(x,45))
    draw.text((10,1240),'Selected visible layout difference. Post-inspection ruler estimates about7.4cm /15.7cm per field; broad sensitivity retained.',fill='black')
    draw.text((10,1258),'No unconditional same-codex exclusion, original fold map, calibrated probability or new discovery.',fill='black')
    proof.save(HERE/'layout-review.png')
    bytes_saved=sum(c['bytes'] for c in captures)
    save('results.json',{'version':'1.0.0','date':'2026-10-30','selected_lead':protocol['selected_existing_lead'],
        'pair':['mpo-10349','mpo-2862'],'source_regions':[a['id'] for a in annotations],
        'target_photo_views_inspected':7,'control_photo_views_inspected':2,
        'new_source_files':len(captures),'confirmed_successful_transfer_bytes':bytes_saved,
        'working_source_files_after':188+len(captures),
        'conservative_transfer_plan_after':1669530774+bytes_saved,
        'network_limit':'A timed-out request can have unmeasured traffic even when no body was saved; existing reserve retained. No claim of exact lifetime transfer accounting.',
        'direct_result':readings['direct_result'],'interpretation':readings['interpretation'],
        'measurement_summary':{r['object_id']:r['nominal_field_width_cm'] for r in measured['measurements']},
        'measurement_limits':measured['scope'],
        'wider_scale_sensitivity_overlaps':not measured['sensitivity_comparison'][-1]['ranges_separate_with_additional_scale'],
        'narrow_visible_layout_difference_supported':True,
        'original_leaf_fold_map_established':False,'historical_same_codex_excluded':False,
        'uniform_layout_unconditionally_excluded':False,'catalogue_correction_established':False,
        'primary_pair_test_executed':True,'primary_pair_test_completed':False,
        'all_planned_target_views_inspected':False,
        'initial_primary_comparison_recorded':True,
        'primary_pair_test_scope':'Initial visible-layout comparison executed under partial coverage; the planned all-source-view inspection and historical adjudication remain incomplete.',
        'decision_state':'unresolved','primary_pair_tests_still_pending':30,
        'missing_sources':[readings['missing_source_view'],readings['lower_resolution_view']],
        '20106_access':'Exact institutional and linked library record opens failed in the web reader and were stopped. No image/physical crosswalk established; no global blocker.',
        'next_test':'Retain the layout distinction as scoped evidence. A historical book decision needs secure original leaf/fold mapping and corresponding text/quire or production evidence, with composite/section alternatives. Preserve the one missing2862 view without retry; continue the remaining30 existing primary pair tests.',
        'new_discovery':False,'independent_confirmation':False,'goal_complete':False,'global_blocker_established':False})
    print(json.dumps({'source_regions':len(annotations),'new_native_files':len(captures),
        'confirmed_transfer_bytes':bytes_saved,'primary_pair_tests_still_pending':30,
        'historical_same_codex_excluded':False}))


if __name__=='__main__':
    main()
