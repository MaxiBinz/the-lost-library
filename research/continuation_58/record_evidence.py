"""Record the unblinded surface comparison and scoped prior-art findings."""
from pathlib import Path
import hashlib, json

ROOT=Path(__file__).resolve().parents[2]
HERE=ROOT/'research/continuation_58'
def write(name, value):
    (HERE/name).write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n')
def main():
    record=next(r for r in json.loads((ROOT/'data/fragments.json').read_text()) if r['id']=='mpo-8311')
    sources=json.loads((HERE/'review_sources.json').read_text())
    texts=[
      ('I58-8311-1-bottom','The bottom line provisionally reads Vocem tuam audivi in paradiso et; the image cuts off below it.'),
      ('I58-8311-2-top','The upper line is damaged and partly covered; timui eo quod nudus [essem] is a tentative continuation candidate. No matching ink has been demonstrated across the two photos.'),
      ('I58-8311-3-bottom','The lower line provisionally ends with the words et dixit ad eum quid fe...; the edge is cropped or occluded.'),
      ('I58-8311-4-top','The upper writing is partly occluded. Later visible text reads ad me de terra, followed by a decorated Maledicta verse. It is compatible with the earlier Abel passage, but matching ink has not been demonstrated across the photos.')]
    caps={c['path']:c for c in record['captures']}; anns=[]
    for s,(ident,body) in zip(sources,texts):
        x1,y1,x2,y2=s['crop_xyxy'];c=caps[s['source']]
        assert hashlib.sha256((ROOT/s['source']).read_bytes()).hexdigest()==s['sha256']
        anns.append({'id':ident,'type':'Annotation','motivation':'describing','body':{'type':'TextualBody','value':body,'language':'en'},
          'target':{'source':s['source'],'selector':{'type':'FragmentSelector','conformsTo':'http://www.w3.org/TR/media-frags/','value':f'xywh={x1},{y1},{x2-x1},{y2-y1}'}},
          'fragment_id':'mpo-8311','source_url':c['url'],'sha256':s['sha256'],'image_dimensions':s['source_size'],
          'rights_url':record['rights_url'],'attribution':record['attribution'],'observer':'Codex AI; unblinded, 2026-11-01',
          'independent_confirmation':False,'interpretation_limits':['Selected text is provisional and incomplete.','Text continuity does not prove photographic overlap or medieval surface identity.']})
    write('observations.json',{'version':'1.0.0','annotations':anns})
    result={
      'version':'1.0.0','date':'2026-11-01','selected_lead':'fr8311-chant','regions':[a['id'] for a in anns],
      'comparison':'Unblinded photographs suggest text continuation 1 to 2 and 3 to 4, but no matching ink, original-side map, exact seam or photographic overlap was demonstrated.',
      'counterexample':'Search-indexed Cantus folio lists for Aachen G 20 060v and Utrecht Ms. 406 065v both show the same six candidate chant/verse identifiers 006537, 006537a, 006937, 006937a, 007804, 007804a consecutively. This is an identifier-level comparison, not an identical full text, melody or physical relationship.',
      'source_variants':'Utrecht indexes Vocem tuam domine audivi; Fr8311 is provisionally Vocem tuam audivi. Aachen indexes Vocem tuam audivi. Utrecht labels the folio Sexagesima; Aachen and Fr8311 catalogue Septuagesima. No independent verification of the feast or text is asserted.',
      'source_status':'Aachen 179885 had failed to open in E57 and was not reopened; Utrecht 493517 failed to open in E58. Both are indexed search results, not fully read pages. The Utrecht source viewer also failed. A different directly opened MMMO index preserves the same IDs but inserts an additional responsory and verses.',
      'full_local_sequence_verified':False,'photographic_overlap_demonstrated':False,'original_surface_map_verified':False,
      'new_discovery':False,'independent_confirmation':False,'new_codex_attribution':False,'new_source_files':0,'new_download_bytes':0,
      'next_test':'Seek a distinctive corresponding primary-source text or physical evidence beyond this six-ID sequence; preserve the incomplete original-side map and independently evaluate potentially meaningful variants.'}
    write('results.json',result)
    print(json.dumps({'regions':len(anns),'book_identity_inferred':False}))
if __name__=='__main__': main()
