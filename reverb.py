import numpy as np
import numpy.random as rnd
import math

import overlap_add

class Reverb:
    def __init__(self, reverberation_time:float, sampling_rate:int):

        self._reverberation_time = reverberation_time
        self._sampling_rate = sampling_rate

        self._impulse_response = rnd.normal(0.0,1.0, size=math.ceil(reverberation_time*sampling_rate))

        alpha = -3.0*np.log(10)/(reverberation_time*sampling_rate)

        self._impulse_response = np.multiply(self._impulse_response, np.exp(alpha*np.arange(0,len(self._impulse_response))))
        self._impulse_response = self._impulse_response/np.linalg.norm(self._impulse_response,2)

    def read_impulse_response(self)->np.ndarray:
        return self._impulse_response
    
    def distort(self,x):
        if x.ndim < 2:
            return overlap_add.fftfilt(self._impulse_response,x)
        else:
            output = np.zeros((x.shape[0],x.shape[1]))
            for i in range(x.shape[1]):
                output [:,i] = overlap_add.fftfilt(self._impulse_response,x[:,i])
            return output
