# Xiaomi Miio with clean by area

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)

A copy of Home Assistant's core **Xiaomi Home** (`xiaomi_miio`) integration that adds
**clean by area** (`vacuum.clean_area`, introduced in Home Assistant 2026.3) for
Roborock vacuums that are paired with the Xiaomi Home app, such as the Roborock S5.

The native Roborock integration supports clean by area, but older models like the S5
only work through the Xiaomi Home app and therefore through `xiaomi_miio`, which does
not. This custom integration overrides the core one with the same domain, so existing
config entries and entities keep working unchanged.

## What is different from core

Only the vacuum platform is extended, everything else is the unchanged core code of the
version in [`CORE_VERSION`](CORE_VERSION):

- The coordinator also reads the room mapping (`get_room_mapping`).
- Vacuums that report rooms get `VacuumEntityFeature.CLEAN_AREA`. Rooms show up as
  segments in the area mapping dialog, rooms without a name by their ID.
- `vacuum.clean_area` starts a segment clean of the mapped rooms.
- A repair issue is raised when the rooms change after the mapping was saved.

The diff to core is kept small on purpose, so it can be proposed upstream.
Compare `main` with the `upstream` branch to see it.

## Installation

1. HACS → three dots → *Custom repositories* → add this repository as *Integration*.
2. Download *Xiaomi Miio (clean by area)* and restart Home Assistant.
   Home Assistant logs a warning that the built-in `xiaomi_miio` is overridden.
3. Open the vacuum entity → *Clean by area* → *Configure areas* and map each room to an
   area.

To go back to core, remove the integration in HACS and restart.

The integration is only usable with the Home Assistant version it was copied from or
newer ones with compatible internals. Check the release notes before updating Home
Assistant.

## Development

```
uv sync
uv run pytest
uv run tools/raumliste.py      # read the room mapping of a real vacuum
tools/core_update.sh 2026.11.0 # take over a new core version
```

The core tests in `tests/components/xiaomi_miio` are unchanged; `conftest.py` points
them at the custom copy.

## License

Apache License 2.0, like Home Assistant core.
