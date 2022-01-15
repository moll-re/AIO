import logging

from persistence import local_io, database


logger = logging.getLogger(__name__)


class Launcher:
    """Template for launching collections of modules"""

    def __init__(self, **modules):
        """"""
        self.persistence = local_io.PersistentDict("persistence/prst.json")
        self.db_utils = database.DatabaseUtils
        self.modules = modules

        logger.info(self.__class__.__name__ + " initialized")

        if len(self.persistence) == 0:
            self.init_persistence()
        self.persistence["global"]["reboots"] += 1
        
        self.launch_modules()

        
        
    def launch_modules(self):
        for module in self.modules.values():
            logger.info("Starting module {}".format(module.__class__.__name__))
            module.modules = self.modules
            module.persistence = self.persistence
            module.db_utils = self.db_utils()
            module.start()


    def init_persistence(self):
        logger.warning("No persistence found, created a new one")

        self.persistence["global"] ={
            "lists" : {},
            "reboots": 0
            }

        for m_name in self.modules.keys():
            data = {}
            if m_name == "bot":
                data =  {
                    "send_activity" : {"hour":[], "count":[]},
                    "receive_activity" : {"hour":[], "count":[]},
                    "execute_activity" : {"hour":[], "count":[]},
                    "log": [],
                    "chat_members": {},
                    "aliases" : {}
                }
            if m_name == "clock":
                data = {
                    "sensors" : {
                        "time" : [],
                        "temperature":[],
                        "humidity":[],
                        "brightness" : [],
                        }
                }
            
            self.persistence[m_name] = data

        