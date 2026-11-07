#!/usr/bin/env python3
"""Build Kinetics' single, original, colourful looping science animation."""

from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "Assets" / "Future" / "kinetics-science-quest.gif"
WIDTH, HEIGHT = 960, 540
OUTPUT_SIZE = (480, 270)
FRAME_COUNT = 48
FRAME_DURATION_MS = 90


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold
        else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf" if bold
        else "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).is_file():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


TITLE_FONT = font(34, True)
SUB_FONT = font(17)
LABEL_FONT = font(14, True)


def mix(a: tuple[int, int, int], b: tuple[int, int, int], t: float) -> tuple[int, int, int]:
    t = max(0.0, min(1.0, t))
    return tuple(round(x + (y - x) * t) for x, y in zip(a, b))


def draw_background(draw: ImageDraw.ImageDraw, frame: int) -> None:
    top = (8, 13, 39)
    bottom = (21, 32, 78)
    for y in range(HEIGHT):
        colour = mix(top, bottom, y / HEIGHT)
        draw.line((0, y, WIDTH, y), fill=colour)

    # Parallax star field: fixed identity, gently drifting positions.
    for i in range(105):
        base_x = (i * 193 + (i % 7) * 31) % WIDTH
        speed = 0.35 + (i % 5) * 0.22
        x = int((base_x - frame * speed) % WIDTH)
        y = (i * 97 + 19) % 390
        radius = 1 + (i % 4 == 0)
        pulse = 0.5 + 0.5 * math.sin(frame * 0.18 + i)
        colour = mix((45, 76, 132), (117, 224, 255), pulse)
        draw.ellipse((x, y, x + radius * 2, y + radius * 2), fill=colour)


def draw_dna(draw: ImageDraw.ImageDraw, frame: int) -> None:
    points_a, points_b = [], []
    for y in range(112, 432, 5):
        phase = (y / 320) * math.tau * 2 + frame * math.tau / FRAME_COUNT
        x = 760 + math.sin(phase) * 76
        xb = 760 - math.sin(phase) * 76
        points_a.append((int(x), y))
        points_b.append((int(xb), y))
        if (y // 5) % 5 == 0:
            draw.line((int(x), y, int(xb), y), fill=(52, 111, 171), width=3)
            draw.ellipse((int(x) - 5, y - 5, int(x) + 5, y + 5), fill=(67, 224, 208))
            draw.ellipse((int(xb) - 5, y - 5, int(xb) + 5, y + 5), fill=(185, 111, 255))
    draw.line(points_a, fill=(69, 231, 220), width=5, joint="curve")
    draw.line(points_b, fill=(185, 111, 255), width=5, joint="curve")


def draw_orbiting_cells(draw: ImageDraw.ImageDraw, frame: int) -> None:
    palette = [(70, 220, 222), (176, 119, 255), (255, 183, 90), (255, 105, 153)]
    for i in range(7):
        angle = frame * math.tau / FRAME_COUNT + i * math.tau / 7
        cx = int(470 + math.cos(angle) * (145 + 12 * math.sin(angle * 2)))
        cy = int(280 + math.sin(angle) * 105)
        radius = 13 + (i % 3) * 5
        colour = palette[i % len(palette)]
        draw.ellipse((cx - radius - 5, cy - radius - 5, cx + radius + 5, cy + radius + 5),
                     outline=tuple(c // 2 for c in colour), width=2)
        draw.ellipse((cx - radius, cy - radius, cx + radius, cy + radius),
                     fill=tuple(c // 3 for c in colour), outline=colour, width=3)
        draw.ellipse((cx - 4, cy - 4, cx + 4, cy + 4), fill=(245, 250, 255))


def draw_portal(draw: ImageDraw.ImageDraw, frame: int) -> None:
    cx, cy = 475, 280
    pulse = 0.5 + 0.5 * math.sin(frame * math.tau / FRAME_COUNT)
    for i in range(6):
        radius = 70 + i * 15 + int(pulse * 8)
        colour = mix((32, 73, 140), (64, 224, 224), i / 5)
        draw.ellipse((cx - radius, cy - radius, cx + radius, cy + radius),
                     outline=colour, width=2)
    draw.ellipse((cx - 52, cy - 52, cx + 52, cy + 52),
                 fill=(24, 47, 100), outline=(107, 230, 255), width=4)
    draw.ellipse((cx - 25, cy - 25, cx + 25, cy + 25),
                 fill=(70, 218, 212), outline=(235, 255, 255), width=3)
    draw.ellipse((cx - 10, cy - 10, cx + 10, cy + 10), fill=(255, 244, 165))


def draw_runner(draw: ImageDraw.ImageDraw, frame: int) -> None:
    # Original pixel-art lab rover mascot with a looping two-step gait.
    x = 145
    bounce = int(8 * math.sin(frame * math.tau / 12))
    y = 382 + bounce
    dark = (10, 29, 57)
    mint = (86, 238, 174)
    cyan = (84, 222, 255)
    # Tail, body, head and visor.
    draw.polygon([(x + 12, y + 48), (x - 23, y + 33), (x + 8, y + 69)], fill=mint)
    draw.rounded_rectangle((x, y + 24, x + 88, y + 83), radius=16,
                           fill=mint, outline=(210, 255, 232), width=3)
    draw.rounded_rectangle((x + 51, y - 12, x + 111, y + 47), radius=15,
                           fill=(80, 203, 231), outline=(220, 250, 255), width=3)
    draw.rounded_rectangle((x + 70, y + 3, x + 103, y + 28), radius=8, fill=dark)
    draw.ellipse((x + 84, y + 9, x + 94, y + 19), fill=(255, 242, 155))
    draw.rectangle((x + 25, y + 43, x + 48, y + 58), fill=(24, 107, 105))
    # Alternating feet and little jet sparks.
    stride = (frame // 6) % 2
    if stride:
        draw.line((x + 27, y + 76, x + 15, y + 101), fill=dark, width=12)
        draw.line((x + 64, y + 76, x + 79, y + 96), fill=dark, width=12)
    else:
        draw.line((x + 27, y + 76, x + 40, y + 98), fill=dark, width=12)
        draw.line((x + 64, y + 76, x + 53, y + 101), fill=dark, width=12)
    draw.line((x + 40, y + 101, x + 52, y + 101), fill=cyan, width=5)
    draw.line((x + 77, y + 98, x + 90, y + 98), fill=cyan, width=5)
    if frame % 8 < 4:
        draw.polygon([(x - 19, y + 49), (x - 39, y + 40), (x - 30, y + 58)],
                     fill=(255, 178, 85))


def draw_track(draw: ImageDraw.ImageDraw, frame: int) -> None:
    draw.rectangle((0, 475, WIDTH, HEIGHT), fill=(13, 23, 57))
    draw.line((0, 475, WIDTH, 475), fill=(60, 218, 213), width=3)
    for i in range(18):
        x = int((i * 83 - frame * 13) % (WIDTH + 80))
        draw.rounded_rectangle((x, 499, x + 42, 504), radius=2, fill=(60, 117, 175))
    for i in range(8):
        x = int((i * 151 - frame * 7) % WIDTH)
        draw.line((x, 475, x - 24, 540), fill=(30, 64, 115), width=2)


def make_frame(frame: int) -> Image.Image:
    image = Image.new("RGB", (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(image)
    draw_background(draw, frame)
    draw_dna(draw, frame)
    draw_orbiting_cells(draw, frame)
    draw_portal(draw, frame)
    draw_track(draw, frame)
    draw_runner(draw, frame)

    # Clean, high-contrast title panel.
    draw.rounded_rectangle((34, 28, 505, 116), radius=22,
                           fill=(16, 34, 76), outline=(71, 210, 229), width=3)
    draw.text((58, 43), "KINETICS", font=TITLE_FONT, fill=(244, 250, 255))
    draw.text((60, 87), "SCIENCE IN MOTION  /  ONE CONNECTED WORLD",
              font=SUB_FONT, fill=(112, 232, 218))
    draw.rounded_rectangle((760, 35, 922, 91), radius=15,
                           fill=(31, 44, 92), outline=(180, 126, 255), width=2)
    draw.text((780, 45), "SCIENCE QUEST", font=LABEL_FONT, fill=(255, 224, 145))
    draw.text((780, 66), f"{frame + 1:02d} / {FRAME_COUNT}", font=SUB_FONT,
              fill=(206, 222, 255))

    # Bottom progress ribbon; the highlight travels but the loop closes cleanly.
    draw.rounded_rectangle((35, 518, 925, 528), radius=5, fill=(35, 57, 102))
    progress = int(890 * ((frame + 1) / FRAME_COUNT))
    draw.rounded_rectangle((35, 518, 35 + progress, 528), radius=5,
                           fill=(78, 225, 190))
    return image.resize(OUTPUT_SIZE, Image.Resampling.LANCZOS)


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    frames = [make_frame(i) for i in range(FRAME_COUNT)]
    frames[0].save(
        OUTPUT,
        save_all=True,
        append_images=frames[1:],
        duration=FRAME_DURATION_MS,
        loop=0,
        optimize=True,
        disposal=2,
    )

    readme = ROOT / "README.md"
    text = readme.read_text(encoding="utf-8")
    marker = "<!-- KINETICS_ANIMATION -->"
    end_marker = "<!-- /KINETICS_ANIMATION -->"
    embed = (
        '<div align="center">\\n'
        '<img src="Assets/Future/kinetics-science-quest.gif" width="960" '
        'alt="Original Kinetics science-in-motion animation">\\n'
        '</div>\\n'
    )
    if marker not in text or end_marker not in text:
        raise RuntimeError("README animation markers are missing")
    before, remainder = text.split(marker, 1)
    _, after = remainder.split(end_marker, 1)
    readme.write_text(
        before + marker + "\\n" + embed + end_marker + after,
        encoding="utf-8",
    )

    with Image.open(OUTPUT) as result:
        if result.format != "GIF" or result.n_frames != FRAME_COUNT:
            raise RuntimeError("Generated animation failed frame validation")
        if result.size != OUTPUT_SIZE or result.info.get("loop") != 0:
            raise RuntimeError("Generated animation has incorrect dimensions or loop settings")
    print(f"Built {OUTPUT.relative_to(ROOT)}: {FRAME_COUNT} frames, {OUTPUT_SIZE[0]}x{OUTPUT_SIZE[1]}, seamless looping GIF.")


if __name__ == "__main__":
    main()
