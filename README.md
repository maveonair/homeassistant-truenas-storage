# homeassistant-truenas-storage

A Home Assistant custom integration for monitoring storage pools on [TrueNAS](https://www.truenas.com/) Scale.

I created this integration to monitor Storage Pools of my TrueNAS Scale systems and learn to write a Home Assistant custom component. There’s a feature-rich TrueNAS integration for Home Assistant worth checking out: https://github.com/tomaae/homeassistant-truenas

## Features

- Connects to your TrueNAS Scale instance via API key
- Monitors storage pool metrics: allocated, free, and total size
- Configuration via Home Assistant UI

## Installation

1. Copy the `custom_components/truenas_storage` directory into your Home Assistant `custom_components` folder.
2. Restart Home Assistant.

## Configuration

1. In Home Assistant, go to **Settings > Devices & Services > Add Integration**.
2. Search for **TrueNAS Storage**.
3. Enter your TrueNAS hostname, port, and API key.
4. Optionally, toggle SSL verification.

## Requirements

- Home Assistant 2025.4.4 or newer
- TrueNAS Scale system with API access enabled

## Development

- Python 3.13+
- See [pyproject.toml](pyproject.toml) for dependencies

## License

[Apache License 2.0](LICENSE)
