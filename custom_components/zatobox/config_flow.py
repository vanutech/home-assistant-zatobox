import logging
from typing import Any, Dict, Optional

from homeassistant import config_entries, core
from homeassistant.const import CONF_ACCESS_TOKEN, CONF_NAME, CONF_PATH, CONF_URL
import homeassistant.helpers.config_validation as cv
import voluptuous as vol

from .const import DOMAIN

_LOGGER: logging.Logger = logging.getLogger(__package__)

import sys


ZATOBOX_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_PATH): cv.string,
        vol.Optional(CONF_NAME): cv.string,
    }
)


from  python_zatobox.vanubus import Vanubus, discover_zt_devices

class ZatoboxConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Github Custom config flow."""

    data: Optional[Dict[str, Any]]

    async def async_step_user(self, user_input: Optional[Dict[str, Any]] = None):
        """Invoked when a user initiates a flow via the user interface."""
        errors: Dict[str, str] = {}


        # Get the Python version
        python_version = sys.version

        _LOGGER.debug(f"Python version {python_version}")
        options = {}
        if user_input is not None:
            self.data = user_input

            if not errors:
                _LOGGER.debug("Creating entity")
                # Create entities when successful
                return self.async_create_entry(title="Zatobox", data=self.data)
            
        else:
            discovered_devices = discover_zt_devices()

            # Create a list of options for each discovered device
            options = {device["name"]: device["name"] for device in discovered_devices}

            # Store the discovered devices in the flow context
            self.context["discovered_devices"] = discovered_devices
            

        _LOGGER.debug("Showing user form")
        # Return a form to select devices
        return self.async_show_form(
            step_id="select_devices",
            data_schema=vol.Schema({
                vol.Optional("devices", default=[]): cv.multi_select(options)
            })
        )

