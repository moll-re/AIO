# functionality
from bot import main
from clock import c_back
from broadcast import b_out 
import launcher

import logging
import platform


import os
if os.getenv("dockerized", "") == "true" or platform.uname().node == "ArchSpectre":
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
    )
else:
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO,
        filename='persistence/server.log',
    )



class BroadcastLauncher(launcher.Launcher):
    """Launcher for all server-side modules. The hard-computations"""
    def __init__(self):
        
        self.bot_module = main.ChatBot(name="Norbit", version="4.1a") 
        self.clock_backend_module = c_back.ClockBackend() # threaded through threading.Timer
        self.broadcast_module = b_out.BroadcastUpdates(port="1111") # Thread

        super().__init__(
            bot = self.bot_module,
            clock = self.clock_backend_module,
            broadcast = self.broadcast_module
        )

BroadcastLauncher()