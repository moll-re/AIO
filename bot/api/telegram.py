import emoji
import requests
import datetime

import bot.api.keys


class TelegramIO():
    def __init__(self, persistence):
        """Inits the Telegram-Interface
        """
        self.base_url = "https://api.telegram.org/bot" + bot.api.keys.telegram_api + "/"
        self.persistence = persistence
        # Dynamic variables for answering
        self.chat_id = ""
        self.offset = 0
        self.message_id = ""
        self.message_queue = []


    def update_commands(self,commands):
        self.commands = commands

    ########################################################################
    """Helper-Functions"""


    def fetch_updates(self):
        """"""
        update_url = self.base_url + "getUpdates"
        data = {"offset":self.offset}

        try:
            result = requests.post(update_url,data=data)
            result = result.json()["result"]
            self.message_queue = result
        except:
            result = []

        return len(result)


    def process_message(self):
        """Inspects the first message from self.message_queue and reacts accordingly."""
        message_data = self.message_queue.pop(0)
        
        self.increase_counter("receive_activity")
        
        self.offset = message_data["update_id"] + 1

        if "edited_message" in message_data:
            return

        message = message_data["message"]
        self.message_id = message["message_id"]
        self.chat_id = message["chat"]["id"]
        author = message["from"]
        
        if str(author["id"]) not in self.persistence["bot"]["chat_members"]:
            name = ""
            if "first_name" in author:
                name += author["first_name"] + " "
            if "last_name" in author:
                name += author["last_name"]
            if len(name) == 0:
                name = "anonymous"
            self.persistence["bot"]["chat_members"][str(author["id"])] = name # seems like the conversion to string is handled implicitly, but it got me really confused
            self.send_message("Welcome to this chat " + name + "!")

        if "text" in message:
            print("Chat said: ", emoji.demojize(message["text"]))

            if "entities" in message:
                for entry in message["entities"]:
                    if entry["type"] == "bot_command":
                        return message["text"] #self.handle_command(message["text"][1:])

        elif "photo" in message:
            print("Photo received, what do I do?")

        return


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

        if message == "" or message == None:
            return

        print("SENDING: " + message)
        # message = message.replace("<","&lt;").replace(">", "&gt;")
        # TODO: sanitize input but keep relevant tags
        data = {
            'chat_id': self.chat_id,
            'text': emoji.emojize(message),
            "parse_mode": "HTML",
            "reply_to_message_id" : self.message_id,
        }

        send_url = self.base_url + "sendMessage"
        try:
            r = requests.post(send_url, data=data)
            if (r.status_code != 200):
                raise Exception

            self.increase_counter("send_activity")
        except:
            out = datetime.datetime.now().strftime("%d.%m.%y - %H:%M")
            out += " @ " + "telegram.send_message"
            out += " --> " + "did not send:\n" + message
            self.persistence["bot"]["log"] += [out]
            

    def send_photo(self, url, caption):
        print("SENDING PHOTO: " + url)
        data = {
            'chat_id': self.chat_id,
            'photo': url,
            "parse_mode": "HTML",
            "reply_to_message_id" : self.message_id,
            'caption' : caption,
        }
        send_url = self.base_url + "sendPhoto"
        try:
            r = requests.post(send_url, data=data)
            self.increase_counter("send_activity")
        except:
            out = datetime.datetime.now().strftime("%d.%m.%y - %H:%M")
            out += " @ " + "telegram.send_photo"
            out += " --> " + "did not send:\n" + url
            self.persistence["bot"]["log"] += [out]

    def increase_counter(self, counter_name):
        current_hour = int(datetime.datetime.now().timestamp() // 3600)
        if len(self.persistence["bot"][counter_name]["hour"]) == 0 or current_hour != self.persistence["bot"][counter_name]["hour"][-1]:
            self.persistence["bot"][counter_name]["hour"].append(current_hour)
            self.persistence["bot"][counter_name]["count"].append(1)
        else:
            self.persistence["bot"][counter_name]["count"][-1] += 1