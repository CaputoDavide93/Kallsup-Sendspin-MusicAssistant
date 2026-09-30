# 🤝 Contributing

Thanks for looking. Small, well-argued changes land fastest.

## Most wanted

Measurements from other KALLSUP units, especially the three 🔍 items in the [Build guide](docs/build-guide.md#before-you-solder): the switched battery point, the second button's pad, and the auto-off behaviour on battery. Include the board revision printed on the front (`V2.0` on the unit this was built from) and how you measured.

## Before you start

Open an issue for anything beyond a fix, so we can agree on the shape first.

## Working on the firmware

```bash
cp firmware/secrets.yaml.example firmware/secrets.yaml
sed -i "s|CHANGE_ME_KEY|$(openssl rand -base64 32)|" firmware/secrets.yaml
pip install esphome
esphome config firmware/kallsup-sendspin.yaml
```

Keep SendspinZero as a pinned remote package; do not copy its YAML in. Bumping `ref` is its own commit, validated, and noted in `CHANGELOG.md`.

## Working on the diagrams and icon

`tools/gen_diagram.py` draws `docs/assets/*-light.svg` and `*-dark.svg`; `tools/gen_brand.py` draws `brand/icon.png`. Edit the script, run it, commit the result; never edit the output by hand. CI runs `python3 tools/gen_diagram.py --check`.

## Style

- Documentation never lies. A finding is marked measured, inferred or open, and moves only when someone measures it.
- Comments explain why, not what.
- Plain English, active voice, no marketing.

## Commits

Conventional prefixes (`feat:`, `fix:`, `docs:`, `ci:`, `chore:`), one concern per commit, a body that says why. No sign-off trailers.
