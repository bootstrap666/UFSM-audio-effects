'''Abramowitz and Stegun error function approximations 7.1.25-28'''
import numpy as np

def erf1(x:float)->float:
    ''' Approximation 1, max error 5E-4 '''
    return (1.0 - 1.0/np.power((np.polyval([0.078108, 0.000972, 0.230389, 0.278393, 1],abs(x))),4))*np.sign(x)

def erf2(x: float)->float:
    ''' Approximation 2, max error 2.5E-5 '''
    t = 1.0/(1.0+0.47047*abs(x))
    return (1.0 - (np.polyval([0.7478556, -0.0958798, 0.3480242, 0], t))*np.exp(-(x**2)))*np.sign(x)

def erf3(x: float)->float:
    ''' Approximation 3, max error 3E-7 '''
    return (1.0 - 1.0/np.power(np.polyval([0.0000430638, 0.0002765672, 0.0001520143, 0.0092705272, 0.0422820123, 0.0705230784, 1], abs(x)),16))*np.sign(x) 
     
def erf4(x: float)->float:
    ''' Approximation 4, max error 1.5E-7 '''
    t = 1.0/(1.0+0.3275911*abs(x))
    return (1.0 - (np.polyval([1.061405429, -1.453152027, 1.421413741, -0.284496736, 0.254829592, 0], t))*np.exp(-(x**2)))*np.sign(x)
          