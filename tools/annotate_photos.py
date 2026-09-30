#!/usr/bin/env python3
"""Draw labelled callouts on copies of the teardown photos.

  docs/assets/photos/<name>.jpg   ->   docs/assets/annotated/<name>.jpg

  python3 tools/annotate_photos.py

The photos are real; only the rings and labels are drawn. Every label says
what the docs say about that spot and no more: a pad that a check has not
settled yet is labelled as a check, never as a place to solder. Needs Pillow.
Edit the CALLOUTS below and rerun; never edit the output by hand.
"""
from __future__ import annotations

import io
import pathlib

from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / "docs" / "assets" / "photos"
OUT = ROOT / "docs" / "assets" / "annotated"

# What a ring means. Green: solder here. Amber: measure first. Red: keep off.
TONES = {
    "solder": (22, 163, 74),
    "check": (217, 119, 6),
    "avoid": (220, 38, 38),
    "info": (37, 99, 235),
}
LEGEND = {
    "solder": "solder here",
    "check": "measure first",
    "avoid": "keep off",
    "info": "for reference",
}

# (ring centre x, y, ring radius), tone, label lines, label top-left x, y.
# Coordinates are in the photos' own pixels (1400 x 1050 or 1050 x 1400).
CALLOUTS = {
    "board-back": [
        ((1012, 545, 26), "solder", ["GND1", "ground for every board"], (1010, 610)),
        ((690, 497, 26), "check", ["VCC_BAT", "check 1: probably always on,", "so not the switched point"], (560, 330)),
        ((530, 152, 24), "check", ["S1", "check 3: which button?"], (590, 40)),
        ((1115, 172, 24), "check", ["S2", "check 3: which button?"], (1010, 230)),
        ((320, 118, 62), "info", ["P2", "unplug the speaker here"], (40, 250)),
        ((868, 545, 22), "info", ["VCC_5V", "USB 5 V, option D only"], (560, 700)),
    ],
    "board-back-speaker-output": [
        ((135, 735, 110), "info", ["P2", "unplug the speaker here"], (20, 960)),
        ((290, 598, 30), "avoid", ["Speaker +1", "amplifier output"], (430, 380)),
        ((290, 808, 30), "avoid", ["Speaker -1", "treat as not ground:", "never tie it to GND"], (430, 960)),
    ],
    "board-front-amplifier": [
        ((620, 338, 46), "check", ["R21", "check 1: try the end", "away from U1"], (330, 110)),
        ((785, 485, 110), "avoid", ["U1, ANT8817S", "never probe its pins"], (960, 420)),
        ((820, 292, 30), "info", ["VCC_PVDD", "joins U1 pin 7"], (960, 200)),
    ],
    "board-front-buttons": [
        ((435, 650, 30), "check", ["IOVDD", "check 3: about 3.3 V?"], (560, 560)),
    ],
}

FONT = ImageFont.load_default(size=30)
FONT_BOLD = ImageFont.load_default(size=34)


def callout(d: ImageDraw.ImageDraw, ring, tone, lines, at):
    x, y, r = ring
    colour = TONES[tone]
    # Label box first, so the leader can start from its nearest edge.
    fonts = [FONT_BOLD] + [FONT] * (len(lines) - 1)
    widths = [d.textlength(s, font=f) for s, f in zip(lines, fonts)]
    pad, gap = 16, 8
    heights = [f.size + gap for f in fonts]
    bw, bh = max(widths) + pad * 2, sum(heights) - gap + pad * 2
    bx, by = at
    cx = min(max(x, bx), bx + bw)
    cy = min(max(y, by), by + bh)
    # Leader from the ring's edge to the box.
    dx, dy = cx - x, cy - y
    dist = max((dx * dx + dy * dy) ** 0.5, 1)
    if dist > r:
        d.line([(x + dx / dist * r, y + dy / dist * r), (cx, cy)], fill=colour, width=5)
    d.ellipse([x - r, y - r, x + r, y + r], outline=(255, 255, 255), width=9)
    d.ellipse([x - r, y - r, x + r, y + r], outline=colour, width=5)
    d.rounded_rectangle([bx, by, bx + bw, by + bh], radius=12, fill=(15, 23, 42, 225),
                        outline=colour, width=4)
    ty = by + pad
    for s, f, h in zip(lines, fonts, heights):
        d.text((bx + pad, ty), s, font=f, fill=(255, 255, 255))
        ty += h


def legend(d: ImageDraw.ImageDraw, w: int, h: int, tones):
    items = [t for t in LEGEND if t in tones]
    x, y = 20, h - 64
    widths = [d.textlength(LEGEND[t], font=FONT) + 70 for t in items]
    d.rounded_rectangle([x - 8, y - 8, x + sum(widths) + 8, y + 50], radius=10,
                        fill=(15, 23, 42, 210))
    for t, width in zip(items, widths):
        d.ellipse([x + 8, y + 7, x + 36, y + 35], outline=TONES[t], width=5)
        d.text((x + 46, y + 4), LEGEND[t], font=FONT, fill=(255, 255, 255))
        x += width


def render(name: str) -> bytes:
    img = Image.open(SRC / f"{name}.jpg").convert("RGB")
    over = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(over)
    tones = []
    for ring, tone, lines, at in CALLOUTS[name]:
        callout(d, ring, tone, lines, at)
        tones.append(tone)
    legend(d, *img.size, tones)
    out = Image.alpha_composite(img.convert("RGBA"), over).convert("RGB")
    buf = io.BytesIO()
    out.save(buf, "JPEG", quality=85, optimize=True)  # no EXIF: nothing is copied over
    return buf.getvalue()


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for name in CALLOUTS:
        (OUT / f"{name}.jpg").write_bytes(render(name))
    print(f"{len(CALLOUTS)} annotated photos -> docs/assets/annotated/")


if __name__ == "__main__":
    main()
