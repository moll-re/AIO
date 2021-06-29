import logging
import datetime
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
    def __init__(self, db):
        self.logger = logging.getLogger(__name__)
        self.db = db


    def log_activity(self, **kwargs):
        # mark that a new command has been executed
        data = self.db.chats(
            time=datetime.datetime.now(),
            **kwargs
            )
        # kwargs can look like
        # receive=True,
        # execute=True,
        # send=False,
        data.save()


