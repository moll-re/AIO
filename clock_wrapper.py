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
        self.weather = {"weather":"", "high":"", "low":"", "show":"weather"}


    def mainloop(self):
        """Runs the showing of the clock-face periodically (better way?)"""
        print("Starting clock mainloop")
        prev_time = 0
        prev_weather_time = datetime.datetime.fromtimestamp(0)
        while True:
            if prev_time == datetime.datetime.now().strftime("%H:%M"):
                time.sleep(15)
            else:
                d = datetime.datetime.now() - prev_weather_time
                mins_elapsed = int(d.total_seconds()/60)

                if mins_elapsed >= 3*60:
                    # fetch new weather every 3 hours (hard coded)
                    prev_weather_time = datetime.datetime.now()
                    weather = self.bot.bot_show_weather("zurich")

                    l1 = weather[weather.find("</b>")+5:weather.find("\n")].replace (":","")
                    # current weather situation (icon): we pick the first line, remove the start string, remove :: indicating an emoji

                    temps_today = weather.splitlines()[4]
                    low = temps_today[temps_today.find("button")+8:temps_today.find("°")]
                    temps_today = temps_today[temps_today.find("°") + 1:]
                    high = temps_today[temps_today.find("button")+8:temps_today.find("°")]
                    self.weather["weather"] = l1
                    self.weather["high"] = high
                    self.weather["low"] = low

                if mins_elapsed % 5 == 0:
                    if self.weather["show"] == "weather":
                        next = "temps"
                    else:
                        next = "weather"
                    self.weather["show"] = next

                prev_time = datetime.datetime.now().strftime("%H:%M")

                self.clock.set_face(self.weather)
