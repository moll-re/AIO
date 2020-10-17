import time
import datetime

import bot.main
import clock.main

class ModuleWrapper():
    """Wrapper for the BOT-functionality"""
    def __init__(self):
        """"""
        print("Initializing bot-functionality")
        #######################################################################

        self.clock = clock.main.ClockFace()
        self.hw_commands = {
            "blink" : self.clock.alarm_blink,
            "wakeup" : self.clock.wake_light,
            "showmessage" : self.clock.show_message,

        }

        self.bot = bot.main.ChatBot("ChatterBot", "2.0", self.hw_commands)


        self.message_loop()


    def message_loop(self):
        """Calls the telegram entity regularly to check for activity"""
        print("Starting bot mainloop")
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
        # Oh yeah, that needs to be changed
        # so params is a list, and so, to pass the commands, we need to unpack it:
        self.hw_commands[command](*params)
