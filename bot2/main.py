# TODO remove in the end
import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

#from .commands import *
from . import api, commands

class ChatBot():
    """better framwork - unites all functions"""

    def __init__(self, name, version, hw_commands, prst, logger):
        """Inits the Bot with a few conf. vars
        Args:   -> name:str - Name of the bot
                -> version:str - Version number
                -> hw_commands - dict with commands executable by the clock module
                -> prst:dict - persistence (overloaded dict that writes to json file)
                -> logger - logging object to unify log messages
        """
        
        # Import submodules
        self.api_weather = api.weather.WeatherFetch(api.keys.weather_api)
        # self.reddit_api = api.reddit.RedditFetch()
        # and so on

        # Mark them as available
        self.help_module = commands.help.Help()
        self.sub_modules = {
            "weather": commands.weather.Weather(self.api_weather),
            "help" : self.help_module,
            "status" : commands.status.Status(name, version, prst, logger),

            }
        #     "log" : self.bot_print_log,
        #     "lorem" : self.bot_print_lorem,
        #     "weather" : self.bot_show_weather,
        #     "google" : self.bot_google_search,
        #     "events" : self.bot_print_events,
        #     "wikipedia" : self.bot_show_wikipedia,
        #     "zvv" : self.bot_zvv,
        #     "cronjob" : self.bot_cronjob,
        #     "joke" : self.bot_tell_joke,
        #     "meme" : self.bot_send_meme,
        #     "news" : self.bot_send_news,
        #     "list" : self.bot_list,
        #     "alias" : self.bot_save_alias,
        # }, **hw_commands)
        # concat bot_commands + hw-commands
        # must be a class that has a method create_handler

        self.telegram = Updater(api.keys.telegram_api, use_context=True)
        self.dispatcher = self.telegram.dispatcher

        self.add_commands()
        self.telegram.start_polling()
        self.telegram.idle()


    
    def add_commands(self):
        self.help_module.add_commands(self.sub_modules)
        for k in self.sub_modules:
            self.dispatcher.add_handler(self.sub_modules[k].create_handler())

