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
