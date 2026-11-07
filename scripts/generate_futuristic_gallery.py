#!/usr/bin/env python3
"""Create 100 original, square, futuristic scientific illustrations for Kinetics.

The artwork is generated locally with Pillow; no remote image service or stock
photography is used. Every output is a 1024x1024 RGB PNG.
"""
from __future__ import annotations

import json
import math
import random
import re
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFilter, ImageFont
except ImportError as exc:
    raise SystemExit(
        "Pillow is required. Termux: pkg install python-pillow; "
        "or python -m pip install Pillow"
    ) from exc

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "Assets" / "Future" / "PNG"
README = ROOT / "README.md"
MANIFEST = ROOT / "Assets" / "Future" / "ARTWORK_MANIFEST.json"
ATTRIBUTION = ROOT / "Assets" / "Future" / "ATTRIBUTION.json"
SIZE = 1024
PALETTES = [
    ((4, 9, 29), (12, 35, 76), (0, 238, 220), (89, 119, 255), (255, 89, 176)),
    ((12, 5, 34), (40, 17, 83), (255, 92, 184), (139, 104, 255), (63, 231, 255)),
    ((3, 19, 31), (8, 58, 75), (38, 255, 190), (0, 184, 255), (194, 255, 95)),
    ((20, 8, 28), (67, 23, 72), (255, 157, 66), (255, 74, 142), (177, 121, 255)),
    ((5, 15, 39), (20, 37, 96), (92, 255, 245), (174, 116, 255), (255, 216, 91)),
    ((13, 13, 23), (45, 35, 68), (255, 95, 95), (255, 190, 85), (100, 232, 255)),
]
FAMILIES = ("helix", "network", "orbital", "cell", "wave", "crystal", "scan", "vessel")


def load_categories():
    # Keep the gallery filenames and labels aligned with the canonical 100-domain catalogue.
    source = ROOT / "scripts" / "import_science_gallery.py"
    namespace = {"__name__": "kinetics_gallery_catalogue", "__file__": str(source)}
    exec(compile(source.read_text(encoding="utf-8"), str(source), "exec"), namespace)
    return namespace["CATEGORIES"]


def font(size: int, bold: bool = False):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/data/data/com.termux/files/usr/share/fonts/TTF/DejaVuSans-Bold.ttf" if bold else "/data/data/com.termux/files/usr/share/fonts/TTF/DejaVuSans.ttf",
    ]
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size)
        except OSError:
            pass
    return ImageFont.load_default()


def gradient(seed: int, palette):
    top, bottom, *_ = palette
    im = Image.new("RGB", (SIZE, SIZE))
    px = im.load()
    rng = random.Random(seed)
    drift = rng.uniform(-12, 12)
    for y in range(SIZE):
        t = y / (SIZE - 1)
        row = tuple(int(top[c] * (1 - t) + bottom[c] * t) for c in range(3))
        for x in range(SIZE):
            vignette = int(22 * ((x - SIZE / 2) ** 2 + (y - SIZE / 2) ** 2) / (SIZE * SIZE))
            noise = rng.randrange(-2, 3)
            px[x, y] = tuple(max(0, min(255, v + int(drift * (x / SIZE - .5)) - vignette + noise)) for v in row)
    return im


def glow_layer(seed: int, palette):
    layer = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    rng = random.Random(seed + 71)
    accents = palette[2:]
    for i in range(5):
        x, y = rng.randint(80, 944), rng.randint(100, 900)
        r = rng.randint(90, 230)
        c = accents[i % len(accents)]
        d.ellipse((x-r, y-r, x+r, y+r), fill=(*c, 42))
    return layer.filter(ImageFilter.GaussianBlur(95))


def draw_grid(draw, seed, accent):
    rng = random.Random(seed + 11)
    for x in range(32, SIZE, 64):
        draw.line((x, 0, x, SIZE), fill=(*accent, 15), width=1)
    for y in range(32, SIZE, 64):
        draw.line((0, y, SIZE, y), fill=(*accent, 15), width=1)
    for _ in range(125):
        x, y = rng.randrange(24, SIZE-24), rng.randrange(24, SIZE-24)
        r = rng.choice((1, 2, 3))
        draw.ellipse((x-r, y-r, x+r, y+r), fill=(*accent, rng.randrange(35, 105)))


def hud(draw, seed, palette):
    rng = random.Random(seed + 23)
    cx, cy = 512, 478
    for radius, start, extent, width, color in [
        (380, 205, 275, 3, palette[2]),
        (355, 18, 130, 2, palette[3]),
        (405, 80, 90, 2, palette[4]),
        (310, 145, 245, 1, palette[2]),
    ]:
        draw.arc((cx-radius, cy-radius, cx+radius, cy+radius), start, start+extent,
                 fill=(*color, 155), width=width)
    for radius in range(330, 421, 30):
        for angle in range(0, 360, 15):
            if rng.random() < .47:
                a = math.radians(angle)
                x, y = cx + radius*math.cos(a), cy + radius*math.sin(a)
                draw.line((x, y, x+8*math.cos(a), y+8*math.sin(a)),
                          fill=(*palette[3], 95), width=2)


def motif(draw, seed, family, palette):
    rng = random.Random(seed + 101)
    a, b, c = palette[2], palette[3], palette[4]
    cx, cy = 512, 462
    # A luminous central scientific object, surrounded by instrument-like geometry.
    draw.ellipse((250, 200, 774, 724), outline=(*a, 70), width=2)
    draw.ellipse((285, 235, 739, 689), outline=(*b, 95), width=3)

    if family == "helix":
        left, right = [], []
        for i in range(81):
            y = 255 + i * 5.2
            phase = i * .22 + seed * .17
            x1 = cx + math.sin(phase) * 145
            x2 = cx - math.sin(phase) * 145
            left.append((x1, y)); right.append((x2, y))
            if i % 5 == 0:
                draw.line((x1, y, x2, y), fill=(*c, 155), width=4)
                draw.ellipse((x1-7,y-7,x1+7,y+7), fill=(*a,235))
                draw.ellipse((x2-7,y-7,x2+7,y+7), fill=(*b,235))
        draw.line(left, fill=(*a,245), width=9)
        draw.line(right, fill=(*b,245), width=9)
    elif family == "network":
        nodes = [(rng.randint(320,704), rng.randint(270,660)) for _ in range(31)]
        for i, p in enumerate(nodes):
            nearest = sorted(nodes, key=lambda q: (q[0]-p[0])**2+(q[1]-p[1])**2)[1:4]
            for q in nearest:
                draw.line((*p,*q), fill=(*a,100), width=3)
        for i,(x,y) in enumerate(nodes):
            r = rng.randint(7,17)
            col = (a,b,c)[i%3]
            draw.ellipse((x-r-8,y-r-8,x+r+8,y+r+8), outline=(*col,70), width=3)
            draw.ellipse((x-r,y-r,x+r,y+r), fill=(*col,235))
    elif family == "orbital":
        for i in range(7):
            box = (300-i*14, 275-i*14, 724+i*14, 649+i*14)
            draw.ellipse(box, outline=(*(a,b,c)[i%3], 175-i*13), width=4)
        for i in range(13):
            ang = i * math.tau/13 + seed
            x, y = cx+205*math.cos(ang), cy+205*math.sin(ang)
            draw.ellipse((x-11,y-11,x+11,y+11), fill=(*(a,b,c)[i%3],245))
        draw.ellipse((455,405,569,519), fill=(*c,235), outline=(255,255,255,220), width=5)
    elif family == "cell":
        for i in range(22):
            ang = rng.random()*math.tau
            rad = rng.randint(30,190)
            x,y = cx+rad*math.cos(ang),cy+rad*math.sin(ang)
            r=rng.randint(18,52)
            col=(a,b,c)[i%3]
            draw.ellipse((x-r,y-r,x+r,y+r), outline=(*col,180), width=4)
            draw.ellipse((x-r*.35,y-r*.35,x+r*.35,y+r*.35), fill=(*col,130))
        draw.ellipse((430,380,594,544), outline=(*c,240), width=10)
    elif family == "wave":
        for k,col in enumerate((a,b,c)):
            points=[]
            for x in range(280,745,4):
                y=cy+(k-1)*62+math.sin(x*.025+seed+k)*48+math.sin(x*.061+k)*17
                points.append((x,y))
            draw.line(points, fill=(*col,235), width=7)
        for x in range(310,730,35):
            draw.line((x,300,x,640), fill=(*a,35), width=1)
    elif family == "crystal":
        for i in range(15):
            x=rng.randint(340,684); y=rng.randint(280,650); h=rng.randint(70,230); w=rng.randint(35,100)
            col=(a,b,c)[i%3]
            draw.polygon([(x,y-h),(x+w,y),(x,y+h//3),(x-w,y)], fill=(*col,45), outline=(*col,220))
            draw.line((x,y-h,x,y+h//3), fill=(*col,210), width=4)
    elif family == "scan":
        for i in range(11):
            r=35+i*17
            draw.ellipse((cx-r,cy-r,cx+r,cy+r), outline=(*a,180-i*10), width=3)
        for angle in range(0,360,30):
            q=math.radians(angle)
            draw.line((cx,cy,cx+210*math.cos(q),cy+210*math.sin(q)), fill=(*b,105), width=2)
        draw.ellipse((cx-24,cy-24,cx+24,cy+24), fill=(*c,245))
    else:  # vessel / branching anatomy
        def branch(x,y,angle,length,depth):
            if depth == 0: return
            nx=x+math.cos(angle)*length; ny=y+math.sin(angle)*length
            draw.line((x,y,nx,ny), fill=(*((a,b,c)[depth%3]), max(80,depth*28)), width=depth*3)
            branch(nx,ny,angle-.48,length*.73,depth-1)
            branch(nx,ny,angle+.48,length*.73,depth-1)
        branch(cx,650,-math.pi/2,100,6)

    # Accent particles and callout ticks around the focal object.
    for _ in range(38):
        x,y=rng.randint(220,804),rng.randint(190,740)
        r=rng.randint(2,5)
        draw.ellipse((x-r,y-r,x+r,y+r), fill=(*rng.choice((a,b,c)),rng.randint(100,220)))


def render(number: int, slug: str, label: str):
    seed = number * 7919
    palette = PALETTES[(number-1) % len(PALETTES)]
    family = FAMILIES[(number-1) % len(FAMILIES)]
    im = gradient(seed, palette).convert("RGBA")
    im = Image.alpha_composite(im, glow_layer(seed, palette))
    overlay = Image.new("RGBA", (SIZE,SIZE), (0,0,0,0))
    d = ImageDraw.Draw(overlay)
    draw_grid(d, seed, palette[2])
    hud(d, seed, palette)
    motif(d, seed, family, palette)
    # Dark title plate, restrained typography and an identifying domain number.
    d.rounded_rectangle((62,790,962,948), radius=28, fill=(3,9,27,218),
                        outline=(*palette[2],170), width=3)
    d.text((94,815), f"FIELD {number:03d}  /  KINETICS SCIENCE ATLAS",
           font=font(21, True), fill=(*palette[2],255))
    title = label.upper()
    title_font = font(39 if len(title) < 22 else 31, True)
    d.text((94,858), title, font=title_font, fill=(245,250,255,255))
    d.text((895,858), f"{number:02d}", font=font(42, True), fill=(*palette[4],245))
    # Four corner registration marks.
    for x,y,sx,sy in [(36,36,1,1),(988,36,-1,1),(36,988,1,-1),(988,988,-1,-1)]:
        d.line((x,y,x+sx*34,y), fill=(*palette[2],190), width=4)
        d.line((x,y,x,y+sy*34), fill=(*palette[2],190), width=4)
    im = Image.alpha_composite(im, overlay).convert("RGB")
    return im


def update_readme(categories):
    text = README.read_text(encoding="utf-8")
    start, end = "<!-- KINETICS_GALLERY_START -->", "<!-- KINETICS_GALLERY_END -->"
    if start not in text or end not in text:
        raise RuntimeError("README gallery markers are missing")
    cells=[]
    for number,(slug,_) in enumerate(categories,1):
        label=slug.replace("-"," ").title()
        cells.append(f'<td align="center"><img src="Assets/Future/PNG/{number:03d}-{slug}.png" width="170" alt="{label}"><br><b>{number:02d} · {label}</b></td>')
    rows=["<table>"]
    for i in range(0,len(cells),4):
        rows.append("<tr>"+"".join(cells[i:i+4])+"</tr>")
    rows.append("</table>")
    block=start+"\n"+"\n".join(rows)+"\n"+end
    before,rest=text.split(start,1)
    _,after=rest.split(end,1)
    README.write_text(before+block+after,encoding="utf-8")


def main():
    categories=load_categories()
    if len(categories)!=100:
        raise SystemExit(f"Expected exactly 100 domains; found {len(categories)}")
    OUT.mkdir(parents=True,exist_ok=True)
    records=[]
    for number,(slug,query) in enumerate(categories,1):
        label=slug.replace("-"," ").title()
        path=OUT/f"{number:03d}-{slug}.png"
        image=render(number,slug,label)
        image.save(path,format="PNG",optimize=True)
        with Image.open(path) as check:
            if check.format!="PNG" or check.size!=(SIZE,SIZE):
                raise RuntimeError(f"Invalid output: {path}")
        records.append({
            "number":number,"domain":label,"file":str(path.relative_to(ROOT)),
            "dimensions":[SIZE,SIZE],"format":"PNG",
            "origin":"Original procedural artwork generated for Kinetics",
            "style":"Futuristic colourful scientific visualization",
            "motif":FAMILIES[(number-1)%len(FAMILIES)],
            "generator":"scripts/generate_futuristic_gallery.py"
        })
        print(f"[{number:03d}/100] {path.name}")
    MANIFEST.write_text(json.dumps(records,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    # These generated files replace the old downloaded gallery; no external image credits apply.
    ATTRIBUTION.write_text("[]\n",encoding="utf-8")
    update_readme(categories)
    print(f"Created and verified {len(records)} square PNG illustrations at {SIZE}x{SIZE}.")
    print(f"Manifest: {MANIFEST.relative_to(ROOT)}")


if __name__=="__main__":
    main()
