import datetime
from bot.api import telegram, google, weather, reddit

import requests
import socket
import numpy as np
import time
import json
import datetime
import emoji

import bot.framework as FW

class ChatBot(FW.BotFramework):
    """"""
    def __init__(self, name, version, prst, hw_commands):
        """Inits the Bot with a few conf. vars
        Args:   -> name:str - Name of the bot
                -> version:str - Version number
                -> prst:shelveObj - persistence
        """
        super().__init__(name, version, prst)
        
        # Available commands. Must be manually updated!
        self.commands = dict({
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
            "list" : self.bot_list,
            "alias" : self.bot_save_alias,
        }, **hw_commands)
        # concat bot_commands + hw-commands



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
        message = "BeebBop, this is " + self.name + " (V." + self.version + ")\n"
        try:
            ip = requests.get('https://api.ipify.org').text
        except:
            ip = "not fetchable"
        local_ips = [i[4][0] for i in socket.getaddrinfo(socket.gethostname(), None)]

        message += "<pre>Status: Running :green_circle:\n"
        message += "Uptime: " + delta[:delta.rfind(".")] + "\n"
        message += "Reboots: " + str(self.persistence["global"]["reboots"]) + "\n"
        message += "IP-Adress (public): " + ip + "\n"
        message += "IP-Adress (private): " + str(local_ips) + "\n"
        tot_r = np.array(self.persistence["bot"]["receive_activity"]["count"]).sum()
        message += "Total messages read: " + str(tot_r) + "\n"

        tot_s = np.array(self.persistence["bot"]["send_activity"]["count"]).sum()
        message += "Total messages sent: " + str(tot_s) + "\n"

        tot_e = np.array(self.persistence["bot"]["execute_activity"]["count"]).sum()
        message += "Commands executed " + str(tot_e) + "</pre>"

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
        
        categories = {"Clouds": ":cloud:", "Rain": ":cloud_with_rain:", "Thunderstorm": "thunder_cloud_rain", "Drizzle": ":droplet:", "Snow": ":cloud_snow:", "Clear": ":sun:", "Mist": "Mist", "Smoke": "Smoke", "Haze": "Haze", "Dust": "Dust", "Fog": "Fog", "Sand": "Sand", "Dust": "Dust", "Ash": "Ash", "Squall": "Squall", "Tornado": "Tornado",}
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        today = datetime.datetime.today().weekday()
        weather = self.weather.show_weather(city)
        
        now = weather.pop(0)
        message = "<b>Now:</b> " + categories[now["short"]] + "\n"
        message += ":thermometer: " + str(now["temps"][0]) + "°\n\n"

        for i, day in enumerate(weather):
            if i == 0:
                message += "<b>" + "Today" + ":</b> " + categories[day["short"]] + "\n"
            else:
                message += "<b>" + days[(today + i + 1) % 7] + ":</b> " + categories[day["short"]] + "\n"
            message += ":thermometer: :fast_down_button: " + str(day["temps"][0]) + "° , :thermometer: :fast_up_button: " + str(day["temps"][1]) + "°\n\n"

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

        if len(args) < 2:
            return "Please send a separator as the first argument, and the text afterwards.\nExample:\n/emojify :heart: Example text"

        sep = args[0]
        string_emoji = ""
        for word in args[1:]:
            out_string = self.emojify_word(word)
            string_emoji += out_string + sep

        return string_emoji


    def bot_show_help(self, *args):
        """Show a help message.
        
        Usage: help {keyword}
        Keywords:
        * no kw - list of all commands
        * full -  all commands and their docstring
        * command-name - specific command and its docstring
        """
        description = False
        if len(args) > 0:
            if args[0] == "full":
                description = True
            elif args[0] in self.commands:
                send_text = "<b>" + args[0] + "</b>\n"
                send_text += "<code>" + self.commands[args[0]].__doc__ + "</code>"
                return send_text

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
        """Show an error-log, mostly of bad api-requests.

        Usage: log {keyword}
        Keywords:
        * clear - clears log
        * system - shows python output
        """

        if "clear" in args:
            self.persistence["bot"]["log"] = []
            return "Log cleared"
        elif "system" in args:
            path="persistence/log.txt"
            try:
                file = open(path,"r")
                content = file.read()
                file.close()
                return content
            except:
                return "could not read File"
        
        send_text = ""
        for event in self.persistence["bot"]["log"]:
            send_text += event + "\n"
        if send_text == "":
            send_text += "No errors up to now"
        return send_text


    def bot_show_wikipedia(self, *args):
        """Shows the wikipedia entry for a given term
        
        Usage: wikipedia &lt;language&gt; &lt;term&gt;
        Keywords:
        * language - de, fr, en ...
        * term - search term, can consist of multiple words
        """
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

        Usage: zvv &lt;start&gt; 'to' &lt;finish&gt;
        Keywords:
        * start - start point (can be more than 1 word9
        * end - end point
        """
        if len(args) < 3:
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
        """ matches a list of two elements to a dict
            returns: {"int": number, "str": name}
        """
        r = {"int": 1, "str": "default"}
        print(args)
        if len(args) == 2:
            p1, p2 = args[0], args[1]
            try:
                try:
                    r1 = int(p1)
                    r2 = p2
                except:
                    r1 = int(p2)
                    r2 = p1

                r["int"] = r1
                r["str"] = r2

            except:
                self.write_bot_log("match_reddit_params", "could not match given params to known pattern")

        elif len(args) == 1:
            try:
                try:
                    r["int"] = int(args[0])
                except:
                    r["str"] = args[0]
            except:
                self.write_bot_log("match_reddit_params", "could not match given params to known pattern")

        return r


    def bot_tell_joke(self, *args):
        """Tells you the top joke on r/jokes
        
        Usage: joke {number}
        Keywords:
        * number - number of jokes
        """

        params_sorted = self.match_reddit_params(*args)

        number = params_sorted["int"]

        if len(params_sorted) > 1:
            self.telegram.send_message("Ignored other params than number of jokes")

        joke = reddit.get_random_rising("jokes", number, "text")
        return joke


    def bot_send_meme(self, *args):
        """Sends a meme from r/"""
        subnames = {
            "default" : "memes", # general case
            "physics" : "physicsmemes",
            "dank" : "dankmemes",
            "biology" : "biologymemes",
            "math" : "mathmemes"
        }

        params_sorted = self.match_reddit_params(*args)

        number = params_sorted["int"]
        if params_sorted["str"] in subnames:
            subreddit_name = subnames[params_sorted["str"]]
        else:
            subreddit_name = subnames["default"]


        urls = reddit.get_random_rising(subreddit_name, number, "photo")
        for u in urls:
            try:
                self.telegram.send_photo(u["image"], u["caption"])
            except:
                self.write_bot_log("bot_send_meme", "could not send image")
                return "Meme won't yeet"

        return ""


    def bot_send_news(self, *args):
        """Sends the first entries for new from r/"""
        subnames = {
            "default" : "worldnews",
            "germany" : "germannews",
            "france" : "francenews",
            "europe" : "eunews",
            "usa" : "usanews"
        }


        params_sorted = self.match_reddit_params(*args)

        number = params_sorted["int"]
        if params_sorted["str"] in subnames:
            subreddit_name = subnames[params_sorted["str"]]
        else:
            subreddit_name = subnames["default"]

        text = reddit.get_top(subreddit_name, number, "text")
        return text


    def bot_list(self, *args):
        """Interacts with a list (like a shopping list eg.)
        
        Usage list &lt;name&gt; &lt;action&gt; {object}
        Keyword:
        * name - name of list
        * action - create, delete, all, print, clear, add, remove
        * object - might not be needed: index to delete, or item to add

        Example usage:
        list create shopping : creates list name shopping
        list shopping add bread : adds bread to the list
        list shopping print
        list shopping clear
        list all
        """
        output = ""
        # args = list(args)
        if len(args) == 0:
            return "Missing parameters"
        try:
            if args[0] == "all":
                try:
                    return "Existing lists are: " + " ".join(list(self.persistence["global"]["lists"].keys()))
                except:
                    return "No lists created."
            if len(args) < 2:
                return "Missing parameters"
            if args[0] == "create":
                lname = " ".join(args[1:])
                self.persistence["global"]["lists"][lname] = []
                output = "Created list " + lname
            elif args[0] == "delete":
                lname = " ".join(args[1:])
                self.persistence["global"]["lists"].pop(lname, None) # no error if key doesnt exist
                output = "Deleted list " + lname
            else:
                lname = args[0]
                act = args[1]
                if act == "print":
                    sl = self.persistence["global"]["lists"][lname]
                    output += "Content of " + lname + ":\n"
                    for ind,thing in enumerate(sl):
                        output += str(ind+1) + ". " + thing + "\n"
                elif act == "clear":
                    self.persistence["global"]["lists"][lname] = []
                    output = "Cleared list " + lname
                elif act == "add":
                    if len(args) < 3:
                        return "Missing paramaeter"
                    add = " ".join(args[2:])
                    self.persistence["global"]["lists"][lname] += [add]
                    return "Added " + add + "."
                elif act == "remove":
                    if len(args) < 3:
                        return "Missing paramaeter"
                    try:
                        ind = int(args[2]) - 1
                        item = self.persistence["global"]["lists"][lname].pop(ind)
                        return "Removed " + item + " from list " + lname + "."
                    except:
                        return "Couldn't remove item."
                    return "Not working yet"
        except:
            output = "Could not handle your request. Maybe check the keys?"
        return output


    def bot_save_alias(self, *args):
        """Save a shortcut for special commands (+params)

        Usage: alias &lt;alias-name&gt; {&lt;alias-name&gt; &lt;command&gt;}
        Keywords:
        * action - all, add, delete or clear (deleta all)
        * alias-name - short name
        * command - command to be executed, can contain arguments for the command
        Example usage:
        * alias sa list shopping add
        * alias sp list shopping print
        Means that '/sa ...' will now be treated as if typed '/list shopping add ...'
        """
        # args = list(args)
        if len(args) == 0:
            return "Missing parameters"
        try:
            if args[0] == "clear":
                self.persistence["bot"]["aliases"] = {}
                return "All aliases cleared"
            elif args[0] == "all":
                try:
                    output = "Existing aliases are:\n"
                    for j, k in self.persistence["bot"]["aliases"].items():
                        output += j + " -&gt; " + k + "\n"
                    return output
                except:
                    return "No aliases created."

            if len(args) < 2:
                return "Missing parameters"
            if args[0] == "delete":
                ak = args[1]
                self.persistence["bot"]["aliases"].pop(ak, None) # no error if key doesnt exist
                return "Deleted alias " + ak

            if len(args) < 3:
                return "Missing parameters"
            if args[0] == "add":
                ak = args[1]
                cmd = " ".join(args[2:])
                self.persistence["bot"]["aliases"][ak] = cmd
                return "Created alias for " + ak

        except:
            return "Could not handle your request. Maybe check the keys?"
        return "Bad input..."
