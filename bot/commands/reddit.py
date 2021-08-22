from .template import *


CHOOSE_NUM = 1
class Joke(BotFunc):
    """Tells a joke from reddit."""
    
    def __init__(self, api, db):
        super().__init__(db)
        self.available_commands = {}
        self.api = api


    def create_handler(self):
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('joke', self.entry_point)],
            states={
                CHOOSE_NUM: [CallbackQueryHandler(self.get_jokes),],
            },
            fallbacks=[CommandHandler('joke', self.entry_point)],
            # conversation_timeout=5,
        )
        return conv_handler


    def entry_point(self, update: Update, context: CallbackContext) -> None:
        
        keyboard = [[InlineKeyboardButton(str(i), callback_data=str(i)) for i in range(1,11)]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        super().log_activity(read=True, execute=True, send=True) # at this point every step has been fulfilled
        update.message.reply_text("How many jokes?", reply_markup=reply_markup)
        return CHOOSE_NUM


    def get_jokes(self, update: Update, context: CallbackContext) -> None:
        query = update.callback_query
        number = int(query.data)
        query.answer()
        jokes = self.api.get_random_rising("jokes", number, "text")
        # formating
        message = ""
        for j in jokes:
            message += "<b>" + j["title"] + "</b> \n" + j["content"] + "\n\n"
        if message == "":
            message += "Could not fetch jokes."
        query.edit_message_text(text = message, parse_mode = ParseMode.HTML)
        return ConversationHandler.END




CHOOSE_TOPIC = 0
class Meme(BotFunc):
    """Gets the latest memes from reddit"""
    
    def __init__(self, api, db):
        super().__init__(db)
        self.available_commands = {}
        self.api = api


    def create_handler(self):
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('meme', self.entry_point)],
            states={
                CHOOSE_TOPIC: [CallbackQueryHandler(self.choose_topic)],
                CHOOSE_NUM :[CallbackQueryHandler(self.get_memes)],
            },
            fallbacks=[CommandHandler('meme', self.entry_point)],
        )
        return conv_handler


    def entry_point(self, update: Update, context: CallbackContext) -> None:

        keyboard = [
            [InlineKeyboardButton("General", callback_data="memes"),],
            [InlineKeyboardButton("Dank memes", callback_data="dankmemes"),],
            [InlineKeyboardButton("Maths", callback_data="mathmemes"),],
            [InlineKeyboardButton("Physics", callback_data="physicsmemes"),],
            [InlineKeyboardButton("Biology", callback_data="biologymemes"),],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        super().log_activity(read=True, execute=True, send=True) # at this point every step has been fulfilled
        update.message.reply_text("What kind of memes?", reply_markup=reply_markup)
        return CHOOSE_TOPIC


    def choose_topic(self, update: Update, context: CallbackContext) -> None:
        query = update.callback_query
        d = query.data
        query.answer()

        keyboard = [[InlineKeyboardButton(str(i), callback_data=d + "-" + str(i)) for i in range(1,11)]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text("How many memes?", reply_markup=reply_markup)
        return CHOOSE_NUM


    def get_memes(self, update: Update, context: CallbackContext) -> None:
        query = update.callback_query
        data = query.data.split("-")
        query.answer()

        memes = self.api.get_random_rising(data[0], int(data[1]), "photo")
        if len(memes) != 0:
            for m in memes:
                super().log_activity(read=False, execute=False, send=True) # we just sent an additional message
                update.effective_chat.send_photo(photo = m["image"],caption = m["caption"])
        else:
           update.effective_chat.send_message("Sorry, the meme won't yeet.")
        return ConversationHandler.END




# class News(BotFunc):
#     """Gets the latest news from reddit"""
    
#     def __init__(self, api, prst):
#         super().__init__(prst)
#         self.available_commands = {}
#         self.api = api


#     def create_handler(self):
#         conv_handler = ConversationHandler(
#             entry_points=[CommandHandler('news', self.entry_point)],
#             states={
#                 CHOOSE_TOPIC: [CallbackQueryHandler(self.choose_topic)],
#                 CHOOSE_NUM :[CallbackQueryHandler(self.get_news)],
#             },
#             fallbacks=[CommandHandler('news', self.entry_point)],
#         )
#         return conv_handler


#     def entry_point(self, update: Update, context: CallbackContext) -> None:
#         super().entry_point()

#         keyboard = [
#             [InlineKeyboardButton("World", callback_data="worldnews"),],
#             [InlineKeyboardButton("Germany", callback_data="germannews"),],
#             [InlineKeyboardButton("France", callback_data="francenews"),],
#             [InlineKeyboardButton("Europe", callback_data="eunews"),],
#             [InlineKeyboardButton("USA", callback_data="usanews"),],
#         ]
#         reply_markup = InlineKeyboardMarkup(keyboard)
#         update.message.reply_text("What kind of news?", reply_markup=reply_markup)
#         return CHOOSE_TOPIC


#     def choose_topic(self, update: Update, context: CallbackContext) -> None:
#         super().entry_point()
#         query = update.callback_query
#         d = query.data
#         query.answer()

#         keyboard = [[InlineKeyboardButton(str(i), callback_data=d + "-" + str(i)) for i in range(1,11)]]
#         reply_markup = InlineKeyboardMarkup(keyboard)
#         query.edit_message_text("How many entries?", reply_markup=reply_markup)
#         return CHOOSE_NUM


#     def get_news(self, update: Update, context: CallbackContext) -> None:
#         query = update.callback_query
#         data = query.data.split("-")
#         query.answer()
#         #try:
#         news = self.api.get_top(data[0], data[1], "text")
#         # formating
#         message = ""
#         for j in news:
#             message += "<b>" + j["title"] + "</b> \n" + j["content"] + "\n\n"
#         if message == "":
#             message += "Could not fetch news."
#         query.edit_message_text(news, paresemode=ParseMode.HTML)
#         return ConversationHandler.END