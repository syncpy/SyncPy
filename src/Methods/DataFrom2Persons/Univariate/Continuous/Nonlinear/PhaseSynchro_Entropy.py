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


class PhaseSynchro_Entropy(Method):
    """
    It computes n:m synchronization index rho_nm by using a Shannon entropy based approach between two univariate signals x and y
    (in pandas DataFrame format). Rho_nm ranges in [0,1] where 0 means no synchronization at all and 1 means perfect synchronization.
   
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
        1. 'auto':the number of bins will be automatically estimated
        2. 'man': the number of bins (nbins) will take the value expressed in nbins parameter
    :type nbins_mode: str
    
    :param nbins:
        it is the number of bins to be used to build phase distribution
    :type nbins: int
    
    :param dist_cyc_rel_phase:
        if True the plot of the distribution of the cyclic relative phase is returned. Default: False
    :type dist_cyc_rel_phase: bool

    """
    argsList = MethodArgList()
    argsList.append('n', 1, int, 'it is the integer for the order of synchronization')
    argsList.append('m', 1, int, 'it is the integer for the order of synchronization ')
    argsList.append('nbins_mode', ['auto','man'], list, 'the number of bins (nbins) will be either automatically computed or specified by "nbin" paramater')
    argsList.append('nbins', 10, int, 'it is the number of bins to be used to build phase distribution')
    argsList.append('plot', False, bool, 'True the plot of Q and q is returned when atype is set to tsl or asl')

    ''' Constructor '''
    def __init__(self, n=1, m=1, nbins_mode='auto', nbins=10, plot=False, **kwargs):
        super(PhaseSynchro_Entropy, self).__init__(plot,**kwargs)
        ' Raise error if parameters are not in the correct type '
        try :
            if not(isinstance(n, int)) : raise TypeError("Requires n to be a np.array of integers") 
            if not(isinstance(m, int))   : raise TypeError("Requires m to be a np.array of integers")
            if not (isinstance(nbins_mode, str)) : raise TypeError("Requires nbins_mode to be a string")
            if not(isinstance(nbins, int))      : raise TypeError("Requires nbins to be an integer")
        except TypeError as err_msg:
            raise TypeError(err_msg)
            return
        
        ' Raise error if parameters do not respect input rules '
        try : 
            if n <= 0 : raise ValueError("Requires n to have a size greater than 0")
            if m <= 0 : raise ValueError("Requires n to have a size greater than 0")
            if nbins_mode!='auto' and nbins_mode!='man' : raise ValueError("Requires nbins_mode to be a 'auto' or 'man'")
            if nbins <= 0 : raise ValueError("Requires nbins to be a positive scalar")
            
        except ValueError as err_msg:
            raise ValueError(err_msg)
            return
    
        self._n = n
        self._m = m
        self._nbins_mode = nbins_mode
        self._nbins = nbins

        self.dist_psi_nm_hist = None
        self.dist_psi_nm_bins = None
            
        return 
    
    
    def plot_result(self):
        """
        It plots the distribution of the cyclic relative phase.
        
        :returns: plt.figure 
         -- figure plot
        """
        dist_psi_nm_hist = self.dist_psi_nm_hist
        dist_psi_nm_bins = self.dist_psi_nm_bins

        figure = plt.figure()
        plt.title('Distribtuion of cyclic relative phase')
        plt.xlabel('Bins')
        plt.ylabel('Number of values')
        width = 0.7 * (dist_psi_nm_bins[1] - dist_psi_nm_bins[0])
        center = (dist_psi_nm_bins[:-1] + dist_psi_nm_bins[1:]) / 2
        plt.bar(center,  dist_psi_nm_hist, align='center', width=width)
        plt.show()
        
        return figure
        
    
    def compute(self, signals):
        """
        It computes the synchronization index lambda_nm
         
        :param signals:
            array containing the 2 signals as pd.DataFrame
        :type signals: list
      
        :returns: dict
            -- rho_mn index
        """
        try:
            if not (isinstance(signals, list)): raise TypeError("Requires signals be an array")
            if len(signals) != 2: raise TypeError("Requires signals be an array of two elements")
        except TypeError as err_msg:
            raise TypeError(err_msg)

        x = signals[0]
        y = signals[1]
        
        ' Raise error if parameters are not in the correct type '
        try :
            if not(isinstance(x, pd.DataFrame)) : raise TypeError("Requires x to be a pd.DataFrame")
            if not(isinstance(y, pd.DataFrame)) : raise TypeError("Requires y to be a pd.DataFrame")
        except TypeError as err_msg:
            raise TypeError(err_msg)
            return
        
        
        'Error if x and y are empty or they have a different length'
        try :
            if (x.shape[0]==0) or (y.shape[0]== 0) : raise ValueError("Empty signal")
            if x.shape[0]!=y.shape[0] : raise ValueError("The two signals have different length")
        except ValueError as err_msg:
            raise ValueError(err_msg)
            return
    
        M = x.shape[0]

        if self._nbins_mode=='auto':
            self._nbins = np.round(np.exp(0.626 + 0.4 * np.log(M - 1)))

        #computing the analytic signal and the instantaneous phase
        x_analytic=hilbert(np.hstack(x.values))
        y_analytic=hilbert(np.hstack(y.values))
        
        phx=np.unwrap(scipy.angle(x_analytic))
        phy=np.unwrap(scipy.angle(y_analytic))

        disc_perc = int(np.floor(phx.shape[0] // 10))
        
        phx_s=phx[disc_perc-1:M-disc_perc]
        phy_s=phy[disc_perc-1:M-disc_perc]

        bins_no = self._nbins
        
        ph_nm = (self._n*phx_s-self._m*phy_s)
        psi_nm = np.mod(np.abs(ph_nm), 2 * np.pi)

        dist_psi_nm_hist, dist_psi_nm_bins = np.histogram(psi_nm, bins=bins_no, range=(-(np.pi / (bins_no - 1)), 2 * np.pi + (np.pi / (bins_no - 1))))

        self.dist_psi_nm_hist = dist_psi_nm_hist
        self.dist_psi_nm_bins = dist_psi_nm_bins

        if psi_nm.shape[0] == 0:
            raise ValueError("Requires psi_nm.size not to be 0")
            return

        dist_psi_nm_rel = dist_psi_nm_hist/(1.0*psi_nm.shape[0])

        self.plot()

        S_terms = np.array([([_ * np.log(_) for _ in dist_psi_nm_rel])])

        S = -np.sum(S_terms[~np.isnan(S_terms)])

        S_max = np.log(bins_no)

        if S_max == 0:
            raise ValueError("Requires S_max not to be 0")
            return

        rho_nm = (S_max-S)/S_max
        
        self.res = dict()
        self.res['rho_nm'] = rho_nm

        return self.res

    @staticmethod
    def getArguments():
        return PhaseSynchro_Entropy.argsList.getMethodArgs()


    @staticmethod
    def getArgumentsAsDictionary():
        return PhaseSynchro_Entropy.argsList.getArgumentsAsDictionary()

