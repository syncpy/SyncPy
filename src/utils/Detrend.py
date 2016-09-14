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

import numpy as np
import pandas as pd

def Detrend(signal,det_type):
    """
    It removes constant or linear trending in a monoviarate/multivariate signal (in pandas DataFrame format).
    In case of multivariate signal, detrending is carried out on each column of the DataFrame
    
    :param signal:
        input signal
    :type signal: pd.DataFrame
    
    :param det_type:
        {'mean' 'linear'} 
    :type det_type: str
    
    :returns: pd.DataFrame 
            -- detrended signal
    """
    
    ' Raise error if parameters are not in the correct type '
    if not(isinstance(signal, pd.DataFrame)) : raise TypeError("Requires signal to be a pd.DataFrame")
    if not(isinstance(det_type, str))      : raise TypeError("Requires det_type to be a string")

    ' Raise error if parameters do not respect input rules '

    if det_type!='mean' and det_type!='linear' : raise ValueError("Requires det_type to be 'mean' or 'linear'")

    if det_type=='mean':
        signal_det=signal-signal.mean(axis=0)
    
    elif det_type=='linear':
        signal=signal.reset_index(drop=True)
        signal_det_tot=pd.DataFrame()
        
        x_signal=pd.Series(np.arange(0,signal.shape[0]))

        if x_signal.var(axis=0)==0 :
            raise ValueError("Linear detrending cannot be computed, a division for zero occurred")
    
        for k in range(0,signal.shape[1]):
            beta=x_signal.cov(signal.iloc[:,k])/x_signal.var(axis=0)
            alpha=signal.iloc[:,k].mean(axis=0)-beta*(x_signal.mean(axis=0))          
            
            signal_det=signal.iloc[:,k]-(alpha + beta*x_signal)
            signal_det_tot.loc[:,k]=signal_det
            signal_det=signal_det_tot
        
    return (signal_det)

