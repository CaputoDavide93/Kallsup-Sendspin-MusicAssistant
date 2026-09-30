# 🔬 KALLSUP board notes

What is on the KALLSUP E2507's board, from one teardown. Each finding is marked:

- ✅ **Measured**: continuity or a reading on this board.
- 🔎 **Inferred**: from markings, layout or the datasheet, not measured.
- 🔍 **Open**: not known yet.

The build in this repository only relies on ✅ findings and the three 🔍 checks in the [Build guide](build-guide.md#before-you-solder). The amplifier details matter only for the Bluetooth-keeping routes in [Alternatives](alternatives.md).

## Identification

| | Finding | Status |
|---|---|---|
| 📦 | IKEA KALLSUP, model E2507 | ✅ |
| 🔋 | Li-ion cell, 3.6 V 750 mAh, on 3-pin connector `P1` (battery, NTC, ground) | ✅ label; 🔎 pin order |
| 🔌 | USB-C input, 5 V 1 A | ✅ label |
| 🔊 | Driver marked 4 Ω 3 W, red and black leads, on 2-pin connector `P2` | ✅ |
| 🟩 | PCB marked `P-SPB-A1-01-A` and `V2.0` on the front, `E324220 JS` and `94V-0` on the back | ✅ |
| 🎧 | No 3.5 mm input | ✅ |

## Main parts

| Ref | Part | Notes | Status |
|---|---|---|---|
| U2 | JieLi **JL7016C8** (second marking line `BP2V742PVD`) | Bluetooth audio SoC | ✅ marking |
| X1 | 24.0 MHz crystal | U2's clock | ✅ marking |
| U1 | Anatek **ANT8817S** (second marking line `HC2611`) | Mono Class D amplifier (with a Class AB mode) and a built-in adaptive boost, eSOP8 | ✅ marking |
| L1 | Shielded power inductor next to U1 | The amplifier's boost inductor, beside pin 8 (`SW`); the datasheet uses 6.8 µH, 3 A | 🔎 |
| R21 | 1 Ω (`1R00`) with C9 | Probably the datasheet's 1 Ω + 2.2 nF snubber on the `SW` switch node, not a supply filter. At DC both ends sit at the amplifier's supply voltage | 🔎 |
| C10, C18 | Next to the `VCC_PVDD` pad | Decoupling on the output-stage supply | 🔎 |
| C8, C11, C19, R22, R23, R24, R25 | Next to U1 pins 1 to 4 | The input and `CTRL` network. The matched pairs fit the datasheet's 0.22 µF + 20 kΩ on each input (C11/C19, R23/R25); R22 fits a `CTRL` divider ([test 10](#continuity-tests)) | 🔎 |
| FB1, FB2 | Ferrite beads | FB1 in the `Speaker +` leg, FB2 in the `Speaker -` leg ([tests 4 to 7](#continuity-tests)) | ✅ continuity |
| C23, C32, C26 | Around FB1 and FB2 | Output filter; C26 across the two legs | 🔎 |
| R26/C22, R27/C31 | Around FB1 and FB2 | An RC snubber on each leg | 🔎 |
| EC1, EC2 | 470 µF 10 V electrolytics | The datasheet has two 470 µF: one on the battery input, one on `PVDD`, the boost output. Which is which is not measured | 🔎 |
| D1 | SS34 Schottky, 3 A 40 V | Power path from USB | 🔎 |
| Q1 | `2301D`, a P-channel MOSFET | Power switching | 🔎 |
| Q2, Q3, ZD1 | Near the power path | Power control | 🔎 |
| R7, R8 | Next to the USB-C port | Probably the USB-C CC resistors | 🔎 |
| TVS1 | Near the USB-C port | Surge protection | 🔎 |
| P1 | 3-pin battery connector | Battery, NTC (`BAT_NTC`) and ground | ✅ labels; 🔎 pin order |
| P2 | 2-pin speaker connector | Upper contact `Speaker +`, lower `Speaker -` ([tests 2 and 3](#continuity-tests)) | ✅ continuity |
| LED1 | Two-colour LED, with R12, R15 and R17 | Status | ✅ |
| S1, S2 | Tactile buttons, each with a test pad on the back | Which is power is 🔍 | ✅ |

## Test pads

| Pad | Side | What it is | Status |
|---|---|---|---|
| `GND1` | Back | Ground; beeps to the USB-C shell | ✅ |
| `VCC_5V` | Back | USB 5 V | 🔎 |
| `USB_DP1`, `USB_DM1` | Back | USB data | 🔎 |
| `VCC_BAT` | Back | Cell | 🔎 |
| `BAT_NTC` | Back | Battery thermistor | 🔎 |
| `Speaker +1`, `Speaker -1` | Back | Amplifier output, beep to the upper and lower `P2` contacts | ✅ |
| `S1`, `S2` | Back | The two buttons | ✅ labels; behaviour 🔍 |
| `RF` | Back | Antenna feed point | 🔎 |
| `VCC_PVDD` | Front | Beeps to U1 pin 7; the output-stage supply | ✅ continuity; 🔎 role |
| `IOVDD` | Front | JL7016C8 I/O supply | 🔎 |
| `GND` | Front | Ground, by the USB-C port | 🔎 |

Early notes from this teardown call the `VCC_PVDD` pad `VCC_PW00`; the silkscreen reads `VCC_PVDD`.

## Continuity tests

The measurements behind the ✅ continuity findings above, all on an unpowered board. Digital multimeter on continuity (beep), black probe in `COM`, red in `VΩmA`, checked by touching the probes together first; USB-C and battery unplugged for every test. Whether the speaker was plugged into `P2` during each test was not recorded.

| # | Probes | Result | What it shows |
|---|---|---|---|
| 1 | `GND1` ↔ USB-C shell | Beep | `GND1` is ground ✅ |
| 2 | `Speaker +1` ↔ upper `P2` contact | Beep | The upper contact is `Speaker +` ✅ |
| 3 | `Speaker -1` ↔ lower `P2` contact | Beep | The lower contact is `Speaker -` ✅ |
| 4 | `Speaker +1` ↔ both ends of FB1 | Beep | FB1 is in the `+` leg ✅ |
| 5 | `Speaker +1` ↔ FB2 | No beep | FB2 is not in the `+` leg ✅ |
| 6 | `Speaker -1` ↔ both ends of FB2 | Beep | FB2 is in the `-` leg ✅ |
| 7 | `Speaker -1` ↔ FB1 | No beep | FB1 is not in the `-` leg ✅ |
| 8 | `VCC_PVDD` ↔ U1 top row, second from left (pin 7) | Beep | `VCC_PVDD` is pin 7 ✅ |
| 9 | FB1 ↔ U1 bottom pin 1; FB2 ↔ U1 bottom pin 2 | Beep (reported) | ⚠️ Disagrees with the layout; see [Pins](#pins) 🔍 |
| 10 | U1 bottom pin 2 ↔ top end of R22 | Beep | ⚠️ See [Pins](#pins) 🔍 |
| 11 | U1 bottom pin 2 ↔ lower end of R22 | No beep | — |
| 12 | Either end of R22 ↔ `GND1` | A resistance, no beep | Neither end is tied straight to ground |
| 13 | Lower end of R22 ↔ C11, C19, R23 | No beep | — |

No test measured `Speaker -1` against `GND1`, so the bridge-tied output below stays 🔎.

## The ANT8817S

The datasheet is only published in Chinese: the **ANT8817S product manual V1.0** from Anatek (深圳市安耐科电子技术有限公司), hosted by the distributor 音芯派 ([PDF](http://www.yinxinpai.com/public/uploads/files/20220805/06e58ba51fd9a66ff64316f2a78a2c8e.pdf)). The facts below are from it. Earlier notes used the manual for the ANT8817, without the S, which calls itself Class H; this board's chip is marked `ANT8817S`, and its own manual describes a Class AB/D amplifier with an adaptive boost.

| | Datasheet fact |
|---|---|
| 🔊 | 3.5 W into 4 Ω at 3.7 V in Class D with ALC (4.3 W at 10% THD); 1.3 W in Class AB at 1% THD; mono |
| ⚡ | Synchronous adaptive boost with several supply rails, up to 80% overall efficiency (78% at 3.5 W); oscillator 350 kHz |
| 🎚️ | ALC: detects clipping and lowers the gain, so a loud track or a sagging battery does not distort |
| 🔀 | `CTRL` pin: 2.1 V to `VDD` is Class D with ALC; 1.3–1.8 V is Class AB; below 0.4 V, or floating (internal pull-down), the chip is off. The level can come from a resistor divider |
| 🎛️ | Fully differential input, usable single-ended with the same gain. Gain = 360 kΩ / (R<sub>in</sub> + 6 kΩ): about 13.8, or 22.8 dB, with the 20 kΩ input resistors |
| 🔋 | 3–5 V single supply (2.5–5.5 V in the electrical table, 5.5 V absolute maximum); 4 mA idle, 0.1 µA off |
| 🛡️ | Over-current and over-temperature protection (150 °C, 20 °C hysteresis); pop suppression at power-up and power-down |
| 📦 | eSOP8, with an exposed pad underneath |

A distributor lists the ANT8817 as a replacement for the ANT8815S; that listing is for the part without the S, so treat it as a loose cross-reference only.

### Pins

With the `ANT8817S` marking upright, the pin 1 dot is **bottom-left** 🔎 photo. Standard SOP numbering applies: bottom row 1 to 4 left to right, top row 5 to 8 right to left.

The datasheet draws the top view with pins 1 to 4 down the left side; turned so the dot is bottom-left, as on this board, the top row reads 8, 7, 6, 5 from left to right.

| Pin | Datasheet | On this board | Status |
|---|---|---|---|
| 1 | `VDD`, supply input | Faces C8 and the input network | 🔎 |
| 2 | `CTRL`, shutdown and mode | Beeps to one end of R22 ([test 10](#continuity-tests)), which fits a `CTRL` divider | 🔎 |
| 3, 4 | `INN`, `INP`, audio inputs | Face R23/R25 and C11/C19 | 🔎 |
| 5, 6 | `VON`, `VOP`, speaker outputs | Top row, right: the output side | 🔎 |
| 7 | `PVDD`, boost output | `VCC_PVDD`, top row second from left, where the datasheet puts pin 7 | ✅ continuity |
| 8 | `SW`, boost switch node | Top-left, beside L1 | 🔎 |
| 9 (exposed pad) | `PGND`, power ground | Underneath | 🔎 |

`PVDD` is the boost output, and its voltage follows the music. Never take power from `VCC_PVDD`.

Test 9 disagrees with the datasheet: it traced FB1 and FB2 to bottom pins 1 and 2, which are `VDD` and `CTRL`, while the outputs are pins 5 and 6 on the top row. Test 10, pin 2 to R22, fits the datasheet. The speaker being plugged in was suggested as the cause, but tests 5 and 7 found no beep between the two legs, which argues against it. Re-measure test 9 with `P2` empty before relying on it. 🔍

### Output

`Speaker +1` goes through ferrite bead FB1 and `Speaker -1` through FB2 ✅ (tests 4 to 7), each with its own filter capacitors and RC snubbers (R26/C22, R27/C31), with C26 across them. The output is **bridge-tied** 🔎, from the layout: each leg has its own ferrite bead and filter. Treat `Speaker -` as not ground: never tie it to ground, and never connect another amplifier to it. Measuring that `Speaker -1` does not beep to `GND1` with `P2` empty would make this ✅.

## Photos

| | |
|---|---|
| <img src="assets/photos/board-front-amplifier.jpg" width="400" alt="U1 ANT8817S with the marking upright and the pin 1 dot bottom-left, L1 to its left, R21, C9, C10, C18 and the VCC_PVDD pad."> | <img src="assets/photos/board-front-amplifier-closeup.jpg" width="300" alt="Close-up of U1 rotated, showing the input network: C8, R22, R23, R24, R25, C11 and C19."> |
| U1 with the marking upright, pin 1 bottom-left | The input network beside pins 1 to 4 |
| <img src="assets/photos/board-front-soc.jpg" width="400" alt="U2 JL7016C8 with its 24 MHz crystal, the S2 button, IOVDD pad, LED1 and the S1 button."> | <img src="assets/photos/board-back-power.jpg" width="400" alt="Back of the board near USB-C: VCC_BAT, D1, VCC_5V, USB_DP1, USB_DM1, GND1, Q1 and Q2."> |
| U2, the JL7016C8 | The power test pads by the USB-C port |
| <img src="assets/photos/board-front-buttons.jpg" width="300" alt="Front of the board: the S2 button beside the IOVDD pad, LED1, and S1 below."> | <img src="assets/photos/board-front-pvdd.jpg" width="300" alt="The S1 button and the VCC_PVDD pad with C10 and C18."> |
| S2, `IOVDD` and LED1 | S1 and `VCC_PVDD` |
| <img src="assets/photos/board-back-speaker-output.jpg" width="300" alt="The P2 speaker connector with Speaker +1 and Speaker -1 pads, FB1, FB2 and the output filter."> | <img src="assets/photos/speaker.jpg" width="300" alt="The KALLSUP driver, marked 4 ohm 3 W, with its red and black leads."> |
| `P2` and the output filter | The driver, 4 Ω 3 W |
