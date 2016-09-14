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
from utils import PeakDetect

class PeakPicking :
    """
    It computes peak picking algorithm with window cross correlation results (see WindowCrossCorrelation)
        
    :param corr_matrix:
        matrix of cross correlation computed by WindowCrossCorrelation module
        (windowed cross correlation DataFrame with (2 * tau_max + 1)/tau_inc rows and (length(x) - window - win_inc)/ win_inc colums) 
    :type corr_matrix: pd.DataFrame
    
    :param tau_max:
        the maximum lag (in samples) at which correlation should be computed. It is in the range [0, (length(x)+length(y)-1)/2]  
    :type tau_max: int
    
    :param tau_inc:
        amount of time (in samples) elapsed between two cross-correlation 
    :type tau_inc: int
    
    :param threshold:
        minimal correlation magnitude acceptable for a peak. It is in the range [-1;1]
    :type threshold: float
    
    :param lookahead:
        distance to look ahead from a peak candidate to determine if it is the actual peak. Default: 200
        (sample / period) / f where 4 >= f >= 1.25 might be a good value
    :type lookahead: int
    
    :param delta:
        it specifies a minimum difference between a peak and the following points, before a peak may be considered a peak.
        Useful to hinder the function from picking up false peaks towards to end of the signal.
        To work well delta should be set to delta >= RMSnoise * 5. Default: 0
    :type delta: int
    
    :param ele_per_sec:
       number of elements in one second
    :type ele_per_sec: int
    
    :param plot:
        if True the plot of peakpicking function is returned. Default: False
    :type plot: bool
    
    :param plot_on_mat:
        if True the plot of peakpicking + correlation matrix function is returned. Default: False
    :type plot_on_mat: bool
    
    :param sorted_peak:
        if True the peaks found will be organized by type of Lag and Magnitude (positive or negative). Default: False
    :type plot_on_mat: bool 
    """

    ''' Constructor '''
    def __init__(self, corr_matrix, tau_max, tau_inc = 0, threshold = 0, lookahead = 300, delta = 0, ele_per_sec = 1, plot = False, plot_on_mat = False, sorted_peak = False):
        
        ' Raise error if parameters are not in the correct type '
        try :
            if not(isinstance(corr_matrix, pd.DataFrame)) : raise TypeError("Requires corr_matrix to be a pd.DataFrame")
            if not(isinstance(tau_max, int))        : raise TypeError("Requires tau_max to be an integer")
            if not(isinstance(tau_inc, int))        : raise TypeError("Requires tau_inc to be an integer")
            if not(isinstance(threshold, float))    : raise TypeError("Requires threshold to be an float")
            if not(isinstance(lookahead, int))      : raise TypeError("Requires plot to be a integer")
            if not(isinstance(delta, int))          : raise TypeError("Requires delta to be an integer")
            if not(isinstance(ele_per_sec, int))    : raise TypeError("Requires ele_per_sec to be an integer")
            if not(isinstance(plot, bool))          : raise TypeError("Requires plot to be a boolean")
            if not(isinstance(plot_on_mat, bool))   : raise TypeError("Requires plot_on_mat to be an boolean")
            if not(isinstance(sorted_peak, bool))   : raise TypeError("Requires sorted_peak to be an boolean")
        except TypeError, err_msg:
            raise TypeError(err_msg)
            return
        
        ' Raise error if parameters do not respect input rules '
        try : 
            if tau_max < 0 : raise ValueError("Requires tau_max to be a positive scalar")
            if tau_inc < 0  or tau_inc > tau_max : raise ValueError("Requires tau_inc to be a positive scalar inferior to tau_max length")
            if threshold <0 or threshold  > 1 : raise ValueError("Requires threshold to be between 0 and 1")
            if ele_per_sec <= 0 : raise ValueError("Requires ele_per_sec to be a strictly positive scalar")
        except ValueError, err_msg:
            raise ValueError(err_msg)
            return
        
        self._corr_matrix = corr_matrix
        self._tau_max = tau_max
        self._tau_inc = tau_inc
        self._threshold = threshold
        self._lookahead = lookahead
        self._delta = delta
        self._ele_per_sec = ele_per_sec
        self._plot = plot
        self._plot_on_mat = plot_on_mat
        self._sorted_peak = sorted_peak
        
        self._peak_found = pd.DataFrame()
        
    
    def plot(self):
        """
         It plots the peakpicking result
         
        :returns: plt.figure 
         -- figure plot
        """
        
        if self._plot_on_mat :
            corr_mat = np.zeros(self._corr_matrix.shape)
        for row in range(self._corr_matrix.shape[0]) :
            for col in range(self._corr_matrix.shape[1]) :
                corr_mat[row, col] =  self._corr_matrix.iloc[row, col]

        x_arr = self._peak_found.index.values
        if(len(x_arr) > 0):
            x_min = x_arr[0]
            x_max = x_arr[len(x_arr)-1]
            y_min = float(self._tau_max) / self._ele_per_sec
            y_max = -float(self._tau_max) / self._ele_per_sec
            
            y_arr_max = []
            y_arr_min = []
            for k in range(len(self._peak_found['extremum'].values)) :
                if self._peak_found['maximum'].values[k][0] == self._peak_found['extremum'].values[k][0] :
                    y_arr_max.append(self._peak_found['maximum'].values[k][0])
                    y_arr_min.append(np.nan)
                else :
                    y_arr_min.append(self._peak_found['minimum'].values[k][0])
                    y_arr_max.append(np.nan)
        
            fig = plt.figure()
            ax = fig.add_subplot(111)
            
            if (self._ele_per_sec == 1):
                ax.set_xlabel('Elapsed Time (in samples)')
                ax.set_ylabel('Lag (in samples)')
            else:
                ax.set_xlabel('Elapsed Time (s)')
                ax.set_ylabel('Lag (s)')
            
            ax.set_xlim(x_min, x_max)
            ax.set_ylim(y_min, y_max)
    
            ax.set_title('Peak Picking - Time lag of peak correlation')
    
            cax = ax.imshow(corr_mat, interpolation='bicubic', aspect='auto', \
                            extent=[x_min, x_max,y_min,y_max], \
                            cmap=plt.cm.hot)
            fig.colorbar(cax)
            
            ax.plot(x_arr,y_arr_max, 'ko')
            ax.plot(x_arr, y_arr_min,'wo')
        
        else :     
            x_arr = self._peak_found.index.values
          
            y_arr_max = []
            y_arr_min = []
            for k in range(len(self._peak_found['extremum'].values)) :
                if self._peak_found['maximum'].values[k][0] == self._peak_found['extremum'].values[k][0] :
                    y_arr_max.append(self._peak_found['maximum'].values[k][0])
                    y_arr_min.append(np.nan)
                else :
                    y_arr_min.append(self._peak_found['minimum'].values[k][0])
                    y_arr_max.append(np.nan)
            
            fig = plt.figure()
            ax = fig.add_subplot(111)
            ax.set_ylim(float(self._tau_max) / self._ele_per_sec, -float(self._tau_max) / self._ele_per_sec)
            
            if (self._ele_per_sec == 1):
                ax.set_xlabel('Elapsed Time (in samples)')
                ax.set_ylabel('Lag (in samples)')
            else:
                ax.set_xlabel('Elapsed Time (s)')
                ax.set_ylabel('Lag (s)')   
            ax.set_title('Peak Picking - Time lag of peak correlation')
            
            ax.grid(True)
            
            ax.plot(x_arr,y_arr_max, 'ro', label='positive correlation')
            ax.plot(x_arr, y_arr_min,'bo', label='negative correlation')
            plt.legend(bbox_transform=plt.gcf().transFigure)
        
        return fig

      
    def compute(self):
        """
        It computes peak picking  from cross correlation matrix
      
        :returns: pd.DataFrame
            -- if sorted_peak is False, peaks found organized per Maximin, Minimum and Extremum
        :returns: pd.DataFrame
            -- if sorted_peak is True, peaks found organized by type of Lag and Magnitude (positive or negative)    
        """
        
        'initialize parameters'
        lag_vect = self._corr_matrix.index
        peak_found = {}
        
        for col in self._corr_matrix :
        
            curr_corr = self._corr_matrix[col].values
            peakind = PeakDetect.peakdetect(curr_corr, lag_vect, self._lookahead, self._delta)
            
            'Keep only the highest correlation'
            max = 0
            max_tab = [np.nan, np.nan]
            for k in range(len(peakind[0])) : #maxima
               if( max < peakind[0][k][1]) :
                    max = peakind[0][k][1]
                    
                    if max > self._threshold:
                        if(type(peakind[0][k][1]) == int):
                            max_tab = [peakind[0][k][0], peakind[0][k][1]]
                        else:
                            max_tab = [peakind[0][k][0], peakind[0][k][1][0]]
                        
            min = 0
            min_tab = [np.nan, np.nan]
            for l in range(len(peakind[1])) : #minima
               if( min > peakind[1][l][1]) : 
                    min = peakind[1][l][1]

                    if min < - self._threshold:
                        if(type(peakind[1][l][1]) == int):
                            min_tab = [peakind[1][l][0], peakind[1][l][1]]
                        else:
                            min_tab = [peakind[1][l][0], peakind[1][l][1][0]] 
                        
            extr_tab = [np.nan, np.nan] #extremum
            if min_tab[1] is np.nan:
                extr_tab = max_tab
            else : 
                if(max_tab[1] > np.abs(min_tab[1])) :
                    extr_tab = max_tab
                    
            if max_tab[1] is np.nan:
                extr_tab = min_tab
            else : 
                if(max_tab[1] <= np.abs(min_tab[1])) :
                    extr_tab = min_tab

            peak_found.update({col : [max_tab,min_tab, extr_tab] })
        
        ' Save result '
        peak_found.update({'Time window' : pd.Series(['maximum', 'minimum', 'extremum'])})
        self._peak_found = pd.DataFrame(peak_found)
        self._peak_found.set_index('Time window', inplace = True)
        self._peak_found = self._peak_found.T
        
        if self._plot :
            plt.ion()
            self.plot()
        
        if self._sorted_peak :
            result = self.sort_peakPickingResult()
        else :
            result = self._peak_found
            
        return result
    
    
    def sort_peakPickingResult(self) : 
        """
        It organizes peakPicking result in order to compute statistics
      
        :returns: pd.DataFrame
            -- peaks found organized by type of Lag and Magnitude (positive or negative)
        """
        
        peak_dict = {}
        for k in range(len(self._peak_found['extremum'].values)) :
            curr_tab = [np.nan] * 14

            curr_tab[0] = self._peak_found['extremum'].values[k][0] #Lag
            curr_tab[1] = self._peak_found['extremum'].values[k][1] # magnitude
            
            if (curr_tab[0] >= 0) : 
                curr_tab [2] = curr_tab[0] # Lag>0
                curr_tab [3] = curr_tab[1] # Lag>0 - Magnitude 
                if(curr_tab[1] >= 0) :
                    curr_tab [4] = curr_tab[0] # Lag>0 AND Mag>0
                    curr_tab [5] = curr_tab[1] # Lag>0 AND Mag>0 - Magnitude 
                else :
                    curr_tab [6] = curr_tab[0] # Lag>0 AND Mag<0
                    curr_tab [7] = curr_tab[1] # Lag>0 AND Mag<0 - Magnitude 
            else :
                curr_tab [8] = curr_tab[0] # Lag<0
                curr_tab [9] = curr_tab[1] # Lag<0 - Magnitude 
                if(curr_tab[1] >= 0) :
                    curr_tab [10] = curr_tab[0] # Lag<0 AND Mag>0
                    curr_tab [11] = curr_tab[1] # Lag<0 AND Mag>0 - Magnitude 
                else :
                    curr_tab [12] = curr_tab[0] # Lag<0 AND Mag<0
                    curr_tab [13] = curr_tab[1] # Lag<0 AND Mag<0 - Magnitude 
            
            peak_dict.update({self._peak_found.index.values[k] : curr_tab })
        
        peak_dict.update({'Time window' : pd.Series(['Lag', 'Magnitude',
                                                     'Lag>0','Lag>0 - Mag',
                                                     'Lag>0 AND Mag>0', 'Lag>0 AND Mag>0 - Mag',
                                                     'Lag>0 AND Mag<0', 'Lag>0 AND Mag<0 - Mag',
                                                     'Lag<0','Lag<0 - Mag',
                                                     'Lag<0 AND Mag>0','Lag<0 AND Mag>0 - Mag',
                                                     'Lag<0 AND Mag<0', 'Lag<0 AND Mag<0 - Mag'])})
        stats_peaks = pd.DataFrame(peak_dict)
        stats_peaks.set_index('Time window', inplace = True)
        stats_peaks = stats_peaks.T
        
        return stats_peaks
        
        
        
        