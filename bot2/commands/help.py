from .template import *

FIRST = 1


class Help(BotFunc):
    """Shows the functions and their usage"""
    
    def __init__(self, prst):
        super().__init__(prst)
        self.available_commands = {}


    def create_handler(self):
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('help', self.entry_point)],
            states={
                FIRST: [
                    CallbackQueryHandler(self.print_all, pattern="^all$"),
                    CallbackQueryHandler(self.choose_specific, pattern="^specific$"),
                    CallbackQueryHandler(self.print_one, pattern='func-'),
                ],
                # ConversationHandler.TIMEOUT : [
                #     CallbackQueryHandler(self.timeout)
                # ]
            },
            fallbacks=[CommandHandler('help', self.entry_point)],
            # conversation_timeout=5,
        )
        return conv_handler

    def add_commands(self, commands):
        # commands is a dict {"name": class}
        for k in commands:
            if k != "plaintext":
                self.available_commands[k] = commands[k].__doc__



    def entry_point(self, update: Update, context: CallbackContext) -> None:
        super().entry_point()
        keyboard = [
            [
                InlineKeyboardButton("All commands", callback_data="all"),
                InlineKeyboardButton("Just one", callback_data="specific"),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text("What exactly do you want?", reply_markup=reply_markup)
        return FIRST


    def print_all(self, update: Update, context: CallbackContext) -> None:
        query = update.callback_query
        query.answer()
        all_cmd = ""
        for h in self.available_commands:
            all_cmd += h + " - `" + self.available_commands[h] + "`\n"

        query.edit_message_text(text="List of all commands:\n" + all_cmd, parse_mode = ParseMode.MARKDOWN)
        return ConversationHandler.END


    def choose_specific(self, update: Update, context: CallbackContext) -> None:
        query = update.callback_query
        query.answer()

        
        keyboard = [[InlineKeyboardButton(k, callback_data="func-" + k)] for k in self.available_commands]
        reply_markup = InlineKeyboardMarkup(keyboard)

        query.edit_message_text(
            text="What command should be printed?", reply_markup=reply_markup
        )
        return FIRST


    def print_one(self, update: Update, context: CallbackContext) -> None:
        """Show new choice of buttons"""
        query = update.callback_query
        name = query.data.replace("func-", "")
        query.answer()

        message = name + ": `" + self.available_commands[name] + "`"
        query.edit_message_text(
            text= message,
            parse_mode = ParseMode.MARKDOWN_V2
        )
        return ConversationHandler.END



    def timeout(self, update: Update, context: CallbackContext) -> None:
        """For dying conversation. Currently unused."""

        query = update.callback_query
        name = query.data.replace("func-", "")
        query.answer()

        message = name + ": `" + self.available_commands[name] + "`"
        query.edit_message_text(
            text= "EHHHHH",
            parse_mode = ParseMode.MARKDOWN_V2
        )
        return ConversationHandler.END