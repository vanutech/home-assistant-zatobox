import logging
from typing import Any, Dict, Optional

from homeassistant import config_entries, core
from homeassistant.const import CONF_ACCESS_TOKEN, CONF_NAME, CONF_PATH, CONF_URL
import homeassistant.helpers.config_validation as cv
import voluptuous as vol

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


ZATOBOX_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_PATH): cv.string,
        vol.Optional(CONF_NAME): cv.string,
        vol.Optional("add_another"): cv.boolean,
    }
)




class ZatoboxConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Github Custom config flow."""

    data: Optional[Dict[str, Any]]

    async def async_step_user(self, user_input: Optional[Dict[str, Any]] = None):
        """Invoked when a user initiates a flow via the user interface."""
        errors: Dict[str, str] = {}

        if user_input is None:
            return self.async_show_form(
                        step_id="setup", data_schema=ZATOBOX_SCHEMA, errors=errors
                    )


        self.data = user_input

        if errors:
            return self.async_show_form(
                        step_id="setup", data_schema=ZATOBOX_SCHEMA, errors=errors
                    )
        
        #create entieties when succes
        return self.async_create_entry(title="Zatobox", data=self.data)
