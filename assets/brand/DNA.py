#!/usr/bin/env python3
"""Generate a transparent, extra-long rainbow DNA particle GIF.

Install: pip install pillow numpy
Run:    python generate_rainbow_dna.py
Output: rainbow_dna_ultra_long.gif
"""
from PIL import Image, ImageDraw
import math, colorsys, numpy as np

WIDTH, HEIGHT = 2800, 400       # 7:1 banner
SUPERSAMPLE = 1                 # set 2 for extra supersampling (slower/larger)
FRAMES = 120                    # 20 seconds at 6 fps; GIF timing below is 160 ms
FRAME_MS = 160
TURNS = 10                       # increase for even more DNA turns
BEADS_PER_STRAND = 260
OUTPUT = "rainbow_dna_ultra_long.gif"

# Smooth HSV rainbow with slightly softened saturation for bright polished beads
def color(h, s=.90, v=.98):
    return tuple(round(c*255) for c in colorsys.hsv_to_rgb(h % 1, s, v))

def bead(draw, x, y, radius, hue):
    r = radius
    # Base sphere + subtle edge depth + broad specular and tiny white glint
    draw.ellipse((x-r, y-r, x+r, y+r), fill=color(hue, .92, .88))
    draw.ellipse((x-r*.62, y-r*.72, x-r*.08, y-r*.16), fill=color(hue, .25, 1.0))
    draw.ellipse((x-r*.79, y-r*.83, x-r*.46, y-r*.50), fill=(255,255,255,235))
    draw.ellipse((x-r*.08, y+r*.48, x+r*.55, y+r*.78), fill=color(hue, .98, .70))

def render(frame):
    canvas = Image.new('RGBA', (WIDTH*SUPERSAMPLE, HEIGHT*SUPERSAMPLE), (0,0,0,0))
    draw = ImageDraw.Draw(canvas, 'RGBA')
    time = frame / FRAMES
    center = HEIGHT*.5
    amplitude = HEIGHT*.31
    margin = 45
    # Back-to-front bead rendering produces a convincing particle depth overlap.
    beads=[]
    for strand, sign in enumerate((1,-1)):
        for i in range(BEADS_PER_STRAND):
            u=i/(BEADS_PER_STRAND-1)
            x=(margin+u*(WIDTH-2*margin))*SUPERSAMPLE
            phase=2*math.pi*TURNS*u+2*math.pi*time
            z=sign*math.cos(phase)
            y=(center+sign*amplitude*math.sin(phase))*SUPERSAMPLE
            # Restrained breathing: ~±6%, slowly small -> big -> small
            pulse=1+.06*math.sin(2*math.pi*time+u*2.0+strand*.25)
            radius=(8.5+1.3*(.5+.5*z))*SUPERSAMPLE*pulse
            hue=(u*.96 + time*.22 + strand*.045)%1
            beads.append((z,x,y,radius,hue))
    for z,x,y,r,h in sorted(beads,key=lambda b:b[0]):
        bead(draw,x,y,r,h)
    if SUPERSAMPLE>1:
        canvas=canvas.resize((WIDTH,HEIGHT),Image.Resampling.LANCZOS)
    return canvas

# Make a shared palette once (far faster than quantizing every frame independently).
frames=[render(i) for i in range(FRAMES)]
# Palette reference composed from every eighth frame; transparent pixels excluded.
ref=Image.new('RGB',(WIDTH,HEIGHT),(0,0,0))
for f in frames[::8]: ref.paste(f.convert('RGB'),mask=f.getchannel('A'))
palette_image=ref.quantize(colors=255,method=Image.Quantize.MEDIANCUT)
palette=palette_image.getpalette()[:765]
palette=[0,0,0]+palette
palette += [0]*(768-len(palette))
indexed=[]
for f in frames:
    p=f.convert('RGB').quantize(palette=palette_image,dither=Image.Dither.NONE)
    # reserve palette index zero for transparent pixels; shift visible indices
    a=np.asarray(f.getchannel('A'))
    ar=np.asarray(p).copy()
    ar=np.minimum(ar.astype(np.uint16)+1,255).astype(np.uint8)
    ar[a==0]=0
    out=Image.fromarray(ar,'P'); out.putpalette(palette)
    indexed.append(out)
indexed[0].save(OUTPUT,save_all=True,append_images=indexed[1:],duration=FRAME_MS,
                loop=0,disposal=2,transparency=0,optimize=False)
print(f'GIF: {OUTPUT} | {WIDTH}x{HEIGHT} | {FRAMES} frames | {FRAMES*FRAME_MS/1000:.1f}s | {TURNS} turns')
