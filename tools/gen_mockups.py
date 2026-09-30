#!/usr/bin/env python3
"""Draw the build mockups: the real boards, wired, as they look on the bench.

  docs/assets/mockups/bench-test.svg      the ESP32 and MAX98357A on jumper wires
  docs/assets/mockups/inside-kallsup.svg  the same, wired to the KALLSUP board
  docs/assets/mockups/solder-a-pad.svg    four close-ups: soldering a wire to a pad

  python3 tools/gen_mockups.py           # write them
  python3 tools/gen_mockups.py --check   # fail if a committed file is stale

The ESP32-S3-Zero and MAX98357A are drawn to scale from the vendors' own
pinout images: Waveshare's (left edge with USB-C up: 5V, GND, 3V3, GP1 to GP6;
right edge: TX, RX, GP13 to GP7) and Adafruit's (header left to right: LRC,
BCLK, DIN, GAIN, SD, GND, Vin; speaker terminal minus on the left). The
KALLSUP board is laid out from the teardown photo, so its pads sit where they
are on the real board, and each carries its silkscreen name. A joint that a
build-guide check has not settled ends in a tag, never on a guessed pad.

Each picture carries its own bench-mat background, so one file serves both
GitHub colour schemes.
"""
from __future__ import annotations

import pathlib
import sys
from xml.sax.saxutils import escape

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "assets" / "mockups"
SANS = "system-ui,-apple-system,'Segoe UI',Roboto,Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,monospace"
MM = 13  # pixels per millimetre for the two small boards

WIRE = {  # body, outline
    "red": ("#d62828", "#8f1414"), "black": ("#2b2d31", "#0b0c0e"),
    "green": ("#2a9d4b", "#17602c"), "blue": ("#2f6fe0", "#1a4596"),
    "purple": ("#8e44ad", "#5b2672"), "yellow": ("#e0a100", "#8f6700"),
}
INK, SUB, MAT, GRID = "#1f2937", "#4b5563", "#dfe4ea", "#cdd4dc"

ESP_BOTTOM = ["5V", "GND", "3V3", "1", "2", "3", "4", "5", "6"]
ESP_TOP = ["TX", "RX", "13", "12", "11", "10", "9", "8", "7"]
MAX_PINS = ["LRC", "BCLK", "DIN", "GAIN", "SD", "GND", "Vin"]


# ── primitives ──────────────────────────────────────────────────────────────

def text(x, y, s, *, size=14, colour=INK, weight=None, anchor="start", font=SANS,
         opacity=None):
    extra = (f' font-weight="{weight}"' if weight else "") + \
            (f' opacity="{opacity}"' if opacity else "")
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{font}" font-size="{size}" '
            f'fill="{colour}" text-anchor="{anchor}"{extra}>{escape(s)}</text>')


def defs():
    return (
        '<defs>'
        '<linearGradient id="esp" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="#2a58bf"/><stop offset="1" stop-color="#1d438f"/></linearGradient>'
        '<linearGradient id="ada" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="#2f6ad6"/><stop offset="1" stop-color="#2150a8"/></linearGradient>'
        '<linearGradient id="metal" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="#f4f6f8"/><stop offset=".5" stop-color="#b9c0c8"/>'
        '<stop offset="1" stop-color="#e6e9ec"/></linearGradient>'
        '<radialGradient id="gold" cx=".4" cy=".35" r=".7">'
        '<stop offset="0" stop-color="#fbe7a1"/><stop offset=".6" stop-color="#d4a73a"/>'
        '<stop offset="1" stop-color="#9c7418"/></radialGradient>'
        '<radialGradient id="tin" cx=".35" cy=".3" r=".75">'
        '<stop offset="0" stop-color="#ffffff"/><stop offset=".35" stop-color="#d7dce1"/>'
        '<stop offset="1" stop-color="#7d868f"/></radialGradient>'
        '<radialGradient id="cone" cx=".5" cy=".5" r=".5">'
        '<stop offset="0" stop-color="#50565e"/><stop offset=".75" stop-color="#2d3238"/>'
        '<stop offset="1" stop-color="#1c1f23"/></radialGradient>'
        '<linearGradient id="iron" x1="0" y1="0" x2="1" y2="0">'
        '<stop offset="0" stop-color="#6b7280"/><stop offset=".45" stop-color="#e5e7eb"/>'
        '<stop offset="1" stop-color="#4b5563"/></linearGradient>'
        '<linearGradient id="copper" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="#f3b27a"/><stop offset=".5" stop-color="#c46a2c"/>'
        '<stop offset="1" stop-color="#e89a5c"/></linearGradient>'
        '<filter id="shadow" x="-10%" y="-10%" width="130%" height="130%">'
        '<feDropShadow dx="2" dy="4" stdDeviation="4" flood-color="#0f172a" flood-opacity=".28"/></filter>'
        '</defs>'
    )


def mat(w, h):
    lines = [f'<rect width="{w}" height="{h}" rx="18" fill="{MAT}"/>']
    for x in range(40, w, 40):
        lines.append(f'<line x1="{x}" y1="0" x2="{x}" y2="{h}" stroke="{GRID}" '
                     f'stroke-width="{1.4 if x % 200 == 0 else .7}"/>')
    for y in range(40, h, 40):
        lines.append(f'<line x1="0" y1="{y}" x2="{w}" y2="{y}" stroke="{GRID}" '
                     f'stroke-width="{1.4 if y % 200 == 0 else .7}"/>')
    return "".join(lines)


def rounded(pts, r=22):
    """An orthogonal polyline with rounded corners, as an SVG path."""
    d = [f"M{pts[0][0]:.1f},{pts[0][1]:.1f}"]
    for (x0, y0), (x1, y1), (x2, y2) in zip(pts, pts[1:], pts[2:]):
        la = max(abs(x1 - x0), abs(y1 - y0))
        lb = max(abs(x2 - x1), abs(y2 - y1))
        k = min(r, la / 2, lb / 2)
        ax = x1 - (x1 - x0) / la * k if la else x1
        ay = y1 - (y1 - y0) / la * k if la else y1
        bx = x1 + (x2 - x1) / lb * k if lb else x1
        by = y1 + (y2 - y1) / lb * k if lb else y1
        d.append(f"L{ax:.1f},{ay:.1f} Q{x1:.1f},{y1:.1f} {bx:.1f},{by:.1f}")
    d.append(f"L{pts[-1][0]:.1f},{pts[-1][1]:.1f}")
    return " ".join(d)


def wire(path, colour, width=8):
    body, edge = WIRE[colour]
    return (f'<path d="{path}" fill="none" stroke="#0f172a" stroke-opacity=".18" '
            f'stroke-width="{width + 4}" stroke-linecap="round" stroke-linejoin="round" '
            f'transform="translate(2,4)"/>'
            f'<path d="{path}" fill="none" stroke="{edge}" stroke-width="{width + 2.5}" '
            f'stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="{path}" fill="none" stroke="{body}" stroke-width="{width}" '
            f'stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="{path}" fill="none" stroke="#ffffff" stroke-opacity=".32" '
            f'stroke-width="{width * .28:.1f}" stroke-linecap="round" stroke-linejoin="round" '
            f'transform="translate(-1,-1.5)"/>')


def dupont(x, y, down=True):
    """A female jumper housing on a header pin, running away from the board edge."""
    h, w = 8 * MM, 2.35 * MM
    y0 = y if down else y - h
    return (f'<g filter="url(#shadow)"><rect x="{x - w / 2:.1f}" y="{y0:.1f}" width="{w:.1f}" '
            f'height="{h:.1f}" rx="3" fill="#1b1d21"/>'
            f'<rect x="{x - w / 2 + 3:.1f}" y="{y0 + 4:.1f}" width="4" height="{h - 8:.1f}" '
            f'rx="2" fill="#ffffff" opacity=".12"/></g>')


def blob(x, y, r=9):
    return (f'<ellipse cx="{x + 1.5:.1f}" cy="{y + 2.5:.1f}" rx="{r}" ry="{r * .8:.1f}" '
            f'fill="#0f172a" opacity=".25"/>'
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="url(#tin)" stroke="#6b7280" '
            f'stroke-width="1"/>')


def pill(x, y, s, colour, *, anchor="middle"):
    w = len(s) * 7.6 + 22
    x0 = x - w / 2 if anchor == "middle" else x
    body = WIRE[colour][0]
    return (f'<rect x="{x0:.1f}" y="{y - 13:.1f}" width="{w:.1f}" height="26" rx="13" '
            f'fill="#ffffff" stroke="{body}" stroke-width="2"/>'
            + text(x0 + w / 2, y + 4.5, s, size=12.5, colour=INK, weight="600",
                   anchor="middle", font=MONO))


def caption(x, y, title, sub=None):
    out = [text(x, y, title, size=15, weight="700")]
    if sub:
        out.append(text(x, y + 19, sub, size=12.5, colour=SUB))
    return "".join(out)


# ── components ──────────────────────────────────────────────────────────────

class Esp32:
    """Waveshare ESP32-S3-Zero, top view, turned so USB-C points left.

    Turning it this way puts its 5V, GND, 3V3, GP1..GP6 edge along the bottom,
    reading left to right, and TX, RX, GP13..GP7 along the top.
    """

    W, H = 23.5 * MM, 18 * MM

    def __init__(self, x, y):
        self.x, self.y = x, y

    def pin(self, name, edge="bottom"):
        names = ESP_BOTTOM if edge == "bottom" else ESP_TOP
        px = self.x + (1.75 + names.index(name) * 2.54) * MM
        py = self.y + self.H if edge == "bottom" else self.y
        return px, py

    def svg(self):
        x, y, W, H = self.x, self.y, self.W, self.H
        o = [f'<g filter="url(#shadow)"><rect x="{x}" y="{y}" width="{W:.1f}" height="{H:.1f}" '
             f'rx="9" fill="url(#esp)" stroke="#15347a" stroke-width="1.5"/></g>']
        # Castellated pads on both long edges.
        for edge, names in (("bottom", ESP_BOTTOM), ("top", ESP_TOP)):
            for n in names:
                px, py = self.pin(n, edge)
                inward = -1 if edge == "bottom" else 1
                o.append(f'<rect x="{px - .75 * MM:.1f}" y="{py + inward * 1.9 * MM if inward > 0 else py - 1.9 * MM:.1f}" '
                         f'width="{1.5 * MM:.1f}" height="{1.9 * MM:.1f}" rx="2" fill="url(#gold)"/>')
                o.append(f'<path d="M{px - .55 * MM:.1f},{py:.1f} A{.55 * MM:.1f},{.55 * MM:.1f} 0 0 {1 if edge == "bottom" else 0} {px + .55 * MM:.1f},{py:.1f} Z" fill="{MAT}"/>')
                ly = py - 2.7 * MM if edge == "bottom" else py + 3.35 * MM
                o.append(text(px, ly, n, size=10.5, colour="#ffffff", anchor="middle",
                              font=MONO, weight="600"))
        # USB-C receptacle, overhanging the left edge.
        ux, uy = x - 1.2 * MM, y + H / 2 - 4.5 * MM
        o.append(f'<rect x="{ux:.1f}" y="{uy:.1f}" width="{6.6 * MM:.1f}" height="{9.0 * MM:.1f}" '
                 f'rx="{1.4 * MM:.1f}" fill="url(#metal)" stroke="#8a939c" stroke-width="1.2"/>')
        o.append(f'<rect x="{ux + .5 * MM:.1f}" y="{uy + 1.2 * MM:.1f}" width="{1.1 * MM:.1f}" '
                 f'height="{6.6 * MM:.1f}" rx="4" fill="#3b4047"/>')
        # BOOT and RESET buttons beside the connector, and the WS2812 LED between them.
        for bx, by in ((x + 7.4 * MM, y + 10.0 * MM), (x + 7.4 * MM, y + 4.3 * MM)):
            o.append(f'<rect x="{bx:.1f}" y="{by:.1f}" width="{3.6 * MM:.1f}" height="{3.8 * MM:.1f}" '
                     f'rx="3" fill="url(#metal)" stroke="#8a939c"/>')
            o.append(f'<circle cx="{bx + 1.8 * MM:.1f}" cy="{by + 1.9 * MM:.1f}" r="{1.05 * MM:.1f}" fill="#22262b"/>')
        lx, ly = x + 12.2 * MM, y + H / 2 - 1.1 * MM
        o.append(f'<rect x="{lx:.1f}" y="{ly:.1f}" width="{2.2 * MM:.1f}" height="{2.2 * MM:.1f}" '
                 f'rx="2" fill="#f5f5f4" stroke="#a8a29e"/>')
        o.append(f'<circle cx="{lx + 1.1 * MM:.1f}" cy="{ly + 1.1 * MM:.1f}" r="4" fill="#e11d48" opacity=".75"/>')
        # The ESP32-S3 module chip, set diagonally as on the board.
        cx, cy, s = x + 17.4 * MM, y + H / 2, 6.4 * MM
        o.append(f'<g transform="rotate(45 {cx:.1f} {cy:.1f})">'
                 f'<rect x="{cx - s / 2:.1f}" y="{cy - s / 2:.1f}" width="{s:.1f}" height="{s:.1f}" '
                 f'rx="3" fill="#15171a" stroke="#3f444b"/>'
                 f'<circle cx="{cx - s / 2 + 9:.1f}" cy="{cy - s / 2 + 9:.1f}" r="3" fill="#3f444b"/></g>')
        # A few passives.
        for px, py in ((12.0, 5.2), (12.0, 11.8), (21.4, 6.2), (21.4, 11.0)):
            o.append(f'<rect x="{x + px * MM:.1f}" y="{y + py * MM:.1f}" width="{1.6 * MM:.1f}" '
                     f'height="{.9 * MM:.1f}" rx="2" fill="#c9b99a" stroke="#8b7d63" stroke-width=".8"/>')
        return "".join(o)


class Max98357:
    """Adafruit MAX98357A breakout, top view, header along the bottom.

    The board prints the header labels alternately above and below the holes;
    here they all sit above, because the jumpers cover the lower row.
    """

    W, H = 19.3 * MM, 17.7 * MM

    def __init__(self, x, y):
        self.x, self.y = x, y

    def pin(self, name):
        i = MAX_PINS.index(name)
        return self.x + (self.W - 6 * 2.54 * MM) / 2 + i * 2.54 * MM, self.y + self.H - 2.1 * MM

    def screw(self, sign):
        cx = self.x + self.W / 2 + (-1.75 if sign == "-" else 1.75) * MM
        return cx, self.y + 4.4 * MM

    def svg(self):
        x, y, W, H = self.x, self.y, self.W, self.H
        o = [f'<g filter="url(#shadow)"><rect x="{x}" y="{y}" width="{W:.1f}" height="{H:.1f}" '
             f'rx="{2.2 * MM:.1f}" fill="url(#ada)" stroke="#173f8a" stroke-width="1.5"/></g>']
        for hx in (x + 2.6 * MM, x + W - 2.6 * MM):
            o.append(f'<circle cx="{hx:.1f}" cy="{y + 2.6 * MM:.1f}" r="{1.9 * MM:.1f}" fill="url(#gold)"/>')
            o.append(f'<circle cx="{hx:.1f}" cy="{y + 2.6 * MM:.1f}" r="{1.25 * MM:.1f}" fill="{MAT}"/>')
        # 3.5 mm two-way screw terminal.
        tx, ty, tw, th = x + W / 2 - 3.9 * MM, y + .9 * MM, 7.8 * MM, 7 * MM
        o.append(f'<g filter="url(#shadow)"><rect x="{tx:.1f}" y="{ty:.1f}" width="{tw:.1f}" '
                 f'height="{th:.1f}" rx="4" fill="#1f7a4a" stroke="#14532d" stroke-width="1.2"/></g>')
        for sign in ("-", "+"):
            cx, cy = self.screw(sign)
            o.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{1.35 * MM:.1f}" fill="url(#metal)" stroke="#6b7280"/>')
            o.append(f'<line x1="{cx - 1.0 * MM:.1f}" y1="{cy - .45 * MM:.1f}" x2="{cx + 1.0 * MM:.1f}" '
                     f'y2="{cy + .45 * MM:.1f}" stroke="#4b5563" stroke-width="3" stroke-linecap="round"/>')
        for sign, dx in (("−", -5.4), ("+", 5.4)):
            o.append(text(x + W / 2 + dx * MM, y + 10.2 * MM, sign, size=19, colour="#ffffff",
                          weight="700", anchor="middle"))
        # The amplifier chip and its passives.
        o.append(f'<rect x="{x + 9.6 * MM:.1f}" y="{y + 9.2 * MM:.1f}" width="{3 * MM:.1f}" '
                 f'height="{3 * MM:.1f}" rx="3" fill="#15171a" stroke="#3f444b"/>')
        for px, py in ((14.2, 8.8), (15.9, 8.8), (14.2, 11.6), (3.4, 8.2), (6.0, 8.2)):
            o.append(f'<rect x="{x + px * MM:.1f}" y="{y + py * MM:.1f}" width="{1.3 * MM:.1f}" '
                     f'height="{2.0 * MM:.1f}" rx="2" fill="#c9b99a" stroke="#8b7d63" stroke-width=".8"/>')
        o.append(text(x + 1.4 * MM, y + 10.4 * MM, "MAX", size=12, colour="#ffffff", weight="700"))
        o.append(text(x + 1.4 * MM, y + 11.7 * MM, "98357A", size=12, colour="#ffffff", weight="700"))
        # Header holes, labels alternating above and below as on the board.
        for i, n in enumerate(MAX_PINS):
            px, py = self.pin(n)
            o.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{.95 * MM:.1f}" fill="url(#gold)"/>')
            o.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{.5 * MM:.1f}" fill="#11151c"/>')
            ly = py - 1.55 * MM
            o.append(text(px, ly, n, size=10.5, colour="#ffffff", font=MONO, weight="600",
                          anchor="middle"))
        return "".join(o)


def speaker(cx, cy, r, label_at=None):
    o = [f'<g filter="url(#shadow)"><circle cx="{cx}" cy="{cy}" r="{r}" fill="#1c1f23"/></g>',
         f'<circle cx="{cx}" cy="{cy}" r="{r * .9:.1f}" fill="#3a3f46"/>',
         f'<circle cx="{cx}" cy="{cy}" r="{r * .8:.1f}" fill="url(#cone)"/>']
    for k in (.62, .46):
        o.append(f'<circle cx="{cx}" cy="{cy}" r="{r * k:.1f}" fill="none" stroke="#5b626b" stroke-width="1"/>')
    o.append(f'<circle cx="{cx}" cy="{cy}" r="{r * .3:.1f}" fill="#15171a"/>')
    o.append(f'<ellipse cx="{cx - r * .08:.1f}" cy="{cy - r * .1:.1f}" rx="{r * .14:.1f}" '
             f'ry="{r * .08:.1f}" fill="#ffffff" opacity=".18"/>')
    return "".join(o)


def usb_cable(x, y, to_x):
    """A USB-C plug in the ESP32 with its cable running off to the left."""
    path = f"M{x - 5 * MM:.1f},{y:.1f} C{x - 14 * MM:.1f},{y:.1f} {to_x + 60},{y + 70} {to_x},{y + 70}"
    return (f'<path d="{path}" fill="none" stroke="#0f172a" stroke-opacity=".18" stroke-width="18" '
            f'transform="translate(2,4)"/>'
            f'<path d="{path}" fill="none" stroke="#3b4047" stroke-width="15" stroke-linecap="round"/>'
            f'<path d="{path}" fill="none" stroke="#ffffff" stroke-opacity=".18" stroke-width="4" '
            f'transform="translate(-1,-2)"/>'
            f'<g filter="url(#shadow)"><rect x="{x - 9 * MM:.1f}" y="{y - 3.6 * MM:.1f}" '
            f'width="{7 * MM:.1f}" height="{7.2 * MM:.1f}" rx="10" fill="#2b2f35"/>'
            f'<rect x="{x - 2.4 * MM:.1f}" y="{y - 2.2 * MM:.1f}" width="{2.6 * MM:.1f}" '
            f'height="{4.4 * MM:.1f}" rx="5" fill="url(#metal)"/></g>')


def speaker_leads(spk, screws):
    (sx, sy), ((mx, my), (px, py)) = spk, screws
    black = rounded([(sx - 40, sy + 20), (mx, sy + 20), (mx, my)], r=30)
    red = rounded([(sx - 40, sy - 20), (px + 60, sy - 20), (px + 60, my - 40), (px, my - 40), (px, my)], r=24)
    return wire(black, "black", 6) + wire(red, "red", 6) + blob(mx, my, 7) + blob(px, my, 7)


def svg_doc(w, h, label, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" '
            f'height="{h}" role="img" aria-label="{escape(label)}">' + defs() + mat(w, h)
            + "".join(body) + "</svg>\n")


# ── the pictures ────────────────────────────────────────────────────────────

def i2s(esp, amp, lanes):
    out = []
    for gp, pin, colour, lane in (("4", "LRC", "purple", lanes[0]), ("3", "BCLK", "blue", lanes[1]),
                                  ("2", "DIN", "green", lanes[2])):
        (ax, ay), (bx, by) = esp.pin(gp), amp.pin(pin)
        start, end = ay + 8 * MM, by + 8 * MM + (amp.y + amp.H - by)
        out.append(wire(rounded([(ax, start), (ax, lane), (bx, lane), (bx, end)]), colour))
    return out


def bench_test():
    w, h = 1400, 880
    esp, amp = Esp32(330, 210), Max98357(880, 216)
    lanes = [585, 620, 655]
    o = [text(40, 58, "Bench test", size=24, weight="700"),
         text(40, 84, "Five jumper wires, powered from the computer. Nothing touches the KALLSUP yet.",
              size=14, colour=SUB)]
    g5, gg = esp.pin("5V"), esp.pin("GND")
    mg, mv = amp.pin("GND"), amp.pin("Vin")
    esp_end = esp.y + esp.H + 8 * MM
    amp_end = amp.y + amp.H + 8 * MM
    o += i2s(esp, amp, lanes)
    o.append(wire(rounded([(gg[0], esp_end), (gg[0], 690), (mg[0], 690), (mg[0], amp_end)]), "black"))
    o.append(wire(rounded([(g5[0], esp_end), (g5[0], 725), (mv[0], 725), (mv[0], amp_end)]), "red"))
    o.append(usb_cable(esp.x - 1.4 * MM, esp.y + esp.H / 2, 0))
    o.append(esp.svg())
    o.append(amp.svg())
    for n in ("5V", "GND", "2", "3", "4"):
        o.append(dupont(esp.pin(n)[0], esp.y + esp.H))
    for n in ("LRC", "BCLK", "DIN", "GND", "Vin"):
        o.append(dupont(amp.pin(n)[0], amp.y + amp.H))
    spk = (1270, 190)
    o.append(speaker(*spk, 88))
    (mx, my), (px, py) = amp.screw("-"), amp.screw("+")
    o += [wire(rounded([(spk[0] - 50, spk[1] - 55), (mx, spk[1] - 55), (mx, my)], r=26), "black", 6),
          wire(rounded([(spk[0] - 70, spk[1] - 12), (px, spk[1] - 12), (px, py)], r=26), "red", 6),
          blob(mx, my, 7), blob(px, py, 7)]
    o += [pill(700, lanes[0], "GP4 → LRC", "purple"), pill(730, lanes[1], "GP3 → BCLK", "blue"),
          pill(760, lanes[2], "GP2 → DIN", "green"), pill(700, 690, "GND → GND", "black"),
          pill(700, 725, "5V → Vin", "red")]
    o += [caption(esp.x, esp.y - 52, "ESP32-S3-Zero", "top view, USB-C to the left"),
          caption(amp.x, amp.y - 52, "MAX98357A", "top view"),
          caption(1200, 310, "Any 4–8 Ω speaker"),
          caption(40, 420, "USB-C to the computer", "power and the first flash"),
          text(amp.x + amp.W + 14, amp.y + amp.H - 10, "GAIN and SD: leave empty", size=12.5, colour=SUB)]
    o.append(text(40, h - 24, "Illustration. Board outlines to scale; pin order from the Waveshare and "
                  "Adafruit pinouts.", size=12, colour=SUB))
    return svg_doc(w, h, "Bench test mockup: an ESP32-S3-Zero with USB-C to a computer, jumper wires "
                   "from 5V to Vin, GND to GND, GP2 to DIN, GP3 to BCLK and GP4 to LRC on a MAX98357A, "
                   "and a small speaker on the MAX98357A's screw terminal.", o)


def kallsup_board(x, y, w):
    """The KALLSUP E2507 board, back side, as a mockup; and a mapper to it.

    Layout coordinates are in teardown-photo pixels (the board spans about
    200..1240 by 60..850 there), so pads sit where they are on the real board.
    Only parts and pads with a silkscreen name are labelled.
    """
    x0, y0, x1, y1 = 200, 60, 1240, 850
    s = w / (x1 - x0)
    h = (y1 - y0) * s

    def P(px, py):
        return x + (px - x0) * s, y + (py - y0) * s

    def R(v):
        return v * s

    o = [f'<g filter="url(#shadow)"><rect x="{P(212, 72)[0]:.1f}" y="{P(212, 72)[1]:.1f}" '
         f'width="{R(1018):.1f}" height="{R(708):.1f}" rx="{R(14):.1f}" fill="#1f6b3e"/></g>',
         f'<rect x="{P(212, 72)[0]:.1f}" y="{P(212, 72)[1]:.1f}" width="{R(1018):.1f}" '
         f'height="{R(708):.1f}" rx="{R(14):.1f}" fill="none" stroke="#134a2a" stroke-width="2"/>']
    silk = "#e8efe9"

    def label(px, py, t, *, size=11, anchor="middle", weight="600", up=False):
        tx, ty = P(px, py)
        t = text(tx, ty, t, size=size, colour=silk, font=MONO, weight=weight, anchor=anchor)
        o.append(f'<g transform="rotate(-90 {tx:.1f} {ty:.1f})">{t}</g>' if up else t)

    def pad(px, py, r=17, ring=True):
        cx, cy = P(px, py)
        if ring:
            o.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{R(r + 9):.1f}" fill="none" '
                     f'stroke="{silk}" stroke-width="1.5" opacity=".8"/>')
        o.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{R(r):.1f}" fill="url(#tin)" '
                 f'stroke="#7d868f" stroke-width="1"/>')

    def part(px, py, pw, ph, fill="#1b1d21", rx=3):
        cx, cy = P(px, py)
        o.append(f'<rect x="{cx:.1f}" y="{cy:.1f}" width="{R(pw):.1f}" height="{R(ph):.1f}" '
                 f'rx="{rx}" fill="{fill}" stroke="#0b0c0e" stroke-width=".8"/>')

    def jst(px, py, pw, ph, pins):
        cx, cy = P(px, py)
        o.append(f'<g filter="url(#shadow)"><rect x="{cx:.1f}" y="{cy:.1f}" width="{R(pw):.1f}" '
                 f'height="{R(ph):.1f}" rx="4" fill="#f1ede4" stroke="#b9b2a3" stroke-width="1.2"/></g>')
        for i in range(pins):
            ix = cx + R(pw) * (i + .5) / pins
            o.append(f'<rect x="{ix - R(9):.1f}" y="{cy + R(ph) * .3:.1f}" width="{R(18):.1f}" '
                     f'height="{R(ph) * .4:.1f}" rx="2" fill="#c9c2b2"/>')

    def cap(px, py, r):
        cx, cy = P(px, py)
        o.append(f'<g filter="url(#shadow)"><circle cx="{cx:.1f}" cy="{cy:.1f}" r="{R(r):.1f}" '
                 f'fill="url(#metal)" stroke="#8a939c" stroke-width="1.2"/></g>')
        o.append(f'<path d="M{cx - R(r) * .6:.1f},{cy - R(r) * .8:.1f} A{R(r):.1f},{R(r):.1f} 0 0 0 '
                 f'{cx - R(r) * .6:.1f},{cy + R(r) * .8:.1f}" fill="none" stroke="#2b2f35" '
                 f'stroke-width="{R(r) * .28:.1f}" opacity=".85"/>')
        o.append(text(cx + R(r) * .1, cy - 2, "470", size=11, colour="#374151", font=MONO,
                      weight="700", anchor="middle"))
        o.append(text(cx + R(r) * .1, cy + 11, "10V", size=10, colour="#374151", font=MONO,
                      anchor="middle"))

    # Speaker connector and its test pads, top left.
    jst(215, 30, 225, 120, 2)
    label(462, 128, "P2")
    for px, py, t in ((272, 212, "Speaker -1"), (405, 215, "Speaker +1")):
        pad(px, py, 15)
        label(px, py + 52, t, size=10)
    part(290, 290, 36, 64)
    part(345, 290, 36, 64)
    label(318, 382, "FB2  FB1", size=10)
    # The two button pads.
    for px, py, t in ((530, 152, "S1"), (1115, 172, "S2")):
        pad(px, py, 16)
        label(px + 46, py + 5, t, size=12)
    # The label area and the board marking.
    cx, cy = P(470, 240)
    o.append(f'<rect x="{cx:.1f}" y="{cy:.1f}" width="{R(128):.1f}" height="{R(120):.1f}" '
             f'fill="#dfe6e0" opacity=".9"/>')
    label(790, 330, "E324220 JS", size=10, weight="500")
    # Bulk capacitors.
    cap(300, 560, 92)
    cap(468, 598, 84)
    label(300, 680, "EC2", size=10)
    label(400, 700, "EC1", size=10)
    # Power pads and the USB test pads.
    pad(690, 497, 18)
    label(690, 455, "VCC_BAT", size=11)
    part(730, 480, 110, 62)
    label(785, 470, "D1", size=10)
    for px, t in ((868, "VCC_5V"), (915, "USB_DP1"), (965, "USB_DM1"), (1012, "GND1")):
        pad(px, 545, 15)
        label(px + 5, 510, t, size=10, anchor="start", up=True)
    pad(680, 628, 14)
    label(680, 600, "BAT_NTC", size=9)
    pad(602, 690, 14)
    label(602, 660, "VBAT+", size=9)
    # Small power parts.
    for px, py, pw, ph in ((745, 582, 60, 42), (900, 595, 60, 42), (915, 668, 60, 42), (990, 660, 36, 56)):
        part(px, py, pw, ph)
    label(940, 735, "Q1 Q2 ZD1", size=9, weight="500")
    # Antenna feed pad and keep-out.
    pad(1072, 428, 22)
    label(1072, 490, "RF", size=10)
    ax, ay = P(1150, 380)
    o.append(f'<rect x="{ax:.1f}" y="{ay:.1f}" width="{R(60):.1f}" height="{R(380):.1f}" '
             f'fill="none" stroke="{silk}" stroke-width="1.2" opacity=".6"/>')
    # Battery connector with its leads, and the USB-C port with its cover.
    jst(395, 720, 180, 115, 3)
    label(385, 770, "P1", anchor="end")
    ux, uy = P(640, 650)
    o.append(f'<g filter="url(#shadow)"><rect x="{ux:.1f}" y="{uy:.1f}" width="{R(220):.1f}" '
             f'height="{R(200):.1f}" rx="{R(24):.1f}" fill="#1b1d21"/></g>')
    o.append(text(ux + R(110), uy + R(120), "USB-C", size=11, colour="#9ca3af", font=MONO,
                  anchor="middle"))
    return "".join(o), P, h


def tag(x, y, lines, colour):
    w = max(len(s) for s in lines) * 7.4 + 30
    hh = 22 + 18 * len(lines)
    body = WIRE[colour][0]
    o = [f'<g filter="url(#shadow)"><rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{hh}" rx="10" '
         f'fill="#ffffff" stroke="{body}" stroke-width="2.5" stroke-dasharray="7 5"/></g>']
    for i, s in enumerate(lines):
        o.append(text(x + 15, y + 26 + i * 18, s, size=13, weight="700" if i == 0 else None,
                      colour=INK if i == 0 else SUB))
    return "".join(o), w, hh


def inside_kallsup():
    w, h = 1560, 1320
    esp, amp = Esp32(800, 150), Max98357(1240, 154)
    board, P, bh = kallsup_board(40, 660, 720)
    lanes = [505, 535, 565]
    gnd1 = P(1012, 545)
    s1, s2, p2 = P(530, 152), P(1115, 172), P(320, 118)
    esp_end = esp.y + esp.H + 8 * MM
    amp_end = amp.y + amp.H + 8 * MM
    g5, gg, g1 = esp.pin("5V")[0], esp.pin("GND")[0], esp.pin("1")[0]
    mg, mv = amp.pin("GND")[0], amp.pin("Vin")[0]
    sw_tag, btn_tag = (300, 572), (900, 640)
    bottom = 660 + bh + 40
    o = [text(40, 58, "Inside the KALLSUP", size=24, weight="700"),
         text(40, 84, "The same five wires as the bench test, now powered from the KALLSUP board.",
              size=14, colour=SUB),
         board]
    o += i2s(esp, amp, lanes)
    # Switched battery: wherever check 1 finds it, so both red wires end at its tag.
    o.append(wire(rounded([(sw_tag[0] + 250, sw_tag[1] + 28), (g5, sw_tag[1] + 28), (g5, esp_end)]), "red"))
    o.append(wire(rounded([(sw_tag[0], sw_tag[1] + 28), (22, sw_tag[1] + 28), (22, bottom),
                           (mv, bottom), (mv, amp_end)]), "red"))
    # Ground: from GND1 over the board to the ESP32, and along it to the amplifier.
    o.append(wire(rounded([gnd1, (gnd1[0], 620), (gg, 620), (gg, esp_end)]), "black"))
    o.append(wire(rounded([gnd1, (gnd1[0], gnd1[1] + 1), (mg, gnd1[1] + 1), (mg, amp_end)]), "black"))
    # Button: S1 or S2, whichever check 3 finds.
    o.append(wire(rounded([(g1, esp_end), (g1, btn_tag[1])]), "yellow"))
    o.append(blob(*gnd1, 10))
    o.append(esp.svg())
    o.append(amp.svg())
    for n in ("5V", "GND", "1", "2", "3", "4"):
        o.append(dupont(esp.pin(n)[0], esp.y + esp.H))
    for n in ("LRC", "BCLK", "DIN", "GND", "Vin"):
        o.append(dupont(amp.pin(n)[0], amp.y + amp.H))
    spk = (1478, 76)
    o.append(speaker(*spk, 52))
    (mx, my), (px, py) = amp.screw("-"), amp.screw("+")
    o += [wire(rounded([(spk[0] - 40, spk[1] + 20), (mx, spk[1] + 20), (mx, my)], r=24), "black", 6),
          wire(rounded([(spk[0] - 30, spk[1] + 36), (spk[0] - 30, spk[1] + 60), (px, spk[1] + 60), (px, py)], r=18), "red", 6),
          blob(mx, my, 7), blob(px, py, 7)]
    t, tw, th = tag(*btn_tag, ["Button pad: S1 or S2", "whichever check 3 finds"], "yellow")
    o.append(t)
    for target in (s1, s2):
        o.append(f'<path d="M{btn_tag[0]:.1f},{btn_tag[1] + 30:.1f} L{target[0]:.1f},{target[1]:.1f}" '
                 f'stroke="{WIRE["yellow"][0]}" stroke-width="2.5" stroke-dasharray="6 5" fill="none"/>')
        o.append(f'<circle cx="{target[0]:.1f}" cy="{target[1]:.1f}" r="16" fill="none" '
                 f'stroke="{WIRE["yellow"][0]}" stroke-width="3.5"/>')
    t, tw, th = tag(*sw_tag, ["Switched battery point", "on this board, found by check 1"], "red")
    o.append(t)
    o.append(f'<circle cx="{p2[0]:.1f}" cy="{p2[1]:.1f}" r="44" fill="none" stroke="#2f6fe0" stroke-width="3.5"/>')
    o.append(pill(p2[0] + 20, p2[1] - 88, "P2: leave empty", "blue"))
    o.append(pill(gnd1[0] - 50, gnd1[1] + 38, "GND1", "black"))
    o += [pill(1120, lanes[0], "GP4 → LRC", "purple"), pill(1150, lanes[1], "GP3 → BCLK", "blue"),
          pill(1180, lanes[2], "GP2 → DIN", "green")]
    o += [caption(esp.x, esp.y - 50, "ESP32-S3-Zero", "top view, USB-C to the left"),
          caption(amp.x, amp.y - 18, "MAX98357A"),
          caption(spk[0] - 150, 40, "Stock speaker", "moved off P2"),
          caption(800, 1140, "KALLSUP board, back", "pads named as on its silkscreen")]
    steps = [("1", "Speaker", "off P2, red to +, black to −"),
             ("2", "GND1", "to the ESP32 GND and the MAX98357A GND"),
             ("3", "Switched point", "to the ESP32 5V and the MAX98357A Vin"),
             ("4", "Button pad", "to the ESP32 GP1"),
             ("5", "Audio", "GP2, 3, 4 to DIN, BCLK, LRC, as on the bench")]
    for i, (n, head, rest) in enumerate(steps):
        yy = 150 + i * 62
        o.append(f'<circle cx="58" cy="{yy - 5}" r="15" fill="{INK}"/>')
        o.append(text(58, yy, n, size=14, colour="#ffffff", weight="700", anchor="middle"))
        o.append(text(84, yy - 4, head, size=15, weight="700"))
        o.append(text(84, yy + 15, rest, size=13, colour=SUB))
    o.append(text(40, 480, "Do checks 1 and 3 before soldering the joints that depend on them.",
                  size=13, colour=WIRE["red"][1], weight="600"))
    o.append(text(40, h - 24, "Illustration. The two tagged joints are not drawn on a pad because "
                  "the checks decide where they go.", size=12, colour=SUB))
    return svg_doc(w, h, "Mockup of the build inside the KALLSUP: on the back of the KALLSUP board, "
                   "GND1 is wired to the ESP32 GND and the MAX98357A GND; the ESP32 5V and the "
                   "MAX98357A Vin go to the switched battery point that check 1 finds; GP1 goes to "
                   "S1 or S2, whichever check 3 finds; GP2, 3 and 4 go to DIN, BCLK and LRC; the stock "
                   "speaker moves from P2 to the MAX98357A terminal.", o)


def solder_a_pad():
    w, h = 1400, 470
    o = [text(40, 52, "Soldering a wire to a test pad", size=24, weight="700"),
         text(40, 78, "The same four moves for GND1, the switched point and the button pad.",
              size=14, colour=SUB)]
    panels = [("1", "Tin the pad", "Iron on the pad, feed a little", "solder until it is shiny."),
              ("2", "Strip and tin the wire", "Strip about 2 mm, twist the", "strands, coat them in solder."),
              ("3", "Join", "Lay the wire on the pad, touch", "the iron for 1–2 s. No extra solder."),
              ("4", "Check and tape it", "A smooth, shiny cone. Tape the", "wire down near the joint.")]
    pw, gap, top = 316, 22, 104
    for i, (n, head, l1, l2) in enumerate(panels):
        x = 40 + i * (pw + gap)
        o.append(f'<clipPath id="p{n}"><rect x="{x}" y="{top}" width="{pw}" height="250" rx="16"/></clipPath>')
        o.append(f'<g filter="url(#shadow)"><rect x="{x}" y="{top}" width="{pw}" height="250" rx="16" '
                 f'fill="#1f6b3e"/></g><g clip-path="url(#p{n})">')
        o.append(f'<rect x="{x}" y="{top}" width="{pw}" height="250" rx="16" fill="none" '
                 f'stroke="#134a2a" stroke-width="2"/>')
        # A trace running into the pad, as on the KALLSUP board.
        o.append(f'<path d="M{x + 30},{top + 210} L{x + 110},{top + 210} L{x + 150},{top + 170}" '
                 f'stroke="#2a8350" stroke-width="10" fill="none" stroke-linecap="round"/>')
        cx, cy = x + 160, top + 150
        o.append(f'<circle cx="{cx}" cy="{cy}" r="40" fill="none" stroke="#e8efe9" stroke-width="3" opacity=".85"/>')
        o.append(f'<circle cx="{cx}" cy="{cy}" r="27" fill="url(#tin)" stroke="#7d868f" stroke-width="1.5"/>')
        if n == "1":
            o.append(iron(cx + 8, cy - 8))
            o.append(f'<path d="M{cx - 120},{cy - 90} C{cx - 70},{cy - 90} {cx - 40},{cy - 40} {cx - 14},{cy - 6}" '
                     f'stroke="#c3c9cf" stroke-width="5" fill="none" stroke-linecap="round"/>')
        elif n == "2":
            o.append(stripped_wire(x + 40, cy - 60, tinned=True))
        elif n == "3":
            o.append(stripped_wire(cx - 170, cy, tinned=True, laid=True))
            o.append(iron(cx + 14, cy - 12))
        else:
            o.append(stripped_wire(cx - 170, cy, tinned=True, laid=True))
            o.append(f'<ellipse cx="{cx - 2}" cy="{cy}" rx="24" ry="20" fill="url(#tin)" stroke="#7d868f"/>')
            o.append(f'<rect x="{cx - 132}" y="{cy - 22}" width="46" height="44" rx="4" fill="#f59e0b" opacity=".55"/>')
            o.append(text(cx - 109, cy + 40, "Kapton", size=11, colour="#fde68a", anchor="middle"))
        o.append('</g>')
        o.append(f'<circle cx="{x + 24}" cy="{top + 26}" r="14" fill="#ffffff"/>')
        o.append(text(x + 24, top + 31, n, size=14, colour=INK, weight="700", anchor="middle"))
        o.append(text(x, top + 282, head, size=16, weight="700"))
        o.append(text(x, top + 304, l1, size=13, colour=SUB))
        o.append(text(x, top + 322, l2, size=13, colour=SUB))
    o.append(text(40, h - 20, "Illustration. Around 330 °C with leaded solder; keep the iron off "
                  "chip pins.", size=12, colour=SUB))
    return svg_doc(w, h, "Four close-ups of soldering a wire to a test pad: tin the pad, strip and tin "
                   "the wire, lay it on the pad and touch the iron for one to two seconds, then check "
                   "for a smooth shiny joint and tape the wire down.", o)


def iron(tx, ty):
    """A soldering-iron tip coming in from the upper right, its point at (tx, ty)."""
    return (f'<g filter="url(#shadow)"><path d="M{tx},{ty} L{tx + 70},{ty - 58} L{tx + 84},{ty - 42} Z" '
            f'fill="url(#iron)" stroke="#4b5563"/>'
            f'<path d="M{tx + 70},{ty - 58} L{tx + 124},{ty - 104} L{tx + 142},{ty - 84} L{tx + 84},{ty - 42} Z" '
            f'fill="#9ca3af" stroke="#4b5563"/>'
            f'<path d="M{tx + 124},{ty - 104} L{tx + 150},{ty - 128} L{tx + 170},{ty - 104} L{tx + 142},{ty - 84} Z" '
            f'fill="#1f2937"/></g>')


def stripped_wire(x, y, *, tinned=False, laid=False):
    """Red silicone wire with its end stripped; laid on the pad or held above it."""
    length = 120 if laid else 150
    body, edge = WIRE["red"]
    end = x + length
    core = "url(#tin)" if tinned else "url(#copper)"
    return (f'<rect x="{x}" y="{y - 9}" width="{length}" height="18" rx="9" fill="{body}" stroke="{edge}" stroke-width="2"/>'
            f'<rect x="{x + 6}" y="{y - 6}" width="{length - 12}" height="4" rx="2" fill="#ffffff" opacity=".3"/>'
            f'<rect x="{end - 4}" y="{y - 5.5}" width="34" height="11" rx="5" fill="{core}" stroke="#7d868f"/>')


PICTURES = {"bench-test": bench_test, "inside-kallsup": inside_kallsup, "solder-a-pad": solder_a_pad}


def main() -> int:
    check = "--check" in sys.argv[1:]
    OUT.mkdir(parents=True, exist_ok=True)
    stale = []
    for name, fn in PICTURES.items():
        path = OUT / f"{name}.svg"
        svg = fn()
        if check:
            if not path.exists() or path.read_text(encoding="utf-8") != svg:
                stale.append(path.relative_to(ROOT))
        else:
            path.write_text(svg, encoding="utf-8")
    if check:
        if stale:
            print("stale, run python3 tools/gen_mockups.py:", *stale, sep="\n  ")
            return 1
        print("mockups up to date")
        return 0
    print(f"{len(PICTURES)} mockups -> docs/assets/mockups/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
