# Coursera Project - Class Integration

import numpy as np
import math

class Integrator:
    def __init__(self, xMin, xMax, N):
        self.xMin = xMin
        self.xMax = xMax
        self.N = N
    
            
    def integrate(self):
        S = 0
        for i in range(0, self.N - 1):
            del_x = (self.xMax - self.xMin)/float((self.N-1))
            x_i = self.xMin + (i*del_x)
            S = S + (x_i**2)*(np.exp(-x_i))*(np.sin(x_i))

        self.result = S
        
    def show(self):
        print ("Printout of value ", self.result)

        

examp = Integrator(1,3,200)
examp.integrate()
examp.show()
