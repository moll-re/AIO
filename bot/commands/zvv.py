from .template import *

import datetime
import requests

START, DEST = range(2)

class Zvv(BotFunc):
    """Connects to the swiss travel-api to get public transport routes"""

    def __init__(self, db):
        super().__init__(db)
        self.start = ""
        self.dest = ""
        pass

    def create_handler(self):
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('zvv', self.entry_point)],
            states={
                START: [MessageHandler(Filters.text, callback=self.get_start)],
                DEST: [MessageHandler(Filters.text, callback=self.get_dest)]
            },
            fallbacks=[CommandHandler('zvv', self.entry_point)],
        )
        return conv_handler


    def entry_point(self, update: Update, context: CallbackContext) -> None:
        super().entry_point(update, context)
        update.message.reply_text("What is the start point?")
        return START


    def get_start(self, update: Update, context: CallbackContext) -> None:
        loc = update.message.text
        self.start = loc
        update.message.reply_text("Ok. Going from " + loc + ", what is the destination?")
        return DEST


    def get_dest(self, update: Update, context: CallbackContext) -> None:
        loc = update.message.text
        self.dest = loc
        route = self.get_result()
        update.message.reply_text("Here are the routes I've got:\n" + route)
        super().log_activity(read=True, execute=True, send=True)
        return ConversationHandler.END


    def get_result(self):
        url = "http://transport.opendata.ch/v1/connections"

        start = self.start
        dest = self.dest

        data = {"from" : start, "to" : dest, "limit" : 2}
        try:
            routes = requests.get(url, params=data).json()
            result = routes["connections"]
            text = result[0]["from"]["station"]["name"] + " ⏩ " + result[0]["to"]["station"]["name"] + "\n\n"
            for con in result:
                text += "Start: " + datetime.datetime.fromtimestamp(int(con["from"]["departureTimestamp"])).strftime("%d/%m - %H:%M") + "\n"
                text += "🏁 " + datetime.datetime.fromtimestamp(int(con["to"]["arrivalTimestamp"])).strftime("%d/%m - %H:%M") + "\n"
                text += "⏳ " + con["duration"] + "\n"
                text += "🗺️ Route:\n"

                for step in con["sections"]:
                    if step["journey"] != None:
                        text += step["journey"]["passList"][0]["station"]["name"] + " (" + datetime.datetime.fromtimestamp(int(step["journey"]["passList"][0]["departureTimestamp"])).strftime("%H:%M") + ")\n"

                        text += "➡️ Linie " + self.number_to_emoji(step["journey"]["number"]) + "\n"

                        text += step["journey"]["passList"][-1]["station"]["name"] + " (" + datetime.datetime.fromtimestamp(int(step["journey"]["passList"][-1]["arrivalTimestamp"])).strftime("%H:%M") +")\n"
                    else:
                        text += "Walk."
                text += "\n"
            return text
        except:
            return "Invalid api call."

    def number_to_emoji(self, number):
        out = ""
        numbers = ["0️⃣","1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣"]
        for i in str(number):
            out += numbers[int(i)]
        return str(out)