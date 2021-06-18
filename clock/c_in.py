import datetime
import time
from threading import Thread, Timer

from . import hardware, helpers


class SensorReadout:
    """Overview class for (actual and potential) sensor sources"""

    def __init__(self):
        """"""
        self.sensor_modules = { # we already call them, they are objects and not classes anymore
            "temperature" : hardware.sensors.TemperatureModule(),
            "humidity" : hardware.sensors.HumidityModule(),
            "brightness" : hardware.sensors.BrightnessModule(),
            # more to come?
        }

    def start(self):
        helpers.timer.RepeatedTimer(300, self.spread_measure)

    def spread_measure(self):
        results = dict((el,[]) for el in self.sensor_modules.keys()) # create an empty dict with a list for each readout-type
        for _ in range(5): # number of measures to average out
            for name in self.sensor_modules.keys():
                measure = self.sensor_modules[name].readout()
                results[name].append(measure)
                time.sleep(3)
        
        self.save_results(results)


    def save_results(self, results):
        current_minute = int(datetime.datetime.now().timestamp() // 60)
        
        self.persistence["clock"]["sensors"]["time"] += [current_minute]

        for name in results.keys():
            keep_value = sum(results[name]) / len(results[name])
            self.persistence["clock"]["sensors"][name] += [keep_value]

    
