import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import TrueNASAPI
from .const import (
    DOMAIN,
    UPDATE_INTERVAL_MINUTES,
)

_LOGGER = logging.getLogger(__name__)


class TrueNASDataUpdateCoordinator(DataUpdateCoordinator):
    config_entry: ConfigEntry

    def __init__(self, hass: HomeAssistant, client: TrueNASAPI):
        super().__init__(
            hass=hass,
            logger=_LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=UPDATE_INTERVAL_MINUTES),
        )
        self.client = client

    async def _async_update_data(self):
        try:
            return await self.hass.async_add_executor_job(self.client.get_pools)
        except Exception as error:
            raise UpdateFailed(f"Error fetching TrueNAS data: {error}") from error
