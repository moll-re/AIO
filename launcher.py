# functionality
import bot.main
import clock.main
import dashboard.main

# wrapper
import clock_wrapper
import bot_wrapper
import dashboard_wrapper

# misc.
from threading import Thread



class Launcher():
    """Launches all other submodules"""

    def __init__(self):
        """"""
        self.bot_module = bot.main.ChatBot("ChatterBot", "2.0")
        self.clock_module = clock.main.ClockFace()

        self.threads = []
        self.threads.append(Thread(target=self.chatbot))
        self.threads.append(Thread(target=self.clock))

        for i in self.threads:
            i.start()


    def clock(self):
        print("Launching clock-functionality")
        self.clock = clock_wrapper.ClockWrapper(self.clock_module, self.bot_module)


    def chatbot(self):
        print("Launching bot-functionality")
        self.bot = bot_wrapper.ModuleWrapper(self.bot_module, self.clock_module)


    def dashboard(self):
        print("Launching dashboard-functionality")
        self.dashboard = dashboard_wrapper.DashBoardWrapper(self.dashboard_module, self.bot_module)

########################################################################
## Aand liftoff!
Launcher()
