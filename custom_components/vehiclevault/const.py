"""Constants for the VehicleVault integration."""

DOMAIN = "vehiclevault"

CONF_URL = "url"
CONF_API_KEY = "api_key"
CONF_SCAN_INTERVAL = "scan_interval"

DEFAULT_NAME = "VehicleVault"
DEFAULT_SCAN_INTERVAL = 300  # 5 minutes in seconds

SENSOR_TYPES = {
    "odometer": {
        "name": "Odometer",
        "icon": "mdi:counter",
        "unit": "km",
        "device_class": "distance",
        "state_class": "total_increasing",
    },
    "apk_expiration_date": {
        "name": "APK Expiration Date",
        "icon": "mdi:calendar-check",
        "device_class": "date",
    },
    "apk_days_remaining": {
        "name": "APK Days Remaining",
        "icon": "mdi:shield-alert",
        "unit": "d",
    },
    "apk_status": {
        "name": "APK Status",
        "icon": "mdi:shield-check",
    },
    "fuel_economy_km_l": {
        "name": "Fuel Economy (km/L)",
        "icon": "mdi:gas-station",
        "unit": "km/L",
    },
    "fuel_consumption_l_100km": {
        "name": "Fuel Consumption (L/100km)",
        "icon": "mdi:gauge",
        "unit": "L/100km",
    },
    "last_refuel_date": {
        "name": "Last Refuel Date",
        "icon": "mdi:calendar",
        "device_class": "date",
    },
    "last_refuel_cost": {
        "name": "Last Refuel Cost",
        "icon": "mdi:cash",
        "unit": "EUR",
        "device_class": "monetary",
    },
    "last_refuel_volume": {
        "name": "Last Refuel Volume",
        "icon": "mdi:fuel",
        "unit": "L",
    },
    "maintenance_alerts": {
        "name": "Maintenance Alerts",
        "icon": "mdi:wrench-alert",
    },
}
