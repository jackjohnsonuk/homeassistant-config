import appdaemon.appapi as appapi
##############################################################################################
# Args:
#
# sensor: binary sensor to use as trigger. several motion detectors are seperated with ,
# entity_on : entity to turn on when detecting motion, can be a light, script, scene or anything else that can be turned on. more lights are sepetated with ,
# entity_off : entity to turn off when detecting motion, can be a light, script or anything else that can be turned off. Can also be a scene which will be turned on. more lights are sepetated with ,
# delay: amount of time after turning on to turn off again. If not specified defaults to 60 seconds.
#
# Release Notes
#
# Version 1.1:
#   Added option for several lights, scripts, scenes (Rene Tode)
#   Added option for several motiondetectors (Rene Tode)
#   Added option to just turn out light after timer ended (Rene Tode)
#   Added controle if timer from motionsensor is longer then the delay (Rene Tode)
#   Changed handlenaming bug (Rene Tode)
#   Changed reset flow (Rene Tode)
# Version 1.0:
#   Initial Version (aimc)

class MotionLights(appapi.AppDaemon):

  def initialize(self):

    self.handle = None

    if "sensor" in self.args:
      self.sensors = self.args["sensor"].split(",")
      for sensor in self.sensors:
        self.listen_state(self.motion, sensor)
    else:
      self.log("No sensor specified, doing nothing")

  def motion(self, entity, attribute, old, new, kwargs):
    if "delay" in self.args:
      delay = self.args["delay"]
    else:
      delay = 60

    if new == "on":
      if self.handle == None:
        if "entity_on" in self.args:
          on_entities = self.args["entity_on"].split(",")
          for on_entity in on_entities:
            self.turn_on(on_entity)
          self.log("First motion detected: i turned {} on, and did set timer".format(self.args["entity_on"]))
        else:
          self.log("First motion detected: i turned nothing on, but did set timer")
        self.handle = self.run_in(self.light_off, delay)
      else:
        self.cancel_timer(self.handle)
        self.handle = self.run_in(self.light_off, delay)
        self.log("Motion detected again, i have reset the timer")

  def light_off(self, kwargs):
    motion_still_detected = False
    for sensor in self.sensors:
      if self.get_state(sensor) == "on":
        motion_still_detected = True
    if not motion_still_detected:
      self.handle = None
      if "entity_off" in self.args:
        off_entities = self.args["entity_off"].split(",")
        for off_entity in off_entities:
          # If it's a scene we need to turn it on not off
          device, entity = self.split_entity(off_entity)
          if device == "scene":
            self.log("I activated {}".format(off_entity))
            self.turn_on(off_entity)
          else:
            self.log("I turned {} off".format(off_entity))
            self.turn_off(off_entity)
    else:
      self.log("Timer has Ended, but a motion detector is still on. This shouldnt happen, probably is the delay to short.")
