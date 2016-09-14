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
.. moduleauthor:: Adem Usta
"""

import numpy as np 				# For math operation
import pandas as pd				# For DataFrame
from scipy import stats			# For computing p-value
import matplotlib.pyplot as plt # Plotting package

from statsmodels.regression.linear_model import OLS 		# Class to compute autoregressive model with 'Ordinary Least Squares'  method
from statsmodels.tsa.tsatools import lagmat2ds				# Specific function
from statsmodels.tools.tools import add_constant			# Specific function


class MultipleGrangerCausality:
	"""
	It computes a Granger causality test between one signal and a couple of other signals
	(in pandas DataFrame format). It computes unidirectionnal causality test with a multivariate autoregressive model and test if
	the unrestricted model is statistically significant compared to the restricted one. An F-test is computed and then the
	interpretation is up to the user.
	
	**Reference :**
	
	* Anil K. Seth. A MATLAB toolbox for Granger causal connectivity analysis. Journal of Neuroscience Methods, 186(2) :262-273, February 2010.
	
	:param max_lag:
		The number of maximum lag (in samples) with which the autoregressive model will be computed. 
		It ranges in [1;length(x)]. Default :1.
	:type max_lag: int
	
	:param criterion: A string that contains the name of the selected criterion to estimate optimal number of lags value.
		Two choices are possible :
		    1.'bic' (Bayesian Information Criterion);
			2 'aic' (for Akaike information criterion)
		Default : 'bic'
	:type criterion: str
	
	:param plot:
		if True the plot of correlation function is returned. Default: False
		:type plot: bool
	"""

	''' Constructor '''
	def __init__(self, max_lag = 1, criterion = 'bic', plot = False):
		
		' Raise error if parameters are not in the correct type '
		try :
			if not(isinstance(criterion, str)) : raise TypeError("Requires criterion to be a str")
			if not(isinstance(max_lag, int))   : raise TypeError("Requires max_lag to be an int")
			if not(isinstance(plot,bool))     : raise TypeError("Requires plot to be a bool")
		except TypeError, err_msg:
			raise TypeError(err_msg)
			return

		' Raise error if parameters do not respect input rules '

		try :
			if max_lag <= 0 : raise ValueError("Requires max_lag to be a strictly positive scalar")
			if criterion != 'bic' and criterion !='aic' : raise ValueError("Requires criterion to be 'bic' or 'aic'")
		except ValueError, err_msg:
			raise ValueError(err_msg)
			return
		
		' Attributes to initialise when creating the object '
		self._max_lag = max_lag
		self._criterion = criterion
		self._plot = plot
		

	def plot_result(self,result):
		"""
		It plots the results of AR process for both restricted and unrestricted models :
		
		:param result:
			Granger Causality result from compute()
		:type result: dict
		
		:returns: plt.figure
			-- A figure that contains all the subplots
		"""
		
		' Raise error if parameters are not in the correct type '
		try :
			if not(isinstance(result, dict)) : raise TypeError("Requires result to be a dictionary")
		except TypeError, err_msg:
			raise TypeError(err_msg)
			return
		
		' Raise error if not the good dictionary '
		try :
			if not 'predicted_signal_restricted' in result : raise ValueError("Requires dictionary to be the output of compute() method")
			if not 'predicted_signal_unrestricted' in result : raise ValueError("Requires dictionary to be the output of compute() method")
		except ValueError, err_msg:
			raise ValueError(err_msg)
			return
		
		# Define 2 subplots
		figure, ax = plt.subplots(2, sharex=True)
		
		# Option on axis 1
		ax[0].grid(True) 											
		ax[0].set_title('Predicted signal - Restricted model')
		ax[0].set_xlabel('Samples') 			
		ax[0].set_ylabel('Amplitude')			
		
		# Option on axis 2
		ax[1].grid(True) 						
		ax[1].set_title('Predicted signal - Unrestricted model')	
		ax[1].set_xlabel('Samples')
		ax[1].set_ylabel('Amplitude')  		
		
		# Plot signals :
		ax[0].plot(result['predicted_signal_restricted'], color = 'blue')
		ax[1].plot(result['predicted_signal_unrestricted'], color = 'green')
		
		# Return figure
		return figure
		
		
	''' Computes GrangerCausality tests '''
	def compute(self,*signals):
		"""
		It computes restricted AR and unrestricted AR models, and evaluates whether the first signal (first parameter) could be forecasted
		by the others. F-value and p-value are computed, the interpretation of the results is up to the user.
		
		:param signals:
			list of signals, one per person.
		:type signals: list[pd.DataFrame]
		
		:returns: dict
			-- F-values and P-values.
		"""
	
		' Raise error if parameters are not in the correct type '
		try :
			for i in range(len(signals)) :
				if not(isinstance(signals[i], pd.DataFrame)): raise TypeError("Requires signal " + str(i+1) + " to be a pd.DataFrame.")
		except TypeError, err_msg:
			raise TypeError(err_msg)
			return
		
		' Raise error if DataFrames have not the same size or same indexes '
		try :
			for i in range(0,len(signals)):
				if len(signals[0]) != len(signals[i]) : raise ValueError("All the signals must have the same size. Signal " + str(i+1) + " does not have the same size as first signal.")
				if signals[0].index.tolist() != signals[i].index.tolist() : raise ValueError("All the signals must have the same time indexes. Signal " + str(i+1) + " does not have the same time index as first signal.")
		except ValueError, err_msg:
			raise ValueError(err_msg)
			return		
		
		# Saving the size of signals (they all supposed to have the same size)
		T = len(signals[0])
		
		# Converting DataFrames to arrays :
		SIGNALS = np.zeros((T,len(signals)))
		
		for i in range(0,len(signals)):
			SIGNALS[:,i] = np.array(signals[i]).reshape(T)
			
		
		# Arrays that will contain BIC or AIC values according to the given criterion :
		C_r = np.zeros((self._max_lag,1))
		C_u = np.zeros((self._max_lag,1))
		
		# Computing OLS models for both 'restricted' and 'unrestricted' models, for each lag between 1 and 'max_lag'
		for lag in range(1, self._max_lag+1):
			
			# Adapting datas :
			data = lagmat2ds(SIGNALS,lag,trim ='both', dropex = 1)
			dataown = add_constant(data[:, 1:(lag + 1)], prepend=False)
			datajoint = add_constant(data[:, 1:], prepend=False)
			
			# OLS models :
			OLS_restricted   = OLS(data[:, 0], dataown).fit()
			OLS_unrestricted = OLS(data[:, 0], datajoint).fit()
			
			# Saving AIC or BIC values :
			if self._criterion == 'bic':
				C_r[lag-1] = OLS_restricted.bic
				C_u[lag-1] = OLS_unrestricted.bic
			elif self._criterion == 'aic':
				C_r[lag-1] = OLS_restricted.aic
				C_u[lag-1] = OLS_unrestricted.aic	
				
		# Determine the optimal 'lag' according to 'bic' or 'aic' criterion :
		olag_r = C_r.argmin()+1
		olag_u = C_u.argmin()+1
		olag = min(olag_r,olag_u)

		# Computing OLS models with the optimal 'lag'
		data = lagmat2ds(SIGNALS,olag,trim ='both', dropex = 1)
		dataown = add_constant(data[:, 1:(olag + 1)], prepend=False)
		datajoint = add_constant(data[:, 1:], prepend=False)
		OLS_restricted   = OLS(data[:, 0], dataown).fit()
		OLS_unrestricted = OLS(data[:, 0], datajoint).fit()
		
		# Doing the F-TEST:
		F_value = ((OLS_restricted.ssr - OLS_unrestricted.ssr)/OLS_unrestricted.ssr/olag*OLS_unrestricted.df_resid)
		p_value = stats.f.sf(F_value, olag, OLS_unrestricted.df_resid)
		
		# Computing predicted signal with restricted model :
		predicted_signal_restricted = np.zeros(T)
		predicted_signal_restricted[0:olag] = np.copy(SIGNALS[0:olag,0])
		
		for i in range(olag,T):
			predicted_signal_restricted[i] =  np.dot(SIGNALS[(i-1)-np.array(range(0,olag)),0],OLS_restricted.params[0:olag])
	
		
		# Computing predicted signal with unrestricted model :
		predicted_signal_unrestricted = np.zeros(T)
		predicted_signal_unrestricted[0:olag] = np.copy(SIGNALS[0:olag,0])

		for i in range(olag,T):
			for k in range(0,len(signals)):
				predicted_signal_unrestricted[i] = predicted_signal_unrestricted[i] + np.dot(SIGNALS[(i-1)-np.array(range(0,olag)),k],OLS_unrestricted.params[k*olag:(k+1)*olag])	
			
		results = dict()
		results['F_value'] = F_value
		results['p_value'] = p_value
		results['optimal_lag'] = olag
		results['predicted_signal_restricted'] = predicted_signal_restricted
		results['predicted_signal_unrestricted'] = predicted_signal_unrestricted
		
		if (self._plot == True):
			plt.ion()
			self.plot_result(results)
		
		return results