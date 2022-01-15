from .template import *

NAME, NEW, ACTION, ITEMADD, ITEMREMOVE = range(5)


class Lists(BotFunc):
    """Create and edit lists"""

    def __init__(self, db_utils):
        super().__init__(db_utils)
        self.current_name = ""
        # self.db_utils set through super()


    def create_handler(self):
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('list', self.entry_point)],
            states={
                NAME: [
                    CallbackQueryHandler(self.choose_list, pattern="^list-"),
                    CallbackQueryHandler(self.new_list, pattern="^new$"),
                    ],
                NEW : [MessageHandler(Filters.text, callback=self.new_listname)],
                ACTION: [
                    CallbackQueryHandler(self.list_add, pattern="^add$"),
                    CallbackQueryHandler(self.list_remove, pattern="^remove$"),
                    CallbackQueryHandler(self.list_clear, pattern="^clear$"),
                    CallbackQueryHandler(self.list_delete, pattern="^delete$"),
                    CallbackQueryHandler(self.list_print, pattern="^print$"),
                    CallbackQueryHandler(self.list_menu, pattern="^overview$"),
                    ],
                ITEMADD : [MessageHandler(Filters.text, callback=self.list_add_item)],
                ITEMREMOVE : [CallbackQueryHandler(self.list_remove_index)]
            },
            fallbacks=[CommandHandler('list', self.entry_point)],
        )
        return conv_handler


    def entry_point(self, update: Update, context: CallbackContext) -> None:
        super().entry_point(update, context)
        lists = self.db_utils.list_get()
        keyboard = [[InlineKeyboardButton(k, callback_data="list-"+k)] for k in lists] + [[InlineKeyboardButton("New list", callback_data="new")]]

        reply_markup = InlineKeyboardMarkup(keyboard)
        super().log_activity(read=True, execute=False, send=True)
        update.message.reply_text(text="Here are the existing lists. You can also create a new one:", reply_markup=reply_markup)
        return NAME


    def choose_list(self, update: Update, context: CallbackContext) -> None:
        query = update.callback_query
        data = query.data
        name = data.replace("list-","")
        query.answer()
        self.current_name = name

        keyboard = [
            [InlineKeyboardButton("Add item", callback_data="add")],
            [InlineKeyboardButton("Remove item", callback_data="remove")],
            [InlineKeyboardButton("Clear list", callback_data="clear")],
            [InlineKeyboardButton("Print list", callback_data="print")],
            [InlineKeyboardButton("Delete list", callback_data="delete")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        query.edit_message_text("Very well. For " + name + " the following actions are available:", reply_markup=reply_markup)
        return ACTION


    def list_menu(self, update: Update, context: CallbackContext) -> None:
        query = update.callback_query
        query.answer()

        keyboard = [
            [InlineKeyboardButton("Add item", callback_data="add")],
            [InlineKeyboardButton("Remove item", callback_data="remove")],
            [InlineKeyboardButton("Clear list", callback_data="clear")],
            [InlineKeyboardButton("Print list", callback_data="print")],
            [InlineKeyboardButton("Delete list", callback_data="delete")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        query.edit_message_text("Very well. For " + self.current_name + " the following actions are available:", reply_markup=reply_markup)
        return ACTION


    def new_list(self, update: Update, context: CallbackContext) -> None:
        query = update.callback_query
        query.answer()
        query.edit_message_text("What's the name of the new list?")
        return NEW
        

    def new_listname(self, update: Update, context: CallbackContext) -> None:
        name = update.message.text
        try:
            self.db_utils.list_create(name)
            keyboard = [[InlineKeyboardButton("Add an item", callback_data="add"), InlineKeyboardButton("To the menu!", callback_data="overview")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            self.current_name = name
            update.message.reply_text("Thanks. List " + name + " was successfully created.", reply_markup=reply_markup)
            super().log_activity(read=False, execute=True, send=True)
            return ACTION
        except Exception as e:
            update.message.reply_text("Oh no! Encountered exception: {}".format(e))
            return ConversationHandler.END

    
    def list_add(self, update: Update, context: CallbackContext) -> None:
        query = update.callback_query
        query.answer()
        query.edit_message_text("What would you like to add?")
        return ITEMADD


    def list_remove(self, update: Update, context: CallbackContext) -> None:
        query = update.callback_query
        query.answer()
        sl = self.db_utils.list_get(self.current_name)

        keyboard = [[InlineKeyboardButton(k, callback_data=i)] for i,k in enumerate(sl)]
        reply_markup = InlineKeyboardMarkup(keyboard)

        query.edit_message_text("Which item would you like to remove?", reply_markup = reply_markup)
        return ITEMREMOVE


    def list_clear(self, update: Update, context: CallbackContext) -> None:
        query = update.callback_query
        query.answer()
        self.db_utils.list_update(self.current_name, replace=[])
        keyboard = [[InlineKeyboardButton("Add an item", callback_data="add"), InlineKeyboardButton("Back to the menu", callback_data="overview")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text("List " + self.current_name + " cleared", reply_markup=reply_markup)
        return ACTION


    def list_delete(self, update: Update, context: CallbackContext) -> None:
        query = update.callback_query
        query.answer()
        self.db_utils.list_delete(self.current_name)
        query.edit_message_text("List " + self.current_name + " deleted")
        return ConversationHandler.END


    def list_print(self, update: Update, context: CallbackContext) -> None:
        query = update.callback_query
        query.answer()
        it = self.db_utils.list_get(self.current_name)
        if it:
            content = "\n".join(it)
        else:
            content = "List empty"
        
        keyboard = [[InlineKeyboardButton("Add an item", callback_data="add"), InlineKeyboardButton("Back to the menu", callback_data="overview")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text("Content of " + self.current_name + ":\n" + content, reply_markup=reply_markup)
        return ACTION


    def list_add_item(self, update: Update, context: CallbackContext) -> None:
        item = update.message.text
        self.db_utils.list_update(self.current_name, append=item)
        keyboard = [[InlineKeyboardButton("Add some more", callback_data="add"), InlineKeyboardButton("Back to the menu", callback_data="overview")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text("Added " + item, reply_markup=reply_markup)
        return ACTION


    def list_remove_index(self, update: Update, context: CallbackContext) -> None:
        query = update.callback_query
        ind = int(query.data)
        query.answer()

        old = self.db_utils.list_get(self.current_name)
        name = old.pop(ind)
        self.db_utils.list_update(self.current_name, replace=old)

        keyboard = [[InlineKeyboardButton("Remove another", callback_data="remove"), InlineKeyboardButton("Back to the menu", callback_data="overview")]]
        reply_markup = InlineKeyboardMarkup(keyboard)      

        query.edit_message_text("Removed " + name, reply_markup=reply_markup)
        return ACTION
