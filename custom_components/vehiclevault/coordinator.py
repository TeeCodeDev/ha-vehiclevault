"""DataUpdateCoordinator for VehicleVault."""
from __future__ import annotations

import async_timeout
from datetime import timedelta
import logging
from typing import Any

from aiohttp import ClientError

from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class VehicleVaultDataCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Class to manage fetching VehicleVault sensor data."""

    def __init__(
        self,
        hass: HomeAssistant,
        url: str,
        api_key: str | None = None,
        update_interval: timedelta = timedelta(seconds=300),
    ) -> None:
        """Initialize the coordinator."""
        self.url = url.rstrip("/")
        self.api_key = api_key.strip() if api_key else None
        self.session = async_get_clientsession(hass)

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=update_interval,
        )

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from VehicleVault API endpoint."""
        endpoint = f"{self.url}/api/integrations/ha/sensors"
        headers: dict[str, str] = {
            "Accept": "application/json",
            "User-Agent": "HomeAssistant-VehicleVault/1.0",
        }

        if self.api_key:
            headers["X-API-Key"] = self.api_key
            headers["Authorization"] = f"Bearer {self.api_key}"

        try:
            async with async_timeout.timeout(15):
                response = await self.session.get(endpoint, headers=headers)
                if response.status == 401 or response.status == 403:
                    raise UpdateFailed("VehicleVault API key is invalid or missing.")
                if response.status != 200:
                    raise UpdateFailed(f"Error fetching VehicleVault data: HTTP {response.status}")

                data = await response.json()

        except TimeoutError as err:
            raise UpdateFailed(f"Timeout communicating with VehicleVault at {endpoint}") from err
        except ClientError as err:
            raise UpdateFailed(f"Network error communicating with VehicleVault: {err}") from err
        except Exception as err:
            raise UpdateFailed(f"Unexpected error communicating with VehicleVault: {err}") from err

        vehicles_list = data.get("vehicles", [])
        return {v["id"]: v for v in vehicles_list if "id" in v}
