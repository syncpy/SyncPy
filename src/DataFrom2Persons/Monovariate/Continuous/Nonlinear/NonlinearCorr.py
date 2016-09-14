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

import numpy as np
import pandas as pd

from utils import Detrend


class NonlinearCorr:
    """
    It computes the nonparametric nonlinear regression coefficient h2 describing the dependency between two signals x and y (in pandas DataFrame format) in the most general way.
    It is equal to 0 when the two signals are independent, 1 when they are perfectly dependent.
    
    **Reference :**
    
    * F.Lopes da Silva, P. J.P., and B.P. Interdependence of eeg signals: linear vs. nonlinear associations and the signifcance of time delays and phase shifts. BrainTopography,2:9-18, 1989.
    
    :param nbins:
        number of bins in which the time series is divided into. 
    :type nbins: int
    """
 
    ''' Constuctor '''
    def __init__(self, nbins):
        ' Raise error if parameters are not in the correct type '
        try :
            if not(isinstance(nbins, int)) : raise TypeError("Requires tau_max to be an integer")
        except TypeError, err_msg:
            raise TypeError(err_msg)
            return
        
        ' Raise error if parameters do not respect input rules '
        try : 
            if nbins <= 0 : raise ValueError("Requires nbins to be a positive integer different from 0")
        except ValueError, err_msg:
            raise ValueError(err_msg)
            return
        
        self.nbins=nbins
            

    def compute(self,x,y):
        """
        It computes the nonlinear correlation coefficient h2.
        
        :param x:
            first input signal
        :type x: pd.DataFrame
        
        :param y:
            second input signal
        :type y: pd.DataFrame
        
        :returns: dict
            -- nonlinear coefficient h2        
        """
        
        ' Raise error if parameters are not in the correct type '
        try :
            if not(isinstance(x, pd.DataFrame)) : raise TypeError("Requires x to be a pd.DataFrame")
            if not(isinstance(y, pd.DataFrame)) : raise TypeError("Requires y to be a pd.DataFrame")
        except TypeError, err_msg:
            raise TypeError(err_msg)
            return
        
        xbincenters=np.array([])
        ybin=np.array([])
        
        x=Detrend.Detrend(x,det_type='mean')
        y=Detrend.Detrend(y,det_type='mean')
                
        ll=x.min(axis=0).values
        ul=x.max(axis=0). values
                
        xi=np.linspace(ll,ul,num=self.nbins)
        
        for j in range(1,xi.size):
            px=(x.iloc[:,0].values>=xi[j-1]) & (x.iloc[:,0].values<xi[j])
            #px=np.hstack(px)
            
            if not px.size:
                continue
            
            xb=x.iloc[px].values
            yb=y.iloc[px].values
            
            xbincenters=np.append(xbincenters,np.mean(xb))
            ybin=np.append(ybin,np.mean(yb))
        
        yinterp=np.hstack(np.interp(x,xbincenters,ybin))
        
        h2 = (np.sum(y.iloc[:,0].values**2)-np.sum((y.iloc[:,0].values-yinterp)**2))/np.sum(y.iloc[:,0].values**2)
        
        h2_res={'h2 coefficient': h2}
        
        return h2_res
            
    
    
    
    
    
    
    
    
    
    