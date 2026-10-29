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
    "apk_date": {
        "name": "APK Expiration Date",
        "icon": "mdi:calendar-check",
        "device_class": "date",
    },
    "apk_days": {
        "name": "APK Days Remaining",
        "icon": "mdi:shield-alert",
        "unit": "d",
    },
    "apk_status": {
        "name": "APK Status",
        "icon": "mdi:shield-check",
    },
    "consumption_km_per_l": {
        "name": "Fuel Economy (km/L)",
        "icon": "mdi:gas-station",
        "unit": "km/L",
    },
    "consumption_l_100km": {
        "name": "Fuel Consumption (L/100km)",
        "icon": "mdi:gauge",
        "unit": "L/100km",
    },
    "last_fuel_date": {
        "name": "Last Fill-up Date",
        "icon": "mdi:calendar",
        "device_class": "date",
    },
    "last_fuel_cost": {
        "name": "Last Fill-up Cost",
        "icon": "mdi:cash",
        "unit": "EUR",
        "device_class": "monetary",
    },
    "last_fuel_liters": {
        "name": "Last Fill-up Volume",
        "icon": "mdi:fuel",
        "unit": "L",
    },
    "maintenance_alerts": {
        "name": "Maintenance Alerts",
        "icon": "mdi:wrench-alert",
    },
}
