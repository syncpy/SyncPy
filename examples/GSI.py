"""
GSI example :
It computes the generalised synchronization index (GSI) between two uni/multi-variate signals x and y(in DataFrame format).
GSI ranges in [0,1] where 0 means no synchronization and 1 perfect generalized synchronization.
"""

""" Import common python packages """
import sys
import os
import numpy as np              # Mathematical package
import pandas as pd             # Time serie package
import matplotlib.pyplot as plt # Plotting package
sys.path.insert(0, '../src/')   # To be able to import packages from parent directory 

import Methods.utils.Standardize

print("\n")
print("*****************************************************************************")
print("This script computes the generalised synchronization index (GSI) between \n" +
      "two uni/multi-variate signals x and y(in DataFrame format).\n" +
      "GSI ranges in [0,1] where 0 means no synchronization and 1 perfect generalized synchronization.")
print("*****************************************************************************")

""" Import wanted module  """
import Methods.DataFrom2Persons.Multivariate.Continuous.Nonlinear.GSI as GSI

""" Define signals in pd.dataFrame format """


#Define parameters
N=1016
t=np.array([np.linspace(0,4*np.pi,N), np.linspace(2,5*np.pi,N)]).T

#Create signals
x=pd.DataFrame(np.sin(t), np.arange(0,N))
y=pd.DataFrame(np.sin(3*t+10), np.arange(0,N))


"""Plot input signals"""
plt.ion()
f, axarr = plt.subplots(2, sharex=True)
axarr[0].set_title('Input signals')
axarr[0].set_xlabel('Samples')
axarr[1].set_xlabel('Samples')
axarr[0].plot(range(0,N), x.values, label="x")
axarr[1].plot(range(0,N), y.values, label="y", color='r')
axarr[0].legend(loc='best')
axarr[1].legend(loc='best')

""" Define parameters of the wanted method """
m=1                       # the mebedding dimension
t=1                       # the delay between data
rr=0.1                    # the threshold rate for recurrence


""" Call CrossRecurrencePlot utils method """
print("\n")

try:
    c = GSI.GSI(m, t, rr)
except TypeError as err :
    print("TypeError in GSI : \n" + str(err))
    sys.exit(-1)
except ValueError as err :
    print("ValueError in GSI : \n" + str(err))
    sys.exit(-1)
except Exception as e :
    print("Exception in GSI : \n" + str(e))
    sys.exit(-1)



print("An instance of the class is now created with the following parameters:\n" +
      "m = " + str(m) + "\n" +
      "t = " + str(t) + "\n" +
      "rr = " + str(rr))


""" Compute the method and get the result """
print("\n")
print("Computing...")


try : 
    res = c.compute([x, y])
except TypeError as err:
    print("TypeError in GSI computation : \n" + str(err))
    sys.exit(-1)
except ValueError as err:
    print("ValueError in GSI computation : \n" + str(err))
    sys.exit(-1)
except Exception as e:
    print("Exception in GSI computation : \n" + str(e))
    sys.exit(-1)


""" Display results """
print("\n")
print("****************************************\n")
print('GSI complete result:\n')
print("****************************************\n")
print("GSI:")
print(res)
print("\n")

input("Push ENTER key to exit.")
plt.close("all")




