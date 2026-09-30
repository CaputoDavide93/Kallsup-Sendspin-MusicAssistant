# 🧰 Hardware

## What is kept from the KALLSUP

| | Part | Role in this build |
|---|---|---|
| 📦 | Case, grille, feet | Unchanged |
| 🔊 | 4 Ω 3 W driver | Moved from the stock `P2` connector to the MAX98357A |
| 🔋 | 3.6 V 750 mAh Li-ion cell | Powers everything, through the stock board |
| 🔌 | USB-C port and charger | Still charges the cell |
| 🔘 | Power button | Still switches the speaker, now Wi-Fi included, through the switched rail from check 1 🔍 |
| 🔘 | Second button | Rewired to the ESP32 as play/pause, next, previous, after check 3 🔍 |
| 📡 | JL7016C8 and ANT8817S | Stay on the board and powered, with no speaker attached |

## What is added

### Waveshare ESP32-S3-Zero

[Product wiki](https://www.waveshare.com/wiki/ESP32-S3-Zero). The ESP32-S3FH4R2 has 2 MB of PSRAM, which is what lets Sendspin run on a board this size. The version with pre-soldered headers makes the bench test a jumper-wire job.

Facts from the Waveshare wiki that matter here:

- The `5V` castellated pad accepts **3.7–6 V** into the on-board 3.3 V regulator, an ME6217C33 ([schematic](https://files.waveshare.com/wiki/ESP32-S3-Zero/ESP32-S3-Zero-Sch.pdf)).
- USB-C `VBUS` connects **straight to the `5V` pad**, with no diode. With the cell on `5V`, plugging in USB pushes 5 V into the cell; never do it once the board is wired in.
- The first flash needs **BOOT** held while the USB-C cable goes in; there is no USB-to-UART chip.
- GPIO21 drives the on-board WS2812 LED, which the firmware uses as a status light.
- Keep metal and other boards off the ceramic antenna. Inside the KALLSUP that means away from the speaker magnet.

### Adafruit I2S 3W Class D Amplifier Breakout, MAX98357A

[Product page](https://www.adafruit.com/product/3006). Takes I2S directly and drives a 4 Ω speaker. `Vin` accepts 2.5–5.5 V, so it runs straight from the cell with no regulator.

The "3 W" is at 5 V. From the cell, the [datasheet](https://cdn-shop.adafruit.com/product-files/3006/MAX98357A-MAX98357B.pdf)'s power-versus-supply curve for 4 Ω gives about **1.7 W at 3.7 V** and 2.25 W at 4.2 V (10% THD), or 1.35 W and 1.75 W at 1% THD. The stock ANT8817S boosts its supply and manages 3.5 W, so this build is **quieter than the stock speaker**: that is the price of battery operation without a boost stage. At full volume it draws about 0.55 A from a 3.7 V cell.

The header pins and screw terminal come loose and need soldering: five of the seven pins are used.

### A regulator for the ESP32, optional

A Li-ion cell runs from about 4.2 V full to about 3.0 V empty. Straight on the `5V` pad, the Zero's ME6217C33 keeps its 3.3 V rail while the pad has about 3.4–3.5 V at a 350 mA Wi-Fi peak (its [datasheet](https://datasheet.lcsc.com/datasheet/pdf/722f7d98b8d249d1938ed34115c5822b.pdf?productCode=C81592) gives 100 mV typical, 180 mV maximum dropout at 300 mA). Below that the rail follows the cell down, and it passes the ESP32-S3's 3.0 V minimum at about 3.1–3.2 V on the pad. These are calculated from the datasheets, not measured. ESPHome keeps ESP-IDF's default brown-out level of 2.44 V, so the chip does not reset in that band; it runs out of specification, which can look like dropped Wi-Fi or odd restarts near empty.

So the plain wiring covers most of the charge. For the whole charge, add a regulator. Two ways, and they are not equal:

| | Module | Into | Trade-off |
|---|---|---|---|
| ✅ | A **5 V** boost or buck-boost module, such as one built on a TPS61023, or a TPS63020 set to 5 V | The `5V` pad, in place of the cell | Keeps every part inside its datasheet limits: the on-board regulator always has 5 V in. Costs some efficiency, since 5 V is then dropped to 3.3 V |
| ⚠️ | A **3.3 V** buck-boost module, such as a TPS63020, TPS63802 or the [Pololu S7V8F3](https://www.pololu.com/product/2122) | The `3V3` pad | More efficient, and a common hack. But with nothing on `5V`, the ME6217C33's output then sits above its input, which its datasheet forbids ("VOUT must not exceed VIN + 0.3 V", or reverse current flows through its parasitic diode). Outside specification 🔎 |

Try without one first, and use the battery run in the build guide to see whether the end of the charge misbehaves. Check any module's output with a multimeter before connecting it: some have solder-selectable outputs, and some ship with the `EN` pin needing a link to `VIN`.

## What does not work

| | Part | Why not |
|---|---|---|
| ❌ | LM2596, MP1584 or any step-down-only module | Needs its input 1.5–2 V above its output. A 3.0–4.2 V cell cannot make a stable 3.3 V through it |
| ❌ | Powering the ESP32 from its own USB-C while it is wired to the cell | `VBUS` goes straight to the `5V` pad, so USB 5 V would go into the cell |
| ❌ | A MAX98357A feeding the stock amplifier's input | Its output is a switching speaker signal, not line level. It would sound terrible and could damage the ANT8817S |
| ❌ | The ESP32 driving the stock amplifier directly | The ESP32-S3 has no analogue audio output. Keeping the stock amplifier needs a DAC such as a PCM5102; see [Alternatives](alternatives.md) |
| ❌ | Two amplifiers wired to the one speaker | Both outputs are bridge-tied; connecting them together damages at least one |
