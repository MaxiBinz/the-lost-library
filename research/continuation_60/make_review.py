"""Create a navigation figure from the original Swedish source pixels only."""
from pathlib import Path
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2]
def main():
    src=Image.open(ROOT/'data/images/mpo-10370-capture-1-1700px.jpg').convert('RGB')
    crop=src.crop((250,60,1460,570))
    canvas=Image.new('RGB',(1210,550),'white');canvas.paste(crop,(0,40))
    ImageDraw.Draw(canvas).text((8,10),'Fr 10370: II-like mark and first preserved lines (no Finnish image)',fill='black')
    canvas.save(ROOT/'research/continuation_60/swedish-head.png')
if __name__=='__main__':main()
