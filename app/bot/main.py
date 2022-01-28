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
        # added by the launcher, we have self.modules (dict) and persistence and db_utils

        self.name = name
        self.version = version
        
        # Import apis
        self.api_weather = api.weather.WeatherFetch(api.apikeys.weather_api)
        self.api_reddit = api.reddit.RedditFetch(api.apikeys.reddit_api)
        self.api_search = api.search.WebSearch()
        self.api_art = api.metmuseum.ArtFetch()
        # and so on

        self.telegram = Updater(api.apikeys.telegram_api, use_context=True)
        self.dispatcher = self.telegram.dispatcher


        
    def add_commands(self):
        # Mark modules as available
        db = self.db_utils
        # self.help_module = commands.help.Help(db)
        self.sub_modules = {
            "weather": commands.weather.Weather(self.api_weather, db),
            "help" : commands.help.Help(db),
            "status" : commands.status.Status(self.name, self.version, db),
            "zvv" : commands.zvv.Zvv(db),
            "list" : commands.lists.Lists(db),
            # "alias" : commands.alias.Alias(self.dispatcher, db),
            "joke" : commands.reddit.Joke(self.api_reddit, db),
            "meme" : commands.reddit.Meme(self.api_reddit, db),
            "search" : commands.search.Search(self.api_search, db),
            "clock" : commands.clock.Clock(self.api_art, self.modules["clock"], db),
            # ...
            "plaintext" : commands.plaintext.Plain(db)
            # for handling non-command messages that should simply contribute to statistics
            }
        # must be a class that has a method create_handler
    
        for k in self.sub_modules:
            self.dispatcher.add_handler(self.sub_modules[k].create_handler())

        # self.help_module.add_commands(self.sub_modules)
        self.sub_modules["help"].add_commands(self.sub_modules)

    	
    def start(self):
        self.add_commands()
        self.telegram.start_polling(
            poll_interval=0.2,
        )
        self.telegram.idle()
