"""
SpectralGrangerCausality example :
Computes a Spectral Granger Causality test between two signals x and y that are stored as a DataFrame
"""

""" Import common python packages """
import sys
import os
import numpy as np              # Mathematical package
import pandas as pd             # Time serie package
import matplotlib.pyplot as plt # Plotting package
sys.path.insert(0, '../src/')       # To be able to import from parent directory

print("\n")
print("*************************************************************************************")
print("This script computes the Granger Causality test in the spectral domain between two monovariate signals \n" +
      "expressed as Python Pandas DataFrame.")
print("*************************************************************************************")

""" Import Utils modules """
from utils.ExtractSignal import ExtractSignalFromCSV
from utils.ResampleAndInterpolate import ResampleAndInterpolate

""" Import wanted module with every parent packages """
import DataFrom2Persons.Univariate.Continuous.Linear.SpectralGrangerCausality as SGC

""" Import signal from a .csv file """
filename = 'data_examples/1Person_Multivariate_Continuous_data.csv'
print "\nLoading signals from csv files : ", filename,"\n"
x1 = ExtractSignalFromCSV(filename, columns = ['x2'])
x2 = ExtractSignalFromCSV(filename, columns = ['x3'])
""" Define class attributes """
max_lag =10	# Define the maximum lag acceptable to estimate autoregressive models
criterion = 'bic'	# Define the criterion to estimate the optimal number of lags to estimate autoregressive models
plot = True		# Authorize the plot of the results

""" Instanciate the class with its attributes """
print("\n")

try : 
	sgc = SGC.SpectralGrangerCausality(max_lag = max_lag, criterion = criterion, plot = plot)
except TypeError, err :
	print("TypeError in SpectralGrangerCausality constructor : \n" + str(err))
	sys.exit(-1)
except ValueError, err :
	print("ValueError in SpectralGrangerCausality constructor : \n" + str(err))
	sys.exit(-1)
except Exception, e :
	print("Exception in SpectralGrangerCausality constructor : \n" + str(e))
	sys.exit(-1)

print("An instance of the class is now created with the following parameters:\n" +
		"max_lag = " + str(max_lag) + "\n" +
		"criterion = " + str(criterion) + "\n" +
		"plot = " + str(plot))
""" Compute the method and get the result """
print("\n")
print("Computing...\n")
try : 
	results = sgc.compute(x1,x2)
except TypeError, err :
	print("TypeError in SpectralGrangerCausality computation : \n" + str(err))
	sys.exit(-1)
except ValueError, err :
	print("ValueError in SpectralGrangerCausality computation : \n" + str(err))
	sys.exit(-1)
except Exception, e :
	print("Exception in SpectralGrangerCausality computation : \n" + str(e))
	sys.exit(-1)


# Displaying results :
print "Computing autoregressive model 'restricted' and 'unrestricted' via the 'Ordinary Least Squares' method\n"

print "According to",sgc._criterion,", the optimal number of lag estimated is :", sgc._olag,"\n"

print "Printing RESULTS  ...\n"

raw_input("Push ENTER key to exit.")