"""
Update your custom_cards.

For more details about this component, please refer to the documentation at
https://github.com/custom-components/custom_cards
"""
import logging
import os
import subprocess
from datetime import timedelta

import requests
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.event import track_time_interval
from homeassistant.helpers.discovery import load_platform
from homeassistant.helpers.dispatcher import async_dispatcher_send

__version__ = '1.1.10'

DOMAIN = 'custom_cards'
DATA_CC = 'custom_cards_data'
CONF_HIDE_SENSOR = 'hide_sensor'
SIGNAL_SENSOR_UPDATE = 'custom_cards_update'

ATTR_CARD = 'card'

INTERVAL = timedelta(days=1)

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Optional(CONF_HIDE_SENSOR, default=False): cv.boolean,
    })
}, extra=vol.ALLOW_EXTRA)

_LOGGER = logging.getLogger(__name__)

BROWSE_REPO = 'https//github.com/ciotlosm/custom-lovelace/master/'
BASE_REPO = 'https://raw.githubusercontent.com/ciotlosm/custom-lovelace/master/'
SENSOR_URL = 'https://raw.githubusercontent.com/custom-components/sensor.custom_cards/master/custom_components/sensor/custom_cards.py'

def setup(hass, config):
    """Set up the component."""
    _LOGGER.info('version %s is starting, if you have ANY issues with this, please report \
                  them here: https://github.com/custom-components/%s',
                 __version__, __name__.split('.')[1])
    conf_dir = str(hass.config.path())
    controller = CustomCards(hass, conf_dir)
    hide_sensor = config[DOMAIN][CONF_HIDE_SENSOR]

    def update_cards_service(call):
        """Set up service for manual trigger."""
        controller.update_cards()

    def update_card_service(call):
        """Set up service for manual trigger."""
        controller.update_card(call.data.get(ATTR_CARD))

    track_time_interval(hass, controller.cache_versions, INTERVAL)
    hass.services.register(
        DOMAIN, 'update_cards', update_cards_service)
    hass.services.register(
        DOMAIN, 'update_card', update_card_service)
    hass.services.register(
        DOMAIN, 'check_versions', controller.cache_versions)
    if not hide_sensor:
        sensor_dir = str(hass.config.path("custom_components/sensor/"))
        sensor_file = 'custom_cards.py'
        sensor_full_path = sensor_dir + sensor_file
        if not os.path.isfile(sensor_full_path):
            _LOGGER.debug('Could not find %s in %s, trying to download.', sensor_file, sensor_dir)
            response = requests.get(SENSOR_URL)
            if response.status_code == 200:
                _LOGGER.debug('Checking folder structure')
                directory = os.path.dirname(sensor_dir)
                if not os.path.exists(directory):
                    os.makedirs(directory)
                with open(sensor_full_path, 'wb+') as sensorfile:
                    sensorfile.write(response.content)
            else:
                _LOGGER.critical('Failed to download sensor from %s', SENSOR_URL)
        load_platform(hass, 'sensor', DOMAIN)
    return True


class CustomCards:
    """Custom cards controller."""
    def __init__(self, hass, conf_dir):
        self.hass = hass
        self.conf_dir = conf_dir
        self.cards = None
        self.hass.data[DATA_CC] = {}
        self.cache_versions(None) # Force a cache update on startup

    def cache_versions(self, time):
        """Cache"""
        self.cards = self.get_installed_cards()
        self.hass.data[DATA_CC] = {} # Empty list to start from scratch
        if self.cards:
            for card in self.cards:
                localversion = self.get_local_version(card[0])
                remoteversion = self.get_remote_version(card[0])
                has_update = (localversion != False and remoteversion != False and remoteversion != localversion)
                self.hass.data[DATA_CC][card[0]] = {
                    "local": localversion,
                    "remote": remoteversion,
                    "has_update": has_update,
                }
                async_dispatcher_send(self.hass, SIGNAL_SENSOR_UPDATE)

    def update_cards(self):
        """Update all cards"""
        for card in self.cards:
            if self.hass.data[DATA_CC][card[0]]['has_update']:
                self.update_card(card[0], card[1])
            else:
                _LOGGER.debug('Skipping upgrade for %s, no update available', card[0])

    def update_card(self, card, card_dir=None):
        """Update one cards"""
        if not card_dir:
            card_dir = self.get_card_dir(card)
        if card in self.hass.data[DATA_CC]:
            if self.hass.data[DATA_CC][card]['has_update']:
                self.download_card(card, card_dir)
                self.update_resource_version(card)
                _LOGGER.info('Upgrade of %s from version %s to version %s complete', card, self.hass.data[DATA_CC][card]['local'], self.hass.data[DATA_CC][card]['remote'])
                self.hass.data[DATA_CC][card]['local'] = self.hass.data[DATA_CC][card]['remote']
                self.hass.data[DATA_CC][card]['has_update'] = False
                async_dispatcher_send(self.hass, SIGNAL_SENSOR_UPDATE)
            else:
                _LOGGER.debug('Skipping upgrade for %s, no update available', card)
        else:
            _LOGGER.error('Upgrade failed, no valid card specified %s', card)

    def download_card(self, card, card_dir):
        """Downloading new card"""
        _LOGGER.debug('Downloading new version of %s', card)
        downloadurl = BASE_REPO + card + '/' + card + '.js'
        response = requests.get(downloadurl)
        if response.status_code == 200:
            with open(self.conf_dir + card_dir + card + '.js', 'wb') as card_file:
                card_file.write(response.content)

    def update_resource_version(self, card):
        """Updating the ui-lovelace file"""
        localversion = self.hass.data[DATA_CC][card]['local']
        remoteversion = self.hass.data[DATA_CC][card]['remote']
        _LOGGER.debug('Updating configuration for %s', card)
        sedcmd = 's/\/'+ card + '.js?v=' + str(localversion) + '/\/'+ card + '.js?v=' + str(remoteversion) + '/'
        _LOGGER.debug('Upgrading card in config from version %s to version %s', localversion, remoteversion)
        subprocess.call(["sed", "-i", "-e", sedcmd, self.conf_dir + '/ui-lovelace.yaml'])
        _LOGGER.debug("sed -i -e %s %s ", sedcmd, self.conf_dir + '/ui-lovelace.yaml')

    def get_installed_cards(self):
        """Get all cards in use from the www dir"""
        _LOGGER.debug('Checking for installed cards in  %s/www', self.conf_dir)
        cards = []
        cards_in_use = []
        for filenames in os.walk(self.conf_dir + '/www'):
            for file in filenames[2]:
                _LOGGER.debug(file)
                if file.endswith(".js"):
                    cards.append(file.split('.')[0])
        if len(cards):
            _LOGGER.debug('Checking which cards that are in use in ui-lovelace.yaml')
            for card in cards:
                with open(self.conf_dir + '/ui-lovelace.yaml', 'r') as local:
                    for line in local.readlines():
                        if '/' + card + '.js' in line:
                            card_dir = self.get_card_dir(card)
                            cards_in_use.append([card, card_dir])
                            break
            _LOGGER.debug('These cards where found: %s', cards_in_use)
        else:
            _LOGGER.debug('No cards where found. %s', cards)
            cards_in_use = None
        return cards_in_use

    def get_card_dir(self, card):
        """Get card dir"""
        with open(self.conf_dir + '/ui-lovelace.yaml', 'r') as local:
            for line in local.readlines():
                if '/' + card + '.js' in line:
                    card_dir = line.split(': ')[1].split(card)[0].replace("local", "www")
                    break
        return card_dir

    def get_remote_version(self, card):
        """Return the remote version if any."""
        remoteversion = BASE_REPO + card + '/VERSION'
        response = requests.get(remoteversion)
        if response.status_code == 200:
            remoteversion = response.text.strip()
            _LOGGER.debug('Remote version of %s is %s', card, remoteversion)
        else:
            _LOGGER.debug('Could not get the remote version for %s', card)
            remoteversion = False
        return remoteversion

    def get_local_version(self, card):
        """Return the local version if any."""
        cardconfig = ''
        with open(self.conf_dir + '/ui-lovelace.yaml', 'r') as local:
            for line in local.readlines():
                if '/' + card + '.js' in line:
                    cardconfig = line
                    break
        if '=' in cardconfig:
            localversion = cardconfig.split('=')[1].split('\n')[0]
            _LOGGER.debug('Local version of %s is %s', card, localversion)
            return localversion
        _LOGGER.debug('Could not get the local version for %s', card)
        return False