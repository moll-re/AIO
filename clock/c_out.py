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
        Thread(target = self.clock_loop).start()


    def clock_loop(self):
        while True: # TODO: allow this to be exited gracefully

            t_start = datetime.datetime.now()

            self.set_brightness()

            has_queue, data = self.modules["receive"].fetch_data()
            tnext = 1 if has_queue else 30

            if data == {}:
                matrices = self.MOP.get_fallback()
                matrices[0][0,0] = [255, 0, 0] # red dot on the top left
            else:
                matrices = [np.asarray(d).astype(int) for d in data["matrices"]]
                matrices[0][0,0] = [0, 255, 0] # green dot on the top left
            
            if not self.kill_output:
                self.IO.put(matrices)
            else:
                z = np.zeros((16,16,3))
                self.IO.put([z,z,z])
            

            t_end = datetime.datetime.now()
            delta_planned = datetime.timedelta(seconds = tnext)
            delta = delta_planned - (t_end - t_start)
            
            time.sleep(max(delta.total_seconds(), 0))


    def set_brightness(self):
        """Kill the brightness at night"""

        is_WE = datetime.datetime.now().weekday() > 4
        now = int(datetime.datetime.now().strftime("%H%M"))

        self.kill_output = (now < 1000 or now > 2200) if is_WE else (now < 830 or now > 2130)

