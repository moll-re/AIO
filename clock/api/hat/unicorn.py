import colorsys
import time
import numpy

import RPi.GPIO as GPIO


class UnicornHat(object):
    def __init__(self, width, height, rotation_offset = 0):
        self.PIN_CLK = 11
        ##################################
        # GPIO Pins for the actual signal. The other ones are for signal clocks and resets.
        self.PINS_DAT = [10, 22]
        ##################################
        self.PIN_CS = 8

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.PIN_CS, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(self.PIN_CLK, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.PINS_DAT, GPIO.OUT, initial=GPIO.LOW)

        self.SOF = 0x72
        self.DELAY = 1.0/120
        self.WIDTH = width #32
        self.HEIGHT = height #16

        self.rotation = 1
        self.brightness = 1
        self.buffer = numpy.zeros((self.HEIGHT,self.WIDTH,3), dtype=int)

        self.reset_clock()

    def reset_clock(self):
        GPIO.output(self.PIN_CS, GPIO.LOW)
        time.sleep(0.000001)
        GPIO.output(self.PIN_CS, GPIO.HIGH)

    def spi_write(self, buf1, buf2):
        GPIO.output(self.PIN_CS, GPIO.LOW)

        self.spi_write_byte(self.SOF, self.SOF)

        for x in range(len(buf1)):
            b1, b2= buf1[x], buf2[x]
            self.spi_write_byte(b1, b2)
            time.sleep(0.0000001)

        GPIO.output(self.PIN_CS, GPIO.HIGH)

    def spi_write_byte(self, b1, b2):
        for x in range(8):
            GPIO.output(self.PINS_DAT[0], b1 & 0b10000000)
            GPIO.output(self.PINS_DAT[1], b2 & 0b10000000)
            GPIO.output(self.PIN_CLK, GPIO.HIGH)
            b1 <<= 1
            b2 <<= 1
            time.sleep(0.00000001)
            GPIO.output(self.PIN_CLK, GPIO.LOW)

    def set_brightness(self, b):
        """Set the display brightness between 0.0 and 1.0.
        :param b: Brightness from 0.0 to 1.0 (default 1)
        """
        self.brightness = b

    def rotation(self, r):
        """Set the display rotation in degrees.
        Actual rotation will be snapped to the nearest 90 degrees.
        """
        self.rotation = int(round(r/90.0))

    def get_rotation(self):
        """Returns the display rotation in degrees."""
        return self.rotation * 90

    def set_layout(self, pixel_map=None):
        """Does nothing, for library compatibility with Unicorn HAT."""
        pass

    def set_all(self, r, g, b):
        self.buffer[:] = r, g, b

    def set_pixel(self, x, y, r, g, b):
        """Set a single pixel to RGB colour.
        :param x: Horizontal position from 0 to width
        :param y: Veritcal position from 0 to height
        :param r: Amount of red from 0 to 255
        :param g: Amount of green from 0 to 255
        :param b: Amount of blue from 0 to 255
        """
        self.buffer[y][x] = r, g, b


    def set_matrix(self, matrix):
        self.buffer = matrix
        self.show()


    def set_pixel_hsv(self, x, y, h, s=1.0, v=1.0):
        """set a single pixel to a colour using HSV.
         :param x: Horizontal position from 0 to 15
         :param y: Veritcal position from 0 to 15
         :param h: Hue from 0.0 to 1.0 ( IE: degrees around hue wheel/360.0 )
         :param s: Saturation from 0.0 to 1.0
         :param v: Value (also known as brightness) from 0.0 to 1.0
        """

        r, g, b = [int(n*255) for n in colorsys.hsv_to_rgb(h, s, v)]
        self.set_pixel(x, y, r, g, b)

    def get_pixel(self, x, y):
        return tuple(self.buffer[x][y])

    def shade_pixels(self, shader):
        for x in range(self.WIDTH):
            for y in range(self.HEIGHT):
                r, g, b = shader(x, y)
                self.set_pixel(x, y, r, g, b)

    def get_pixels(self):
        return self.buffer

    def get_shape(self):
        """Return the shape (width, height) of the display."""

        return self.WIDTH, self.HEIGHT

    def clear(self):
        """Clear the buffer."""
        self.buffer.fill(0)

    def off(self):
        """Clear the buffer and immediately update Unicorn HAT HD.
        Turns off all pixels.
        """
        self.clear()
        self.show()

    def show(self):
        """Output the contents of the buffer to Unicorn HAT HD."""
        ##########################################################
        ## Change to desire
        buff1 = numpy.rot90(self.buffer[:self.HEIGHT,:16],1)
        buff2 = numpy.rot90(self.buffer[:self.HEIGHT,16:32],1)
        ##########################################################

        buff1, buff2 = [(x.reshape(768) * self.brightness).astype(numpy.uint8).tolist() for x in (buff1, buff2)]

        self.spi_write(buff1, buff2)

        time.sleep(self.DELAY)
