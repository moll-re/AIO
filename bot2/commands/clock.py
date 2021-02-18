from .template import *
import time
import numpy

CHOOSE, ADDARG = range(2)
MESSAGE, WAKE, ALARM, IMAGE, ART = range(3,8)

class Clock(BotFunc):
    """pass on commands to clock-module"""
    def __init__(self, prst, clock_module):
        super().__init__(prst)
        self.clock = clock_module

    def create_handler(self):
        handler = ConversationHandler(
            entry_points=[CommandHandler("clock", self.entry_point)],
            states={
                CHOOSE : [
                    CallbackQueryHandler(self.wake_light, pattern="^wake$"),
                    CallbackQueryHandler(self.alarm_blink, pattern="^alarm$"),
                    CallbackQueryHandler(self.show_message, pattern="^message$"),
                    CallbackQueryHandler(self.show_image, pattern="^image$"),
                    CallbackQueryHandler(self.art_gallery, pattern="^gallery$"),
                ],
                ADDARG : [MessageHandler(Filters.text, callback=self.get_arg1)],
                MESSAGE: [MessageHandler(Filters.text, callback=self.exec_show_message)],
                WAKE : [MessageHandler(Filters.text, callback=self.exec_wake_light)],
                ALARM : [MessageHandler(Filters.text, callback=self.exec_alarm_blink)],
                IMAGE : [MessageHandler(Filters.photo, callback=self.exec_show_image)],
                ART : [MessageHandler(Filters.text, callback=self.exec_art_gallery)],
            },
            fallbacks=[CommandHandler('clock', self.entry_point)],
        )
        return handler

    def entry_point(self, update: Update, context: CallbackContext) -> None:
        super().entry_point()
        keyboard = [
            [InlineKeyboardButton("Make a wake-light", callback_data="wake")],
            [InlineKeyboardButton("Blink as alarm", callback_data="alarm")],
            [InlineKeyboardButton("Show a message", callback_data="message")],
            [InlineKeyboardButton("Show an image", callback_data="image")],
            [InlineKeyboardButton("Art gallery!", callback_data="gallery")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text("What exactly do you want?", reply_markup=reply_markup)
        return CHOOSE


    def wake_light(self, update: Update, context: CallbackContext) -> None:
        query = update.callback_query
        query.answer()

        query.edit_message_text("Ok. How long should the color cycle last? (In seconds)")
        return WAKE

    def alarm_blink(self, update: Update, context: CallbackContext) -> None:
        query = update.callback_query
        query.answer()

        query.edit_message_text("Ok. How long should it blink? (In seconds)")
        self.next_state = {"ALARM" : "What frequency (Hertz)"}
        return ADDARG

    def show_message(self, update: Update, context: CallbackContext) -> None:
        query = update.callback_query
        query.answer()

        query.edit_message_text("Ok. What message will I show?")
        return MESSAGE

    def show_image(self, update: Update, context: CallbackContext) -> None:
        query = update.callback_query
        query.answer()

        query.edit_message_text("How long (in minutes) should the image be displayed?")
        self.next_state = {"IMAGE" : "Please send me the photo to display."}
        return ADDARG

    def art_gallery(self, update: Update, context: CallbackContext) -> None:
        query = update.callback_query
        query.answer()

        query.edit_message_text("Ok. How long should we display art? (in hours")
        return ART

    def get_arg1(self, update: Update, context: CallbackContext) -> None:
        a = update.message.text
        self.additional_argument = a
        update.message.reply_text("Furthermore: "+ list(self.next_state.values())[0])
        return list(self.next_state.keys())[0]
    



###### actually running clock actions
    def exec_wake_light(self, update: Update, context: CallbackContext) -> None:
        duration = update.message.text

        def output(duration):
            self.clock.set_brightness(value=0.1)
            start_color = numpy.array([153, 0, 51])
            end_color = numpy.array([255, 255, 0])
            empty = numpy.zeros((16,32))
            ones = empty
            ones[ones == 0] = 1
            gradient = end_color - start_color
            # 20 steps should be fine => sleep_time = duration / 20
            for i in range(20):
                ct = i/20 * gradient
                col = [int(x) for x in ct+start_color]
                self.clock.IO.set_matrix(ones,colors=[col])
                time.sleep(int(duration) / 20)

        self.clock.run(output,(duration,))
        return ConversationHandler.END


    def exec_alarm_blink(self, update: Update, context: CallbackContext) -> None:
        duration = self.additional_argument
        frequency = update.message.text

        def output(duration, frequency):
            self.set_brightness(value=1)
            duration =  int(duration)
            frequency = int(frequency)
            n = duration * frequency / 2
            empty = numpy.zeros((16,32))
            red = empty.copy()
            red[red == 0] = 3
            for i in range(int(n)):
                self.IO.set_matrix(red)
                time.sleep(1/frequency)
                self.IO.set_matrix(empty)
                time.sleep(1/frequency)

        if not(duration == 0 or frequency == 0):
            update.message.reply_text("Now blinking")
            self.clock.run(output,(duration, frequency))
        print("DOOONE")
        return ConversationHandler.END
        


    def exec_show_image(self, update: Update, context: CallbackContext) -> None:
        duration = self.additional_argument
        img = update.message.photo

        def output(image, duration):
            self.clock.IO.set_matrix_rgb([100,0,0])

        self.clock.run(output,("image", duration))
        return ConversationHandler.END


    def exec_show_message(self, update: Update, context: CallbackContext) -> None:
        message_str = update.message.text
        update.message.reply_text("Now showing: " + message_str)
        self.clock.run(self.clock.IO.text_scroll,(message_str, self.clock.tspeed, [200,200,200]))
        return ConversationHandler.END


    def exec_art_gallery(self, update: Update, context: CallbackContext) -> None:
        update.message.reply_text("Puuh, thats tough, I'm not ready for that.")
        return ConversationHandler.END