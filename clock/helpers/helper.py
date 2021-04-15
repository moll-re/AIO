from PIL import Image, ImageDraw, ImageFont
import numpy as np
import datetime
import time

# bulky hard-coded values:
from . import shapes
digits = shapes.digits
weather_categories = shapes.weather_categories
digit_position = [[2,4], [2,10], [9,4], [9,10]]


days = np.append(np.zeros((15,16)), np.array([0,1,0,1,0,1,0,1,0,1,0,1,1,0,1,1])).reshape((16,16))




class MatrixOperations():
    """Helper functions to generate frequently-used images"""
    def __init__(self, shape, default_colors):
        self.shape = shape
        # shape is going to be (16,32) for the moment
        self.primary = default_colors["primary"]
        self.secondary = default_colors["secondary"]
        self.error = default_colors["error"]


    def time_converter(self, top="", bottom=""):
        """Converts 4-digit time to a pixel-matrix
        returns: np.array wich fills one half of self.shape (horizontally)"""
        nshape = (self.shape[0], int(self.shape[1]/2))
        pixels = np.zeros(nshape,dtype=np.uint8)

        if bottom == "" or top == "":
            top = datetime.datetime.now().strftime("%H")
            bottom = datetime.datetime.now().strftime("%M")

        if len(top) < 2:
            top = "0" * (2 - len(top)) + top
        if len(bottom) < 2:
            bottom = "0" * (2 - len(bottom)) + bottom

        if ("-" in top and len(top) > 2) or ("-" in bottom and len(bottom) > 2):
            time_split = 4*["-"]
        elif "error" in top and "error" in bottom:
            time_split = 4*["error"]
        else:
            time_split = [i for i in top] + [i for i in bottom]

        if "-1" in top and len(top) != 2:
            time_split = ["-1", top[-1]] + [i for i in bottom]
        if "-1" in bottom and len(bottom) != 2:
            time_split = [i for i in top] + ["-1", bottom[-1]]
        
        for i in range(4):
            x = digit_position[i][0]
            y = digit_position[i][1]
            number = digits[time_split[i]]
            pixels[x: x + 5, y: y + 3] = np.array(number)

        return pixels


    def date_converter(self):
        nshape = (self.shape[0], int(self.shape[1]/2))
        today = datetime.datetime.today()
        weekday = datetime.datetime.weekday(today)
        # size of the reduced array according to weekday
        size = [2,4,6,8,10,13,16]

        pixels = days.copy() #base color background
        lrow = np.append(pixels[15,:size[weekday]], [0 for i in range(16 - size[weekday])])
        lrow = np.append(np.zeros((15,16)), lrow).reshape(nshape)
        pixels += lrow
        return pixels


    def weather_converter(self, name):
        """Fills one half of the screen with weather info."""
        nshape = (self.shape[0], int(self.shape[1]/2))
        result = np.zeros(nshape)
        cwd = __file__.replace("\\","/") # for windows
        cwd = cwd.rsplit("/", 1)[0]  # the current working directory (where this file is)
        if len(cwd) == 0:
            cwd = "."
        icon_spritesheet = cwd + "/weather-icons.bmp"

        icons = Image.open(icon_spritesheet)
        icons_full = np.array(icons)

        icon_loc = ["sun","moon","sun and clouds", "moon and clouds", "cloud","fog and clouds","2 clouds", "3 clouds", "rain and cloud", "rain and clouds", "rain and cloud and sun", "rain and cloud and moon", "thunder and cloud", "thunder and cloud and moon", "snow and cloud", "snow and cloud and moon", "fog","fog night"]
        #ordered 1 2 \n 3 4 \ 5 5 ...
        name = weather_categories[name]
        try:
            iy, ix = int(icon_loc.index(name)/2), icon_loc.index(name)%2
            # x and y coords
        except:
            return np.zeros((*nshape,3))

        icon_single = icons_full[16*iy:16*(iy + 1),16*ix:16*(ix + 1),...]
        return icon_single


    def matrix_add_depth(self, matrix, colors = []):
        """transforms a 2d-array with 0,1,2 to a 3d-array with the rgb values for primary and secondary color"""

        c1 = self.primary
        c2 = self.secondary
        c3 = self.error
        if len(colors) > 0:
            c1 = colors[0]
        if len(colors) > 1:
            c2 = colors[1]
        if len(colors) > 2:
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



    def clock_face(self, weather):
        """weather as a dict"""
        hour = self.time_converter()
        day = self.date_converter()
        face1 = hour + day
        face1_3d = self.matrix_add_depth(face1)

        if weather["show"] == "weather":
            face2_3d = self.weather_converter(weather["weather"])
        else:
            face2 = self.time_converter(top=str(weather["low"]), bottom=str(weather["high"]))
            face2 = np.concatenate((face2[:8,...],2*face2[8:,...]))
            face2_3d = self.matrix_add_depth(face2,[[0, 102, 255],[255, 102, 0]])

        face = np.zeros((max(face1_3d.shape[0],face2_3d.shape[0]),face1_3d.shape[1]+face2_3d.shape[1],3))

        face[:face1_3d.shape[0],:face1_3d.shape[1],...] = face1_3d
        face[:face2_3d.shape[0],face1_3d.shape[1]:,...] = face2_3d
        
        return face

    
    def text_converter(self, text, height, color):
        """Converts a text to a pixel-matrix
        returns: np.array((16, x, 3))"""

        font = ImageFont.truetype("verdanab.ttf", height)
        size = font.getsize(text)
        img = Image.new("1",size,"black")
        draw = ImageDraw.Draw(img)
        draw.text((0, 0), text, "white", font=font)
        pixels = np.array(img, dtype=np.uint8)
        pixels3d = self.matrix_add_depth(pixels, color)
        return pixels3d
