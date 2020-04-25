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
import sys                                            	# To be able to import from parent directory
import numpy as np 										# For math operation
import pandas as pd										# For DataFrame
from scipy import stats									# For computing p-value
import matplotlib.pyplot as plt							# Plotting package
import networkx as nx

from statsmodels.regression.linear_model import OLS 	# Class to compute autoregressive model with 'Ordinary Least Squares'  method
from statsmodels.tsa.tsatools import lagmat2ds			# Specific function
from statsmodels.tools.tools import add_constant		# Specific function
from Method import Method, MethodArgList


import DataFrom2Persons.Univariate.Continuous.Linear.GrangerCausality as GC # For Pairwise Granger Causality

class ConditionalGrangerCausality(Method):
    """
    It computes a bi-directional pairwise Granger causality test between all the signals, to detect temporary direct links.
    For each detected link, a conditional test is made to know if the link between the two signals is mediated by another signal.
    At the end of the test, a node graphic is shown to see the links between the signals.

    **Reference :**

    * XiaotongWen, Govindan Rangarajan, and Mingzhou Ding. Univariate Granger causality : an estimation framework based on factorization of the spectral density matrix. Philosophical Transactions of the Royal Society of London A : Mathematical, Physical and Engineering Sciences, 371(1997) :20110610, August 2013.

    :param max_lag:
        The number of maximum lag (in samples) with which the autoregressive model will be computed.
        It ranges in [1;length(x)]. Default :1.
    :type max_lag: int

    :param criterion: A string that contains the name of the selected criterion to estimate optimal number of lags value.
        Two choices are possible :
            1. 'bic' (Bayesian Information Criterion);
            2. 'aic' (Akaike information criterion)
        Default : 'bic'
    :type criterion: str

    :param plot:
        if True the plot of correlation function is returned. Default: False
    :type plot: bool
    """
    argsList = MethodArgList()
    argsList.append('max_lag', 1, int,
                    'The number of maximum lag (in samples) with which the autoregressive model will be computed. It ranges in [1;length(x)]')
    argsList.append('criterion', ['bic', 'aic'], list, 'criterion to estimate optimal number of lags value')
    argsList.append('plot', False, bool, ' plot of correlation function ')

    ''' Constructor '''
    def __init__(self, max_lag = 1, criterion = 'bic', plot = False, **kwargs):
        super(ConditionalGrangerCausality, self).__init__(plot, **kwargs)

        ' Raise error if parameters are not in the correct type '
        try :
            if not(isinstance(criterion, str)) : raise TypeError("Requires criterion to be a str")
            if not(isinstance(max_lag, int))   : raise TypeError("Requires max_lag to be an int")
            if not(isinstance(plot,bool))     : raise TypeError("Requires plot to be a bool")
        except TypeError as err_msg:
            raise TypeError(err_msg)
            return

        ' Raise error if parameters do not respect input rules '

        try :
            if max_lag <= 0 : raise ValueError("Requires max_lag to be a strictly positive scalar")
            if criterion != 'bic' and criterion !='aic' : raise ValueError("Requires criterion to be 'bic' or 'aic'")
        except ValueError as err_msg:
            raise ValueError(err_msg)
            return

        ' Attributes to initialise when creating the object '
        self._max_lag = max_lag
        self._criterion = criterion
        self._plot = plot


    def plot_result(self):
        """
        It plots the final result of the module : a graphic that shows the links between the signals.

        :param result:
            Conditional Granger Causality result from compute()
        :type result: dict

        :returns: plt.figure
            -- A figure that contains the nodes graph
        """
        result = self.res
        ' Raise error if parameters are not in the correct type '
        try :
            if not(isinstance(result, dict)) : raise TypeError("Requires result to be a dictionary")
        except TypeError as err_msg:
            raise TypeError(err_msg)
            return

        ' Raise error if not the good dictionary '
        try :
            if not 'link_matrix' in result : raise ValueError("Requires dictionary to be the output of compute() method")
        except ValueError as err_msg:
            raise ValueError(err_msg)
            return

        # Define a plot figure
        fig = plt.figure()
        ax1 = fig.add_subplot(111)

        # Option on axis
        ax1.set_title('Causality graphic')
        plt.axis('off')

        # Creating a new graph
        G = nx.DiGraph()
        N = np.shape(result['link_matrix'])[0]

        for k in range(0,N):
            G.add_node(str(k+1))

        for i in range(0,N):
            for j in range(0,N):
                if result['link_matrix'][i,j] == 1:
                    G.add_edge(str(j+1),str(i+1))

        # Plot graphic :
        nx.draw_networkx(G, pos = nx.spring_layout(G), with_label = True, node_size = 600, node_color = 'white', edge_color = 'black')
        self._G = G

        # Return figure
        return fig


    ''' Computes ConditionalGrangerCausality test '''
    def compute(self, signals):
        """
        It computes restricted AR and unrestricted AR models, and evaluates whether the x signal could be forecasted
        by the y signal. F-value and p-value are computed, the interpretation of the results is up to the user.

        :param signals:
            array containing the 2 signals as pd.DataFrame
        :type signals: list

        :returns: dict
            -- matrix of links between the signals.

        """

        ' Raise error if parameters are not in the correct type '
        try:
            for i in range(0, len(signals)) :
                if not(isinstance(signals[i], pd.DataFrame)) : raise TypeError("Requires signal " + str(i+1) + " to be a pd.DataFrame, ")

        except TypeError as err_msg:
            raise TypeError(err_msg)
            return

        ' Raise error if DataFrames have not the same size '
        try:
            for i in range(0, len(signals)):
                if len(signals[0]) != len(signals[i]) : raise ValueError("All the signals must have the same size. Signal " + str(i+1) + " does not have the same size as signal 1")
        except ValueError as err_msg:
            raise ValueError(err_msg)
            return

        # Saving the size of signals (they all supposed to have the same size)
        T = len(signals[0])

        # Converting DataFrames to arrays :
        SIGNALS = np.zeros((T,len(signals)))

        for i in range(0,len(signals)):
            SIGNALS[:,i] = np.array(signals[i]).reshape(T)

        # Creating Matrix to save the links between the signals :
        M_direct = np.zeros((len(signals),len(signals)))

        # Testing for direct links between signals :
        for i in range(0,len(signals)):
            for j in range(0,len(signals)):
                if (i != j):
                    gc = GC.GrangerCausality(max_lag = self._max_lag, criterion = self._criterion, plot = False)
                    res = gc.compute([signals[i],signals[j]])
                    if res['ratio'] > 0 and res['p_value'] < 0.01:
                        print ("Results : signal",j+1,"->",i+1,"detected")
                        M_direct[i,j] = 1

        # Computing the FULL VAR model :

        #First we have to determine the optimal order according to the given criterion
        olag_AR = np.zeros((len(signals),1))

        # For each order, computing VAR :
        for k in range(0,len(signals)+1):

            # Permuting columns to compute VAR :
            SIGNALS = np.concatenate((SIGNALS[:,k:],SIGNALS[:,0:k]),axis = 1)

            if k == len(signals):
                break

            criterion_value = np.zeros((self._max_lag,1))

            #Testing each order :
            for lag in range(1, self._max_lag+1):

                data = lagmat2ds(SIGNALS,lag,trim ='both', dropex = 1)
                datajoint = add_constant(data[:, 1:], prepend=False)
                OLS_ = OLS(data[:, 0], datajoint).fit()

                # Saving AIC or BIC temporary values :
                if self._criterion == 'bic':
                    criterion_value[lag-1] = OLS_.bic
                elif self._criterion == 'aic':
                    criterion_value[lag-1] = OLS_.aic

            olag_AR[k] = criterion_value.argmin()+1

        # The optimal order is chosen as the mean order between all the estimated orders from all models
        olag = int(np.ceil(np.mean(olag_AR)))

        # Now we can compute the VAR model with the computed order :
        VAR_resid = np.zeros((T-olag,len(signals)))

        for k in range(0,len(signals)):
            # Permuting columns to compute VAR :
            SIGNALS = np.concatenate((SIGNALS[:,k:],SIGNALS[:,0:k]),axis = 1)

            if k == len(signals):
                break

            data = lagmat2ds(SIGNALS,olag,trim ='both', dropex = 1)
            datajoint = add_constant(data[:, 1:], prepend=False)
            OLS_ = OLS(data[:,0], datajoint).fit()
            VAR_resid[:,k] = OLS_.resid

        # Computing the noise covariance matrix of the full model :
        VAR_noise_matrix = np.cov(VAR_resid.T)


        M_final = np.zeros((len(signals),len(signals)))

        # Testing for mediated links between signals :
        for i in range(0,len(signals)):
            for j in range(0,len(signals)):
                if M_direct[i,j] == 1:
                    # We have detected a "direct link", we need to test with other signals to know if there is a mediated link:
                    for k in range(0,len(signals)):
                        if k != j and k != i:
                            S = np.concatenate((SIGNALS[:,j].reshape(T,1),SIGNALS[:,k].reshape(T,1)),axis = 1)
                            data = lagmat2ds(S,olag,trim ='both', dropex = 1)
                            datajoint = add_constant(data[:, 1:], prepend=False)
                            OLS_ = OLS(data[:,0], datajoint).fit()
                            var_noise = np.var(OLS_.resid)
                            ratio = np.log(var_noise/VAR_noise_matrix[j,j])
                            if ratio <= 0:
                                print ("signal",j+1,"->",i+1," is mediated by signal",k+1)
                                M_direct[i,j] = 0
                                M_final[i,k] = 1
                                M_final[k,j] = 1
                                break
                            else:
                                M_final[i,j] = 1

        self.res = dict()
        self.res['link_matrix'] = M_final

        self.plot()

        return self.res

    @staticmethod
    def getArguments():
        return ConditionalGrangerCausality.argsList.getMethodArgs()

    @staticmethod
    def getArgumentsAsDictionary():
        return ConditionalGrangerCausality.argsList.getArgumentsAsDictionary()
