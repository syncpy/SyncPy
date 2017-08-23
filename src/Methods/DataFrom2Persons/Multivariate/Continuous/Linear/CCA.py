# coding: utf-8
### This file was generated for use with the Syncpy library.
### Copyright 2016, ISIR / Universite Pierre et Marie Curie (UPMC)
### syncpy@isir.upmc.fr
###
### Main contributor(s): Jean Zagdoun
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
.. moduleauthor:: Jean Zagdoun
"""
import warnings

with warnings.catch_warnings():
    warnings.simplefilter("ignore", category=RuntimeWarning)
from Method import Method, MethodArgList
from utils import Standardize
from utils.ExtractSignal import ExtractSignalFromCSV
import numpy as np
from numpy.linalg import eig
from numpy.linalg import inv
from numpy.linalg import svd
from numpy import diag
from math import sqrt
import pandas as pd
from math import ceil
from matplotlib import pyplot as plt


class CCA(Method):
    """
    It extracts the highest correlations possible between linear combinations of the features of the two multivariate signals.
    These signals must contain the same number of row (samples), but
    can contain a different number of features (i.e different number of colums)

    **reference paper** :

      - David Weenink, Canonical correlation analysis
      - Karl Stratos, A Hitchhiker’s Guide to PCA and CCA
      - Alvin C. Rencher, Methods of Multivariate Analysis
      - Mehmet Emre Sargin, Audiovisual Synchronization and Fusion Using Canonical Correlation Analysis

     to see the algorithm on 2 exemples see CCA_simple and CCA_signals in SyncPy-master/expemples

     inputs : Due to technical constraints(graphical issues) the two signals to be processed are passed as contructor's parameters

     :param nbr_correlations: is the number of maximized correlation you want to have at the end
     default 0 means you choose the minimum between the number of features of your two multivariate signals

     :param Synchrony: if True it means that you want to seek if by shifting a little bit your two multivariate signals you will find a better synchrony
     between them.
     default False

     :param Proportion: integer between 0 and 20, represent the proportion of lag you are willing to investigate synchrony on
     default 0: 20% of time lag is used if Synchrony is True

     :param plot: if True gives the distribution of the score(as define bellow) of your Synchrony search


    returns:

    :res['xWeights'] and res['xWeights']: the weights of the linear combinations

    :res['corr']: squared correlations that comes with those weights (length of this array is define by nbr_correlations)

    :res['score']: score is the sum of the squared maximised correlations (with no shift)

    :res['scoreMax']: scoreMax is the score (as define above) maximal that we can find by shifting the two datasets

    :res['shift']: How should we shift the first dataset w.r.t the second to find the scoreMax

    :res{'storage']: is mainly used to plot the distributions of the different score through the shifting process

    """

    argsList = MethodArgList()
    argsList.append('ignoreInputSignals', True, bool, 'Data really comes from the file below', True)
    argsList.append('xData_filename', '', file,
                    'First data set in cvs format')
    argsList.append('yData_filename', '', file,
                    'Second data set in cvs format')
    argsList.append('nbr_correlations', 0, int, 'number of maximised correlations wanted')
    argsList.append('Synchrony', False, bool, 'Do we look for optimal Synchrony')
    argsList.append('Proportion', 0, int, 'how the decay can maximally happen')
    argsList.append('plot', False, bool, 'if True and Synchrony is on toot, the plot of coherence function is returned')

    def __init__(self, ignoreInputSignals = True, nbr_correlations=0, xData=None, yData=None, xData_filename=None, yData_filename=None,
                 Synchrony=False, Proportion=0, plot=False, **kwargs):
        ' Init '
        super(CCA, self).__init__(plot, **kwargs)
        if xData is None:
            if not (xData_filename and isinstance(xData_filename, file)) \
                    or len(xData_filename.name) == 0: raise TypeError("Requires xData_filename to be a file")

        if yData is None:
            if not (yData_filename and isinstance(yData_filename, file)) \
                    or len(yData_filename.name) == 0: raise TypeError("Requires yData_filename to be a file")

        if not (isinstance(nbr_correlations, int)): raise TypeError("Requires m to be an integer")
        # other rule for parameters
        if nbr_correlations < 0: raise ValueError("Requires m to be positive or greater than 0")

        if isinstance(xData_filename, file):
            xData = pd.DataFrame.from_csv(xData_filename)

        if isinstance(yData_filename, file):
            yData = pd.DataFrame.from_csv(yData_filename)
        if not (isinstance(Synchrony, bool)): raise TypeError("Synchrony must be a boolean")
        if not (isinstance(plot, bool)): raise TypeError("plot must be a boolean")
        if (Proportion > 0 and Synchrony == False): raise ValueError(
            "you can't havea positiv proportion if you do not seek synchrony")
        if (Synchrony == True and Proportion == 0): Proportion = 20
        if (Proportion < 0 or Proportion > 20): raise ValueError("Proportion must be between 0 and 20 purcents")

        if not (isinstance(xData, pd.DataFrame)): raise TypeError("Requires xData to be a panda dataframe")
        if not (isinstance(yData, pd.DataFrame)): raise TypeError("Requires yData to be a panda dataframe")

        self._xData = xData
        self._yData = yData
        self._nbr_correlations = nbr_correlations
        self.sync = Synchrony
        self.proportion = Proportion
        self.lx = None
        self.ly = None
        self._plot = plot
        return

    def plot_result(self, result):
        """
        It plots the cca function if you are lokking for synchrony between two signals

        :param result:
             storage from compute()
        :type result: dict

        :returns: plt.figure
         -- figure plot
        """

        ' Raise error if parameters are not in the correct type '
        try:
            if not (isinstance(result, dict)): raise TypeError("Requires result to be a dictionary")
        except TypeError, err_msg:
            raise TypeError(err_msg)
            return

        ' Raise error if not the good dictionary '
        try:
            if not 'storage' in result: raise ValueError("Requires storage to be the output of compute() method")
        except ValueError, err_msg:
            raise ValueError(err_msg)
            return

        dim = result['storage'].shape[0]
        figure = plt.figure()  # Define a plot figure
        ax = figure.add_subplot(111)  # Add axis on the figure
        plot_axis = np.arange(-dim / 2 + 1, dim / 2 + 1)
        ax.set_ylabel('score')
        ax.set_xlabel('lag')
        ax.set_title('sum of maximized correlations')
        ax.set_xlim(-dim / 2 + 1, dim / 2)
        ax.set_ylim(0, min(self.lx, self.ly))
        ax.plot(plot_axis, result['storage'])
        return figure

    def vector_root(self, V):
        l = V.size
        U = np.array(V, float)
        for i in range(0, l):
            U[i] = sqrt(U[i])
        return U

    def inv_vector_root(self, V):
        l = V.size
        U = np.array(V, float)
        for i in range(0, l):
            if (V[i] > 0):
                U[i] = 1 / sqrt(U[i])
            else:
                V[i] = 0
        return U

    def cov(self, A, B):
        l, c = A.shape
        aux = 1.0 / (l - 1)
        sigma = aux * np.dot(A.T, B)
        return sigma

    def SVD_CCA(self, S_X, S_Y, S_XY, m):
        D, v_x = eig(S_X)
        D = self.inv_vector_root(D)
        D = diag(D)
        CX = np.dot(np.dot(v_x, D), inv(v_x))
        D, v_y = eig(S_Y)
        D = self.inv_vector_root(D)
        D = diag(D)
        CY = np.dot(np.dot(v_y, D), inv(v_y))
        omega = np.dot(np.dot(CX, S_XY), CY)
        U, D, T = svd(omega, full_matrices=0)
        A = np.dot(CX, U)
        A = A[:, :m]
        B = np.dot(CY, T.T)
        B = B[:, :m]
        D = D[0:m]
        D = self.vector_root(D)
        return D, B, A

    def compute(self, signals):

        x = self._xData
        y = self._yData

        ' Raise error if parameters are not in the correct type '
        try:
            if not (isinstance(x, pd.DataFrame)): raise TypeError("Requires x to be a pd.DataFrame")
            if not (isinstance(y, pd.DataFrame)): raise TypeError("Requires y to be a pd.DataFrame")
        except TypeError, err_msg:
            raise TypeError(err_msg)
            return
        x = Standardize.Standardize(x)
        y = Standardize.Standardize(y)
        x = x.values
        y = y.values
        if self._nbr_correlations == 0:
            self.lx = x.shape[1]
            self.ly = y.shape[1]
            self._nbr_correlations = min(self.lx, self.ly)
        cov_x = self.cov(x, x)
        cov_y = self.cov(y, y)
        cov_xy = self.cov(x, y)
        D, A, B = self.SVD_CCA(cov_x, cov_y, cov_xy, self._nbr_correlations)

        ' Synchrony seeking '
        if self.sync:
            Max = np.trace(diag(D))
            storage_aux = [Max]
            shift = 0
            prop = int(ceil((self.proportion * x.shape[0]) / 100))
            x_del = x
            y_del = y
            for i in range(prop):
                x_del = np.delete(x_del, (0), axis=0)
                y_del = np.delete(y_del, (-1), axis=0)
                cov_x = self.cov(x_del, x_del)
                cov_y = self.cov(y_del, y_del)
                cov_xy = self.cov(x_del, y_del)
                D1, A1, B1 = self.SVD_CCA(cov_x, cov_y, cov_xy, self._nbr_correlations)
                score_aux = np.trace(diag(D1))
                storage_aux = np.append(storage_aux, score_aux)
                if score_aux >= Max:
                    Max = score_aux
                    shift = i + 1
            x_del = x
            y_del = y
            storage = np.array(5 * np.ones(prop))
            for i in range(prop):
                x_del = np.delete(x_del, (-1), axis=0)
                y_del = np.delete(y_del, (0), axis=0)
                cov_x = self.cov(x_del, x_del)
                cov_y = self.cov(y_del, y_del)
                cov_xy = self.cov(x_del, y_del)
                D1, A1, B1 = self.SVD_CCA(cov_x, cov_y, cov_xy, self._nbr_correlations)
                score_aux = np.trace(diag(D1))
                storage[i] = score_aux
                if score_aux >= Max:
                    Max = score_aux
                    shift = -(i + 1)
            storage = storage[::-1]  # inversion of array
            storage = np.append(storage, storage_aux)

        res = {}
        res['corr'] = D
        res['yWeights'] = A
        res['xWeights'] = B
        res['score'] = np.trace(diag(D))
        if self.sync:
            res['scoreMax'] = Max
            res['shift'] = shift
            res['storage'] = storage
            if self._plot:
                self.plot_result(res)

        return res

    @staticmethod
    def getArguments():
        return CCA.argsList.getMethodArgs()

    @staticmethod
    def getArgumentsAsDictionary():
        return CCA.argsList.getArgumentsAsDictionary()

