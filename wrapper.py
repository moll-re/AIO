import time
import datetime


class Wrapper():
    """Wrapper skeleton for the modules (bot, clock dashboard...)"""

    def __init__(self, own_module, *other_modules):
        self.own = own_module
        self.others = other_modules
        print("Starting " + self.__class__.__name__ + " functionality")

        

    def mainloop(self, sleep_delta, action):
        """sleep_delta in seconds sets the sleep period of the loop
            action is a function that is performed every * seconds"""
        print("Launching " + self.__class__.__name__ + " mainloop")
        while True:
            action()
            time.sleep(sleep_delta)



class ClockWrapper(Wrapper):
    """Wrapper for the CLOCK-functionality"""
    def __init__(self, own_module, *other_modules):
        """"""
        super().__init__(own_module, *other_modules)
        self.weather = {"weather":"", "high":"", "low":"", "show":"temps"}
        self.mainloop(15)
        


    def mainloop(self, sleep_delta):
        """Runs the showing of the clock-face periodically (better way?)"""
        
        self.prev_time = 0
        self.prev_weather_time = datetime.datetime.fromtimestamp(0)

        def perform_loop():
            if self.prev_time != datetime.datetime.now().strftime("%H:%M"):
                d = datetime.datetime.now() - self.prev_weather_time
                mins_elapsed = int(d.total_seconds()/60)

                if mins_elapsed >= 3*60:
                    # fetch new weather every 3 hours (hard coded)
                    self.prev_weather_time = datetime.datetime.now()
                    weather = self.others[0].bot_show_weather("zurich")
                    if not (":sad:" in weather):
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

                self.prev_time = datetime.datetime.now().strftime("%H:%M")

                self.own.set_face(self.weather)

        super().mainloop(sleep_delta,perform_loop)



class BotWrapper(Wrapper):
    """Wrapper for the BOT-functionality"""
    def __init__(self, own_module, *other_modules):
        """"""
        super().__init__(own_module, *other_modules)

        self.bot = own_module
        self.clock = other_modules[0]
        

        # available hw-commands. Must be updated manually!
        self.hw_commands = {
            "blink" : self.clock.alarm_blink,
            "wakeup" : self.clock.wake_light,
            "showmessage" : self.clock.show_message,

        }
        self.bot.add_commands(self.hw_commands)

        self.mainloop(10)


    def mainloop(self, sleep_delta):
        """Calls the telegram entity regularly to check for activity"""
        def perform_loop():
            result = self.bot.telegram.fetch_updates()
            if len(result) != 0:
                command, params = self.bot.telegram.handle_result(result)
                if command != "nothing":
                    if command in self.hw_commands:
                        self.react_hw_command(command,params) # hw-level
                    else:
                        self.bot.react_command(command,params) # sw-level

        super().mainloop(sleep_delta, perform_loop)

    def react_hw_command(self, command, params):
        """"""
        # so params is a list, and so, to pass the commands, we need to unpack it:
        self.hw_commands[command](*params)
