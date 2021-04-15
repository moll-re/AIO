import datetime
import time
from threading import Thread
import numpy

from . import hardware, helpers


class ClockFace:
    """Actual functions one might need for a clock"""

    def __init__(self, text_speed=18, prst=object):
        """"""
        # added by the launcher, we have self.modules (dict)

        # hard coded, but can be changed to taste
        self.tspeed = text_speed
        self.primary = [200, 200, 200]
        self.secondary = [10, 200, 10]
        self.error = [200, 10, 10]
        
        self.persistence = prst
        self.IO = hardware.led.get_handler()
        self.shape = self.IO.shape # (16,32) for now
        self.MOP = helpers.helper.MatrixOperations(self.shape, default_colors={"primary": self.primary, "secondary": self.secondary, "error": self.error})
        
        self.output_thread = ""
        # Action the thread is currently performing
        self.output_queue = []
        # Threads to execute next

        self.weather = {"weather":"", "high":"", "low":"", "show":"temps"}
        self.weather_raw = {}

        self.brightness = 1
        self.brightness_overwrite = {"value" : 1, "duration" : 0}


    def start(self):
        self.clock_loop()
        while datetime.datetime.now().strftime("%H%M%S")[-2:] != "00":
            pass
        helpers.timer.RepeatedTimer(60, self.clock_loop)
        self.clock_loop()


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

        self.run(self.set_face,())
    

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
                self.set_face()

        if len(self.output_thread) == 0:
            t = Thread(target=enhanced_run, args=(command, kw))
            t.start()
        else:
            self.output_queue.append([command,kw])


    ############################################################################
    ### basic clock commands
    def set_face(self):
        """Set the clock face (time + weather) by getting updated info - gets called every minute"""
        face = self.MOP.clock_face(self.weather)
        self.IO.put(face * self.brightness)


    def set_brightness(self, value=-1, overwrite=[]):
        """Checks, what brightness rules to apply"""

        if value != -1:
            self.brightness = value
            return

        if len(overwrite) != 0:
            self.brightness_overwrite = overwrite

        is_WE = datetime.datetime.now().weekday() > 4
        now = int(datetime.datetime.now().strftime("%H%M"))
        if (is_WE and (now > 1000 and now < 2200)) or ((not is_WE) and (now > 800 and now < 2130)):
            brightness = 0.8
        else:
            brightness = 0.01

        self.brightness = brightness


    def text_scroll(self, text, color=[[200,200,200]]):
        pixels = self.MOP.text_converter(text, 12, color)
        sleep_time = 1 / self.tspeed
        width = self.shape[1]
        frames = pixels.shape[1] - width
        if frames <= 0:
            frames = 1

        for i in range(frames):
            visible = pixels[:,i:width+i]
            self.IO.put(visible*self.brightness)
            time.sleep(sleep_time)
        time.sleep(10 * sleep_time)

