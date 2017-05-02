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
.. moduleauthor:: Marie Avril
"""

import numpy as np
import pandas as pd
from Method import Method, MethodArgList
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

class WindowCrossCorrelation(Method):
    """
    It computes the window cross correlation between two univariate signals (in pandas DataFrame format) x and y 
    
    :param tau_max:
        the maximum lag (in samples) at which correlation should be computed. It is in the range [0; (length(x)+length(y)-1)/2] 
    :type tau_max: int
    
    :param window:
        length (in samples) of the windowed signals 
    :type window: int
    
    :param win_inc:
        amount of time (in samples) elapsed between two windows 
    :type win_inc: int
    
    :param tau_inc:
        amount of time (in samples) elapsed between two cross-correlation 
    :type tau_inc: int
    
    :param plot:
        if True the plot of correlation function is returned. Default: False
    :type plot: bool
    
    :param ele_per_sec:
       number of element in one second
    :type ele_per_sec: int  
    """
    argsList = MethodArgList()
    argsList.append('tau_max', 10, int,
                    'the maximum lag (in samples) at which correlation should be computed. It is in the range [0; (length(x)+length(y)-1)/2]')
    argsList.append('window', 10, int, 'length (in samples) of the windowed signals')
    argsList.append('win_inc', 1, int, 'amount of time (in samples) elapsed between two windows')
    argsList.append('tau_inc', 1, int, 'amount of time (in samples) elapsed between two cross-correlation')
    argsList.append('plot', False, bool, 'if True the plot of correlation function is returned')
    argsList.append('ele_per_sec', 1, bool, 'number of element in one second')
    #argsList.append('test', "D:/projets/2016/SyncPy-Git/src/samples/syncpy_out-20170502/121412-WindowCrossCorrelation-log.txt", file, 'test')

    ''' Constructor '''
    def __init__(self, tau_max = 0, window = 0 , win_inc = 1, tau_inc = 1, plot = False, ele_per_sec = 1, **kwargs):
        super(WindowCrossCorrelation, self).__init__(plot,**kwargs)

        ' Raise error if parameters are not in the correct type '
        try :
            if not(isinstance(tau_max, int))     : raise TypeError("Requires tau_max to be an integer")
            if not(isinstance(window, int))      : raise TypeError("Requires window to be an integer")
            if not(isinstance(win_inc, int))     : raise TypeError("Requires win_inc to be an integer")
            if not(isinstance(tau_inc, int))     : raise TypeError("Requires tau_inc to be an integer")
            if not(isinstance(plot, bool))       : raise TypeError("Requires plot to be a boolean")
            if not(isinstance(ele_per_sec, int)) : raise TypeError("Requires ele_per_sec to be an integer")
        except TypeError, err_msg:
            raise TypeError(err_msg)
            return
        
        ' Raise error if parameters do not respect input rules '
        try : 
            if tau_max < 0 : raise ValueError("Requires tau_max to be a positive scalar")
            if window  < 0 : raise ValueError("Requires window to be a positive scalar")
            if win_inc < 0  or win_inc >= window : raise ValueError("Requires win_inc to be a positive scalar inferior to window length" )
            if tau_inc < 0  or tau_inc > tau_max : raise ValueError("Requires tau_inc to be a positive scalar inferior to tau_max length")
            if ele_per_sec <= 0 : raise ValueError("Requires ele_per_sec to be a strictly positive scalar")
        except ValueError, err_msg:
            raise ValueError(err_msg)
            return
            
        self._tau_max = tau_max
        self._window = window
        self._win_inc = win_inc
        self._tau_inc = tau_inc
        self._plot = plot
        self._ele_per_sec = ele_per_sec
    
    
    ''' Plot the cross matrix '''
    def plot_result(self, result):
        """
        It plots the window cross correlation matrix
         
        :param result:
            window cross correlation dictionary from compute()
        :type result: dict
        
        :returns: plt.figure 
            -- figure plot
        """
        ' Raise error if parameters are not in the correct type '
        try :
            if not(isinstance(result, dict)) : raise TypeError("Requires result to be a dictionary")
        except TypeError, err_msg:
            raise TypeError(err_msg)
            return
        
        ' Raise error if not the good dictionary '
        try :
            if not 'Lag' in result : raise ValueError("Requires dictionary to be the output of compute() method")
        except ValueError, err_msg:
            raise ValueError(err_msg)
            return
        
        corr_mat = np.zeros( (len(result[result.keys()[0]]), len(result)-1) )
        
        idx = 0
        time_window_array = np.zeros(len(result)-1)
        for col in sorted(result.keys()):
            if col != 'Lag':
                for row in range(len(result[col])):
                    corr_mat[row, idx] =  result[col][row]
                time_window_array[idx] = float(col)
                idx += 1
        
        fig = plt.figure()
        ax = fig.add_subplot(111)
        
        ax.set_xlabel('Elapsed Time (s)')
        ax.set_ylabel('Lag (s)')
            
        ax.set_title('Windowed cross correlation matrix')
        
        x_min = time_window_array[0]
        x_max = time_window_array[len(time_window_array)-1]
        y_min = float(max(result['Lag']))
        y_max = float(min(result['Lag']))
        cax = ax.imshow(corr_mat, interpolation='bicubic', aspect='auto', \
                        extent=[x_min, x_max,y_min,y_max], \
                        cmap=plt.cm.hot)
        fig.colorbar(cax)
        
        return fig
           
  
    def compute(self, signals):
        """
         it computes correlation function
         
        :param signals:
            array containing the 2 signals as pd.DataFrame
        :type signals: list
      
        :returns: dict
            -- windowed cross correlation dictionary with (2 * tau_max + 1)/tau_inc rows and (length(x) - window - win_inc)/ win_inc columns
        """
        try:
            if not (isinstance(signals, list)): raise TypeError("Requires signals be an array")
            if len(signals) != 2: raise TypeError("Requires signals be an array of two elements")
        except TypeError, err_msg:
            raise TypeError(err_msg)

        x = signals[0]
        y = signals[1]

        ' Raise error if parameters are not in the correct type '
        try :
            if not(isinstance(x, pd.DataFrame)) : raise TypeError("Requires x to be a pd.DataFrame")
            if not(isinstance(y, pd.DataFrame)) : raise TypeError("Requires y to be a pd.DataFrame")
        except TypeError, err_msg:
            raise TypeError(err_msg)
            return
        
        lx = x.size
        ly = y.size
        
        'Error if x and y have not the same size'
        try :
            if lx != ly:
                raise ValueError("x and y signals must have same size")
        except ValueError, err_msg:
            raise ValueError(err_msg)
            return
        
        ' Initialize default values if not given '
        if self._tau_max == 0:
            self._tau_max = lx / 10
        if self._window == 0:
            self._window = lx / 10
        
        rate = 'sec' if(self._ele_per_sec != 1) else 'samples'
        lag_array = np.arange(-self._tau_max, self._tau_max +1, self._tau_inc)
        
        ' Initialize results '
        cross_corr = {}
        
        i = self._tau_max
        while i <= lx - self._window:
            curr_coef_lag = np.zeros(len(lag_array))
            idx = 0
            for k in lag_array:
                if k <= 0:  # For negative tau
                    curr_x = x[i: i + self._window].values
                    curr_y = y[i + k: i + k + self._window].values
                        
                else:      # For positive tau
                    curr_x = x[i - k: i - k + self._window].values
                    curr_y = y[i: i + self._window].values
                    
                r = 0
                for g in range(len(curr_x)):
                    r += ((curr_x[g] - np.mean(curr_x)) * (curr_y[g] - np.mean(curr_y)) ) / (np.std(curr_x) * np.std(curr_y))
                        
                curr_coef_lag[idx] = r/len(curr_x)
                idx += 1
                
            cross_corr[float(i)/self._ele_per_sec] = curr_coef_lag
            
            ' go to the next window '
            i += self._win_inc
        
        ' Save result '
        results = dict()
        results['Lag'] = [float(x)/self._ele_per_sec for x in lag_array]
        results['cross_corr'] = cross_corr
        if self._plot:
            #plt.ion()
            self.plot_result(cross_corr)
        return results
        #return cross_corr

    @staticmethod
    def getArguments():
        return WindowCrossCorrelation.argsList.getMethodArgs()

    @staticmethod
    def getArgumentsAsDictionary():
        return WindowCrossCorrelation.argsList.getArgumentsAsDictionary()
        
        
        