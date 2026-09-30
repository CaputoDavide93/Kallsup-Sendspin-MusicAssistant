# 🔊 KALLSUP Sendspin: findings, tests and decisions

> **Archived.** Davide Caputo's working log from the teardown, kept as it was written on 30 September 2026. Its findings were merged into the docs, which are the current state and correct several points below: the ANT8817S's own datasheet describes a Class AB/D amplifier, not Class H; the bridge-tied output is inferred, not measured; the switched battery point may not be a large pad; the optional regulator is now a 5 V module on the ESP32's `5V` pad. Start from [Board notes](../../board-notes.md) and the [Build guide](../../build-guide.md).

Everything established so far in converting an IKEA KALLSUP (E2507) into a battery-powered Music Assistant (Sendspin) Wi-Fi speaker. Last updated 30 September 2026.

Each finding is marked:

- ✅ **Measured**: continuity, a reading or a validation run.
- 🔎 **Inferred**: from markings, layout, photos or the datasheet.
- 🔍 **Open**: still to be measured.

---

## 1. Goal and final decision

**Goal:** turn the KALLSUP into a Music Assistant speaker while keeping as much of the original as possible.

**Final build (decided):**

| Keep | Drop | Add |
|---|---|---|
| Case, 4 Ω 3 W speaker, battery, USB-C charging, power button, second button | Bluetooth | ESP32-S3-Zero, Adafruit MAX98357A, optional TPS63020 |

**Why Bluetooth was dropped:** keeping it needs audio injected into the stock amplifier's input (a small 0603 solder joint plus more reverse engineering) or relays to switch the speaker (extra parts, about £20). Wi-Fi is the only source that will be used, so dropping Bluetooth gives the simplest build: three joints on the KALLSUP board, all on large test pads.

---

## 2. Product identification

| | Finding | Status |
|---|---|---|
| 📦 | IKEA KALLSUP, model E2507 | ✅ |
| 🔋 | Li-ion cell 3.6 V 750 mAh | ✅ label |
| 🔌 | USB-C input 5 V 1 A | ✅ label |
| 🔊 | Driver marked 4 Ω 3 W, red and black leads | ✅ |
| 🎧 | No 3.5 mm input | ✅ |
| 🟩 | PCB front `P-SPB-A1-01-A`, `V2.0`; back `E324220 JS`, `94V-0` | ✅ |

---

## 3. Board components

| Ref | Part | Notes | Status |
|---|---|---|---|
| U2 | JieLi **JL7016C8** (marked `BP2V742PVD`) | Bluetooth audio SoC | ✅ marking |
| X1 | 24.0 MHz crystal | For U2 | ✅ marking |
| U1 | Anatek **ANT8817S** (marked `HC2611`) | Mono Class H amplifier, built-in boost, eSOP8 | ✅ marking |
| L1 | Large shielded inductor beside U1 | Boost inductor for U1 | 🔎 |
| R21 | 1 Ω (`1R00`), with C9 | Probably U1's supply filter | 🔎 |
| C10, C18 | Beside the `VCC_PVDD` pad | PVDD decoupling | 🔎 |
| C8, C11, C19, R22, R23, R24, R25 | Next to U1 pins 1–4 | Input and CTRL network | 🔎 |
| FB1, FB2 | Ferrite beads | In the + and − speaker paths | ✅ |
| C23, C32, C26 | Around FB1/FB2 | Output filter; C26 across the outputs | 🔎 |
| R26/C22, R27/C31 | Around FB1/FB2 | RC snubbers on each output | 🔎 |
| EC1, EC2 | 470 µF 10 V electrolytics | Bulk capacitance, likely boosted rail | 🔎 |
| D1 | SS34 Schottky, 3 A 40 V | Power path from USB | 🔎 |
| Q1 | `2301D` P-channel MOSFET | Power switching | 🔎 |
| Q2, Q3, ZD1 | Near the power path | Power control | 🔎 |
| R7, R8 | Beside the USB-C port | Probably USB-C CC resistors | 🔎 |
| TVS1 | Near USB | Surge protection | 🔎 |
| P1 | 3-pin battery connector | Battery, NTC (`BAT_NTC`), ground | ✅ labels; 🔎 pin order |
| P2 | 2-pin speaker connector | Upper = +, lower = − | ✅ |
| LED1 | Two-colour LED with R12/R15/R17 | Status light | ✅ |
| S1, S2 | Tactile buttons, with test pads on the back | Which one is power is 🔍 | ✅ |

---

## 4. Test pads

| Pad | Side | What it is | Status |
|---|---|---|---|
| `GND1` | Back | Ground | ✅ beeps to USB-C shell |
| `VCC_5V` | Back | USB 5 V | 🔎 |
| `USB_DP1`, `USB_DM1` | Back | USB data | 🔎 |
| `VCC_BAT` | Back | Battery | 🔎 |
| `BAT_NTC` | Back | Battery thermistor | 🔎 |
| `Speaker +1`, `Speaker -1` | Back | Amplifier output | ✅ |
| `S1`, `S2` | Back | Button pads | ✅ labels; behaviour 🔍 |
| `RF` | Back | Antenna feed point | 🔎 |
| `VCC_PVDD` | Front | U1 output-stage supply, pin 7 | ✅ continuity; 🔎 role |
| `IOVDD` | Front | JL7016C8 I/O supply | 🔎 |
| `GND` | Front | Ground by the USB-C port | 🔎 |

Correction made during the project: the pad earlier noted as `VCC_PW00` is silkscreened **`VCC_PVDD`**.

---

## 5. Continuity tests (all done unpowered)

**Setup:** AstroAI-style digital multimeter, black probe in `COM`, red in `VΩmA`, continuity (beep) mode, verified by shorting the probes. USB-C and battery disconnected for every test.

| # | Test | Result | Conclusion |
|---|---|---|---|
| 1 | `GND1` ↔ USB-C shell | Beep | `GND1` is ground ✅ |
| 2 | `Speaker +1` ↔ upper `P2` contact | Beep | Upper `P2` = speaker + ✅ |
| 3 | `Speaker -1` ↔ lower `P2` contact | Beep | Lower `P2` = speaker − ✅ |
| 4 | `Speaker +1` ↔ both ends of FB1 | Beep | FB1 is in the + path ✅ |
| 5 | `Speaker +1` ↔ FB2 | No beep | |
| 6 | `Speaker -1` ↔ both ends of FB2 | Beep | FB2 is in the − path ✅ |
| 7 | `Speaker -1` ↔ FB1 | No beep | |
| 8 | `VCC_PVDD` ↔ U1 top row, 2nd from left (pin 7) | Beep | Pin 7 is PVDD ✅ |
| 9 | FB1 → U1 bottom pin 1, FB2 → U1 bottom pin 2 | Reported beep | ⚠️ Conflicts with layout, see §6 |
| 10 | U1 bottom pin 2 ↔ top end of R22 | Beep | ⚠️ See §6 |
| 11 | U1 bottom pin 2 ↔ lower end of R22 | No beep | |
| 12 | Either end of R22 ↔ `GND1` | Resistance, no beep | R22 is not a ground link |
| 13 | Lower end of R22 ↔ C11, C19, R23 | No beep | |

**Key consequence:** the speaker output is **bridge-tied (BTL)**. `Speaker -` is not ground. Never connect either speaker wire to ground, and never connect two amplifiers to the speaker at the same time.

---

## 6. ANT8817S amplifier

### Datasheet (Chinese only)

Sources: the manufacturer's product manual V1.0.3 attached to a [21ic forum post](https://bbs.21ic.com/icview-3050260-1-1.html), and distributor listings that reproduce it ([dzsc](https://product.dzsc.com/product/785710-202112214757633.html), sandtech, bilibili). No English datasheet or official pinout was found.

| | Fact |
|---|---|
| 🔊 | 3.5 W into 4 Ω at 3.7 V and 1% THD, mono |
| ⚡ | Synchronous adaptive boost, multiple supply rails (Class H), up to 80% efficiency |
| 🎚️ | ALC anti-clipping: detects distortion and lowers gain |
| 🔀 | `CTRL` pin: its voltage selects the mode and switches ALC on or off |
| 🎛️ | Fully differential input |
| 🔋 | 3–5 V single supply |
| 🛡️ | Over-current, over-temperature, short-circuit protection; pop suppression |
| 📦 | eSOP8 (exposed pad underneath) |
| 🔁 | Listed as a drop-in replacement for the ANT8815S |

### Pin numbering

With the `ANT8817S` text upright, the **pin 1 dot is bottom-left** (from the teardown photos). Standard SOP numbering applies:

| Physical position | Pin |
|---|---|
| Bottom row, left to right | 1, 2, 3, 4 |
| Top row, right to left | 5, 6, 7, 8 |

### Pin findings

| Pin | Finding | Status |
|---|---|---|
| 7 | `VCC_PVDD` | ✅ |
| 1–4 | Face the input network; the matched pairs C11/C19 and R23/R25 fit the differential input | 🔎 |
| 5, 6, 8 | Face L1 and the output side; boost switch and outputs likely here | 🔎 |
| Exposed pad | Probably the main ground | 🔎 |

### Unresolved conflict 🔍

Tests 9 and 10 put the outputs (FB1, FB2) and R22 on bottom pins 1 and 2. The layout suggests the outputs are on the **top** row and the inputs on the bottom. A likely cause is that the speaker was still plugged into `P2`, joining both outputs through its 4 Ω coil. **Not needed for the chosen build**, but re-measure with `P2` empty before using any Bluetooth-keeping route.

---

## 7. Parts

### Bought

| Part | Price | Used in final build |
|---|---|---|
| Waveshare ESP32-S3-Zero, pre-soldered headers | £6.30 | ✅ |
| 2× Adafruit MAX98357A I2S 3 W Class D amplifier | £11.40 | ✅ one; one spare |
| Adafruit PCM5102 I2S DAC, line out | £4.80 | ❌ Only for the Bluetooth-keeping route |

### Considered

| Part | Verdict | Why |
|---|---|---|
| TPS63020 3.3 V buck-boost module (e.g. Youmile XL63020, Amazon) | ✅ Suitable, optional | Holds 3.3 V as the battery drains from 4.2 V to 3.0 V |
| Pololu S7V8F3 | ✅ Suitable | Same job; unavailable on Amazon UK, about £9 at RobotShop UK |
| LM2596 step-down boards (already owned) | ❌ Not suitable | Need input 1.5–2 V above output; a Li-ion cell cannot make 3.3 V through them |
| MAX98357A into the stock amplifier's input | ❌ | Its output is a speaker-level switching signal, not line level |
| ESP32 directly into the stock amplifier | ❌ | The ESP32-S3 has no analogue audio output |

### Relevant specs

| Part | Spec | Source |
|---|---|---|
| ESP32-S3-Zero | ESP32-S3FH4R2, 2 MB PSRAM; `5V` pad accepts 3.7–6 V; BOOT held for first flash; GPIO21 = WS2812 LED; keep the antenna clear of metal | Waveshare wiki |
| MAX98357A | `Vin` 2.5–5.5 V; `GAIN` open = 9 dB, to GND = 12 dB, 100 kΩ to GND = 15 dB | Adafruit, SendspinZero |

---

## 8. Final wiring

| From | To | Status |
|---|---|---|
| Switched battery point | MAX98357A `Vin` | 🔍 point not yet found |
| Switched battery point | ESP32 `5V` (or TPS63020 `VIN`, its `OUT` → ESP32 `3V3`) | 🔍 |
| `GND1` | ESP32 `GND`, MAX98357A `GND`, TPS63020 `GND` | ✅ pad confirmed |
| Second-button pad (`S1` or `S2`) | ESP32 `GPIO1` | 🔍 behaviour not yet measured |
| ESP32 `GPIO2` / `GPIO3` / `GPIO4` | MAX98357A `DIN` / `BCLK` / `LRC` | ✅ from firmware |
| MAX98357A `+` / `−` | Speaker red / black (unplugged from `P2`) | ✅ |
| MAX98357A `SD`, `GAIN` | Left open | — |

**Rules:**
- Never feed the ESP32's `5V` and `3V3` at the same time.
- Do not use `VCC_BAT` directly unless it turns off with the speaker, or the ESP32 will drain the battery while "off".
- Do not plug the ESP32's own USB-C in while it is battery-powered; flash on the bench, then update over the air.

**Soldering budget:** 3 joints on the KALLSUP board (large pads), 5 pins + terminal on the MAX98357A, 4 pads on the TPS63020 if used.

---

## 9. Firmware

**Base:** [SendspinZero](https://github.com/RealDeco/SendspinZero) `SendspinZero-Speaker.yaml` by RealDeco (MIT), used as an ESPHome remote package pinned to commit `0c7f82b685b78dfcc09b04564cdd68ee0a222fd5`.

**Added on top:**

| Addition | Detail |
|---|---|
| Name | `kallsup-sendspin` / `KALLSUP Sendspin` |
| API | Encrypted with `api_encryption_key` |
| OTA | `encryption: {}`: uploads require the API key |
| Wi-Fi | SSID and password from `secrets.yaml` |
| Fallback hotspot | Protected by `fallback_password` |
| Button | `GPIO1`, pull-up, inverted, 20 ms debounce: single = play/pause, double = next, triple = previous |

SendspinZero on its own leaves the API, OTA and fallback hotspot open.

### Validation ✅

| Test | Result |
|---|---|
| `esphome config firmware/kallsup-sendspin.yaml` on ESPHome 2026.9.1 | **Configuration is valid** |
| Name substitution applied | ✅ |
| API encryption, OTA encryption, Wi-Fi and hotspot password merged | ✅ |
| Warning: GPIO3 is a strapping pin | Expected; SendspinZero's BCLK pin; MAX98357A `BCLK` is an input |
| Warning: merged multiple OTA configurations | Expected; the key requirement merges into SendspinZero's OTA entry |
| First attempt with an OTA password | Valid, but ESPHome recommended `encryption` instead; switched |

### Entities exposed

Sendspin Group Media Player, Media Player, Song Title, Song Artist, Album Name, Startup sound, Restart, LED light (from SendspinZero), Button (added). LED: red idle, green playing.

---

## 10. Tests still to do 🔍

All with the multimeter. Continuity: unpowered. Voltage: DC volts, black probe on `GND1`, touch test pads or passive-part ends only, never chip pins.

| # | Test | How | Pass condition | If it fails |
|---|---|---|---|---|
| 1 | **Find the switched battery point** | Battery only; measure `VCC_BAT`, the non-U1 end of R21 and other power-side points with the speaker off, then on | ~3.6–4.2 V on, ~0 V off | Open question; do not use `VCC_BAT` |
| 2 | **Auto-off on battery** | Battery only, switch on, no Bluetooth, wait 30–60 min | Stays on | Use the USB-only option, or find a keep-awake method |
| 3a | **Which pad is the second button** | Unpowered, continuity from `S1`/`S2` back pads to each button's legs | Identified | — |
| 3b | **Button pad behaviour** | Powered; measure `IOVDD`, then the pad idle and pressed | `IOVDD` ~3.3 V; pad ~3.3 V idle, ~0 V pressed | Pulls high → firmware `INPUT_PULLDOWN`, `inverted: false`; ladder or `IOVDD` > 3.6 V → do not wire |
| 4 | **TPS63020 output** (if used) | Power it, measure `OUT` | ~3.3 V | 0 V → link `EN` to `VIN`; wrong voltage → check the 3V3/4V2/5V pads |
| 5 | **Bench test** | ESP32 + MAX98357A + any speaker on USB; play from Music Assistant | Sound, LED green | See §12 |
| 6 | **First power-up in the case** | Switch on, play quietly, press button, switch off, charge | All work; ESP32 goes dark when off | See §12 |
| 7 | **Low-battery stability** | Play until the battery is low | No resets | Add the TPS63020 |
| 8 | **Battery runtime** | Play from full to cut-off | Recorded | — |

Not needed for the chosen build, only for Bluetooth-keeping routes: re-measure the U1 output pins with `P2` empty (§6), find the input pins, trace and measure `CTRL`.

---

## 11. Routes considered

| Option | Keeps | Loses | KALLSUP joints | Extra parts | Status |
|---|---|---|---|---|---|
| A. PCM5102 into the stock amplifier (mixer) | Everything | Nothing | 3, one on a 0603 pad | Resistor, capacitor | Documented, not chosen |
| B. Relays switch the speaker between amplifiers | BT, battery, buttons | Simultaneous play | 2 large + speaker pads | 2× 3 V relays, cables | Documented, not chosen |
| **C. MAX98357A on switched battery** | **Battery, charging, buttons** | **Bluetooth** | **3 large pads** | **Optional TPS63020** | **Chosen** |
| D. USB-powered only | Case, speaker | BT, battery playback | 2 (`VCC_5V`, `GND1`) | None | Fallback if test 2 fails |

Notes for option A: the PCM5102 outputs ~2.1 V RMS, far hotter than the JL7016C8, so it needs attenuation; the amplifier may mute when the JL7016C8 idles, requiring the ESP32 to hold `CTRL` through a diode at the JL7016C8's voltage.

---

## 12. Troubleshooting reference

| Symptom | Likely cause | Fix |
|---|---|---|
| LED red while "playing" | Stream not arriving | Check Wi-Fi and Home Assistant logs |
| LED green, no sound | I2S wires swapped, no `Vin`, speaker loose | Recheck `GPIO2→DIN`, `GPIO3→BCLK`, `GPIO4→LRC` |
| ESP32 resets on low battery | `5V` pad below 3.7 V | Add TPS63020 to `3V3` |
| Speaker turns itself off | Stock auto-off | Test 2; USB-only option |
| Battery drains when off | ESP32 on an unswitched point | Move to the switched point |
| Button does nothing | Pad does not pull to ground | Redo test 3b, adjust firmware |
| Hum or crackle | Ground loops, long I2S wires | All grounds to `GND1`, short wires |
| Weak Wi-Fi | Antenna near magnet or metal | Reposition the ESP32 |
| Won't flash | BOOT not held, charge-only cable | Hold BOOT while plugging in |

---

## 13. Repository

[`CaputoDavide93/Kallsup-Sendspin-MusicAssistant`](https://github.com/CaputoDavide93/Kallsup-Sendspin-MusicAssistant), built to the house standards: README, firmware, seven docs, light/dark diagrams from `tools/gen_diagram.py`, icon from `tools/gen_brand.py`, CI (ESPHome validation and diagram check), teardown photos resized and stripped of metadata. Status: prepared, not yet pushed.

---

## 14. Next steps

1. Push the repository.
2. Bench test: flash the firmware, play through the MAX98357A.
3. Tests 1, 2, 3a, 3b on the KALLSUP board.
4. Solder the three joints and the speaker; first power-up.
5. Run tests 7 and 8, and add the TPS63020 if needed.
6. Update the 🔍 items in the repository with the results.
