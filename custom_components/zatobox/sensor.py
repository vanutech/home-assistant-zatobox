"""Platform for sensor integration."""
from datetime import timedelta
import logging
from typing import Any, Callable, Dict, Optional

from homeassistant import config_entries, core
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.typing import (
    ConfigType,
    DiscoveryInfoType,
    HomeAssistantType,
)
import voluptuous as vol

from .const import (
    DOMAIN,
)

import async_timeout

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import UnitOfPower
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)

_LOGGER: logging.Logger = logging.getLogger(__package__)


async def async_setup_entry(
    hass: core.HomeAssistant,
    config_entry: config_entries.ConfigEntry,
    async_add_entities,
):
    
    _LOGGER.debug("async setup")
    my_api = hass.data[DOMAIN][config_entry.entry_id]
    
    _LOGGER.debug(my_api)
    coordinator = ZatoboxCoordinator(hass, config_entry, my_api)

    
    _LOGGER.debug("setup entities with coordinator")

    await coordinator.async_config_entry_first_refresh()


    _LOGGER.debug(coordinator.data)
    async_add_entities(
        ZatoboxEntity(coordinator, idx) for idx, ent in enumerate(coordinator.data)
    )

async def async_setup_platform(
    hass: HomeAssistantType,
    config: ConfigType,
    async_add_entities: Callable,
    discovery_info: Optional[DiscoveryInfoType] = None,
) -> None:
    """Set up the sensor platform."""
    
    _LOGGER.debug("async platform setup")
    my_api = None
    
    _LOGGER.debug(my_api)
    coordinator = ZatoboxCoordinator(hass, None, my_api)

    _LOGGER.debug("setup platform entities with coordinator")
    await coordinator.async_config_entry_first_refresh()

    _LOGGER.debug(coordinator.data)
    async_add_entities(
        ZatoboxEntity(coordinator, idx) for idx, ent in enumerate(coordinator.data)
    )

class ZatoboxCoordinator(DataUpdateCoordinator):
    """My custom coordinator."""

    def __init__(self, hass, config_entry, my_api):
        """Initialize my coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            # Name of the data. For logging purposes.
            name="zatobox_sensor",
            config_entry=config_entry,
            # Polling interval. Will only be polled if there are subscribers.
            update_interval=timedelta(seconds=5),
            # Set always_update to `False` if the data returned from the
            # api can be compared via `__eq__` to avoid duplicate updates
            # being dispatched to listeners
            always_update=True
        )
        self.my_api = my_api

        #self._device: MyDevice | None = None

    async def _async_setup(self):
        """Set up the coordinator

        This is the place to set up your coordinator,
        or to load data, that only needs to be loaded once.

        This method will be called automatically during
        coordinator.async_config_entry_first_refresh.
        """
        #self._device = await self.my_api.get_device()
        
        _LOGGER.debug("load device data")

    async def _async_update_data(self):
        """Fetch data from API endpoint.

        This is the place to pre-process the data to lookup tables
        so entities can quickly look up their data.
        """
        coordinator_data = [
            {"name": "Zatobox 1", "power": "10", "attribute1": "value1"},
            {"name": "Zatobox 2", "power": "20", "attribute1": "value2"},
            {"name": "Zatobox 3", "power": "30", "attribute1": "value3"},
        ]
        return coordinator_data; #await self.my_api.fetch_data(listening_idx)



class ZatoboxEntity(CoordinatorEntity, SensorEntity):
    """Representation of a Sensor."""

    _attr_name = "Vanubus Sensor"
    _attr_native_unit_of_measurement = UnitOfPower.WATT
    _attr_device_class = SensorDeviceClass.POWER
    _attr_state_class = SensorStateClass.MEASUREMENT


    def __init__(self, coordinator, idx):
        """Pass coordinator to CoordinatorEntity."""
        super().__init__(coordinator, context=idx)
        self.idx = idx        
        host = "192.168.68.102"  # Replace with the actual IP address of the device

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        
        _LOGGER.debug(f"update entity {self.idx}")

        self._attr_native_value = self.coordinator.data[self.idx]["power"]
        self.async_write_ha_state()

    def update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """

        