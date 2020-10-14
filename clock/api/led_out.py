import time
import numpy as np

from clock.api import converter
try:
    from clock.api.hat import unicorn as HAT
except ImportError:
    print("Using the simulator")
    from clock.api.hat import sim as HAT



class OutputHandler():
    def __init__(self, width, height):
        """width is presumed to be larger than height"""
        self.width = width
        self.height = height
        self.output = HAT.UnicornHat(width, height)
        self.primary = [230, 230, 230]
        self.secondary = [10, 200, 10]
        self.red = [200, 10, 10]
        self.weather_string = ""
        self.weather_matrix = []


    def set_matrix(self, matrix, quadrant, colors = []):
        """assumes 1 for primary, 2 for secondary color (everything beyond is treated as an error)
        quadrant: 1,2,3,4 : 4|1
                            ___
                            3|2
        """

        # reshape to the main size: (eg 32x16) (always aligns the given matrix on top left.)

        c1 = self.primary
        c2 = self.secondary
        c3 = self.red
        if len(colors) == 1:
            c1 = colors[0]
        if len(colors) == 2:
            c2 = colors[1]
        if len(colors) == 3:
            c3 = colors[2]
        if len(colors) > 3:
            print("Too many colors")

        result = np.zeros((self.height, self.width))
        if quadrant == 1:
            result[:matrix.shape[0], self.width-matrix.shape[1]:] = matrix
        elif quadrant == 2:
            result[self.height-matrix.shape[0]:, self.width-matrix.shape[1]:] = matrix
        elif quadrant == 3:
            result[self.height-matrix.shape[0]:, :matrix.shape[1]] = matrix
        else: # 4 or more
            result[:matrix.shape[0], :matrix.shape[1]] = matrix

        # add depth (rgb values)
        r3 = np.zeros((self.height,self.width,3),dtype=int)
        for i in range(self.height):
            for j in range(self.width):
                t = int(result[i, j])
                if t == 0:
                    r3[i, j, :] = [0,0,0]
                elif t == 1:
                    r3[i, j, :] = c1
                elif t == 2:
                    r3[i, j, :] = c2
                else:
                    r3[i, j, :] = c3
        self.output.set_matrix(r3)


    def clock_face(self,weather):
        hour = converter.time_converter()
        day = converter.date_converter()
        face1 = hour + day

        if self.weather_matrix == [] or weather != self.weather_string:
            self.weather_matrix = converter.weather_converter("clouds")
            self.weather_string = weather

        face2 = self.weather_matrix

        face = np.zeros((max(face1.shape[0],face2.shape[0]),face1.shape[1]+face2.shape[1]))
        face[:face1.shape[0],:face1.shape[1]] = face1
        face[:face2.shape[0],face1.shape[1]:] = face2
        self.set_matrix(face, 4)


    def text_scroll(self, text, speed, color):
        pixels = converter.text_converter(text, 12)
        sleep_time = 1 / speed
        if color == "":
            colors = []
        else:
            colors = [color]

        frames = pixels.shape[1] - self.width
        if frames <= 0:
            frames = 1

        for i in range(frames):
            visible = pixels[:,i:self.width+i]
            self.set_matrix(visible,4,colors)
            time.sleep(sleep_time)
        time.sleep(10 * sleep_time)
