#!/usr/bin/env python3
"""Draw brand/icon.svg: a speaker cube with Wi-Fi arcs on the house blue tile.

  python3 tools/gen_brand.py           # write it
  python3 tools/gen_brand.py --check   # fail if the committed file is stale

Flat vector shapes only, so it stays sharp from the 32 px favicon size up.
Edit this script and rerun it; never edit the SVG by hand.
"""
from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "brand" / "icon.svg"
S = 512


def arc(cx, cy, r):
    """An arc over the top of (cx, cy), from 45 degrees left of vertical to 45 right."""
    k = r * 0.7071
    return f"M{cx - k:.1f},{cy - k:.1f} A{r},{r} 0 0 1 {cx + k:.1f},{cy - k:.1f}"


def icon() -> str:
    cx = S / 2
    body_x, body_y, body_w, body_h = 104, 226, 304, 212
    mesh = (126, 248, 260, 168)
    dcx, dcy = cx, body_y + body_h / 2
    arcs = "".join(
        f'<path d="{arc(cx, 206, r)}" fill="none" stroke="#ffffff" stroke-width="26" '
        f'stroke-linecap="round"/>'
        for r in (40, 86, 132)
    )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {S} {S}" width="{S}" height="{S}" '
        f'role="img" aria-label="KALLSUP Sendspin: a speaker sending Wi-Fi">'
        '<defs>'
        '<linearGradient id="tile" x1="0" y1="0" x2="1" y2="1">'
        '<stop offset="0" stop-color="#4378ea"/><stop offset="1" stop-color="#1f47a8"/></linearGradient>'
        '<linearGradient id="body" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#e3e7ee"/></linearGradient>'
        '<pattern id="mesh" width="14" height="14" patternUnits="userSpaceOnUse">'
        '<circle cx="7" cy="7" r="3.2" fill="#9ea7b5"/></pattern>'
        '<clipPath id="round"><rect width="512" height="512" rx="114"/></clipPath>'
        '</defs>'
        '<g clip-path="url(#round)">'
        '<rect width="512" height="512" fill="url(#tile)"/>'
        '<path d="M0,0 H512 V200 C360,250 150,170 0,230 Z" fill="#ffffff" opacity=".07"/>'
        # Shadow under the speaker.
        f'<ellipse cx="{cx}" cy="{body_y + body_h + 8}" rx="160" ry="18" fill="#0b1f55" opacity=".35"/>'
        # Speaker body, mesh panel and driver.
        f'<rect x="{body_x}" y="{body_y}" width="{body_w}" height="{body_h}" rx="52" fill="url(#body)"/>'
        f'<rect x="{mesh[0]}" y="{mesh[1]}" width="{mesh[2]}" height="{mesh[3]}" rx="34" fill="#cfd5de"/>'
        f'<rect x="{mesh[0]}" y="{mesh[1]}" width="{mesh[2]}" height="{mesh[3]}" rx="34" fill="url(#mesh)"/>'
        f'<circle cx="{dcx}" cy="{dcy}" r="62" fill="#262b33"/>'
        f'<circle cx="{dcx}" cy="{dcy}" r="50" fill="#4a5261"/>'
        f'<circle cx="{dcx}" cy="{dcy}" r="36" fill="#3a414d"/>'
        f'<circle cx="{dcx}" cy="{dcy}" r="17" fill="#1a1d22"/>'
        + arcs +
        '</g></svg>\n'
    )


def main() -> int:
    svg = icon()
    if "--check" in sys.argv[1:]:
        if not OUT.exists() or OUT.read_text(encoding="utf-8") != svg:
            print("stale, run python3 tools/gen_brand.py:\n  brand/icon.svg")
            return 1
        print("icon up to date")
        return 0
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(svg, encoding="utf-8")
    print("brand/icon.svg")
    return 0


if __name__ == "__main__":
    sys.exit(main())
