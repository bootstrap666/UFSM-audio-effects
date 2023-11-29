import numpy as np
from numpy.fft import fft,ifft

class Fractional_delay:
    def __init__(self, magnitude:float, delay:float, sampling_rate:int, fft_length:int, filter_length=-1):

        self._magnitude = magnitude
        self._delay = delay
        self._sampling_rate = sampling_rate
        self._fft_length = fft_length
        
        if(filter_length<0):
            self._filter_length = 1024
        else:
            self._filter_length = filter_length
            
        self.set_delay(delay)

    def read_impulse_response(self)->np.ndarray:
        return ifft(self._freq_response)
    
    def set_delay(self, delay:float):
        D = delay*self._sampling_rate

        self._freq_response = np.power(np.e,np.sqrt(-1)*2*np.pi*delay*np.arange(self._filter_length)/self._filter_length)
   
    def get_filter_length(self):
        return  self._filter_length