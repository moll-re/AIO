import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ParseMode
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, Filters
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    CallbackContext,
)


import datetime


class BotFunc():
    """Base class for a specific bot-functionality"""
    def __init__(self, prst):
        self.logger = logging.getLogger(__name__)
        self.persistence = prst


    def entry_point(self):
        self.increase_counter("execute_activity")


    def increase_counter(self, counter_name):
        current_hour = int(datetime.datetime.now().timestamp() // 3600)
        if len(self.persistence["bot"][counter_name]["hour"]) == 0 or current_hour != self.persistence["bot"][counter_name]["hour"][-1]:
            self.persistence["bot"][counter_name]["hour"].append(current_hour)
            self.persistence["bot"][counter_name]["count"].append(1)
        else:
            self.persistence["bot"][counter_name]["count"][-1] += 1