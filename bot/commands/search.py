from .template import *


SEARCH, MORE = range(2)
class Search(BotFunc):
    """Browse the web for a topic."""
    
    def __init__(self, api, db):
        super().__init__(db)
        self.available_commands = {}
        self.api = api


    def create_handler(self):
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('search', self.entry_point)],
            states={
                SEARCH: [MessageHandler(Filters.text, self.get_results),],
                MORE: [CallbackQueryHandler(self.show_more, pattern="^more$"),],
            },
            fallbacks=[CommandHandler('search', self.entry_point)],
            conversation_timeout=20,
        )
        return conv_handler


    def entry_point(self, update: Update, context: CallbackContext) -> None:

        update.message.reply_text("What are we searching?")
        return SEARCH


    def get_results(self, update: Update, context: CallbackContext) -> None:
        search = update.message.text
        results = self.api.get_result(search)
        keyboard = [[InlineKeyboardButton("More!", callback_data="more")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # formating
        self.results = results
        first = results[0]
        message = first["text"] + "\n(" + first["url"] + ")\n\n"

        update.message.reply_text(text = message, reply_markup=reply_markup)
        super().log_activity(read = True, execute = True, send = True)
        return MORE
    

    def show_more(self, update: Update, context: CallbackContext) -> None:
        query = update.callback_query
        query.answer()

        message = ""
        for r in self.results:
            message += r["text"] + "\n(" + r["url"] + ")\n\n"

        query.edit_message_text(message)
        super().log_activity(read = False, execute = False, send = True)
        return ConversationHandler.END