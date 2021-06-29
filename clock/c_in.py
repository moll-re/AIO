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
            "luminosity" : hardware.sensors.BrightnessModule(),
            # more to come?
        }

    def start(self):
        helpers.timer.RepeatedTimer(300, self.spread_measure)

    def spread_measure(self):
        measurements = dict((el,[]) for el in self.sensor_modules.keys())
        # create an empty dict with a list for each readout-type

        for _ in range(5): # number of measures to average out
            for name in self.sensor_modules.keys():
                measure = self.sensor_modules[name].readout()
                measurements[name].append(measure)
                time.sleep(3)

        results = {}
        for e in measurements.keys():
            lst = measurements[e]
            results[e] = int(sum(lst) / len(lst))

        self.save_results(**results)


    # def save_results(self, results):
    #     current_minute = int(datetime.datetime.now().timestamp() // 60)
        
    #     self.persistence["clock"]["sensors"]["time"] += [current_minute]

    #     for name in results.keys():
    #         keep_value = sum(results[name]) / len(results[name])
    #         self.persistence["clock"]["sensors"][name] += [keep_value]

    
    def save_results(self, **results):
        data = self.db.sensors(
            time=datetime.datetime.now(),
            **results,
            )
        data.save()
