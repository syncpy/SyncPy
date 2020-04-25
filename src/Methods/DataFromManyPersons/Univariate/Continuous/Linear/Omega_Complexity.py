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
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from math import exp
from Method import Method, MethodArgList

class Omega_Complexity(Method):
    """
    It computes Omega complexity among many monovariate signals (organized as a list of pandas DataFrame).
    It is a measure based on spatial principal component analysis (SPCA) carried out on the covariance matrix of the DataFrame. It ranges in [0,N], where 1 stands for maximum synchrony, N minimum synchrony.
    
    **Reference :**
    
    * Wackermann, J. Beyond mapping: estimating complexityof multichannel EEG recordings. Acta Neurobiol. Exp., 1996, 56:197-208.
 
    """
    argsList = MethodArgList()
 
    ''' Constructor '''
    def __init__(self, plot = False, **kwargs):
        super(Omega_Complexity, self).__init__(plot, **kwargs)
        pass

    def plot_result(self):
        pass
    
    def compute(self, signals):
        """
        It computes the Omega complexity for multiple monovariate signals (organized as a list).
        If input signals are multivariates, only the first column of the signal is considered
        
        :param signals:
            list of signals, one per person. 
        :type signals: list[pd.DataFrame]
        
        :returns: dict
            -- omega
        
        """
        
        ' Raise error if parameters are not in the correct type '
        try :
            for i in range(len(signals)) :
                if not(isinstance(signals[i], pd.DataFrame)): raise TypeError("Requires signal " + str(i+1) + " to be a pd.DataFrame.")
        except TypeError as err_msg:
            raise TypeError(err_msg)
            return
        
        ' Raise error if DataFrames have not the same size or same indexes '
        try :
            for i in range(0,len(signals)):
                if len(signals[0]) != len(signals[i]) : raise ValueError("All the signals must have the same size. Signal " + str(i+1) + " does not have the same size as first signal.")
                if signals[0].index.tolist() != signals[i].index.tolist() : raise ValueError("All the signals must have the same time indexes. Signal " + str(i+1) + " does not have the same time index as first signal.")
        except ValueError as err_msg:
            raise ValueError(err_msg)
            return

        'Formate signals in one DataFrame for computing'
        # If input signals are multivariates, only the first column is considered
        x = pd.DataFrame()
        for i in range(0,len(signals)): 
            if x.empty :
                x = pd.DataFrame(signals[i].iloc[:,0], signals[i].index)
                x.columns = [signals[i].columns[0]]
            else :
                x[signals[i].columns[0]] = signals[i].iloc[:,0]
    
        cov_mat=x.cov()
        eig_val,eig_vect=np.linalg.eig(cov_mat.values)
        trace_cov_mat=(cov_mat.values).trace()
        
        lambda_spectrum=eig_val/trace_cov_mat
        
        lambda_spectrum_nozero=lambda_spectrum[lambda_spectrum >0]
        
        omega= exp(-np.sum(li*np.log(li) for li in lambda_spectrum_nozero))
        
        results = dict()
        results['omega'] = omega
        
        return results

    @staticmethod
    def getArguments():
        return Omega_Complexity.argsList.getMethodArgs()

    @staticmethod
    def getArgumentsAsDictionary():
        return Omega_Complexity.argsList.getArgumentsAsDictionary()
         

            



        