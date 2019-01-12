"""
@ Author      : Suresh Kalavala
@ Date        : 09/14/2017
@ Description : Input Label  - A label that holds data

@ Notes:        Copy this file and services.yaml files and place it in your 
                "Home Assistant Config folder\custom_components\" folder

                To use the component, have the following in your .yaml file:
                The 'value' is optional, by default, it is set to 0 

input_label:
  some_string1:
    name: Some String 1 
    icon: mdi:alphabetical

  input_label:
    name: Some String 2
    value: 'Hello, Home Assistant!'
    icon: mdi:alphabetical

"""

"""
Component to provide input_label.

For more details about this component, please contact Suresh Kalavala
"""
import logging

import voluptuous as vol

import homeassistant.helpers.config_validation as cv
from homeassistant.const import (ATTR_ENTITY_ID, CONF_ICON, CONF_NAME)
from homeassistant.core import callback
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.entity_component import EntityComponent
from homeassistant.loader import bind_hass
from homeassistant.helpers.entity import ToggleEntity
from homeassistant.helpers.restore_state import RestoreEntity

DOMAIN = 'input_label'

ENTITY_ID_FORMAT = DOMAIN + '.{}'

_LOGGER = logging.getLogger(__name__)

ATTR_VALUE   = "value"
DEFAULT_VALUE = "not set"

DEFAULT_ICON = "mdi:label"

SERVICE_SETNAME  = 'set_name'
SERVICE_SETVALUE = 'set_value'
SERVICE_SETICON  = 'set_icon'

SERVICE_SCHEMA = vol.Schema({
    vol.Optional(ATTR_ENTITY_ID): cv.entity_ids,
    vol.Optional(ATTR_VALUE): cv.string,
    vol.Optional(CONF_NAME): cv.icon,
    vol.Optional(CONF_ICON): cv.icon,
})

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        cv.slug: vol.Any({
            vol.Optional(CONF_ICON, default=DEFAULT_ICON): cv.icon,
            vol.Optional(ATTR_VALUE, default=DEFAULT_VALUE): cv.string,
            vol.Optional(CONF_NAME): cv.string,
        }, None)
    })
}, extra=vol.ALLOW_EXTRA)

async def async_setup(hass, config):
    """Set up a input_label."""
    component = EntityComponent(_LOGGER, DOMAIN, hass)

    entities = []

    for object_id, cfg in config[DOMAIN].items():
        if not cfg:
            cfg = {}

        name = cfg.get(CONF_NAME)
        value = cfg.get(ATTR_VALUE)
        icon = cfg.get(CONF_ICON)

        entities.append(LabelData(object_id, name, value, icon))

    if not entities:
        return False

    component.async_register_entity_service(
        SERVICE_SETNAME, SERVICE_SCHEMA,
        'async_set_name'
    )

    component.async_register_entity_service(
        SERVICE_SETVALUE, SERVICE_SCHEMA,
        'async_set_value'
    )

    component.async_register_entity_service(
        SERVICE_SETICON, SERVICE_SCHEMA,
        'async_set_icon'
    )

    await component.async_add_entities(entities)
    return True

class LabelData(RestoreEntity):
    """Representation of a input_label."""

    def __init__(self, object_id, name, value, icon):
        """Initialize a input_label."""
        self.entity_id = ENTITY_ID_FORMAT.format(object_id)
        self._name = name
        self._state = value
        self._icon = icon
 
    @property
    def should_poll(self):
        """If entity should be polled."""
        return False

    @property
    def name(self):
        """Return name of the input_label."""
        return self._name

    @property
    def icon(self):
        """Return the icon to be used for this entity."""
        return self._icon

    @property
    def state(self):
        """Return the current value of the input_label."""
        return self._state

    @property
    def state_attributes(self):
        """Return the state attributes."""
        return {
            ATTR_VALUE: self._state,
        }

    async def async_added_to_hass(self):
        """Call when entity about to be added to Home Assistant."""
        # If not None, we got an initial value.
        await super().async_added_to_hass()
        if self._state is not None:
            return

        state = await self.async_get_last_state()
        self._state = state and state.state == state

    async def async_set_name(self, name):
        self._name = name
        await self.async_update_ha_state()

    async def async_set_icon(self, icon):
        self._icon = icon
        await self.async_update_ha_state()

    async def async_set_value(self, value):
        self._state = value
        await self.async_update_ha_state()
