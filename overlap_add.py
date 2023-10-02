import numpy as np

def fftfilt(h:np.ndarray, x:np.ndarray, fft_length=-1)->:np.ndarray:
    """
    The classical overlap-add method for filtering a continuous stream of data

    Filter an input signal `x[n]` with a FIR filter specified by `h`.
    Unless specified, the FFT size is determined as the next higher power of 2 of twice the length of `b`.

    Parameters
    ----------
    h : The impulse response of the filter
    x : input signal

    Returns
    -------
    y : output signal
    """

    filter_length = h.shape[0]
    if fft_length < filter_length: # if no fft_length was specified, use the smallest power of 2 larger than the filter length
        fft_length = 2<<(filter_length-1).bit_length()
    window_length = fft_length - filter_length + 1
    signal_length = x.shape[0]
    offsets = range(0, signal_length, window_length)

    output = np.zeros(signal_length+fft_length)

    frequency_response = np.fft.rfft(h, n=fft_length)

    # overlap and add
    for n in offsets:
        output[n:n+fft_length] += np.fft.irfft(np.fft.rfft(x[n:n+window_length], n=fft_length)*frequency_response)

    return output[:signal_length]