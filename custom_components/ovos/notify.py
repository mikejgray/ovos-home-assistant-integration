"""OpenVoiceOS (OVOS) and Neon AI notification platform."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.notify import BaseNotificationService
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType
from homeassistant.helpers.typing import DiscoveryInfoType
from ovos_bus_client import Message
from ovos_bus_client import MessageBusClient

_LOGGER = logging.getLogger(__name__)


def get_service(
    hass: HomeAssistant,
    config: ConfigType,
    discovery_info: DiscoveryInfoType | None = None,
) -> OvosNotificationService:
    """Get the OVOS notification service."""
    return OvosNotificationService(hass.data["ovos"])


class OvosNotificationService(BaseNotificationService):
    """The OVOS Notification Service."""

    def __init__(self, ovos_ip: str, ovos_port: int = 8181, **kwargs) -> None:
        """Initialize the service."""
        self.ovos_ip = ovos_ip
        self.ovos_port = ovos_port

    def send_message(
        self, message: str = "", lang: str = "en-us", **kwargs: Any
    ) -> None:
        """Send a message to OVOS/Neon to speak on instance."""
        try:
            _LOGGER.log(level=3, msg=kwargs)
            client = MessageBusClient(host=self.ovos_ip, port=self.ovos_port)
            client.run_in_thread()
            client.emit(Message("speak", {"utterance": message, "lang": lang}))
            client.close()
        except ConnectionRefusedError:
            _LOGGER.log(
                level=1, msg="Could not reach this instance of OVOS", exc_info=True
            )
        except ValueError:
            _LOGGER.log(level=1, msg="Error from OVOS messagebus", exc_info=True)

    def authenticate(self):
        """Authenticate with OVOS/Neon instance."""
        return True
