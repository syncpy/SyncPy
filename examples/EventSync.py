"""
Event Synchronisation example:
It computes Event Synchornisation (ES) and time delay patterns between two monovariate signals x and y
(in pandas DataFrame format) in which events can be identified using Quian Quiroga's method.
"""

""" Import common python packages """
import sys
import os
import numpy as np      # Mathematical package
import pandas as pd     # Time serie package
import matplotlib.pyplot as plt # Plotting package
sys.path.insert(0, '../src/')   # To be able to import packages from parent directory 

print ("\n")
print("******************************************************************************************")
print("This scripts compute the synchronisation and time delay pattern between two monovariate\n"+
      "signals (in pandas DataFrame format) showing events.")
print("******************************************************************************************")

""" Import wanted module with every parent packages """
import DataFrom2Persons.Monovariate.Categorical.Nonlinear.EventSync as EventSync

""" Import Utils modules """
from utils.ExtractSignal import ExtractSignalFromCSV

'''
""" Define input signals in pd.dataFrame format """

#input signals
print("\n")
print("Generating the input signals...")

N=26

x = pd.DataFrame([0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0],np.arange(0,N))
y = pd.DataFrame([0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0],np.arange(0,N))

'''
"""OR"""
""" Import signals from a .csv file """
#Data from files
filename = 'data_examples/2Persons_Monovariate_Categorical_data.csv'


x = ExtractSignalFromCSV(filename, columns = ['0'])
y = ExtractSignalFromCSV(filename, columns = ['1'])



s=np.arange(0,x.shape[0])

plt.ion()
f, axarr = plt.subplots(2, sharex=True)
axarr[0].set_title('Input signals')
axarr[0].set_xlabel('Samples')
axarr[1].set_xlabel('Samples')
axarr[0].stem(s,x,label="x")
axarr[1].stem(s, y, label="y")
axarr[0].legend(loc='best')
axarr[1].legend(loc='best')


""" Define class attributes of the wanted method """
atype = 'tot'                      # algorithm to be used to compute Q and q
tau = 1                            # algorithm is used to estimates the delay
lag_tau = 3                        # number of samples will be used as delay
window = 1                         # size of the window to compute Q and q
plot= False                        # plot of Q and q

""" Instanciate the class with its attributes """
print("\n")

try : 
    c=EventSync.EventSync(atype, tau, lag_tau, window, plot)
except TypeError, err :
    print("TypeError in EventSync constructor : \n" + str(err))
    sys.exit(-1)
except ValueError, err :
    print("ValueError in EventSync constructor : \n" + str(err))
    sys.exit(-1)
except Exception, e :
    print("Exception in EventSync constructor : \n" + str(e))
    sys.exit(-1)

print("An instance the class is now created with the following parameters:\n" +
      "type = " + str(atype) + "\n" +
      "tau = " + str(tau) + "\n" +
      "lag_tau = " + str(lag_tau) + "\n" +
      "window= " + str(window) + "\n" +
      "plot = " + str(plot))


""" Compute the method and get the result """
print("\n")
print("Computing...")

try : 
    res= c.compute(x, y)
except TypeError, err :
    print("TypeError in EventSync computation : \n" + str(err))
    sys.exit(-1)
except ValueError, err :
    print("ValueError in EventSync computation : \n" + str(err))
    sys.exit(-1)
except Exception, e :
    print("Exception in EventSync computation : \n" + str(e))
    sys.exit(-1)

""" Display result """
print("\n")
print("**************************************** \n")
print('EventSync complete result :')
print("****************************************\n")

print("Q:")
print(res['Q'])
print("q:")
print(res['q'])

""" OTHER EXAMPLE WITH TSL TYPE """
print("\n")
print("*************************************************** \n")
print("*************************************************** \n")

""" Define class attributes of the wanted method """
atype = 'tsl'                      # algorithm to be used to compute Q and q
tau = 1                            # algorithm is used to estimates the delay
lag_tau = 3                        # number of samples will be used as delay
window = 30                         # size of the window to compute Q and q
plot= True                         # plot of Q and q

""" Instanciate the class with its attributes """
print("\n")

try : 
    c=EventSync.EventSync(atype, tau, lag_tau, window, plot)
except TypeError, err :
    print("TypeError in EventSync constructor : \n" + str(err))
    sys.exit(-1)
except ValueError, err :
    print("ValueError in EventSync constructor : \n" + str(err))
    sys.exit(-1)
except Exception, e :
    print("Exception in EventSync constructor : \n" + str(e))
    sys.exit(-1)


print("An instance the class is now created with the following parameters:\n" +
      "type = " + str(atype) + "\n" +
      "tau = " + str(tau) + "\n" +
      "lag_tau = " + str(lag_tau) + "\n" +
      "window= " + str(window) + "\n" +
      "plot = " + str(plot))

""" Compute the method and get the result """

print("\n")
print("Computing...")

try : 
    res= c.compute(x, y)
except TypeError, err :
    print("TypeError in EventSync computation : \n" + str(err))
    sys.exit(-1)
except ValueError, err :
    print("ValueError in EventSync computation : \n" + str(err))
    sys.exit(-1)
except Exception, e :
    print("Exception in EventSync computation : \n" + str(e))
    sys.exit(-1)

""" Display result """
print("\n")
print("**************************************** \n")
print('EventSync complete result :')
print("****************************************\n")

print("Q:")
print(res['Q'])
print("q:")
print(res['q'])

raw_input("Push ENTER key to exit.")

