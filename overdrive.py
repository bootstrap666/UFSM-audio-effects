import numpy as np

import erfapprox

class Overdrive:
    def __init__(self,gain:float,volume:float):
        self.gain = gain
        self.volume = volume
    
    def set_volume(self,volume:float):
        self.volume = volume
    
    def set_gain(self, gain:float):
        self.gain = gain

    def read_volume(self)->float:
        return self.volume
    
    def read_gain(self)->float:
        return self.gain
    
    def distort(self, x):
        return self.volume*erfapprox.erf1(self.gain*x)