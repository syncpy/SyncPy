"""
ConditionalGrangerCausality example :
It computes Condtional Granger Causality among signals (in pandas DataFrame format) organized as a list. 
"""

""" Import common python packages """
import sys
import os
import numpy as np              # Mathematical package
import pandas as pd             # Time serie package
import matplotlib.pyplot as plt # Plotting package
sys.path.insert(0, '../src/')       # To be able to import from parent directory
sys.path.insert(0, '../src/Methods')

print("=================================================================")
print("== Testing for Conditional Granger Causality between 4 signals ==")
print("=================================================================")

""" Import Utils modules """
from utils.ExtractSignal import ExtractSignalFromCSV
from utils.ResampleAndInterpolate import ResampleAndInterpolate

""" Import wanted module with every parent packages """
import DataFromManyPersons.Univariate.Continuous.Linear.ConditionalGrangerCausality as CGC

""" Import signal from a .csv file """
filename = 'data_examples/1Person_Multivariate_Continous_data.csv'
print("\nLoading signals from csv files : ", filename,"\n")
x1 = ExtractSignalFromCSV(filename, columns = ['x1'])
x2 = ExtractSignalFromCSV(filename, columns = ['x2'])
x3 = ExtractSignalFromCSV(filename, columns = ['x3'])
x4 = ExtractSignalFromCSV(filename, columns = ['x4'])


""" Define class attributes """
max_lag = 10 		# Define the maximum lag acceptable to estimate autoregressive models
criterion = 'bic'	# Define the criterion to estimate the optimal number of lags to estimate autoregressive models
plot = True			# Authorize the plot of the results

""" Instantiate the class with its attributes """
print("\n")
try : 
	cgc = CGC.ConditionalGrangerCausality(max_lag = max_lag, criterion = criterion, plot = plot)
except TypeError as err :
	print("TypeError in ConditionalGrangerCausality constructor : \n" + str(err))
	sys.exit(-1)
except ValueError as err :
	print("ValueError in ConditionalGrangerCausality constructor : \n" + str(err))
	sys.exit(-1)
except Exception as e :
	print("Exception in ConditionalGrangerCausality constructor : \n" + str(e))
	sys.exit(-1)

print("An instance of the class is now created with the following parameters:\n" +
		"max_lag = " + str(max_lag) + "\n" +
		"criterion = " + str(criterion) + "\n" +
		"plot = " + str(plot))
	
""" Compute the method and get the result """
print("\n")
print("Computing...\n")
try : 
	results = cgc.compute([x1,x2,x3,x4])
except TypeError as err :
	print("TypeError in ConditionalGrangerCausality computation : \n" + str(err))
	sys.exit(-1)

except ValueError as err :
	print("ValueError in ConditionalGrangerCausality computation : \n" + str(err))
	sys.exit(-1)

except Exception as e :
	print("Exception in ConditionalGrangerCausality computation : \n" + str(e))
	sys.exit(-1)
	
input("Press any key to exit")