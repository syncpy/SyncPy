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

import numpy as np # For math operation
import pandas as pd # For DataFrame 
import matplotlib.pyplot as plt # For plotting
import matplotlib.dates as mdates # For plotting dates and timeFormat
import scipy
from scipy.signal import hilbert

from Method import Method, MethodArgList


class PhaseSynchro_Fourier(Method):
    """
    It computes n:m synchronization index gamma2_nm as the intensity of the first Fourier mode of the cyclic relative phase of two univariate signals x and y
    (in pandas DataFrame format). Gamma2_nm ranges in [0,1] where 0 means no synchronization at all and 1 means perfect synchronization.
   
    **Reference :**
    M. Rosenblum, A. Pikovsky, J. Kurths, C. Schafer and P. A. Tass. Phase synchronizatio:from theory to practice. In Handbook of Biological Physics,
    Elsiever Science, Series Editor A.J. Hoff, Vol. , Neuro-Informatics, Editors: F. Moss and S. Gielen, Chapter 9.
    
    :param n:
        it is the integer for the order of synchronization 
    :type n: int 
    
    :param m:
        it is the integer for the order of synchronization 
    :type m: int
    

    """
    argsList = MethodArgList()
    argsList.append('n', 1, int, 'it is the integer for the order of synchronization')
    argsList.append('m', 1, int, 'it is the integer for the order of synchronization ')

    ''' Constructor '''
    def __init__(self, n=1, m=1, **kwargs):
        super(PhaseSynchro_Fourier, self).__init__(plot=False, **kwargs)
        ' Raise error if parameters are not in the correct type '
        try :
            if not(isinstance(n, int)) : raise TypeError("Requires n to be an integer")
            if not(isinstance(m, int))   : raise TypeError("Requires m to be an integer")
        except TypeError, err_msg:
            raise TypeError(err_msg)
            return
        
        ' Raise error if parameters do not respect input rules '
        try : 
            if n <= 0 : raise ValueError("Requires n to have a size greater than 0")
            if m <= 0 : raise ValueError("Requires n to have a size greater than 0")            
        except ValueError, err_msg:
            raise ValueError(err_msg)
            return
    
        self._n = n
        self._m = m
            
        return 
    
    
    def compute(self, signals):
        """
        It computes the synchronization index lambda_nm
         
        :param signals:
            array containing the 2 signals as pd.DataFrame
        :type signals: list
        
      
        :returns: dict
            -- gamma2_mn index
        """
        try:
            if not (isinstance(signals, list)): raise TypeError("Requires signals be an array")
            if len(signals) != 2: raise TypeError("Requires signals be an array of two elements")
        except TypeError, err_msg:
            raise TypeError(err_msg)

        x = signals[0]
        y = signals[1]
        
        ' Raise error if parameters are not in the correct type '
        try :
            if not(isinstance(x, pd.DataFrame)) : raise TypeError("Requires x to be a pd.DataFrame")
            if not(isinstance(y, pd.DataFrame)) : raise TypeError("Requires y to be a pd.DataFrame")
        except TypeError, err_msg:
            raise TypeError(err_msg)
            return
        
        
        'Error if x and y are empty or they have a different length'
        try :
            if (x.shape[0]==0) or (y.shape[0]== 0) : raise ValueError("Empty signal")
            if x.shape[0]!=y.shape[0] : raise ValueError("The two signals have different length")
        except ValueError, err_msg:
            raise ValueError(err_msg)
            return
        
    
        M=x.shape[0]
                

        #computing the analytic signal and the instantaneous phase
        x_analytic=hilbert(np.hstack(x.values))
        y_analytic=hilbert(np.hstack(y.values))
        
        phx=np.unwrap(scipy.angle(x_analytic))
        phy=np.unwrap(scipy.angle(y_analytic))

        disc_perc = np.floor(phx.shape[0] / 10.0)
        
        phx_s=phx[disc_perc-1:M-disc_perc]
        phy_s=phy[disc_perc-1:M-disc_perc]
        
        ph_nm=(self._n*phx_s-self._m*phy_s)
        psi_nm=np.mod(ph_nm, 2*np.pi)

        gamma2_nm=np.square(np.mean(np.cos(psi_nm))) + np.square(np.mean(np.sin(psi_nm)))
        gamma_nm = np.sqrt(gamma2_nm)

        result = dict()
        result['gamma_nm'] = gamma_nm

        return result

    @staticmethod
    def getArguments():
        return PhaseSynchro_Fourier.argsList.getMethodArgs()


    @staticmethod
    def getArgumentsAsDictionary():
        return PhaseSynchro_Fourier.argsList.getArgumentsAsDictionary()