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

def ResampleAndInterpolate(signal, rule='100ms', limit=None):
    """
    It resamples signal and does linear interpolation to values added by the resampling.
    Signal must have DateTime index. 
    
    :param signal:
        monovariate signal
    :type signal: pd.DataFrame
    
    :param rule:
        string with the resampling rule (ex: for 100ms resampling, rule='100ms'). Default: '100ms'
    :type rule: str
    :param limit:
        for interpolation, maximum number of consecutive NaN values to fill. Default: None
    :type limit: int
    
    :returns: pd.DataFrame
        -- resampled signal with linear interpolation of added data
    """

    if(type(signal.index[0]) != pd.tslib.Timestamp):
        print('ERROR : signal must have DateTime type index')
        return pd.DataFrame()
    
    signal = signal.resample(rule=rule)
    signal.interpolate(limit=limit, inplace = True)

    #convert back the time series in dataFrame 
    out = pd.DataFrame(signal.values, signal.index)
    
    return out
