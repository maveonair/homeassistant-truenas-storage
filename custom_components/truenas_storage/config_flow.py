import logging

import voluptuous as vol
from homeassistant import config_entries

from .api import TrueNASAPI
from .const import (
    CONF_API_KEY,
    CONF_HOST,
    CONF_PORT,
    CONF_VERIFY_SSL,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)

DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_HOST): str,
        vol.Required(CONF_PORT, default=443): int,
        vol.Required(CONF_API_KEY): str,
        vol.Optional(CONF_VERIFY_SSL, default=True): bool,
    }
)


class TrueNASConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            host = user_input[CONF_HOST]
            port = user_input[CONF_PORT]
            api_key = user_input[CONF_API_KEY]
            verify_ssl = user_input[CONF_VERIFY_SSL]

            try:
                client = TrueNASAPI(
                    host=host, port=port, api_key=api_key, verify_ssl=verify_ssl
                )

                await self.hass.async_add_executor_job(client.get_pools)

                return self.async_create_entry(title=f"{host}:{port}", data=user_input)
            except Exception as error:
                _LOGGER.error(f"Config failure: {error}")
                errors["base"] = "cannot_connect"

        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA, errors=errors
        )
