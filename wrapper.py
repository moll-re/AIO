import time
import datetime
import logging
import threading

logger = logging.getLogger(__name__)

class Wrapper():
    """Wrapper skeleton for the modules (bot, clock, dashboard ... maybe more to come?)"""

    def __init__(self, own_module, *other_modules):
        self.own = own_module
        self.others = other_modules

        logger.debug("Starting " + self.own.__class__.__name__ + " through wrapper.")

        
    def external_action(self, func, *args, **kwargs):
        """do a special action initiated by other modules"""
        logger.info("External request to " + self.own.__class__.__name__ + ".")




class ClockWrapper(Wrapper):
    """Wrapper for the CLOCK-functionality"""
    def __init__(self, own_module, *other_modules):
        """"""
        super().__init__(own_module, *other_modules)
        self.weather = {"weather":"", "high":"", "low":"", "show":"temps"}
        self.weather_raw = {}
        self.START()
        


    def START(self): # I prefer the name tick_tack
        """Runs the showing of the clock-face periodically: update every minute"""    
        def perform_loop():
            t = int(datetime.datetime.now().strftime("%H%M"))

            if t % 5 == 0:
                # switch secondary face every 5 minutes
                weather = self.others[0].api_weather.show_weather([47.3769, 8.5417]) # zürich

                if weather != self.weather_raw and len(weather) != 0:
                    td = weather[1]
                    low = td["temps"][0]
                    high = td["temps"][1]
                    self.weather["weather"] = td["short"]
                    self.weather["high"] = high
                    self.weather["low"] = low
                elif len(weather) == 0:
                    self.weather["weather"] = "error"
                    self.weather["high"] = "error"
                    self.weather["low"] = "error"
                # if weather == self.weather.raw do nothing

                if self.weather["show"] == "weather":
                    next = "temps"
                else:
                    next = "weather"
                self.weather["show"] = next
    
            self.own.set_face(self.weather)
        
        perform_loop()
        while datetime.datetime.now().strftime("%H%M%S")[-2:] != "00":
            pass
        RepeatedTimer(60, perform_loop)
        


class BotWrapper(Wrapper):
    """Wrapper for the BOT-functionality"""
    def __init__(self, own_module, *other_modules):
        """"""
        super().__init__(own_module, *other_modules)
        self.own.START()



class DashBoardWrapper(Wrapper):
    def __init__(self, own_module, *other_modules):
        """Wrapper for the dashboard functionality"""
        super().__init__(own_module, other_modules)
        # self.mainloop(1 * 3600) # 1 hour refresh-cycle
        # cannot get called through mainloop, will use the included callback-functionality of Dash
        self.own.bot = other_modules[0]
        self.own.START()



class RepeatedTimer(object):
  def __init__(self, interval, function, *args, **kwargs):
    self._timer = None
    self.interval = interval
    self.function = function
    self.args = args
    self.kwargs = kwargs
    self.is_running = False
    self.next_call = time.time()
    self.start()

  def _run(self):
    self.is_running = False
    self.start()
    self.function(*self.args, **self.kwargs)

  def start(self):
    if not self.is_running:
      self.next_call += self.interval
      self._timer = threading.Timer(self.next_call - time.time(), self._run)
      self._timer.start()
      self.is_running = True

  def stop(self):
    self._timer.cancel()
    self.is_running = False
