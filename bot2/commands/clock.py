from .template import *

CHOOSE, ARGS = range(2)

class Clock(BotFunc):
    """pass on commands to clock-module"""
    def __init__(self, prst, hw_commands):
        super().__init__(prst)
        self.hw_commands = hw_commands

    def create_handler(self):
        handler = ConversationHandler(
            entry_points=[CommandHandler("clock", self.entry_point)],
            states={
                CHOOSE : [],
                ARGS : []
            },
            fallbacks=[CommandHandler('clock', self.entry_point)],
        )
        return handler

    def entry_point(self):
        super().entry_point()