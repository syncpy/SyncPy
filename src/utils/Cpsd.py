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
import Detrend
from   scipy import signal
import matplotlib.pyplot as plt


def Cpsd(x,y,fs=1.0, NFFT=256, detrend=0,noverlap=0, plot=False):

    """
    It computes the cross power spectral density of two monovariate signals x and y (in pandas DataFrame format) by Welch's.
    This density is as the average of the density through the epochs (segments) of x and y
    and it is corrected for the power leakage due to (the hanning) windowing.
    
    :param x:
        first input signal
    :type x: pd.DataFrame
    
    :param y:
        second input signal
    :type y: pd.DataFrame
        
    :param fs:
        it is the sampling frequency of x (in Hz);
    :type fs: float     
  
    :param NFFT: 
        it is the length of each epoch (segment);
    :type NFFT: int
  
    :param detrend:
        it specifies how the data can be detrended. Three options are avaliable:
        1. 0 none;
        2. 1 mean detrending; and
        3. 1 linear detrending
    :type detrend: bool
  
    :param noverlap:
        it is the number of samples to overlap between epochs (segments);
    :type noverlap: bool
  
    :param plot:
        if it is True the plot of the absolute of the density function is returned. Default: False
    :type plot: bool
    
    :returns: dict 
        -- the cross power spectral density and the frequencies over which the coherence is computed
    """

    ' Raise error if parameters are not in the correct type '
    try :
      if not(isinstance(x, pd.DataFrame)): raise TypeError("Requires x to be a pd.DataFrame")
      if not(isinstance(y, pd.DataFrame)): raise TypeError("Requires y to be a pd.DataFrame")
      if not(isinstance(fs, float)):       raise TypeError("Requires fs to be a float")
      if not(isinstance(NFFT, int)):       raise TypeError("Requires NFFT to be an integer")
      if not(isinstance(detrend, int)):   raise TypeError("Requires detrend to be a boolean")
      if not(isinstance(noverlap, int)):   raise TypeError("Requires noverlap to be an integer")
      if not(isinstance(plot, bool)):      raise TypeError("Requires plot to be a boolean")
    except TypeError, err_msg:
            raise TypeError(err_msg)
            return
     
    ' Raise error if parameters do not respect input rules '
    try :
      if x.shape[1] != 1 :  raise ValueError("Requires signal x to be monovariate")
      if y.shape[1] != 1 :  raise ValueError("Requires signal y to be monovariate")
      if fs < 0 :           raise ValueError("Requires fs to be a positive scalar")
      if NFFT <=0:          raise ValueError("Requires NFFT to be a strictly positive scalar")
      if NFFT %2 != 0:      raise ValueError("Requires NNFT to be a multiple of 2")
      if detrend != 0  and detrend != 1 and detrend != 2 : raise ValueError("Requires detrend to be 0, 1 or 2" )
      if NFFT-noverlap <= 0: raise ValueError("Requires NFFT to be greater than noverlap")
    except ValueError, err_msg:
            raise ValueError(err_msg)
            return

    if x.shape[0] < NFFT:
        res_x=pd.DataFrame(0*np.arange(0,NFFT))
        pd_x=x.combine_first(res_x)
        x=pd_x.fillna(0)
        
    if y.shape[0] < NFFT:
        res_y=pd.DataFrame(0*np.arange(0,NFFT))
        pd_y=y.combine_first(res_y)
        y=pd_y.fillna(0)

    window=signal.get_window('hanning', NFFT)
    step=NFFT-noverlap
    num_wind=np.arange(0,x.shape[0]+1-NFFT,step)
    NFreqs=NFFT//2+1
    
    Pxy_re=np.zeros((NFreqs,len(num_wind)))
    Pxy_im=np.zeros((NFreqs,len(num_wind))) 
    Pxy=np.vectorize(complex)(Pxy_re, Pxy_im) 

    count=0
    pos =0
    
           
    while((pos+NFFT)<x.shape[0]):
        end = pos+NFFT-1
                
        if detrend==0:
            windowed_x = pd.DataFrame(np.multiply(window,np.hstack(x.iloc[pos:end+1].values)))
            windowed_y = pd.DataFrame(np.multiply(window,np.hstack(y.iloc[pos:end+1].values)))  
        elif detrend==1:
            det_x = Detrend.Detrend(x.iloc[pos:end+1],det_type='mean')
            windowed_x = pd.DataFrame(np.multiply(window,np.hstack(det_x.values)))
            det_y = Detrend.Detrend(y.iloc[pos:end+1],det_type='mean')
            windowed_y = pd.DataFrame(np.multiply(window,np.hstack(det_y.values)))
        elif detrend==2:
            det_x = Detrend.Detrend(x.iloc[pos:end+1],det_type='linear')
            windowed_x = pd.DataFrame(np.multiply(window,np.hstack(det_x.values)))
            det_y = Detrend.Detrend(y.iloc[pos:end+1],det_type='linear')
            windowed_y = pd.DataFrame(np.multiply(window,np.hstack(det_y.values)))

        FFT_windowed_x=np.fft.fft(windowed_x.iloc[:,0].values) / NFFT
        FFT_windowed_y=np.fft.fft(windowed_y.iloc[:,0].values) / NFFT
        
        
        Pxy[:,count]=np.multiply(FFT_windowed_y[:NFreqs],np.conj(FFT_windowed_x[:NFreqs])) 
                
        pos = pos + step
        count=count+1
  
    if  len(num_wind) > 1:
        Pxy=np.mean(Pxy, axis=1)
        
    corrected_Pxy=np.divide(Pxy,(np.square(window).sum(axis=0)))
    f = (float(fs)/NFFT)*np.arange(0,NFreqs)
  
    if plot==True:
        plt.ion()
        figure = plt.figure() 
        ax = figure.add_subplot(111) 
        ax.set_ylabel('Cpsd')
        ax.set_xlabel('Frequency(Hz)')
        ax.set_title('Cross Power Spectral Density')
        ax.set_xlim(0,np.amax(f))
        ax.set_ylim(0,np.amax(np.absolute(corrected_Pxy))) 
        x_ticks=np.arange(0,np.amax(f),np.amax(f)/10)
        ax.set_xticks(x_ticks)
     
        #y_ticks=np.arange(0,np.amax(Pxy),1)
        #ax.set_yticks(y_ticks)
        ax.plot(f, np.absolute(corrected_Pxy)) 
        plt.show()
         
    res_cpsd_f={'psd': corrected_Pxy, 'Frequency': f} 
     
    return res_cpsd_f






    
    

