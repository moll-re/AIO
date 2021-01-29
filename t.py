import bot2.main
import persistence.main

import logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    #filename='persistence/complete.log',
)
logger = logging.getLogger(__name__)
prst = persistence.main.PersistentDict("persistence/prst.json")

test = bot2.main.ChatBot("Test", ".1", "HW", prst, logger)