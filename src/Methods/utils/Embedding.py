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

def Embedding(x,m,t):
    """
    It embeds the input signal x by using a dimension equal to m and
    a delay between data equal to t.
    
    :param x:
        first input signal    
    :type x: pd.DataFrame
    
    :param m:
        the embedding dimension
    :type m: int
    
    :param t:
        the embedding delay expressed in samples
    :type t: int
    
    :return: pd.DataFrame
        -- the embedded DataFrame
    
    """
    
    ' Raise error if parameters are not in the correct type '
    try :
        if not(isinstance(x, pd.DataFrame)) : raise TypeError("Requires x to be a pd.DataFrame")
    except TypeError as err_msg:
            raise TypeError(err_msg)
            return
    try : 
        if m <= 0 : raise ValueError("Requires m to be positive and greater than 0") 
        if t <= 0 : raise ValueError("Requires t to be positive and  greater from 0")
    except ValueError as err_msg:
            raise ValueError(err_msg)
            return    
    
    ' Raise error if m and t are too big to do embedding '
    try:
        if ((x.shape[0]-t*(m-1)) < 1):
               raise ValueError("m or t values are too big")
    except ValueError as err_msg:
        raise ValueError(err_msg)
        return
    
    x_=pd.DataFrame()
    x_emb=pd.DataFrame()
    

    for i in range(0,x.shape[0]):
        if i-(m-1)*t < 0:
            continue
        x_i=x.ix[i-(m-1)*t:i:t]
        x_i=x_i.reset_index().drop('index',axis=1)
        x_=pd.concat([x_, x_i], axis=1)
        x_T=x_.T
        x_emb=x_T.reset_index(drop=True)
       
    return (x_emb)