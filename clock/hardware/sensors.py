import time
import logging
logger = logging.getLogger(__name__)

class TempSim:
    """Simulates a temperature for running on windows"""
    temperature = 23 # return a celsius value
    humidity = 30
    

class LightSim:
    def input(self, *args):
        return 1




class SensorModule:
    def __init__(self):
        logger.info("Using module " + self.__class__.__name__)



## Real sensors!
try:
    import board
    import adafruit_dht 
    dht11 = adafruit_dht.DHT11(board.D18)
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(4, GPIO.IN)
except ImportError:
    logger.warn("Simulating sensor modules")
    dht11 = TempSim()
    GPIO = LightSim()


class TemperatureModule(SensorModule):
    """Takes readouts from the DHT 11
    Returns: temperature"""
    def __init__(self):
        super().__init__()
        self.device = dht11
        
    def readout(self):
        try:
            temp = self.device.temperature
        except:
            time.sleep(1)
            try:
                temp = self.device.temperature
            except:
                temp = -1
        
        return temp
                        
class HumidityModule(SensorModule):
    """Takes readouts from the DHT 11
    Returns: humidity"""
    def __init__(self):
        super().__init__()
        self.device = dht11
        
    def readout(self):
        try:
            hum = self.device.humidity
        except:
            time.sleep(1)
            try:
                hum = self.device.humidity
            except:
                hum = -1
        
        return hum

class BrightnessModule(SensorModule):
    """Returns one for HIGH and zero for LOW"""
    def __init__(self):
        super().__init__()

    def readout(self):
        # The sensor is reversed: 0 when bright and 1 if dark
        light = GPIO.input(4)
        if light == 0:
            return 1
        else:
            return 0
