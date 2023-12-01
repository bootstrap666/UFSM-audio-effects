import numpy as np

from sinusoid import Sinusoid
from fractional_delay import Fractional_delay

class Flanger:
    def __init__(self, sampling_rate:float, lfo_frequency=0.5, lfo_amplitude=0.008, average_delay=0.015, dry=0.5, wet=0.5):
        
        self._average_delay = int(average_delay*sampling_rate)
        self._lfo_amplitude = int(lfo_amplitude*sampling_rate)
        self._delay_filter = np.zeros(2*(self._lfo_amplitude+self._average_delay))
        self._dry = dry
        self._wet = wet
        self._delay = average_delay

        self._reset_input_vector()
        self._fft_length = 2<<(len(self._delay_filter)-1).bit_length()
        
        if self._fft_length < 8192:
            self._fft_length = 8192
        
        self._window_length = self._fft_length - len(self._delay_filter) + 1

        self._lfo = Sinusoid(frequency=lfo_frequency*self._window_length/sampling_rate)

    def _reset_input_vector(self):
        self._input_vector = np.zeros(self._lfo_amplitude+self._average_delay)

    def _set_delay(self):
        self._delay_filter = np.sinc(np.arange(self._lfo_amplitude+self._average_delay)-self._delay)

    def _overlap_add(self,x:np.ndarray)->np.ndarray:
        
        signal_length = x.shape[0]
        offsets = range(0, signal_length, self._window_length)

        output = np.zeros(signal_length+self._fft_length)
        output[:signal_length] = self._dry*x

        # overlap and add
        for n in offsets:
#            frequency_response = np.exp(np.sqrt(-1)*2*np.pi*np.arange((self._fft_length//2)+1)*self._delay)
            self._set_delay()
            frequency_response = np.fft.rfft(self._delay_filter,n=self._fft_length)
            output[n:n+self._fft_length] += self._wet*np.fft.irfft(np.multiply(np.fft.rfft(x[n:n+self._window_length], n=self._fft_length) , frequency_response), n=self._fft_length) 
            self._delay = self._average_delay +  self._lfo.step(self._lfo_amplitude)

        return output[:signal_length]
    
    def distort(self, x)->np.ndarray:
        if x.ndim < 2:
            output = x + self._overlap_add(x)
        else:
            output = np.zeros((x.shape[0],x.shape[1]))
            for i in range(x.shape[1]):
                output [:,i] = x[:,i] + self._overlap_add(x[:,i])
                self._lfo.reset()
            return output
        return output
