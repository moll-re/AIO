import time
import numpy as np



try:
    from . import unicorn
    output = unicorn.ClockOut
except ImportError:
    from . import sim
    output = sim.ClockOut

# import sim
# output = sim.ClockOut

class OutputHandler():
    """Matrix of led-points (RGB- values). It has the two given dimensions + a third which is given by the color values"""

    # def __new__(subtype, shape, dtype=float, buffer=None, offset=0,
    #             strides=None, order=None, info=None):
    #     # Create the ndarray instance of our type, given the usual
    #     # ndarray input arguments.  This will call the standard
    #     # ndarray constructor, but return an object of our type.
    #     # It also triggers a call to InfoArray.__array_finalize__

    #     # expand the given tuple (flat display) to a 3d array containing the colors as well
    #     nshape = (*shape, 3)
    #     obj = super(OutputHandler, subtype).__new__(subtype, nshape, "int",
    #                                             buffer, offset, strides,
    #                                             order)
    #     # set the new 'info' attribute to the value passed
    #     obj.info = info
    #     obj.OUT = output(shape)
    #     # Finally, we must return the newly created object:
    #     return obj
    def __init__(self, shape):
        nshape = (*shape, 3)
        self.array = np.array(shape, dtype=np.uint8)
        self.OUT = output(shape)


    # def __array_finalize__(self, obj):
    #     self.OUT = sim.ClockOut()
    #     # ``self`` is a new object resulting from
    #     # ndarray.__new__(), therefore it only has
    #     # attributes that the ndarray.__new__ constructor gave it -
    #     # i.e. those of a standard ndarray.
    #     #
    #     # We could have got to the ndarray.__new__ call in 3 ways:
    #     # From an explicit constructor - e.g. InfoArray():
    #     #    obj is None
    #     #    (we're in the middle of the InfoArray.__new__
    #     #    constructor, and self.info will be set when we return to
    #     #    InfoArray.__new__)
    #     if obj is None: return
    #     # From view casting - e.g arr.view(InfoArray):
    #     #    obj is arr
    #     #    (type(obj) can be InfoArray)
    #     # From new-from-template - e.g infoarr[:3]
    #     #    type(obj) is InfoArray
    #     #
    #     # Note that it is here, rather than in the __new__ method,
    #     # that we set the default value for 'info', because this
    #     # method sees all creation of default objects - with the
    #     # InfoArray.__new__ constructor, but also with
    #     # arr.view(InfoArray).
    #     self.info = getattr(obj, 'info', None)
        
    #     # We do not need to return anything
        


    def SHOW(self):
        # self.output.set_matrix(self)
        
        self.OUT.put(self.array)


    # def __init__(self, width, height, primary = [200, 200, 200], secondary = [10, 200, 10], error = [200, 10, 10]):
    #     """width is presumed to be larger than height"""
    #     self.width = width
    #     self.height = height
    #     self.output = HAT.UnicornHat(width, height)
    #     self.primary = primary
    #     self.secondary = secondary
    #     self.red = error



    

