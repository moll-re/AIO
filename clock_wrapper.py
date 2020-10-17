import time
import datetime
from threading import Thread

import clock.main
import bot.main

class ModuleWrapper():
    """Wrapper for the CLOCK-functionality"""
    def __init__(self):
        """"""
        print("Initializing clock-functionality")
        self.clock = clock.main.ClockFace()
        self.bot = bot.main.ChatBot("Clockbot","1.1",{})
        self.time_thread = Thread(target=self.mainloop)
        self.time_thread.start()
        self.weather = ""
        self.categories = categories = {
            "cloud": "cloud",
            "cloud_with_rain": "rain and cloud",
            "thunder_cloud_rain": "thunder and cloud",
            "droplet": "rain and cloud",
            "cloud_snow": "snow and cloud",
            "sun": "sun",
            "Mist": "fog and clouds",
            "Smoke": "Smoke",
            "Haze": "Haze",
            "Dust": "Dust",
            "Fog": "fog",
            "Sand": "Sand",
            "Dust": "Dust",
            "Ash": "Ash",
            "Squal": "Squal",
            "Tornado": "Tornado",
        }


    def mainloop(self):
        """Runs the showing of the clock-face periodically (better way?)"""
        print("Starting clock mainloop")
        prev_time = 0
        prev_weather_time = datetime.datetime.fromtimestamp(0)
        while True:
            if prev_time == datetime.datetime.now().strftime("%H:%M"):
                time.sleep(10)
            else:
                d = datetime.datetime.now() - prev_weather_time
                if d.total_seconds() >= 3*3600:
                    prev_weather_time = datetime.datetime.now()
                    weather = self.bot.bot_show_weather(["zurich"])
                    offset = weather.find("</b>") + 6
                    weather = weather[offset:]
                    weather = weather[:weather.find(":")]
                    self.weather = weather

                prev_time = datetime.datetime.now().strftime("%H:%M")
                self.clock.set_face(self.categories[self.weather])
