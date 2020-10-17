import clock_wrapper
import bot_wrapper
from threading import Thread


class Launcher():
    """Launches all other submodules"""

    def __init__(self):
        self.threads = []
        self.threads.append(Thread(target=self.chatbot))
        self.threads.append(Thread(target=self.clock))


        for i in self.threads:
            i.start()


    def clock(self):
        print("Launching clock-functionality")
        self.clock = clock_wrapper.ModuleWrapper()

    def chatbot(self):
        print("Launching bot-functionality")
        self.bot = bot_wrapper.ModuleWrapper()


Launcher()
