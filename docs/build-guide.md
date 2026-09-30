# 🧭 Build guide

Bench test, measure, then solder. Each stage catches a problem while it is still cheap to fix.

## 1. Bench test

Before the KALLSUP is opened, prove the new parts work on the desk.

1. Solder the header pins (or five wires) onto the MAX98357A, and its screw terminal.
2. Connect the ESP32 and the MAX98357A with jumper wires: `5V` to `Vin`, `GND` to `GND`, `GPIO2` to `DIN`, `GPIO3` to `BCLK`, `GPIO4` to `LRC`.
3. Connect any small 4–8 Ω speaker to the terminal.
4. Flash the firmware and adopt it in Home Assistant: [Firmware](firmware.md).
5. Play something from Music Assistant. The ESP32's LED turns green while it plays.

Powered from the ESP32's USB-C on the bench, the whole thing is safe to rewire.

## Before you solder

Three checks on the KALLSUP board, all with the multimeter, about fifteen minutes. They settle the three 🔍 items; nothing gets soldered until they are done.

For continuity: battery unplugged, USB unplugged, meter on the beep range. For voltage: meter on DC volts, black probe on `GND1`, and touch only test pads or the ends of passive parts, never the pins of a chip.

### Check 1: find the switched battery point 🔍

On battery only, no USB. Measure each candidate with the speaker **off**, then **on**:

| Point | Speaker off | Speaker on |
|---|---|---|
| `VCC_BAT` | | |
| End of `R21` away from `U1` | | |
| Other test pads or capacitor ends near the power circuit | | |

The point to use reads battery voltage (about 3.6–4.2 V) when on and about 0 V when off. `VCC_BAT` probably reads the cell in both states; do not use it, or the ESP32 drains the battery while the speaker looks off.

If nothing switches, the speaker's power button probably switches only the stock chips' logic. Open an issue with your readings before improvising.

### Check 2: does it switch itself off on battery? 🔍

On battery only, switch the speaker on, connect nothing over Bluetooth, and time how long it stays on. Leave it at least 30 minutes.

If it switches itself off, the switched rail goes with it and the ESP32 loses power mid-song. That is solvable, but it changes the design; open an issue with how long it lasted. Running from the stock USB-C (Option D in [Alternatives](alternatives.md)) avoids it entirely.

### Check 3: the second button's pad 🔍

1. Unpowered, with continuity, find which of the back-side pads `S1` and `S2` connects to the second button (not the power button).
2. Powered and on, measure `IOVDD`, then that pad idle and with the button held.

| Reading | Meaning | What to do |
|---|---|---|
| `IOVDD` about 3.3 V; pad about 3.3 V idle, about 0 V pressed | Pulls to ground | Wire it to `GPIO1`; the firmware already expects this |
| Pad about 0 V idle, high when pressed | Pulls high | In the firmware set `mode: INPUT_PULLDOWN` and `inverted: false` |
| Several different voltages across buttons | A resistor ladder read by an ADC | Do not wire it; open an issue with the readings |
| `IOVDD` above 3.6 V | Higher logic than the ESP32 tolerates | Do not wire it directly |

## 2. Solder

1. **Speaker**: unplug it from `P2` and connect it to the MAX98357A terminal, red to `+`, black to `−`. See [Wiring](wiring.md#speaker).
2. **Power**: from the switched point found in check 1, one wire to MAX98357A `Vin` and one to the ESP32 `5V` pad (or to the TPS63020 `VIN`, with its `OUT` to the ESP32 `3V3`).
3. **Ground**: from `GND1` to every `GND`.
4. **Button**: from the pad found in check 3 to `GPIO1`.
5. **Audio**: `GPIO2`, `GPIO3`, `GPIO4` to `DIN`, `BCLK`, `LRC`, as on the bench.

Tin each pad and each wire first, then touch them together for a second. Tape or glue every wire down near its joint; a tugged wire lifts a pad.

## 3. First power-up

1. Switch on. The ESP32's LED lights red, then Home Assistant shows it online.
2. Play from Music Assistant, quietly first.
3. Press the second button once: playback pauses.
4. Switch off. The ESP32 should go dark with everything else.
5. Plug in USB-C and confirm it still charges.

## 4. Assemble

- Insulate every bare joint and the backs of the small boards with Kapton tape or heat-shrink.
- Mount the boards with foam tape or a small printed carrier so they cannot rattle.
- Keep the ESP32's ceramic antenna away from the speaker magnet and the metal grille.
- Route wires away from the screw posts before closing the case.
