#!/usr/bin/env python3
"""Generate a colourful, looping pixel-art Kinetics science explorer GIF."""
from __future__ import annotations
import math
from pathlib import Path
try:
    from PIL import Image, ImageDraw
except ImportError as exc:
    raise SystemExit("Install Pillow first: python -m pip install Pillow") from exc
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"Assets"/"Future"/"kinetics-science-quest.gif"
W,H,FRAMES=320,120,32
COLORS=[(5,10,34),(12,25,64),(18,48,92),(27,92,128),(50,220,220),(130,255,230),(255,210,80),(255,110,150),(180,125,255),(245,250,255)]
def draw_frame(t):
    im=Image.new("RGB",(W,H),COLORS[0]); d=ImageDraw.Draw(im)
    for i in range(72):
        x=(i*37+t*(1+i%4))%W; y=(i*23+9)%H
        d.rectangle((x,y,x+(i%3),y+(i%3)),fill=COLORS[4+i%6])
    for y in range(18,H,18): d.line((0,y,W,y),fill=(12,34,68))
    d.line((0,96,W,96),fill=(23,85,120),width=1)
    for x in range(5,175,4):
        phase=x*.11+t*.28
        y1=58+int(17*math.sin(phase)); y2=58-int(17*math.sin(phase))
        d.line((x,y1,x,y2),fill=(37,113,160))
        d.rectangle((x-1,y1-1,x+1,y1+1),fill=COLORS[4])
        d.rectangle((x-1,y2-1,x+1,y2+1),fill=COLORS[7])
    nodes=[(205,38),(232,25),(258,42),(286,27),(304,48),(230,70),(263,80),(293,70)]
    edges=[(0,1),(1,2),(2,3),(3,4),(1,5),(5,6),(6,7),(2,6),(3,7)]
    for a,b in edges: d.line((*nodes[a],*nodes[b]),fill=(54,135,194),width=2)
    for i,(x,y) in enumerate(nodes):
        p=2+int((1+math.sin(t*.4+i))>1)
        d.ellipse((x-p,y-p,x+p,y+p),fill=COLORS[4+i%5],outline=COLORS[9])
    cx=240+int(22*math.sin(t*math.pi/16)); cy=101+int(5*math.cos(t*math.pi/16))
    d.polygon([(cx,cy-7),(cx+6,cy+5),(cx,cy+2),(cx-6,cy+5)],fill=COLORS[6],outline=COLORS[9])
    d.rectangle((cx-1,cy+5,cx+1,cy+9),fill=COLORS[7])
    d.rectangle((8,7,166,20),fill=(8,20,54),outline=(39,115,165))
    d.text((13,11),"KINETICS // SCIENCE QUEST",fill=(215,250,255))
    for i in range(8):
        c=COLORS[4+i%5] if i<=(t//4)%9 else (24,48,82)
        d.rectangle((248+i*8,9,251+i*8,12),fill=c)
    return im.resize((640,240),Image.Resampling.NEAREST)
def main():
    OUT.parent.mkdir(parents=True,exist_ok=True)
    frames=[draw_frame(i) for i in range(FRAMES)]
    frames[0].save(OUT,save_all=True,append_images=frames[1:],duration=90,loop=0,optimize=True,disposal=2)
    with Image.open(OUT) as check:
        assert check.format=="GIF" and check.size==(640,240)
        assert check.n_frames==FRAMES and check.info.get("loop")==0
    print(f"Generated {OUT.relative_to(ROOT)} — 640x240, {FRAMES} frames, looping.")
if __name__=="__main__": main()
