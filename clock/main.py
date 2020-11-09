import datetime
import time
import json
from threading import Thread
import numpy


from clock.api import led
import persistence.rw


################################################################################
#start of actual programm.
class ClockFace(object):
    """Actual functions one might need for a clock"""

    def __init__(self, text_speed=18):
        self.IO = led.OutputHandler(32,16)
        self.tspeed = text_speed

        self.output_thread = ""
        # Action the thread is currently performing
        self.output_queue = []
        # Threads to execute next

        self.weather = ""
        self.brightness_overwrite = {"value" : 1, "duration" : 0}


    def run(self, command, kw=()):
        """Checks for running threads and executes the ones in queue"""
        def enhanced_run(command, kw):
            """"""
            self.output_thread = "Running " + str(command)
            command(*kw)
            self.set_brightness()
            self.output_thread = ""
            if len(self.output_queue) != 0:
                n = self.output_queue.pop(0)
                enhanced_run(n[0],n[1])
            else:
                self.IO.clock_face(self.weather)

        if len(self.output_thread) == 0:
            t = Thread(target=enhanced_run, args=(command, kw))
            t.start()
        else:
            self.output_queue.append([command,kw])


    ############################################################################
    ### basic clock commands
    def set_face(self, weather):
        """"""
        self.weather = weather
        self.run(self.IO.clock_face,(weather,))


    def text_scroll(self, text, color=""):
        """"""
        self.run(self.IO.text_scroll,(text, self.tspeed, color))


    def set_brightness(self, overwrite=[],value=-1):
        """Checks, what brightness rules to apply"""

        if value != -1:
            self.IO.output.set_brightness(value)
            return


        if len(overwrite) != 0:
            self.brightness_overwrite = overwrite

        is_WE = datetime.datetime.now().weekday() > 4
        now = int(datetime.datetime.now().strftime("%H%M"))
        if (is_WE and (now > 1000 and now < 2200)) or ((not is_WE) and (now > 800 and now < 2130)):
            brightness = 0.8
        else:
            brightness = 0.01

        self.IO.output.set_brightness(brightness)


    ############################################################################
    ### Higher level commands, accessible from the chat-bot
    def wake_light(self, duration=600):
        """Simulates a sunris, takes one optional parameter: the duration"""
        def output(duration):
            self.set_brightness(value=0.1)
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
                self.IO.set_matrix(ones,colors=[col])
                time.sleep(int(duration) / 20)


        self.run(output,(duration,))


    def alarm_blink(self, duration, frequency):
        """Blinks the whole screen (red-black). Duration in seconds, frequency in Hertz"""
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

        self.run(output,(duration, frequency))


    def image_show(self, image, duration):
        """Shows a 16x32 image for duration seconds"""
        def output(image, duration):
            self.IO.set_matrix_rgb(red)

        self.run(output,(image, duration))


    def show_message(self, *args):
        """Runs a text message over the screen. Obviously needs the text"""
        # keep in mind, in this case args is a tuple of all words
        message_str = " ".join(args)
        print("SENDING: " + message_str)
        self.text_scroll(message_str)
