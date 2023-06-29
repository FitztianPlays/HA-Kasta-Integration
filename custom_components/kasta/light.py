from typing import Any
from homeassistant.components.light import LightEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from . import BasicHub
from .const import DOMAIN

import logging

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass,
    config_entry,
    async_add_entities,
) -> None:
    bridge: BasicHub = hass.data[DOMAIN][config_entry.entry_id]
    devices = []
    for device, status in (
        await hass.async_add_executor_job(bridge.get_devices)
    ).items():
        devices.append(MyEntity(device, status, bridge, hass))

    async_add_entities(devices)


class MyEntity(LightEntity):
    _attr_has_entity_name = True

    def __init__(self, name, state, hub, hass: HomeAssistant) -> None:
        self._is_on = state
        self._attr_unique_id = name
        self._attr_name = f"{name.capitalize()} Light"
        self.hub = hub
        self.hass = hass
        _LOGGER.debug(f"[KASTA] {self._attr_unique_id} was registred in state: {state}")

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
