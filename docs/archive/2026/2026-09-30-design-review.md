# 🔎 Design review, 30 September 2026

An outside review of the wiring, the diagrams and whether the build can work, by Codex, then each point checked against primary sources. The docs were changed where a point held up. This file records what was found; the docs are the current state.

## Checked and adopted

| Point | Source | What changed |
|---|---|---|
| The Zero's `5V` pad is rated 3.7–6 V into an ME6217C33. From the cell, its 3.3 V rail holds to about 3.4–3.5 V on the pad at a 350 mA Wi-Fi peak and falls below the ESP32-S3's 3.0 V minimum at about 3.1–3.2 V | [Waveshare schematic](https://files.waveshare.com/wiki/ESP32-S3-Zero/ESP32-S3-Zero-Sch.pdf); [ME6217 datasheet](https://datasheet.lcsc.com/datasheet/pdf/722f7d98b8d249d1938ed34115c5822b.pdf?productCode=C81592), dropout 100 mV typ, 180 mV max at 300 mA; [ESP32-S3 datasheet](https://www.espressif.com/sites/default/files/documentation/esp32-s3_datasheet_en.pdf) table 5-2 | Hardware and wiring give the calculated range instead of "fine down to 3.7 V" |
| ESPHome keeps ESP-IDF's default brown-out level, 2.44 V on the S3, so the chip does not reset in that band | [ESP-IDF Kconfig](https://raw.githubusercontent.com/espressif/esp-idf/v5.4.2/components/esp_system/port/soc/esp32s3/Kconfig.system) | Troubleshooting says it misbehaves rather than resets |
| USB `VBUS` goes straight to the `5V` pad, with no diode | Waveshare schematic | The USB warning is now absolute |
| Driving `3V3` while `5V` is unpowered puts the ME6217's output above its input, which its datasheet forbids | ME6217 datasheet, p.5 and absolute maximum ratings | The recommended regulator is now a 5 V module on the `5V` pad; the 3.3 V route is listed as outside specification |
| The MAX98357A's 3.2 W is at 5 V. From 3.7 V into 4 Ω it makes about 1.7 W (10% THD), 1.35 W (1%) | [MAX98357A datasheet](https://cdn-shop.adafruit.com/product-files/3006/MAX98357A-MAX98357B.pdf), TOC19 | Parts, hardware, the architecture diagram and troubleshooting say the build is quieter than stock |
| A load on the cell can stop a terminating charger from ever finishing | [Microchip AN1149](https://ww1.microchip.com/downloads/en/AppNotes/01149c.pdf) | The battery runs include charging while playing |
| The auto-off check should be repeated with music playing | — | Check 2 says so |
| ESP32-S3 Wi-Fi transmit peaks at 340 mA at 21 dBm; ESPHome's `wifi: output_power` lowers it | ESP32-S3 datasheet table 5-7; [ESPHome Wi-Fi](https://esphome.io/components/wifi/) | Troubleshooting suggests it as an option, not a default |

## Adopted as inferred

| Point | Why only inferred | What changed |
|---|---|---|
| A button pad held high while the ESP32 is unpowered feeds current into `GPIO1` | The datasheet limits input high to VDD + 0.3 V, but Espressif does not describe the mechanism | Check 3 adds a reading with the speaker off, and a 10 kΩ series resistor if it stays high |
| The stock switched path can carry the new load | The stock board already fed a 3.5 W boosted amplifier from the same cell | Wiring gives wire size and points to the battery run |

## Checked and not adopted

| Point | Why not |
|---|---|
| GPIO3 as a strapping pin may upset boot | With default eFuses the S3 ignores GPIO3 at reset (datasheet table 3-5); firmware notes now say exactly that |
| The package's I2S pins were not verified | They were, against the pinned `SendspinZero-Speaker.yaml`, in the first review |
