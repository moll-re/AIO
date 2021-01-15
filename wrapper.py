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
        self.weather_raw = {}
        self.mainloop(15)
        


    def mainloop(self, sleep_delta):
        """Runs the showing of the clock-face periodically (better way?)"""
        
        self.prev_time = "0"

        def perform_loop():
            if self.prev_time != datetime.datetime.now().strftime("%H%M"):

                if int(self.prev_time) % 5 == 0:
                    weather = self.others[0].weather.show_weather([47.3769, 8.5417]) # zürich

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

                self.prev_time = datetime.datetime.now().strftime("%H%M")

                self.own.set_face(self.weather)

        super().mainloop(sleep_delta,perform_loop)



class BotWrapper(Wrapper):
    """Wrapper for the BOT-functionality"""
    def __init__(self, own_module, *other_modules):
        """"""
        super().__init__(own_module, *other_modules)

        self.bot = own_module
        self.clock = other_modules[0]

        self.mainloop(10)


    def mainloop(self, sleep_delta):
        """Calls the telegram entity regularly to check for activity"""
        def perform_loop():
            self.bot.react_chats()
            # num = self.bot.telegram.fetch_updates()
            # for message in range(num):
            #     command, params = self.bot.react_command() # returns None if handled internally
            #     if command != None:
            #         self.clock.external_action(command, params)
        super().mainloop(sleep_delta, perform_loop)



class DashBoardWrapper(Wrapper):
    def __init__(self, own_module, *other_modules):
        """Wrapper for the dashboard functionality"""
        super().__init__(own_module, other_modules)
        # self.mainloop(1 * 3600) # 1 hour refresh-cycle
        # cannot get called through mainloop, will use the included callback-functionality of Dash
        own_module.bot = other_modules[0]
        own_module.launch_dashboard()