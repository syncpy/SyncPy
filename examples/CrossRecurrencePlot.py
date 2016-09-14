"""
CrossRecurrencePlot example :
It computes the (cross) recurrence between two uni/multi-variate signals x and y(in DataFrame format).
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
print("This script computes ...\n")
print("**************************************************************")

""" Import wanted module with every parent packages """
import DataFrom2Persons.Multivariate.Continuous.Nonlinear.CrossRecurrencePlot as CrossRecurrencePlot


""" Define signals in pd.dataFrame format """

#Define parameters
N=1000
t=np.linspace(0,4*np.pi,N)

#Create signals
x=pd.DataFrame(3.0*np.sin(t+0.0001), np.arange(0,N))
y=pd.DataFrame(4.0*np.cos(t+0.0001), np.arange(0,N))


""" Define class attributes of the wanted method """
m=1                       # the mebedding dimension
t=1                       # the delay between data
e=0.1                     # the threshold for recurrence
distance= 'euclidean'     # the distance method to be used
standardization= True    # standardization of the time series to mean 0 and variance 1
plot = True             # plot of the (cross)recurrence matrix 


""" Instanciate the class with its attributes """
print("\n")

try : 
    c =CrossRecurrencePlot.CrossRecurrencePlot(m, t, e,distance, standardization)
except TypeError, err :
    print("TypeError in constructor : \n" + str(err))
    sys.exit(-1)
except ValueError, err :
    print("ValueError in constructor : \n" + str(err))
    sys.exit(-1)
except Exception, e :
    print("Exception in constructor : \n" + str(e))
    sys.exit(-1)


print("An instance the class is now created with the following parameters:\n" +
      "m = " + str(m) + "\n" +
      "t = " + str(t) + "\n" +
      "e = " + str(e) + "\n" +
      "distance = " + str(distance) + "\n" +
      "standardization = " + str(standardization) + "\n" +
      "plot = " + str(plot))


""" Compute the method and get the result """
print("\n")
print("Computing...")
try : 
    res = c.compute([x,y])
except TypeError, err :
    print("TypeError in computation : \n" + str(err))
    sys.exit(-1)
except ValueError, err :
    print("ValueError in computation : \n" + str(err))
    sys.exit(-1)
except Exception, e :
    print("Exception in computation : \n" + str(e))
    sys.exit(-1)


raw_input("Push ENTER key to exit.")
plt.close("all")




