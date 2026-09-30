#!/usr/bin/env python3
"""Draw brand/icon.png from code: a speaker with Wi-Fi arcs on the house accent.

  python3 tools/gen_brand.py

Drawn at four times the size and scaled down, which is the cheapest
antialiasing Pillow offers. Edit this script and rerun it; never edit the PNG
by hand.
"""
from __future__ import annotations

import pathlib

from PIL import Image, ImageDraw

ROOT = pathlib.Path(__file__).resolve().parents[1]
SIZE, SS = 512, 4
ACCENT, WHITE = (43, 89, 195, 255), (255, 255, 255, 255)


def main() -> None:
    n = SIZE * SS
    img = Image.new("RGBA", (n, n), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, n - 1, n - 1], radius=int(n * 0.22), fill=ACCENT)

    u = n / 24  # the same 24-unit grid as the diagram icons
    # Speaker body and cone.
    d.polygon([(4.5 * u, 9.5 * u), (8 * u, 9.5 * u), (12.5 * u, 6 * u),
               (12.5 * u, 18 * u), (8 * u, 14.5 * u), (4.5 * u, 14.5 * u)], fill=WHITE)
    # Three arcs, the outer two doubling as Wi-Fi.
    w = int(1.5 * u)
    for r in (3.2, 5.8, 8.4):
        box = [12.5 * u - r * u, 12 * u - r * u, 12.5 * u + r * u, 12 * u + r * u]
        d.arc(box, start=-50, end=50, fill=WHITE, width=w)

    out = ROOT / "brand"
    out.mkdir(exist_ok=True)
    img.resize((SIZE, SIZE), Image.LANCZOS).save(out / "icon.png", optimize=True)
    print("brand/icon.png")


if __name__ == "__main__":
    main()
