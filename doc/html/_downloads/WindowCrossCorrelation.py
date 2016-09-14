"""
WindowCrossCorrelation example :
Computes the window cross correlation between times series (in DataFrame format) x and y
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
print("This script computes the windowed cross-correlation between two monovariate time series \n" +
      "expressed as Python Pandas DataFrame.")
print("*************************************************************************************")

""" Import wanted module with every parent packages """
import DataFrom2Persons.Monovariate.Continuous.Linear.WindowCrossCorrelation as WindowCrossCorrelation

""" Import Utils modules """
from utils.ExtractSignal import ExtractSignalFromCSV
from utils.ExtractSignal import ExtractSignalFromMAT
from utils.ResampleAndInterpolate import ResampleAndInterpolate

'''
""" Define signals in pd.dataFrame format """
# preparing the input time series
N = 20             # number of samples
f = 1.0             # sinewave frequency (Hz)
Fs = 200            # sampling frequency (Hz)
n = np.arange(0,N)  # number of samples
# input time series
x = pd.DataFrame({'X':np.sin(2*3.14*f*n/Fs)})
y = pd.DataFrame({'Y':np.sin(2*3.14*2*f*n/Fs)})
'''

"""OR"""
""" Import signal from a .csv file """
filename = 'data_examples/2Persons_Monovariate_Continuous_data_2.csv'
x = ExtractSignalFromCSV(filename, columns = ['x'], unit = 's')
y = ExtractSignalFromCSV(filename, columns = ['y'], unit = 's')

# Resample and Interpolate data to have constant frequency
x = ResampleAndInterpolate(x, rule='500ms', limit=5)
y = ResampleAndInterpolate(y, rule='500ms', limit=5)

'''
"""OR"""
""" Import signal from a .mat file """
filename = 'data_examples/data_example_MAT.mat'
x = ExtractSignalFromMAT(filename, columns_index =[0,2], columns_wanted_names=['Time', 'GlobalBodyActivity0'])
y = ExtractSignalFromMAT(filename, columns_index =[10], columns_wanted_names=['GlobalBodyActivity1'])
'''

""" Plot input signals """
n = [float(i)/2 for i in range(x.size)] # create x axis values
plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111)
ax.grid(True)
ax.set_xlabel('Samples')
ax.set_title('Input signals')
ax.plot(n, x, label=x.columns[0])
ax.plot(n, y, label=y.columns[0])
plt.legend(bbox_transform=plt.gcf().transFigure)

""" Define class attributes of the wanted method """
tau_max = 5 * 2     # the maximum lag at which correlation should be computed. It is in the range [0; (lx+ly-1)/2] (in samples)
window = 5 * 10     # length of the windowed signals (in samples)
window_inc = 5 * 2  # amount of time elapsed between two windows (in samples)
tau_inc= 1          # amount of time elapsed between two cross-correlation (in samples)
plot = True         # if True the plot of correlation function is returned. Default: False
ele_per_sec = 5     # number of element in one second

""" Instanciate the class with its attributes """
print("\n")
try : 
    corr = WindowCrossCorrelation.WindowCrossCorrelation(tau_max, window, window_inc, tau_inc, plot, ele_per_sec)
except TypeError, err :
    print("TypeError in WindowCrossCorrelation constructor : \n" + str(err))
    sys.exit(-1)
except ValueError, err :
    print("ValueError in WindowCrossCorrelation constructor : \n" + str(err))
    sys.exit(-1)
except Exception, e :
    print("Exception in WindowCrossCorrelation constructor : \n" + str(e))
    sys.exit(-1)
    
print("An instance the class is now created with the following parameters:\n" +
      "tau max = " + str(tau_max) + "\n" +
      "window length = " + str(window) + "\n" +
      "window increment = " + str(window_inc) + "\n" +
      "tau increment = " + str(window_inc) + "\n" +
      "number of element per second = " + str(ele_per_sec) + "\n" +
      "plot result = " + str(plot))

""" Compute the method and get the result """
print("\n")
print("Computing...")

try : 
    cross_corr = corr.compute(x,y)
except TypeError, err :
    print("TypeError in WindowCrossCorrelation computation : \n" + str(err))
    sys.exit(-1)
except ValueError, err :
    print("ValueError in WindowCrossCorrelation computation : \n" + str(err))
    sys.exit(-1)
except Exception, e :
    print("Exception in WindowCrossCorrelation computation : \n" + str(e))
    sys.exit(-1)

""" Display result """
print("\n")
print("********************************* \n")
print('Window Cross correlation result :')
print("********************************* \n")
print(cross_corr)

raw_input("Push ENTER key to exit.")
