"""Stand-in for Home Assistant core's ``tests.common`` (keeps core tests unchanged)."""

from pytest_homeassistant_custom_component import common as _common

globals().update(
    {name: value for name, value in vars(_common).items() if not name.startswith("__")}
)
