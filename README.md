# OVOS Home Assistant Integration

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

[![pre-commit][pre-commit-shield]][pre-commit]
[![Black][black-shield]][black]

[![hacs][hacsbadge]][hacs]
[![Project Maintenance][maintenance-shield]][user_profile]

[![Discord][discord-shield]][discord]
[![Community Forum][forum-shield]][forum]

**This component will set up the following actions.**

| Platform | Description                                            |
| -------- | ------------------------------------------------------ |
| `notify` | Send a notification to an OVOS/Neon.AI Voice Assistant |

## Installation

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
2. If you do not have a `custom_components` directory (folder) there, you need to create it.
3. In the `custom_components` directory (folder) create a new folder called `ovos`.
4. Download _all_ the files from the `custom_components/ovos/` directory (folder) in this repository.
5. Place the files you downloaded in the new directory (folder) you created.
6. Restart Home Assistant
7. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "OVOS Home Assistant Integration"

Using your HA configuration directory (folder) as a starting point you should now also have this:

```text
custom_components/ovos/translations/en.json
custom_components/ovos/__init__.py
custom_components/ovos/const.py
custom_components/ovos/manifest.json
custom_components/ovos/notify.py
```

## Configuration

In `configuration.yaml`:

```yaml
ovos:
  host: 192.168.42.42 # Replace with your IP/hostname
notify:
  - platform: ovos
    name: mark2 # Name it whatever you want
```

Then call `notify.mark2` with a message you'd like the OVOS/Neon.AI Voice Assistant to speak.

## Available services

- notify
- mute_mic
- unmute_mic

## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

## Credits

This project was generated from [@oncleben31](https://github.com/oncleben31)'s [Home Assistant Custom Component Cookiecutter](https://github.com/oncleben31/cookiecutter-homeassistant-custom-component) template.

Code template was mainly taken from [@Ludeeus](https://github.com/ludeeus)'s [integration_blueprint][integration_blueprint] template

---

[integration_blueprint]: https://github.com/custom-components/integration_blueprint
[black]: https://github.com/psf/black
[black-shield]: https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge
[commits-shield]: https://img.shields.io/github/commit-activity/y/mikejgray/ovos-home-assistant-integration.svg?style=for-the-badge
[commits]: https://github.com/mikejgray/ovos-home-assistant-integration/commits/main
[hacs]: https://hacs.xyz
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge
[discord]: https://discord.gg/Qa5fW2R
[discord-shield]: https://img.shields.io/discord/330944238910963714.svg?style=for-the-badge
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=for-the-badge
[forum]: https://community.home-assistant.io/
[license-shield]: https://img.shields.io/github/license/mikejgray/ovos-home-assistant-integration.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-%40mikejgray-blue.svg?style=for-the-badge
[pre-commit]: https://github.com/pre-commit/pre-commit
[pre-commit-shield]: https://img.shields.io/badge/pre--commit-enabled-brightgreen?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/mikejgray/ovos-home-assistant-integration.svg?style=for-the-badge
[releases]: https://github.com/mikejgray/ovos-home-assistant-integration/releases
[user_profile]: https://github.com/mikejgray
