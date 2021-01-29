# functionality
import bot.main
import bot2.main
import clock.main
import dashboard.main
# wrapper
import wrapper
import persistence.main

# various
import logging
from threading import Thread

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

class Launcher():
    """Launches all other submodules"""

    def __init__(self):
        """"""
        self.persistence = persistence.main.PersistentDict("persistence/prst.json")
        self.logger = logging.getLogger(__name__)
        self.logger.info("Starting")

        if len(self.persistence) == 0:
            self.init_persistence()
        self.persistence["global"]["reboots"] += 1

        self.clock_module = clock.main.ClockFace(prst=self.persistence)
        self.bot_module = bot2.main.ChatBot(name="Norbit", version="3.0a", prst=self.persistence, hw_commands=self.clock_module.commands)
        self.dashboard_module = dashboard.main.DashBoard(host_ip="0.0.0.0", prst=self.persistence)

        self.threads = []
        #self.threads.append(Thread(target=self.chatbot))
        
        self.threads.append(Thread(target=self.clock))
        self.threads.append(Thread(target=self.dashboard))
        
        for i in self.threads:
            i.start()
        self.chatbot()
        

    def clock(self):
        self.clock = wrapper.ClockWrapper(self.clock_module, self.bot_module)

    def chatbot(self):
        self.bot = wrapper.BotWrapper(self.bot_module, self.clock_module)

    def dashboard(self):
        self.dashboard = wrapper.DashBoardWrapper(self.dashboard_module, self.bot_module)


    def init_persistence(self):
        self.logger.warn("No persistence found, created a new one")

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