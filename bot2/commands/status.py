from .template import *

import datetime
import requests
import socket
import numpy as np
import os
import json


FIRST = 1

class Status(BotFunc):
    """Shows a short status of the program."""
    
    def __init__(self, name, version, prst):
        super().__init__(prst)
        self.start_time = datetime.datetime.now()
        self.name = name
        self.version = version

    def create_handler(self):
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('status', self.entry_point)],
            states={
                FIRST: [
                    CallbackQueryHandler(self.send_log, pattern="^full$"),
                ]
            },
            fallbacks=[CommandHandler('status', self.entry_point)],
        )
        return conv_handler


    def entry_point(self, update: Update, context: CallbackContext) -> None:
        super().entry_point()
        user = update.message.from_user
        keyboard = [
            [
                InlineKeyboardButton("And the log?", callback_data="full"),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        delta = str(datetime.datetime.now() - self.start_time)
        message = "BeebBop, this is " + self.name + " (V." + self.version + ")\n"

        try:
            ip = requests.get('https://api.ipify.org').text
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.connect(('8.8.8.8', 80))
                (addr, port) = s.getsockname()
            local_ips = addr
        except:
            ip = "not fetchable"
            local_ips = "not fetchable"

        message += "Status: Running 🟢\n"
        message += "Uptime: `" + delta[:delta.rfind(".")] + "`\n"
        message += "Reboots: `" + str(self.persistence["global"]["reboots"]) + "`\n"
        message += "IP (public): `" + ip + "`\n"
        message += "IP (private): `" + str(local_ips) + "`\n"
        u = str(self.get_ngrok_url())
        message += "URL: [" + u + "](" + u + "]\n"
        
        tot_r = np.array(self.persistence["bot"]["receive_activity"]["count"]).sum()
        message += "Total messages read: `" + str(tot_r) + "`\n"

        tot_s = np.array(self.persistence["bot"]["send_activity"]["count"]).sum()
        message += "Total messages sent: `" + str(tot_s) + "`\n"

        tot_e = np.array(self.persistence["bot"]["execute_activity"]["count"]).sum()
        message += "Commands executed `" + str(tot_e) + "`\n"

        update.message.reply_text(message, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)
        return FIRST


    def send_log(self, update: Update, context: CallbackContext) -> None:
        query = update.callback_query
        wanted = query.data.replace("status-","")
        query.answer()
        with open("persistence/complete.log") as l:
            query.message.reply_document(l)

        return ConversationHandler.END


    def get_ngrok_url(self):
        try:
            url = "http://localhost:4040/api/tunnels/"
            res = requests.get(url)
            res_unicode = res.content.decode("utf-8")
            res_json = json.loads(res_unicode)
            for i in res_json["tunnels"]:
                if i['name'] == 'command_line':
                    return i['public_url']
                    break
        except:
            return "Not available"