from .template import *

import datetime
import requests
import socket
import json


FIRST = 1

class Status(BotFunc):
    """Shows a short status of the program."""
    
    def __init__(self, name, version, db_utils):
        super().__init__(db_utils)
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
        super().entry_point(update, context)
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
        # message += "Reboots: `" + str(self.persistence["global"]["reboots"]) + "`\n"
        message += "IP (public): `" + ip + "`\n"
        message += "IP (private): `" + str(local_ips) + "`\n"
        u = str(self.get_ngrok_url())
        message += "URL: [" + u + "](" + u + ")\n"
        
        # TODO new DB
        tot_r = self.db_utils.chat_count("read")
        message += "Total messages read: `{}`\n".format(tot_r)

        tot_s = self.db_utils.chat_count("send")
        message += "Total messages sent: `{}`\n".format(tot_s)

        tot_e = self.db_utils.chat_count("execute")
        message += "Total commands executed: `{}`\n".format(tot_e)

        if update.message:
            update.message.reply_text(message, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)
        else:
            update._effective_chat.send_message(message, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)
        
        super().log_activity(read = True, execute = True, send = True)
        return FIRST


    def send_log(self, update: Update, context: CallbackContext) -> None:
        query = update.callback_query
        wanted = query.data.replace("status-","")
        query.answer()
        with open("persistence/server.log") as l:
            query.message.reply_document(l)

        super().log_activity(read = False, execute = False, send = True)
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
        except:
            return "Not available"