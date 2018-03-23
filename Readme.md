# Home Assistant (0.64.3) configuration
This is my [Home Assistant](https://home-assistant.io/) configuration, I'm currently running 0.64.3. It is installed on a Raspberry Pi 3, using the [Hassio Installer](https://home-assistant.io/hassio/), on a 16 GB card. I use a [Smart Things Hub](http://www.samsung.com/uk/smartthings/hub-f-hub-uk-v2/) for both Z-Wave, and Zigbee control.

## On the Pi itself I run

* [Home Assistant](https://home-assistant.io/) with the following addons:
  * [Dropbox Sync](https://github.com/danielwelch/hassio-addons/) to enable me to remote backup my evening snapshots
  * [Duck DNS](https://github.com/hassio-addons/repository/) for enabling external access via a DNS
  * [FireTV Server](http://github.com/gollo/hassio-addons/) for enabling me to add my fire-tv's as media players
  * [Git Pull](https://github.com/vkorn/hassio-addons/) for pulling amends I've made to my git repository, for example anything I ight think of while at work.
  * [Mosquitto Broker](https://github.com/hassio-addons/repository/) MQTT Broker to receive and pass all my mqtt devices into Hass.IO
  * [PS4WakerBridge](https://github.com/vkorn/hassio-addons/) I'm still playing with this, but hoping to link in my PS4 wake-up
  * [SSH server](https://github.com/hassio-addons/repository/) to allow me to ssh into my instance
  * [Samba Share](https://github.com/hassio-addons/repository/) to allow access through samba to files stored on the install
  * [SmartThings Bridge](https://github.com/vkorn/hassio-addons/) links my [SmartThings Hub](http://www.samsung.com/uk/smartthings/hub-f-hub-uk-v2/) into home assistant which allows me to operate all my z-wave and zig-bee devices, this then forwards everything to the MQTT Broker



## The devices, services, and software I use (with HA)

### Hardware Components

* [Samsung SmartThings Hub](http://www.samsung.com/uk/smartthings/hub-f-hub-uk-v2/) linking through:
  * [Fibaro Motion Sensor](https://www.fibaro.com/us/products/motion-sensor/) x2  //TODO locations of items
  * [Fibaro Dimmers](https://www.fibaro.com/us/products/dimmer-2/) x3
  * [Xiaomi Motion Sensor](https://www.gearbest.com/alarm-systems/pp_659226.html) x2
  * [Samsung SmartThings Multi Sensor](http://www.samsung.com/uk/smartthings/sensors-plug-f-mlt-uk-v2/F-MLT-UK-V2/)
  * [Samsung SmartThings Motion Sensor](http://www.samsung.com/uk/smartthings/sensors-plug-f-irm-uk-v2/)
  * [Samsung SmartThings Plug](http://www.samsung.com/uk/smartthings/sensors-plug-f-app-uk-v2/)
* Media
  * TVs - put in Sony model details
  * [Logitech Harmony Ultimate](https://www.logitech.com/en-gb/harmony-universal-remotes)
  * [Sony Playstation 4](https://www.playstation.com/en-gb/explore/ps4/buy-ps4/buy-new-ps4/)
  * [Fire TV Stick](https://www.amazon.co.uk/dp/B01ETRIFOW/ref=asc_df_B01ETRIFOW50970935/?tag=googshopuk-21&creative=22110&creativeASIN=B01ETRIFOW&linkCode=df0&hvadid=205236640281&hvpos=1o3&hvnetw=g&hvrand=15126035685830008529&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=1007009&hvtargid=pla-335245349918&th=1&psc=1) x2
  * [Fire TV 4k](https://www.amazon.co.uk/dp/B06XTWLSRF/ref=asc_df_B06XTWLSRF50970935/?tag=googshopuk-21&creative=22110&creativeASIN=B06XTWLSRF&linkCode=df0&hvadid=218757371956&hvpos=1o1&hvnetw=g&hvrand=15126035685830008529&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=1007009&hvtargid=pla-375613946768&th=1&psc=1)
  * [Broadlink RF Mini](http://www.ibroadlink.com/rmMini3/)
  * [Sonos Play:1](https://www.sonos.com/en-gb/shop/play1.html)
  * [Sonos Play:3](https://www.sonos.com/en-gb/shop/play3.html)
  * [Google Home Mini](https://store.google.com/product/google_home_mini) x4
  * [Google Home](https://store.google.com/product/google_home)
* Lighting
  * [Philips Hue Bridge](https://www.philips.co.uk/c-p/8718696516850/hue-bridge)
  * [Philips Hue Dimmer](https://www.philips.co.uk/c-p/8718696743157/hue-dimmer-switch)
  * [Philips Hue Motion Sensor](https://www.philips.co.uk/c-p/8718696743171/hue-motion-sensor)
  * [Philips Hue Living Colors Iris -LCT010](https://www.philips.co.uk/c-m-li/hue/bulbs/latest#filters=BULBS_SU&sliders=&support=&price=&priceBoxes=&page=&layout=96.subcategory.p-grid-icon) x2
  * [Philips Hue LED White (version2) LWB010](https://www.philips.co.uk/c-m-li/hue/bulbs/latest#filters=BULBS_SU&sliders=&support=&price=&priceBoxes=&page=&layout=96.subcategory.p-grid-icon) x3
  * [Philips Hue Ambiance GU10 spotlight (version 2) LTW013](https://www.philips.co.uk/c-m-li/hue/bulbs/latest#filters=BULBS_SU&sliders=&support=&price=&priceBoxes=&page=&layout=96.subcategory.p-grid-icon) x4
  * [Philips Hue Living Colors E14 LCT015](https://www.philips.co.uk/c-m-li/hue/bulbs/latest#filters=BULBS_SU&sliders=&support=&price=&priceBoxes=&page=&layout=96.subcategory.p-grid-icon) x2
* Security
  * [Nest Cam Outdoor](https://nest.com/uk/cameras/nest-cam-outdoor/overview/)
  * [Hikvision Cube Cameras](http://www.hikvision.com/europe/Products_accessries_761_i33113.html) x4
* Misc
  * [Xiaomi Mi Robot Vacuum](https://www.gearbest.com/robot-vacuum/pp_440546.html)
  * [Nest Thermostat](https://store.nest.com/uk/product/thermostat/T3028GBBI)
  * Raspberry Pi with [Octoprint](https://octoprint.org/) and [Webcam](https://www.logitech.com/en-gb/product/hd-webcam-c270)
  * [Sonoff Basic](https://www.itead.cc/smart-home/sonoff-wifi-wireless-switch.html) x3

### Software Components
* [Bayesian Sensor](https://home-assistant.io/components/binary_sensor.bayesian/)
* [Light Group](https://home-assistant.io/components/light.group/)
* [Google Map Travel Times](https://home-assistant.io/components/sensor.google_travel_time/)
* [Speedtest](https://home-assistant.io/components/sensor.speedtest/)
* [Template Sensor](https://home-assistant.io/components/sensor.template/)
* [Statistic Sensor](https://home-assistant.io/components/sensor.statistics/)
* [Time Sensor](https://home-assistant.io/components/sensor.time_date/)
* [YR Weather Sensor](https://home-assistant.io/components/sensor.yr/)
* [Dark Sky Weather](https://home-assistant.io/components/weather.darksky/)
* [Dark Sky Weather Sensor](https://home-assistant.io/components/sensor.darksky/)
* [Mjpeg Sensor](https://home-assistant.io/components/camera.mjpeg/)
* [Google TTS](https://home-assistant.io/components/tts.google/)
* [OwnTracks](https://home-assistant.io/components/device_tracker.owntracks/)
* [nMap](https://home-assistant.io/components/device_tracker.nmap_tracker/)
* [IFTTT](https://home-assistant.io/components/ifttt/)
* [Octoprint Hub](https://home-assistant.io/components/octoprint/)
* [Octoprint Binary Sensor](https://home-assistant.io/components/binary_sensor.octoprint/)
* [Octoprint Sensor](https://home-assistant.io/components/sensor.octoprint/)
* [Xiamoi Vacuum](https://home-assistant.io/components/vacuum.xiaomi_miio/)
* [Nest Hub](https://home-assistant.io/components/nest/)
* [Nest Binary Sensor](https://home-assistant.io/components/binary_sensor.nest/)
* [Nest Camera](https://home-assistant.io/components/camera.nest/)
* [Nest Sensor](https://home-assistant.io/components/sensor.nest/)
* [Nest Thermostat](https://home-assistant.io/components/climate.nest/)
* [Google Assistant](https://home-assistant.io/components/google_assistant/)
* [Google Calendar](https://home-assistant.io/components/calendar.google/)
* [Philips Hue Bridge](https://home-assistant.io/components/hue/)

### Other software
Software that's run through my server and feeds into the rest of my HA setup
* [Blue Iris](http://blueirissoftware.com/)
* [Plex Media Server](https://www.plex.tv/)
* [Github](https://github.com/)

## Presence detection
Currently I run a Bayesian Sensor that monitors both Owntracks and nMap

## Template sensors


## Automations

## Notes

# Future plans
General I add ideas and plans to the issues tab...However my general goal is to move away from *remote control home* to full automation.  


## Devices

-------------------------------------------------------------------------------------

<del>

### Other software

* [PiVPN](http://www.pivpn.io/) for remote access to my network
* [Pi Hole](https://pi-hole.net/) for blocking those pesky adverts

## Presence detection

## Template sensors

* [Skalavala](https://github.com/skalavala/smarthome) provided a fantastic [template](sensors/zwave_battery_front_door.yaml) that sets the icon for the entity to a representation of the battery level. I use this for all mobile devices, and sensors.
  * ![Screenshot of battery template](https://i.imgur.com/4MnzuLM.png)
* Recycling collection [file and template sensors](sensors/bin.yaml), and [supporting script](local/bin/parse-email)
  * Notifications about upcoming collections are sent by email, the supporting script parses these emails and writes the date of the next collection for each type to it's own file, in JSON formatting
  * A file sensor for each collection type, using the above files
  * A template sensor for each collection type. This tracks whether the collection is two or more days away (future), tomorrow (tomorrow), this morning (today) or past (past). These states are used in automations, and in the HA Dashboard display.

## Automations

* Master and second bedrooms
  * Using the remote with the light strip to control the light, including dimming and colour temperature
  * Dim the light through the night, turning it to lowest brightness and red at midnight
  * Turn the light off if it was left on for half an hour
  * Turn the light on with the alarm
* Front of the house
  * Turn on the light by the house number on at dusk, and at 06:00 (or earlier if we're awake earlier than normal)
  * Turn the light off at sunrise and (just before) midnight
  * Send alerts if we've left the garage doors open for 10 minutes (and nag every 10 minutes)
  * Warn us if an outside door is opened when we're away from home
  * Warn us if the garage doors are opened once we've gone to bed
* Back of the house
  * Turn on the garden lights if the utility door is opened between dusk and dawn (elevation below -5). This temporarily turns off the "off" automations - for 8 seconds (controlled by an input_number)
  * Turn off the garden lights when the utility door is closed
  * Turn off the lights if they're left on and the door is closed
* Lounge
  * Turn on the lights when we come home and it's dark
  * Turn off the lights if we all leave (and the TV is off)
  * Turn on lights as the room gets dark (if we're home, and the TV is on)
  * Turn on the table light if motion is detected in the dark, and turn it off 2 minutes after the last motion detection
  * Mute the TV if the Sonos starts playing, and unmute when it stops
  * Stop the Sonos if the TV is turned on
  * At the end of the night, when the TV has been off for 5 minutes, or the utility door has been shut after the TV is turned off, run the bedtime script (turns of the lights one at a time)
* Hall
  * During Autumn and Winter, turn on the LED lights when the sun is below 5 degrees elevation (and we're home). Our hall is an internal hall with no windows, so it gets dark quickly.
* Home office
  * When I'm working for home, start music at the beginning of the day, and stop it at the end
* People
  * Track when we get up, go to bed, leave, and return, for other automations
  * Notify about commute delays
  * Let the adults know when the other is going to be home
* Misc
  * When battery powered sensors are getting low (25%) warn us so that we know to order a replacement, remind again at 10% and 5%
  * Check the health of the Z-Wave mesh (by looking to see that at least one device has checked in within the last 5 minutes) and run a Heal and Test if necessary
  * Send notifications on startup and shutdown of HA, and when the Z-Wave mesh is ready
  * Notify us about bin collections being due (links in with a green/amber/red Floorplan notification)
* MoreToDo

### Garden lights

This is the most complex of my current automations, to make it "human friendly". The basic logic is that there are automations to turn the light on when the door opens, and off when it closes. To stop that simply having the light on when the door is open, it actually calls a script to turn on the lights. That script turns off the "off" automation temporarily - the duration is determined by the value of `input_number.door_delay` (in seconds).  That means that if we open and close the door (to let the dog out or going out into the garden for some other reason) the lights will stay on when the door closes.  There's another automation (and a template binary sensor) to track if the lights have been left on, and if so to turn them off. That supports a variable delay up to 2 hours, or we can just turn off the automation.

## Notes

* These are (automatically) modified versions of my actual configurations
* My primary goal is to minimise human actions, and where that isn't possible streamline those human actions

# Future plans
A large amount of this will require a rewire of the lighting circuits, so that all the light switches have a neutral wire.

## Devices

* Dimmer modules at most light switches, the exception will be the toilet (since there's a fan linked to it) and the outside light
* Switch modules for the extractor fans
* Multisensors (light/motion/humidity/temperature) in the bedrooms and bathrooms
* Multisensors (light/motion/temperature) in all other rooms
* Lots more door and window sensors, including on the garden gate
* Some form of distance sensor (ultrasonic or laser) in the garage
* BLE beacons
* Digital LED strip for the front of the garage, based upon the [Bruh Automation](https://github.com/bruhautomation/ESP-MQTT-JSON-Digital-LEDs) work
* Analogue LED strips (likely with a Z-Wave controller) for accent lighting and pathway lighting

## Automation thoughts

* Turn on extractor fans when the humidity is more than 5 points above the adjacent room, turning off once they drop to within 5 points
* During darkness, if a bathroom door is opened, turn the bathroom light on at a low level, turning up to medium when the door closes, turning it off when the person leaves
* Turn on the outside front light when the front door opens, the doorbell rings, or somebody is less than 5 minutes away, and coming home
* Other than bedrooms, when the room is in darkness and there's movement turn on the light at a very low level
* During daytime, if the lights are on for *too long* turn them off
* Seasonal use of the digital LED strip
* Flash the relevant section of the LED strip red if the garage door is opening or closing

</del>
# Useful links

* [Home Assistant documentation](https://home-assistant.io/docs/) and [component list](https://home-assistant.io/components/)
