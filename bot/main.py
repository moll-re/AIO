# -*- coding: utf-8 -*-

from bot.api import telegram, google, weather, reddit
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
        self.persistence = pvars.Variables("bot")
        # Uptime counter
        self.start_time = datetime.datetime.now()
        self.persistence.increment("reboots")

        # Available commands. Must be manually updated!
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

    def add_commands(self, commands):
        """adds new commands to an existing list"""
        self.commands = {**self.commands, **commands}
        self.telegram.update_commands(self.commands)


    def react_command(self, command, params):
        """"""
        result = self.commands[command](*params)
        #*params means the list is unpacked and handed over as separate arguments.
        self.telegram.send_message(result)


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

    def bot_print_lorem(self, *args):
        """Prints a placeholder text."""

        if "full" in args:
            message = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. At tellus at urna condimentum mattis pellentesque id nibh. Convallis aenean et tortor at risus viverra adipiscing at in. Aliquet risus feugiat in ante metus dictum. Tincidunt augue interdum velit euismod in pellentesque massa placerat duis. Tincidunt vitae semper quis lectus nulla at. Quam nulla porttitor massa id neque aliquam vestibulum morbi blandit. Phasellus egestas tellus rutrum tellus pellentesque eu tincidunt. Gravida rutrum quisque non tellus orci. Adipiscing at in tellus integer feugiat. Integer quis auctor elit sed vulputate mi sit amet mauris. Risus pretium quam vulputate dignissim suspendisse in est. Cras fermentum odio eu feugiat pretium. Ut etiam sit amet nisl purus in mollis nunc sed. Elementum tempus egestas sed sed risus pretium quam. Massa ultricies mi quis hendrerit dolor magna eget."
        else:
            message = "Lorem ipsum dolor sit amet, bla bla bla..."
        return message


    def bot_print_status(self, *args):
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

        return message

        if "full" in args:
            self.bot_print_log()


    def bot_show_weather(self, *args):
        """Shows a weather-forecast for a given location"""
        if len(args) != 1:
            return "Invalid Syntax, please give one parameter, the location"

        locations = {"freiburg": [47.9990, 7.8421], "zurich": [47.3769, 8.5417], "mulhouse": [47.7508, 7.3359]}
        loc = args[0]
        if loc.lower().replace("ü","u") in locations:
            city = locations[loc.lower().replace("ü","u")]
        else:
            return "Couldn't find city, it might be added later though."

        message = weather.show_weather(city)

        return message


    def bot_google_search(self, *args):
        """Does a google search and shows relevant links"""
        if len(args) < 1:
            return "Please tell me what to look for"

        send_string = google.query(args)
        return send_string


    def bot_print_events(self, *args):
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

        return send_string


    def bot_emojify(self, *args):
        """Converts a string to emojis"""

        if len(params) < 2:
            return "Please send a separator as the first argument, and the text afterwards.\nExample:\n/emojify :heart: Example text"

        sep = args[0]
        string_emoji = ""
        for word in args[1:]:
            out_string = self.emojify_word(word)
            string_emoji += out_string + sep

        return string_emoji


    def bot_show_help(self, *args):
        """Shows a list of all commands and their description"""
        description = False
        if "verbose" in args:
            description = True

        send_text = "BeebBop, this is " + self.name + " (V." + self.version + ")\n"
        send_text += "Here is what I can do up to now: \n"

        entries = sorted(list(self.commands.keys()))
        for entry in entries:
            send_text += "<b>" + entry + "</b>"
            if description:
                send_text += " - <code>" + self.commands[entry].__doc__ + "</code>\n\n"
            else:
                send_text += "\n"
        return send_text


    def bot_print_log(self, *args):
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
        return send_text


    def bot_show_wikipedia(self, *args):
        """Shows the wikipedia entry for a given term"""
        if len(args) == 0:
            return "Please provide the first argument for language (de or fr or en or ...) and then your query"
        args = list(args)
        if len(args) >= 2:
            url = "https://" + args.pop(0) + ".wikipedia.org/wiki/" + args.pop(0)
            for word in args:
                url +=  "_" + word
        else:
            url = "https://en.wikipedia.org/wiki/" + args[0]

        print(url)
        r = requests.get(url)
        if r.status_code == 404:
            return "No result found for query (404)"

        return url


    def bot_zvv(self, *args):
        """Uses the swiss travel api to return the best route between a start- and endpoint.
        usage: <start> to <finish>"""
        if len(args) <= 3:
            return "Please specify a start- and endpoint as well as a separator (the 'to')"

        url = "http://transport.opendata.ch/v1/connections"
        args = list(args)
        goal = " ".join(args[:args.index("to")])
        dest = " ".join(args[args.index("to")+1:])

        data = {"from" : goal, "to" : dest, "limit" : 2}
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
            return text
        except:
            return "Invalid api call."


    def bot_cronjob(self, params):
        """Allows you to add a timed command, in a crontab-like syntax. Not implemented yet.
        Example usage: /cronjob add 0 8 * * * weather Zürich
        """
        return "I'm not functional yet. But when I am, it is gonna be legendary!"


    def match_reddit_params(self, *args):
        """matches a list of two elements to one int and one string
        returns int, string or invalid, invalid
        """
        if len(args) == 2:
            p1 = args[0], p2 = args[1]
            try:
                try:
                    r1 = int(p1)
                    r2 = p2
                except:
                    r2 = int(p2)
                    r1 = p1
            except:
                return None

            return [r1, r2]
        elif len(args) == 1:
            try:
                r1 = int(args[0])
            except:
                return None
            return [r1]


    def bot_tell_joke(self, *args):
        """Tells you the top joke on r/jokes"""

        number = 1
        params_sorted = self.match_reddit_params(*args)
        if params_sorted != None:
            if len(params_sorted) >= 1:
                number = params_sorted[0]
            if len(params_sorted) > 1:
                self.telegram.send_message("Please only specify one argument: the number of jokes")


        joke = reddit.get_random_rising("jokes", number, "text")
        return joke


    def bot_send_meme(self, *args):
        """Sends a meme from r/"""
        subreddit_name = "memes"
        subnames = {
            "physics" : "physicsmemes",
            "dank" : "dankmemes",
            "biology" : "biologymemes",
            "math" : "mathmemes"
        }

        number = 1
        params_sorted = self.match_reddit_params(*args)
        if params_sorted != None:
            if len(params_sorted) >= 1:
                number = params_sorted[0]
            if len(params_sorted) >= 2:
                subreddit_name = params_sorted[1]
            if len(args) > 2:
                self.telegram.send_message("Memes takes 2 parameters: the number of memes, and their topic.")

        urls = reddit.get_random_rising(subreddit_name, number, "photo")
        for u in urls:
            try:
                self.telegram.send_photo(u["image"], u["caption"])
                return ""
            except:
                return "Meme won't yeet"


    def bot_send_news(self, *args):
        """Sends the first entries for new from r/"""
        subnames = {
            "germany" : "germannews",
            "france" : "francenews",
            "europe" : "eunews",
            "usa" : "usanews"
        }
        if len(params) == 0:
            subreddit_name = "worldnews"
        else:
            params_sorted = self.match_reddit_params(*args)
            if params_sorted != None:
                if len(params_sorted) >= 1:
                    number = params_sorted[0]
                if len(params_sorted) > 1:
                    return "Please only specify one argument: the location"


        text = reddit.get_top(subreddit_name, 10, "text")
        return text
