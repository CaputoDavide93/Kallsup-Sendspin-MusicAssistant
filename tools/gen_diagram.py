#!/usr/bin/env python3
"""Draw this repository's diagrams as SVG, one file per colour scheme.

  docs/assets/<name>-light.svg
  docs/assets/<name>-dark.svg

House diagram kit (canonical copy: ~/.claude/skills/new-repo/assets/gen_diagram.py,
first built for InkFrame-Immich). The engine below the "diagrams" line is shared
verbatim across repos; only the diagram functions and DIAGRAMS change per repo.

GitHub sanitises SVG in markdown: no <style>, no <script>, no web font, no
<foreignObject>. Everything is a presentation attribute and the type is a system
stack. Each pair is served from one <picture>, which GitHub switches on
prefers-color-scheme. Layout is explicit rather than solved.

House rules: a slate scale, a single accent on the one thing that matters in each
picture, drawn icons rather than emoji, monospace for anything literally typed,
text contrast at or above 4.5:1 in both schemes.

  python3 tools/gen_diagram.py          # write the SVGs
  python3 tools/gen_diagram.py --check  # exit 1 if any SVG is stale (for CI)
"""
from __future__ import annotations

import pathlib
from xml.sax.saxutils import escape

ROOT = pathlib.Path(__file__).resolve().parents[1]
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
    "library":  "M3 7h13v11H3z M6 4h13v11 M7 14l3-3 2.5 2.5L15 11l2 2.5",
    "chip":     "M8 8h8v8H8z M5 5h14v14H5z M10 2v3 M14 2v3 M10 19v3 M14 19v3 M2 10h3 M2 14h3 M19 10h3 M19 14h3",
    "frame":    "M3 5h18v12H3z M9 20h6 M12 17v3 M6 13l3.5-4 2.5 3 2-2.5L18 13",
    "house":    "M4 11 12 4l8 7 M6 10v9h12v-9 M10 19v-5h4v5",
    "moon":     "M20 14.5A8.5 8.5 0 0 1 9.5 4 8.5 8.5 0 1 0 20 14.5z",
    "bolt":     "M13 2 4 14h7l-1 8 9-12h-7z",
    "server":   "M4 4h16v6H4z M4 14h16v6H4z M7 7h.01 M7 17h.01 M11 7h6 M11 17h6",
    "database": "M4 6c0-1.7 3.6-3 8-3s8 1.3 8 3-3.6 3-8 3-8-1.3-8-3z M4 6v12c0 1.7 3.6 3 8 3s8-1.3 8-3V6 M4 12c0 1.7 3.6 3 8 3s8-1.3 8-3",
    "cloud":    "M7 18h10a4 4 0 0 0 .5-7.97A6 6 0 0 0 6.1 9.5 4.3 4.3 0 0 0 7 18z",
    "laptop":   "M5 5h14v10H5z M2 19h20 M9 19l1-2h4l1 2",
    "phone":    "M8 2h8a1 1 0 0 1 1 1v18a1 1 0 0 1-1 1H8a1 1 0 0 1-1-1V3a1 1 0 0 1 1-1z M11 18h2",
    "mail":     "M3 6h18v12H3z M3 7l9 6 9-6",
    "clock":    "M12 3a9 9 0 1 0 0 18 9 9 0 0 0 0-18z M12 7v5l3 2",
    "shield":   "M12 3 4 6v6c0 4.5 3.4 8.3 8 9 4.6-.7 8-4.5 8-9V6z M9 12l2 2 4-4",
    "box":      "M12 3 3 7.5v9L12 21l9-4.5v-9z M3 7.5 12 12l9-4.5 M12 12v9",
    "user":     "M12 12a4 4 0 1 0 0-8 4 4 0 0 0 0 8z M4 21c0-4 3.6-6 8-6s8 2 8 6",
    "users":    "M9 11a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7z M2 20c0-3.5 3-5.5 7-5.5s7 2 7 5.5 M16 4.5a3.5 3.5 0 0 1 0 6.5 M18 14.8c2.4.6 4 2.3 4 5.2",
    "key":      "M14 10a4 4 0 1 0-3.2 3.9L13 16h2v2h2v2h3v-3l-5.1-5.1c.1-.3.1-.6.1-.9z M8 9h.01",
    "camera":   "M3 8h4l2-3h6l2 3h4v11H3z M12 17a4 4 0 1 0 0-8 4 4 0 0 0 0 8z",
    "chart":    "M4 20V4 M4 20h16 M8 16v-5 M12 16V8 M16 16v-3",
    "api":      "M8 7 3 12l5 5 M16 7l5 5-5 5 M14 4l-4 16",
    "bell":     "M6 16V11a6 6 0 1 1 12 0v5l2 2H4z M10 21h4",
    "chat":     "M4 5h16v11H9l-5 4z",
    "gear":     "M12 15a3 3 0 1 0 0-6 3 3 0 0 0 0 6z M19.4 13a7.6 7.6 0 0 0 0-2l2-1.6-2-3.4-2.4 1a7.4 7.4 0 0 0-1.7-1L15 3.5h-4l-.4 2.5a7.4 7.4 0 0 0-1.7 1l-2.4-1-2 3.4 2 1.6a7.6 7.6 0 0 0 0 2l-2 1.6 2 3.4 2.4-1a7.4 7.4 0 0 0 1.7 1l.4 2.5h4l.4-2.5a7.4 7.4 0 0 0 1.7-1l2.4 1 2-3.4z",
    "code":     "M4 4h16v16H4z M9 9l-3 3 3 3 M15 9l3 3-3 3",
    "tv":       "M3 5h18v12H3z M8 21h8",
    "play":     "M6 4l14 8-14 8z",
    "file":     "M6 2h8l5 5v15H6z M14 2v5h5 M9 13h6 M9 17h6",
    "lock":     "M6 11h12v10H6z M8 11V7a4 4 0 0 1 8 0v4",
    "globe":    "M12 3a9 9 0 1 0 0 18 9 9 0 0 0 0-18z M3 12h18 M12 3c2.5 2.7 3.8 5.7 3.8 9s-1.3 6.3-3.8 9 M12 3c-2.5 2.7-3.8 5.7-3.8 9s1.3 6.3 3.8 9",
    "wifi":     "M2 9a15 15 0 0 1 20 0 M5.5 12.5a10 10 0 0 1 13 0 M9 16a5 5 0 0 1 6 0 M12 19.5h.01",
    "disk":     "M3 6h18v12H3z M7 14h.01 M11 14h6",
    "terminal": "M3 5h18v14H3z M7 10l3 2.5L7 15 M12.5 15h4.5",
    "calendar": "M4 6h16v15H4z M4 10h16 M8 3v5 M16 3v5 M8 14h2 M14 14h2 M8 17.5h2",
    "refresh":  "M20 12a8 8 0 1 1-2.3-5.7 M20 4v4.5h-4.5",
    "search":   "M10.5 4a6.5 6.5 0 1 0 0 13 6.5 6.5 0 1 0 0-13z M15.5 15.5 20 20",
    "filter":   "M4 5h16l-6 7.5V19l-4 1.5v-8z",
    "send":     "M21 3 3 10.5l7.5 3 3 7.5z M10.5 13.5 21 3",
    "alert":    "M12 3 22 20H2z M12 10v4 M12 17h.01",
    "archive":  "M3 4h18v4H3z M5 8v12h14V8 M10 12h4",
    "tag":      "M3 3h8l10 10-8 8L3 11z M7.5 7.5h.01",
    "user_plus":  "M10 11a4 4 0 1 0 0-8 4 4 0 1 0 0 8z M3 21c0-4 3-7 7-7s7 3 7 7 M19 8v6 M16 11h6",
    "user_x":     "M10 11a4 4 0 1 0 0-8 4 4 0 1 0 0 8z M3 21c0-4 3-7 7-7s7 3 7 7 M16.5 8.5l5 5 M21.5 8.5l-5 5",
    "user_check": "M10 11a4 4 0 1 0 0-8 4 4 0 1 0 0 8z M3 21c0-4 3-7 7-7s7 3 7 7 M16 11l2 2 4-4",
    "bucket":   "M4 6h16l-2 14H6z M4 6c0-1.5 3.6-2.5 8-2.5s8 1 8 2.5",
    "download": "M12 3v12 M7 10l5 5 5-5 M4 20h16",
    "wrench":   "M14.7 6.3a4 4 0 0 1 5-1.5l-2.6 2.6.5 2 2 .5 2.6-2.6a4 4 0 0 1-5.4 5.1L10 19.2",
    "bug":      "M9 7a3 3 0 0 1 6 0 M7 9h10v5a5 5 0 0 1-10 0z M12 9v10 M3 12h4 M17 12h4",
    "pulse":    "M3 12h4l2.5-6 5 12 2.5-6h4",
    "sliders":  "M4 6h9 M17 6h3 M4 12h3 M11 12h9 M4 18h11 M19 18h1 M15 4v4 M9 10v4 M17 16v4",
    "heart":    "M12 20s-7.5-4.6-7.5-10A4.5 4.5 0 0 1 12 7a4.5 4.5 0 0 1 7.5 3c0 5.4-7.5 10-7.5 10z",
    "sparkle":  "M11 3l1.9 5.6L18.5 10.5l-5.6 1.9L11 18l-1.9-5.6L3.5 10.5l5.6-1.9z",
    "rewind":   "M11 6 4 12l7 6z M20 6l-7 6 7 6z",
}


class Canvas:
    """Parts plus a size. No layout engine, on purpose."""

    def __init__(self, w: int, h: int, scheme: str, label: str) -> None:
        self.w, self.h, self.c, self.label = w, h, SCHEMES[scheme], label
        self.parts: list[str] = []

    def add(self, *svg: str) -> "Canvas":
        self.parts.extend(svg)
        return self

    # ── primitives ────────────────────────────────────────────────────────
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

    def diamond(self, cx, cy, w, h, lines):
        c = self.c
        pts = f"{cx},{cy - h/2} {cx + w/2},{cy} {cx},{cy + h/2} {cx - w/2},{cy}"
        out = [f'<polygon points="{pts}" fill="{c["soft"]}" stroke="{c["border"]}" '
               f'stroke-width="1"/>']
        n = len(lines)
        for i, s in enumerate(lines):
            out.append(self.text(cx, cy - (n - 1) * 7 + i * 14 + 4, s, size=12,
                                 colour=c["title"], anchor="middle"))
        return "".join(out)

    def pill(self, cx, cy, text, *, tone="plain", pad=16, size=13):
        c = self.c
        w = len(text) * size * 0.58 + pad * 2
        h = 32
        fill, edge, col = c["card"], c["border"], c["title"]
        if tone == "accent":
            fill = edge = c["accent"]; col = c["on_accent"]
        elif tone == "soft":
            fill = c["soft"]
        return (f'<rect x="{cx - w/2:.1f}" y="{cy - h/2}" width="{w:.1f}" height="{h}" '
                f'rx="{h/2}" fill="{fill}" stroke="{edge}" stroke-width="1"/>'
                + self.text(cx, cy + 4.5, text, size=size, colour=col, anchor="middle",
                            weight="500")), w

    def edge(self, pts, *, label=None, dash=False, both=False, label_at=0.5,
             label_dy=-9, label_anchor="middle", mono=True):
        c = self.c
        d = ' stroke-dasharray="5 4"' if dash else ""
        path = " ".join(f"{x},{y}" for x, y in pts)
        out = [f'<polyline points="{path}" fill="none" stroke="{c["line"]}" '
               f'stroke-width="1.5"{d} marker-end="url(#a)"'
               + (' marker-start="url(#b)"' if both else "") + "/>"]
        if label:
            (x1, y1), (x2, y2) = pts[0], pts[-1]
            lx = x1 + (x2 - x1) * label_at
            ly = y1 + (y2 - y1) * label_at
            out.append(self.text(lx, ly + label_dy, label, size=11.5,
                                 colour=c["chip"], font=MONO if mono else SANS,
                                 anchor=label_anchor))
        return "".join(out)

    def group(self, x, y, w, h, title):
        c = self.c
        return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" '
                f'fill="{c["group"]}" stroke="{c["border"]}" stroke-width="1" '
                f'stroke-dasharray="6 5"/>'
                + self.text(x + 18, y + 24, title, size=12, colour=c["sub"],
                            weight="600"))

    def footer(self, note):
        return (f'<line x1="24" y1="{self.h - 52}" x2="{self.w - 24}" y2="{self.h - 52}" '
                f'stroke="{self.c["rule"]}" stroke-width="1"/>'
                + self.text(24, self.h - 26, note, size=12.5, colour=self.c["sub"]))

    def render(self) -> str:
        c = self.c
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" '
            f'width="{self.w}" height="{self.h}" role="img" aria-label="{escape(self.label)}">'
            f'<defs>'
            f'<marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" '
            f'markerHeight="6" orient="auto-start-reverse">'
            f'<path d="M0 0 10 5 0 10z" fill="{c["line"]}"/></marker>'
            f'<marker id="b" viewBox="0 0 10 10" refX="1" refY="5" markerWidth="6" '
            f'markerHeight="6" orient="auto">'
            f'<path d="M10 0 0 5 10 10z" fill="{c["line"]}"/></marker>'
            f'</defs>' + "".join(self.parts) + "</svg>"
        )


# ── the diagrams ──────────────────────────────────────────────────────────
# Glyphs this repository needs that the shared kit does not carry.
ICONS.update({
    "wave":    "M2 12h3l2.5-6 3.5 12 3-9 2 3h6",
    "speaker": "M4 9h4l5-4v14l-5-4H4z M16 9a4 4 0 0 1 0 6 M18.5 6.5a7.5 7.5 0 0 1 0 11",
    "battery": "M3 8h15v8H3z M18 10.5h2.5v3H18 M6 11v2 M9 11v2 M12 11v2",
})


def chip(k, x, y, s, *, anchor="start"):
    """A wire label that is not attached to a single straight edge."""
    return k.text(x, y, s, size=11.5, colour=k.c["chip"], font=MONO, anchor=anchor)


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
        k.box(xs[3], top, W, H, "Speaker", ["Stock 4 Ω 3 W,", "moved off P2"], icon="speaker"),
        k.edge([(xs[0] + W + 8, mid), (xs[1] - 8, mid)], label="Wi-Fi"),
        k.edge([(xs[1] + W + 8, mid), (xs[2] - 8, mid)], label="I2S"),
        k.edge([(xs[2] + W + 8, mid), (xs[3] - 8, mid)], label="+ / −"),
        k.box(kb_x, kb_y, kb_w, 72, "KALLSUP board, stock",
              ["Battery, USB-C charging, power button, second button"], icon="battery", tone="soft"),
        k.edge([(esp_x, kb_y - 8), (esp_x, top + H + 8)], dash=True),
        chip(k, esp_x + 12, (kb_y + top + H) / 2 + 4, "battery, button"),
        k.edge([(amp_x, kb_y - 8), (amp_x, top + H + 8)], dash=True),
        chip(k, amp_x + 12, (kb_y + top + H) / 2 + 4, "battery"),
        k.footer("The stock board keeps the battery, charging and power button. "
                 "The ESP32 and the amplifier only add Wi-Fi audio."),
    )
    return k.render()


def wiring(scheme):
    k = Canvas(1180, 480, scheme,
               "Switched battery feeds the MAX98357A Vin and the ESP32, either on its 5V pin "
               "or through a TPS63020 on its 3V3 pin. The second-button pad goes to GPIO1. GPIO2, 3 and 4 carry "
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
              ["Stock 4 Ω 3 W, off P2", "red to +, black to −"], icon="speaker"),
        k.edge([(332, 100), (432, 100)], label="VIN"),
        k.edge([(580, 160), (580, 228)]),
        chip(k, 592, 198, "OUT to 3V3"),
        k.edge([(332, 152), (380, 152), (380, 290), (432, 290)]),
        chip(k, 336, 278, "GPIO1"),
        k.edge([(728, 296), (848, 296)], label="GPIO2, 3, 4"),
        k.edge([(1006, 228), (1006, 160)]),
        chip(k, 1018, 198, "+ / −"),
        k.edge([(174, 184), (174, 404), (1006, 404), (1006, 364)]),
        chip(k, 590, 396, "battery to Vin", anchor="middle"),
        k.footer("Every GND pin joins GND1. Measure the two marked pads before soldering: "
                 "docs/build-guide.md."),
    )
    return k.render()


# ── hookup views: the boards as they sit on the desk ──────────────────────
# Pin order is copied from the vendors' own pinout images: Waveshare's
# ESP32-S3-Zero (left edge, USB-C up: 5V, GND, 3V3, GP1 to GP6) and Adafruit's
# MAX98357A (header left to right: LRC, BCLK, DIN, GAIN, SD, GND, Vin; speaker
# terminal minus on the left). Wire colour carries meaning here, so these two
# pictures use a wire palette on top of the kit's single accent.
WIRE = {
    "light": dict(bat="#dc2626", gnd="#1f2937", btn="#ca8a04", din="#16a34a",
                  bclk="#2563eb", lrc="#9333ea", pad="#c9a227", page="#ffffff"),
    "dark":  dict(bat="#f87171", gnd="#d1d5db", btn="#facc15", din="#4ade80",
                  bclk="#60a5fa", lrc="#c084fc", pad="#d4b04a", page="#0d1117"),
}

ESP_X, ESP_Y, ESP_W, ESP_H = 380, 150, 340, 160
MAX_X, MAX_Y, MAX_W, MAX_H = 820, 150, 330, 160
PIN_Y = ESP_Y + ESP_H - 18
# USB-C turned to the left, so the pin edge reads left to right along the bottom.
ESP_PINS = ["5V", "GND", "3V3", "GP1", "GP2", "GP3", "GP4", "GP5", "GP6"]
MAX_PINS = ["LRC", "BCLK", "DIN", "GAIN", "SD", "GND", "Vin"]


def esp_pin(name):
    return ESP_X + 32 + ESP_PINS.index(name) * 34


def max_pin(name):
    return MAX_X + 35 + MAX_PINS.index(name) * 43


def wire(k, pts, colour):
    """A wire with a halo in the page colour, so crossings read as over/under."""
    w = WIRE[k.scheme]
    path = " ".join(f"{x},{y}" for x, y in pts)
    return (f'<polyline points="{path}" fill="none" stroke="{w["page"]}" '
            f'stroke-width="7" stroke-linejoin="round" stroke-linecap="round"/>'
            f'<polyline points="{path}" fill="none" stroke="{colour}" '
            f'stroke-width="3.5" stroke-linejoin="round" stroke-linecap="round"/>')


def pad(k, x, y, r=7):
    w = WIRE[k.scheme]
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="{w["pad"]}" '
            f'stroke="{k.c["title"]}" stroke-opacity="0.35" stroke-width="1"/>')


def boards(k):
    c, out = k.c, []
    # ESP32-S3-Zero, top view, USB-C pointing left.
    out.append(f'<rect x="{ESP_X}" y="{ESP_Y}" width="{ESP_W}" height="{ESP_H}" rx="12" '
               f'fill="{c["accent"]}" stroke="{c["accent"]}"/>')
    out.append(f'<rect x="{ESP_X - 18}" y="{ESP_Y + 52}" width="30" height="46" rx="6" '
               f'fill="{c["soft"]}" stroke="{c["border"]}"/>')
    out.append(k.text(ESP_X + 26, ESP_Y + 34, "ESP32-S3-Zero", size=15,
                      colour=c["on_accent"], weight="600"))
    out.append(k.text(ESP_X + 26, ESP_Y + 54, "top view, USB-C on the left", size=12.5,
                      colour=c["on_accent"], opacity="0.85"))
    for name in ESP_PINS:
        x = esp_pin(name)
        out.append(k.text(x, PIN_Y - 16, name, size=10.5, colour=c["on_accent"],
                          font=MONO, anchor="middle"))
        out.append(pad(k, x, PIN_Y))
    # MAX98357A, top view, as Adafruit prints it.
    out.append(f'<rect x="{MAX_X}" y="{MAX_Y}" width="{MAX_W}" height="{MAX_H}" rx="12" '
               f'fill="{c["card"]}" stroke="{c["border"]}"/>')
    out.append(f'<rect x="{MAX_X + 95}" y="{MAX_Y + 14}" width="140" height="40" rx="4" '
               f'fill="{c["soft"]}" stroke="{c["border"]}"/>')
    for sx, sign, dx in ((MAX_X + 130, "−", -24), (MAX_X + 200, "+", 24)):
        out.append(f'<circle cx="{sx}" cy="{MAX_Y + 34}" r="9" fill="{c["card"]}" '
                   f'stroke="{c["line"]}" stroke-width="1.5"/>')
        out.append(k.text(sx + dx, MAX_Y + 39, sign, size=15, colour=c["title"],
                          weight="600", anchor="middle"))
    out.append(k.text(MAX_X + 20, MAX_Y + 84, "MAX98357A", size=15, colour=c["title"],
                      weight="600"))
    for name in MAX_PINS:
        x = max_pin(name)
        out.append(k.text(x, PIN_Y - 16, name, size=10.5, colour=c["title"],
                          font=MONO, anchor="middle"))
        out.append(pad(k, x, PIN_Y))
    return out


def speaker(k, label):
    x, y = MAX_X + 85, 24
    w = WIRE[k.scheme]
    return [
        k.box(x, y, 160, 56, label, icon="speaker"),
        wire(k, [(MAX_X + 200, y + 56), (MAX_X + 200, MAX_Y + 34)], w["bat"]),
        wire(k, [(MAX_X + 130, y + 56), (MAX_X + 130, MAX_Y + 34)], w["gnd"]),
    ]


def audio_wires(k):
    """GPIO2, 3 and 4 to DIN, BCLK and LRC, nested so none of them cross."""
    w, out = WIRE[k.scheme], []
    for gp, amp, lane, col in (("GP4", "LRC", 356, "lrc"), ("GP3", "BCLK", 380, "bclk"),
                               ("GP2", "DIN", 404, "din")):
        a, b = esp_pin(gp), max_pin(amp)
        out.append(wire(k, [(a, PIN_Y), (a, lane), (b, lane), (b, PIN_Y)], w[col]))
    return out


def legend(k, y, items):
    w, out, x = WIRE[k.scheme], [], 24
    for key, text in items:
        out.append(f'<line x1="{x}" y1="{y}" x2="{x + 26}" y2="{y}" stroke="{w[key]}" '
                   f'stroke-width="3.5" stroke-linecap="round"/>')
        out.append(k.text(x + 34, y + 4.5, text, size=12.5))
        x += 34 + len(text) * 7.1 + 26
    return out


def hookup_bench(scheme):
    k = Canvas(1180, 560, scheme,
               "Bench test with jumper wires: ESP32 5V to MAX98357A Vin, GND to GND, GPIO2 to "
               "DIN, GPIO3 to BCLK, GPIO4 to LRC, any small speaker on the terminal, USB-C "
               "to the computer.")
    k.scheme = scheme
    w = WIRE[scheme]
    g5, gg = esp_pin("5V"), esp_pin("GND")
    mg, mv = max_pin("GND"), max_pin("Vin")
    k.add(
        *boards(k), *speaker(k, "Any 4–8 Ω"), *audio_wires(k),
        wire(k, [(gg, PIN_Y), (gg, 428), (mg, 428), (mg, PIN_Y)], w["gnd"]),
        wire(k, [(g5, PIN_Y), (g5, 452), (mv, 452), (mv, PIN_Y)], w["bat"]),
        k.edge([(ESP_X - 26, ESP_Y + 75), (170, ESP_Y + 75)], label="USB-C cable"),
        k.text(24, ESP_Y + 70, "Computer", size=14, colour=k.c["title"], weight="600"),
        k.text(24, ESP_Y + 92, "powers the bench test", size=12.5),
        k.text(24, ESP_Y + 110, "and does the first flash", size=12.5),
        *legend(k, 488, [("bat", "5V to Vin"), ("gnd", "GND to GND"), ("din", "GP2 to DIN"),
                         ("bclk", "GP3 to BCLK"), ("lrc", "GP4 to LRC")]),
        k.footer("Five jumper wires. GAIN and SD stay unconnected. Nothing here touches the KALLSUP yet."),
    )
    return k.render()


def hookup_kallsup(scheme):
    k = Canvas(1180, 780, scheme,
               "Inside the KALLSUP: the switched battery point feeds ESP32 5V and MAX98357A "
               "Vin, GND1 goes to both GND pins, the second-button pad goes to GPIO1, the "
               "audio wires stay as on the bench, and the stock speaker moves to the terminal.")
    k.scheme = scheme
    c, w = k.c, WIRE[scheme]
    bx, by, bw, bh = 24, 520, 560, 150
    py = by + 44                      # the three pads
    sw, gnd, btn = 150, 300, 450
    g5, gg, g1 = esp_pin("5V"), esp_pin("GND"), esp_pin("GP1")
    mg, mv = max_pin("GND"), max_pin("Vin")
    k.add(
        *boards(k), *speaker(k, "Stock, off P2"), *audio_wires(k),
        f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="12" fill="{c["soft"]}" '
        f'stroke="{c["border"]}"/>',
        k.icon("battery", bx + 16, by + bh - 34, c["title"]),
        k.text(bx + 47, by + bh - 18, "KALLSUP board, back side", size=14,
               colour=c["title"], weight="600"),
        # Up to the ESP32, nested so that none of the three cross.
        wire(k, [(sw, py), (sw, 432), (g5, 432), (g5, PIN_Y)], w["bat"]),
        wire(k, [(gnd, py), (gnd, 456), (gg, 456), (gg, PIN_Y)], w["gnd"]),
        wire(k, [(btn, py), (btn, 480), (g1, 480), (g1, PIN_Y)], w["btn"]),
        # Down, along the board and up to the amplifier: a second wire from each point.
        wire(k, [(gnd, py), (gnd, by + 100), (mg, by + 100), (mg, PIN_Y)], w["gnd"]),
        wire(k, [(sw, py), (sw, by + 118), (mv, by + 118), (mv, PIN_Y)], w["bat"]),
        pad(k, sw, py, r=9), pad(k, gnd, py, r=9), pad(k, btn, py, r=9),
        k.text(sw + 16, py - 4, "switched point", size=12.5, colour=c["title"]),
        k.text(sw + 16, py + 13, "found by check 1", size=11.5),
        k.text(gnd + 16, py - 4, "GND1", size=12.5, colour=c["title"], font=MONO),
        k.text(gnd + 16, py + 13, "by the USB-C port", size=11.5),
        k.text(btn + 16, py - 4, "S1 or S2", size=12.5, colour=c["title"], font=MONO),
        k.text(btn + 16, py + 13, "found by check 3", size=11.5),
        k.text(640, by + 30, "Optional TPS63020: switched point to its VIN,", size=12.5),
        k.text(640, by + 48, "its OUT to the ESP32 3V3 pad instead of 5V.", size=12.5),
        k.text(640, by + 66, "Never feed both 5V and 3V3.", size=12.5, colour=c["warn"],
               weight="600"),
        *legend(k, by + bh + 30, [("bat", "switched battery"), ("gnd", "ground"),
                                  ("btn", "button"), ("din", "DIN"), ("bclk", "BCLK"),
                                  ("lrc", "LRC")]),
        k.footer("Three joints on the KALLSUP board. Do checks 1 and 3 in docs/build-guide.md "
                 "before soldering the two that depend on them."),
    )
    return k.render()


DIAGRAMS = {"architecture": architecture, "wiring": wiring,
            "hookup-bench": hookup_bench, "hookup-kallsup": hookup_kallsup}


def main() -> None:
    import sys
    check = "--check" in sys.argv[1:]
    out = ROOT / "docs" / "assets"
    out.mkdir(parents=True, exist_ok=True)
    stale = []
    for name, fn in DIAGRAMS.items():
        for scheme in SCHEMES:
            path = out / f"{name}-{scheme}.svg"
            svg = fn(scheme)
            if check:
                if not path.exists() or path.read_text(encoding="utf-8") != svg:
                    stale.append(str(path.relative_to(ROOT)))
            else:
                path.write_text(svg, encoding="utf-8")
    if check:
        if stale:
            print("stale diagrams (run python3 tools/gen_diagram.py):\n  " + "\n  ".join(stale))
            sys.exit(1)
        print(f"{len(DIAGRAMS) * len(SCHEMES)} diagram files up to date")
        return
    print(f"{len(DIAGRAMS)} diagrams x {len(SCHEMES)} schemes -> docs/assets/")


if __name__ == "__main__":
    main()
