from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfInformation
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import TrueNASDataUpdateCoordinator


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
):
    coordinator: TrueNASDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    entities = []

    for pool in coordinator.data:
        name = pool.get("name")

        for metric in ("allocated", "free", "size"):
            entities.append(
                TrueNASStorageSensor(coordinator, entry.entry_id, name, metric)
            )

    async_add_entities(entities)


class TrueNASStorageSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, entry_id, pool_name, metric):
        super().__init__(coordinator)

        self._pool_name = pool_name
        self._metric = metric
        self._attr_name = f"TrueNAS {pool_name} {metric.capitalize()}"

        self._attr_native_unit_of_measurement = UnitOfInformation.BYTES
        self._attr_suggested_unit_of_measurement = UnitOfInformation.TERABYTES
        self._attr_device_class = "data_size"
        self._attr_state_class = "measurement"

        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry_id)},
            "name": f"TrueNAS Storage ({pool_name})",
            "manufacturer": "iXsystems",
            "model": "TrueNAS",
        }

    @property
    def unique_id(self):
        return self._get_unique_id()

    @property
    def native_value(self):
        return self._get_metric_value()

    def _get_unique_id(self):
        for pool in self.coordinator.data:
            if pool.get("name") == self._pool_name:
                guid = pool["guid"]
                return (
                    f"{self._pool_name.lower().replace(' ', '_')}_{self._metric}_{guid}"
                )

    def _get_metric_value(self):
        for pool in self.coordinator.data:
            if pool.get("name") == self._pool_name:
                return pool.get(self._metric)

        return None
