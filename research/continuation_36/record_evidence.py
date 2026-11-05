"""Serialize the E36 manual readings and check source integrity, not reading truth.

No transcription model or network request is executed. Literal readings below were
recorded from all sixteen retained originals before external chant lookup.
"""
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
SITES = [
    ("I36-I-end", "mpo-7960", "data/images/mpo-7960-capture-4.jpg", [85,920,600,85],
     "quoniam firmamentu[m] meum et refugiu[m] meum", "quoniam firmamentum meum et refugium meum",
     "The final written row ends the phrase before es tu; bracketed letters expand visible abbreviation marks."),
    ("I36-I-catchword", "mpo-7960", "data/images/mpo-7960-capture-4.jpg", [475,1035,115,70],
     "es tu", "es tu", "A lower-margin catchword reads es tu. It is separate from the sung main-line text; these two words alone are not unique."),
    ("I36-I-start", "mpo-7961", "data/images/mpo-7961.jpg", [50,207,590,48],
     "es tu et propter nomen tuum dux michi eris et enu[...]tries me", "es tu et propter nomen tuum dux michi eris et enutries me",
     "The first written row begins es tu and continues the Esto mihi text; the partly compressed enutries is normalized provisionally."),
    ("I36-II-end", "mpo-8343", "data/images/mpo-8343-capture-2.jpg", [300,800,450,95],
     "[...]scunt me mee. Alle lu ya", "[...]scunt me meae. Alleluia",
     "The prior Ego sum pastor bonus passage ends and a new Alleluia is written at the bottom. This is a generic chant boundary, not a distinctive split phrase."),
    ("I36-II-start", "mpo-8344", "data/images/mpo-8344-capture-3.jpg", [85,175,505,160],
     "Surre xit / xp[istu]s et illu xit populo suo quem rede[m]p[...]", "Surrexit Christus et illuxit populo suo quem redemit [...]",
     "The first two rows begin a Surrexit Christus et illuxit alleluia verse. Christogram expansion and redemit spelling are normalized candidates, not a melodic transcription."),
    ("I36-III-end", "mpo-8344", "data/images/mpo-8344-capture-2.jpg", [215,825,545,75],
     "Iubilate deo omnis terra psalmum dicite nomini eius", "Iubilate deo omnis terra psalmum dicite nomini eius",
     "The last text row supplies the prefix of the Vocem iucunditatis introit's psalm verse. No date is inferred from a possibly differing feast-number convention."),
    ("I36-III-start", "mpo-8343", "data/images/mpo-8343-capture-3.jpg", [45,185,520,65],
     "date gloriam laudi eius. Gloria euouae. Alle lu ya", "date gloriam laudi eius; Gloria euouae; Alleluia",
     "The first text row completes the preceding verse before the doxology cue and next Alleluia. There is no asserted physical seam.")
]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def main():
    frozen = json.loads((ROOT / "research/continuation_33/results.json").read_text())["frozen_inputs"]
    assert frozen == {p:sha(ROOT/p) for p in frozen}
    records = {r["id"]:r for r in json.loads((ROOT / "data/fragments.json").read_text())}
    annotations = []
    inventory = []
    for rid in ["mpo-7960","mpo-7961","mpo-8343","mpo-8344"]:
        for cap in records[rid]["captures"]:
            assert cap["sha256"] == sha(ROOT/cap["path"])
            inventory.append({"fragment_id":rid, "path":cap["path"], "sha256":cap["sha256"],
                              "canvas_id":cap.get("canvas_id"), "source_url":cap["url"],
                              "dimensions":[cap["width"],cap["height"]],
                              "inspection":"Original image inspected by project AI in E36; not an independent reader."})
    proof_rows = []
    for ident,rid,path,box,literal,normalized,description in SITES:
        record = records[rid]
        cap = next(c for c in record["captures"] if c["path"]==path)
        with Image.open(ROOT/path) as im:
            x,y,w,h = box
            assert im.size==(cap["width"],cap["height"])
            assert 0<=x<x+w<=im.width and 0<=y<y+h<=im.height
            proof_rows.append((ident,path,box,im.convert("RGB").crop((x,y,x+w,y+h)).resize((w*2,h*2),Image.Resampling.NEAREST)))
        annotations.append({"id":ident,"type":"Annotation","motivation":"describing",
            "body":{"type":"TextualBody","value":description,"language":"en"},
            "target":{"source":path,"selector":{"type":"FragmentSelector","conformsTo":"http://www.w3.org/TR/media-frags/","value":"xywh="+",".join(map(str,box))}},
            "fragment_id":rid,"source_url":cap["url"],"sha256":cap["sha256"],
            "image_dimensions":[cap["width"],cap["height"]],"rights_url":record["rights_url"],
            "literal_candidate":literal,"normalized_candidate":normalized,
            "observer":"Codex AI source inspection, 2026-10-27","independent_confirmation":False,
            "interpretation_limits":["Provisional AI reading; no independent transcription, melodic identity or novelty is established.","Catalogue folio-side mapping is a content-based local interpretation, not an inference from capture ordinal."]})
    write(HERE/"observations.json",{"version":"1.0.0","assessment_date":"2026-10-27","annotations":annotations})
    write(HERE/"inventory.json",{"version":"1.0.0","source_images_inspected":inventory})
    proof = Image.new("RGB",(1400,sum(im.height+55 for _,_,_,im in proof_rows)),"white")
    draw=ImageDraw.Draw(proof);y=0
    for ident,path,box,im in proof_rows:
        draw.text((10,y+8),ident+" / "+path+" / xywh="+str(box)+" / 2x nearest source-pixel display",fill="black")
        proof.paste(im,(10,y+40));y+=im.height+55
    proof.save(HERE/"boundary-reading-proof.png")
    # Consistency checks on declared readings; these do not independently validate
    # paleography, correctness of catalogue sides, rarity or historical identity.
    tests = {"catchword_reappears_at_next_start":SITES[1][5]==" ".join(SITES[2][5].split()[:2]),
             "III_forward_prefix_suffix":"nomini eius date gloriam" in (SITES[5][5]+" "+SITES[6][5]),
             "III_reverse_lacks_that_boundary":"nomini eius date gloriam" not in (SITES[6][5]+" "+SITES[5][5]),
             "non_neighbour_does_not_repeat_catchword":not SITES[4][5].startswith(SITES[1][5])}
    assert all(tests.values())
    write(HERE/"checks.json",{"source_hashes_and_bounds_valid":True,"verified_regions":len(annotations),
                             "inspected_source_files":len(inventory),"declared_reading_consistency":tests,
                             "scope":"Checks retained inputs and recorded strings; no automated verification of manuscript readings."})
    assert frozen == {p:sha(ROOT/p) for p in frozen}
    print(json.dumps({"regions":len(annotations),"source_files":len(inventory),"checks":tests,"frozen_unchanged":True}))


if __name__=="__main__":
    main()
