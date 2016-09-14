"""
WindowMututalInformation example :
Computes the windowed mutual information between times series (in DataFrame format) x and y
"""

""" Import common python packages """
import sys
import os
import numpy as np                  # Mathematical package
import pandas as pd                 # Time serie package
import matplotlib.pyplot as plt     # Plotting package
sys.path.insert(0, '../src/')       # To be able to import from parent directory

print("\n")
print("***************************************************************************************")
print("This script computes the windowed mutual information between two monovariate time series \n" +
      "expressed as Python Pandas DataFrame.")
print("***************************************************************************************")

""" Import wanted module with every parent packages """
import DataFrom2Persons.Univariate.Continuous.Nonlinear.WindowMutualInformation as WindowMutualInformation


""" Define signals in pd.dataFrame format """
# Create signals
n = 100
x = pd.DataFrame(1.0*np.random.rand(n,1), range(0,n))
y = pd.DataFrame(1.0*np.random.rand(n,1), range(0,n))

""" Plot input signals """
n = [float(i) for i in range(x.size)] # create x axis values
plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111)
ax.grid(True)
ax.set_xlabel('Time (s)')
ax.set_ylabel('signals')
ax.set_title('Input signals')
ax.plot(n , y, label='y')
ax.plot(n , x, label='x')
plt.legend(bbox_transform=plt.gcf().transFigure)

""" Define class attributes of the wanted method """
n_neighbours = 5         # the number of the nearest neighbours to be used
my_type = 1              # the type of estimators
var_res = True           # rescaling of the time series
noise = True             # adding random noise to the time series

tau_max = 10             # the maximum lag at which correlation should be computed. It is in the range [0; (lx+ly-1)/2] (in samples)
window = 10              # length of the windowed signals (in samples)
window_inc =  1          # amount of time elapsed between two windows (in samples)
tau_inc= 1               # amount of time elapsed between two cross-correlation (in samples)
plot = True              # if True the plot of correlation function is returned. Default: False


""" Instanciate the class with its attributes """
print("\n")
try : 
    wmi = WindowMutualInformation.WindowMutualInformation(n_neighbours, my_type, var_res,noise, tau_max, window, window_inc, tau_inc, plot)
except TypeError, err :
    print("TypeError in WindowMutualInformation constructor : \n" + str(err))
    sys.exit(-1)
except ValueError, err :
    print("ValueError in WindowMutualInformation constructor : \n" + str(err))
    sys.exit(-1)
except Exception, e :
    print("Exception in WindowMutualInformation constructor : \n" + str(e))
    sys.exit(-1)
    
print("An instance the class is now created with the following parameters:\n" +
      "n_neighbours = " + str(n_neighbours) + "\n" +
      "my_type = " + str(my_type) + "\n" +
      "var_res = " + str(var_res) + "\n" +
      "noise = " + str(noise) + "\n" +
      "tau max = " + str(tau_max) + "\n" +
      "window length = " + str(window) + "\n" +
      "window increment = " + str(window_inc) + "\n" +
      "tau increment = " + str(window_inc) + "\n" +
      "plot result = " + str(plot))

print("\n")

""" Compute the method and get the result """
print("\n")
print("Computing...")

try : 
    win_MI = wmi.compute(x,y)
except TypeError, err :
    print("TypeError in WindowMutualInformation computation : \n" + str(err))
    sys.exit(-1)
except ValueError, err :
    print("ValueError in WindowMutualInformation computation : \n" + str(err))
    sys.exit(-1)
except Exception, e :
    print("Exception in WindowMutualInformation computation : \n" + str(e))
    sys.exit(-1)


""" Display result """
print("\n")
print("********************************* \n")
print('Window Mutual Information result :')
print("********************************* \n")
'''print(win_MI)'''

raw_input("Push ENTER key to exit.")
