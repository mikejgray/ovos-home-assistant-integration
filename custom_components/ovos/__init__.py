"""Support for OpenVoiceOS (OVOS) and Neon AI."""
import logging
from typing import Any
from typing import Dict
from typing import Optional

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers import discovery
from homeassistant.helpers.typing import ConfigType
from ovos_bus_client import Message
from ovos_bus_client import MessageBusClient

_LOGGER = logging.getLogger(__name__)
DOMAIN = "ovos"

CONFIG_SCHEMA = vol.Schema(
    {DOMAIN: vol.Schema({vol.Required(CONF_HOST): cv.string})}, extra=vol.ALLOW_EXTRA
)


def generate_message(
    message_type: str, message_data: Optional[Dict[Any, Any]] = None
) -> Message:
    """Generate a message for OVOS."""
    if message_data is None:
        message_data = {}
    message_context = {"source": "Home Assistant", type: message_type}
    return Message(message_type, message_data, message_context)


MUTE_MESSAGE = generate_message("mycroft.volume.mute", {"speak_message": False})
UNMUTE_MESSAGE = generate_message("mycroft.volume.unmute", {"speak_message": False})


def setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the OVOS/Neon component."""

    def handle_mute_mic(_):
        """Handle the service call to mute the OVOS mic."""
        _LOGGER.info("Muting OVOS mic")
        send_ovos_message(MUTE_MESSAGE, "ovos.mic_muted", True)

    def handle_unmute_mic(_):
        """Handle the service call to unmute the OVOS mic."""
        _LOGGER.info("Unmuting OVOS mic")
        send_ovos_message(UNMUTE_MESSAGE, "ovos.mic_muted", False)

    def send_ovos_message(message: Message, state: str, state_value: bool):
        try:
            client = MessageBusClient(
                host=config[DOMAIN][CONF_HOST],
                port=config[DOMAIN].get("ovos_port", 8181),
            )
            client.run_in_thread()
            client.emit(message)
            client.close()
        except ConnectionRefusedError:
            _LOGGER.log(
                level=1, msg="Could not reach this instance of OVOS", exc_info=True
            )
        except ValueError:
            _LOGGER.log(level=1, msg="Error from OVOS messagebus", exc_info=True)
            hass.states.set(state, state_value)
        except Exception as err:  # pylint: disable=broad-except
            _LOGGER.error("Error emitting OVOS message:\n\n%s", exc_info=err)

    # Service registration
    hass.services.register(DOMAIN, "mute_mic", handle_mute_mic)
    hass.services.register(DOMAIN, "unmute_mic", handle_unmute_mic)

    # Standard setup
    hass.data[DOMAIN] = config[DOMAIN][CONF_HOST]
    discovery.load_platform(hass, Platform.NOTIFY, DOMAIN, {}, config)
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up entry."""
    return setup(hass, entry.data.get(DOMAIN) or {})
