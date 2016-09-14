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
import matplotlib.pyplot as plt # For plotting

from statsmodels.regression.linear_model import OLS 		# Class to compute autoregressive model with 'Ordinary Least Squares'  method
from statsmodels.tsa.tsatools import lagmat2ds				# Specific function
from statsmodels.tools.tools import add_constant			# Specific function


class SpectralGrangerCausality:
    """
    It computes a Granger causality test between two univariate signals x and y (in pandas DataFrame format), in the
    spectral domain.

    **Reference :**

    * Adam B. Barrett, Michael Murphy, Marie-Aurelie Bruno, Quentin Noirhomme, Melanie Boly, Steven Laureys, and Anil K. Seth. Granger Causality Analysis of Steady-State Electroencephalographic Signals during Propofol-Induced Anaesthesia. PLoS ONE, 7(1) :e29072, January 2012.

    :param max_lag: The number of maximum lag (in samples) with which the autoregressive model will be computed. 
        It ranges in [1;length(x)]. Default : 1.
    :type max_lag: int
    
    :param criterion: A string that contains the name of the selected criterion to estimate optimal number of lags value.
        Two choices are possible :
            1.'bic' (Bayesian Information Criterion);
            2.'aic' (Akaike information criterion)
        Default : 'bic'
    :type criterion: str
    
    :param plot:
        if True the plot of correlation function is returned. Default: False
    :type plot: bool
    """
    
    ''' Constructor '''
    def __init__(self, max_lag = 1, criterion = 'bic', plot = False):
        ' Raise error if parameters are not in the correct type '
        try:
            if not(isinstance(plot, bool))     : raise TypeError("Requires plot to be a bool")
            if not(isinstance(criterion, str)) : raise TypeError("Requires criterion to be a str")
            if not(isinstance(max_lag, int))   : raise TypeError("Requires max_lag to be an int")
        except TypeError, err_msg:
            raise TypeError(err_msg)
            return

        ' Raise error if parameters do not respect input rules '
        try:
            if max_lag <= 0 : raise ValueError("Requires max_lag to be a strictly positive scalar")
            if criterion != 'bic' and criterion !='aic' : raise ValueError("Requires criterion to be 'bic' or 'aic'")
        except ValueError, err_msg:
            raise ValueError(err_msg)
            return

        'Attributes to initialise when creating the object '
        self._max_lag = max_lag
        self._criterion = criterion
        self._plot = plot

        'Attributes that will be initialised when the compute method is called '
        self._OLS_restricted_x = None
        self._OLS_unrestricted_x = None
        self._OLS_restricted_y = None
        self._OLS_unrestricted_y = None
        self._freq = None
        self._F_xy = None
        self._F_value = 0
        self._p_value = 0
        self._olag = 0

    def plot_result(self, result):
        """
        It plots the results of SpectralGrangerCausality Test : F y->x is computed for each frequency (Hz), and then plotted

        :param result:
            Spectral Granger Causality result from compute()
        :type result: dict

        :returns: plt.figure
            -- A figure that contains the plot
        """

        ' Raise error if parameters are not in the correct type '
        try:
            if not(isinstance(result, dict)) : raise TypeError("Requires result to be a dictionary")
        except TypeError, err_msg:
            raise TypeError(err_msg)
            return

        ' Raise error if not the good dictionary '
        try:
            if 'Freq' not in result : raise ValueError("Requires dictionary to be the output of compute() method")
            if 'F_xy' not in result : raise ValueError("Requires dictionary to be the output of compute() method")
        except ValueError, err_msg:
            raise ValueError(err_msg)
            return

        # Define a plot figure
        fig = plt.figure()

        # Define 1 subplots
        ax1 = fig.add_subplot(111)

        # Option on axis 1
        ax1.grid(True)
        ax1.set_title('F y->x expressed as a log ratio')
        ax1.set_xlabel('Frequency (Hz)')
        ax1.set_ylabel('Value')

        # Plot
        ax1.plot(result['Freq'],result['F_xy'], color = 'black')

        # Return figure
        return fig



    ''' Computes GrangerCausality tests '''
    def compute(self,x,y):
        """
        It computes restricted AR and unrestricted AR models, and evaluates whether the x signal could be forecasted
        by the y signal. F-value and p-value are computed, the interpretation of the results is up to the user.

        :param x:
            first input signal - 'signal_to_predict'
        :type x: pd.DataFrame

        :param y:
            second input signal - 'helping_signal'
        :type y: pd.DataFrame

        :returns: dict
            -- F_xy
        """

        ' Raise error if parameters are not in the correct type '
        try:
            if not(isinstance(x, pd.DataFrame)) : raise TypeError("Requires x to be a pd.DataFrame")
            if not(isinstance(y, pd.DataFrame)) : raise TypeError("Requires y to be a pd.DataFrame")
        except TypeError, err_msg:
            raise TypeError(err_msg)
            return

        ' Raise error if DataFrames have not the same length '
        try:
            if len(x) != len(y) : raise ValueError("x and y signals must have same length")
        except ValueError, err_msg:
            raise ValueError(err_msg)
            return


        ' FIRST PART - Computing OLS models '
        # Saving the size of signals (they all supposed to have the same size)
        T = len(x)

        # Saving Sampling rate :
        Delta = x.index[1] - x.index[0]
        self._Time_sampling = Delta.total_seconds()

        # Converting DataFrames to arrays :
        signal_to_predict = np.array(x).reshape(len(x))
        helping_signal = np.array(y).reshape(len(y))

        # Concatenate the two signals in a (nobs,2) array
        X = np.array([signal_to_predict,helping_signal]).T
        Y = np.array([helping_signal,signal_to_predict]).T

        # Arrays that will contain BIC or AIC values according to the given criterion :
        C_r = np.zeros((self._max_lag,1))
        C_u = np.zeros((self._max_lag,1))

        # Computing OLS models for both 'restricted' and 'unrestricted' models, for each lag between 1 and 'max_lag'
        for lag in range(1, self._max_lag+1):

            # Adapting datas :
            data = lagmat2ds(X,lag,trim ='both', dropex = 1)
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
        self._olag = olag

        # Computing OLS models of 'x' signal with the optimal 'lag'
        data = lagmat2ds(X,olag,trim ='both', dropex = 1)
        dataown = add_constant(data[:, 1:(olag + 1)], prepend=False)
        datajoint = add_constant(data[:, 1:], prepend=False)
        self._OLS_restricted_x   = OLS(data[:, 0], dataown).fit()
        self._OLS_unrestricted_x = OLS(data[:, 0], datajoint).fit()

        # Computing OLS models of 'y' signal with the optimal 'lag'
        data = lagmat2ds(Y,olag,trim ='both', dropex = 1)
        dataown = add_constant(data[:, 1:(olag + 1)], prepend=False)
        datajoint = add_constant(data[:, 1:], prepend=False)
        self._OLS_restricted_y = OLS(data[:, 0], dataown).fit()
        self._OLS_unrestricted_y = OLS(data[:, 0], datajoint).fit()

        # checking division by zeros
        if np.any(self._OLS_unrestricted_x.ssr == 0) :
            raise ValueError("self._OLS_unrestricted_x.ssr can't be zero because we divide by it")
            return
        if olag == 0:
            raise ValueError("olag can't be eq to zero because we divide by it")
            return

        # Doing the F-TEST: !!! I don't know if it's necessary here !!!
        self._F_value = ((self._OLS_restricted_x.ssr - self._OLS_unrestricted_x.ssr)/self._OLS_unrestricted_x.ssr/olag*self._OLS_unrestricted_x.df_resid)
        self._p_value = stats.f.sf(self._F_value, olag, self._OLS_unrestricted_x.df_resid)

        ' SECOND PART : Spectral domain causality '

        # Preparing matrix
        K = T
        A_f = np.zeros((K,2,2),dtype = complex)			# Coefficients matrix - spectral domain
        A_t = np.zeros((olag,2,2))						# Coefficients matrix - time domain
        A_tmp = np.zeros((olag,2,2), dtype = complex)	# Tmp matrix
        I = np.identity(2)								# Identity matrix

        T_s = self._Time_sampling		# Sampling time

        # checking division by zeros
        if T_s == 0:
            raise ValueError("T_s can't be eq to zero because we divide by it")
            return
        f = np.linspace(0,1/(2*T_s),K)	# Frequencies
        freq = np.copy(f)			# Saving frequency (Hz) into object (for plot)
        z = np.exp(-1j*2*np.pi*T_s*f)	# complexe value associated with f

        # Assembling parameters :
        for k in range(0,olag):
            A_t[k][0][0] = self._OLS_unrestricted_x.params[k]
            A_t[k][0][1] = self._OLS_unrestricted_x.params[k+olag]
            A_t[k][1][0] = self._OLS_unrestricted_y.params[k+olag]
            A_t[k][1][1] = self._OLS_unrestricted_y.params[k]

        # Computing A(w) :
        for i in range(0,K):
            for k in range(0,olag):
		kk=k+1
                A_tmp[k] = A_t[k]*(z[i]**kk)
            A_f[i] = I - sum(A_tmp)

        # Computing H(w) as the inverse of A(w):
        H_w = np.zeros((K,2,2),dtype = complex)			# Transfert matrix for each w
        for i in range(0,K):
            H_w[i] = np.linalg.inv(A_f[i])

        # Computing F y->x :
        SIG = np.cov(self._OLS_unrestricted_x.resid,self._OLS_unrestricted_y.resid) 	# Covariance matrix
        F_xy = np.zeros(K)														# F y->x value

        for i in range(0,K):
            Sxx = SIG[0][0]*(H_w[i][0][0].real**2 + H_w[i][0][0].imag**2) + SIG[1][1]*(H_w[i][0][1].real**2 + H_w[i][0][1].imag**2)
            Den = SIG[0][0]*(H_w[i][0][0].real**2 + H_w[i][0][0].imag**2)
            # checking division by zeros
            if Den == 0:
                raise ValueError("Den can't be eq to zero because we divide by it")
                return
            F_xy[i] = np.log(Sxx)-np.log(Den)

        result = dict()
        result['Freq'] = freq
        result['F_xy'] = F_xy

        if self._plot:
            plt.ion()
            self.plot_result(result)

        return result
