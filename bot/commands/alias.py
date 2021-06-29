from .template import *

FIRST = range(1)
class Alias(BotFunc):
    """create a new command for command-paths you often use"""

    def __init__(self, dispatcher, db):
        super().__init__(db)
        self.dispatcher = dispatcher
        # do not interact with him yet!

    def create_handler(self):
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('alias', self.entry_point)],
            states={
                FIRST: [
                    CallbackQueryHandler(self.print_all, pattern="^all$"),
                    CallbackQueryHandler(self.create_alias, pattern="^new$"),
                    CallbackQueryHandler(self.delete_alias, pattern='^delete$'),
                ]
            },
            fallbacks=[CommandHandler('alias', self.entry_point)],
        )
        return conv_handler


    def entry_point(self, update: Update, context: CallbackContext) -> None:
        test = self.dispatcher
        print(self.dispatcher.handlers[0])
        keyboard = [
            [InlineKeyboardButton("All aliases", callback_data="all")],
            [InlineKeyboardButton("Create new alias", callback_data="new")],
            [InlineKeyboardButton("Delete alias", callback_data="delete")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        super().log_activity(receive=True, execute=False, send=True)
        update.message.reply_text("What exactly do you want?", reply_markup=reply_markup)
        return FIRST
    

    def print_all(self, update: Update, context: CallbackContext) -> None:
        query = update.callback_query
        query.answer()

        all_alias = ""
        for k in self.persistence["bot"]["aliases"]:
            all_alias += k + " - " + self.persistence["bot"]["aliases"] +"\n"

        query.edit_message_text(text="List of all commands:\n" + all_alias)
        return ConversationHandler.END
    
    
    def create_alias(self, update: Update, context: CallbackContext) -> None:
        query = update.callback_query
        query.answer()

        all_alias = ""
        for k in self.persistence["bot"]["aliases"]:
            all_alias += k + " - " + self.persistence["bot"]["aliases"] +"\n"

        query.edit_message_text(text="List of all commands:\n" + all_alias)
        return ConversationHandler.END

    def delete_alias(self, update: Update, context: CallbackContext) -> None:
        return ConversationHandler.END