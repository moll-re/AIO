import time
import numpy as np
from threading import Thread

import converter
try:
    from hat import unicorn as HAT
except ImportError:
    print("Using the simulator")
    from hat import sim as HAT



class OutputHandler():
    def __init__(self, width, height):
        """width is presumed to be larger than height"""
        self.width = width
        self.height = height
        self.output = HAT.UnicornHat(width, height)
        self.threads = []
        self.running = False
        self.primary = [200, 200, 200]
        self.secondary = [10, 200, 10]
        self.red = [200, 10, 10]



    def stop(self):
        for t in threads:
            t.stop()
        self.output.off()


    def run(self, func, args):
        self.running = True
        t = Thread(target=func,args=tuple(args))
        t.start()
        self.threads.append(t)


    def set_matrix(self, matrix):
        """assumes 1 for primary, 2 for secondary color"""

        for x in range(matrix.shape[0]):
            for y in range(matrix.shape[1]):
                if matrix[x,y] == 1:
                    self.output.set_pixel(x,y,self.primary[0],self.primary[1],self.primary[2])
                elif matrix[x,y] == 2:
                    self.output.set_pixel(x,y,self.secondary[0],self.secondary[1],self.secondary[2])
        self.output.show()

    def clock_face(self):
        hour = converter.time_converter()
        day = converter.date_converter()

        self.set_matrix(hour + day)
        self.running = False


    def text_scroll(self, text, speed):
        pixels = converter.text_converter(text,16)
        sleep_time = 1 / speed
        frames = pixels.shape[1] - 16
        if frames <= 0:
            frames = 1
        for i in range(frames):
            #self.output.clear()
            #self.set_matrix(np.zeros((16,16)))
            self.set_matrix(pixels[:,i:16+i])
            time.sleep(sleep_time)


        self.clock_face()


test = OutputHandler(16,32)
test.clock_face()
test.text_scroll("Hello world. How are you?",4)
