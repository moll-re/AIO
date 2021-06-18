from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

from . import api, commands

import logging
logger = logging.getLogger(__name__)

class ChatBot():
    """better framwork - unites all functions"""

    def __init__(self, name, version):
        """Inits the Bot with a few conf. vars
        Args:   -> name:str - Name of the bot
                -> version:str - Version number
                -> hw_commands - dict with commands executable by the clock module
                -> prst:dict - persistence (overloaded dict that writes to json file)
                -> logger - logging object to unify log messages
        """
        # added by the launcher, we have self.modules (dict) and persistence

        self.name = name
        self.version = version
        
        # Import submodules
        self.api_weather = api.weather.WeatherFetch(api.keys.weather_api)
        self.api_reddit = api.reddit.RedditFetch(api.keys.reddit_api)
        self.api_search = api.search.WebSearch()
        self.api_art = api.metmuseum.ArtFetch()
        # and so on

        self.telegram = Updater(api.keys.telegram_api, use_context=True)
        self.dispatcher = self.telegram.dispatcher
        self.commands = commands


        
    def add_commands(self):
        # Mark modules as available
        prst = self.persistence
        self.help_module = self.commands.help.Help(prst)
        self.sub_modules = {
            "weather": self.commands.weather.Weather(self.api_weather, prst),
            "help" : self.help_module,
            "status" : self.commands.status.Status(self.name, self.version, prst),
            "zvv" : self.commands.zvv.Zvv(prst),
            "list" : self.commands.lists.Lists(prst),
            # "alias" : commands.alias.Alias(self.dispatcher, prst),
            "joke" : self.commands.reddit.Joke(self.api_reddit, prst),
            "meme" : self.commands.reddit.Meme(self.api_reddit, prst),
            # "news" : self.commands.reddit.News(self.api_reddit, prst),
            "search" : self.commands.search.Search(self.api_search, prst),
            # ...

            "plaintext" : self.commands.plaintext.Plain(prst) # for handling non-command messages that should simply contribute to statistics
            }
        # must be a class that has a method create_handler
    
        for k in self.sub_modules:
            self.dispatcher.add_handler(self.sub_modules[k].create_handler())

        self.help_module.add_commands(self.sub_modules)
    	
    def start(self):
        self.sub_modules = {"clock" : self.commands.clock.Clock(self.persistence, self.modules["clock"], self.api_art)}
        self.add_commands()
        self.telegram.start_polling()
        # self.telegram.idle()
