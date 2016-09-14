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
sys.path.insert(0, '../src/')   # To be able to import packages from parent directory 

print ("\n")
print("***********************************************************************************************************************")
print("This scripts computes the correlation between two monovariate signals."
       "First input is a sinewave of 1 Hz frequency, the second one\n is the sum of this sinewave"
       "with a gaussian random process having zero mean and unitary\n variance.")
print("************************************************************************************************************************")

""" Import wanted module with every parent packages """
import DataFrom2Persons.Univariate.Continuous.Linear.Correlation as Correlation

""" Import Utils modules """
from utils import Standardize
from utils.ExtractSignal import ExtractSignalFromCSV


""" Define signals in pd.dataFrame format """

#Define parameters
N=1024 # number of samples
f=1.0  # sinewave frequency (Hz)
Fs=200 # sampling frequency (Hz)

n=np.arange(0,N)#number of samples

# Create signals
x = pd.DataFrame({'X':np.sin(2*3.14*f*n/Fs)}, np.arange(0,N))
y = pd.DataFrame({'Y':np.sin(2*3.14*f*n/Fs)+10*np.random.randn(1,N)[0]},np.arange(0,N))

'''
"""OR"""
""" Import signals from a .csv file """
#Data from files
filename = 'data_examples/2Persons_Monovariate_Continuous_data.csv'

x = ExtractSignalFromCSV(filename, columns = ['x1'])
y = ExtractSignalFromCSV(filename, columns = ['x2'])
n=np.arange(0,x.shape[0])
'''



"""Plot input signals"""
plt.ion()
f, axarr = plt.subplots(2, sharex=True)
axarr[0].set_title('Input signals')
axarr[0].set_xlabel('Samples')
axarr[1].set_xlabel('Samples')

axarr[0].plot(n, x, label="x")
axarr[1].plot(n, y, label="y", color='r')
axarr[0].legend(loc='best')
axarr[1].legend(loc='best')



""" Define class attributes of the wanted method """

tau_max = 999                       # the maximum lag at which correlation should be computed (in samples)
plot=True                           # plot of the correlation fucntion
standardization = True              # standardization of the time series to mean 0 and variance 1
corr_tau_max = True                 # return of the maximum of correlation and its lag
corr_coeff = True                   # computation of the correlation coefficient (Pearson's version)
scale=True                          # scale factor to have correlaton in [-1,1]

""" Instanciate the class with its attributes """
print("\n")

try : 
    c=Correlation.Correlation(tau_max, plot, standardization, corr_tau_max, corr_coeff, scale)
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
      "tau max = " + str(tau_max) + "\n" +
      "plot = " + str(plot) + "\n" +
      "standardization= " + str(standardization) + "\n" +
      "corr_tau_max = " + str(corr_tau_max) + "\n" +
      "corr_coeff =" + str(corr_coeff) +"\n" +
      "scale =" + str(scale))

""" Compute the method and get the result """
print("\n")
print("Computing...")

try : 
    res= c.compute(x, y)
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
print("\n")
print("**************************************** \n")
print('Correlation complete result :')
print("****************************************\n")
print("Correlation function array:")
print(res['corr_funct'])
print("Maximum value of the correlation %f and lag (in samples) %d:" %(res['max_corr'],res['t_max']))
print("Pearson's correlation coefficient %f:" %(res['corr_coeff']))



raw_input("Push ENTER key to exit.")
plt.close("all")
