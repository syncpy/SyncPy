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
import DataFromManyPersons.Univariate.Continuous.Linear.MultipleGrangerCausality as MGC
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

""" Plot input signals """
Signals = [X, Y1, Y2, Y3]
plt.ion()

nrows = len(Signals)
figure, ax = plt.subplots(nrows, sharex=True)
idx = 0 
for col in  range(len(Signals)) :
    ax[idx].grid(True) # Display a grid
    ax[idx].set_title('Input signal : ' + str(Signals[col].columns[0]))
    ax[idx].plot(Signals[col].index, Signals[col].iloc[:,0])
    idx += 1
    
ax[idx-1].set_xlabel('Time')

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
print "According to",criterion,", the optimal number of lag estimated is :", results['optimal_lag'],"\n"
print "F_value =",results['F_value']," with p_value =",results['p_value'],"\n"

raw_input("Push ENTER key to exit.")