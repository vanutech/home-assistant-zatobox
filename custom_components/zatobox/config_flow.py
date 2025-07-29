


import logging
from typing import Any, Dict, Optional

from homeassistant import config_entries, core
from homeassistant.const import CONF_ACCESS_TOKEN, CONF_NAME, CONF_PATH, CONF_URL
import homeassistant.helpers.config_validation as cv

from homeassistant.data_entry_flow import FlowResult

from homeassistant.components.zeroconf import ZeroconfServiceInfo

import voluptuous as vol

from .const import  DOMAIN, CONF_HOSTNAME

from homeassistant.const import (
    CONF_HOST,
    CONF_NAME,
    CONF_PASSWORD,
    CONF_PORT,
    CONF_SCAN_INTERVAL,
    UnitOfTemperature,
)

_LOGGER: logging.Logger = logging.getLogger(__package__)




class ZatoboxConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Github Custom config flow."""
    
    data: Optional[Dict[str, Any]]
    
    def __init__(self) -> None:
        """Initialize the wiser flow."""
        self.discovery_info = {}
        

    async def async_step_user(self, user_input: Optional[Dict[str, Any]] = None):
        """Invoked when a user initiates a flow via the user interface."""
        errors: Dict[str, str] = {}



        if user_input is not None:
            self.data = user_input

            if not errors:
                _LOGGER.debug("Creating entity")
                # Create entities when successful
                return self.async_create_entry(title="Zatobox", data=self.data)
            

        self._discovered_devices = []
        # Create a list of options for each discovered device
        options = {device["name"]: device["name"] for device in self._discovered_devices}

        _LOGGER.debug(options)


        _LOGGER.debug("Showing user form")
        # Return a form to select devices
        return self.async_show_form(
            step_id="select_devices",
            data_schema=vol.Schema({
                vol.Optional("devices", default=[]): cv.multi_select(options)
            })
        )


    #zeroconf example from
    #https://github.com/asantaga/wiserHomeAssistantPlatform/blob/master/custom_components/wiser/config_flow.py#L170
    async def async_step_zeroconf(
        self, discovery_info: ZeroconfServiceInfo
    ) -> FlowResult:
        """Handle zeroconf discovery."""
        

        _LOGGER.debug(discovery_info.name)

        host = discovery_info.host
        port = discovery_info.port
        zctype = discovery_info.type
        name = discovery_info.name.replace(f".{zctype}", "")

        await self.async_set_unique_id(name)
        self._abort_if_unique_id_configured()

        self.context.update({"title_placeholders": {"name": name}})

        self.discovery_info.update(
            {
                CONF_HOST: host,
                CONF_PORT: port,
                CONF_HOSTNAME: discovery_info.hostname.replace(".local.", ".local"),
                CONF_NAME: name,
            }
        )
        return await self.async_step_zeroconf_confirm()

    async def async_step_zeroconf_confirm(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle a confirmation flow initiated by zeroconf."""
        errors = {}
        if user_input is not None:

            _LOGGER.debug(user_input)
            # Create entities when successful
            return self.async_create_entry(title="Zatobox", data=user_input)

        return self.async_show_form(
            step_id="zeroconf_confirm",
            description_placeholders={
                "name": self.discovery_info[CONF_NAME],
                "hostname": self.discovery_info[CONF_HOSTNAME],
                "ip_address": self.discovery_info[CONF_HOST],
                "port": self.discovery_info[CONF_PORT],
            },
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_NAME, default=self.discovery_info[CONF_NAME]
                    ): str,
                    vol.Optional(
                        CONF_HOST, default=self.discovery_info[CONF_HOST]
                    ): str
                }
            ),
            errors=errors,
        )


