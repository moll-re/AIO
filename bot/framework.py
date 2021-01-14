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
    	
        self.emoji_dict = {
            "a" : ":regional_indicator_symbol_letter_a:",
            "b" : ":regional_indicator_symbol_letter_b:",
            "c" : ":regional_indicator_symbol_letter_c:",
            "d" : ":regional_indicator_symbol_letter_d:",
            "e" : ":regional_indicator_symbol_letter_e:",
            "f" : ":regional_indicator_symbol_letter_f:",
            "g" : ":regional_indicator_symbol_letter_g:",
            "h" : ":regional_indicator_symbol_letter_h:",
            "i" : ":regional_indicator_symbol_letter_i:",
            "j" : ":regional_indicator_symbol_letter_j:",
            "k" : ":regional_indicator_symbol_letter_k:",
            "l" : ":regional_indicator_symbol_letter_l:",
            "m" : ":regional_indicator_symbol_letter_m:",
            "n" : ":regional_indicator_symbol_letter_n:",
            "o" : ":regional_indicator_symbol_letter_o:",
            "p" : ":regional_indicator_symbol_letter_p:",
            "q" : ":regional_indicator_symbol_letter_q:",
            "r" : ":regional_indicator_symbol_letter_r:",
            "s" : ":regional_indicator_symbol_letter_s:",
            "t" : ":regional_indicator_symbol_letter_t:",
            "u" : ":regional_indicator_symbol_letter_u:",
            "v" : ":regional_indicator_symbol_letter_v:",
            "w" : ":regional_indicator_symbol_letter_w:",
            "x" : ":regional_indicator_symbol_letter_x:",
            "y" : ":regional_indicator_symbol_letter_y:",
            "z" : ":regional_indicator_symbol_letter_z:",
            "0" : ":keycap_digit_zero:",
            "1" : ":keycap_digit_one:",
            "2" : ":keycap_digit_two:",
            "3" : ":keycap_digit_three:",
            "4" : ":keycap_digit_four:",
            "5" : ":keycap_digit_five:",
            "6" : ":keycap_digit_six:",
            "7" : ":keycap_digit_seven:",
            "8" : ":keycap_digit_eight:",
            "9" : ":keycap_digit_nine:",
        }

        self.telegram = telegram.TelegramIO(self.persistence)
        self.weather = weather.WeatherFetch()

    def react_chats(self):
        """Checks unanswered messages and answers them"""

        # HACKY: TODO remove
        self.persistence.sync()
        # writes persistent variables to file so that they ACTUALLY persist
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
            self.telegram.send_message(result)

            current_hour = int(datetime.datetime.now().timestamp() // 3600)
            if len(self.persistence["bot"]["execute_activity"]["hour"]) == 0 or current_hour != self.persistence["bot"]["execute_activity"]["hour"][-1]:
                self.persistence["bot"]["execute_activity"]["hour"].append(current_hour)
                self.persistence["bot"]["execute_activity"]["count"].append(1)
            else:
                self.persistence["bot"]["execute_activity"]["count"][-1] += 1

        if self.is_command(cmd): # first word
            call_command(cmd, params)
        elif cmd in self.persistence["bot"]["aliases"]:
            dealias = self.persistence["bot"]["aliases"][cmd].split(" ") # as a list
            new_cmd = dealias[0]
            params = dealias[1:] + params
            self.telegram.send_message("Substituted <code>" + cmd + "</code> to <code>" + self.persistence["bot"]["aliases"][cmd] + "</code> and got:")
            call_command(new_cmd, params)
        else:
            self.telegram.send_message("Command <code>" + tmp[0] + "</code> not found.")


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


    def emojify_word(self,word):
        """"""
        string_emoji = ""
        for letter in word:
            if letter in self.emoji_dict:
                string_emoji += self.emoji_dict[letter.lower()]
            else:
                string_emoji += letter
        return string_emoji


    def write_bot_log(self, function_name, error_message):
        """"""
        out = datetime.datetime.now().strftime("%d.%m.%y - %H:%M")
        out += " @ " + function_name
        out += " --> " + error_message
        self.persistence["bot"]["log"] += [out]

    