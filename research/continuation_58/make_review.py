"""Arrange fixed source strips for inspection; no inferred alignment or generated pixels."""
from pathlib import Path
import hashlib, json
from PIL import Image, ImageOps, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / 'research/continuation_58'
SPECS = [
    ('data/images/mpo-8311.jpg', (0, 300, 800, 521), 'Capture 1 bottom'),
    ('data/images/mpo-8311-capture-2.jpg', (0, 0, 1000, 240), 'Capture 2 top'),
    ('data/images/mpo-8311-capture-3.jpg', (0, 430, 1000, 663), 'Capture 3 bottom'),
    ('data/images/mpo-8311-capture-4.jpg', (0, 0, 1000, 240), 'Capture 4 top'),
]
def main():
    rows=[]
    for path, box, label in SPECS:
        data=(ROOT/path).read_bytes()
        with Image.open(ROOT/path) as im:
            size=im.size; im=im.convert('RGB').crop(box)
            im=ImageOps.contain(im,(1200,400),method=Image.Resampling.NEAREST)
        rows.append((label,im,{'source':path,'sha256':hashlib.sha256(data).hexdigest(),'source_size':list(size),'crop_xyxy':list(box)}))
    out=Image.new('RGB',(1200,sum(i.height+34 for _,i,_ in rows)),'white'); draw=ImageDraw.Draw(out); y=0
    for label,im,_ in rows:
        draw.text((8,y+8),label,fill='black');y+=34;out.paste(im,(0,y));y+=im.height
    out.save(HERE/'seam-review.png')
    (HERE/'review_sources.json').write_text(json.dumps([r for _,_,r in rows],indent=2)+'\n')
if __name__=='__main__': main()
