"""Stand-in for Home Assistant core's ``tests.typing`` (keeps core tests unchanged)."""

from pytest_homeassistant_custom_component import typing as _typing

globals().update(
    {name: value for name, value in vars(_typing).items() if not name.startswith("__")}
)
