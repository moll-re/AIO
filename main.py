# -*- coding: utf-8 -*-

from api import telegram, google, reddit, weather
from persistence import rw as pvars

import requests
import time
import json
import datetime
import emoji

class ChatBot():
    """"""
    def __init__(self, name, version):
        """Inits the Bot with a few conf. vars
        Args:   -> name:str - Name of the bot
                -> api_key:str - t.me api-key
                -> version:str - Version number
        """

        self.version = version
        self.name = name

        # Persistent variable
        self.persistence = pvars.Variables("persistence/persistent_vars.json", "persistence/persistent_init.json")
        # Uptime counter
        self.start_time = datetime.datetime.now()
        self.persistence.increment("reboots")

        # Available commands
        self.commands = {
            "help" : self.bot_show_help,
            "status" : self.bot_print_status,
            "log" : self.bot_print_log,
            "lorem" : self.bot_print_lorem,
            "weather" : self.bot_show_weather,
            "google" : self.bot_google_search,
            "events" : self.bot_print_events,
            "emojify" : self.bot_emojify,
            "wikipedia" : self.bot_show_wikipedia,
            "bot_do_all" : self.bot_do_all,
            "zvv" : self.bot_zvv,
            "cronjob" : self.bot_cronjob,
            "joke" : self.bot_tell_joke,
            "meme" : self.bot_send_meme,
            "news" : self.bot_send_news,
        }


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

        self.telegram = telegram.TelegramIO(self.persistence, self.commands)

        self.message_loop()


    def message_loop(self):
        """Calls the telegram entity regularly to check for activity"""
        while(True):
            result = self.telegram.fetch_updates()
            if len(result) != 0:
                command, params = self.telegram.handle_result(result)
                if command != "nothing":
                    self.commands[command](params)
            time.sleep(5)


    def emojify_word(self,word):
        """"""
        string_emoji = ""
        for letter in word:
            if letter in self.emoji_dict:
                string_emoji += self.emoji_dict[letter.lower()]
            else:
                string_emoji += letter
        return string_emoji

    ############################################################################
    """BOT-Commands: implementation"""

    def bot_print_lorem(self, params):
        """Prints a placeholder text."""
        if "full" in params:
            message = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. At tellus at urna condimentum mattis pellentesque id nibh. Convallis aenean et tortor at risus viverra adipiscing at in. Aliquet risus feugiat in ante metus dictum. Tincidunt augue interdum velit euismod in pellentesque massa placerat duis. Tincidunt vitae semper quis lectus nulla at. Quam nulla porttitor massa id neque aliquam vestibulum morbi blandit. Phasellus egestas tellus rutrum tellus pellentesque eu tincidunt. Gravida rutrum quisque non tellus orci. Adipiscing at in tellus integer feugiat. Integer quis auctor elit sed vulputate mi sit amet mauris. Risus pretium quam vulputate dignissim suspendisse in est. Cras fermentum odio eu feugiat pretium. Ut etiam sit amet nisl purus in mollis nunc sed. Elementum tempus egestas sed sed risus pretium quam. Massa ultricies mi quis hendrerit dolor magna eget."
        else:
            message = "Lorem ipsum dolor sit amet, bla bla bla..."
        self.telegram.send_message(message)


    def bot_print_status(self, params):
        """Prints the bots current status and relevant information"""
        delta = str(datetime.datetime.now() - self.start_time)
        try:
            ip = requests.get('https://api.ipify.org').text
        except:
            ip = "not fetchable"
        message = "<pre>Status: Running :green_circle:\n"
        message += "Uptime: " + delta[:delta.rfind(".")] + "\n"
        message += "Reboots: " + str(self.persistence.read("reboots")) + "\n"
        message += "IP-Adress: " + ip + "\n"
        message += "Messages read: " + str(self.persistence.read("messages_read")) + "\n"
        message += "Messages sent: " + str(self.persistence.read("messages_sent")) + "\n"
        message += "Commands executed " + str(self.persistence.read("commands_executed")) + "</pre>"
        self.telegram.send_message(message)
        if "full" in params:
            self.bot_print_log([])


    def bot_show_weather(self, params):
        """Shows a weather-forecast for a given location"""
        if len(params) != 1:
            self.telegram.send_message("Invalid Syntax, please give one parameter, the location")
            return

        locations = {"freiburg": [47.9990, 7.8421], "zurich": [47.3769, 8.5417], "mulhouse": [47.7508, 7.3359]}
        if params[0].lower().replace("ü","u") in locations:
            city = locations[params[0].lower().replace("ü","u")]
        else:
            self.telegram.send_message("Couldn't find city, it might be added later though.")
            return

        message = weather.show_weather(city)

        self.telegram.send_message(message)


    def bot_google_search(self, params):
        """Does a google search and shows relevant links"""
        if len(params) < 1:
            self.telegram.send_message("Please tell me what to look for")
            return
        send_string = google.query(params)
        self.telegram.send_message(send_string)


    def bot_print_events(self, params):
        """Shows a list of couple-related events and a countdown"""
        events = {
            "anniversary :red_heart:" : datetime.date(datetime.datetime.now().year,12,7),
            "valentine's day :rose:": datetime.date(datetime.datetime.now().year,2,14),
            "Marine's birthday :party_popper:": datetime.date(datetime.datetime.now().year,8,31),
            "Remy's birthday :party_popper:": datetime.date(datetime.datetime.now().year,3,25),
            "Christmas :wrapped_gift:" : datetime.date(datetime.datetime.now().year,12,24),
        }

        send_string = "Upcoming events: \n"
        for key in events:
            delta = events[key] - datetime.date.today()
            if delta < datetime.timedelta(0):
                delta += datetime.timedelta(days = 365)
            send_string += key + ": " + str(delta.days) + " days \n"

        self.telegram.send_message(send_string)


    def bot_emojify(self, params):
        """Converts a string to emojis"""

        if len(params) < 2:
            self.telegram.send_message(emoji.emojize("Please send a separator as the first argument, and the text afterwards.\nExample:\n/emojify :heart: Example text"))

        sep = params[0]
        string_emoji = ""
        for word in params[1:]:
            out_string = self.emojify_word(word)
            string_emoji += out_string + sep

        self.telegram.send_message(string_emoji)


    def bot_show_help(self, params):
        """Shows a list of all commands and their description"""
        send_text = "BeebBop, this is " + self.name + " (V." + self.version + ")\n"
        send_text += "Here is what I can do up to now: \n"
        entries = sorted(list(self.commands.keys()))
        for entry in entries:
            send_text += "<b>" + entry + "</b> - "
            send_text += "<code>" + self.commands[entry].__doc__ + "</code>\n\n"
        self.telegram.send_message(send_text)


    def bot_print_log(self, params):
        """Shows an error-log, mostly of bad api-requests"""
        if "clear" in params:
            self.persistence.write("log",[])
            self.telegram.send_message("Log cleared")
            return
        send_text = ""
        for event in self.persistence.read("log"):
            send_text += event + "\n"
        if send_text == "":
            send_text += "No errors up to now"
        self.telegram.send_message(send_text)


    def bot_show_wikipedia(self, params):
        """Shows the wikipedia entry for a given therm"""
        if len(params) > 2 or len(params) == 0:
            self.telegram.send_message("Please only search for one word at a time. 1rst param is for language (de or fr or en or ...)")
            return

        if len(params) == 2:
            url = "https://" + params[0] + ".wikipedia.org/wiki/" + params[1]
        else:
            url = "https://en.wikipedia.org/wiki/" + params[0]

        try:
            r = requests.get(url)
        except:
            url = "https://en.wikipedia.org/wiki/" + params[0]
            r = requests.get(url)
            if r.status_code == 404:
                self.telegram.send_message("No result found for query")
                return
        self.telegram.send_message(url)


    def bot_do_all(self,params):
        """Executes every single command with random params"""
        for command in self.commands:
            if command != "bot_do_all":
                	self.commands[command](["en","Freiburg"])


    def bot_zvv(self,params):
        """Uses the swiss travel api to return the best route between a start- and endpoint in Zurich (actually whole Switzerland, but I haven't tested that)"""
        if len(params) != 2:
            self.telegram.send_message("Please give me your start and endpoint")
            return

        url = "http://transport.opendata.ch/v1/connections"
        data = {"from" : params[0], "to" : params[1], "limit" : 2}
        try:
            routes = requests.get(url, params=data).json()
            result = routes["connections"]
            text = result[0]["from"]["station"]["name"] + " :fast-forward_button: " + result[0]["to"]["station"]["name"] + "\n\n"
            for con in result:
                text += "Start: " + datetime.datetime.fromtimestamp(int(con["from"]["departureTimestamp"])).strftime("%d/%m - %H:%M") + "\n"
                text += ":chequered_flag: " + datetime.datetime.fromtimestamp(int(con["to"]["arrivalTimestamp"])).strftime("%d/%m - %H:%M") + "\n"
                text += ":hourglass_not_done: " + con["duration"] + "\n"
                text += ":world_map: Route:\n"

                for step in con["sections"]:
                    if step["journey"] != None:
                        text += step["journey"]["passList"][0]["station"]["name"] + " (" + datetime.datetime.fromtimestamp(int(step["journey"]["passList"][0]["departureTimestamp"])).strftime("%H:%M") + ")\n"

                        text += ":right_arrow: Linie " + self.emojify_word(step["journey"]["number"]) + "\n"

                        text += step["journey"]["passList"][-1]["station"]["name"] + " (" + datetime.datetime.fromtimestamp(int(step["journey"]["passList"][-1]["arrivalTimestamp"])).strftime("%H:%M") +")\n"
                    else:
                        text += "Walk."
                text += "\n"
            self.telegram.send_message(text)
        except:
            self.telegram.send_message("Invalid api call.")


    def bot_cronjob(self, params):
        """Allows you to add a timed command, in a crontab-like syntax. Not implemented yet.
        Example usage: /cronjob add 0 8 * * * weather Zürich
        """
        self.telegram.send_message("I'm not functional yet. But when I am, it is gonna be legendary!")


    def bot_tell_joke(self, params):
        """Tells you the top joke on r/jokes"""
        if len(params) == 0:
            number = 1
        elif len(params) == 1:
            number = int(params[0])
        else:
            self.telegram.send_message("Jokes takes only one parameter, the number of jokes.")
            return

        joke = reddit.get_random_rising("jokes", number, "text")
        self.telegram.send_message(joke)


    def bot_send_meme(self, params):
        """Sends a meme from r/"""
        subreddit_name = "memes"
        subnames = {
            "physics" : "physicsmemes",
            "dank" : "dankmemes",
            "biology" : "biologymemes",
            "math" : "mathmemes"
        }
        number = 1

        if len(params) == 1:
            try:
                number = int(params[0])
            except:
                try:
                    subreddit_name = subnames[str(params[0])]
                except:
                    self.telegram.send_message("Topic not found")
        elif len(params) == 2:
            try:
                number = int(params[0])
                subreddit_name = subnames[str(params[1]).lower()]
            except:
                number = int(params[1])
                subreddit_name = subnames[str(params[0]).lower()]

        elif len(params) > 2:
            self.telegram.send_message("Memes takes 2 parameters: the number of memes, and their topic.")
            return

        urls = reddit.get_random_rising(subreddit_name, number, "photo")
        for u in urls:
            try:
                self.telegram.send_photo(u["image"], u["caption"])
            except:
                self.telegram.send_message("Meme won't yeet")


    def bot_send_news(self, params):
        """Sends the first entries for new from r/"""
        subreddit_name = "worldnews"
        subnames = {
            "germany" : "germannews",
            "france" : "francenews",
            "europe" : "eunews",
            "usa" : "usanews"
        }
        if len(params) == 1:
            try:
                subreddit_name = subnames[str(params[0]).lower()]
            except:
                self.telegram.send_message("Argument not supported")
                return
        elif len(params) > 1:
            self.telegram.send_message("News takes one argument: the location (world, germany, europe, ...)")
            return

        text = reddit.get_top(subreddit_name, 10, "text")
        self.telegram.send_message(text)


#######################################################################

bot = ChatBot("ChatterBot", version="1.03")
