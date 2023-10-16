"""Config flow for OVOS integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError

from .const import DOMAIN
from .notify import OvosNotificationService

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required("host"): str,
        vol.Required("name"): str,
        vol.Optional("ovos_port", default=8181): int,
    }
)


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect.

    Data has the keys from STEP_USER_DATA_SCHEMA with values provided by the user.
    """
    try:
        hub: Any = await hass.async_add_executor_job(
            OvosNotificationService(data["host"], data["ovos_port"]).authenticate
        )
        if not await hub.authenticate():
            raise InvalidAuth
    except Exception as exc:  # pylint: disable=broad-except
        raise CannotConnect() from exc

    # Return info that you want to store in the config entry.
    return {"host": hub.ovos_ip, "ovos_port": hub.ovos_port}


class OvosConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for OVOS."""

    VERSION = 1

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize."""
        self.config_entry = config_entry
        self.options = dict(config_entry.options) if config_entry else {}

    async def async_step_device(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}
        if user_input is not None:
            try:
                await validate_input(self.hass, user_input)
                await self.async_set_unique_id(user_input["name"])
                self._abort_if_unique_id_configured()
                self.options.update(user_input)
                # return self.async_create_entry(title="", data=self.options)
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except InvalidAuth:
                errors["base"] = "invalid_auth"
            except Exception as err:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception:\n\n%s", err)
                errors["base"] = "unknown"
        else:
            return self.async_show_form(
                step_id="device", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
            )


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""
