"""Sensor platform for VehicleVault."""
from __future__ import annotations

from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfLength
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
    """Set up VehicleVault sensors based on a config entry."""
    coordinator: VehicleVaultDataCoordinator = hass.data[DOMAIN][entry.entry_id]

    entities: list[VehicleVaultSensor] = []

    # Iterate over active vehicles and build sensors
    for vehicle_id, vehicle in coordinator.data.items():
        # 1. Odometer
        entities.append(
            VehicleVaultSensor(
                coordinator=coordinator,
                vehicle_id=vehicle_id,
                sensor_type="odometer",
                name="Kilometerstand",
                icon="mdi:counter",
                native_unit=UnitOfLength.KILOMETERS,
                device_class=SensorDeviceClass.DISTANCE,
                state_class=SensorStateClass.TOTAL_INCREASING,
                value_fn=lambda v: v.get("odometer"),
            )
        )

        # 2. APK Expiration Date
        entities.append(
            VehicleVaultSensor(
                coordinator=coordinator,
                vehicle_id=vehicle_id,
                sensor_type="apk_date",
                name="APK Vervaldatum",
                icon="mdi:calendar-check",
                device_class=SensorDeviceClass.DATE,
                value_fn=lambda v: v.get("apk", {}).get("expiration_date"),
            )
        )

        # 3. APK Days Remaining
        entities.append(
            VehicleVaultSensor(
                coordinator=coordinator,
                vehicle_id=vehicle_id,
                sensor_type="apk_days",
                name="APK Dagen Resterend",
                icon="mdi:shield-alert",
                native_unit="d",
                value_fn=lambda v: v.get("apk", {}).get("days_remaining"),
                attrs_fn=lambda v: {
                    "apk_status": v.get("apk", {}).get("status"),
                    "vervaldatum": v.get("apk", {}).get("expiration_date"),
                },
            )
        )

        # 4. APK Status
        entities.append(
            VehicleVaultSensor(
                coordinator=coordinator,
                vehicle_id=vehicle_id,
                sensor_type="apk_status",
                name="APK Status",
                icon="mdi:shield-check",
                value_fn=lambda v: v.get("apk", {}).get("status"),
            )
        )

        # 5. Consumption km/L
        entities.append(
            VehicleVaultSensor(
                coordinator=coordinator,
                vehicle_id=vehicle_id,
                sensor_type="consumption_km_per_l",
                name="Verbruik (km/L)",
                icon="mdi:gas-station",
                native_unit="km/L",
                state_class=SensorStateClass.MEASUREMENT,
                value_fn=lambda v: v.get("fuel_stats", {}).get("consumption_km_per_liter"),
            )
        )

        # 6. Consumption L/100km
        entities.append(
            VehicleVaultSensor(
                coordinator=coordinator,
                vehicle_id=vehicle_id,
                sensor_type="consumption_l_100km",
                name="Verbruik (L/100km)",
                icon="mdi:gauge",
                native_unit="L/100km",
                state_class=SensorStateClass.MEASUREMENT,
                value_fn=lambda v: v.get("fuel_stats", {}).get("consumption_l_per_100km"),
            )
        )

        # 7. Last Fuel Date
        entities.append(
            VehicleVaultSensor(
                coordinator=coordinator,
                vehicle_id=vehicle_id,
                sensor_type="last_fuel_date",
                name="Laatste Tankbeurt",
                icon="mdi:calendar",
                device_class=SensorDeviceClass.DATE,
                value_fn=lambda v: v.get("fuel_stats", {}).get("last_fuel_date"),
            )
        )

        # 8. Last Fuel Cost
        entities.append(
            VehicleVaultSensor(
                coordinator=coordinator,
                vehicle_id=vehicle_id,
                sensor_type="last_fuel_cost",
                name="Laatste Tankkosten",
                icon="mdi:cash",
                native_unit="EUR",
                device_class=SensorDeviceClass.MONETARY,
                value_fn=lambda v: v.get("fuel_stats", {}).get("last_fuel_cost"),
            )
        )

        # 9. Last Fuel Volume
        entities.append(
            VehicleVaultSensor(
                coordinator=coordinator,
                vehicle_id=vehicle_id,
                sensor_type="last_fuel_volume",
                name="Laatst Getankt Volume",
                icon="mdi:fuel",
                native_unit="L",
                value_fn=lambda v: v.get("fuel_stats", {}).get("last_fuel_liters") or v.get("fuel_stats", {}).get("last_kwh"),
                attrs_fn=lambda v: {
                    "station_name": v.get("fuel_stats", {}).get("last_station_name"),
                    "price_per_liter": v.get("fuel_stats", {}).get("last_fuel_price_per_liter"),
                    "energy_type": v.get("fuel_stats", {}).get("last_energy_type"),
                    "kwh": v.get("fuel_stats", {}).get("last_kwh"),
                },
            )
        )

        # 10. Maintenance Alerts
        entities.append(
            VehicleVaultSensor(
                coordinator=coordinator,
                vehicle_id=vehicle_id,
                sensor_type="maintenance_alerts",
                name="Onderhoudsmeldingen",
                icon="mdi:wrench-alert",
                value_fn=lambda v: v.get("maintenance", {}).get("alerts_count", 0),
                attrs_fn=lambda v: {
                    "alerts": v.get("maintenance", {}).get("alerts", []),
                },
            )
        )

    async_add_entities(entities)


class VehicleVaultSensor(CoordinatorEntity[VehicleVaultDataCoordinator], SensorEntity):
    """Representation of a VehicleVault sensor entity."""

    def __init__(
        self,
        coordinator: VehicleVaultDataCoordinator,
        vehicle_id: str,
        sensor_type: str,
        name: str,
        icon: str | None = None,
        native_unit: str | None = None,
        device_class: SensorDeviceClass | None = None,
        state_class: SensorStateClass | None = None,
        value_fn: Any = None,
        attrs_fn: Any = None,
    ) -> None:
        """Initialize the sensor entity."""
        super().__init__(coordinator)
        self.vehicle_id = vehicle_id
        self.sensor_type = sensor_type
        self._attr_name_suffix = name
        self._attr_icon = icon
        self._attr_native_unit_of_measurement = native_unit
        self._attr_device_class = device_class
        self._attr_state_class = state_class
        self._value_fn = value_fn
        self._attrs_fn = attrs_fn

        self._attr_unique_id = f"vehiclevault_{vehicle_id}_{sensor_type}"

    @property
    def vehicle(self) -> dict[str, Any]:
        """Return the current vehicle data dictionary."""
        return self.coordinator.data.get(self.vehicle_id, {})

    @property
    def name(self) -> str:
        """Return full friendly name of sensor."""
        v_name = self.vehicle.get("name") or "Voertuig"
        return f"{v_name} {self._attr_name_suffix}"

    @property
    def native_value(self) -> Any:
        """Return the current sensor value."""
        if self._value_fn:
            return self._value_fn(self.vehicle)
        return None

    @property
    def extra_state_attributes(self) -> dict[str, Any] | None:
        """Return additional attributes."""
        if self._attrs_fn:
            return self._attrs_fn(self.vehicle)
        return None

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information linking sensor to its vehicle."""
        v = self.vehicle
        v_name = v.get("name") or "Voertuig"
        make = v.get("make") or "VehicleVault"
        model = v.get("model") or "Auto"
        plate = v.get("license_plate")

        return DeviceInfo(
            identifiers={(DOMAIN, self.vehicle_id)},
            name=v_name,
            manufacturer=make,
            model=model,
            serial_number=plate or self.vehicle_id,
            suggested_area="Garage",
        )
