# functionality
from bot import main
from clock import cin, cout
from dashboard import dout

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


class Launcher:
    """Launches all other submodules"""

    def __init__(self):
        """"""
        self.persistence = persistence.main.PersistentDict("persistence/prst.json")
        self.logger = logging.getLogger(__name__)
        self.logger.info("Launcher initialized")

        if len(self.persistence) == 0:
            self.init_persistence()
        self.persistence["global"]["reboots"] += 1

        self.clock_module = cout.ClockFace(prst=self.persistence)
        self.bot_module = main.ChatBot(name="Norbit", version="3.0a", prst=self.persistence)
        self.dashboard_module = dout.DashBoard(host_ip="0.0.0.0", prst=self.persistence)
        self.sensors = cin.SensorReadout(prst=self.persistence)

        self.modules = {
            "sensors" : self.sensors,
            "bot" : self.bot_module,
            "clock" : self.clock_module,
            "dashboard" : self.dashboard_module,
        }

        for module in self.modules.values():
            self.logger.info("Starting module "+ module.__class__.__name__)
            module.modules = self.modules
            module.start()
        

    def init_persistence(self):
        self.logger.warning("No persistence found, created a new one")

        self.persistence["bot"] =  {
            "send_activity" : {"hour":[], "count":[]},
            "receive_activity" : {"hour":[], "count":[]},
            "execute_activity" : {"hour":[], "count":[]},
            "log": [],
            "chat_members": {},
            "aliases" : {}
        }
        self.persistence["clock"] = {
            "sensors" : {
                "time" : [],
                "temperature":[],
                "humidity":[],
                "brightness" : [],
                }
        }
        self.persistence["dashboard"] = {}
        self.persistence["global"] = {
            "lists" : {},
            "reboots": 0
            }


########################################################################
## Aand liftoff!
Launcher()
