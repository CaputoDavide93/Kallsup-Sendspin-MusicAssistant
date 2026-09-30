# 📚 KALLSUP Sendspin docs

| Doc | What it covers |
|---|---|
| [build-guide.md](build-guide.md) | Bench test, the three board measurements, then soldering, first power-up, battery runs and assembly |
| [wiring.md](wiring.md) | Every connection, pad by pad, with photos and the reason for each |
| [hardware.md](hardware.md) | The parts, what each one is for, and what does not work |
| [firmware.md](firmware.md) | The ESPHome config, flashing, adopting in Home Assistant, updating |
| [board-notes.md](board-notes.md) | What is on the KALLSUP board, measured versus inferred, with the continuity test log |
| [alternatives.md](alternatives.md) | The other routes, most of which keep Bluetooth, and why this build does not |
| [troubleshooting.md](troubleshooting.md) | Symptom-first fixes |

Superseded and dated material is in [archive/](archive/): the [design review of 30 September 2026](archive/2026/2026-09-30-design-review.md) records the outside review of the power design and how each point was checked.

Items marked 🔍 are not yet measured on a board. Diagrams in [assets/](assets/) are drawn by `tools/gen_diagram.py`; the photos in [assets/photos/](assets/photos/) are from the teardown this project was designed on, and [assets/annotated/](assets/annotated/) holds copies of them with the pads to solder, measure or keep off ringed by `tools/annotate_photos.py`.
