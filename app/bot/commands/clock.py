from .template import *
import time
import numpy
from PIL import Image
import io

CHOOSE, ADDARG = range(2)
MESSAGE, WAKE, ALARM, IMAGE, ART = range(3,8)

class Clock(BotFunc):
    """pass on commands to clock-module"""
    def __init__(self, db_utils, clock_module, art_api):
        super().__init__(db_utils)
        self.clock = clock_module
        self.art_api = art_api

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
        self.next_state = {ALARM : "What frequency (Hertz)"}
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
        self.next_state = {IMAGE : "Please send me the photo to display."}
        return ADDARG

    def art_gallery(self, update: Update, context: CallbackContext) -> None:
        query = update.callback_query
        query.answer()

        query.edit_message_text("Ok. How long should we display art? (in hours")
        self.next_state = {ART : "And how many artworks would you like to see during that time?"}
        return ADDARG

    def get_arg1(self, update: Update, context: CallbackContext) -> None:
        a = update.message.text
        self.additional_argument = a
        update.message.reply_text("Furthermore: "+ list(self.next_state.values())[0])
        return list(self.next_state.keys())[0]
    



###### actually running clock actions
    def exec_wake_light(self, update: Update, context: CallbackContext) -> None:
        duration = update.message.text

        matrices = []
        start_color = numpy.array([153, 0, 51])
        end_color = numpy.array([255, 255, 0])
        col_show = numpy.zeros((*self.clock.MOP.shape, 3))
        col_show[:,:,...] = start_color

        gradient = end_color - start_color
        # steps are shown at a frequency of ?? frames / second =>
        for i in range(duration * 2): # / 0.5
            ct = i/20 * gradient
            col_show[:,:,...] = [int(x) for x in ct+start_color]
            matrices.append(col_show)

        self.clock.out.queue.append({"matrices" : matrices})
        return ConversationHandler.END


    def exec_alarm_blink(self, update: Update, context: CallbackContext) -> None:
        duration = self.additional_argument

        matrices = []
        duration =  int(duration * 2)
        empty = numpy.zeros((*self.clock.MOP.shape,3))
        red = numpy.ones_like(empty) * 255

        for _ in range(int(duration / 2)):
            matrices.append(red)
            matrices.append(empty)

        self.clock.out.queue.append({"matrices": matrices})
        return ConversationHandler.END
        


    def exec_show_image(self, update: Update, context: CallbackContext) -> None:
        duration = self.additional_argument
        i = update.message.photo
        img = update.message.photo[0]
        bot = img.bot
        id = img.file_id

        file = bot.getFile(id).download_as_bytearray()
        width = self.clock.shape[1]
        height = self.clock.shape[0]

        img = Image.open(io.BytesIO(file))
        im_height = img.height
        im_width = img.width

        scalex = im_width // width
        scaley = im_height // height
        scale = min(scalex, scaley)

        t = img.resize((width, height),box=(0,0,width*scale,height*scale))
        a = numpy.asarray(t)
        
        matrices = [a for _ in range(2*60*duration)]

        self.clock.out.queue.append({"matrices": matrices})
        return ConversationHandler.END


    def exec_show_message(self, update: Update, context: CallbackContext) -> None:
        message_str = update.message.text
        update.message.reply_text("Now showing: " + message_str)
        self.clock.run(self.clock.text_scroll,(message_str,))
        return ConversationHandler.END


    def exec_art_gallery(self, update: Update, context: CallbackContext) -> None:
        duration = float(self.additional_argument)
        number = int(update.message.text)
        
        def output(number, duration):
            for i in range(number):
                img = self.art_api.get_random_art() # returns an PIL.Image object
                im_height = img.height
                im_width = img.width

                width = self.clock.shape[1]
                height = self.clock.shape[0]
                
                scalex = im_width // width
                scaley = im_height // height
                scale = min(scalex, scaley)

                t = img.resize((width, height),box=(0,0,width*scale,height*scale))
                a = numpy.asarray(t)
                self.clock.IO.put(a)

                time.sleep(duration*3600 / number)


        update.message.reply_text("Ok. Showing art for the next "+ str(duration) + " hours.")
        self.clock.run(output,(number, duration))
        return ConversationHandler.END







# TODO FIx this to work with the new backend