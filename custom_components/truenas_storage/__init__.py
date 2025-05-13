from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .api import TrueNASAPI
from .const import CONF_API_KEY, CONF_HOST, CONF_PORT, CONF_VERIFY_SSL, DOMAIN
from .coordinator import TrueNASDataUpdateCoordinator


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    host = entry.data[CONF_HOST]
    port = entry.data[CONF_PORT]
    api_key = entry.data[CONF_API_KEY]
    verify_ssl = entry.data.get(CONF_VERIFY_SSL)

    client = TrueNASAPI(host=host, port=port, api_key=api_key, verify_ssl=verify_ssl)
    coordinator = TrueNASDataUpdateCoordinator(hass=hass, client=client)

    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, [Platform.SENSOR])
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    await hass.config_entries.async_forward_entry_unload(entry, Platform.SENSOR)
    hass.data[DOMAIN].pop(entry.entry_id)
    return True
