import sys
import colorsys
import pygame.gfxdraw
import time
import pygame

class UnicornHat(object):
    def __init__(self, width, height, rotation_offset = 0):
        # Compat with old library

        # Set some defaults
        self.rotation_offset = rotation_offset
        self.rotation(0)
        self.pixels = [(0, 0, 0)] * width * height
        self.pixel_size = 25
        self.height = height
        self.width = width
        self.window_width = width * self.pixel_size
        self.window_height = height * self.pixel_size

        # Init pygame and off we go
        pygame.init()
        pygame.display.set_caption("Unicorn HAT simulator")
        self.screen = pygame.display.set_mode([self.window_width, self.window_height])
        self.clear()

    def set_pixel(self, x, y, r, g, b):
        i = (x * self.width) + y
        self.pixels[i] = [int(r), int(g), int(b)]

    def draw(self):
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT:
                print("Exiting...")
                sys.exit()

        for x in range(self.width):
            for y in range(self.height):
                self.draw_led(x, y)

    def show(self):
        self.clear()
        self.draw()
        pygame.display.flip()
        #time.sleep(5)

    def draw_led(self, x, y):
        p = self.pixel_size
        w_x = int(x * p + p / 2)
        w_y = int((self.height - 1 - y) * p + p / 2)
        r = int(p / 4)
        color = self.pixels[self.index(x, y)]
        pygame.gfxdraw.aacircle(self.screen, w_x, w_y, r, color)
        pygame.gfxdraw.filled_circle(self.screen, w_x, w_y, r, color)

    def get_shape(self):
        return (self.width, self.height)

    def brightness(self, *args):
        pass

    def rotation(self, r):
        self._rotation = int(round(r/90.0)) % 3

    def clear(self):
        self.screen.fill((0, 0, 0))

    def get_rotation(self):
        return self._rotation * 90

    def set_layout(self, *args):
        pass

    def set_pixel_hsv(self, x, y, h, s=1.0, v=1.0):
        r, g, b = [int(n*255) for n in colorsys.hsv_to_rgb(h, s, v)]
        self.set_pixel(x, y, r, g, b)

    def off(self):
        print("Closing window")
        #pygame.quit()

    def index(self, x, y):
        # Offset to match device rotation
        rot = (self.get_rotation() + self.rotation_offset) % 360

        if rot == 0:
            xx = x
            yy = y
        elif rot == 90:
            xx = self.height - 1 - y
            yy = x
        elif rot == 180:
            xx = self.width - 1 - x
            yy = self.height - 1 - y
        elif rot == 270:
            xx = y
            yy = self.width - 1 - x
        return (xx * self.width) + yy


"""
# SD hats works as expected
#unicornhat = UnicornHatSim(8,8)
#unicornphat = UnicornHatSim(8, 4)

# Unicornhat HD seems to be the other way around (not that there's anything wrong with that), so we rotate it 180°
# unicornhathd = UnicornHatSim(16, 16, 180)
twohats = UnicornHatSim(16, 32, 180)


for i in range(16):
    twohats.set_pixel(i,i, 200,200,200)
    twohats.show()
    time.sleep(1)
"""
