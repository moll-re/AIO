from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

from . import api, commands

import logging
logger = logging.getLogger(__name__)

class ChatBot():
    """better framwork - unites all functions"""

    def __init__(self, name, version, prst):
        """Inits the Bot with a few conf. vars
        Args:   -> name:str - Name of the bot
                -> version:str - Version number
                -> hw_commands - dict with commands executable by the clock module
                -> prst:dict - persistence (overloaded dict that writes to json file)
                -> logger - logging object to unify log messages
        """
        # added by the launcher, we have self.modules (dict)
        
        self.persistence = prst
        # Import submodules
        self.api_weather = api.weather.WeatherFetch(api.keys.weather_api)
        # self.reddit_api = api.reddit.RedditFetch()
        # and so on

        self.telegram = Updater(api.keys.telegram_api, use_context=True)
        self.dispatcher = self.telegram.dispatcher
        self.commands = commands


        # Mark them as available
        self.help_module = self.commands.help.Help(prst)
        self.sub_modules = {
            "weather": self.commands.weather.Weather(self.api_weather, prst),
            "help" : self.help_module,
            "status" : self.commands.status.Status(name, version, prst),
            "zvv" : self.commands.zvv.Zvv(prst),
            "list" : self.commands.lists.Lists(prst),
            #"alias" : commands.alias.Alias(self.dispatcher, prst),
            "plaintext" : self.commands.plaintext.Plain(prst) # for handling non-command messages that should simply contribute to statistics
            }
            
        #     "events" : self.bot_print_events,
        #     "wikipedia" : self.bot_show_wikipedia,
        #     "cronjob" : self.bot_cronjob,
        #     "joke" : self.bot_tell_joke,
        #     "meme" : self.bot_send_meme,
        #     "news" : self.bot_send_news,
        # }
        # must be a class that has a method create_handler
    
    def add_commands(self):
        for k in self.sub_modules:
            self.dispatcher.add_handler(self.sub_modules[k].create_handler())

        self.help_module.add_commands(self.sub_modules)
    	
    def start(self):
        self.sub_modules = {**{"clock" : self.commands.clock.Clock(self.persistence, self.modules["clock"])}, **self.sub_modules}
        self.add_commands()
        self.telegram.start_polling()
        # self.telegram.idle()
