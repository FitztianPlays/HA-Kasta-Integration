from datetime import timedelta
import requests

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

import logging
_LOGGER = logging.getLogger(__name__)

class BasicHub:
    def __init__(self, host: str) -> None:
        self.host = host

    def verify_connection(self):
        try:
            r = requests.get(f"http://{self.host}/verify", timeout=10000)
            return r.status_code == 200
        except:
            return False

    def get_devices(self):
        r = requests.get(f"http://{self.host}/ha_status", timeout=10000)
        return r.json()

    def toggle(self, name):
        r = requests.get(f"http://{self.host}/toggle?name=" + name, timeout=10000)
        return r.json()


class MyCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, my_api) -> None:
        self.hass = hass
        super().__init__(
            hass,
            _LOGGER,
            name="Astra Polling",
            update_interval=timedelta(seconds=3),
        )
        self.my_api = my_api

    async def _async_update_data(self):
        stat = await self.hass.async_add_executor_job(self.my_api.get_devices)
        return stat
