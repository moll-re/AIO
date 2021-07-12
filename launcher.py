import logging

from persistence import p_io, p_out


logger = logging.getLogger(__name__)


class Launcher:
    """base launcher that launches other submodules"""

    def __init__(self, **modules):
        """"""
        self.persistence = p_io.PersistentDict("persistence/prst.json")
        self.db = p_out.DBLogging()

        logger.info(self.__class__.__name__ + " initialized")

        self.modules = modules
        if len(self.persistence) == 0:
            self.init_persistence()
        self.persistence["global"]["reboots"] += 1
        
        self.launch_modules()

        
        
    def launch_modules(self):

        for module in self.modules.values():
            logger.info("Starting module "+ module.__class__.__name__)
            module.modules = self.modules
            module.persistence = self.persistence
            module.db = self.db
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

        

########################################################################
## Aand liftoff!
# Launcher()
