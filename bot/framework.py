import datetime 
from bot.api import telegram, google, weather, reddit
import Levenshtein as lev





class BotFramework():
    """Main functionality for a bot """

    def __init__(self, name, version, prst):
        """Inits the Bot with a few conf. vars
        Args:   -> name:str - Name of the bot
                -> version:str - Version number
                -> prst:shelveObj - persistence
        """

        self.version = version
        self.name = name

        # Persistent variable
        self.persistence = prst
        # Uptime counter
        self.start_time = datetime.datetime.now()

        self.telegram = telegram.TelegramIO(self.persistence)
        self.weather = weather.WeatherFetch()

    def react_chats(self):
        """Checks unanswered messages and answers them"""

        num = self.telegram.fetch_updates()
        for i in range(num):
            self.react_command()


    def react_command(self):
        """Reacts if a new command is present
        
        Returns command, params iff the command is a hardware-one (for the clock), else None"""
        message = self.telegram.process_message()
        if message == None:
            return
        
        message = message[1:] #remove first "/"
        tmp = message.split(" ")
        cmd = tmp[0]
        params = tmp[1:]

        def call_command(cmd, par):
            result = self.commands[cmd](*par)
            # *params means the list is unpacked and handed over as separate arguments.
            self.telegram.increase_counter("execute_activity")
            return result
            

        if self.is_command(cmd): # first word
            result = call_command(cmd, params)
        elif cmd in self.persistence["bot"]["aliases"]:
            dealias = self.persistence["bot"]["aliases"][cmd].split(" ") # as a list
            new_cmd = dealias[0]
            params = dealias[1:] + params
            result  = "Substituted <code>" + cmd + "</code> to <code>" + self.persistence["bot"]["aliases"][cmd] + "</code> and got:\n\n"
            result += call_command(new_cmd, params)
        else:
            result = "Command <code>" + tmp[0] + "</code> not found."
        self.telegram.send_message(result)

    def is_command(self, input):
        """checks if we have a command. Returns true if yes and False if not
        
        Also sends a mesage if close to an existing command
        """
        max_match = 0
        command_candidate = ""
        for command in self.commands.keys():
            match = lev.ratio(input.lower(),command)
            if match > 0.7 and match > max_match:
                max_match = match
                command_candidate = command
        if max_match == 1:
            return True
        if max_match != 0:
            self.telegram.send_message("Did you mean <code>" + command_candidate + "</code>?")
        return False


    def write_bot_log(self, function_name, error_message):
        """"""
        out = datetime.datetime.now().strftime("%d.%m.%y - %H:%M")
        out += " @ " + function_name
        out += " --> " + error_message
        self.persistence["bot"]["log"] += [out]

    