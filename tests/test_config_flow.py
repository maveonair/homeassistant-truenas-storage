from typing import Any, Generator
from unittest.mock import MagicMock, patch

from homeassistant import config_entries, setup
from homeassistant.const import CONF_API_KEY, CONF_HOST, CONF_PORT, CONF_VERIFY_SSL
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType

from custom_components.truenas_storage.const import DOMAIN


async def test_form(
    hass: HomeAssistant, mock_truenas_api_response: Generator[MagicMock, Any, None]
):
    await setup.async_setup_component(hass, "persistent_notification", {})

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    assert result["type"] == "form"
    assert result["errors"] == {}

    with patch(
        "custom_components.truenas_storage.async_setup_entry",
        return_value=True,
    ) as mock_setup_entry:
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                CONF_HOST: "truenas.local",
                CONF_PORT: 443,
                CONF_API_KEY: "test-api-key",
            },
        )
        await hass.async_block_till_done()

    assert result["type"] == FlowResultType.CREATE_ENTRY
    assert result["title"] == "truenas.local:443"
    assert result["data"] == {
        CONF_HOST: "truenas.local",
        CONF_PORT: 443,
        CONF_API_KEY: "test-api-key",
        CONF_VERIFY_SSL: True,
    }
    assert len(mock_setup_entry.mock_calls) == 1
