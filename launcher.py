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
        self.persistence = shelve.DbfilenameShelf("persistence/prst.db", writeback = True)
        if len(self.persistence) == 0:
            self.init_persistence()
        self.persistence["global"]["reboots"] += 1
        self.clock_module = clock.main.ClockFace(prst=self.persistence)
        self.bot_module = bot.main.ChatBot(name="ChatterBot", version="2.1", prst=self.persistence, hw_commands=self.clock_module.commands)
        
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
        print("New Persistence created")
        self.persistence["bot"] =  {
            "messages_read": 0,
            "messages_sent": 0,
            "commands_executed": 0,
            "photos_sent": 0,
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