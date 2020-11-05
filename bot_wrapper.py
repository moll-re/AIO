import time
import datetime


class ModuleWrapper():
    """Wrapper for the BOT-functionality"""
    def __init__(self, bot_module, clock_module):
        """"""
        print("Initializing bot-functionality")
        #######################################################################

        self.bot = bot_module
        self.clock = clock_module

        # available hw-commands. Must be updated manually!
        self.hw_commands = {
            "blink" : self.clock.alarm_blink,
            "wakeup" : self.clock.wake_light,
            "showmessage" : self.clock.show_message,

        }
        self.bot.add_commands(self.hw_commands)

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
                        self.react_hw_command(command,params) # hw-level
                    else:
                        self.bot.react_command(command,params) # sw-level
            time.sleep(5)


    def react_hw_command(self, command, params):
        """"""
        # so params is a list, and so, to pass the commands, we need to unpack it:
        self.hw_commands[command](*params)
