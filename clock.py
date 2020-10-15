import time
import datetime
from threading import Thread

import clock.main
import bot.main

class ModuleWrapper():
    """Wrapper for the CLOCK-functionality"""
    def __init__(self, module_name):
        """"""
        self.clock = clock.main.ClockFace()
        self.time_thread = Thread(target=self.mainloop)
        self.time_thread.start()


    def mainloop(self):
        """Runs the showing of the clock-face periodically (better way?)"""
        prev_time = 0
        while True:
            if prev_time == datetime.datetime.now().strftime("%H:%M"):
                time.sleep(10)
            else:

                prev_time = datetime.datetime.now().strftime("%H:%M")
                self.clock.set_face("sun")


test = ModuleWrapper("clock")
