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


class PhaseSynchro_Strobo:
    """
    It computes n:m synchronization index lambda_nm by using a stroboscopic approach between two univariate signals x and y
    (in pandas DataFrame format).
   
    **Reference :**
    M. Rosenblum, A. Pikovsky, J. Kurths, C. Schafer and P. A. Tass. Phase synchronizatio:from theory to practice. In Handbook of Biological Physics,
    Elsiever Science, Series Editor A.J. Hoff, Vol. , Neuro-Informatics, Editors: F. Moss and S. Gielen, Chapter 9.
    
    :param n:
        it is the integer for the order of synchronization 
    :type n: int 
    
    :param m:
        it is the integer for the order of synchronization 
    :type m: int
    
    :param nbins_mode:
        It can be:
        1. 'auto':the number of bis  wil be automatically estimated
        2. 'man': the number of bins (nbins) will take the value expressed in nbins parameter
    :type nbins_mode: str
    
    :param nbins:
        it is the number of bins to be used to build phase distribution
    :type nbins: int

    """

    ''' Constructor '''
    def __init__(self, n=1, m=1, nbins_mode='auto', nbins=10):
        
        ' Raise error if parameters are not in the correct type '
        try :
            if not(isinstance(n, int)) : raise TypeError("Requires n to be a np.array of integers") 
            if not(isinstance(m, int))   : raise TypeError("Requires m to be a np.array of integers")
            if not (isinstance(nbins_mode, str)) : raise TypeError("Requires nbins_mode to be a string")
            if not(isinstance(nbins, int))      : raise TypeError("Requires nbins to be an integer")
        except TypeError, err_msg:
            raise TypeError(err_msg)
            return
        
        ' Raise error if parameters do not respect input rules '
        try : 
            if n <= 0 : raise ValueError("Requires n to have a size greater than 0")
            if m <= 0 : raise ValueError("Requires n to have a size greater than 0")
            if nbins_mode!='auto' and nbins_mode!='man' : raise ValueError("Requires nbins_mode to be a 'auto' or 'man'")
            if nbins <= 0 : raise ValueError("Requires nbins to be a positive scalar")
            
        except ValueError, err_msg:
            raise ValueError(err_msg)
            return
    
        self._n = n
        self._m = m
        self._nbins_mode = nbins_mode
        self._nbins = nbins
            
        return 
    
  
    def compute(self, x, y):
        """
        It computes the synchronization index lambda_nm
         
        :param x:
            first input signal
        :type x: pd.DataFrame
        
        :param y:
            second input signal
        :type y: pd.DataFrame
        
      
        :returns: dict
            -- lambda_mn index
        """
        
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
        

        if self._nbins_mode=='auto':
            self._nbins=np.exp(0.626+0.4*np.log(M-1))

        try:
            if self._nbins <= 0 : raise ValueError("Requires nbins to be a positive scalar")

        except ValueError, err_msg:
            raise ValueError(err_msg)
            return
        

        #computing the analytic signal and the instantaneous phase
        x_analytic=hilbert(np.hstack(x.values))
        y_analytic=hilbert(np.hstack(y.values))
        
        phx=np.unwrap(scipy.angle(x_analytic))
        phy=np.unwrap(scipy.angle(y_analytic))
    
         
        disc_perc=np.floor(x.shape[0]/10.0)    
        
        phx_s=phx[disc_perc-1:M-disc_perc]
        phy_s=phy[disc_perc-1:M-disc_perc]
         
        bins=np.linspace(0,2*np.pi*self._m,self._nbins)
        bins_no=bins.size

        try:
            if bins_no <= 0 : raise ValueError("Requires bins_no to be a positive scalar")

        except ValueError, err_msg:
            raise ValueError(err_msg)
            return
        
        Lambda=np.array([])
        
        #distribution of of the phase of the first signal
        for b in range(0,bins_no-1):
            lb=bins[b]
            ub=bins[b+1]

            mod_phx_s=np.mod(phx_s,2*np.pi*self._m)
           
            indices=np.where(np.all([mod_phx_s<=ub,mod_phx_s>=lb], axis=0))
            
            M=len(indices[0])
            
            eta=np.mod(phy_s[indices[0]], 2*np.pi*self._n)
            
            Lambda_=1.0*np.sum(np.exp(1j*(eta/self._n)))/M
            
            if np.isnan(Lambda_):
                Lambda_=0
            
            Lambda=np.append(Lambda,Lambda_)
        
        lambda_nm=1.0*(np.sum(np.abs(Lambda)))/bins_no 

        result = dict()
        result['lambda_nm'] = lambda_nm
        
        return result  
        

            
        
        
        