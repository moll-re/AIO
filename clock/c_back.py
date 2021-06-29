import numpy as np
import datetime

from . import helpers

class ClockBackend:
    """Heavy lifting of matrix operations"""
    def __init__(self):
        self.MOP = helpers.computations.MatrixOperations()

        self.weather = {"weather":"", "high":"", "low":""}
        self.weather_raw = {}
        self.weather_face_swap = False

        self.brightness = 1
        self.brightness_overwrite = {"value" : 1, "duration" : 0}


    def start(self):
        self.out = self.modules["broadcast"]
        helpers.timer.RepeatedTimer(15, self.clock_loop)


    
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
            self.weather_face_swap = not self.weather_face_swap

        self.send_face()




    def send_face(self):
        """Set the clock face (time + weather) by getting updated info - gets called every minute"""
        matrices = self.MOP.clock_face(self.weather)
        if self.weather_face_swap:
            matrices = [matrices[0], matrices[2], matrices[1]]

        # apply brightness
        b = self.get_brightness()
        matrices = [(b * m).tolist() for m in matrices]
        self.out.queue.append({"matrices" : matrices})


    def get_brightness(self):
        """Checks, what brightness rules to apply"""

        is_WE = datetime.datetime.now().weekday() > 4
        now = int(datetime.datetime.now().strftime("%H%M"))
        if (is_WE and (now > 1000 and now < 2200)) or ((not is_WE) and (now > 800 and now < 2130)):
            brightness = 0.8
        else:
            brightness = 0.01

        return brightness


    # def text_scroll(self, text, color=[[200,200,200]]):
    #     pixels = self.MOP.text_converter(text, 12, color)
    #     sleep_time = 1 / self.tspeed
    #     width = self.shape[1]
    #     frames = pixels.shape[1] - width
    #     if frames <= 0:
    #         frames = 1

    #     for i in range(frames):
    #         visible = pixels[:,i:width+i]
    #         self.IO.put(visible*self.brightness)
    #         time.sleep(sleep_time)
    #     time.sleep(10 * sleep_time)


