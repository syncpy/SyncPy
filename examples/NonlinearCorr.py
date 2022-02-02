"""
Nonlinear Correlation example :
It computes the nonparametric nonlinear regression coefficient h2 describing the dependency
between two signals (in DataFrame format) x and y in a most general way
"""

""" Import common python packages """
import sys
import os
import numpy as np          # Mathematical package
import pandas as pd         # Time serie package
import matplotlib.pyplot as plt # Plotting package
sys.path.insert(0, '../src/')   # To be able to import packages from parent directory
sys.path.insert(0, '../src/Methods')

print("\n")
print("**************************************************************")
print("This script computes the nonlinear correlation coefficient \n"+
      "of two continouos monovariate signals \n")
print("**************************************************************")

""" Import wanted module with every parent packages """
import DataFrom2Persons.Univariate.Continuous.Nonlinear.NonlinearCorr as NonlinearCorr
from utils.ExtractSignal import ExtractSignalFromCSV
from DataFrom2Persons.Univariate.Continuous.Linear import Correlation



""" Define signals in pd.dataFrame format """

#Define parameters
N=1000                     # number of samples
t=np.linspace(0,4*np.pi,N) # number of samples


#Create signals
x=pd.DataFrame({'X':3.0*np.sin(t+0.0001)}, np.arange(0,N))
y=x**2

'''
"""OR"""
""" Import signals from a .csv file """
#Data from files
filename = 'data_examples/2Persons_Monovariate_Continuous_data.csv'

x = ExtractSignalFromCSV(filename, columns = ['x1'])
y = ExtractSignalFromCSV(filename, columns = ['x2'])
'''


""" Plot input signals"""

plt.ion()
f, axarr = plt.subplots(2, sharex=True)
axarr[0].set_title('Input signals')
axarr[0].set_xlabel('Samples')
axarr[1].set_xlabel('Samples')
axarr[0].plot(t, x.values, label="x")
axarr[1].plot(t, y.values, label="y", color='r')
axarr[0].legend(loc='best')
axarr[1].legend(loc='best')



""" Define class attributes of the wanted method """
nbins=100   # number of bins in which the time series is divided into


""" Instanciate the class with its attributes """
print("\n")

try : 
    c = NonlinearCorr.NonlinearCorr(nbins)
except TypeError as err :
    print("TypeError in NonlinearCorr constructor : \n" + str(err))
    sys.exit(-1)
except ValueError as err :
    print("ValueError in NonlinearCorr constructor : \n" + str(err))
    sys.exit(-1)
except Exception as e :
    print("Exception in NonlinearCorr constructor : \n" + str(e))
    sys.exit(-1)


print("An instance the class is now created with the following parameters:\n" +
      "number of bin = " + str(nbins))

""" Compute the method and get the result """
print("\n")
print("Computing...")

try:
    res = c.compute([x, y])
except TypeError as err:
    print("TypeError in NonlinearCorr computation : \n" + str(err))
    sys.exit(-1)
except ValueError as err:
    print("ValueError in NonlinearCorr computation : \n" + str(err))
    sys.exit(-1)
except Exception as e:
    print("Exception in NonlinearCorr computation : \n" + str(e))
    sys.exit(-1)

""" Display result """
print("\n")
print("**************************************** \n")
print('NonlinearCorr complete result :\n')
print("****************************************\n")
print(res['h2 coefficient'])

""" Computing the linear correlation coeffcient"""
print("\n")
print ("Computing the linear correlation coefficient:")
print("\n")
""" Define class attributes of the wanted method """

tau_max = 999                       # the maximum lag at which correlation should be computed (in samples)
plot=False                          # plot of the correlation fucntion
standardization = True              # standardization of the time series to mean 0 and variance 1
corr_tau_max = False                # return of the maximum of correlation and its lag
corr_coeff = True                   # computation of the correlation coefficient (Pearson's version)
scale= False                        # scale factor to have correlaton in [-1,1]

""" Instanciate the class with its attributes """
print("\n")

try:
    c = Correlation.Correlation(tau_max, plot, standardization, corr_tau_max, corr_coeff, scale)
except TypeError as err :
    print("TypeError in Correlation constructor : \n" + str(err))
    sys.exit(-1)
except ValueError as err :
    print("ValueError in Correlation constructor : \n" + str(err))
    sys.exit(-1)
except Exception as e:
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
    res = c.compute([x, y])
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
print("\n")
print("**************************************** \n")
print('Correlation complete result :\n')
print("****************************************\n")
print("Pearson's correlation coefficient {}:".format(res['corr_coeff']))
print("\n")

print("As expected the two coefficient provide different results, \n" +
       "that is high value of nonlinear correlation coefficient and \n" +
       "low value of linear correlation coefficient.")


input("Push ENTER key to exit.")
plt.close("all")




