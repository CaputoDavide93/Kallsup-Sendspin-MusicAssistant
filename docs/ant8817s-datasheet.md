# 📄 ANT8817S datasheet, in English

An unofficial English translation of the **ANT8817S 产品手册 (product manual) V1.0** by **深圳市安耐科电子技术有限公司, Shenzhen Anatek Electronic Technology Co., Ltd. (ANATEK)**, the maker of the amplifier on the KALLSUP board.

> **Credit and copyright.** The original manual and everything in it is © ANATEK. This page is a translation made for the builders of this project, who cannot read the Chinese original; it is not endorsed by ANATEK, and this project is not affiliated with it. The repository's MIT licence does not cover this page. Where this translation and the original disagree, the original is right. The original PDF is hosted by the distributor 深圳音芯派科技 (Yinxinpai): [download it here](http://www.yinxinpai.com/public/uploads/files/20220805/06e58ba51fd9a66ff64316f2a78a2c8e.pdf). If you represent ANATEK and want this page changed or removed, open an issue.

Nine A4 pages; the body carries no date, the PDF metadata says 2022-01-04. What this project concluded from it, compared with the board, is in [Board notes](board-notes.md#the-ant8817s).

Where the original is ambiguous, a translator's note says so in *[brackets]*. Figures that are images in the original (the characteristic curves) are listed by caption only.

---

## Page header (every page)

**ANT8817S** — THD+N = 1% / 3.5 W / 3.7 V, built-in synchronous adaptive boost, anti-clipping, Class AB/D dual-mode, mono audio power amplifier.

---

## Overview

The ANT8817S is a mono audio power amplifier with synchronous adaptive boost, ultra-low EMI and very high efficiency, with an ALC (anti-clipping) function, and dual Class AB/D modes. The chip integrates a multi-rail adaptive boost stage: powered from a 3.7 V lithium battery and driving a 4 Ω load at 1% distortion, it delivers a constant 3.5 W. The ANT8817S uses an ultra-low-EMI technique, so that in Class D mode the amplifier reaches EMI performance comparable to a Class AB amplifier.

The audio CTRL pin sets the operating mode by its voltage: Class D with ALC, or Class AB. This makes the part very flexible in use.

The ALC function automatically detects output distortion and adjusts the amplifier gain dynamically. It prevents output clipping caused by an over-large input signal (music, for example) or by battery-voltage fluctuation, which noticeably improves music quality and listening comfort.

Class AB mode ensures there is no interference at all in products that include a radio. The AB/D switching function shares the IC's enable pin, which keeps the application flexible.

The ANT8817S also has built-in over-current and over-temperature protection, for reliability and stability in all operating environments.

## Features

- 3.5 W output power at 3.7 V and 1% THD+N
- Multi-rail adaptive boost
- ALC automatic gain control against clipping
- Ultra-low EMI
- Overall efficiency up to 80%
- Fully differential circuit structure, strong immunity to interference
- Suppression of pop-click noise at power-up and power-down
- Single supply, 3 V to 5 V
- Over-current and over-temperature protection
- eSOP8 package

## Applications

- Wi-Fi speakers, AI speakers
- Portable Bluetooth speakers
- Portable voice amplifiers (megaphones)
- In-car GPS, and similar

## Ordering information

| Part number | Package | Marking | Packing |
|---|---|---|---|
| ANT8817S | eSOP8 | ANT8817S | Tape and reel |

---

## Typical application circuit

*[The schematic, described in words. Values as printed.]*

- **Battery input (`VBAT`):** 1 µF and 470 µF from `VBAT` to ground. `VBAT` feeds pin 1 (`VDD`) directly.
- **Boost inductor:** 6.8 µH, rated 3 A, from `VBAT` to pin 8 (`SW`).
- **Snubber on the switch node:** 1 Ω in series with 2.2 nF, from pin 8 (`SW`) to ground.
- **Boost output (`PVDD`, pin 7):** 0.1 µF (marked 104), 22 µF (marked 226) and 470 µF, all to ground.
- **Control (`CTRL`, pin 2):** driven by an external control signal.
- **Inputs:** each input through 0.22 µF in series with 20 kΩ, to pin 3 (`INN`) and pin 4 (`INP`).
- **Outputs:** the speaker connects directly between pin 5 (`VON`) and pin 6 (`VOP`).
- **Ground:** pin 9 (`PGND`, the exposed pad) to ground.

---

## Pin assignment

eSOP8, top view. The dot marks pin 1.

```text
        ┌───────────┐
  VDD  1│ ●         │8  SW
 CTRL  2│     9     │7  PVDD
  INN  3│   PGND    │6  VOP
  INP  4│           │5  VON
        └───────────┘
```

## Pin functions

| No. | Name | Type | Description |
|---|---|---|---|
| 1 | VDD | P | Supply input |
| 2 | CTRL | I | Shutdown control and mode-select pin |
| 3 | INN | A | Audio inverting (negative) input |
| 4 | INP | A | Audio non-inverting (positive) input |
| 5 | VON | P | Audio negative output |
| 6 | VOP | P | Audio positive output |
| 7 | PVDD | P | Power supply, boost output |
| 8 | SW | P | Switch node |
| 9 | PGND | P | Power ground (exposed pad) |

*Type: P power, I digital input, A analogue.*

---

## Absolute maximum ratings

| Parameter | Min | Max | Unit | Note |
|---|---|---|---|---|
| Supply voltage `VDD` | −0.3 | 5.5 | V | |
| Ambient operating temperature | −40 | 85 | °C | |
| Operating junction temperature | −40 | 150 | °C | |
| Storage temperature | −40 | 125 | °C | |
| ESD withstand (human body model) | 2000 | | V | HBM |
| Soldering temperature | | 260 | °C | Within 15 s |

---

## Electrical characteristics

Conditions: `VDD` = 3.7 V, T<sub>A</sub> = 25 °C.

### DC parameters

| Parameter | Symbol | Conditions | Min | Typ | Max | Unit |
|---|---|---|---|---|---|---|
| Supply voltage | VDD | | 2.5 | | 5.5 | V |
| Power-down current | I<sub>SD</sub> | CTRL = 0 | | 0.1 | 5 | µA |
| Quiescent current | I<sub>DD</sub> | CTRL = 1, Vin = 0, I<sub>LOAD</sub> = 0 | | 4 | | mA |
| Oscillator frequency | F<sub>OSC</sub> | CTRL = 1, Vin = 0 | | 350 | | kHz |
| Output offset voltage | V<sub>OS</sub> | CTRL = 1, Vin = 1, I<sub>LOAD</sub> = 0 *[as printed; probably Vin = 0]* | | 7 | 20 | mV |
| Efficiency | η | P<sub>OUT</sub> = 3.5 W | | 78 | | % |

*[The supply range here is 2.5–5.5 V; the features list says 3–5 V. The table is the operating range, the feature line the recommended one.]*

### AC parameters

| Parameter | Symbol | Conditions | Typ | Unit |
|---|---|---|---|---|
| Class D output power, ALC on | P<sub>AON</sub> | R<sub>L</sub> = 3 Ω, 1 kHz, ALC mode | 4.2 | W |
| | | R<sub>L</sub> = 3 Ω, 1 kHz, THD+N = 10% | 5 | W |
| | | R<sub>L</sub> = 4 Ω, 1 kHz, ALC mode | 3.5 | W |
| | | R<sub>L</sub> = 4 Ω, 1 kHz, THD+N = 10% | 4.3 | W |
| Class AB output power | P<sub>AB</sub> | R<sub>L</sub> = 4 Ω, 1 kHz, THD+N = 1% | 1.3 | W |
| | | R<sub>L</sub> = 4 Ω, 1 kHz, THD+N = 10% | 1.6 | W |
| Total harmonic distortion plus noise | THD+N | P<sub>out</sub> = 0.1 W | 0.06 | % |
| | | P<sub>out</sub> = 1 W | 0.06 | % |
| | | P<sub>out</sub> = 2 W | 0.08 | % |
| Output noise | V<sub>N</sub> | A<sub>V</sub> = 22 dB | 85 | µV |
| Signal-to-noise ratio | SNR | A<sub>V</sub> = 22 dB, A-weighted, THD+N = 1% | 92 | dB |
| Power-supply rejection ratio | PSRR | f = 1 kHz | 70 | dB |

### CTRL control levels

| Parameter | Symbol | Min | Max | Unit |
|---|---|---|---|---|
| Shutdown threshold | V<sub>SD</sub> | | 0.4 | V |
| Class AB threshold | V<sub>ClassAB</sub> | 1.3 | 1.8 | V |
| Class D threshold | V<sub>ClassD</sub> | 2.1 | VDD | V |

### Protection

| Parameter | Symbol | Typ | Unit |
|---|---|---|---|
| Over-temperature protection threshold | OTP | 150 | °C |
| Over-temperature hysteresis | | 20 | °C |

---

## Typical characteristic curves

*[Images in the original; captions only.]*

Measured with R<sub>LOAD</sub> = 3 Ω: Output power vs. THD+N; VDD vs. output power; frequency vs. THD+N (two plots); frequency vs. gain (two plots); output power vs. efficiency; VDD vs. I<sub>DD</sub>.

Measured with R<sub>LOAD</sub> = 4 Ω: the same eight plots.

---

## CTRL enable control

The CTRL pin turns the amplifier on and off, and its level also sets Class D or Class AB mode. The level can be set with an external resistor divider. The pin has an internal pull-down resistor; left floating, the chip is off.

| CTRL level | State |
|---|---|
| High, 2.1–5.5 V | Class D, anti-clipping on (ALC on) |
| High, 1.3–1.8 V | Audio on, Class AB |
| Low, below 0.4 V | Chip off |
| Floating | Chip off |

---

## Setting the external components

### Gain

The ANT8817S input is a differential amplifier. It can be driven differentially or single-ended, with the same gain either way. The chip has a 6 kΩ input resistance built in. The gain is adjusted with the external input resistor, following:

**A<sub>V</sub> = R<sub>f</sub> / (R<sub>in</sub> + 6 kΩ)**

where R<sub>f</sub> is the internal feedback resistor, 360 kΩ, and R<sub>in</sub> is the external input resistor, which the user chooses for the gain they need.

*[With the 20 kΩ of the application circuit: 360 / 26 ≈ 13.8, about 22.8 dB, which matches the A<sub>V</sub> = 22 dB test condition.]*

### Output filter

Where EMI requirements are modest, the speaker can be connected straight to the outputs, or through a ferrite bead on each output:

- *Ferrite-bead design:* `OUTP` and `OUTN` each through a ferrite bead (1000 Ω *[impedance, typically at 100 MHz]*), with 1 nF to ground after each bead.

For systems with stricter EMI requirements, an LC filter goes in series with each output:

- *LC-filter design:* `OUTP` and `OUTN` each through 15 µH, with 2.2 µF to ground after each inductor.

---

## Single-ended input circuit

Same as the typical application circuit above. *[In the original drawing, one input's coupling capacitor goes to the signal and the other input's coupling capacitor goes to ground, which is the single-ended connection. The typical application circuit on page 2 is drawn the same way.]*

## Differential input circuit

Same components, with both inputs, each through 0.22 µF and 20 kΩ, driven by the two halves of a differential source.

---

## Package dimensions

eSOP8, millimetres.

| Symbol | Min | Nom | Max |
|---|---|---|---|
| A | — | — | 1.75 |
| A1 | 0.10 | — | 0.225 |
| A2 | 1.30 | 1.40 | 1.50 |
| A3 | 0.60 | 0.65 | 0.70 |
| b | 0.39 | — | 0.48 |
| b1 | 0.38 | 0.41 | 0.43 |
| c | 0.21 | — | 0.26 |
| c1 | 0.19 | 0.20 | 0.21 |
| D | 4.70 | 4.90 | 5.10 |
| D1 (exposed pad) | 1.90 | 2.00 | 2.20 |
| E | 5.80 | 6.00 | 6.20 |
| E1 | 3.70 | 3.90 | 4.10 |
| E2 (exposed pad) | 1.90 | 2.00 | 2.20 |
| e | | 1.27 BSC | |
| h | 0.25 | — | 0.50 |
| L | 0.50 | — | 0.80 |
| L1 | | 1.05 BSC | |
| θ | 0° | — | 8° |
