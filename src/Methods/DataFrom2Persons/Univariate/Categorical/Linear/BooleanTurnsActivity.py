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

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from Method import Method, MethodArgList

class BooleanTurnsActivity(Method):
    """
    It computes data turns statistics between two boolean univariate signals (in pandas DataFrame format) x and y :
    x signal activity duration, y signal activity duration, pause duration, overlap duration,
    x signal pause duration, y signal pause duration, pause duration between x and y activity,
    synchrony ratios between x and y (defined by max_latency).
    
    :param max_latency:
        the maximal delay (in second) between the two signals activity to define synchrony 
    :type max_latency: float
    
    :param min_pause_duration:
        minimal time (in second) for defining a pause 
    :type min_pause_duration: float
    
    :param ele_per_sec:
        number of elements in one second. Default: 1
    :type ele_per_sec: int
    
    :param duration:
        total activity duration (in second). If -1, duration = len(x)*ele_per_sec. Default : -1
    :type duration: int
    """
    argsList = MethodArgList()
    argsList.append('max_latency', 1, float,
                    'the maximal delay (in second) between the two signals activity to define synchrony')
    argsList.append('min_pause_duration', 1, float, 'minimal time (in second) for defining a pause ')
    argsList.append('ele_per_sec', 1, int, 'number of elements in one second')
    argsList.append('duration', -1, int, 'total activity duration (in second)')


    ''' Constructor '''
    def __init__(self, max_latency, min_pause_duration, ele_per_sec=1, duration=-1, **kwargs):
        super(BooleanTurnsActivity, self).__init__(plot=False, **kwargs)
        try :
            if not(isinstance(max_latency, float))          : raise TypeError("Requires max_latency to be an float")
            if not(isinstance(min_pause_duration, float)) : raise TypeError("Requires min_pause_duration to be an integer")
            if not(isinstance(ele_per_sec, int))          : raise TypeError("Requires ele_per_sec to be an integer")
            if not(isinstance(duration, int))             : raise TypeError("Requires duration to be an integer")
        except TypeError as err_msg:
            raise TypeError(err_msg)
            return
        
        try :
            if max_latency < 0 : raise ValueError("Requires max_latency to be a positive scalar")
            if min_pause_duration < 0 : raise ValueError("Requires min_pause_duration to be a positive scalar")
            if ele_per_sec <= 0 : raise ValueError("Requires ele_per_sec to be a strictly positive scalar")
            if duration!=-1 and duration <= 0 : raise ValueError("Requires duration to be a strictly positive scalar (or -1)")
        except ValueError as err_msg:
            raise ValueError(err_msg)
            return

        self._max_latency = max_latency
        self._min_pause_duration = min_pause_duration
        self._freq_per_sec = 1 / float(ele_per_sec) 
        self._duration = duration
        
        self._pause_duration = []
        self._overlap_duration = []
        self._activity_x_duration = []
        self._activity_y_duration = []
        self._overlap_duration = []
        self._y_latency = []
        self._x_latency = []
        self._pause_duration_x = []
        self._pause_duration_y = []
        self._pause_duration_inter_x_y = []
        self._pause_duration_inter_y_x = []
        self._ratio_inter = []
        self._ratio_synchrony = []
        
        self._turns_activity =pd.DataFrame()
        self._turns_activity_ratios = pd.DataFrame()
        
      
    def diff(self, vector):
        """
        Compute  a diff vector
         
        :param np.array:
            input vector to diff
        :type vector: np.array
      
        :retuns: np.array
            -- list of differences between each two consecutive values
        
        """  
        res = []         
        for ind in range(len(vector) - 1):
            res.append(vector[ind+1] - vector[ind])  
        return res

    
    def compute(self, signals):
        """
        Compute data turns activities
          
        :param x:
            first input signal
        :type x: pd.DataFrame
        
        :param y:
            second input signal
        :type y: pd.DataFrame
      
        :returns: pd.DataFrame
            -- duration for each type of activity
        :returns: pd.DataFrame
            -- ratios for each type of activity  
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
        
        '''Initialization'''
        lx=x.size
        ly=y.size
        
        ' Raise error if x and y have not the same size'
        try :
            if lx != ly :
                raise ValueError("x and y signals must have same size")
        except ValueError as err_msg:
            raise ValueError(err_msg)
            return

        if(self._duration == -1):
            self._duration = max(lx, ly) * self._freq_per_sec

        '''X activity'''
        ind_act_x = []
        for ind in range(lx):
            if x.iloc[ind].values == 1 :
                ind_act_x.append(ind)
        
        ind_act_y = []
        for ind in range(ly):
            if y.iloc[ind].values == 1 :
                ind_act_y.append(ind)
        
        diff_act_x = self.diff(ind_act_x)        
        dur_act_x = []
        lat_y = []
        if len(diff_act_x) > 0:
            dur=1
            for i in range(len(diff_act_x)):
                if diff_act_x[i] > 1 :
                    id1 = ind_act_x[i] - dur + 1
                    found = False
                    id2 = -1
                    k = 0;
                    while (found == False and k < len(ind_act_y)):
                        if ind_act_y[k] - id1 > 0:
                            id2 = k
                            found = True;
                        k += 1
                    if(id2 != -1):
                        lat_y.append(ind_act_y[id2] - id1)   
                    dur_act_x.append(dur)
                    dur=0
                dur += 1
            
            id1 = ind_act_x[i] - dur + 1
            found = False
            id2 = -1
            k = 0; 
            while (found == False and k < len(ind_act_y)):
                if ind_act_y[k] - id1 > 0:
                    id2 = k
                    found = True;
                k += 1
            if(id2 != -1):
                lat_y.append(ind_act_y[id2] - id1)
                        
            dur_act_x.append(dur)
            
        '''Y activity'''
        diff_act_y = self.diff(ind_act_y)
        dur_act_y = []
        lat_x = []
        if len(diff_act_y) > 0:
            dur=1
            for i in range(len(diff_act_y)):
                if diff_act_y[i] > 1 :
                    id1 = ind_act_y[i] - dur + 1
                    found = False
                    id2 = -1
                    k = 0; 
                    while (found == False and k < len(ind_act_x)):
                        if ind_act_x[k] - id1 > 0:
                            id2 = k
                            found = True;
                        k += 1
                    if(id2 != -1):
                        lat_x.append(ind_act_x[id2] - id1)
                    dur_act_y.append(dur)
                    dur=0
                dur += 1
              
            id1 = ind_act_y[i] - dur + 1
            found = False
            id2 = -1
            k = 0;
            while (found == False and k < len(ind_act_x)):
                if ind_act_x[k] - id1 > 0:
                    id2 = k
                    found = True;
                k += 1
            if(id2 != -1):
                lat_x.append(ind_act_x[id2] - id1)
         
            dur_act_y.append(dur)
  
        '''Pause duration'''
        ind_pause = []
        for ind in range(lx):
            if x.iloc[ind].values == 0 and y.iloc[ind].values == 0:
                ind_pause.append(ind)
 
        diff_pause = self.diff(ind_pause)        
        dur_pause = []
        if len(diff_pause) > 0:
            dur = 1
            for i in range(len(diff_pause)):
                if diff_pause[i] > 1 :
                    dur_pause.append(dur)
                    dur=0
                dur += 1
            dur_pause.append(dur)

        '''Overlap duration'''
        ind_overlap = []
        for ind in range(lx):
            if x.iloc[ind].values == 1 and y.iloc[ind].values == 1:
                ind_overlap.append(ind)
 
        diff_overlap = self.diff(ind_overlap)
        dur_overlap = []
        if len(diff_overlap) > 0:
            dur = 1
            for i in range(len(diff_overlap)):
                if diff_overlap[i] > 1 :
                    dur_overlap.append(dur)
                    dur=0
                dur += 1
            dur_overlap.append(dur)
            
        ''' Pause inter signals + latency '''
        activity = [0]*lx
        for i in range(lx):
            if x.iloc[i].values == 1 or y.iloc[i].values == 1 : 
                activity[i] = 1
        
        pause_inter = 0
        b_x = 0;
        b_y = 0;
        
        # Find first pause
        try:
            idx_first_pause = activity[1:len(activity)].index(0) + 1
        except ValueError:
            idx_first_pause = len(activity)
        
        if x.iloc[idx_first_pause -1].values == 1 : # End x activity
            b_x = 1
            db_x = 1;
            fn_x = idx_first_pause - 1
        else :                          # End y activity 
            b_y = 1
            db_y = 1
            fn_y = idx_first_pause - 1
            
        dur_pause_x = []
        dur_pause_y = []
        dur_pause_inter_x_y = []
        dur_pause_inter_y_x = []
        ratio_inter = []
        
        while idx_first_pause < len(activity) - 1:
            # Find next activity
            try:
                idx_first_activity = activity[idx_first_pause:len(activity)].index(1) + idx_first_pause
            except ValueError:
                idx_first_activity = len(activity) - 1
                            
            if x.iloc[idx_first_activity].values == 1 :     # Begin x activity
                db_x = idx_first_activity
                if b_x == 1 :                       # Pause inter x activity
                    dur_pause_x.append(idx_first_activity - idx_first_pause)
                else :                              # Pause x => y activity
                    pause_inter = 1
                    dur_pause_inter_y_x.append(idx_first_activity - idx_first_pause)
                    
            else :                              # Begin y activity
                db_y = idx_first_activity
                if b_x == 1 :                       # Pause y => x activity
                    pause_inter = 1
                    dur_pause_inter_x_y.append(idx_first_activity - idx_first_pause)
                else :                              # Pause inter y activity
                    dur_pause_y.append(idx_first_activity - idx_first_pause)
            
            # Find next pause
            try:
                idx_first_pause = activity[idx_first_activity:len(activity)].index(0) + idx_first_activity
            except ValueError:
                idx_first_pause = len(activity)
                
            if x.iloc[idx_first_pause - 1].values == 1 :    # End x activity
                found = False
                idd = idx_first_pause - 1; 
                while (found == False and idd >= 0) :
                    if x.iloc[idd].values == 0:
                        found = True;
                    idd -= 1
                idd += 1
                
                db_x = idd
                fn_x = idx_first_pause - 1
                b_x = 1
                b_y = 0
                if pause_inter == 1 :
                    if((db_x - db_y) != 0) : 
                        ratio_inter.append( float((fn_x - db_y)) / (db_x - db_y) )
                    else:
                         ratio_inter.append(0)
                    pause_inter = 0
                
            else :                              # End y activity
                found = False
                idd = idx_first_pause - 1; 
                while (found == False and idd >= 0) :
                    if y.iloc[idd].values == 0:
                        found = True;
                    idd -= 1
                idd += 1
                
                db_y = idd
                fn_y = idx_first_pause - 1
                b_x = 0
                b_y = 1
                
                if pause_inter == 1 :
                    if((db_y - db_x) != 0) :
                        ratio_inter.append( float((fn_y - db_x)) / (db_y - db_x) )
                    else:
                         ratio_inter.append(0)
                    pause_inter = 0
         
        ''' Save Results '''
        self._activity_x_duration = [k*self._freq_per_sec for k in dur_act_x]
        self._activity_y_duration = [k*self._freq_per_sec for k in dur_act_y] 
        self._overlap_duration = [k*self._freq_per_sec for k in dur_overlap]
        self._ratio_inter = ratio_inter
        
        'Compute pause durations'
        for i in range(len(dur_pause)):
            if(dur_pause[i] * self._freq_per_sec >= self._min_pause_duration):
                self._pause_duration.append(dur_pause[i] * self._freq_per_sec)
        
        for i in range(len(dur_pause_x)):
            if(dur_pause_x[i] * self._freq_per_sec >= self._min_pause_duration):
                self._pause_duration_x.append(dur_pause_x[i] * self._freq_per_sec)

        for i in range(len(dur_pause_y)):
            if(dur_pause_y[i] * self._freq_per_sec >= self._min_pause_duration):
                self._pause_duration_y.append(dur_pause_y[i] * self._freq_per_sec)     
        
        self._pause_duration_inter_x_y = [k*self._freq_per_sec for k in dur_pause_inter_x_y]
        self._pause_duration_inter_y_x = [k*self._freq_per_sec for k in dur_pause_inter_y_x]

        'Compute synchrony ratio for each signal'
        sum_x_latency = 0
        for i in range(len(lat_x)):
            if(lat_x[i] * self._freq_per_sec <= self._max_latency):
                sum_x_latency += 1
        if len(lat_x) > 0 : 
            self._ratio_synchrony.append(float(sum_x_latency) / len(lat_x))
        else :
            self._ratio_synchrony.append(0)
         
        sum_y_latency = 0
        for i in range(len(lat_y)):
            if(lat_y[i] * self._freq_per_sec <= self._max_latency):
                sum_y_latency += 1
        if len(lat_y) > 0 : 
            self._ratio_synchrony.append(float(sum_y_latency) / len(lat_y))
        else :
            self._ratio_synchrony.append(0)
        
        'Save all results in dataFrame'
        res_dict = ({'activity duration x' : pd.Series(self._activity_x_duration), 
                     'activity duration y' : pd.Series(self._activity_y_duration),
                     'overlap duration' : pd.Series(self._overlap_duration),
                     'pause duration' : pd.Series(self._pause_duration),
                     'pause x duration' : pd.Series(self._pause_duration_x),
                     'pause y duration' : pd.Series(self._pause_duration_y),
                     'pause x-y duration' : pd.Series(self._pause_duration_inter_x_y),
                     'pause y-x duration' : pd.Series(self._pause_duration_inter_y_x),
                     'ratio inter' : pd.Series(self._ratio_inter)
                     })
                     
        res_ratio_dict = ({'ratio overlap' : pd.Series(np.sum(self._overlap_duration)/self._duration ),
                     'ratio pause' : pd.Series(np.sum(self._pause_duration)/self._duration ),
                     'ratio activity x' : pd.Series(np.sum(self._activity_x_duration)/self._duration ),
                     'ratio activity y' : pd.Series(np.sum(self._activity_y_duration)/self._duration ),
                     'synchrony ratio x' : pd.Series(self._ratio_synchrony[0]),
                     'synchrony ratio y' : pd.Series(self._ratio_synchrony[1]),
                     'total duration' : pd.Series(self._duration )
                    })
                     
        self._turns_activity = pd.DataFrame(res_dict)
        self._turns_activity[sorted(self._turns_activity.columns)]
        
        self._turns_activity_ratios = pd.DataFrame(res_ratio_dict)
        self._turns_activity_ratios[sorted(self._turns_activity_ratios.columns)]

        result = dict()
        result['turns_activity'] = self._turns_activity
        result['turns_activity_ratios'] = self._turns_activity_ratios
        return result

    @staticmethod
    def getArguments():
        return BooleanTurnsActivity.argsList.getMethodArgs()

    @staticmethod
    def getArgumentsAsDictionary():
        return BooleanTurnsActivity.argsList.getArgumentsAsDictionary()
            
        