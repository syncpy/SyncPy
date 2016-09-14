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
import matplotlib.pyplot as plt

from MutualInformation import MutualInformation
from Method import Method, MethodArgList


class WindowMutualInformation(Method):
    """
    It computes Windowed Mutual Information (MI) estimators starting from entropy estimates from k-nearest-neighbours distances.
    
    **Reference :**
    
    * A.Kraskov, H.Stogbauer, and P.Grassberger. Estimating mutual information. Physical Review E, 69(6):066138, 2004
    
    :param n_neighbours:
        number of nearest neighbours  
    :type n_neighbours: int
    
    :param my_type:
        Type of the estimators will be used to compute MI. Two options (1 and 2) are available:
            1. the number of the points nx and ny is computed by taking into account only the points whose distance is stricly
            less than the distance of the k-nearest neighbours; 
            2. the number of the points nx and ny is computed by taking into account only the points whose distance is equal to
            or less than the distance of the k-nearest neighbours; 
       Default: 1 
    :type my_type: int
    
    :param var_resc:
        Boolean value indicating if the input signals should be rescaled at unitary variance. Default: True
    :type var_resc: bool
    
    :param noise:
        Boolean value indicating if a very low amplitude random noise should be added to the signals.
        It is done to avoid that there are many signals points having identical coordinates. Default: True
    :type noise: bool
    
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
        
    """
    argsList = MethodArgList()
    argsList.append('n_neighbours', 5, int, 'number of nearest neighbours')
    argsList.append('my_type', 1, int, 'type of the estimators will be used to compute MI (1 or 2)')
    argsList.append('var_resc', True, bool, 'input signals should be rescaled at unitary variance')
    argsList.append('noise', True, bool, 'random noise should be added to the signals')
    argsList.append('tau_max', 10, int, 'maximum lag (in samples), range [0; (length(x)+length(y)-1)/2]')
    argsList.append('window', 10, int, 'length (in samples) of the windowed signals')
    argsList.append('win_inc', 1, int, 'amount of time (in samples) elapsed between two windows')
    argsList.append('tau_inc', 1, int, 'amount of time (in samples) elapsed between two cross-correlation')
    argsList.append('plot', False, bool, 'plot the correlation function or not')
    
    ''' Constuctor '''
    def __init__(self, n_neighbours, my_type=1, var_resc=True, noise=True, tau_max = 0, window = 0 , win_inc = 1, tau_inc = 1, plot = False, **kwargs):
        
        ' Raise error if parameters are not in the correct type '
        super(WindowMutualInformation, self).__init__(plot,**kwargs)

        try :
            if not(isinstance(n_neighbours, int)) : raise TypeError("Requires n_neighbours to be an integer")
            if not(isinstance(my_type, int))      : raise TypeError("Requires my_type to be an integer")
            if not(isinstance(var_resc, bool))    : raise TypeError("Requires var_resc to be a boolean")
            if not(isinstance(noise, bool))    : raise TypeError("Requires noise to be a boolean")
            if not(isinstance(tau_max, int))     : raise TypeError("Requires tau_max to be an integer")
            if not(isinstance(window, int))      : raise TypeError("Requires window to be an integer")
            if not(isinstance(win_inc, int))     : raise TypeError("Requires win_inc to be an integer")
            if not(isinstance(tau_inc, int))     : raise TypeError("Requires tau_inc to be an integer")
            if not(isinstance(plot, bool))       : raise TypeError("Requires plot to be a boolean")
        except TypeError, err_msg:
            raise TypeError(err_msg)
            return
        
        ' Raise error if parameters do not respect input rules '
        try :
            if n_neighbours<=0 or n_neighbours>= window: raise ValueError("Requires n_neighbours to be a positive integer greater than 0 inferior to window length")
            if my_type != 1  and my_type != 2 : raise ValueError("Requires my_type to be to be 1 or 2" )
            if tau_max < 0 : raise ValueError("Requires tau_max to be a positive scalar")
            if window  < 0 : raise ValueError("Requires window to be a positive scalar")
            if win_inc < 0  or win_inc >= window : raise ValueError("Requires win_inc to be a positive scalar inferior to window length" )
            if tau_inc < 0  or tau_inc > tau_max : raise ValueError("Requires tau_inc to be a positive scalar inferior to tau_max length")
        except ValueError, err_msg:
            raise ValueError(err_msg)
            return
        
        self._n_neighbours=n_neighbours
        self._type=my_type
        self._var_resc=var_resc
        self._noise=noise
        self._tau_max = tau_max
        self._window = window
        self._win_inc = win_inc
        self._tau_inc = tau_inc
        self.res = None
        
    
    def plot_result(self):
        """
        It plots the window mutual information matrix
        
        :param result:
            Windowed Mutual Information from compute()
        :type result: dict
            
        :returns: plt.figure 
            -- figure plot
        """
        result = self.res
        
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
            
        mi_mat = np.zeros( (len(result[result.keys()[0]]), len(result)-1) )
        
        idx = 0
        time_window_array = np.zeros(len(result)-1)
        for col in sorted(result.keys()):
            if col != 'Lag':
                for row in range(len(result[col])):
                    mi_mat[row, idx] =  result[col][row]
                time_window_array[idx] = float(col)
                idx += 1
        
        fig = plt.figure()
        ax = fig.add_subplot(111)
        
        ax.set_xlabel('Elapsed Time (in samples)')
        ax.set_ylabel('Lag (in samples)')
            
        ax.set_title('Windowed Mutual Information matrix')
        
        x_min = time_window_array[0]
        x_max = time_window_array[len(time_window_array)-1]
        y_min = float(max(result['Lag']))
        y_max = float(min(result['Lag']))
        cax = ax.imshow(mi_mat, interpolation='bicubic', aspect='auto', \
                        extent=[x_min, x_max,y_min,y_max], \
                        cmap=plt.cm.hot)
        fig.colorbar(cax)

        return fig
    
    def compute(self,signals):
        """
        It computes Mutual Information.
         
        :param x:
            first input signal
        :type x: pd.DataFrame
        
        :param y:
            second input signal
        :type y: pd.DataFrame
        
        :returns: dict
            -- Windowed Mutual Information
        """
        x = signals[0]
        y = signals[1]
        
        ' Raise error if parameters are not in the correct type '
        try :
            if not(isinstance(x, pd.DataFrame)) : raise TypeError("Requires x to be a pd.DataFrame")
            if not(isinstance(y, pd.DataFrame)) : raise TypeError("Requires y to be a pd.DataFrame")
        except TypeError, err_msg:
            raise TypeError(err_msg)
            return
        
        lx=x.size
        ly=y.size
        
        'Error if x and y have not the same size'
        try :
            if lx != ly :
                raise ValueError("x and y signals must have same size")
        except ValueError, err_msg:
            raise ValueError(err_msg)
            return
        
        ' Initialize default values if not given '
        if self._tau_max == 0 :
            self._tau_max = lx / 10
        if self._window == 0 :
            self._window = lx / 10
        
        ' Initialize lag array'
        lag_array = np.arange(-self._tau_max, self._tau_max +1, self._tau_inc)
        
        ' Initialize Mutual information instance once '
        mi = MutualInformation(self._n_neighbours, self._type, self._var_resc, self._noise)
        
        ' Initialize results '
        window_MI = {}
        
        i = self._tau_max
        while i <= lx - self._window : 
            curr_coef_lag = []
            for k in lag_array :
                if k <= 0 :  # For negative tau
                    curr_x = x[i : i + self._window].values
                    curr_y = y[i + k : i + k + self._window].values
                        
                else :      # For positive tau
                    curr_x = x[i - k : i - k + self._window].values
                    curr_y = y[i : i + self._window].values
                    
                'Compute MI for current segments'
                curr_MI = mi.compute([pd.DataFrame(curr_x), pd.DataFrame(curr_y)])
                 
                curr_coef_lag.append(curr_MI['MI'])
                
            window_MI.update({float(i) : curr_coef_lag})
            
            ' go to the next window '
            i += self._win_inc

        window_MI['Lag'] = [float(x) for x in lag_array]

        self.res = window_MI
        
        self.plot()
        
        return window_MI

    @staticmethod
    def getArguments():
        return WindowMutualInformation.argsList.getMethodArgs()

    @staticmethod
    def getArgumentsAsDictionary():
        return WindowMutualInformation.argsList.getArgumentsAsDictionary()

    