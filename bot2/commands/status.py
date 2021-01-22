from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    CallbackContext,
)

import datetime
import requests
import socket
import numpy as np
FIRST = 1

class Status():
    """Shows a short status of the program."""
    
    def __init__(self, name, version, prst, logger):
        self.start_time = datetime.datetime.now()
        self.name = name
        self.version = version
        self.persistence = prst
        self.logger = logger

    def create_handler(self):
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('status', self.entry_point)],
            states={
                FIRST: [
                    CallbackQueryHandler(self.print_status, pattern="^status-"),
                ]
            },
            fallbacks=[CommandHandler('status', self.entry_point)],
        )
        return conv_handler


    def entry_point(self, update: Update, context: CallbackContext) -> None:
        user = update.message.from_user
        keyboard = [
            [
                InlineKeyboardButton("Status", callback_data="status-simple"),
                InlineKeyboardButton("With log", callback_data="status-full"),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text("What exactly do you want?", reply_markup=reply_markup)
        return FIRST


    def print_status(self, update: Update, context: CallbackContext) -> None:
        query = update.callback_query
        wanted = query.data.replace("status-","")
        query.answer()

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

        message += "<pre>Status: Running 🟢\n"
        message += "Uptime: " + delta[:delta.rfind(".")] + "\n"
        message += "Reboots: " + str(self.persistence["global"]["reboots"]) + "\n"
        message += "IP (public): " + ip + "\n"
        message += "IP (private): " + str(local_ips) + "\n"
        tot_r = np.array(self.persistence["bot"]["receive_activity"]["count"]).sum()
        message += "Total messages read: " + str(tot_r) + "\n"

        tot_s = np.array(self.persistence["bot"]["send_activity"]["count"]).sum()
        message += "Total messages sent: " + str(tot_s) + "\n"

        tot_e = np.array(self.persistence["bot"]["execute_activity"]["count"]).sum()
        message += "Commands executed " + str(tot_e) + "</pre>\n"

        if wanted == "full":
            message += str(dir(self.logger))

        query.edit_message_text(
            text= message
        )

        return ConversationHandler.END
