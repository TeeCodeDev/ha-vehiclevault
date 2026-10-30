"""The VehicleVault integration."""
from __future__ import annotations

from datetime import timedelta
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import CONF_API_KEY, CONF_SCAN_INTERVAL, CONF_URL, DEFAULT_SCAN_INTERVAL, DOMAIN
from .coordinator import VehicleVaultDataCoordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR, Platform.IMAGE]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up VehicleVault from a config entry."""
    url: str = entry.data[CONF_URL]
    api_key: str | None = entry.data.get(CONF_API_KEY)

    interval_seconds: int = entry.options.get(
        CONF_SCAN_INTERVAL,
        entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL),
    )

    coordinator = VehicleVaultDataCoordinator(
        hass=hass,
        url=url,
        api_key=api_key,
        update_interval=timedelta(seconds=interval_seconds),
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id, None)

    return unload_ok


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry after options change."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)

