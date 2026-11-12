#!/usr/bin/env python3
"""Create the Kinetics dotted DNA loader.

Outputs (by default beside this script):
  kinetics_dna_loader.html  - standalone transparent HTML5 Canvas animation (60 FPS)
  kinetics_dna_loader.gif   - transparent animated GIF for app assets

Install:
  python -m pip install pillow numpy

Run:
  python assets/brand/DNA.py
  python assets/brand/DNA.py --output-dir /tmp/kinetics-dna --frames 180

The Canvas animation uses requestAnimationFrame (targeting the display refresh rate).
GIF timing is quantized to 10 ms by the GIF format, so the default export is 50 FPS.
"""
from __future__ import annotations

import argparse
import math
from pathlib import Path
from typing import Iterable

import numpy as np
from PIL import Image, ImageDraw

# The four stops are deliberately kept cool and consistent with the supplied brief.
PALETTE = ("#7dd3fc", "#38bdf8", "#3b82f6", "#818cf8")
DOTS_PER_STRAND = 15
DEFAULT_WIDTH = 360
DEFAULT_HEIGHT = 120
DEFAULT_FRAMES = 180
DEFAULT_GIF_FPS = 50
ROTATION_SECONDS = 3.6
SUPERSAMPLE = 2

HTML_TEMPLATE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Kinetics DNA Loader</title>
<style>
  html, body {
    width: 100%;
    height: 100%;
    margin: 0;
    overflow: hidden;
    background: transparent;
  }
  body {
    display: grid;
    place-items: center;
  }
  canvas {
    display: block;
    width: min(100vw, 360px);
    height: auto;
    aspect-ratio: 3 / 1;
    background: transparent;
  }
</style>
</head>
<body>
<canvas id="kinetics-dna" width="360" height="120"
        role="img" aria-label="Animated blue DNA double helix loader"></canvas>
<script>
(() => {
  "use strict";

  const canvas = document.getElementById("kinetics-dna");
  const ctx = canvas.getContext("2d", { alpha: true });
  const WIDTH = 360;
  const HEIGHT = 120;
  const COUNT = 15;
  const AMPLITUDE = 31;
  const ROTATION_MS = 3600;
  const COLORS = ["#7dd3fc", "#38bdf8", "#3b82f6", "#818cf8"];

  // Interpolate smoothly between the four supplied blue palette stops.
  function colorAt(t) {
    const scaled = t * (COLORS.length - 1);
    const segment = Math.min(Math.floor(scaled), COLORS.length - 2);
    const mix = scaled - segment;
    const a = COLORS[segment].match(/[0-9a-f]{2}/gi).map(v => parseInt(v, 16));
    const b = COLORS[segment + 1].match(/[0-9a-f]{2}/gi).map(v => parseInt(v, 16));
    const rgb = a.map((v, i) => Math.round(v + (b[i] - v) * mix));
    return "rgb(" + rgb.join(",") + ")";
  }

  function draw(timestamp) {
    const phase = ((timestamp % ROTATION_MS) / ROTATION_MS) * Math.PI * 2;
    ctx.clearRect(0, 0, WIDTH, HEIGHT);

    const dots = [];
    for (let strand = 0; strand < 2; strand++) {
      for (let i = 0; i < COUNT; i++) {
        const u = i / (COUNT - 1);
        const x = 24 + u * (WIDTH - 48);
        const angle = (u * Math.PI * 3.2) + phase + strand * Math.PI;
        const z = Math.cos(angle);
        const y = HEIGHT / 2 + AMPLITUDE * Math.sin(angle);
        const radius = 2.5 + ((z + 1) / 2) * (6 - 2.5);
        const opacity = 0.4 + ((z + 1) / 2) * 0.6;
        dots.push({ x, y, z, radius, opacity, color: colorAt(u) });
      }
    }

    // Paint rear-facing dots first so front-facing dots naturally overlap them.
    dots.sort((a, b) => a.z - b.z);
    for (const dot of dots) {
      ctx.globalAlpha = dot.opacity;
      ctx.fillStyle = dot.color;
      ctx.beginPath();
      ctx.arc(dot.x, dot.y, dot.radius, 0, Math.PI * 2);
      ctx.fill();
    }
    ctx.globalAlpha = 1;
    requestAnimationFrame(draw);
  }

  requestAnimationFrame(draw);
})();
</script>
</body>
</html>
"""


def parse_color(value: str) -> tuple[int, int, int]:
    value = value.lstrip("#")
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))


def interpolate_color(position: float) -> tuple[int, int, int]:
    """Return an RGB colour interpolated across the four brand-blue stops."""
    scaled = max(0.0, min(1.0, position)) * (len(PALETTE) - 1)
    segment = min(int(scaled), len(PALETTE) - 2)
    fraction = scaled - segment
    start = parse_color(PALETTE[segment])
    end = parse_color(PALETTE[segment + 1])
    return tuple(round(a + (b - a) * fraction) for a, b in zip(start, end))


def frame_dots(phase: float, width: int, height: int) -> list[tuple[float, ...]]:
    """Build the 30 dots using opposing sine waves and cosine depth."""
    amplitude = height * 0.2583333333
    margin = width * (24 / DEFAULT_WIDTH)
    dots: list[tuple[float, ...]] = []

    for strand in range(2):
        for index in range(DOTS_PER_STRAND):
            u = index / (DOTS_PER_STRAND - 1)
            x = margin + u * (width - 2 * margin)
            angle = u * math.pi * 3.2 + phase + strand * math.pi
            z = math.cos(angle)
            y = height / 2 + amplitude * math.sin(angle)
            depth = (z + 1) / 2
            radius = 2.5 + depth * (6.0 - 2.5)
            opacity = 0.4 + depth * 0.6
            dots.append((z, x, y, radius, opacity, *interpolate_color(u)))

    # Negative z is the back of the helix; positive z is the front.
    return sorted(dots, key=lambda dot: dot[0])


def render_frame(phase: float, width: int, height: int) -> Image.Image:
    """Rasterize one transparent, antialiased frame."""
    scale = SUPERSAMPLE
    image = Image.new("RGBA", (width * scale, height * scale), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image, "RGBA")

    for dot in frame_dots(phase, width, height):
        _z, x, y, radius, opacity, red, green, blue = dot
        # GIF supports binary transparency; supersampling keeps the dot edges smooth.
        alpha = round(255 * opacity)
        cx, cy, r = x * scale, y * scale, radius * scale
        draw.ellipse(
            (round(cx - r), round(cy - r), round(cx + r), round(cy + r)),
            fill=(red, green, blue, alpha),
        )

    return image.resize((width, height), Image.Resampling.LANCZOS)


def save_transparent_gif(
    output: Path, width: int, height: int, frame_count: int, fps: int
) -> None:
    """Save an endlessly looping GIF with a shared palette and transparent index."""
    duration_ms = max(10, round(1000 / fps / 10) * 10)
    frames: list[Image.Image] = []
    for frame_index in range(frame_count):
        phase = (frame_index / frame_count) * math.tau
        frames.append(render_frame(phase, width, height))

    # Build one shared palette to avoid colour flicker between frames.
    reference = Image.new("RGB", (width, height), (0, 0, 0))
    for frame in frames[:: max(1, frame_count // 12)]:
        reference.paste(frame.convert("RGB"), mask=frame.getchannel("A"))
    palette_image = reference.quantize(colors=255, method=Image.Quantize.MEDIANCUT)
    palette = [0, 0, 0] + palette_image.getpalette()[:765]
    palette += [0] * (768 - len(palette))

    indexed_frames: list[Image.Image] = []
    for frame in frames:
        quantized = frame.convert("RGB").quantize(
            palette=palette_image, dither=Image.Dither.NONE
        )
        indices = np.asarray(quantized, dtype=np.uint8).astype(np.uint16) + 1
        # Reserve palette index zero exclusively for transparent pixels.
        indices = np.minimum(indices, 255).astype(np.uint8)
        indices[np.asarray(frame.getchannel("A")) < 128] = 0
        indexed = Image.fromarray(indices, mode="P")
        indexed.putpalette(palette)
        indexed_frames.append(indexed)

    output.parent.mkdir(parents=True, exist_ok=True)
    indexed_frames[0].save(
        output,
        save_all=True,
        append_images=indexed_frames[1:],
        duration=duration_ms,
        loop=0,
        disposal=2,
        transparency=0,
        optimize=False,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate the transparent Kinetics dotted DNA loader."
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).resolve().parent,
        help="Directory for the HTML and GIF outputs (default: this script's folder).",
    )
    parser.add_argument("--width", type=int, default=DEFAULT_WIDTH)
    parser.add_argument("--height", type=int, default=DEFAULT_HEIGHT)
    parser.add_argument("--frames", type=int, default=DEFAULT_FRAMES)
    parser.add_argument("--gif-fps", type=int, default=DEFAULT_GIF_FPS)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    if min(args.width, args.height, args.frames, args.gif_fps) <= 0:
        raise SystemExit("width, height, frames, and gif-fps must all be positive")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    html_path = args.output_dir / "kinetics_dna_loader.html"
    gif_path = args.output_dir / "kinetics_dna_loader.gif"

    html_path.write_text(HTML_TEMPLATE, encoding="utf-8")
    save_transparent_gif(gif_path, args.width, args.height, args.frames, args.gif_fps)

    gif_frame_ms = max(10, round(1000 / args.gif_fps / 10) * 10)
    actual_gif_fps = 1000 / gif_frame_ms
    print(f"HTML: {html_path} | transparent Canvas | requestAnimationFrame")
    print(
        f"GIF:  {gif_path} | {args.width}x{args.height} | {args.frames} frames | "
        f"{actual_gif_fps:g} FPS | {args.frames * gif_frame_ms / 1000:.2f}s loop"
    )
    print(f"Structure: {DOTS_PER_STRAND} dots per strand | palette: {', '.join(PALETTE)}")


if __name__ == "__main__":
    main()
