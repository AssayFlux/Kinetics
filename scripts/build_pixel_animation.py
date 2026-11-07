#!/usr/bin/env python3
"""Build Kinetics' colourful, looping pixel-art science-runner GIF."""

from __future__ import annotations

import math
from pathlib import Path

try:
    from PIL import Image, ImageDraw
except ImportError as exc:
    raise SystemExit("Install Pillow: python -m pip install Pillow") from exc

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "Assets" / "Future" / "kinetics-science-quest.gif"
WIDTH = 960
HEIGHT = 360
FRAMES=32  # noqa: E225 - asserted by the visual-asset regression test
SCALE = 3
DURATION_MS = 75


def draw_pixel_character(draw: ImageDraw.ImageDraw, x: int, y: int, frame: int) -> None:
    """Draw a small original pixel dinosaur with a two-frame running gait."""
    leg = (frame // 4) % 2
    green = "#58e08b"
    dark = "#153f45"
    draw.rectangle((x + 12, y + 18, x + 48, y + 49), fill=green)
    draw.rectangle((x + 32, y + 5, x + 57, y + 29), fill=green)
    draw.rectangle((x + 46, y + 11, x + 62, y + 19), fill=green)
    draw.rectangle((x + 53, y + 8, x + 57, y + 12), fill=dark)
    draw.rectangle((x + 3, y + 26, x + 16, y + 34), fill=green)
    draw.rectangle((x + 19, y + 44, x + 28, y + 54), fill=dark)
    if leg:
        draw.rectangle((x + 31, y + 44, x + 38, y + 57), fill=dark)
        draw.rectangle((x + 10, y + 47, x + 22, y + 53), fill=dark)
    else:
        draw.rectangle((x + 14, y + 44, x + 21, y + 57), fill=dark)
        draw.rectangle((x + 33, y + 47, x + 45, y + 53), fill=dark)
    draw.rectangle((x + 37, y + 28, x + 43, y + 34), fill="#f5f6a5")


def make_frame(index: int) -> Image.Image:
    image = Image.new("RGB", (WIDTH, HEIGHT), "#101b3d")
    draw = ImageDraw.Draw(image)
    # Distant science-coloured stars and orbital dots.
    for star in range(42):
        sx = (star * 137 + index * (2 + star % 3)) % WIDTH
        sy = (star * 67 + 23) % 210
        radius = 2 if star % 4 else 3
        colour = ("#65d9ff", "#c78bff", "#fff18b")[star % 3]
        draw.ellipse((sx, sy, sx + radius, sy + radius), fill=colour)
    draw.rectangle((0, 250, WIDTH, HEIGHT), fill="#172d50")
    draw.rectangle((0, 265, WIDTH, 274), fill="#245c65")
    # Moving floor marks create a continuous runner effect.
    for mark in range(18):
        mx = (mark * 71 - index * 13) % (WIDTH + 30)
        draw.rectangle((mx, 282, mx + 28, 286), fill="#58e08b")
    # Stylized molecular-orbit decoration.
    for cx, cy, colour in ((760, 92, "#54d9ff"), (850, 150, "#c78bff")):
        draw.ellipse((cx - 28, cy - 10, cx + 28, cy + 10), outline=colour, width=2)
        draw.ellipse((cx - 10, cy - 28, cx + 10, cy + 28), outline=colour, width=2)
        draw.ellipse((cx - 5, cy - 5, cx + 5, cy + 5), fill="#fff18b")
    # Obstacles are abstract lab-science shapes, not logos or copied game art.
    obstacle_x = WIDTH - ((index * 19) % (WIDTH + 120))
    if obstacle_x > 300:
        draw.rectangle((obstacle_x, 252, obstacle_x + 18, 280), fill="#ff8b6e")
        draw.rectangle((obstacle_x + 5, 240, obstacle_x + 13, 252), fill="#ffd166")
    jump = max(0, int(48 * math.sin((index % 16) / 15 * math.pi)))
    draw_pixel_character(draw, 150, 205 - jump, index)
    # Minimal title panel, kept inside the safe margins.
    draw.rounded_rectangle((28, 22, 438, 76), radius=12, fill="#1b3159", outline="#65d9ff", width=2)
    draw.text((48, 39), "KINETICS  /  SCIENCE QUEST", fill="#f5f7ff")
    draw.text((WIDTH - 180, 30), "100 DOMAINS", fill="#fff18b")
    draw.text((WIDTH - 180, 52), f"RUN {index + 1:02d} / {FRAMES}", fill="#65d9ff")
    return image.resize((WIDTH // SCALE, HEIGHT // SCALE), Image.Resampling.NEAREST)


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    frames = [make_frame(index) for index in range(FRAMES)]
    frames[0].save(
        OUTPUT,
        save_all=True,
        append_images=frames[1:],
        duration=DURATION_MS,
        loop=0,
        optimize=True,
        disposal=2,
    )
    with Image.open(OUTPUT) as result:
        if result.n_frames != FRAMES:
            raise RuntimeError(f"Expected {FRAMES} GIF frames, got {result.n_frames}")
    print(f"Created {OUTPUT.relative_to(ROOT)} ({FRAMES} frames, looping GIF).")


if __name__ == "__main__":
    main()
