from typing import Any
from homeassistant.components.light import LightEntity
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import BasicHub
from .hub import MyCoordinator
from .const import DOMAIN

import logging

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass,
    config_entry,
    async_add_entities,
) -> None:
    bridge: BasicHub = hass.data[DOMAIN][config_entry.entry_id]
    coordinator = MyCoordinator(hass, bridge)
    await coordinator.async_config_entry_first_refresh()
    devices = []

    for device, status in (coordinator.data).items():
        print(device, status)
        devices.append(MyEntity(device, status, bridge, hass, coordinator))

    async_add_entities(devices)


class MyEntity(LightEntity, CoordinatorEntity):
    _attr_has_entity_name = True

    def __init__(self, name, state, hub, hass: HomeAssistant, coordinator) -> None:
        super().__init__(coordinator)
        self._is_on = state
        self._attr_unique_id = name
        self._attr_name = f"{name.capitalize()} Light"
        self.hub = hub
        self.hass = hass
        self.device = name
        _LOGGER.debug(f"[KASTA] {self._attr_unique_id} was registred in state: {state}")

    @callback
    def _handle_coordinator_update(self) -> None:
        state = self.coordinator.data[self.device]
        self._is_on = state
        self.async_write_ha_state()

    @property
    def device_info(self) -> DeviceInfo:
        """Return the device info."""
        return DeviceInfo(
            identifiers={
                # Serial numbers are unique identifiers within a specific domain
                (DOMAIN, self.unique_id)
            },
            name=self.name,
            manufacturer="Kasta Smart Living",
            model="MD-X1",
            sw_version="1.-.-",
            via_device=(DOMAIN, "KastaHub"),
        )

    @property
    def name(self) -> str:
        return self._attr_name

    @property
    def is_on(self) -> bool:
        return self._is_on

    def turn_on(self, **kwargs: Any) -> None:
        self.hub.toggle(self._attr_unique_id)
        _LOGGER.debug(f"[KASTA] Sent a request to turn on {self._attr_unique_id}")
        self._is_on = True

    def turn_off(self, **kwargs: Any) -> None:
        self.hub.toggle(self._attr_unique_id)
        _LOGGER.debug(f"[KASTA] Sent a request to turn off {self._attr_unique_id}")
        self._is_on = False
