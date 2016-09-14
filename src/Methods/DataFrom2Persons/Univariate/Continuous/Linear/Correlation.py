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

from Method import Method, MethodArgList

from utils import Standardize


class Correlation(Method):
    """
    It computes the linear correlation between two univariate signals x and y (in pandas DataFrame format) as a function of their delay tau.
    It computes autocorrelation when y coincides with x.
    
    :param tau_max:
        the maximum lag (in samples) at which correlation should be computed. It is in the range [0; (length(x)+length(y)-1)/2] 
    :type tau_max: int
    
    :param plot:
        if True the plot of correlation function is returned. Default: False
    :type plot: bool
    
    :param standardization:
        if True the inputs are standardize to mean 0 and variance 1. Default: False
    :type standardization: bool
    
    :param corr_tau_max:
        if True the maximum of correlation and its lag are returned. Default: False
    :type corr_tau_max: bool
    
    :param corr_coeff:
        if True the correlation coefficient (Pearson's version) is computed. It is enabled only if the parameter standardize is True. Default: False
    :type corr_coeff: bool
    
    :param scale:
        if True the correlation function is scaled in the range [-1;1]
    :type scale: bool
    """
    argsList = MethodArgList()
    argsList.append('tau_max', 0, int,
                    'the maximum lag (in samples) at which correlation should be computed')
    argsList.append('standardization', False, bool, 'if True the inputs are standardize to mean 0 and variance 1')
    argsList.append('corr_tau_max', False, bool, 'if True the maximum of correlation and its lag are returned')
    argsList.append('corr_coeff', False, bool, 'if True the correlation coefficient (Pearson\'s version) is computed')
    argsList.append('scale', False, bool, 'if True the correlation function is scaled in the range [-1;1]')
    argsList.append('plot', False, bool, 'if True the plot of correlation function is returned')

    ''' Constructor '''
    def __init__(self, tau_max, plot=False, standardization=False, corr_tau_max=False, corr_coeff=False, scale=False, **kwargs):
        super(Correlation, self).__init__(plot,**kwargs)
        
        ' Raise error if parameters are not in the correct type '
        try :
            if not(isinstance(tau_max, int))          : raise TypeError("Requires tau_max to be an integer")
            if not(isinstance(plot, bool))            : raise TypeError("Requires plot to be a boolean")
            if not(isinstance(standardization, bool)) : raise TypeError("Requires standardization to be a boolean")
            if not(isinstance(corr_tau_max, bool))    : raise TypeError("Requires corr_tau_max to be a boolean")
            if not(isinstance(corr_coeff, bool))      : raise TypeError("Requires corr_coeff to be a boolean")
            if not(isinstance(scale, bool))           : raise TypeError("Requires scale to be a boolean")
        except TypeError, err_msg:
            raise TypeError(err_msg)
            return
        
        ' Raise error if parameters do not respect input rules '
        try : 
            if tau_max < 0 : raise ValueError("Requires tau_max to be a strictly positive scalar")
        except ValueError, err_msg:
            raise ValueError(err_msg)
            return
        
        self.tau_max=tau_max
        self.standardization=standardization
        self.corr_tau_max=corr_tau_max
        self.corr_coeff=corr_coeff
        self.scale=scale
    

    def plot_result(self):
        """
        It plots the correlation function in the range specified.

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
            if not 'corr_funct' in result : raise ValueError("Requires dictionary to be the output of compute() method")
            if not 'tau_array' in result : raise ValueError("Requires dictionary to be the output of compute() method")
        except ValueError, err_msg:
            raise ValueError(err_msg)
            return
        
        figure = plt.figure() # Define a plot figure 
        ax = figure.add_subplot(111) # Add axis on the figure
        
        ax.set_ylabel('Value')
        ax.set_xlabel('Lag')
        ax.set_title('Correlation Function')
        #ax.set_xlim(max(-self.tau_max, (- (self.ly - 1))),min(self.tau_max, (self.lx - 1)))
        ax.set_ylim(np.min(result['corr_funct']),np.max(result['corr_funct']))
                
        ax.plot(result['tau_array'], result['corr_funct'])
        
        return figure
    
    
    def compute_tau_range(self, lx, ly):
        """
        Computes the range of tau values the correlation function is returned for.
        
        :param self.lx:
            length of the first input signal
        :type self.lx: int
        
        :param self.ly:
            length of the second input signal
        :type self.ly: int
        
        :returns: numpy.array 
          -- the range of tau values the correlation function is returned for
        """
        ll=max(-self.tau_max,(-(ly - 1)))
        ul=min(self.tau_max,(lx - 1))+1

        tau_array=np.arange(ll,ul,1)
        start = tau_array[0]+(ly-1)
        stop = tau_array[tau_array.size - 1] + (ly-1)
        
        return (tau_array, start, stop)
    
    
    def compute_coeff(self, corr_f, lmin, ly):
        """
        It computes the Pearson's correlation coefficient.
        
        :param corr_f:
            correlation function
        :type corr_f: numpy.array
        
        :param lmin:
            the length of the shortest input 
        :type limn: int
        
        :param ly:
            length of the second input 
        :type ly: int
        
        :returns: numpy.array 
          -- time/Pearson's correlation coefficient
        """
        
        corr_coeff=corr_f[ly-1]/(lmin-1)
        
        return corr_coeff
    
         
    def compute(self, signals):
        """
        It computes the correlation function between x and y
        
        :param signals:
            array containing the 2 signals as pd.DataFrame
        :type signals: list

        :returns: dict 
                -- correlation function/maximum of correlation and its lag/Pearson's coefficient
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
        
        
        self.lx=x.shape[0]
        self.ly=y.shape[0]
        
        lmax=max(self.lx,self.ly)
        lmin=min(self.lx,self.ly)
        
        tau_range=self.compute_tau_range(self.lx,self.ly)
        self.tau_array=tau_range[0]
        start=tau_range[1]
        stop=tau_range[2]
        
        
        ' Raise error if parameters do not respect input rules '
        try : 
            if self.tau_max < 0 or self.tau_max >(self.lx-1) : raise ValueError("Requires tau_max to be in the range [0,length x -1]")            
        except ValueError, err_msg:
            raise ValueError(err_msg)
            return
        
        ' Raise warnings '
        try : 
            if self.standardization==False and self.corr_coeff==True :
                raise Warning("Warning! The computation of the correlation coefficient is enabled only when the time series are standardized")
            if self.scale==True and (x.shape[0]!=y.shape[0]) :
                raise Warning("Warning! The computation of scaled correlation function is enabled only when the time series have the same length")
            if self.tau_max > self.ly :
                raise Warning("the value -(length y -1) will be used as -tau_max")       
        except Warning, war_msg:
            raise Warning(war_msg)
        
            
        if self.standardization==False:
            self.corr_f_full=np.correlate(x.iloc[:,0],y.iloc[:,0], mode='full')
            self.corr_f=self.corr_f_full[start:stop+1]
                    
        else:
            x_std=Standardize.Standardize(x)
            y_std=Standardize.Standardize(y)
                              
            self.corr_f_full=np.correlate(x_std.iloc[:,0],y_std.iloc[:,0], mode='full')
            self.corr_f=self.corr_f_full[start:stop+1]
            
        if self.scale==True:
            nx=np.linalg.norm(x.values,2)
            ny=np.linalg.norm(y.values,2)
            self.corr_f=self.corr_f_full[start:stop+1]/(nx*ny)
                
            
        res_corr={}
        res_corr['corr_funct']=self.corr_f
        
        if self.corr_tau_max : 
            max_corr=np.amax(self.corr_f)
            t_max=np.argmax(self.corr_f)
            t_max=self.tau_array[t_max]
            corr_coeff = self.compute_coeff(self.corr_f_full, lmin, self.ly)
            res_corr['max_corr']=max_corr
            res_corr['t_max']=t_max
 
            
        if self.corr_coeff : 
            corr_coeff = self.compute_coeff(self.corr_f_full, lmin, self.ly)
            res_corr['corr_coeff']=corr_coeff
        
        res_corr['tau_array']=self.tau_array

        self.res = res_corr
        
        self.plot()

        return res_corr

    @staticmethod
    def getArguments():
        return Correlation.argsList.getMethodArgs()

    @staticmethod
    def getArgumentsAsDictionary():
        return Correlation.argsList.getArgumentsAsDictionary()

            



        