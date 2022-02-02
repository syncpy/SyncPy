"""
GrangerCausality example :
Computes a Granger Causality test between two signals x and y that are stored as a DataFrame
"""

""" Import common python packages """
import sys
import numpy as np              # Mathematical package
import matplotlib.pyplot as plt # Plotting package
sys.path.insert(0, '../src/')       # To be able to import from parent directory
sys.path.insert(0, '../src/Methods')

print("\n")
print("*************************************************************************************")
print("This script computes the Granger Causality test between two monovariate signals \n" +
      "in pandas DataFrame format.")
print("*************************************************************************************")

""" Import Utils modules """
from utils.ExtractSignal import ExtractSignalFromCSV
from utils.ResampleAndInterpolate import ResampleAndInterpolate

""" Import wanted module with every parent packages """
import DataFrom2Persons.Univariate.Continuous.Linear.GrangerCausality as GC

""" Import signal from a .csv file """
filename = 'data_examples/2Persons_Monovariate_Continuous_data.csv'
print("\nLoading signals from csv files : ", filename,"\n")
x1 = ExtractSignalFromCSV(filename, columns = ['x1'])
x2 = ExtractSignalFromCSV(filename, columns = ['x2'])

# Resample and Interpolate data to have constant frequency
x1 = ResampleAndInterpolate(x1, rule='200ms', limit=5)
x2 = ResampleAndInterpolate(x2, rule='200ms', limit=5)

""" Plot input signals """
Signals = [x1, x2]
plt.ion()

nrows = len(Signals)
figure, ax = plt.subplots(nrows, sharex=True)
idx = 0
for col in range(len(Signals)):
    ax[idx].grid(True)		# Display a grid
    ax[idx].set_title('Input signal : ' + str(Signals[col].columns[0]))
    ax[idx].plot(Signals[col].index, Signals[col].iloc[:,0])
    idx += 1

ax[idx-1].set_xlabel('Time')


""" Define class attributes """
max_lag = 3 			# Define the maximum lag acceptable to estimate autoregressive models
criterion = 'bic'   	# Define the criterion to estimate the optimal number of lags to estimate autoregressive models
plot = True				# Authorize the plot of the results

""" Instanciate the class with its attributes """
print("\n")

try : 
	gc = GC.GrangerCausality(max_lag = max_lag, criterion = criterion, plot = plot)
except TypeError as err :
	print("TypeError in GrangerCausality constructor : \n" + str(err))
	sys.exit(-1)
except ValueError as err :
	print("ValueError in GrangerCausality constructor : \n" + str(err))
	sys.exit(-1)
except Exception as e :
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
	results = gc.compute([x1,x2])
except TypeError as err :
	print("TypeError in GrangerCausality computation : \n" + str(err))
	sys.exit(-1)
except ValueError as err :
	print("ValueError in GrangerCausality computation : \n" + str(err))
	sys.exit(-1)
except Exception as e :
	print("Exception in GrangerCausality computation : \n" + str(e))
	sys.exit(-1)

# Displaying results :
print("Computing autoregressive model 'restricted' and 'unrestricted' via the 'Ordinary Least Squares' method\n")
print("According to",criterion,", the optimal number of lag estimated is :", results['optimal_lag'],"\n")
print("F_value =",results['F_value']," with p_value =",results['p_value'],"\n")

input("Push ENTER key to exit.")