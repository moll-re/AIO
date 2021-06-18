# functionality
from clock import c_in, c_out
from broadcast import b_in

import launcher



class ReceiverLauncher(launcher.Launcher):
    """Launcher for all server-side modules. The hard-computations"""
    def __init__(self):
        
        self.clock_sensor_module = c_in.SensorReadout()
        # active: periodically takes readouts
        self.clock_hardware_module = c_out.ClockFace()
        # active: periodically calls fetcher
        self.receive_module = b_in.FetchUpdates(server_ip="192.168.1.110", port="1111")
        # passive: fetches data on demand

        super().__init__(
            sensors = self.clock_sensor_module,
            clock = self.clock_hardware_module,
            receive = self.receive_module
        )

        

ReceiverLauncher()