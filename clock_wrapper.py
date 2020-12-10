import wrapper
import datetime


class ClockWrapper(wrapper.Wrapper):
    """Wrapper for the CLOCK-functionality"""
    def __init__(self, own_module, *other_modules):
        """"""
        super().__init__(own_module, *other_modules)
        print("Initializing clock-functionality")
        self.weather = {"weather":"", "high":"", "low":"", "show":"temps"}
        self.mainloop(15)
        


    def mainloop(self, sleep_delta):
        """Runs the showing of the clock-face periodically (better way?)"""
        print("Starting clock mainloop")
        self.prev_time = 0
        self.prev_weather_time = datetime.datetime.fromtimestamp(0)

        def perform_loop():
            if self.prev_time != datetime.datetime.now().strftime("%H:%M"):
                d = datetime.datetime.now() - self.prev_weather_time
                mins_elapsed = int(d.total_seconds()/60)

                if mins_elapsed >= 3*60:
                    # fetch new weather every 3 hours (hard coded)
                    prev_weather_time = datetime.datetime.now()
                    weather = self.others[0].bot_show_weather("zurich")
                    if not (sad in weather):
                        l1 = weather[weather.find("</b>")+5:weather.find("\n")].replace (":","")
                        # current weather situation (icon): we pick the first line, remove the start string, remove :: indicating an emoji

                        temps_today = weather.splitlines()[4]
                        low = temps_today[temps_today.find("button")+8:temps_today.find("°")]
                        temps_today = temps_today[temps_today.find("°") + 1:]
                        high = temps_today[temps_today.find("button")+8:temps_today.find("°")]
                        self.weather["weather"] = l1
                        self.weather["high"] = high
                        self.weather["low"] = low
                    else:
                        self.weather["weather"] = "error"
                        self.weather["high"] = "error"
                        self.weather["low"] = "error"

                if mins_elapsed % 5 == 0:
                    if self.weather["show"] == "weather":
                        next = "temps"
                    else:
                        next = "weather"
                    self.weather["show"] = next

                prev_time = datetime.datetime.now().strftime("%H:%M")

                self.own.set_face(self.weather)

        super().mainloop(sleep_delta,perform_loop)