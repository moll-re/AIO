import sys
import colorsys
import pygame.gfxdraw
import time
import pygame
import numpy

class ClockOut:
    """Creates a drawable window in case the real hardware is not accessible. For development"""
    def __init__(self, shape):
        self.pixel_size = 20

        self.shape = shape
        self.pixels = numpy.zeros((*shape,3), dtype=int)
        self.WIDTH = shape[1]
        self.HEIGHT = shape[0]
        self.window_width = self.WIDTH * self.pixel_size
        self.window_height = self.HEIGHT * self.pixel_size

        pygame.init()
        pygame.display.set_caption("Unicorn HAT simulator")
        self.screen = pygame.display.set_mode([self.window_width, self.window_height])


    def put(self, matrix):
        self.screen.fill((0, 0, 0))
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT:
                print("Exiting...")
                pygame.quit()
                sys.exit()
        self.pixels = matrix
        self.draw_pixels()
        
        pygame.display.flip()
        pygame.event.pump()


    def draw_pixels(self):
        p = self.pixel_size
        
        r = int(p / 4)
        for i in range(self.HEIGHT):
            for j in range(self.WIDTH):
                w_x = int(j * p + p / 2)
                #w_y = int((self.HEIGHT - 1 - y) * p + p / 2)
                w_y = int(i * p + p / 2)
                color = self.pixels[i,j,:]
                color = color.astype("int")

                pygame.gfxdraw.aacircle(self.screen, w_x, w_y, r, color)
                pygame.gfxdraw.filled_circle(self.screen, w_x, w_y, r, color)
