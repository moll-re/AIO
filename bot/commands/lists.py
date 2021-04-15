from .template import *

import datetime
import requests

NAME, NEW, ACTION, ITEMADD, ITEMREMOVE = range(5)


class Lists(BotFunc):
    """Create and edit lists"""

    def __init__(self, prst):
        super().__init__(prst)
        self.current_name = ""


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
        super().entry_point()
        keyboard = [[InlineKeyboardButton(k, callback_data="list-"+k)] for k in self.persistence["global"]["lists"]] + [[InlineKeyboardButton("New list", callback_data="new")]]

        reply_markup = InlineKeyboardMarkup(keyboard)
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
        if name not in self.persistence["global"]["lists"]:
            self.persistence["global"]["lists"][name] = []

            keyboard = [[InlineKeyboardButton("Add an item", callback_data="add"), InlineKeyboardButton("To the menu!", callback_data="overview")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            self.current_name = name
            update.message.reply_text("Thanks. List " + name + " was successfully created.", reply_markup=reply_markup)
            return ACTION
        else:
            update.message.reply_text("Oh no! That list already exists")
            return ConversationHandler.END

    
    def list_add(self, update: Update, context: CallbackContext) -> None:
        query = update.callback_query
        query.answer()
        query.edit_message_text("What would you like to add?")
        return ITEMADD


    def list_remove(self, update: Update, context: CallbackContext) -> None:
        query = update.callback_query
        query.answer()
        keyboard = [[InlineKeyboardButton(k, callback_data=i)] for i,k in enumerate(self.persistence["global"]["lists"][self.current_name])]
        reply_markup = InlineKeyboardMarkup(keyboard)

        query.edit_message_text("Which item would you like to remove?", reply_markup = reply_markup)
        return ITEMREMOVE


    def list_clear(self, update: Update, context: CallbackContext) -> None:
        query = update.callback_query
        query.answer()
        self.persistence["global"]["lists"][self.current_name] = []
        keyboard = [[InlineKeyboardButton("Add an item", callback_data="add"), InlineKeyboardButton("Back to the menu", callback_data="overview")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text("List " + self.current_name + " cleared", reply_markup=reply_markup)
        return ACTION


    def list_delete(self, update: Update, context: CallbackContext) -> None:
        query = update.callback_query
        query.answer()
        self.persistence["global"]["lists"].pop(self.current_name, None)  
        query.edit_message_text("List " + self.current_name + " deleted")
        return ConversationHandler.END


    def list_print(self, update: Update, context: CallbackContext) -> None:
        query = update.callback_query
        query.answer()
        content = "\n".join(self.persistence["global"]["lists"][self.current_name])
        keyboard = [[InlineKeyboardButton("Add an item", callback_data="add"), InlineKeyboardButton("Back to the menu", callback_data="overview")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text("Content of " + self.current_name + ":\n" + content, reply_markup=reply_markup)
        return ACTION


    def list_add_item(self, update: Update, context: CallbackContext) -> None:
        name = update.message.text
        self.persistence["global"]["lists"][self.current_name] += [name]
        keyboard = [[InlineKeyboardButton("Add some more", callback_data="add"), InlineKeyboardButton("Back to the menu", callback_data="overview")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text("Added " + name, reply_markup=reply_markup)
        return ACTION


    def list_remove_index(self, update: Update, context: CallbackContext) -> None:
        query = update.callback_query
        ind = int(query.data)
        query.answer()

        old = self.persistence["global"]["lists"][self.current_name]
        name = old.pop(ind)
        self.persistence["global"]["lists"][self.current_name] = old

        keyboard = [[InlineKeyboardButton("Remove another", callback_data="remove"), InlineKeyboardButton("Back to the menu", callback_data="overview")]]
        reply_markup = InlineKeyboardMarkup(keyboard)      

        query.edit_message_text("Removed " + name, reply_markup=reply_markup)
        return ACTION
