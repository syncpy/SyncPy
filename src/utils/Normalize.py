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

def Normalize(signal, min_value = [0], max_value = [1]):
    """
    It normalizes function normalizes signal between min_value and max_value.
    If the signal is constant, the normalization converts it into the max_value.
    
    :param signal:
        input signal
    :type signal: pd.DataFrame
    
    :param min_value:
        minimal value desired. Default: [0]
    :type min_value: array
    
    :param max_value:
        maximal value desired. Default: [1]
    :type max_value: array
    
    :returns: pd.DataFrame 
            -- normalized signal
    """
    
    norm_data = signal.copy()
    
    # If an int is given, convert it in a sigleton
    if (isinstance(min_value, int)):
        min_value = [min_value]
    if (isinstance(max_value, int)):
        max_value = [max_value]
     
    # If only a singleton is given, normalize all columns with this value
    if(len(min_value) == 1):
        min_value = min_value * len(signal.columns)
    else:
        if(len(min_value) != len(signal.columns)):
            print('Normalize() error : min_value must be singleton or having same length as the input signal')
            return norm_data
    if(len(max_value) == 1):
        max_value = max_value * len(signal.columns)
    else:
        if(len(max_value) != len(signal.columns)):
            print('Normalize() error : max_value must be singleton or having same length as the input signal')
            return norm_data
    
    k = 0 
    for col in signal.columns :
        col_scope = signal[col].max() - signal[col].min()
        
        if 0 != col_scope: 
            col_min = signal[col].min()
            norm_data[col] = ((signal[col] - col_min) / col_scope ) * (max_value[k] - min_value[k]) + min_value[k]
        else:
            norm_data[col] = max_value[k]
        
        k += 1
        
    return norm_data
