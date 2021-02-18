# functionality
import bot2.main
import clock.main
import dashboard.main

import persistence.main

# various
import logging
from threading import Thread
import os


if os.name == "nt":
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
    )
else:
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO,
        filename='persistence/complete.log',
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
        self.bot_module = bot2.main.ChatBot(name="Norbit", version="3.0a", prst=self.persistence)
        self.dashboard_module = dashboard.main.DashBoard(host_ip="0.0.0.0", prst=self.persistence)

        self.modules = {
            "clock" : self.clock_module,
            "bot" : self.bot_module,
            "dashboard" : self.dashboard_module,
        }

        for module in self.modules.values():
            module.modules = self.modules
            module.start()


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