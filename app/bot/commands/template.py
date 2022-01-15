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
    def __init__(self, db_utils):
        self.logger = logging.getLogger(__name__)
        self.db_utils = db_utils

    def log_activity(self, **kwargs):
        # mark that a new command has been executed
        self.db_utils.sensor_log(**kwargs)

    def entry_point(self, update: Update, context: CallbackContext) -> None:
        if update.message.text:
            self.logger.info("Chat said: {}".format(update.message.text))
        else:
            self.logger.info("Chat said: {}".format(update.message))

