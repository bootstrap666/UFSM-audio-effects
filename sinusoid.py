import numpy as np

class Sinusoid:
    def __init__(self, frequency:float):
        self._state = np.zeros(2)
        self._b = np.array([0, np.sin(2*np.pi*frequency), -np.sin(2*np.pi*frequency)])
        self._a = np.array([1, -2*np.cos(2*np.pi*frequency), 1])

    def step(self,input:float)->float:
        y = self._state[1]
        self._state[1] = self._state[0] + input*self._b[1] - y *self._a[1]
        self._state[0] = input*self._b[2] - y*self._a[2]
        return y
    
    def reset(self):
        self._state[1] = 0
        self._state[0] = 0

    def steps(self,input:float, nsteps:int):
        for i in range(nsteps):
            self.step(input)