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


def Crqa(x,y,m,t,e,distance,standardization,window,window_size,step,lmin,thw):
    """
    It computes the following (cross)recurrence measures from the (cross)recurrence plot of two uni/multi-variate signals x and y
    (in pandas DataFrame format): Recurrence Rate (RR), Determinism (DET), Average Diagonal Line Length (L), Maximum Diagonal Line Length (L_max),
    Entropy (ENT).
    
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
    
    :param window:
        second input signal
    :type window: bool
    
    :param window_size:
        embedding dimension
    :type window_size: int
    
    :param step:
       embedding delay
    :type step: int
    
    :param lmin:
        threshold
    :type lmin: int    
    
    :param thw:
        distance method
    :type thw: int
    
    """
    
    ' Raise error if parameters are not in the correct type '
    if not(isinstance(x, pd.DataFrame)) : raise TypeError("Requires x to be a pd.DataFrame")
    if not(isinstance(y, pd.DataFrame)) : raise TypeError("Requires y to be a pd.DataFrame")
    if not(isinstance(m, int)) : raise TypeError("Requires m to be an integer")
    if not(isinstance(t, int)) : raise TypeError("Requires t to be an integer")
    if not(isinstance(e, float)): raise TypeError("requires eps to be a float")
    if not(isinstance(distance, str)) : raise TypeError("Requires distance to be a string")
    if not(isinstance(standardization, bool)) : raise TypeError("Requires standardization to be a bool")
    if not(isinstance(window, bool)) : raise TypeError("Requires window to be an boolean")
    if not(isinstance(window_size, int)) : raise TypeError("Requires window_size to be an integer")
    if not(isinstance(step, int)) : raise TypeError("Requires step to be an integer")
    if not(isinstance(lmin, int)) : raise TypeError("Requires lmin to be an integer")
    if not(isinstance(thw, int)) : raise TypeError("Requires thw to be an integer")


    ' Raise error if parameters do not respect input rules '
    if m <= 0 : raise ValueError("Requires m to be positive and greater than 0")
    if t <= 0 : raise ValueError("Requires t to be positive and  greater from 0")
    if e <0: raise ValueError("Requires eps to be positive")
    if distance != 'euclidean' and distance != 'maximum' and distance !='manhattan': raise ValueError("Requires a valid way to compute distance")
    if window_size<= 0 or window_size>x.shape[0]: raise ValueError("Requires window_size to be positive and greater than 0 and lesser than the length of the input signals")
    if step <= 0 or step > x.shape[0]/3.0: raise ValueError("Requires window to be positive and greater than 0 and lesser equal to one third of the length of the signals")
    if lmin <=0 or lmin > x.shape[0]: raise ValueError("Requires lmin to be positive and greater than 0 and lesser than the length of the input signal")
    if thw < 0 or thw > x.shape[0]: raise ValueError("Requires thw to be positive and greater than 0 and lesser than the length of the input signals")
    
    'Error if x and y have not the same size'

    if x.shape[0]!=y.shape[0] :
        raise ValueError("The two signals have different length")
     
    plot=False

    RR_w=np.array([])
    DET_w=np.array([])
    L_w=np.array([])
    L_w_max=np.array([])
    Entr_w=np.array([])

    pos = 0
    
    result=dict()
            
    if not window:
        
        c=CrossRecurrencePlot.CrossRecurrencePlot(x,y,m,t,e,distance,standardization,plot)
        
        crp_m=1-c['crp'].copy()
           
        if (crp_m.shape[0]!=crp_m.shape[1]):
            thw=0 
        
        hist_P=np.zeros([1,crp_m.shape[0]])[0]            
               
        RR_w=np.append(RR_w, RR(crp_m,thw))
        DET_w=np.append(DET_w, DET(crp_m,hist_P,RR_w,lmin))
        L_w=np.append(L_w, L(crp_m,hist_P,lmin))
        L_w_max=np.append(L_w_max, L_max(crp_m,hist_P,lmin))
        Entr_w=np.append(Entr_w,Entr(crp_m,hist_P,lmin))
        
        result['RR']= RR_w
        result['DET']= DET_w
        result['L']= L_w
        result['L_max']= L_w_max
        result['ENT']=Entr_w
    
    else:
        if window_size < 5+(m-1)*t:
            window_size=5+(m-1)*t

        while((pos+window_size)<x.shape[0]):
            end = pos+window_size-1
             
            windowed_x=x[pos:end].reset_index(drop=True) 
            windowed_y=y[pos:end].reset_index(drop=True)
             
            hist_P=np.zeros([1,window_size])[0]
        
            c_wind=CrossRecurrencePlot.CrossRecurrencePlot(windowed_x,windowed_y,m,t,e,distance,standardization,plot)
             
            crp_m_wind=1-c_wind['crp'].copy()
            
            RR_w=np.append(RR_w, RR(crp_m_wind,thw))
            DET_w=np.append(DET_w, DET(crp_m_wind,hist_P,RR_w,lmin))
            L_w=np.append(L_w, L(crp_m_wind,hist_P,lmin))
            L_w_max=np.append(L_w_max, L_max(crp_m_wind,hist_P,lmin))
            Entr_w=np.append(Entr_w,Entr(crp_m_wind,hist_P,lmin))
            
            
            result['RR']= RR_w
            result['DET']= DET_w
            result['L']= L_w
            result['L_max']= L_w_max
            result['ENT']=Entr_w

            pos += step

    return result
    
#crqa measures


def RR(crp_matrix,thw):
    """
    It computes the Recurrence Rate (RR)
    """
    if crp_matrix.shape[0] == 0 : raise ValueError("Error : crp_matrix signal 0 is empty")
    if crp_matrix.shape[1] == 0 : raise ValueError("Error : crp_matrix signal 1 is empty")
    
    if (thw==0) or (thw==1):
        rr=(1.0/(crp_matrix.shape[0]*crp_matrix.shape[1]))*(np.count_nonzero(crp_matrix)-thw*np.trace(crp_matrix,offset=thw)) 
    else:
        rr=(1.0/(crp_matrix.shape[0]*crp_matrix[1]))*(np.count_nonzero(crp_matrix)-2*np.trace(crp_matrix,offset=thw))

    return rr


def DET(crp_matrix,hist_P,rr,lmin): 
    """
    It computes the Determinism (DET)
    """

    if np.any(rr == 0) :
        raise ValueError("DET cannot computed, a division for zero occurred")
    
    for offs in range(-(crp_matrix.shape[0]-1),crp_matrix.shape[0],1):
        diag_line=np.diagonal(crp_matrix,offset=offs)
        length_diag_line=np.array(length_ones_seq(diag_line))

        if (not length_diag_line.size) or (length_ones_seq(length_diag_line)<lmin).all():
            continue

        indices_diag_line=np.hstack(np.where(length_diag_line >=lmin))

        for i in range(0,indices_diag_line.size):
            hist_P[length_diag_line[indices_diag_line[i]]-1]=hist_P[length_diag_line[indices_diag_line[i]]-1]+1
           
    det=1.0*(sum(np.arange(lmin,crp_matrix.shape[0])*hist_P[lmin:crp_matrix.shape[0]]))/(rr*(crp_matrix.shape[0]*crp_matrix.shape[1]))
    
    if det>1:
       det=1.0
        
    return det


def L(crp_matrix,hist_P,lmin):
    """
    It computes the Average Diagonal Line Length (L)
    """
    if sum(hist_P[lmin-1:crp_matrix.shape[0]])==0 :
        raise ValueError("L cannot computed, a division for zero occurred")
    
    l_avg=1.0*(np.sum(np.arange(lmin,crp_matrix.shape[0]+1)*hist_P[lmin-1:crp_matrix.shape[0]]))/sum(hist_P[lmin-1:crp_matrix.shape[0]])
    return l_avg


def L_max(crp_matrix,hist_P,lmin):
    """
    It computes the Maximum Diagonal Line Length (L)
    """
    l_max=np.max(np.where(hist_P!=0))+1
    return l_max


def Entr(crp_matrix,hist_P,lmin): 
    """
    It computes the Entropy (ENTR)
    """
    if np.sum(hist_P[lmin-1:crp_matrix.shape[0]])==0 :
         raise ValueError("ENTR cannot computed, a division for zero occurred")
    
    hist_P_norm=1.0*hist_P[lmin-1:crp_matrix.shape[0]]/np.sum(hist_P[lmin-1:crp_matrix.shape[0]])
    hist_P_norm_def=hist_P_norm[np.nonzero(hist_P_norm)]
    entr=-np.sum(hist_P_norm_def*np.log(hist_P_norm_def))
    return entr


def length_ones_seq(diag_line):
    """
    It computes the length of a sequence of ones
    """
    return np.array([sum(g) for b, g in itertools.groupby(diag_line) if b])

