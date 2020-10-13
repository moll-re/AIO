import datetime
import time
import json
from dashboard_api import led_out
from threading import Thread


################################################################################
#start of actual programm.
class DashBoard(object):
    """runs all the dashboard operations autonomusly. Accepts outside pokes to change output."""
    def __init__(self, text_speed=7):
        self.IO = led_out.OutputHandler(32,16)
        self.tspeed = text_speed
        self.start()
        # self.text_threads = []
        print("INIT")


    def mainloop(self):
        """Runs the clockface automatically"""
        prev_time = 0
        while True:
            if prev_time == datetime.datetime.now().strftime("%H:%M"):
                time.sleep(5)
            else:
                print("implement me!")

                prev_time = datetime.datetime.now().strftime("%H:%M")
                self.IO.clock_face([])


    def stop(self):
        self.time_thread.join(0)


    def start(self):
        self.time_thread = Thread(target=self.mainloop)
        self.time_thread.start()


    def text_scroll(self, text, color=""):
        self.stop()
        self.IO.text_scroll(text, self.tspeed, color)
        self.start()

test = DashBoard()
# time.sleep(5)
# test.text_scroll("Hello my choupinous!")
