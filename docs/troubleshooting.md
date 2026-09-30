# 🛠️ Troubleshooting

## No sound

1. **Is it playing?** The ESP32's LED is green while playing and red when idle. Red while Music Assistant says it is playing means the stream is not arriving: check Wi-Fi and the Home Assistant logs.
2. **Green but silent?** Check the three audio wires. `GPIO2` goes to `DIN`, `GPIO3` to `BCLK`, `GPIO4` to `LRC`; swapping two is the usual mistake.
3. **Power to the amplifier?** Measure `Vin` to `GND` on the MAX98357A with the speaker on.
4. **Speaker on the terminal?** Red to `+`, black to `−`, screws tight.

## The ESP32 resets or drops Wi-Fi as the battery runs down

On the `5V` pad, the ESP32's 3.3 V rail follows the cell down below about 3.4–3.5 V, and ESPHome's default brown-out level (2.44 V) does not reset it, so near empty it can misbehave rather than restart. Add a regulator: [Hardware](hardware.md#a-regulator-for-the-esp32-optional).

If it happens during Wi-Fi bursts and the signal is strong, lowering the transmit power cuts the current peaks (the ESP32-S3 datasheet gives 340 mA at 21 dBm). In `firmware/kallsup-sendspin.yaml`, add `output_power: 17dB` under `wifi:`, then check that the stream still holds.

## The speaker switches itself off on battery 🔍

If the stock board powers down when it thinks nobody is listening, it takes the ESP32 with it. Check 2 in the [Build guide](build-guide.md#check-2-does-it-switch-itself-off-on-battery-) measures how long it waits. Option D in [Alternatives](alternatives.md), powered from USB 5 V directly, avoids it. A fix that keeps battery playback is an open question; open an issue with your timing.

## The battery drains while the speaker is off

The ESP32 is wired to a point that stays live when the speaker is off, probably `VCC_BAT`. Move it to the switched point from check 1. If the switched point is right, check the button pad with the speaker off (check 3, step 3): a pad held high feeds the ESP32 through `GPIO1`.

## It is quieter than it was

Expected. The stock amplifier boosts its supply and makes 3.5 W; the MAX98357A runs straight from the cell and makes about 1.7 W at 3.7 V. Tying `GAIN` to `GND` (12 dB) or through 100 kΩ to `GND` (15 dB) makes quiet material louder, but it does not raise the maximum.

## It never finishes charging while playing

The charger may be waiting for the charge current to fall, and the new boards keep drawing from the cell. Stop playback to let it finish. See the battery runs in the [Build guide](build-guide.md#battery-runs).

## The button does nothing

- Watch the **Button** entity in Home Assistant while pressing. If it never changes, the pad does not pull to ground; redo check 3 and adjust `mode` and `inverted`.
- If it changes but nothing happens, the presses may be falling outside the timing windows: one press is at most 350 ms down, then at least 351 ms up.

## Hum, hiss or crackle

- Every ground to `GND1`, with short wires.
- Keep the I2S wires short and away from the boost inductor `L1`.
- A little hiss close to the speaker is typical of a small class D amplifier. Tying `GAIN` to `Vin` lowers the gain to 6 dB, from 9 dB with it open.

## Weak Wi-Fi

The ESP32-S3-Zero's antenna is the small ceramic part at the end of the board. Keep it clear of the speaker magnet, the grille and the other boards.

## It will not flash over USB

Hold **BOOT** while plugging in the cable, then release. Use a data cable, not a charge-only one.
