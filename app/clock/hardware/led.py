from . import unicorn as led
# or neopixel soon:
# from . import neopixel as led

def get_handler():
    OUT = led.ClockOut()
    shape = OUT.shape

    if led.SETUP_FAIL:
        # we use the sim
        del OUT
        from . import sim
        OUT = sim.ClockOut(shape)

    return OUT


