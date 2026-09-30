# 🧭 Alternatives

This build gives up Bluetooth to keep the soldering simple. These are the routes that were worked out along the way, for anyone who wants a different trade.

| Option | Keeps | Loses | Solder on the KALLSUP board | Extra parts |
|---|---|---|---|---|
| **A. PCM5102 into the stock amplifier** | Bluetooth, battery, buttons, stock amplifier | Nothing | 3, one of them a small 0603 pad | PCM5102 DAC, a resistor and a capacitor |
| **B. Relays switch the speaker** | Bluetooth, battery, buttons | Playing both at once | 2 large pads plus the speaker pads | Two 3 V relays, cables |
| **C. This repository** | Battery, charging, buttons | Bluetooth | 3 large pads | Optional TPS63020 |
| **D. USB-powered only** | Case and speaker | Bluetooth, battery playback | 2 large pads (`VCC_5V`, `GND1`) | None |

## A. PCM5102 into the stock amplifier

The ESP32-S3 has no analogue output, so a DAC turns its I2S into line-level audio, which is fed into the ANT8817S's input alongside the JL7016C8's. The amplifier's input then acts as a mixer: Bluetooth and Wi-Fi both play, and nothing needs switching.

What it needs first:

1. **Find the input pins.** With the board unpowered and `P2` empty, probe the inner pads of C11, C19, R23 and R25 against pins 1 to 4. The datasheet says the input is differential, and the two matched pairs fit that.
2. **Inject through the existing coupling capacitor.** A series resistor from the PCM5102's left output to the amplifier-side pad of R23 or R25; leave the other input as it is.
3. **Attenuate.** The PCM5102 puts out about 2.1 V RMS, far hotter than the JL7016C8's drive. Start at 10% volume and add a divider or cap the software volume until the ALC just starts to act.
4. **Check CTRL.** If the amplifier mutes when the JL7016C8 idles, the ESP32 has to hold `CTRL` on, through a diode so the two do not fight, at the same voltage the JL7016C8 uses.

The only fiddly part is one wire on a 0603 pad, about 0.8 mm.

## B. Relays switch the speaker

A MAX98357A drives the speaker for Wi-Fi, the stock amplifier drives it for Bluetooth, and relays choose between them. Both amplifiers are bridge-tied, so **both** speaker wires must switch: two single-pole relays on one ESP32 pin, or one double-pole relay.

- Stock `P2` to the normally-closed contacts, so with the ESP32 off the speaker behaves as stock.
- MAX98357A to the normally-open contacts.
- Speaker to the common contacts.

The relays need 3 V coils to work from the battery, and they click when they switch.

## D. USB-powered only

The simplest build: the ESP32 and MAX98357A take `VCC_5V` and `GND1`, and play whenever USB is connected. The only check is `VCC_5V` reading about 5 V with USB in. It also sidesteps the auto-off question, because the 5 V rail comes straight from USB.

## Things that looked like shortcuts

| | Idea | Why not |
|---|---|---|
| ❌ | MAX98357A into the ANT8817S input | Its output is a switching speaker signal, not line level |
| ❌ | Both amplifiers on the speaker, no relay | Two bridge-tied outputs fighting each other |
| ❌ | LM2596 to make 3.3 V from the cell | Needs 1.5–2 V more input than output |
| ❌ | ESP32 audio straight into the amplifier | No DAC on the ESP32-S3 |
