"""Tests for cleaning by area (segments) on the Xiaomi vacuum platform."""

from collections.abc import Generator
from datetime import timedelta
from unittest.mock import MagicMock, patch

from miio import DeviceException
import pytest

from homeassistant.components.vacuum import (
    DOMAIN as VACUUM_DOMAIN,
    SERVICE_CLEAN_AREA,
    VacuumEntityFeature,
)
from homeassistant.components.xiaomi_miio.const import (
    CONF_FLOW_TYPE,
    DOMAIN,
    MODELS_VACUUM,
)
from homeassistant.const import (
    ATTR_ENTITY_ID,
    ATTR_SUPPORTED_FEATURES,
    CONF_DEVICE,
    CONF_HOST,
    CONF_MAC,
    CONF_MODEL,
    CONF_TOKEN,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er, issue_registry as ir

from . import TEST_MAC

from tests.common import MockConfigEntry, async_fire_time_changed
from tests.typing import WebSocketGenerator

ENTITY_ID = f"{VACUUM_DOMAIN}.test_vacuum"
ROOMS = [[16, "Schlafzimmer"], [17, ""]]


@pytest.fixture(name="mock_vacuum")
def mock_vacuum_fixture() -> Generator[MagicMock]:
    """Mock a docked Roborock vacuum that reports two rooms."""
    mock_vacuum = MagicMock()
    mock_vacuum.status().state_code = 8
    mock_vacuum.status().got_error = False
    mock_vacuum.fan_speed_presets.return_value = {"Standard": 102}
    mock_vacuum.status().fanspeed = 102
    mock_vacuum.timer.return_value = []
    mock_vacuum.status().clean_time = timedelta(0)
    mock_vacuum.get_room_mapping.return_value = ROOMS

    with patch(
        "homeassistant.components.xiaomi_miio.RoborockVacuum"
    ) as mock_vacuum_cls:
        mock_vacuum_cls.return_value = mock_vacuum
        yield mock_vacuum


async def setup_vacuum(hass: HomeAssistant) -> None:
    """Set up the vacuum config entry."""
    config_entry = MockConfigEntry(
        domain=DOMAIN,
        unique_id="123456",
        title="test_vacuum",
        data={
            CONF_FLOW_TYPE: CONF_DEVICE,
            CONF_HOST: "192.168.1.100",
            CONF_TOKEN: "12345678901234567890123456789012",
            CONF_MODEL: MODELS_VACUUM[0],
            CONF_MAC: TEST_MAC,
        },
    )
    config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()


def supported_features(hass: HomeAssistant) -> VacuumEntityFeature:
    """Return the supported features of the test vacuum."""
    state = hass.states.get(ENTITY_ID)
    assert state
    return VacuumEntityFeature(state.attributes[ATTR_SUPPORTED_FEATURES])


async def test_clean_area_supported_with_rooms(
    hass: HomeAssistant, mock_vacuum: MagicMock
) -> None:
    """Test CLEAN_AREA is offered when the vacuum reports rooms."""
    await setup_vacuum(hass)

    assert VacuumEntityFeature.CLEAN_AREA in supported_features(hass)


@pytest.mark.parametrize(
    "room_mapping",
    [[], DeviceException("unknown_method")],
    ids=["no_rooms", "unsupported"],
)
async def test_clean_area_not_supported_without_rooms(
    hass: HomeAssistant, mock_vacuum: MagicMock, room_mapping
) -> None:
    """Test CLEAN_AREA is not offered without rooms or room mapping support."""
    mock_vacuum.get_room_mapping.side_effect = (
        room_mapping if isinstance(room_mapping, Exception) else None
    )
    mock_vacuum.get_room_mapping.return_value = room_mapping
    await setup_vacuum(hass)

    assert VacuumEntityFeature.CLEAN_AREA not in supported_features(hass)


async def test_clean_area_kept_when_fetch_fails(
    hass: HomeAssistant, mock_vacuum: MagicMock, freezer
) -> None:
    """Test CLEAN_AREA stays once rooms were seen, even if a later fetch fails."""
    await setup_vacuum(hass)

    mock_vacuum.get_room_mapping.side_effect = DeviceException("timeout")
    freezer.tick(timedelta(minutes=1))
    async_fire_time_changed(hass)
    await hass.async_block_till_done()

    assert VacuumEntityFeature.CLEAN_AREA in supported_features(hass)


async def test_get_segments(
    hass: HomeAssistant,
    hass_ws_client: WebSocketGenerator,
    mock_vacuum: MagicMock,
) -> None:
    """Test the rooms are returned as segments, unnamed rooms by their id."""
    await setup_vacuum(hass)

    client = await hass_ws_client(hass)
    await client.send_json_auto_id(
        {"type": "vacuum/get_segments", "entity_id": ENTITY_ID}
    )
    msg = await client.receive_json()

    assert msg["success"]
    assert msg["result"]["segments"] == [
        {"id": "16", "name": "Schlafzimmer", "group": None},
        {"id": "17", "name": "17", "group": None},
    ]


async def test_clean_area(
    hass: HomeAssistant,
    entity_registry: er.EntityRegistry,
    mock_vacuum: MagicMock,
) -> None:
    """Test cleaning an area starts a segment clean of the mapped rooms."""
    await setup_vacuum(hass)
    entity_registry.async_update_entity_options(
        ENTITY_ID,
        VACUUM_DOMAIN,
        {
            "area_mapping": {"schlafzimmer": ["16"], "flur_og": ["17"]},
            "last_seen_segments": [
                {"id": "16", "name": "Schlafzimmer", "group": None},
                {"id": "17", "name": "17", "group": None},
            ],
        },
    )

    await hass.services.async_call(
        VACUUM_DOMAIN,
        SERVICE_CLEAN_AREA,
        {ATTR_ENTITY_ID: ENTITY_ID, "cleaning_area_id": ["schlafzimmer", "flur_og"]},
        blocking=True,
    )

    mock_vacuum.segment_clean.assert_called_once_with(segments=[16, 17])


async def test_segments_changed_issue(
    hass: HomeAssistant,
    entity_registry: er.EntityRegistry,
    issue_registry: ir.IssueRegistry,
    mock_vacuum: MagicMock,
    freezer,
) -> None:
    """Test a repair issue is raised when the rooms differ from the mapping."""
    await setup_vacuum(hass)
    entity_registry.async_update_entity_options(
        ENTITY_ID,
        VACUUM_DOMAIN,
        {
            "area_mapping": {"schlafzimmer": ["16"]},
            "last_seen_segments": [
                {"id": "16", "name": "Schlafzimmer", "group": None},
                {"id": "17", "name": "17", "group": None},
            ],
        },
    )
    await hass.async_block_till_done()
    assert not issue_registry.issues

    mock_vacuum.get_room_mapping.return_value = [[16, "Schlafzimmer"]]
    freezer.tick(timedelta(minutes=1))
    async_fire_time_changed(hass)
    await hass.async_block_till_done()

    assert len(issue_registry.issues) == 1
    issue = next(iter(issue_registry.issues.values()))
    assert issue.domain == VACUUM_DOMAIN
    assert issue.translation_key == "segments_changed"
