import time
import datetime

import bot.main
import clock.main

class ModuleWrapper():
    """Wrapper for the BOT-functionality"""
    def __init__(self, module_name):
        """"""
        #######################################################################
        self.bot = bot.main.ChatBot("ChatterBot", version="1.2")
        self.clock = clock.main.ClockFace()

        self.hw_commands = {
            "blink": self.clock.alarm_blink,
        }
        self.message_loop()


    def message_loop(self):
        """Calls the telegram entity regularly to check for activity"""
        while(True):
            result = self.bot.telegram.fetch_updates()
            if len(result) != 0:
                command, params = self.bot.telegram.handle_result(result)
                if command != "nothing":
                    if command in self.hw_commands:
                        self.react_command(command,params)
                    else:
                        self.bot.react_command(command,params)
            time.sleep(5)

    def react_command(self, command, params):
        """"""
        self.hw_commands[command](params[0],params[1])

test = ModuleWrapper("bot")
