#!/usr/bin/env python3
"""Draw every diagram in this repository as SVG, one file per colour scheme.

  docs/assets/<name>-light.svg
  docs/assets/<name>-dark.svg

  python3 tools/gen_diagram.py           # write them
  python3 tools/gen_diagram.py --check   # fail if a committed file is stale

This is the same small kit as the other repositories here. GitHub sanitises SVG
in markdown, so there is no <style>, no <script>, no web font and no
<foreignObject>: everything is a presentation attribute and the type is a
system stack. Each pair is served from one <picture>, which GitHub switches on
prefers-color-scheme.

Layout is placed by hand on purpose. The diagrams are small, and a hand-placed
diagram never rearranges itself when a label changes. House rules: a slate
scale, one accent on the part that matters, drawn icons rather than emoji,
monospace for anything literally typed or wired.
"""
from __future__ import annotations

import pathlib
import sys
from xml.sax.saxutils import escape

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "assets"
SANS = "system-ui,-apple-system,'Segoe UI',Roboto,Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,monospace"

SCHEMES = {
    "light": dict(card="#ffffff", border="#d8dee4", title="#0f172a", sub="#5b6673",
                  accent="#2b59c3", on_accent="#ffffff", soft="#f1f4f9",
                  line="#94a3b8", rule="#e6e9ee", chip="#475569",
                  warn="#9a3412", warn_soft="#fff4ed", group="#f7f9fb"),
    "dark":  dict(card="#161b22", border="#30363d", title="#e6edf3", sub="#9aa4b0",
                  accent="#4c7ef3", on_accent="#ffffff", soft="#1b2230",
                  line="#6b7684", rule="#232a33", chip="#aeb7c2",
                  warn="#ffa657", warn_soft="#2a1d14", group="#11151b"),
}

# Stroked glyphs on a 24x24 grid, drawn rather than typed.
ICONS = {
    "house":   "M4 11 12 4l8 7 M6 10v9h12v-9 M10 19v-5h4v5",
    "chip":    "M8 8h8v8H8z M5 5h14v14H5z M10 2v3 M14 2v3 M10 19v3 M14 19v3 M2 10h3 M2 14h3 M19 10h3 M19 14h3",
    "wave":    "M2 12h3l2.5-6 3.5 12 3-9 2 3h6",
    "speaker": "M4 9h4l5-4v14l-5-4H4z M16 9a4 4 0 0 1 0 6 M18.5 6.5a7.5 7.5 0 0 1 0 11",
    "battery": "M3 8h15v8H3z M18 10.5h2.5v3H18 M6 11v2 M9 11v2 M12 11v2",
    "bolt":    "M13 2 4 14h7l-1 8 9-12h-7z",
}


class Canvas:
    """Parts plus a size. No layout engine, on purpose."""

    def __init__(self, w: int, h: int, scheme: str, label: str) -> None:
        self.w, self.h, self.c, self.label = w, h, SCHEMES[scheme], label
        self.parts: list[str] = []

    def add(self, *svg: str) -> "Canvas":
        self.parts.extend(svg)
        return self

    def icon(self, name, x, y, colour, size=21):
        s = size / 24
        return (f'<g transform="translate({x:.1f},{y:.1f}) scale({s:.4f})" fill="none" '
                f'stroke="{colour}" stroke-width="1.7" stroke-linecap="round" '
                f'stroke-linejoin="round"><path d="{ICONS[name]}"/></g>')

    def text(self, x, y, s, *, size=13, colour=None, font=None, weight=None,
             anchor="start", opacity=None):
        c = colour or self.c["sub"]
        extra = (f' font-weight="{weight}"' if weight else "") + \
                (f' opacity="{opacity}"' if opacity else "")
        return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{font or SANS}" '
                f'font-size="{size}" fill="{c}" text-anchor="{anchor}"{extra}>'
                f'{escape(s)}</text>')

    def box(self, x, y, w, h, title, subs=(), *, icon=None, tone="plain", rx=10):
        c = self.c
        fill, edge, tt = c["card"], c["border"], c["title"]
        st, op = c["sub"], ""
        if tone == "accent":
            fill = edge = c["accent"]; tt = st = c["on_accent"]; op = "0.85"
        elif tone == "soft":
            fill = c["soft"]
        elif tone == "warn":
            fill, edge, tt, st = c["warn_soft"], c["warn"], c["warn"], c["warn"]
        out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" '
               f'stroke="{edge}" stroke-width="1"/>']
        tx = x + 16
        ty = y + (28 if subs else h / 2 + 5)
        if icon:
            out.append(self.icon(icon, x + 16, y + (13 if subs else h / 2 - 10), tt))
            tx = x + 47
        out.append(self.text(tx, ty, title, size=15 if subs else 14,
                             colour=tt, weight="600"))
        for i, s in enumerate(subs):
            out.append(self.text(x + 16, y + 52 + i * 18, s, size=12.5,
                                 colour=st, opacity=op or None))
        return "".join(out)

    def edge(self, pts, *, label=None, dash=False, label_at=0.5, label_dy=-9,
             label_anchor="middle"):
        c = self.c
        d = ' stroke-dasharray="5 4"' if dash else ""
        path = " ".join(f"{x},{y}" for x, y in pts)
        out = [f'<polyline points="{path}" fill="none" stroke="{c["line"]}" '
               f'stroke-width="1.5"{d} marker-end="url(#a)"/>']
        if label:
            (x1, y1), (x2, y2) = pts[0], pts[-1]
            out.append(self.mono(x1 + (x2 - x1) * label_at,
                                 y1 + (y2 - y1) * label_at + label_dy,
                                 label, anchor=label_anchor))
        return "".join(out)

    def mono(self, x, y, s, *, anchor="start"):
        return self.text(x, y, s, size=11.5, colour=self.c["chip"], font=MONO,
                         anchor=anchor)

    def footer(self, note):
        return (f'<line x1="24" y1="{self.h - 52}" x2="{self.w - 24}" y2="{self.h - 52}" '
                f'stroke="{self.c["rule"]}" stroke-width="1"/>'
                + self.text(24, self.h - 26, note, size=12.5, colour=self.c["sub"]))

    def render(self) -> str:
        c = self.c
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" '
            f'width="{self.w}" height="{self.h}" role="img" aria-label="{escape(self.label)}">'
            f'<defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" '
            f'markerHeight="6" orient="auto-start-reverse">'
            f'<path d="M0 0 10 5 0 10z" fill="{c["line"]}"/></marker></defs>'
            + "".join(self.parts) + "</svg>\n"
        )


# ── the diagrams ──────────────────────────────────────────────────────────

def architecture(scheme):
    k = Canvas(1180, 400, scheme,
               "Music Assistant streams over Wi-Fi to the ESP32-S3-Zero, which sends I2S to "
               "the MAX98357A amplifier, which drives the stock speaker. The stock KALLSUP "
               "board supplies battery power and the second button.")
    W, H, top = 240, 108, 56
    xs = [24, 321, 618, 915]
    mid = top + H / 2
    kb_x, kb_y, kb_w = 321, 250, 537
    esp_x, amp_x = xs[1] + W / 2, xs[2] + W / 2
    k.add(
        k.box(xs[0], top, W, H, "Music Assistant", ["Sendspin server,", "one player per speaker"], icon="house"),
        k.box(xs[1], top, W, H, "ESP32-S3-Zero", ["SendspinZero Speaker", "firmware, button"], icon="chip", tone="accent"),
        k.box(xs[2], top, W, H, "MAX98357A", ["3 W class D amp,", "runs off the battery"], icon="wave"),
        k.box(xs[3], top, W, H, "Speaker", ["Stock 4 \u03a9 3 W,", "moved off P2"], icon="speaker"),
        k.edge([(xs[0] + W + 8, mid), (xs[1] - 8, mid)], label="Wi-Fi"),
        k.edge([(xs[1] + W + 8, mid), (xs[2] - 8, mid)], label="I2S"),
        k.edge([(xs[2] + W + 8, mid), (xs[3] - 8, mid)], label="+ / \u2212"),
        k.box(kb_x, kb_y, kb_w, 72, "KALLSUP board, stock",
              ["Battery, USB-C charging, power button, second button"], icon="battery", tone="soft"),
        k.edge([(esp_x, kb_y - 8), (esp_x, top + H + 8)], dash=True),
        k.mono(esp_x + 12, (kb_y + top + H) / 2 + 4, "3.3 V, button"),
        k.edge([(amp_x, kb_y - 8), (amp_x, top + H + 8)], dash=True),
        k.mono(amp_x + 12, (kb_y + top + H) / 2 + 4, "battery"),
        k.footer("The stock board keeps the battery, charging and power button. "
                 "The ESP32 and the amplifier only add Wi-Fi audio."),
    )
    return k.render()


def wiring(scheme):
    k = Canvas(1180, 480, scheme,
               "Switched battery feeds the MAX98357A Vin and, optionally through a TPS63020, "
               "the ESP32 3V3 pin. The second-button pad goes to GPIO1. GPIO2, 3 and 4 carry "
               "I2S to DIN, BCLK and LRC. The MAX98357A drives the speaker.")
    k.add(
        k.box(24, 56, 300, 120, "KALLSUP pads",
              ["Switched battery (measure first)", "GND1", "Second-button pad (measure first)"],
              icon="battery", tone="soft"),
        k.box(440, 56, 280, 96, "TPS63020, optional",
              ["Holds 3.3 V as the battery drains.", "Without it: battery to the 5V pin"], icon="bolt"),
        k.box(440, 236, 280, 120, "ESP32-S3-Zero",
              ["3V3 (or 5V), GND", "GPIO1: button", "GPIO2, 3, 4: I2S"], icon="chip", tone="accent"),
        k.box(856, 236, 300, 120, "MAX98357A",
              ["Vin, GND", "DIN, BCLK, LRC", "SD and GAIN left open"], icon="wave"),
        k.box(856, 56, 300, 96, "Speaker",
              ["Stock 4 \u03a9 3 W, off P2", "red to +, black to \u2212"], icon="speaker"),
        k.edge([(332, 100), (432, 100)], label="VIN"),
        k.edge([(580, 160), (580, 228)]),
        k.mono(592, 198, "OUT to 3V3"),
        k.edge([(332, 152), (380, 152), (380, 290), (432, 290)]),
        k.mono(336, 278, "GPIO1", anchor="start"),
        k.edge([(728, 296), (848, 296)], label="GPIO2, 3, 4"),
        k.edge([(1006, 228), (1006, 160)]),
        k.mono(1018, 198, "+ / \u2212"),
        k.edge([(174, 184), (174, 404), (1006, 404), (1006, 364)]),
        k.mono(590, 396, "battery to Vin", anchor="middle"),
        k.footer("Every GND pin joins GND1. Measure the two marked pads before soldering: "
                 "docs/build-guide.md."),
    )
    return k.render()


DIAGRAMS = {"architecture": architecture, "wiring": wiring}


def main() -> int:
    check = "--check" in sys.argv[1:]
    OUT.mkdir(parents=True, exist_ok=True)
    stale = []
    for name, fn in DIAGRAMS.items():
        for scheme in SCHEMES:
            path = OUT / f"{name}-{scheme}.svg"
            svg = fn(scheme)
            if check:
                if not path.exists() or path.read_text(encoding="utf-8") != svg:
                    stale.append(path.relative_to(ROOT))
            else:
                path.write_text(svg, encoding="utf-8")
    if check:
        if stale:
            print("stale, run python3 tools/gen_diagram.py:", *stale, sep="\n  ")
            return 1
        print("diagrams up to date")
        return 0
    print(f"{len(DIAGRAMS)} diagrams x {len(SCHEMES)} schemes -> docs/assets/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
