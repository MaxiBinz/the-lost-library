"""Record bounded manual row/word observations; never assemble a fake leaf."""
import hashlib
import json
from pathlib import Path
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]

ROWS = {
    1: [(350,410),(510,575),(675,735),(835,900),(995,1065),(1155,1225)],
    2: [(60,115),(225,280),(390,450),(550,615),(715,775)],
    3: [(345,420),(510,580),(675,740),(835,900),(1000,1070),(1160,1235)],
    4: [(65,120),(230,295),(390,455),(545,620),(715,780)],
}
BOUNDARY_BOXES = {1:[295,990,1210,256],2:[230,25,1190,260],
                  3:[410,990,1190,247],4:[355,20,1185,270]}
SITES = [
    ('I42-8994-c1-last-two',1,BOUNDARY_BOXES[1],
     '[...] ad fi dem conuertere uigi[... ?] | [...] [Ps?] [...] [Gloria?] [a] N[o?]',
     '[...] ad fidem convertere [...] | [...] N[o?]',
     'The last two visible text rows are retained with gaps rather than completed from a reference. The decorated terminal N and possible small o are the proposed split-word prefix; o remains uncertain.'),
    ('I42-8994-c2-second-row',2,[230,215,1190,70],
     'bi xpisti graciam pas sim omnibus pre di cabat',
     'bi Christi graciam passim omnibus predicabat',
     'The first full lower row begins bi, consistent with the preceding row ending uer-. This is a within-photo word-division control. The christogram expansion is provisional; it is not an independent witness.'),
    ('I42-8994-c3-last-two',3,BOUNDARY_BOXES[3],
     '[...] les. [V] Aſ ti te runt reges ter | re et princi[pes?] [...] aduerſus do[minum?] et aduerſus',
     '[...] Astiterunt reges terre et principes [...] adversus [Dominum?] et adversus',
     'The terminal words et adversus are directly visible. The broader verse identification/abbreviation expansion is assisted by the indexed Vulgate text after initial inspection; unresolved middle text is not supplied from it.'),
    ('I42-8994-c4-first-row',4,[355,20,1185,110],
     'xpistum eius. Vere. [R] E gre',
     'Christum eius. Vere. [R] Egre-',
     'The upper row supplies Christum eius after capture3 ends adversus. A new responsory begins Egre- and continues gius in the next row, already retained as I40-8994-nocte. The first staff is partly outside the frame; the photographed text is present.'),
]


def save(path,value):
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')


def main():
    record=next(r for r in json.loads((ROOT/'data/fragments.json').read_text()) if r['id']=='mpo-8994')
    paths=json.loads((HERE/'protocol.json').read_text())['fixed_sources']
    descriptors={c['path']:c for c in record['captures']}
    images={}
    coverage=[]
    overview=Image.new('RGB',(1840,1370),'white')
    od=ImageDraw.Draw(overview)
    for number,path in enumerate(paths,1):
        d=descriptors[path]
        assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==d['sha256']
        im=Image.open(ROOT/path).convert('RGB'); images[number]=im
        assert list(im.size)==[d['width'],d['height']]
        text_rows=[]
        for ordinal,(start,end) in enumerate(ROWS[number],1):
            flag='fold-shadow' if (number,ordinal) in [(1,6),(2,1)] else 'visible'
            text_rows.append({'row':ordinal,'y_range':[start,end],'visibility':flag,
                'scope':'Approximate text-body band, not a measured musical system or complete chant.'})
        coverage.append({'capture':number,'path':path,'sha256':d['sha256'],
            'dimensions':list(im.size),'source_url':d['url'],'canvas_id':d['canvas_id'],
            'visible_medieval_text_rows':len(text_rows),'rows':text_rows,
            'music_limit':'Captures2/4 have a partially framed upper staff; text-row counts do not establish complete musical coverage.',
            'complete_medieval_surface_verified':False})
        # This half-scale labelled overview is only a navigation aid. Raw
        # boundary panels and original coordinates remain the reading record.
        thumb=im.resize((im.width//2,im.height//2),Image.Resampling.LANCZOS)
        td=ImageDraw.Draw(thumb)
        for ordinal,(start,end) in enumerate(ROWS[number],1):
            td.line((110,start//2,800,start//2),fill='#b62248',width=1)
            td.text((100,start//2),str(ordinal),fill='#b62248')
        x=((number-1)%2)*920;y=((number-1)//2)*680
        od.text((x+8,y+8),f'Capture {number}: {len(text_rows)} visible text rows; side unverified',fill='black')
        overview.paste(thumb,(x+4,y+35))
    overview.save(HERE/'row-coverage-overview.png')
    save(HERE/'row_coverage.json',{'version':'1.0.0','date':'2026-10-28',
        'method':'Manual AI count of visible medieval text-body bands in all four originals; modern wrapper annotations excluded. Row y-ranges are approximate locators, not calibrated measurements.',
        'catalogue_rows_literal':record['raw']['zeilenzahl1'],
        'catalogue_source':'research/mpo.csv, signatur8994; inherited source assertion, not an independent count',
        'captures':coverage,'duplicated_complete_text_row_identified':False,
        'duplicate_row_limit':'No complete duplicated text row was demonstrated at the proposed boundaries; this is not proof that none exists in obscured material.',
        'independent_confirmation':False})
    annotations=[]
    for ident,number,box,literal,normalized,meaning in SITES:
        path=paths[number-1];d=descriptors[path]
        annotations.append({'id':ident,'type':'Annotation','motivation':'describing',
            'body':{'type':'TextualBody','value':meaning,'language':'en'},
            'target':{'source':path,'selector':{'type':'FragmentSelector',
                'conformsTo':'http://www.w3.org/TR/media-frags/',
                'value':'xywh='+','.join(map(str,box))}},
            'fragment_id':record['id'],'source_url':d['url'],'sha256':d['sha256'],
            'image_dimensions':[d['width'],d['height']],'rights_url':record['rights_url'],
            'literal_candidate':literal,'normalized_candidate':normalized,
            'observer':'Codex AI exploratory, nonblind reading, 2026-10-28',
            'independent_confirmation':False,
            'interpretation_limits':['Gaps and uncertain abbreviations are retained; normalized text is not a diplomatic transcription.',
                'Textual fit is separate from repeated photographed ink, immediate physical adjacency, complete surface and medieval side.',
                'No new codex, unique witness variant or novelty clearance established.']})
    save(HERE/'observations.json',{'version':'1.0.0','assessment_date':'2026-10-28',
        'annotations':annotations,'reused_regions':['I34-8994-novo','I40-8994-nocte']})
    panel=Image.new('RGB',(1240,sum(b[3]+65 for b in BOUNDARY_BOXES.values())+45),'white')
    draw=ImageDraw.Draw(panel);offset=0
    for number,box in BOUNDARY_BOXES.items():
        x,y,w,h=box
        draw.text((10,offset+7),f'Capture {number}; raw pixels xywh={box}; separate panels, no physical join implied',fill='black')
        panel.paste(images[number].crop((x,y,x+w,y+h)),(10,offset+35));offset+=h+65
    draw.text((10,offset+5),'Readings are provisional. No warped/stitched leaf or complete medieval side is shown.',fill='black')
    panel.save(HERE/'boundary-text-review.png')
    comparisons=[]
    for left,right,outcome,reason in [
        (1,2,'provisional_split_word_fit','Terminal N[o?] plus upper uo rerum is consistent with Novo rerum. The small o and damaged surrounding text remain uncertain.'),
        (3,4,'locally_supported_phrase_fit','Terminal et adversus continues into xpistum eius, provisionally expanded Christum eius. This is a common verse phrase, not a unique manuscript fingerprint.'),
        (1,4,'no_direct_boundary_fit_identified','N[o?] followed by Christum eius does not give the proposed Novo split-word continuation. This does not exclude a hidden gap or a different nonadjacent relation.'),
        (3,2,'no_direct_boundary_fit_identified','Adversus followed by uo rerum does not supply the verse continuation Christum eius. This does not establish different books or surfaces.'),
    ]:
        comparisons.append({'pair':[left,right],'role':'proposed' if (left,right) in [(1,2),(3,4)] else 'deliberately_mismatched',
            'visible_row_sum':len(ROWS[left])+len(ROWS[right]),'text_outcome':outcome,'reason':reason,
            'physical_adjacency_established':False,'complete_surface_map_established':False})
    unchanged=json.loads((ROOT/'research/continuation_41/results.json').read_text())['unchanged_inputs']
    result={'version':'1.0.0','date':'2026-10-28','comparisons':comparisons,
        'question':json.loads((HERE/'protocol.json').read_text())['question'],
        'row_count_result':'Visible text-row counts are 6,5,6,5. All four predeclared pairings sum to11. Agreement with the inherited #11 field cannot select the proposed pairing.',
        'text_result':'Two more exact local boundary checks sharpen E34 reading order: N[o?]+uo rerum is a provisional Novo split-word fit; et adversus+xpistum eius gives a clearer verse continuation. Neither deliberately mismatched pairing supplies these direct joins in the selected visible text.',
        'within_photo_controls':['Capture2 upper uer- plus next-row bi is consistent with verbi.','Capture4 Egre- plus next-row gius is consistent with Egregius. These are word-division controls within a photograph, not independent codex evidence.'],
        'new_regions':[a['id'] for a in annotations],
        'reused_regions':['I34-8994-novo','I40-8994-nocte'],
        'e35_screens_unchanged':True,'accepted_photographic_overlap':False,
        'physical_adjacency_established':False,'complete_surface_map_established':False,
        'physical_join_established':False,'new_codex_attribution':False,
        'novelty_cleared':False,'independent_confirmation':False,'new_download_bytes_retained':0,
        'scope':'Local exploratory textual fit and a failed discriminating row-count test; no complete diplomatic transcription, melody, physical surface or medieval recto/verso assignment.',
        'next_action':'Audit the complete bounded ten-case queue and limited pivot for remaining executable discriminating tests; distinguish these from repetitions and claim-specific inaccessible originals. Do not repeat this row-count screen or refit the failed features for promotion.',
        'unchanged_inputs':unchanged}
    save(HERE/'results.json',result)
    print(json.dumps({'new_regions':len(annotations),'visible_text_rows':[len(v) for v in ROWS.values()],
        'pair_row_sums':[r['visible_row_sum'] for r in comparisons],'complete_surface_map_established':False}))


if __name__=='__main__':
    main()
