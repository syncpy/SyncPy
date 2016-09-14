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
.. moduleauthor:: Marie Avril
"""

import numpy as np # For math operation
import pandas as pd # For DataFrame 
import matplotlib.pyplot as plt # For plotting
import matplotlib.dates as mdates # For plotting dates and timeFormat
from numpy.linalg import inv #for inversing a matrix

#Import Welch module for computing spectrum
from utils import Welch_psd
from utils import Cpsd

class PartialCoherence:
    """
    It computes the partial coherence in a list of signals, 3 signals at a time.
    
    **Reference :**
    
    * Pereda, E. and al., Nonlinear multivariate analysis of neurophysiological signals. Progress in Neurobiology 77 (2005) I-37.
    
  :param fs:
    sampling frequency (in Hz) of the input signal. Default: 1.0
  :type fs: float
  
  :param NFFT:
    length of each epoch (in samples). Default: 256
  :type NFFT: int
  
  :param detrend:
    it specifies which kind of detrending should be computed on data. Ranges in [0;1]:
        1. 0 constant detrending;
        2. 1 linear detrending.
    Default: 0
  :type detrend: int
  
  :param noverlap:
    number of samples to overlap between epochs. Default: 0
  :type noverlap: int
    """

    ''' Constructor '''
    def __init__(self, fs=1.0, NFFT=256, detrend=0, noverlap=0):
        
        #In the constructor we can check that params have corrects values and initialize stuff
        
        ' Raise error if parameters are not in the correct type '
        try :
          if not(isinstance(fs, float))     : raise TypeError("Requires fs to be an float")
          if not(isinstance(NFFT, int))     : raise TypeError("Requires NFFT to be an integer")
          if not(isinstance(detrend, int))  : raise TypeError("Requires detrend to be an integer")
          if not(isinstance(noverlap, int)) : raise TypeError("Requires noverlap to be an integer")
        except TypeError, err_msg:
          raise TypeError(err_msg)
          return
        
        ' Raise error if parameters do not respect input rules '
        try :     
            if fs < 0 :           raise ValueError("Requires fs to be a positive scalar")
            if NFFT <=0:          raise ValueError("Requires NFFT to be a strictly positive scalar")
            if NFFT %2 != 0:      raise ValueError("Requires NNFT to be a multiple of 2")
            if detrend != 0  and detrend != 1 and detrend != 2 : raise ValueError("Requires detrend to be 0, 1 or 2" )
        except ValueError, err_msg:
          raise ValueError(err_msg)
          return
              
        self.fs=fs
        self.NFFT=NFFT
        self.detrend=detrend
        self.noverlap=noverlap
        
        return

        
    def compute_partial_cross_spectrum(self, X, Y, Z):
        """
         It computes partial cross-spectrum between X and Y given all the linear information of Z 
         
        :param X:
            first signal
        :type X: pd.DataFrame
        
        :param Y:
            second signal
        :type Y: pd.DataFrame
        
        :param Z:
            third signal
        :type Z: pd.DataFrame
      
        :returns: np.array
            -- partial cross-spectrum 
        """

        S_zz = Welch_psd.Welch_psd(Z,self.fs, self.NFFT,self.detrend,self.noverlap,False)['psd']
        
        S_xy = Cpsd.Cpsd(X,Y,self.fs, self.NFFT,self.detrend,self.noverlap,False)['psd']
        S_xz = Cpsd.Cpsd(X,Z,self.fs, self.NFFT,self.detrend,self.noverlap,False)['psd']
        S_yz = Cpsd.Cpsd(Y,Z,self.fs, self.NFFT,self.detrend,self.noverlap,False)['psd']

        S_xy_z = S_xy - S_xz*S_zz* S_yz

        return S_xy_z
    
    
    def compute(self, *signals):
        """
         It computes the partial coherence between each signals. 
         
        :param signals:
            list of signals, one per person. 
        :type signals: list[pd.DataFrame]
      
        :returns: dict
            -- partial coherence between each signal, organized in a dict:
            {z : {(x,y): K_xy_z}} with K_xy_z the partial coherence betwen signals[x] and signals[y] given all the linear informaiton of signals[z]
        """
        
        ' Raise error if parameters are not in the correct type '
        try :
            for i in range(len(signals)) :
                if not(isinstance(signals[i], pd.DataFrame)): raise TypeError("Requires signal " + str(i+1) + " to be a pd.DataFrame.")
        except TypeError, err_msg:
            raise TypeError(err_msg)
            return
        
        ' Raise error if DataFrames have not the same size or same indexes '
        try :
            for i in range(0,len(signals)):
                if len(signals[0]) != len(signals[i]) : raise ValueError("All the signals must have the same size. Signal " + str(i+1) + " does not have the same size as first signal.")
                if signals[0].index.tolist() != signals[i].index.tolist() : raise ValueError("All the signals must have the same time indexes. Signal " + str(i+1) + " does not have the same time index as first signal.")
        except ValueError, err_msg:
            raise ValueError(err_msg)
            return
        
        N = len(signals) #number of signals
        
        self.partial_coherence = {}
        for z in range(N): # for the third signal Z
            
            K_xy = {}
            for x in range(N): # for the first signal X

                for y in range(N): # For the second signal Y
                    if x != y and x!= z and y!=z : # Compute K(XY|Z)
                        X = signals[x]
                        Y = signals[y]
                        Z = signals[z]
                        
                        S_xy_z = self.compute_partial_cross_spectrum(X, Y, Z)
                        S_xx_z = self.compute_partial_cross_spectrum(X, X, Z)
                        S_yy_z = self.compute_partial_cross_spectrum(Y, Y, Z)
                        
                        K_xy_z = np.divide(S_xy_z, S_xy_z**2, S_xx_z* S_yy_z)

                        K_xy.update({(x,y) : K_xy_z})
            
            self.partial_coherence.update({z : K_xy})

        return self.partial_coherence 
        

            
        
        
        