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
It allows to compute several distance measures between monovariate/multivariate signals (in pandas DataFrame format).
"""

import numpy as np
import pandas as pd
from math import sqrt

''' Distance metrics for pandas DataFrames '''
def Minkowski(x,y, order):
    """
    It computes the Minkowski distance of order p (p cannot be less than 1).
        1. p = 1, Manhattan distance;
        2. p = 2, Euclidean distance; and 
        3. p = np.inf, Cebysev distance
    
    :param x:
        first input signal
    :type x: pd.DataFrame
    
    :param y:
        second input signal
    :type y: pd.DataFrame
    
    :param order:
        the order of the distance to be computed
    :type p1: int
    
    :returns: float 
            -- a pandas DataFrame with the p-order distance between the two signals
    """
    
    ' Raise error if parameters are not in the correct type '
    if not(isinstance(x, pd.DataFrame)) : raise TypeError("Requires x to be a pd.DataFrame")
    if not(isinstance(y, pd.DataFrame)) : raise TypeError("Requires y to be a pd.DataFrame")
    
    'Error if p1 and p2 have not the same size'
    if x.shape[1]!=y.shape[1] :
        raise ValueError("The two points have different size")

    ' Raise error if parameters do not respect input rules '
    if order < 0 : raise ValueError("Requires order to be a positive scalar greater than 0")

    if order!=np.inf:
       d=((x.subtract(y)**(1.0*order)).sum(axis=1))**(1.0/order)
    else:
       d=(x.subtract(y).abs()).max(axis=1)
        
    d=pd.DataFrame(d)
    return (d)


''' Distance metrics for distributions'''
def Mahalanobis(df1,df2):
    """
    It computes the Mahalanobis distance 
    
    :param df1:
        first input signal 
    :type df1: pd.DataFrame
    
    :param df2:
        second input signal
    :type df2: pd.DataFrame
    
    :returns: float
            -- distance between the two signals
    """
    if df1.shape[0]+df2.shape[0]-2 == 0 : raise ValueError("Divide by zero exception : signal1.size+signal2.size-2 = 0  ")


    n1=df1.shape[0]
    n2=df2.shape[0]
        
    if df1.shape[1] !=1:
        df1_cov=df1.cov().values
        df2_cov=df2.cov().values
    else:
        df1_cov=df1.var(axis=0).values
        df2_cov=df2.var(axis=0).values
       
    pooled_cov=((n1-1)*df1_cov+ (n2-1)*df2_cov)/(n1+n2-2)
        
    if df1.shape[1] !=1:
        inv_pooled_cov=np.linalg.inv(pooled_cov)
               
    diff_mxy=df1.mean(axis=0).values-df2.mean(axis=0).values
    
    if df1.shape[1] !=1:
        D2=np.dot(np.dot(diff_mxy.T,inv_pooled_cov),diff_mxy)
    else:
        D2=np.absolute(diff_mxy)/pooled_cov
    
    return sqrt(D2)

