# 🔒 Security Policy

## Reporting a vulnerability

Report privately through
[GitHub Security Advisories](https://github.com/CaputoDavide93/Kallsup-Sendspin-MusicAssistant/security/advisories/new)
rather than a public issue. You should hear back within a week.

## What this project touches

- **Your Wi-Fi.** The SSID and password are compiled into the firmware from `secrets.yaml`, which is gitignored.
- **The ESPHome API.** Encrypted with `api_encryption_key`. Home Assistant needs the key to adopt the speaker.
- **Over-the-air updates.** Accepted over the network only from an uploader holding the same key (`ota: encryption: {}`). The SendspinZero config on its own leaves both the API and OTA open; this repository closes them. One exception: while the fallback hotspot is up, its captive portal also accepts a firmware upload without the key, so anyone who has joined the hotspot can reflash the speaker.
- **A fallback access point.** If the configured Wi-Fi is unreachable, the speaker opens its own hotspot with a captive portal after about 90 seconds. It is protected by `fallback_password`; the SendspinZero config on its own leaves it open. Because of the captive portal's upload page, that password guards reflashing while the hotspot is up.

## What it does not do

- No microphone. It plays audio and reports what is playing; it records nothing.
- No cloud. It talks to Home Assistant and Music Assistant on your network, and fetches its startup chime from GitHub, pinned to a commit, when the firmware is built, not at runtime.

## Deployment checklist

- Generate a fresh `api_encryption_key` with `openssl rand -base64 32`, and choose a strong `fallback_password`: it guards reflashing while the hotspot is up. Never keep the example values.
- Keep `firmware/secrets.yaml` out of commits. `.gitignore` already excludes it.
- Put the speaker on a network you trust.

## Supported versions

The latest commit on `main`.
