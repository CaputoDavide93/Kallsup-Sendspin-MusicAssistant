# 🤝 Contributing

Thanks for looking. Small, well-argued changes land fastest.

## Most wanted

Measurements from other KALLSUP units, especially the three 🔍 items in the [Build guide](docs/build-guide.md#before-you-solder): the switched battery point, the second button's pad, and the auto-off behaviour on battery. Include the board revision printed on the front (`V2.0` on the unit this was built from) and how you measured.

## Before you start

Open an issue for anything beyond a fix, so we can agree on the shape first.

## Working on the firmware

```bash
cp firmware/secrets.yaml.example firmware/secrets.yaml
sed -i.bak "s|CHANGE_ME_KEY|$(openssl rand -base64 32)|" firmware/secrets.yaml && rm firmware/secrets.yaml.bak
pip install esphome
esphome config firmware/kallsup-sendspin.yaml
```

Keep SendspinZero as a pinned remote package; do not copy its YAML in. Bumping `ref` is its own commit, validated, and noted in `CHANGELOG.md`.

## Working on the diagrams and icon

`tools/gen_diagram.py` draws `docs/assets/*-light.svg` and `*-dark.svg`; `tools/gen_mockups.py` draws the build mockups in `docs/assets/mockups/`; `tools/annotate_photos.py` draws the rings and labels on copies of the teardown photos into `docs/assets/annotated/`. `tools/gen_brand.py` draws `brand/icon.svg`. `tools/annotate_photos.py` needs `pip install pillow`. Edit the script, run it, commit the result; never edit the output by hand. CI runs the `--check` of `gen_diagram.py`, `gen_mockups.py` and `gen_brand.py`.

An annotation says what the docs say about that spot and nothing more: a pad a check has not settled is ringed amber as a check, never green as a place to solder.

## Photos of your build

The wiring pictures are mockups, because nobody has finished this build yet. Real photos of a build are the next most useful contribution after measurements. Resize them to 1400 px on the long side, strip the metadata, and put them in `docs/assets/photos/` with these names:

| File | Shot |
|---|---|
| `bench-test.jpg` | The ESP32 and MAX98357A on jumper wires, playing, LED green |
| `joint-gnd1.jpg` | The wire soldered to `GND1`, close up |
| `joint-switched-point.jpg` | The wire on the switched point from check 1, with the part it is on in frame |
| `joint-button.jpg` | The wire on the second button's pad |
| `speaker-terminal.jpg` | The stock speaker leads in the MAX98357A terminal |
| `inside-assembled.jpg` | Everything taped down inside the case, before closing it |

Say which check readings the photo goes with, so the matching 🔍 item can move to ✅.

## Style

- Documentation never lies. A finding is marked measured, inferred or open, and moves only when someone measures it.
- Comments explain why, not what.
- Plain English, active voice, no marketing.

## Commits

Conventional prefixes (`feat:`, `fix:`, `docs:`, `ci:`, `chore:`), one concern per commit, a body that says why. No sign-off trailers.
