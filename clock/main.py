import datetime
import time
import json
from clock.api import led_out
from threading import Thread
import numpy

import persistence.rw
################################################################################
#start of actual programm.
class ClockFace(object):
    """Actual functions one might need for a clock"""

    def __init__(self, text_speed=10):
        self.IO = led_out.OutputHandler(32,16)
        self.tspeed = text_speed

        self.output_thread = ""
        # Action the thread is currently performing
        self.output_queue = []
        # Threads to execute next

        self.weather = ""

    def run(self, command, kw=()):
        """Checks for running threads and executes the ones in queue"""
        def enhanced_run(command, kw):
            self.output_thread = "Running " + str(command)
            command(*kw)
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



    def set_face(self):
        """"""
        self.run(self.IO.clock_face,("C"))


    def text_scroll(self, text, color=""):
        """"""
        self.run(self.IO.text_scroll,(text, self.tspeed, color))



    def wake_light(self, duration=600):
        """Duration in seconds"""
        def output(duration):
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
                self.IO.set_matrix(ones,5,colors=[col])
                time.sleep(duration / 20)


        self.run(output,(duration,))


    def alarm_blink(self, duration, frequency):
        """Duration in seconds, frequency in Hertz"""
        def output(duration, frequency):
            duration =  int(duration)
            frequency = int(frequency)
            n = duration * frequency / 2
            empty = numpy.zeros((16,32))
            red = empty.copy()
            red[red == 0] = 3
            for i in range(int(n)):
                self.IO.set_matrix(red,5)
                time.sleep(1/frequency)
                self.IO.set_matrix(empty,5)
                time.sleep(1/frequency)




        self.run(output,(duration, frequency))


    def image_show(self, image):
        def output():
            self.output_threads.append("Showing: " + text)
            self.IO.text_scroll(text, self.tspeed, color)
            time.sleep(2)
            self.output_threads.remove("Showing: " + text)
            self.set_face()

        scroll_thread = Thread(target = output)
        scroll_thread.start()
