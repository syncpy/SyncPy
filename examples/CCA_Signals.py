"""
Canonical Correlation example2: signal analysis
It computes Canonical Correlation Analysis between two multivariate signals x and y (in pandas DataFrame format).
s.t. correlations between their linear combinations is maximized.
"""

""" Import common python packages """
import sys
import pandas as pd
import numpy as np

sys.path.insert(0, '../src/')
sys.path.insert(0, '../src/Methods/')

import matplotlib.pyplot as plt # Plotting package
from utils.ExtractSignal import ExtractSignalFromCSV


print ("\n")
print("*********************************************************************************************************************************")
print("This scripts computes CCA between two multivariate signals and study it\'s maximal correlation, i.e. the maximal synchrony between them.\n"
      "The two multivariate signals contain features extracted from an audiovisual recording in which a person pronounces the voyels \'a\', \'o\', and \'e\'\n"
      "For the face we extracted the following action unit (AU): AU25 and AU26"
      "For the voice we extracted RMS and roughness\n"
      "Synchrony is expected to be maximised in a neighborhood of 0\n")
print("**********************************************************************************************************************************")

"""Import wanted module with every parent packages"""
import DataFrom2Persons.Multivariate.Continuous.Linear.CCA as CCA

x = ExtractSignalFromCSV('../src/samples/CCAVoicedata.csv')
y = ExtractSignalFromCSV('../src/samples/CCAFilteredAU.csv')

"removing headers"
x = x.values
y = y.values
x0 = x[:,0]
x1 = x[:,1]
y0 = y[:,0]
y1 = y[:,1]


t=np.arange(0,x.shape[0])


""" Plot input signals """
plt.ion()
f, axarr = plt.subplots(4, sharex=True)
axarr[0].set_title('Input signals')
axarr[0].set_xlabel('Samples')
axarr[1].set_xlabel('Samples')
axarr[2].set_xlabel('samples')
axarr[3].set_xlabel('samples')
axarr[0].set_ylabel('RMS')
axarr[1].set_ylabel('Roughnes')
axarr[2].set_ylabel('AU25')
axarr[3].set_ylabel('AU26')
axarr[0].plot(t, x0, color='g')
axarr[1].plot(t, x1, color='g')
axarr[2].plot(t, y0, color='r')
axarr[3].plot(t, y1, color='r')
axarr[0].legend(loc='best')
axarr[1].legend(loc='best')
axarr[2].legend(loc='best')
axarr[3].legend(loc='best')

nbr_correlations = 0

"cast to pd.Dataframe"
y = pd.DataFrame(y)
x = pd.DataFrame(x)


try :
    c = CCA.CCA(nbr_correlations, xData=x, yData=y, Synchrony=True,plot=True)
except TypeError, err :
    print("TypeError in Coherence constructor : \n" + str(err))
    sys.exit(-1)
except ValueError, err :
    print("ValueError in Coherence constructor : \n" + str(err))
    sys.exit(-1)
except Exception, e :
    print("Exception in Coherence constructor : \n" + str(e))
    sys.exit(-1)


res = c.compute([])

print("************************************************ ")
print('Canonical correlation analysis complete result :')
print("************************************************\n")
print("Correlation function array:")
print(res['corr'])
print('score:')
print(res['score'])
print('maximised corelation by shifting the signals:')
print(res['scoreMax'])
print('obtained by a shift of:')
print(res['shift'])


print("\n\n***********************************************************************************************************************")
print('Synchrony between facial expression and speech is maximised at a delay of 2 samples\n'
      'This delay is coherent with the results obtained in literature from both  psychology and computer science (cfr. the paper of : Mehmet Emre Sargin:\n'
      'Audiovisual Synchronization and Fusion Using Canonical Correlation Analysis\n)'
      'As we used voyells it is coherent to detect an asynchrony between audio speach and video speach if we refer to :\n'
      'http://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1003743#pcbi-1003743-g007\n')
print("***********************************************************************************************************************\n")


raw_input("Push ENTER key to exit.")


