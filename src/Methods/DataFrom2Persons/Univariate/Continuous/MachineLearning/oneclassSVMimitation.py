### This file is a part of the Syncpy library.
### Copyright 2015, ISIR / Universite Pierre et Marie Curie (UPMC)
### Main contributor(s): ELBANI Wail
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
.. module author:: ELBANI Wail
"""

from sklearn import svm
import matplotlib.pyplot as plt
from sklearn.cross_validation import KFold
from sklearn.cluster import KMeans
from sklearn import preprocessing
from sklearn import metrics
from time import time
import numpy as np
import pandas as pd
# import sys, ossns
# import seaborn as
from Method import Method, MethodArgList


class oneclassSVMimitation(Method):
    """
    It compute the recurrence matrix between two videos in order to detect imitation. The data used is STIP (Space-Time Interest Points) extracted
    from each video using Ivan LAPTEV stip.exe.
    This code is inspired by "Automatic measure of imitation during social interaction: A behavioraland hyperscanning-EEG benchmark"
    credits to: Emilie Delaherche, Guillaume Dumas, Jacqueline Nadel, Mohamed Chetouani

    example:
        -Walk-simple.avi===>apply stip.exe=====>walk-simple.csv ====> put csv file generated in video1_STIP(SyncPy\src\samples\video1_STIP)
        -Walk-complex.avi===>apply stip.exe=====>walk-complex.csv ====> put csv file generated in video2_STIP(SyncPy\src\samples\video2_STIP)
        -Now you are set (see example provided in example folder in SyncPy\examples\oneclassSVMimitation)

        -Instructions on how to extract STIP yourself are in README file in Syncpy/src/samples/ExtractSTIP/
        -The link to Ivan LAPTEV: https://www.di.ens.fr/~laptev/interestpoints.html for further details.

    :param vid1file
        the  path the first video
    :type vid1file: file

    :param vid2file
        the path to the second video
    :type vid2file: file

    :param K
        number of words in the codebook or the codewords or visual vocabulary or K means number of clusters
    :type K: int


    :param threshold
        threshold on oneClassSVM scores
    :type threshold: float

"""

    argsList = MethodArgList()
    argsList.append('vid1file', '', file, 'the  path the first video ')
    argsList.append('vid2file', '', file, 'the path to the second video ')
    argsList.append('K', 100, int,
                    ' number of words in the codebook or the codewords or visual vocabulary or K means number of clusters')
    argsList.append('threshold', 0.1, float, 'threshold on oneClassSVM scores ')
    argsList.append('plot', False, bool, 'if True the plot of Recurrence Matrix')

    def __init__(self, vid1file, vid2file, K, threshold=0.1, plot=False, **kwargs):
        super(oneclassSVMimitation, self).__init__(plot, **kwargs)
        """
        -init:
            vid1file: the  path the first video
            vid2file: the  path the second video
            K: number of words in the codebook or the codewords or visual vocabulary or K means number of clusters
            windowsize: number of frames for each training vector  example of 2 frame : vect[1,2]--vect[3,4]--vect[5,6]
            threshold: Rij=heaviside(threshold-Sab) where Rij is the recurrence matrix
        """

        ' Raise error if parameters are not in the correct type '
        try:
            if not (isinstance(vid1file, file)): raise TypeError("Requires vid1file to be an file")
            if not (isinstance(vid2file, file)): raise TypeError("Requires vid2file to be an file")
            if not (isinstance(K, int)): raise TypeError("Requires K to be an integer")
            if not (isinstance(threshold, float)): raise TypeError("Requires threshold to be a float")
            if not (isinstance(plot, bool)): raise TypeError("Requires plot to be a boolean")
        except TypeError, err_msg:
            raise TypeError(err_msg)
            return

        self.vid1file = str(vid1file.name)
        self.vid2file = str(vid2file.name)
        self.K = K
        self.threshold = threshold

    def compute(self, signals):
        """
        return recurrence Matrix
        """

        data1, data2, hoghof = self.load_process_data()
        kmean = self.k_means_predict(hoghof, self.K)
        h2 = self.histograms(data2, self.K, kmean)
        h1 = self.histograms(data1, self.K, kmean)

        self.res = {}
        self.res['Rij'], self.res['Dij'] = self.recurrence_matrix(h1, h2, self.threshold)

        self.plot()

        return self.res

    def Cross_validation(self, h):
        n_folds = 4
        nu = np.linspace(0.001, 1, 1000)
        results = []
        for d in nu:
            onesvm = svm.OneClassSVM(kernel=self.my_kernel, nu=d)
            hypothesisresults = []
            for train, test in KFold(len(h), n_folds):
                onesvm.fit(h[train])  # fit
                hypothesisresults.append(np.mean(onesvm.predict(h[test]) == 1))

            results.append(np.mean(hypothesisresults))

        return nu[np.argmax(results)]

    def histograms(self, data, K, kmean):
        """
        -input:
            -data: hoghof descriptor
            -number of principal component (comes from applying pca)
            -K: number of words in the codebook or the codewords or visual vocabulary or K means number of clusters
        """
        i = 0
        gbp = data
        predclust = kmean.predict(preprocessing.scale(data.drop(['frame'], axis=1)))
        gbp['pred'] = predclust
        gbp = gbp.groupby('frame')
        train = np.zeros((len(gbp), K))
        for name, group in gbp:
            train[i][group.pred.values] = 1
            i += 1

        return train

    def k_means_predict(self, data, K, ini='k-means++'):
        """
        input:
            -data: hoghf descriptor
        output:
            -Kmean classifier
        descrition: apply Kmeans
        """
        t0 = time()
        kmean = KMeans(init=ini, n_clusters=K, n_init=10)
        kmean.fit(data)
        t = time()
        print("training  time for kmeans------:" + str(t - t0))
        print("silhouette ------:" + str(metrics.silhouette_score(data, kmean.labels_, metric='euclidean')))
        return kmean

    def my_kernel(self, X, Y):

        return X.dot(Y.T)

    def OneSVM_predict(self, h, my_kernel):
        nuu = self.Cross_validation(h)
        print('nu coeficient is:    ' + str(nuu))
        onesvm = svm.OneClassSVM(kernel=my_kernel, nu=nuu)
        onesvm.fit(h)
        return onesvm

    def SAB(self, h1, h2):
        svm1 = self.OneSVM_predict(h1, self.my_kernel)
        svm2 = self.OneSVM_predict(h2, self.my_kernel)
        Sab1 = (svm1.decision_function(h2) - svm1.intercept_)
        Sab2 = (svm2.decision_function(h1) - svm1.intercept_)

        return Sab1, Sab2

    def recurrence_matrix(self, h1, h2, threshold):
        """
        input:
            -h1,h2 histograms
        output:
            -Rij:Recurrence matrix
            -Dij:Raw Recurrence matrix (before applying the threshold)
        """
        sab1, sab2 = self.SAB(h1, h2)
        Rij = np.zeros((h1.shape[0], h2.shape[0]))
        Dij = np.zeros((h1.shape[0], h2.shape[0]))

        for i in range(h1.shape[0]):
            for j in range(h2.shape[0]):
                Rij[i][j] = np.where(np.square(sab1[j] - sab2[i]) - threshold < 0, 1, 0)
                Dij[i][j] = np.square(sab1[j] - sab2[i])

        return Rij, Dij

    def plot_result(self, interpol='nearest'):
        """
        This method is not fully functional. it is used for test purposes only
        """
        x = []
        y = []
        plt.rcParams.update(plt.rcParamsDefault)


        for index, v in np.ndenumerate(self.res['Rij']):
            if v == 1:
                x.append(index[0])
                y.append(index[1])

        H, xedges, yedges = np.histogram2d(x, y, normed=True)
        extent = [yedges[0], yedges[-1], xedges[-1], xedges[0]]
        plt.imshow(H, extent=extent, interpolation=interpol)
        #        plt.colorbar()
        plt.gca().invert_yaxis()
        #plt.show()
        return plt.figure()

    def load_process_data(self):
        """
        output:
            -data1: dataframe for the first videoc 'STIP' points
            -data2: dataframe for the second video 'STIP' points
            -hoghof: descriptor of both videos. We used a combination of  histogram of gradients and histogram of flow
        """

        print("################ loading data ######################")

        'loading the STIP into a panda dataframe'
        try:
            data1 = pd.read_csv(self.vid1file, header=None, sep=r"\s+", skiprows=3)
            data2 = pd.read_csv(self.vid2file, header=None, sep=r"\s+", skiprows=3)
        except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)

        'drop useless columns'

        data1.drop(data1.columns[[0, 1, 2, 4, 5, 6]], axis=1, inplace=True)
        data2.drop(data2.columns[[0, 1, 2, 4, 5, 6]], axis=1, inplace=True)

        'columns names'

        column = ["hgf" + str(i) for i in range(162)]
        column.insert(0, 'frame')

        'naming the columns'
        data1.columns = column
        data2.columns = column

        ' Working in the same frame range'
        data1 = data1[(data1.frame >= max(min(data1.frame), min(data2.frame))) & (
        data1.frame <= min(max(data1.frame), max(data2.frame)))]
        data2 = data2[(data2.frame >= max(min(data1.frame), min(data2.frame))) & (
        data2.frame <= min(max(data1.frame), max(data2.frame)))]

        'merging the two dataframes'
        data = data1.append(data2, ignore_index=True)
        data = data.drop(['frame'], axis=1)
        #        data=preprocessing.scale(data)

        return data1, data2, data

    @staticmethod
    def getArguments():
        return oneclassSVMimitation.argsList.getMethodArgs()

    @staticmethod
    def getArgumentsAsDictionary():
        return oneclassSVMimitation.argsList.getArgumentsAsDictionary()

