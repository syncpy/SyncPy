"""
Canonical Correlation example:
It computes the linear projections between two datasets s.t. correlations between them is maximized
"""

""" Import common python packages """
import sys
import os
import numpy as np      # Mathematical package
import pandas as pd     # Time serie package
import matplotlib.pyplot as plt # Plotting package

from sklearn import datasets

sys.path.insert(0, '../src/')   # To be able to import packages from parent directory
sys.path.insert(0, '../src/Methods/')


print ("\n")
print("*********************************************************************************************************************************")
print("This scripts computes CCA between two datasets of a gym club "
       "These two datasets represent different views of the client :\n In the first one we have physical realisation (how good they are)"
       "In the second we have physiological data over the persons\n So we expect a strong correlation between these two datasets\n"
	"For more detail see the description in data = datasets.load_linnerud()\n"
    "This is a simple use and interpretation of the CCA algorithm to see how it is working and what kind of outputs we can expect of it" )
print("**********************************************************************************************************************************")

""" Import wanted module with every parent packages """
import DataFrom2Persons.Multivariate.Continuous.Linear.CCA as CCA



""" Define signals in pd.dataFrame format """


# Create signals
data = datasets.load_linnerud()
x = pd.DataFrame(data.data)
y = pd.DataFrame(data.target)


nbr_correlations = 0

try :
    c = CCA.CCA(nbr_correlations, xData=x, yData=y)
except TypeError as err :
    print("TypeError in Correlation constructor : \n" + str(err))
    sys.exit(-1)
except ValueError as err :
    print("ValueError in Correlation constructor : \n" + str(err))
    sys.exit(-1)
except Exception as e :
    print("Exception in Correlation constructor : \n" + str(e))
    sys.exit(-1)

print("An instance the class is now created with the following parameters:\n" +
      "nbr_correlations = " + str(nbr_correlations) + "\n")

""" Compute the method and get the result """

print("Computing...")

try :
    res = c.compute([])
except TypeError as err :
    print("TypeError in Correlation computation : \n" + str(err))
    sys.exit(-1)
except ValueError as err :
    print("ValueError in Correlation computation : \n" + str(err))
    sys.exit(-1)
except Exception as e :
    print("Exception in Correlation computation : \n" + str(e))
    sys.exit(-1)

""" Display result """

print("************************************************ ")
print('Canonical correlation analysis complete result :')
print("************************************************\n")
print("Correlation function array:")
print(res['corr'])
print("xWeights:")
print(res['xWeights'])
print("yWeights:")
print(res['yWeights'])
print('score:')
print(res['score'])


print("\n\n***********************************************************************************************************************")
print('Having a correlation of 0.89 is good (highest possible is 1):\n'
	'Now looking at firts columns of weights matrices we can say that the variable\n'
	'Waist and sit ups play a more important role when it comes to linking the correlation between these two datasets\n'
	'Indeed they have the highest value\n')
print("***********************************************************************************************************************\n")


print("\nIf you want to see exactly what kind of role does those variable have you can look at canonical loadings\n")
print("For more documentation see :\"Robust methods for data reduction\" by Alessio Farcomeni and Luca Greco ")

input("Push ENTER key to exit.")
plt.close("all")
