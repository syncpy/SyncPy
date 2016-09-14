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
import matplotlib.pyplot as plt
import itertools

import CrossRecurrencePlot


def Crqa_diag(x,y,m,t,e,distance,standardization,window_size,lmin):
    """
    It computes the following diagonalwise (cross) recurrence measures from the (cross)recurrence plot of two uni/multi-variate signals x and y
    (in pandas DataFrame format): Recurrence Rate (RR), Determinism (DET), Average Diagonal Line Length (L).
    
    **Reference :**
    
    * N. Marwan, M. Carmen Romano, M. Thiel and J. Kurths. "Recurrence plots for the analysis of complex systems". Physics Reports 438(5), 2007.
    
    :param x:
        first input signal
    :type x: pd.DataFrame
    
    :param y:
        second input signal
    :type y: pd.DataFrame
    
    :param m:
        embedding dimension
    :type m: int
    
    :param t:
       embedding delay
    :type t: int
    
    :param eps:
        threshold for recurrence
    :type eps: float    
    
    :param distance:
        It specifies which distance method is used. It can assumes the following values:\n
        1. 'euclidean';
        2. 'maximum';
        3. 'manhattan'
        
    :type distance: str
    
    :param standardization:
       if True data are nomalize to zero mean and unitary variance
    :type standardization: bool
    
    :param window_size:
        it is the size of the window around the main diagonal over which the measures will be computed
    :type window_size: int
    
    :param lmin:
        it is the minimum value of the diagonal length line will be used when measures will be computed
    :type lmin: int     
      
    """
    
    ' Raise error if parameters are not in the correct type '
    try :
        if not(isinstance(x, pd.DataFrame)) : raise TypeError("Requires x to be a pd.DataFrame")
        if not(isinstance(y, pd.DataFrame)) : raise TypeError("Requires y to be a pd.DataFrame")
        if not(isinstance(m, int)) : raise TypeError("Requires m to be an integer")
        if not(isinstance(t, int)) : raise TypeError("Requires t to be an integer")
        if not(isinstance(e, float)): raise TypeError("requires eps to be a float")
        if not(isinstance(distance, str)) : raise TypeError("Requires distance to be a string")
        if not(isinstance(standardization, bool)) : raise TypeError("Requires standardization to be a bool")
        if not(isinstance(window_size, int)) : raise TypeError("Requires window_size to be an integer")
        if not(isinstance(lmin, int)) : raise TypeError("Requires lmin to be an integer")
    except TypeError, err_msg:
        raise TypeError(err_msg)
        return

    ' Raise error if parameters do not respect input rules '
    try :
        
        if m <= 0 : raise ValueError("Requires m to be positive and greater than 0") 
        if t <= 0 : raise ValueError("Requires t to be positive and  greater from 0") 
        if e <0: raise ValueError("Requires eps to be positive")
        if distance != 'euclidean' and distance != 'maximum' and distance !='manhattan': raise ValueError("Requires a valid way to compute distance")
        if window_size<= 0 or window_size>x.shape[0]: raise ValueError("Requires window_size to be positive and greater than 0 and lesser than the length of the input signals")
        if lmin <=0 or lmin > x.shape[0]: raise ValueError("Requires lmin to be positive and greater than 0 and lesser than the length of the input signal")  
        if x.shape[0]!=y.shape[0]: raise ValueError("Requires data to have the same length")
    except ValueError, err_msg:
        raise ValueError(err_msg)
        return
    
    'Error if x and y have not the same size'
    try :
        if x.shape[0]!=y.shape[0] :
            raise ValueError("The two signals have different length")
    except ValueError, err_msg:
        raise ValueError(err_msg)
        return
    
     
    plot=False

    thw=0
    w=window_size
    
    
    result=dict()

    c=CrossRecurrencePlot.CrossRecurrencePlot(x,y,m,t,e,distance,standardization,plot)
    
    crp_m=1-c['crp'].copy()
    
    RR_tau=np.array([])
    L_tau=np.array([])
    DET_tau=np.array([])
    
    tau_vect=np.arange(-w,w+1)
    

    for tau in tau_vect:
        #print tau
        hist_P_tau=np.zeros([1,crp_m.shape[0]])[0]
        
        diag_line=np.diagonal(crp_m,offset=tau)
        length_diag_line=np.array(length_ones_seq(diag_line))
            
        if (not length_diag_line.size) or (length_ones_seq(length_diag_line)<lmin).all(): 
            pass
                                
        indices_diag_line=np.hstack(np.where(length_diag_line >=lmin))

        for i in range(0,indices_diag_line.size):
            hist_P_tau[length_diag_line[indices_diag_line[i]]-1]=hist_P_tau[length_diag_line[indices_diag_line[i]]-1]+1

        try :
            if crp_m.shape[0]-np.abs(tau) == 0 : raise ValueError("Divide by zero exception : RR_tau_i ")
        except ValueError, err_msg:
            raise ValueError(err_msg)
            return

        RR_tau_i = (1.0/(crp_m.shape[0]-np.abs(tau)))*(sum(np.arange(lmin,crp_m.shape[0]-np.abs(tau))*hist_P_tau[lmin:crp_m.shape[0]-np.abs(tau)]))
        
        if np.isnan(RR_tau_i):
            RR_tau_i=0
        
        RR_tau=np.append(RR_tau,RR_tau_i)
        
        L_tau_N = 1.0*(np.sum(np.arange(lmin,crp_m.shape[0]+1-np.abs(tau))*hist_P_tau[lmin-1:crp_m.shape[0]-np.abs(tau)]))
        L_tau_D = sum(hist_P_tau[lmin-1:(crp_m.shape[0]-np.abs(tau))])

        try :
            if np.any(L_tau_D == 0) : raise ValueError("Divide by zero exception : L_tau_D ")
        except ValueError, err_msg:
            raise ValueError(err_msg)
            return

        L_tau_i = L_tau_N / L_tau_D
        
        if np.isnan(L_tau_i):
            L_tau_i=0
        
        L_tau=np.append(L_tau,L_tau_i)
        
        DET_tau_N = L_tau_N
        DET_tau_D = RR_tau_i*(crp_m.shape[0]-np.abs(tau))

        try :
            if DET_tau_D == 0 : raise ValueError("Divide by zero exception : DET_tau_D ")
        except ValueError, err_msg:
            raise ValueError(err_msg)
            return
        
        DET_tau_i = DET_tau_N/DET_tau_D
        
        if DET_tau_i > 1:
           DET_tau_i=1
           
        elif np.isnan(DET_tau_i):
            DET_tau_i=0
        
        DET_tau=np.append(DET_tau,DET_tau_i)
           
    result['tau']=tau_vect
    result['RR']= RR_tau
    result['L']= L_tau
    result['DET']= DET_tau

    return result

    
    

def length_ones_seq(diag_line):
    """
    It computes the length of a sequence of ones
    """
    return np.array([sum(g) for b, g in itertools.groupby(diag_line) if b])


