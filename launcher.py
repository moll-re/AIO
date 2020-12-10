# functionality
import bot.main
import clock.main
import dashboard.main

# wrapper
import wrapper

# misc.
from threading import Thread
import shelve


class Launcher():
    """Launches all other submodules"""

    def __init__(self):
        """"""
        self.persistence = shelve.open('persistence/prst.db', writeback=True)
        self.init_persistence()
        # TODO populate the persistence
        self.bot_module = bot.main.ChatBot(name="ChatterBot", version="2.1", prst=self.persistence)
        self.clock_module = clock.main.ClockFace(prst=self.persistence)

        self.threads = []
        self.threads.append(Thread(target=self.chatbot))
        self.threads.append(Thread(target=self.clock))

        for i in self.threads:
            i.start()


    def clock(self):
        self.clock = wrapper.ClockWrapper(self.clock_module, self.bot_module)


    def chatbot(self):
        self.bot = wrapper.BotWrapper(self.bot_module, self.clock_module)


    def dashboard(self):
        self.dashboard = wrapper.DashBoardWrapper(self.dashboard_module, self.bot_module)

    def init_persistence(self):
        self.persistence["bot"] =  {
            "messages_read": 0,
            "messages_sent": 0,
            "commands_executed": 0,
            "photos_sent": 0,
            "log": [],
            "chat_members": {},
            "reboots": 0
        }
        self.persistence["clock"] = {}
        self.persistence["dashboard"] = {}
        self.persistence["global"] = {
            "lists" : {}
            }


########################################################################
## Aand liftoff!
Launcher()
