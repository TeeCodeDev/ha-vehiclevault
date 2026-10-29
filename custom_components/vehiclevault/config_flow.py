"""Config flow for VehicleVault integration."""
from __future__ import annotations

import async_timeout
import logging
from typing import Any

from aiohttp import ClientError
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant, callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import CONF_API_KEY, CONF_SCAN_INTERVAL, CONF_URL, DEFAULT_SCAN_INTERVAL, DOMAIN

_LOGGER = logging.getLogger(__name__)


async def validate_connection(hass: HomeAssistant, url: str, api_key: str | None) -> dict[str, Any]:
    """Test connection to the VehicleVault server."""
    clean_url = url.rstrip("/")
    endpoint = f"{clean_url}/api/integrations/ha/sensors"
    session = async_get_clientsession(hass)

    headers: dict[str, str] = {
        "Accept": "application/json",
        "User-Agent": "HomeAssistant-VehicleVault/1.0",
    }
    if api_key and api_key.strip():
        headers["X-API-Key"] = api_key.strip()
        headers["Authorization"] = f"Bearer {api_key.strip()}"

    try:
        async with async_timeout.timeout(10):
            response = await session.get(endpoint, headers=headers)
            if response.status in (401, 403):
                return {"error": "invalid_auth"}
            if response.status != 200:
                return {"error": "cannot_connect"}
            data = await response.json()
            if not isinstance(data, dict) or "vehicles" not in data:
                return {"error": "invalid_response"}
            return {"data": data}
    except (TimeoutError, ClientError):
        return {"error": "cannot_connect"}
    except Exception:
        return {"error": "unknown"}


class VehicleVaultConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for VehicleVault."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            url = user_input[CONF_URL].strip()
            api_key = user_input.get(CONF_API_KEY, "").strip()

            await self.async_set_unique_id(url.lower())
            self._abort_if_unique_id_configured()

            validation = await validate_connection(self.hass, url, api_key)
            if "error" in validation:
                errors["base"] = validation["error"]
            else:
                data = validation["data"]
                total = len(data.get("vehicles", []))
                title = f"VehicleVault ({total} vehicle{'s' if total != 1 else ''})"
                return self.async_create_entry(
                    title=title,
                    data={
                        CONF_URL: url,
                        CONF_API_KEY: api_key,
                        CONF_SCAN_INTERVAL: DEFAULT_SCAN_INTERVAL,
                    },
                )

        schema = vol.Schema(
            {
                vol.Required(CONF_URL, default="http://homeassistant.local:3084"): str,
                vol.Optional(CONF_API_KEY, default=""): str,
            }
        )

        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> config_entries.OptionsFlow:
        """Get the options flow for this handler."""
        return VehicleVaultOptionsFlowHandler(config_entry)


class VehicleVaultOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle VehicleVault options."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        current_interval = self.config_entry.options.get(
            CONF_SCAN_INTERVAL,
            self.config_entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL),
        )

        options_schema = vol.Schema(
            {
                vol.Optional(
                    CONF_SCAN_INTERVAL,
                    default=current_interval,
                ): vol.All(vol.Coerce(int), vol.Range(min=30, max=3600)),
            }
        )

        return self.async_show_form(step_id="init", data_schema=options_schema)

