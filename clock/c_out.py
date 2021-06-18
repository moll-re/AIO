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
        
        

    def start(self):
        helpers.timer.RepeatedTimer(60, self.clock_loop)
        # schedule for in 60 seconds
        self.clock_loop()
        # run once now
        # TODO start as a thread


# TODO Turn off when button pressed?

    def clock_loop(self):
        t_start = datetime.datetime.now()
        
        t_minutes = int(datetime.datetime.now().strftime("%H%M"))

        has_queue, data = self.modules["receive"].fetch_data()
        
        if data == {}:
            matrices = self.MOP.get_fallback()
        else:
            matrices = [np.asarray(d).astype(int) for d in data["matrices"]]

        self.IO.put(matrices)
        
        if has_queue:
            tnext = 1
        else:
            tnext = 30


        t_end = datetime.datetime.now()
        delta_planned = datetime.timedelta(seconds = tnext)
        delta = delta_planned - (t_end - t_start)
        
        time.sleep(max(delta.total_seconds(), 0))
        self.clock_loop() 

