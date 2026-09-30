# 📟 Firmware

[`firmware/kallsup-sendspin.yaml`](../firmware/kallsup-sendspin.yaml) is an ESPHome config with two parts.

- **The audio**: [SendspinZero](https://github.com/RealDeco/SendspinZero)'s `SendspinZero-Speaker.yaml`, pulled in as a remote package and pinned to a commit. It sets up I2S on `GPIO2`/`GPIO3`/`GPIO4` for a MAX98357A, the Sendspin media player, the status LED and the entities listed below.
- **This build**: the device name, an encrypted API, OTA that requires the same key, Wi-Fi and a fallback-hotspot password from `secrets.yaml`, and the KALLSUP's second button.

Nothing from SendspinZero is copied into this repository. Pinning the commit means an upstream change reaches the speaker only when `ref` is bumped on purpose.

## Flashing

```bash
cp firmware/secrets.yaml.example firmware/secrets.yaml
# fill in wifi_ssid, wifi_password, fallback_password and
# api_encryption_key (openssl rand -base64 32)
pip install esphome
esphome run firmware/kallsup-sendspin.yaml
```

For the first flash, hold **BOOT** on the ESP32-S3-Zero while plugging in the USB-C cable; the board has no USB-to-UART chip and will not accept a flash otherwise. Later flashes go over the air, authenticated by the API key.

The ESPHome Device Builder add-on in Home Assistant works too: paste the YAML into a new device and put the four secrets in its secrets editor.

If Wi-Fi is unreachable at boot, the speaker opens its own access point, protected by `fallback_password`, with a captive portal after about 90 seconds, so it can still be put on a network.

## Adopting it

Home Assistant discovers the speaker as an ESPHome device and asks for the `api_encryption_key`. Once adopted, Music Assistant offers it as a Sendspin player.

Entities:

| Entity | From | What it is |
|---|---|---|
| Sendspin Group Media Player | SendspinZero | The player Music Assistant streams to |
| Media Player | SendspinZero | Local player, used for announcements |
| Song Title, Song Artist, Album Name | SendspinZero | What is playing |
| Startup sound | SendspinZero | Switch: chime on boot |
| Restart | SendspinZero | Button |
| LED light | SendspinZero | The ESP32's WS2812: red idle, green playing |
| Button | This repository | The KALLSUP's second button, as a binary sensor |

## The button

`GPIO1`, internal pull-up, inverted: pressed reads as on. A 20 ms debounce, then:

| Press | Action on the Sendspin player |
|---|---|
| Single | `media_player.toggle` (play/pause) |
| Double | `media_player.next` |
| Triple | `media_player.previous` |

This assumes the KALLSUP's pad is pulled to ground when pressed; check 3 in the [Build guide](build-guide.md#check-3-the-second-buttons-pad-) confirms it. If the pad pulls high instead, change `mode` to `INPUT_PULLDOWN` and `inverted` to `false`.

The stock Bluetooth chip still sees the button too. With nothing paired over Bluetooth that does no harm.

## Validation warnings

`esphome config` prints two warnings, both expected:

- **GPIO3 is a strapping pin.** SendspinZero uses it for the I2S bit clock. Its level only matters at reset, and the MAX98357A's `BCLK` is an input, so it does not pull the pin either way.
- **Merged multiple configurations for OTA.** This config adds the key requirement to SendspinZero's OTA entry; ESPHome merges the two into one, which is the intent.

## Updating SendspinZero

1. Find the new commit: `git ls-remote https://github.com/RealDeco/SendspinZero HEAD`.
2. Put it in `ref:` in the YAML.
3. `esphome config firmware/kallsup-sendspin.yaml`, then flash.
4. Note the bump in `CHANGELOG.md`.
