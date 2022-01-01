import time
import numpy as np
import colorsys
import random

try:
    import rpi_ws281x as ws
except ImportError:
    from unittest.mock import Mock
    ws = Mock()
    SETUP_FAIL = True


class ClockOut:
    def __init__(self):
        self.shape = (45, 20) # H x W
        num = self.shape[0] * self.shape[1]
        pin = 18 
        freq = 800000 # maybe higher
        dma = 5
        invert = False
        brightness = 100
        channel = 0
        led_type = None # ??
        self.strip = ws.PixelStrip(num, pin, freq, dma, invert, brightness, channel, led_type)
        self.strip.begin()
    

    def put(self, matrix):
        self.render(matrix)


    def render(self, matrix):
        p = 0
        for i in range(matrix.shape[0]):
            for j in range(matrix.shape[1]):
                col = int(ws.Color(*matrix[i,j]))

                self.strip.setPixelColor(p, col)
                p += 1
        self.strip.show()


# test = ClockOut()
# z = np.zeros((30,30, 3), dtype=int)
# for i in range(30):
#     for j in range(30):
#         z[i, j, ...] = [random.randint(0,255), random.randint(0,255), random.randint(0,255)]
#         test.put(z)
#         #time.sleep(0.1)

