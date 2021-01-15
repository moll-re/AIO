# functionality
import bot.main
import clock.main
import dashboard.main
# wrapper
import wrapper
import persistence.main
# misc.
from threading import Thread

class Launcher():
    """Launches all other submodules"""

    def __init__(self):
        """"""
        self.persistence = persistence.main.PersistentDict("persistence/prst.json")
        if len(self.persistence) == 0:
            self.init_persistence()
        self.persistence["global"]["reboots"] += 1

        self.clock_module = clock.main.ClockFace(prst=self.persistence)
        self.bot_module = bot.main.ChatBot(name="ChatterBot", version="2.2", prst=self.persistence, hw_commands=self.clock_module.commands)
        self.dashboard_module = dashboard.main.DashBoard(host_ip="0.0.0.0", prst=self.persistence)

        self.threads = []
        self.threads.append(Thread(target=self.chatbot))
        self.threads.append(Thread(target=self.clock))
        self.threads.append(Thread(target=self.dashboard))
        for i in self.threads:
            i.start()


    def clock(self):
        self.clock = wrapper.ClockWrapper(self.clock_module, self.bot_module)


    def chatbot(self):
        self.bot = wrapper.BotWrapper(self.bot_module, self.clock_module)


    def dashboard(self):
        self.dashboard = wrapper.DashBoardWrapper(self.dashboard_module, self.bot_module)

    def init_persistence(self):
        print("New Persistence created")
        self.persistence["bot"] =  {
            "send_activity" : {"hour":[], "count":[]},
            "receive_activity" : {"hour":[], "count":[]},
            "execute_activity" : {"hour":[], "count":[]},
            "log": [],
            "chat_members": {},
            "aliases" : {}
        }
        self.persistence["clock"] = {}
        self.persistence["dashboard"] = {}
        self.persistence["global"] = {
            "lists" : {},
            "reboots": 0
            }


########################################################################
## Aand liftoff!
Launcher()