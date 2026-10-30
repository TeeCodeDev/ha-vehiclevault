"""Image platform for VehicleVault."""
from __future__ import annotations

from datetime import datetime
from typing import Any

from homeassistant.components.image import ImageEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import VehicleVaultDataCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up VehicleVault vehicle image entities based on a config entry."""
    coordinator: VehicleVaultDataCoordinator = hass.data[DOMAIN][entry.entry_id]

    entities: list[VehicleVaultImage] = []
    for vehicle_id, vehicle in coordinator.data.items():
        if vehicle.get("image_url") or vehicle.get("attributes", {}).get("image_url"):
            entities.append(VehicleVaultImage(hass, coordinator, vehicle_id))

    if entities:
        async_add_entities(entities)


class VehicleVaultImage(CoordinatorEntity[VehicleVaultDataCoordinator], ImageEntity):
    """Representation of a VehicleVault vehicle photo entity."""

    def __init__(
        self,
        hass: HomeAssistant,
        coordinator: VehicleVaultDataCoordinator,
        vehicle_id: str,
    ) -> None:
        """Initialize the image entity."""
        CoordinatorEntity.__init__(self, coordinator)
        ImageEntity.__init__(self, hass)
        self.vehicle_id = vehicle_id
        self._attr_unique_id = f"vehiclevault_{vehicle_id}_photo"
        self._attr_icon = "mdi:car"
        self._attr_image_last_updated = datetime.now()

    @property
    def vehicle(self) -> dict[str, Any]:
        """Return the current vehicle data dictionary."""
        return self.coordinator.data.get(self.vehicle_id, {})

    @property
    def name(self) -> str:
        """Return full friendly name of image entity."""
        v_name = self.vehicle.get("name") or "Vehicle"
        return f"{v_name} Photo"

    @property
    def image_url(self) -> str | None:
        """Return the full URL of the vehicle image."""
        rel_url = self.vehicle.get("image_url") or self.vehicle.get("attributes", {}).get("image_url")
        if not rel_url:
            return None
        if rel_url.startswith("http://") or rel_url.startswith("https://"):
            return rel_url
        return f"{self.coordinator.url}{rel_url}"

    async def async_image(self) -> bytes | None:
        """Return bytes of image."""
        url = self.image_url
        if not url:
            return None
        headers: dict[str, str] = {}
        if self.coordinator.api_key:
            headers["X-API-Key"] = self.coordinator.api_key
            headers["Authorization"] = f"Bearer {self.coordinator.api_key}"
        try:
            resp = await self.coordinator.session.get(url, headers=headers, timeout=10)
            if resp.status == 200:
                self._attr_content_type = resp.headers.get("Content-Type", "image/jpeg")
                return await resp.read()
        except Exception:
            return None
        return None

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information linking image to its vehicle."""
        v = self.vehicle
        v_name = v.get("name") or "Vehicle"
        make = v.get("make") or "VehicleVault"
        model = v.get("model") or "Car"
        plate = v.get("license_plate")

        return DeviceInfo(
            identifiers={(DOMAIN, self.vehicle_id)},
            name=v_name,
            manufacturer=make,
            model=model,
            serial_number=plate or self.vehicle_id,
            suggested_area="Garage",
        )

