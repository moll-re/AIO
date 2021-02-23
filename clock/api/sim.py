import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
mpl.rcParams['toolbar'] = 'None'
mpl.use('WX')




class ClockOut():
    """Simulate a clock output on a computer screen"""
    def __init__(self, shape):
        plt.axis('off')
        plt.ion()
        nshape = (*shape, 3)
        zero = np.zeros(nshape)
        self.figure, ax = plt.subplots()
        ax.set_axis_off()
        i = Image.fromarray(zero, "RGB")
        self.canvas = ax.imshow(i)
    
    def put(self, matrix):
        matrix_rescale = matrix / 255
        self.canvas.set_array(matrix_rescale)        
        self.figure.canvas.draw()
        self.figure.canvas.flush_events()        
