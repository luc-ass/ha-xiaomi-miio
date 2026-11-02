"""Run Home Assistant core's xiaomi_miio tests against the custom copy.

The tests in ``tests/components/xiaomi_miio`` are kept byte-identical to core,
so they import and patch ``homeassistant.components.xiaomi_miio``. Those names
are aliased to ``custom_components.xiaomi_miio`` here, before any test module
is imported, so imports and ``mock.patch`` targets hit the custom code.
"""

import importlib
import pkgutil
import sys

import pytest

import custom_components.xiaomi_miio as custom

CORE = "homeassistant.components.xiaomi_miio"

sys.modules[CORE] = custom
for module in pkgutil.iter_modules(custom.__path__):
    sys.modules[f"{CORE}.{module.name}"] = importlib.import_module(
        f"{custom.__name__}.{module.name}"
    )

pytest_plugins = ["pytest_homeassistant_custom_component"]


@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(enable_custom_integrations):
    """Load xiaomi_miio from custom_components instead of core."""
    return
