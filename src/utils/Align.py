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

def Align(signal_1, signal_2, how='inner'):
    """
    It aligns two monovariate signals (in pandas DataFrame format) according to their times indexes
    
    :param signal_1:
        first monovariate signal
    :type signal_1: pd.DataFrame
    
    :param  signal_2:
        second monovariate signal
    :type signal_2: pd.DataFrame
    
    :param how:
        {'left', 'right', 'outer', 'inner'}
        How to handle indexes of the two objects for joining on index, None otherwise. Default: 'inner'.\n

        -- left: use calling frame's index \n
        -- right: use input frame's index\n
        -- outer: form union of indexes\n
        -- inner: use intersection of indexes
    :type how: str
    
    :returns: pd.DataFrame
            -- first aligned signal
    :returns: pd.DataFrame
            -- second aligned signal
    """

    aligned_data = pd.DataFrame()
    aligned_data = signal_1.join(signal_2, how = how, lsuffix ='_1', rsuffix='_2')
    
    #convert back the time series in dataFrame 
    out_1 = pd.DataFrame(aligned_data.iloc[:,0], aligned_data.index)
    out_2 = pd.DataFrame(aligned_data.iloc[:,1], aligned_data.index)
        
    return out_1, out_2
