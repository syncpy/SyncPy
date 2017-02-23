### This file is a part of the Syncpy library.
### Copyright 2015, ISIR / Universite Pierre et Marie Curie (UPMC)
### Main contributor(s): Giovanna Varni, Marie Avril,
### syncpy@isir.upmc.fr
### 
### This software is a computer program whose for investigating
### synchrony in a fast and exhaustive way. 
### 
### This software is governed by the CeCILL-B license under French law
### and abiding by the rules of distribution of free software.  You
### can use, modify and/ or redistribute the software under the terms
### of the CeCILL-B license as circulated by CEA, CNRS and INRIA at the
### following URL "http://www.cecill.info".

### As a counterpart to the access to the source code and rights to
### copy, modify and redistribute granted by the license, users are
### provided only with a limited warranty and the software's author,
### the holder of the economic rights, and the successive licensors
### have only limited liability.
### 
### In this respect, the user's attention is drawn to the risks
### associated with loading, using, modifying and/or developing or
### reproducing the software by the user in light of its specific
### status of free software, that may mean that it is complicated to
### manipulate, and that also therefore means that it is reserved for
### developers and experienced professionals having in-depth computer
### knowledge. Users are therefore encouraged to load and test the
### software's suitability as regards their requirements in conditions
### enabling the security of their systems and/or data to be ensured
### and, more generally, to use and operate it in the same conditions
### as regards security.
### 
### The fact that you are presently reading this means that you have
### had knowledge of the CeCILL-B license and that you accept its terms.

"""
.. moduleauthor:: Giovanna Varni
"""
import sys
sys.path.insert(0, '../src/')


import numpy as np # For math operation
import pandas as pd # For DataFrame 
import matplotlib.pyplot as plt # For plotting
import matplotlib.dates as mdates # For plotting dates and timeFormat
from Methods.utils import JointRecurrencePlot

from Method import Method, MethodArgList

class GSI(Method):
    """
    It computes the generalised synchronization index (GSI) between two uni/multi-variate signals x and y(in DataFrame format).
    GSI ranges in [0,1] where 0 means no synchronization and 1 perfect generalized synchronization.
    
    :param m:
        embedding dimension
    :type m: int
    
    :param t:
        embedding delay
    :type t: int
    
    :param rr:
        recurrence rate
    :type t: float
    
    """
    argsList = MethodArgList()
    argsList.append('m', 1, int, 'embedding dimension')
    argsList.append('t', 1, int, 'embedding delay')
    argsList.append('rr', 0.1, float, 'recurrence rate')

    ''' Constructor '''
    def __init__(self, m, t, rr, **kwargs):
        ' Raise error if parameters are not in the correct type '
        super(GSI, self).__init__(plot=False, **kwargs)
        #In the constructor we can check that params have corrects values and initialize stuff
        ' Raise error if parameters are not in the correct type '
        if not(isinstance(m, int))   : raise TypeError("Requires m to be an integer")
        if not(isinstance(t, int))   : raise TypeError("Requires t to be a integer")
        if not(isinstance(rr, float)): raise TypeError("Requires rr to be a float")
        
        ' Raise error if parameters do not respect input rules '
        if m <= 0 : raise ValueError("Requires m to be positive and greater than 0")
        if t <= 0 : raise ValueError("Requires t to be positive and  greater from 0")
        if rr <= 0: raise ValueError("Requires eps to be positive")

        self._m = m
        self._t = t 
        self._rr = rr
        
        return

    def compute(self, signals):
        """
        It computes GSI
         
        :param signals:
            array of two input signals as pd.DataFrame
        :type signals: list
        
        :returns: dict
            -- gsi 
        """
        x = signals[0]
        y = signals[1]


        ' Raise error if parameters are not in the correct type '
        if not(isinstance(x, pd.DataFrame)): raise TypeError("Requires x to be a pd.DataFrame")
        if not(isinstance(y, pd.DataFrame)): raise TypeError("Requires y to be a pd.DataFrame")

        standardization = True
        plot = False
        
        jrp = JointRecurrencePlot.JointRecurrencePlot(x, y, self._m, self._t, self._rr, 'rr', standardization, plot)
        
        f_jrp = (1 - jrp['jrp']).flatten()
        
        jrr = np.mean(f_jrp)
        
        GSI_no_norm = jrr / self._rr
                
        GSI = (GSI_no_norm - self._rr) / (1 - self._rr)
        
        if GSI > 1:
            GSI = 1
           
        result = dict()
        result['GSI'] = GSI

        return result


    @staticmethod
    def getArguments():
        return GSI.argsList.getMethodArgs()


    @staticmethod
    def getArgumentsAsDictionary():
        return GSI.argsList.getArgumentsAsDictionary()
