"""
GrangerCausality example :
Computes a Granger Causality test between some signals that are stored as a DataFrame
"""

""" Import common python packages """
import sys
import os
import numpy as np              # Mathematical package
import pandas as pd             # Time serie package
import matplotlib.pyplot as plt # Plotting package
sys.path.insert(0, '../src/')       # To be able to import from parent directory

print("=================================================================")
print("== Testing for Conditional Granger Causality between 5 signals ==")
print("=================================================================")

""" Import Utils modules """
from utils.ExtractSignal import ExtractSignalFromCSV
from utils.ResampleAndInterpolate import ResampleAndInterpolate

""" Import wanted module with every parent packages """
import DataFromManyPersons.Univariate.Continuous.Linear.ConditionalGrangerCausality as CGC

""" Import signal from a .csv file """
filename = 'data_examples/data_jouet_3.csv'
print "\nLoading signals from csv files : ", filename,"\n"
x1 = ExtractSignalFromCSV(filename, columns = ['x1'])
x2 = ExtractSignalFromCSV(filename, columns = ['x2'])
x3 = ExtractSignalFromCSV(filename, columns = ['x3'])
x4 = ExtractSignalFromCSV(filename, columns = ['x4'])
x5 = ExtractSignalFromCSV(filename, columns = ['x5'])

# Resample and Interpolate data to have constant frequency
x1 = ResampleAndInterpolate(x1, rule='200ms', limit=5)
x2 = ResampleAndInterpolate(x2, rule='200ms', limit=5)
x3 = ResampleAndInterpolate(x3, rule='200ms', limit=5)
x4 = ResampleAndInterpolate(x4, rule='200ms', limit=5)
x5 = ResampleAndInterpolate(x5, rule='200ms', limit=5)

""" Define class attributes """
max_lag = 10 		# Define the maximum lag acceptable to estimate autoregressive models
criterion = 'bic'	# Define the criterion to estimate the optimal number of lags to estimate autoregressive models
plot = True			# Authorize the plot of the results

""" Instanciate the class with its attributes """
print("\n")
try : 
	cgc = CGC.ConditionalGrangerCausality(max_lag = max_lag, criterion = criterion, plot = plot)
except TypeError, err :
	print("TypeError in GrangerCausality constructor : \n" + str(err))
	sys.exit(-1)
except ValueError, err :
	print("ValueError in GrangerCausality constructor : \n" + str(err))
	sys.exit(-1)
except Exception, e :
	print("Exception in GrangerCausality constructor : \n" + str(e))
	sys.exit(-1)

print("An instance of the class is now created with the following parameters:\n" +
		"max_lag = " + str(max_lag) + "\n" +
		"criterion = " + str(criterion) + "\n" +
		"plot = " + str(plot))
	
""" Compute the method and get the result """
print("\n")
print("Computing...\n")
try : 
	results = cgc.compute(x1,x2,x3,x4,x5)
except TypeError, err :
	print("TypeError in GrangerCausality computation : \n" + str(err))
	sys.exit(-1)

except ValueError, err :
	print("ValueError in GrangerCausality computation : \n" + str(err))
	sys.exit(-1)

except Exception, e :
	print("Exception in GrangerCausality computation : \n" + str(e))
	sys.exit(-1)
	
raw_input("Press any key to exit")