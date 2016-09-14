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
import itertools

import Standardize
import Distance
import Embedding


def _row_rep(s, size, i, vd, e, crp_tmp):
    row_rep_T = pd.concat([s.iloc[i, :]] * size, axis=1, ignore_index=True)
    row_rep = row_rep_T.transpose()

    diff_threshold_norm = e - Distance.Minkowski(row_rep, s, vd)

    diff_threshold_norm = np.ma.MaskedArray(diff_threshold_norm < 0).data
    #diff_threshold_norm[diff_threshold_norm >= 0] = 0
    #diff_threshold_norm[diff_threshold_norm < 0] = 1

    crp_tmp[size - 1 - i, :] = diff_threshold_norm.T
    return np.fliplr(crp_tmp.T)

def _rr_row_rep(s, size, vd, e, crp_tmp, curRange):
    dist_m = np.zeros((size, size))

    for i in curRange:
        row_rep_T = pd.concat([s.iloc[i, :]] * size, axis=1, ignore_index=True)
        row_rep = row_rep_T.transpose()

        dist = Distance.Minkowski(row_rep, s, vd)

        dist_m[i, :] = dist.T

    dist_m_f = dist_m.flatten()
    dist_m_f.sort()

    s_x = dist_m_f[np.ceil(e * len(dist_m_f))]

    for i in curRange:
        diff_threshold_norm = s_x - dist_m[i, :].T

        diff_threshold_norm = np.ma.MaskedArray(diff_threshold_norm < 0).data
        #diff_threshold_norm[diff_threshold_norm >= 0] = 0
        #diff_threshold_norm[diff_threshold_norm < 0] = 1

        crp_tmp[size - 1 - i, :] = diff_threshold_norm.T

    return np.fliplr(crp_tmp.T)

def JointRecurrencePlot(x,y,m,t,e,distance,standardization = False, plot = False):
    """
    It computes and plots the joint recurrence plot of the uni/multivariate input signal(s) x and y (in pandas DataFrame format).

    **Reference :**

    * N. Marwan, M. Carmen Romano, M. Thiel and J. Kurths. "Recurrence plots for the analysis of complex systems". Physics Reports 438(5), 2007.

    :param x:
        first input signal
    :type x: pd.DataFrame

    :param y:
        second input signal
    :type y: pd.DataFrame

    :param m:
        embedding dimension
    :type m: int

    :param t:
       embedding delay
    :type t: int

    :param eps:
        threshold for recurrence
    :type eps: float

    :param distance:
        It specifies which distance method is used. It can assumes the following values:\n
        1. 'euclidean';
        2. 'maximum';
        3. 'manhattan'
        4. 'fixed distance maximum norm'

    :type distance: str

    :param standardization:
       if True data are nomalize to zero mean and unitary variance. Default: False
    :type standardization: bool


    :param plot:
       if True the plot of correlation function is returned. Default: False
    :type standardization: bool


    """
    ' Raise error if parameters are not in the correct type '
    if not(isinstance(x, pd.DataFrame)): raise TypeError("Requires x to be a pd.DataFrame")
    if not(isinstance(y, pd.DataFrame)): raise TypeError("Requires y to be a pd.DataFrame")

    if not(isinstance(m, int)): raise TypeError("Requires m to be an integer")
    if not(isinstance(t, int)): raise TypeError("Requires t to be an integer")
    if not(isinstance(e, float)): raise TypeError("requires eps to be a float")
    if not(isinstance(distance, str)): raise TypeError("Requires distance to be a string")
    if not(isinstance(standardization, bool)): raise TypeError("Requires standardization to be a bool")
    if not(isinstance(plot, bool)): raise TypeError("Requires plot to be a bool")

    ' Raise error if parameters do not respect input rules '
    if m <= 0: raise ValueError("Requires m to be positive and greater than 0")
    if t <= 0: raise ValueError("Requires t to be positive and  greater from 0")
    if e < 0: raise ValueError("Requires eps to be positive")
    if distance != 'euclidean' and distance != 'maximum' and distance != 'manhattan' and distance != 'rr':
        raise ValueError("Requires a valid way to compute distance")

    'Error if x and y have not the same size'
    if x.shape[0] != y.shape[0]: raise ValueError("The two signals have different length")

    if standardization:
        x = Standardize.Standardize(x)
        y = Standardize.Standardize(y)

    if m != 1 or t != 1:
        x = Embedding.Embedding(x, m, t)
        y = Embedding.Embedding(y, m, t)

    vd = 2
    if distance == 'euclidean':
        pass
    elif distance == 'manhattan':
        vd = 1
    elif distance == 'maximum':
        vd = np.inf

    size = x.shape[0]
    crp_x_tmp = np.ones((size, size))
    crp_y_tmp = crp_x_tmp.copy()

    curRange = range(0, size)
    if distance != 'rr':
        for i in curRange:
            crp_x = _row_rep(x, size, i, vd, e, crp_x_tmp)
            crp_y = _row_rep(y, size, i, vd, e, crp_y_tmp)
    else:
        crp_x = _rr_row_rep(x, size, vd, e, crp_x_tmp, curRange)
        crp_y = _rr_row_rep(y, size, vd, e, crp_y_tmp, curRange)

    jrp = (1 - crp_x)*(1 - crp_y)
    jrp = 1 - jrp

    result = dict()
    result['jrp'] = jrp

    if plot:
        plt.ion()
        figure = plt.figure()
        ax = figure.add_subplot(111)

        ax.set_xlabel('Time (in samples)')
        ax.set_ylabel('Time (in samples)')
        ax.set_title('Joint recurrence matrix')

        ax.imshow(result['jrp'], plt.cm.binary_r, origin='lower', interpolation='nearest', vmin=0, vmax=1)

    return result

