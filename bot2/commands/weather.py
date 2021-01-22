from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    CallbackContext,
)

import datetime
FIRST = 1

class Weather():
    """Shows a weatherforecast for a given location"""
    def __init__(self, api):
        """initialize api and persistence"""
        self.api = api
        self.city = ""

    def create_handler(self):
        """returns the handlers with button-logic"""
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('weather', self.entry_point)],
            states={
                FIRST: [
                    CallbackQueryHandler(self.choose_city, pattern="^city-"),
                    CallbackQueryHandler(self.choose_time, pattern="^time-"),
                ]
            },
            fallbacks=[CommandHandler('weather', self.entry_point)],
        )

        return conv_handler


    def entry_point(self, update: Update, context: CallbackContext) -> None:
        """Reacts the call of the command. Prints the first buttons"""
        keyboard = [
            [
                InlineKeyboardButton("Zürich", callback_data="city-zurich"),
                InlineKeyboardButton("Freiburg", callback_data="city-freiburg"),
                InlineKeyboardButton("Mulhouse", callback_data="city-mulhouse"),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text("Which city?", reply_markup=reply_markup)
        return FIRST


    def choose_city(self, update: Update, context: CallbackContext) -> None:
        """Prompt same text & keyboard as `start` does but not as new message"""
        # Get CallbackQuery from Update
        query = update.callback_query
        data = query.data
        self.city = data.replace("city-","")
        query.answer()
        keyboard = [
            [
                InlineKeyboardButton("Now", callback_data="time-now"),
                InlineKeyboardButton("Tomorrow", callback_data="time-tomorrow"),
                InlineKeyboardButton("7 days", callback_data="time-7"),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(
            text = "Which time?", reply_markup=reply_markup
        )
        return FIRST


    def choose_time(self, update: Update, context: CallbackContext) -> None:
        """Show new choice of buttons"""
        query = update.callback_query
        query.answer()
        forecast_time = query.data.replace("time-","")
        weather = self.get_weather(self.city, forecast_time)
        query.edit_message_text(
            text = "Weather: \n" + weather
        )
        return ConversationHandler.END


    def get_weather(self, city, forecast_time) -> None:
        """get the weather that matches the given params"""
        locations = {"freiburg": [47.9990, 7.8421], "zurich": [47.3769, 8.5417], "mulhouse": [47.7508, 7.3359]}

        city = locations[city]
        
        categories = {"Clouds": "☁", "Rain": "🌧", "Thunderstorm": "🌩", "Drizzle": ":droplet:", "Snow": "❄", "Clear": "☀", "Mist": "🌫", "Smoke": "Smoke", "Haze": "Haze", "Dust": "Dust", "Fog": "Fog", "Sand": "Sand", "Dust": "Dust", "Ash": "Ash", "Squall": "Squall", "Tornado": "Tornado",}
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        today = datetime.datetime.today().weekday()
        weather = self.api.show_weather(city)
        message = ""
        if forecast_time == "now" or forecast_time == "7":
            now = weather.pop(0)
            message += "<b>Now:</b> " + categories[now["short"]] + "\n"
            message += "🌡" + str(now["temps"][0]) + "°\n\n"
            tod = weather.pop(0)
            message += "<b>" + "Today" + ":</b> " + categories[tod["short"]] + "\n"
            message += "🌡 ❄ " + str(tod["temps"][0]) + "° , 🌡 🔥 " + str(tod["temps"][1]) + "°\n\n"

        if forecast_time == "tomorrow" or forecast_time == "7":
            tom = weather.pop(0)
            print(tom)
            message += "<b>" + "Tomorrow" + ":</b> " + categories[tom["short"]] + "\n"
            message += "🌡 ❄ " + str(tom["temps"][0]) + "° , 🌡 🔥 " + str(tom["temps"][1]) + "°\n\n"

        if forecast_time == "7":
            for i, day in enumerate(weather):
                message += "<b>" + days[(today + i + 2) % 7] + ":</b> " + categories[day["short"]] + "\n"
                message += "🌡 ❄ " + str(day["temps"][0]) + "° , 🌡 🔥 " + str(day["temps"][1]) + "°\n\n"

        return message
