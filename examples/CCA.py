"""
Correlation example:
It computes the linear correlation between two monovariate signals x and y (in DataFrame format) as a function of their delay tau.
It computes autocorrelation when y coincides with x. 
"""

""" Import common python packages """
import sys
import os
import numpy as np      # Mathematical package
import pandas as pd     # Time serie package
import matplotlib.pyplot as plt # Plotting package

from sklearn import datasets
sys.path.insert(0, '../src/')   # To be able to import packages from parent directory
sys.path.insert(0, '../src/Methods')


print ("\n")
print("***********************************************************************************************************************")
print("This scripts computes the correlation between two monovariate signals."
       "First input is a sinewave of 1 Hz frequency, the second one\n is the sum of this sinewave"
       "with a gaussian random process having zero mean and unitary\n variance.")
print("************************************************************************************************************************")

""" Import wanted module with every parent packages """
import DataFrom2Persons.Multivariate.Continuous.Linear.CCA as CCA

""" Import Utils modules """
from utils import Standardize


""" Define signals in pd.dataFrame format """


# Create signals
data = datasets.load_linnerud()
x = pd.DataFrame(data.data)
y = pd.DataFrame(data.target)

#x.to_csv("CCA_x.csv")
#y.to_csv("CCA_y.csv")

nbr_correlations = 0
standerdized = False

try :
    c = CCA.CCA(nbr_correlations, standerdized, xData=x, yData=y)
except TypeError, err :
    print("TypeError in Correlation constructor : \n" + str(err))
    sys.exit(-1)
except ValueError, err :
    print("ValueError in Correlation constructor : \n" + str(err))
    sys.exit(-1)
except Exception, e :
    print("Exception in Correlation constructor : \n" + str(e))
    sys.exit(-1)

print("An instance the class is now created with the following parameters:\n" +
      "nbr_correlations = " + str(nbr_correlations) + "\n" +
      "standerdized = " + str(standerdized))

""" Compute the method and get the result """

print("Computing...")

try : 
    res = c.compute([])
except TypeError, err :
    print("TypeError in Correlation computation : \n" + str(err))
    sys.exit(-1)
except ValueError, err :
    print("ValueError in Correlation computation : \n" + str(err))
    sys.exit(-1)
except Exception, e :
    print("Exception in Correlation computation : \n" + str(e))
    sys.exit(-1)

""" Display result """

print("**************************************** \n")
print('Canonical correlation analysis complete result :')
print("****************************************\n")
print("Correlation function array:")
print(res['corr'])
print("xWeights:")
print(res['xWeights'])
print("yWeights:")
print(res['yWeights'])


nbr_correlations = 0
standerdized = True

try :
    c = CCA.CCA(nbr_correlations, standerdized, xData=x, yData=y)
except TypeError, err :
    print("TypeError in Correlation constructor : \n" + str(err))
    sys.exit(-1)
except ValueError, err :
    print("ValueError in Correlation constructor : \n" + str(err))
    sys.exit(-1)
except Exception, e :
    print("Exception in Correlation constructor : \n" + str(e))
    sys.exit(-1)

print("\n\n**************************************\n"
      "An instance the class is now created with the following parameters:\n" +
      "nbr_correlations = " + str(nbr_correlations) + "\n" +
      "standerdized = " + str(standerdized))

""" Compute the method and get the result """

print("Computing...")

try :
    res = c.compute([])
except TypeError, err :
    print("TypeError in Correlation computation : \n" + str(err))
    sys.exit(-1)
except ValueError, err :
    print("ValueError in Correlation computation : \n" + str(err))
    sys.exit(-1)
except Exception, e :
    print("Exception in Correlation computation : \n" + str(e))
    sys.exit(-1)

""" Display result """
print("**************************************** \n")
print('Canonical correlation analysis complete result :')
print("****************************************\n")
print("Correlation function array:")
print(res['corr'])
print("xWeights:")
print(res['xWeights'])
print("yWeights:")
print(res['yWeights'])


raw_input("Push ENTER key to exit.")
plt.close("all")
