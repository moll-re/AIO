import datetime
import time
from threading import Thread
import numpy as np

from . import hardware, helpers


class ClockFace:
    """Actual functions one might need for a clock"""

    def __init__(self):
        """"""
        # added by the launcher, we have self.modules (dict)

        self.IO = hardware.led.get_handler()
        self.shape = self.IO.shape # (16,32) for now
        # TODO handle differently!
        self.MOP = helpers.computations.MatrixOperations()
        
        self.kill_output = False

    def start(self):
        # helpers.timer.RepeatedTimer(60, self.clock_loop)
        # # schedule for in 60 seconds
        Thread(target = self.clock_loop).start()


# TODO Turn off when button pressed?

    def clock_loop(self):
        t_start = datetime.datetime.now()
        
        t_minutes = int(datetime.datetime.now().strftime("%H%M"))

        has_queue, data = self.modules["receive"].fetch_data()
        self.set_brightness()
        
        if data == {}:
            matrices = self.MOP.get_fallback()
        else:
            matrices = [np.asarray(d).astype(int) for d in data["matrices"]]
        
        if not self.kill_output:
            self.IO.put(matrices)
        else:
            z = np.zeros((16,16,3))
            self.IO.put([z,z,z])
        
        if has_queue:
            tnext = 1
        else:
            tnext = 30


        t_end = datetime.datetime.now()
        delta_planned = datetime.timedelta(seconds = tnext)
        delta = delta_planned - (t_end - t_start)
        
        time.sleep(max(delta.total_seconds(), 0))
        self.clock_loop() 


    def set_brightness(self):
        """Kill the brightness at night"""

        is_WE = datetime.datetime.now().weekday() > 4
        now = int(datetime.datetime.now().strftime("%H%M"))
        if (is_WE and (now > 1000 and now < 2200)) or ((not is_WE) and (now > 830 and now < 2130)):
            self.kill_output = False
        else:
            self.kill_output = True

