"""
MultipleGrangerCausality example :
Computes a Granger Causality test between some signals that are stored as a pandas DataFrame
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
print("This script computes the Granger Causality test between some signals \n" +
      "in pandas DataFrame format.")
print("*************************************************************************************")

""" Import wanted module with every parent packages """
import DataFromManyPersons.Monovariate.Continuous.Linear.MultipleGrangerCausality as MGC
from utils.ExtractSignal import ExtractSignalFromCSV


""" Define signals in pd.dataFrame format """
# preparing the input time series
N = 1000 								# Size of signals
X  = pd.DataFrame({'X' :np.random.randn(N)})	# Signal to test
Y1 = pd.DataFrame({'Y1':np.random.randn(N)})	# Helping signal n1
Y2 = pd.DataFrame({'Y2':np.random.randn(N)})	# Helping signal n2
Y3 = pd.DataFrame({'Y3':np.random.randn(N)})	# Helping signal n3
signal = [X,Y1,Y2,Y3]

'''
"""OR"""
""" Import signal from a .csv file """
filename = 'data_examples/1Person_Multivariate_Continous_data.csv'
x1 = ExtractSignalFromCSV(filename, columns = ['x1'])
x2 = ExtractSignalFromCSV(filename, columns = ['x2'])
x3 = ExtractSignalFromCSV(filename, columns = ['x3'])
x4 = ExtractSignalFromCSV(filename, columns = ['x4'])
x5 = ExtractSignalFromCSV(filename, columns = ['x5'])
signal = [x1,x2,x3,x4,x5]
'''

""" Define class attributes """
max_lag = 10 		# Define the maximum lag acceptable to estimate autoregressive models
criterion = 'aic'	# Define the criterion to estimate the optimal number of lags to estimate autoregressive models
plot = True		# Authorize the plot of the results

""" Instanciate the class with its attributes """
print("\n")
try : 
	mgc = MGC.MultipleGrangerCausality(max_lag = max_lag, criterion = criterion, plot = plot)
except TypeError, err :
	print("TypeError in MultipleGrangerCausality constructor : \n" + str(err))
	sys.exit(-1)
except ValueError, err :
	print("ValueError in MultipleGrangerCausality constructor : \n" + str(err))
	sys.exit(-1)
except Exception, e :
	print("Exception in MultipleGrangerCausality constructor : \n" + str(e))
	sys.exit(-1)

print("An instance of the class is now created with the following parameters:\n" +
		"max_lag = " + str(max_lag) + "\n" +
		"criterion = " + str(criterion) + "\n" +
		"plot = " + str(plot))
	
""" Compute the method and get the result """
print("\n")
print("Computing...\n")

try : 
	results = mgc.compute(*signal)
except TypeError, err :
	print("TypeError in MultipleGrangerCausality computation : \n" + str(err))
	sys.exit(-1)

except ValueError, err :
	print("ValueError in MultipleGrangerCausality computation : \n" + str(err))
	sys.exit(-1)

except Exception, e :
	print("Exception in MultipleGrangerCausality computation : \n" + str(e))
	sys.exit(-1)


# Displaying results :
print "Computing autoregressive model 'restricted' and 'unrestricted' via the 'Ordinary Least Squares' method\n"

print "According to",mgc._criterion,", the optimal number of lag estimated is :", mgc._olag,"\n"

print "Printing RESULTS  ...\n"

print "RESTRICTED model :\n"

print "	Coefficients :\n"
for i in range(0,mgc._olag):
	print"	lag",i+1,":",mgc._OLS_restricted.params[i]
print "\n"
print "	Variance of residual error :", np.var(mgc._OLS_restricted.resid),"\n"

print "UNRESTRICTED model :\n"

print "	Coefficients of 'signal_to_predict' :\n"
for i in range(0,mgc._olag):
	print"	lag",i+1,":",mgc._OLS_unrestricted.params[i]
print "\n"

for k in range(1,4):
	print "	Coefficients of 'helping_signal' " + str(k) + " :\n"
	for i in range(0,mgc._olag):
		print"	lag",i+1,":",mgc._OLS_unrestricted.params[i+k*mgc._olag]
	print "\n"

print "	Variance of residual error :", np.var(mgc._OLS_unrestricted.resid),"\n"

print "F_value =",mgc._F_value," with p_value =",mgc._p_value,"\n"

raw_input("Push ENTER key to exit.")