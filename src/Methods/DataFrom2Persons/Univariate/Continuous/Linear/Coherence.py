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

from utils import Welch_psd
from utils import Cpsd
from utils import Detrend
from Method import Method, MethodArgList

class Coherence(Method):
  """
  It computes the linear correlation between two univariate signals x and y (in pandas DataFrame format) as a function of the frequency.
  It is the cross-spectral density function normalized by the autospectral density function of x and y.
  
   **Reference :**
   
   * Inspired by a John Hunter's Python code 
  
  :param fs:
    sampling frequency (in Hz) of the input DataFrame . Default: 1.0
  :type fs: float
  
  :param NFFT:
    length (in samples) of each epoch. Default: 256
  :type NFFT: int
  
  :param detrend:
    it specifies which kind of detrending should be computed on the inout. It ranges in [0;2]:
        1. 0 no detrending;
        2. 1 constant detrending;
        3. 2 linear detrending.
    Default: 0
  :type detrend: int
  
  :param noverlap:
    number of sampels to overlap between epochs. Default: 0
  :type noverlap: int
  
  :param plot:
    if True the plot of coherence function is returned. Default: False
  :type plot: bool
  """
  argsList = MethodArgList()
  argsList.append('fs', 1.0, float, 'sampling frequency (in Hz) of the input DataFrame')
  argsList.append('NFFT', 256, int, 'length (in samples) of each epoch')
  argsList.append('detrend', 0, int, 'which kind of detrending should be computed on the inout [0;2]')
  argsList.append('noverlap', 0, int, 'number of sampels to overlap between epochs')
  argsList.append('plot', False, bool, 'if True the plot of coherence function is returned')

  ''' Constructor '''
  def __init__(self, fs=1.0, NFFT=256, detrend=0, noverlap=0, plot=False, **kwargs):
    super(Coherence, self).__init__(plot,**kwargs)
    
    ' Raise error if parameters are not in the correct type '
    try :
      if not(isinstance(fs, float))     : raise TypeError("Requires fs to be an float")
      if not(isinstance(NFFT, int))     : raise TypeError("Requires NFFT to be an integer")
      if not(isinstance(detrend, int))  : raise TypeError("Requires detrend to be an integer")
      if not(isinstance(noverlap, int)) : raise TypeError("Requires noverlap to be an integer")
      if not(isinstance(plot, bool))    : raise TypeError("Requires plot to be a boolean")
    except TypeError as err_msg:
      raise TypeError(err_msg)
      return
    
    ' Raise error if parameters do not respect input rules '
    try : 
      if (detrend != 0)  and (detrend != 1) and (detrend != 2): raise ValueError("Requires detrend to be 0 or 1 or 2" )
    except ValueError as err_msg:
      raise ValueError(err_msg)
      return
          
    self.fs=fs
    self.NFFT=NFFT
    self.detrend=detrend
    self.noverlap=noverlap
    self._plot=plot
  
  
  def plot_result(self, result):
    """
    It plots the coherence function
    
    :param result:
        coherence and frequencies from compute()
    :type result: dict
        
    :returns: plt.figure 
     -- figure plot
    """
    
    ' Raise error if parameters are not in the correct type '
    try :
        if not(isinstance(result, dict)) : raise TypeError("Requires result to be a dictionary")
    except TypeError as err_msg:
        raise TypeError(err_msg)
        return
      
    ' Raise error if not the good dictionary '
    try : 
        if not 'Frequency' in result : raise ValueError("Requires dictionary to be the output of compute() method")
        if not 'Coherence' in result : raise ValueError("Requires dictionary to be the output of compute() method")
    except ValueError as err_msg:
        raise ValueError(err_msg)
        return
          
    figure = plt.figure() # Define a plot figure 
    ax = figure.add_subplot(111) # Add axis on the figure
    
    ax.set_ylabel('Coherence')
    ax.set_xlabel('Frequency (Hz)')
    ax.set_title('Coherence')
    ax.set_xlim(0,np.amax(result['Frequency']))
    ax.set_ylim(0,1)
    
    step_x = np.amax(result['Frequency'])/10
    ax.set_xticks(np.arange(0,np.amax(result['Frequency']),step_x))
    
    ax.plot(result['Frequency'],result['Coherence'])
    return figure
    
    
  def compute(self, signals):
    """
    It computes the coherence function between x and y.
    
    :param x:
      first input signal
    :type x: pd.DataFrame
    
    :param y:
      second input signal
    :type y: pd.DataFrame
    
    :returns: dict
          --coherence and frequencies over which the coherence is computed
    """
    x = signals[0]
    y = signals[1]
    
    ' Raise error if parameters are not in the correct type '
    try :
        if not(isinstance(x, pd.DataFrame)) : raise TypeError("Requires x to be a pd.DataFrame")
        if not(isinstance(y, pd.DataFrame)) : raise TypeError("Requires y to be a pd.DataFrame")
    except TypeError as err_msg:
        raise TypeError(err_msg)
        return
    
     
    res_x = Welch_psd.Welch_psd(x, self.fs, self.NFFT,self.detrend,self.noverlap,False)
    res_y = Welch_psd.Welch_psd(y, self.fs, self.NFFT,self.detrend,self.noverlap,False)
    

    res_xy = Cpsd.Cpsd(x,y, self.fs, self.NFFT,self.detrend,self.noverlap,False)
    

    f=res_xy['Frequency']
    
    coherence = np.divide(np.absolute(res_xy['psd'])**2 ,np.multiply(res_x['psd'],res_y['psd'])) #
    
    res_coherence_f={'Coherence': coherence, 'Frequency': f}
    
    if self._plot :
      self.plot_result(res_coherence_f)
      
    return res_coherence_f

  @staticmethod
  def getArguments():
      return Coherence.argsList.getMethodArgs()

  @staticmethod
  def getArgumentsAsDictionary():
      return Coherence.argsList.getArgumentsAsDictionary()





