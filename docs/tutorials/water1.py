import sys
import math
from fluidframe import fluidframe

class fluid(fluidframe):
    def __init__(self):
        self._rhomass = 1000.
        self._molar_mass = 18.E-3
        self._viscosity = 1.31E-3
        self._adiabatic_compressibility=1./2.07E9 #4.7E-10
        self._isothermal_compressibility=1./2.07E9 #assumed same as adiabatic_compressibility
        # self._first_partial_deriv = self._isothermal_compressibility*self._rhomass
        self._cpmass=4184.
        self._cvmass=4183.9
        self._phase = 0
        self._Q = -1000.
        self._p = 1.E5
        self._conductivity = 0.6
        self._speed_sound = math.sqrt(1./(self._adiabatic_compressibility*self._rhomass))

    def update(self,input_pair,val1,val2):
        if input_pair == 9: #PT_INPUTS tag in CoolProp
            self._T = val2
            self._hmass = self._cpmass*self._T
        elif input_pair == 20: #HmassP_INPUTS tag in CoolProp
            self._T = val1/self._cpmass
            self._hmass = self._cpmass*self._T
        elif input_pair == 2: #PQ_INPUTS
            if (val2 >= 0. and val2 <= 1.):
                self._T = 100.+273.
                self._hmass = self._cpmass*self._T + val2*2.23E6
            else:
                print ("Q out of range. stopping",val2)
                sys.exit()
        else:
            print ("input_pair not recognized. stopping",input_pair)
            sys.exit()
