import wrapper

from threading import Thread
import time

class DashBoardWrapper(wrapper.Wrapper):
    def __init__(self, own_module, *other_modules):
        """"""
        super().__init__(own_module, other_modules)
        print("Initializing DASHBOARD-functionality")
        # mainloop

    def mainloop(self):
        super(DashBoardWrapper, self).mainloop(sleep_delta = 3600*3) #3hours refresh-cycle
        self.set_weather()
        self.set_shopping_list()
        self.set_bot_logs()
        self.set_joke()
        self.bot.refresh()

    def set_weather(self):
        weather = self.bot.bot_show_weather("zurich")
        ...
        self.own.set_weather(weather)
