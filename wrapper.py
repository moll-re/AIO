import time

class Wrapper():
    """Wrapper skeleton for the modules (bot, clock dashboard...)"""

    def __init__(self, own_module, *other_modules):
        self.own = own_module
        self.others = other_modules

        

    def mainloop(self, sleep_delta, action):
        """sleep_delta in seconds sets the sleep period of the loop
            action is a function that is performed every * seconds"""
        while True:
            action()
            time.sleep(sleep_delta)
