import time
import numpy as np

from clock.api import converter
try:
    from clock.api.hat import unicorn as HAT
except ImportError:
    print("Using the simulator")
    from clock.api.hat import sim as HAT



class OutputHandler():
    def __init__(self, width, height, primary = [200, 200, 200], secondary = [10, 200, 10], error = [200, 10, 10]):
        """width is presumed to be larger than height"""
        self.width = width
        self.height = height
        self.output = HAT.UnicornHat(width, height)
        self.primary = primary
        self.secondary = secondary
        self.red = error



    def set_matrix(self, matrix, quadrant = 1, colors = []):
        """assumes 1 for primary, 2 for secondary color (everything beyond is treated as an error)
        quadrant: 1,2,3,4 : 4|1
                            ___
                            3|2
        """

        # reshape to the main size: (eg 32x16) (always aligns the given matrix on top left.)


        # add depth (rgb values)
        r3 = self.matrix_add_depth(matrix,colors)
        self.set_matrix_rgb(r3,quadrant)


    def matrix_add_depth(self, matrix, colors = []):
        """transforms a 2d-array with 0,1,2 to a 3d-array with the rgb values for primary and secondary color"""

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


        r3 = np.zeros((matrix.shape[0],matrix.shape[1],3),dtype=int)
        for i in range(matrix.shape[0]):
            for j in range(matrix.shape[1]):
                t = int(matrix[i, j])
                if t == 0:
                    r3[i, j, :] = [0,0,0]
                elif t == 1:
                    r3[i, j, :] = c1
                elif t == 2:
                    r3[i, j, :] = c2
                else:
                    r3[i, j, :] = c3
        return r3



    def set_matrix_rgb(self, matrix, quadrant=1):
        result = np.zeros((self.height, self.width,3))
        if quadrant == 1:
            result[:matrix.shape[0], self.width-matrix.shape[1]:,...] = matrix
        elif quadrant == 2:
            result[self.height-matrix.shape[0]:, self.width-matrix.shape[1]:,...] = matrix
        elif quadrant == 3:
            result[self.height-matrix.shape[0]:, :matrix.shape[1],...] = matrix
        else: # 4 or more
            result[:matrix.shape[0], :matrix.shape[1],...] = matrix

        self.output.set_matrix(result)


    def clock_face(self,weather):
        hour = converter.time_converter()
        day = converter.date_converter()
        face1 = hour + day
        face1_3d = self.matrix_add_depth(face1)


        face2_3d = converter.weather_converter(weather)
        face = np.zeros((max(face1_3d.shape[0],face2_3d.shape[0]),face1_3d.shape[1]+face2_3d.shape[1],3))

        face[:face1_3d.shape[0],:face1_3d.shape[1],...] = face1_3d
        face[:face2_3d.shape[0],face1_3d.shape[1]:,...] = face2_3d
        self.set_matrix_rgb(face)


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
