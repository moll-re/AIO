# functionality
from bot import main
from clock import c_back
from broadcast import b_out 
# from dashboard import d_out

import launcher



class BroadcastLauncher(launcher.Launcher):
    """Launcher for all server-side modules. The hard-computations"""
    def __init__(self):
        
        self.bot_module = main.ChatBot(name="Norbit", version="4.0a") # ??? 
        self.clock_backend_module = c_back.ClockBackend() # threaded through threading.Timer
        self.broadcast_module = b_out.BroadcastUpdates(port="1111") # Thread
        # self.dashboard_module = d_out.DashBoard(port="80") # ??? threaded as Thread

        # "sensors" : self.sensors,
        # "bot" : self.bot_module,
        # "clock" : self.clock_module,
        # "dashboard" : self.dashboard_module,
        super().__init__(
            bot = self.bot_module,
            clock = self.clock_backend_module,
            # dashboard = self.dashboard_module,
            broadcast = self.broadcast_module
        )

BroadcastLauncher()