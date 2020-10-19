import time
import datetime
from threading import Thread


class ModuleWrapper():
    """Wrapper for the CLOCK-functionality"""
    def __init__(self, bot_module, clock_module):
        """"""
        print("Initializing clock-functionality")
        self.clock = clock_module
        self.bot = bot_module
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
                    l1 = weather[:weather.find("\n")]
                    l1 = l1.replace("<b>Today:</b> ","")
                    l1 = l1.replace (":","")
                    self.weather = l1

                prev_time = datetime.datetime.now().strftime("%H:%M")

                self.clock.set_face(self.categories[self.weather])
