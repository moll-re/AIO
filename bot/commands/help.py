from .template import *

FIRST, EXECUTE = range(2)


class Help(BotFunc):
    """Shows the functions and their usage"""
    
    def __init__(self, db):
        super().__init__(db)
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
                EXECUTE :[CallbackQueryHandler(self.execute_now)],
                # ConversationHandler.TIMEOUT : [
                #     CallbackQueryHandler(self.timeout)
                # ]
            },
            fallbacks=[CommandHandler('help', self.entry_point)],
            conversation_timeout=15,
        )
        return conv_handler

    def add_commands(self, commands):
        # commands is a dict {"name": class}
        for k in commands:
            if k != "plaintext":
                self.available_commands[k] = commands[k].__doc__



    def entry_point(self, update: Update, context: CallbackContext) -> None:
        super().entry_point(update, context)

        keyboard = [
            [
                InlineKeyboardButton("All commands", callback_data="all"),
                InlineKeyboardButton("Just one", callback_data="specific"),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        super().log_activity(read=True, execute=True, send=True) # at this point every step has been fulfilled
        if update.message:
            update.message.reply_text("What exactly do you want?", reply_markup=reply_markup)
        else:
            update._effective_chat.send_message("What exactly do you want?", reply_markup=reply_markup)
        return FIRST


    def print_all(self, update: Update, context: CallbackContext) -> None:
        query = update.callback_query
        query.answer()
        all_cmd = ""
        for h in self.available_commands:
            all_cmd += "{} - `{}`\n".format(h, self.available_commands[h])

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

        keyboard = [[InlineKeyboardButton("Call " + name + " now", callback_data=name),]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        query.edit_message_text(
            text= message,
            reply_markup = reply_markup,
            parse_mode = ParseMode.MARKDOWN_V2
        )
        return EXECUTE


    def execute_now(self, update: Update, context: CallbackContext) -> None:
        query = update.callback_query
        name = query.data
        query.answer()
        funcs = context.dispatcher.handlers[0]
        for func in funcs:
            if name == func.entry_points[0].command[0]:
                break
        callback = func.entry_points[0].handle_update
        callback(update, context.dispatcher, check_result=True, context=context)
        return ConversationHandler.END
        

    def timeout(self, update: Update, context: CallbackContext) -> None:
        """For dying conversation. Currently unused."""

        query = update.callback_query
        name = query.data.replace("func-", "")
        query.answer()

        message = name + ": `" + self.available_commands[name] + "`"
        query.edit_message_text(
            text= "Timed out...",
            parse_mode = ParseMode.MARKDOWN_V2
        )
        return ConversationHandler.END