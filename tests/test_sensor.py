from typing import Any, Generator
from unittest.mock import MagicMock

from homeassistant.const import UnitOfInformation
from homeassistant.core import HomeAssistant
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.truenas_storage.const import (
    CONF_API_KEY,
    CONF_HOST,
    CONF_PORT,
    CONF_VERIFY_SSL,
    DOMAIN,
)


async def test_sensor(
    hass: HomeAssistant, mock_truenas_api_response: Generator[MagicMock, Any, None]
):
    config_entry = MockConfigEntry(
        domain=DOMAIN,
        data={
            CONF_HOST: "truenas.local",
            CONF_PORT: 443,
            CONF_API_KEY: "test-api-key",
            CONF_VERIFY_SSL: True,
        },
    )
    config_entry.add_to_hass(hass)

    config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    for state in hass.states.async_all():
        print(state.entity_id)
        print(state.state)

    state_allocated = hass.states.get("sensor.truenas_tank_allocated")

    assert state_allocated.state == "6.597069766656"
    assert (
        state_allocated.attributes["unit_of_measurement"] == UnitOfInformation.TERABYTES
    )

    state_free = hass.states.get("sensor.truenas_tank_free")

    assert state_free.state == "4.398046511104"
    assert state_free.attributes["unit_of_measurement"] == UnitOfInformation.TERABYTES

    state_size = hass.states.get("sensor.truenas_tank_size")

    assert state_size.state == "10.995116277760"
    assert state_size.attributes["unit_of_measurement"] == UnitOfInformation.TERABYTES
