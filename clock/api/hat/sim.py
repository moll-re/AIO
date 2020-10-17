import sys
import colorsys
import pygame.gfxdraw
import time
import pygame
import numpy

class UnicornHat(object):
    def __init__(self, width, height):
        # Compat with old library

        # Set some defaults
        self.rotation(0)
        self.pixel_size = 20
        self.height = height
        self.width = width
        self.pixels = numpy.zeros((self.height,self.width,3), dtype=int)

        self.window_width = self.width * self.pixel_size
        self.window_height = self.height * self.pixel_size

        # Init pygame and off we go
        pygame.init()
        pygame.display.set_caption("Unicorn HAT simulator")
        self.screen = pygame.display.set_mode([self.window_width, self.window_height])
        self.clear()


    def set_pixel(self, x, y, r, g, b):
        self.pixels[x][y] = int(r), int(g), int(b)


    def set_matrix(self, matrix):
        self.pixels = matrix
        self.show()


    def draw(self):
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT:
                print("Exiting...")
                sys.exit()

        for i in range(self.height):
            for j in range(self.width):
                self.draw_led(i,j)


    def draw_led(self,i, j):
        p = self.pixel_size
        w_x = int(j * p + p / 2)
        #w_y = int((self.height - 1 - y) * p + p / 2)
        w_y = int(i * p + p / 2)
        r = int(p / 4)
        color = self.pixels[i,j,:]
        pygame.gfxdraw.aacircle(self.screen, w_x, w_y, r, color)
        pygame.gfxdraw.filled_circle(self.screen, w_x, w_y, r, color)


    def show(self):
        self.clear()
        self.draw()
        pygame.display.flip()
        pygame.event.pump()
        #time.sleep(5)


    def get_shape(self):
        return (self.width, self.height)


    def set_brightness(self, *args):
        pass


    def rotation(self, r):
        self._rotation = int(round(r/90.0)) % 3


    def clear(self):
        self.screen.fill((0, 0, 0))


    def get_rotation(self):
        return self._rotation * 90


    def set_layout(self, *args):
        pass


    def off(self):
        print("Closing window")
        pygame.quit()
