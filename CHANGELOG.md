# Changelog

All notable changes to this project are recorded here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project uses
[Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added
- **Firmware.** ESPHome config built on SendspinZero Speaker, pinned to
  `0c7f82b`, with an encrypted API, OTA that requires the API key, Wi-Fi from
  `secrets.yaml`, and the KALLSUP's second button on `GPIO1` as play/pause,
  next and previous.
- **Build documentation.** Build guide with the three board measurements,
  pad-by-pad wiring, hardware notes, firmware notes, troubleshooting, and the
  Bluetooth-keeping alternatives.
- **Board notes.** The KALLSUP E2507 teardown: parts, test pads, the ANT8817S
  datasheet summary and pin findings, each marked measured, inferred or open.
- **Diagrams and brand.** Architecture and wiring diagrams in light and dark,
  drawn by `tools/gen_diagram.py`; the icon, drawn by `tools/gen_brand.py`.
- **CI.** ESPHome config validation and a diagram freshness check.
- **Board notes: continuity log and more parts.** The unpowered continuity
  tests behind the measured findings, the rest of the identified parts (X1,
  the PVDD and output-filter capacitors, FB1/FB2, Q2, Q3, ZD1, TVS1, P1, P2,
  LED1's resistors), the `RF` pad, the `94V-0` marking, and the
  `VCC_PW00`/`VCC_PVDD` correction.
- **Build guide: extra tests.** A TPS63020 output check on the bench, and
  low-battery and runtime runs after first power-up.
- **Pictures for the build.** Two hookup views drawn with the boards' real
  pin order and coloured wires, one for the bench test and one inside the
  KALLSUP, in the build guide and wiring doc. Annotated copies of the teardown
  photos ring what to solder, measure first or keep off, drawn by
  `tools/annotate_photos.py`. CONTRIBUTING.md lists the real build photos
  wanted.

### Security
- **Pinned startup chime.** The package fetches its chime from another
  repository's `main` branch; `firmware/kallsup-sendspin.yaml` now pins it to
  `e8f5c27`, so the `ref` pin really freezes what the package brings in.
- **Captive-portal upload documented.** While the fallback hotspot is up, its
  captive portal accepts firmware without the API key. SECURITY.md, the README
  and the firmware notes now say so, and that `fallback_password` guards it.
