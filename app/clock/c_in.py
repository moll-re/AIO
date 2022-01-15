import time

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
        # self db_utils set externally

    def start(self):
        helpers.timer.RepeatedTimer(120, self.spread_measure)

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
            results[e] = sum(lst) / len(lst)

        self.db_utils.sensor_log(**results)

