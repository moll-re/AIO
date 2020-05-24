# -*- coding: utf-8 -*-

import key
import requests
import time
import json
import datetime
import googlesearch
import emoji

from persistence import PersistentVars

class ChatBot():

    def __init__(self, name, api_key, version):
        """Inits the Bot with a few conf. vars
        Args:   -> name:str - Name of the bot
                -> api_key:str - t.me api-key
                -> version:str - Version number
        """

        self.base_url = "https://api.telegram.org/bot" + api_key + "/"
        self.version = version
        self.name = name

        # Persisten variable
        self.persistence = PersistentVars("permanent_vars.json")

        # Uptime counter
        self.start_time = datetime.datetime.now()
        self.persistence.write("reboots", self.persistence.read("reboots")+1)


        # Dynamic variables for answering
        self.chat_id = ""
        self.offset = 0
        self.message_id = ""


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
        }

        self.message_loop()


    def message_loop(self):
        """"""
        while(True):
            result = self.fetch_updates()
            if len(result) != 0:
                self.handle_result(result)
            time.sleep(5)


    def fetch_updates(self):
        """"""
        update_url = self.base_url + "getUpdates"
        data = {"offset":self.offset}

        try:
            result = requests.post(update_url,data=data)
            result = result.json()["result"]
        except:
            result = ""

        return result


    def handle_result(self, result):
        """Inspects the message and reacts accordingly. Can easily be extended"""
        for message_data in result:
            message_read = self.persistence.read("message_read")
            self.persistence.write("message_read", message_read + 1)
            self.offset = message_data["update_id"] + 1
            message = message_data["message"]
            self.message_id = message["message_id"]
            self.chat_id = message["chat"]["id"]
            author = message["from"]

            chat_members = self.persistence.read("chat_members")
            if str(author["id"]) not in chat_members:
                name = ""
                if "first_name" in author:
                    name += author["first_name"] + " "
                if "last_name" in author:
                    name += author["last_name"]
                if len(name) == 0:
                    name += "anonymous"
                chat_members[author["id"]] = name
                self.persistence.write("chat_members", chat_members)
                self.send_message("Welcome to this chat " + name + "!")

            if "text" in message:
                print("Chat said: ", emoji.demojize(message["text"]))

                if "entities" in message:
                    for entry in message["entities"]:
                        if entry["type"] == "bot_command":
                            self.handle_command(message["text"][1:])

            elif "photo" in message:
                print("Photo received, what do I do?")


    def handle_command(self, command):
        """Handles commands and stuff, using a bash-like syntax:
        /[command] [argument 1] [argument 2] ...
        """
        full = command.split(" ")
        if full[0] in self.commands:
            self.commands[full[0]](full[1:])
        else:
            self.send_message("Command <code>" + full[0] + "</code> not found. Please try again.")

    def send_thinking_note(self):
        data = {
            "chat_id" : self.chat_id,
            "action" : "typing",
        }
        send_url = self.base_url + "sendChatAction"
        try:
            r = requests.post(send_url, data=data)
        except:
            print("Could not show that I'm thinking =(")

    def send_message(self, message):
        print("SENDING: " + emoji.demojize(message))

        data = {
            'chat_id': self.chat_id,
            'text': emoji.emojize(message),
            "parse_mode": "HTML",
            "reply_to_message_id" : self.message_id,
        }
        send_url = self.base_url + "sendMessage"
        try:
            r = requests.post(send_url, data=data)
        except:
            log = self.persistence.read("log")
            log.append(str(datetime.datetime.now()) + " - did not send:\n" + message)
            self.persistence.write("log", log)
        message_sent = self.persistence.read("message_sent")
        self.persistence.write("message_sent", message_sent + 1)




    ############################################################################
    """Command-implementation"""

    def bot_print_lorem(self, params):
        """Prints a placeholder text."""
        if "full" in params:
            message = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. At tellus at urna condimentum mattis pellentesque id nibh. Convallis aenean et tortor at risus viverra adipiscing at in. Aliquet risus feugiat in ante metus dictum. Tincidunt augue interdum velit euismod in pellentesque massa placerat duis. Tincidunt vitae semper quis lectus nulla at. Quam nulla porttitor massa id neque aliquam vestibulum morbi blandit. Phasellus egestas tellus rutrum tellus pellentesque eu tincidunt. Gravida rutrum quisque non tellus orci. Adipiscing at in tellus integer feugiat. Integer quis auctor elit sed vulputate mi sit amet mauris. Risus pretium quam vulputate dignissim suspendisse in est. Cras fermentum odio eu feugiat pretium. Ut etiam sit amet nisl purus in mollis nunc sed. Elementum tempus egestas sed sed risus pretium quam. Massa ultricies mi quis hendrerit dolor magna eget."
        else:
            message = "Lorem ipsum dolor sit amet, bla bla bla..."
        self.send_message(message)


    def bot_print_status(self, params):
        """Prints the bots current status and relevant information"""
        delta = str(datetime.datetime.now() - self.start_time)
        message = "<pre>Status: Running :green_circle:\n"
        message += "Uptime: " + delta + "\n"
        message += "Reboots: " + str(self.persistence.read("reboots")) + "\n"
        message += "Messages read: " + str(self.persistence.read("message_read")) + "\n"
        message += "Messages sent: " + str(self.persistence.read("message_sent")) + "</pre>"
        self.send_message(message)
        if "full" in params:
            self.bot_print_log([])


    def bot_show_weather(self, params):
        """Shows a weather-forecast for a given location"""
        if len(params) != 1:
            self.send_message("Invalid Syntax, please give one parameter, the location")
            return

        locations = {"freiburg": [47.9990, 7.8421], "zurich": [47.3769, 8.5417], "mulhouse": [47.7508, 7.3359]}
        if params[0].lower().replace("ü","u") in locations:
            city = locations[params[0].lower().replace("ü","u")]
        else:
            self.send_message("Couldn't find city, it might be added later though.")
            return
        url = "https://api.openweathermap.org/data/2.5/onecall?"
        data = {"lat" : city[0], "lon" : city[1], "exclude" : "minutely,hourly", "appid" : key.weather_api, "units" : "metric"}

        try:
            weather = requests.get(url,params=data).json()
        except:
            self.send_message("Query failed, it's my fault, I'm sorry :sad:")
            return

        categories = {"Clouds": ":cloud:", "Rain": ":cloud_with_rain:", "Thunderstorm": "thunder_cloud_rain", "Drizzle": ":droplet:", "Snow": ":cloud_snow:", "Clear": ":sun:", "Mist": "Mist", "Smoke": "Smoke", "Haze": "Haze", "Dust": "Dust", "Fog": "Fog", "Sand": "Sand", "Dust": "Dust", "Ash": "Ash", "Squall": "Squall", "Tornado": "Tornado",}
        now = weather["current"]
        message = "<b>Now:</b> " + categories[now["weather"][0]["main"]] + "\n"
        message += ":thermometer: " + str(int(now["temp"])) + "°\n\n"
        for i, day in enumerate(weather["daily"]):
             message += "<b>+" + str(i+1) + ":</b> " + categories[day["weather"][0]["main"]] + "\n"
             message += ":thermometer: :fast_down_button: " + str(int(day["temp"]["min"])) + "° , :thermometer: :fast_up_button: " + str(int(day["temp"]["max"])) + "°\n\n"

        self.send_message(message)


    def bot_google_search(self, params):
        """Does a google search and shows relevant links"""
        if len(params) < 1:
            self.send_message("Please tell me what to look for")
            return

        param_string = ""
        for word in params:
            param_string += word + "+"
        param_string = param_string[:-1]
        search_url = "https://google.com/search?q=" + param_string

        try:
            res = googlesearch.search(param_string.replace("+"," ") ,num=5,start=0,stop=5)
            send_string = "Google search for <b>" + param_string.replace("+"," ") + "</b>:\n"
            for url in res:
                send_string += url + "\n\n"
            send_string += "Search url:\n" + search_url
        except:
            send_string = "Search url:\n" + search_url
        self.send_message(send_string)


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

        self.send_message(send_string)


    def bot_emojify(self, params):
        """Converts a string to emojis"""

        if len(params) < 2:
            self.send_message(emoji.emojize("Please send a separator as the first argument, and the text afterwards.\nExample:\n/emojify :heart: Example text"))
        sep = params[0]
        emoji_dict = {"a" : ":regional_indicator_symbol_letter_a:","b" : ":regional_indicator_symbol_letter_b:","c" : ":regional_indicator_symbol_letter_c:","d" : ":regional_indicator_symbol_letter_d:","e" : ":regional_indicator_symbol_letter_e:","f" : ":regional_indicator_symbol_letter_f:","g" : ":regional_indicator_symbol_letter_g:","h" : ":regional_indicator_symbol_letter_h:","i" : ":regional_indicator_symbol_letter_i:","j" : ":regional_indicator_symbol_letter_j:","k" : ":regional_indicator_symbol_letter_k:","l" : ":regional_indicator_symbol_letter_l:","m" : ":regional_indicator_symbol_letter_m:","n" : ":regional_indicator_symbol_letter_n:","o" : ":regional_indicator_symbol_letter_o:","p" : ":regional_indicator_symbol_letter_p:","q" : ":regional_indicator_symbol_letter_q:","r" : ":regional_indicator_symbol_letter_r:","s" : ":regional_indicator_symbol_letter_s:","t" : ":regional_indicator_symbol_letter_t:","u" : ":regional_indicator_symbol_letter_u:","v" : ":regional_indicator_symbol_letter_v:","w" : ":regional_indicator_symbol_letter_w:","x" : ":regional_indicator_symbol_letter_x:","y" : ":regional_indicator_symbol_letter_y:","z" : ":regional_indicator_symbol_letter_z:"," " : sep}

        prep_string = ""
        for i in params[1:]:
            prep_string += i.lower() + " "
        out_string = ""
        for i in prep_string[:-1]:
            if i in emoji_dict:
                out_string += emoji_dict[i] + " "
            else:
                out_string += i
        self.send_message(out_string)


    def bot_show_help(self, params):
        """Shows a list of all commands and their description"""
        send_text = "Hello, this is " + self.name + ", V." + self.version + "\n"
        send_text += "Here is a list of the available commands:\n"
        for entry in self.commands:
            send_text += "<b>" + entry + "</b> - "
            send_text += "<code>" + self.commands[entry].__doc__ + "</code>\n\n"
        self.send_message(send_text)


    def bot_print_log(self, params):
        """Shows an error-log, mostly of bad api-requests"""
        if "clear" in params:
            self.persistence.write("log",[])
            self.send_message("Log cleared")
            return
        send_text = ""
        for event in self.persistence.read("log"):
            send_text += event + "\n"
        if send_text == "":
            send_text += "No errors up to now"
        self.send_message(send_text)


    def bot_show_wikipedia(self, params):
        """Shows the wikipedia entry for a given therm"""
        if len(params) > 2 or len(params) == 0:
            self.send_message("Please only search for one word at a time. 1rst param is for language (de or fr or en or ...)")
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
                self.send_message("No result found for query")
                return
        self.send_message(url)


    def bot_do_all(self,params):
        """Executes every single command with random params"""
        for key in self.commands:
            if key != "bot_do_all":
                	self.commands[key](["en","Freiburg"])



    def bot_zvv(self,params):
        """Uses the swiss travel api to return the best route between a start- and endpoint in Zurich (actually whole Switzerland, but I haven't tested that)"""
        if len(params) != 2:
            self.send_message("Please give me your start and endpoint")
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
                text += ":world_map: \n"

                for step in con["sections"]:
                    if step["journey"] != None:
                        text += step["journey"]["passList"][0]["station"]["name"] + " (" + datetime.datetime.fromtimestamp(int(step["journey"]["passList"][0]["departureTimestamp"])).strftime("%H:%M") + ")\n"
                        text += ":right_arrow: L. " + step["journey"]["number"] + " :right_arrow: \n"
                        text += step["journey"]["passList"][-1]["station"]["name"] + " (" + datetime.datetime.fromtimestamp(int(step["journey"]["passList"][-1]["arrivalTimestamp"])).strftime("%H:%M") +")\n"
                    else:
                        text += On foot. \n"
                text += "\n"
            self.send_message(text)
        except:
            self.send_message("Invalid api call.")



###########################
bot = ChatBot("ChatterBot", key.telegram_api, version="1.01")
