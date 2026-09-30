# 🛠️ Troubleshooting

## No sound

1. **Is it playing?** The ESP32's LED is green while playing and red when idle. Red while Music Assistant says it is playing means the stream is not arriving: check Wi-Fi and the Home Assistant logs.
2. **Green but silent?** Check the three audio wires. `GPIO2` goes to `DIN`, `GPIO3` to `BCLK`, `GPIO4` to `LRC`; swapping two is the usual mistake.
3. **Power to the amplifier?** Measure `Vin` to `GND` on the MAX98357A with the speaker on.
4. **Speaker on the terminal?** Red to `+`, black to `−`, screws tight.

## The ESP32 resets or drops Wi-Fi as the battery runs down

Its `5V` pad needs at least 3.7 V, and the cell goes down to about 3.0 V. Add a 3.3 V buck-boost module feeding the `3V3` pin instead of `5V`: [Hardware](hardware.md#tps63020-33-v-buck-boost-module-optional).

## The speaker switches itself off on battery 🔍

If the stock board powers down when it thinks nobody is listening, it takes the ESP32 with it. Check 2 in the [Build guide](build-guide.md#check-2-does-it-switch-itself-off-on-battery-) measures how long it waits. Option D in [Alternatives](alternatives.md), powered from USB 5 V directly, avoids it. A fix that keeps battery playback is an open question; open an issue with your timing.

## The battery drains while the speaker is off

The ESP32 is wired to a point that stays live when the speaker is off, probably `VCC_BAT`. Move it to the switched point from check 1.

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
