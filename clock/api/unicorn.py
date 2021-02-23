import colorsys
import time
import numpy

import RPi.GPIO as GPIO


class ClockOut(object):
    def __init__(self, shape):
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

        self.HEIGHT = shape[0] #16
        self.WIDTH = shape[1] #32

        self.reset_clock()


    def reset_clock(self):
        GPIO.output(self.PIN_CS, GPIO.LOW)
        time.sleep(0.00001)
        GPIO.output(self.PIN_CS, GPIO.HIGH)


    def spi_write(self, buf1, buf2):
        GPIO.output(self.PIN_CS, GPIO.LOW)

        self.spi_write_byte(self.SOF, self.SOF)

        for x in range(len(buf1)):
            b1, b2= buf1[x], buf2[x]
            self.spi_write_byte(b1, b2)


        GPIO.output(self.PIN_CS, GPIO.HIGH)


    def spi_write_byte(self, b1, b2):
        for x in range(8):
            GPIO.output(self.PINS_DAT[0], b1 & 0b10000000)
            GPIO.output(self.PINS_DAT[1], b2 & 0b10000000)
            GPIO.output(self.PIN_CLK, GPIO.HIGH)

            b1 <<= 1
            b2 <<= 1
            #time.sleep(0.00000001)
            GPIO.output(self.PIN_CLK, GPIO.LOW)




    def put(self, matrix):
        """Sets a height x width matrix directly"""
        self.reset_clock()
        self.show(matrix)


    def clear(self):
        """Clear the buffer."""
        zero = np.zero((self.HEIGHT, self. WIDTH))
        self.put(zero)


    def show(self, matrix):
        """Output the contents of the buffer to Unicorn HAT HD."""
        ##########################################################
        ## Change to desire
        buff2 = numpy.rot90(matrix[:self.HEIGHT,:16],3)
        buff1 = numpy.rot90(matrix[:self.HEIGHT,16:32],1)
        ##########################################################

        buff1, buff2 = [(x.reshape(768)).astype(numpy.uint8).tolist() for x in (buff1, buff2)]

        self.spi_write(buff1, buff2)

        time.sleep(self.DELAY)
