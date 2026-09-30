# 🧰 Hardware

## What is kept from the KALLSUP

| | Part | Role in this build |
|---|---|---|
| 📦 | Case, grille, feet | Unchanged |
| 🔊 | 4 Ω 3 W driver | Moved from the stock `P2` connector to the MAX98357A |
| 🔋 | 3.6 V 750 mAh Li-ion cell | Powers everything, through the stock board |
| 🔌 | USB-C port and charger | Still charges the cell |
| 🔘 | Power button | Still switches the speaker, now Wi-Fi included |
| 🔘 | Second button | Rewired to the ESP32 as play/pause, next, previous |
| 📡 | JL7016C8 and ANT8817S | Stay on the board and powered, with no speaker attached |

## What is added

### Waveshare ESP32-S3-Zero

[Product wiki](https://www.waveshare.com/wiki/ESP32-S3-Zero). The ESP32-S3FH4R2 has 2 MB of PSRAM, which is what lets Sendspin run on a board this size. The version with pre-soldered headers makes the bench test a jumper-wire job.

Facts from the Waveshare wiki that matter here:

- The `5V` castellated pad accepts **3.7–6 V** into the on-board 3.3 V regulator.
- The first flash needs **BOOT** held while the USB-C cable goes in; there is no USB-to-UART chip.
- GPIO21 drives the on-board WS2812 LED, which the firmware uses as a status light.
- Keep metal and other boards off the ceramic antenna. Inside the KALLSUP that means away from the speaker magnet.

### Adafruit I2S 3W Class D Amplifier Breakout, MAX98357A

[Product page](https://www.adafruit.com/product/3006). Takes I2S directly and drives a 4 Ω speaker. `Vin` accepts 2.5–5.5 V, so it runs straight from the cell with no regulator. From a Li-ion cell it is quieter than at 5 V; that is the price of battery operation.

The header pins and screw terminal come loose and need soldering: five of the seven pins are used.

### TPS63020 3.3 V buck-boost module, optional

A Li-ion cell runs from about 4.2 V full to about 3.0 V empty. The ESP32's `5V` pad wants at least 3.7 V, so without help the ESP32 may reset in the lower part of the charge. A buck-boost module holds 3.3 V whether its input is above or below that, and feeds the ESP32's `3V3` pin.

Try without it first. If the ESP32 resets as the battery drains, add it.

Suitable: any module that says *buck-boost* or *step up/down* with a fixed **3.3 V** output, such as a TPS63020, TPS63802 or the [Pololu S7V8F3](https://www.pololu.com/product/2122). Check the output with a multimeter before connecting it: some modules have solder-selectable outputs, and some ship with the `EN` pin needing a link to `VIN`.

## What does not work

| | Part | Why not |
|---|---|---|
| ❌ | LM2596, MP1584 or any step-down-only module | Needs its input 1.5–2 V above its output. A 3.0–4.2 V cell cannot make a stable 3.3 V through it |
| ❌ | A MAX98357A feeding the stock amplifier's input | Its output is a switching speaker signal, not line level. It would sound terrible and could damage the ANT8817S |
| ❌ | The ESP32 driving the stock amplifier directly | The ESP32-S3 has no analogue audio output. Keeping the stock amplifier needs a DAC such as a PCM5102; see [Alternatives](alternatives.md) |
| ❌ | Two amplifiers wired to the one speaker | Both outputs are bridge-tied; connecting them together damages at least one |
