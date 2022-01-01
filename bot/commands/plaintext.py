from .template import *


class Plain(BotFunc):
    """Not a command: just keeps logs and usage_data"""
    def __init__(self, db_utils):
        super().__init__(db_utils)
    
    def create_handler(self):
        h = MessageHandler(Filters.text, callback=self.add_to_log)
        return h

    def add_to_log(self, update: Update, context: CallbackContext) -> None:
        super().entry_point(update, context)
        super().log_activity(
            read = True,
            send = False,
            execute = False
        )
