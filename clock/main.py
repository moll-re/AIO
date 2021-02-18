import datetime
import time
import json
from threading import Thread, Timer
import numpy

from clock.api import led


class ClockFace(object):
    """Actual functions one might need for a clock"""

    def __init__(self, text_speed=18, prst=""):
        """"""
        # added by the launcher, we have self.modules (dict)

        self.persistence = prst
        self.IO = led.OutputHandler(32,16)
        self.tspeed = text_speed

        self.output_thread = ""
        # Action the thread is currently performing
        self.output_queue = []
        # Threads to execute next

        self.weather = {"weather":"", "high":"", "low":"", "show":"temps"}
        self.weather_raw = {}
        # different?
        self.brightness_overwrite = {"value" : 1, "duration" : 0}


    def start(self):
        while datetime.datetime.now().strftime("%H%M%S")[-2:] != "00":
            pass
        RepeatedTimer(60, self.clock_loop)


    def clock_loop(self):
        t = int(datetime.datetime.now().strftime("%H%M"))

        if t % 5 == 0:
            # switch secondary face every 5 minutes
            weather = self.modules["bot"].api_weather.show_weather([47.3769, 8.5417]) # zürich

            if weather != self.weather_raw and len(weather) != 0:
                td = weather[1]
                low = td["temps"][0]
                high = td["temps"][1]
                self.weather["weather"] = td["short"]
                self.weather["high"] = high
                self.weather["low"] = low
            elif len(weather) == 0:
                self.weather["weather"] = "error"
                self.weather["high"] = "error"
                self.weather["low"] = "error"
            # if weather == self.weather.raw do nothing

            if self.weather["show"] == "weather":
                next = "temps"
            else:
                next = "weather"
            self.weather["show"] = next

        self.set_face()
    

    def run(self, command, kw=()):
        """Checks for running threads and executes the ones in queue"""
        def enhanced_run(command, kw):
            """"""
            self.output_thread = "Running " + str(command)
            command(*kw)
            self.set_brightness()
            self.output_thread = ""
            if len(self.output_queue) != 0:
                n = self.output_queue.pop(0)
                enhanced_run(n[0],n[1])
            else:
                self.IO.clock_face(self.weather)

        if len(self.output_thread) == 0:
            t = Thread(target=enhanced_run, args=(command, kw))
            t.start()
        else:
            self.output_queue.append([command,kw])


    ############################################################################
    ### basic clock commands
    def set_face(self):
        """"""
        self.run(self.IO.clock_face,(self.weather,))


    def set_brightness(self, overwrite=[],value=-1):
        """Checks, what brightness rules to apply"""

        if value != -1:
            self.IO.output.set_brightness(value)
            return


        if len(overwrite) != 0:
            self.brightness_overwrite = overwrite

        is_WE = datetime.datetime.now().weekday() > 4
        now = int(datetime.datetime.now().strftime("%H%M"))
        if (is_WE and (now > 1000 and now < 2200)) or ((not is_WE) and (now > 800 and now < 2130)):
            brightness = 0.8
        else:
            brightness = 0.01

        self.IO.output.set_brightness(brightness)


    



#######################################################
class RepeatedTimer(object):
  def __init__(self, interval, function, *args, **kwargs):
    self._timer = None
    self.interval = interval
    self.function = function
    self.args = args
    self.kwargs = kwargs
    self.is_running = False
    self.next_call = time.time()
    self.start()

  def _run(self):
    self.is_running = False
    self.start()
    self.function(*self.args, **self.kwargs)

  def start(self):
    if not self.is_running:
      self.next_call += self.interval
      self._timer = Timer(self.next_call - time.time(), self._run)
      self._timer.start()
      self.is_running = True

  def stop(self):
    self._timer.cancel()
    self.is_running = False
