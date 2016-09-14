"""
PeakPicking example :
Computes peak picking algorithm with window cross correlation results
"""

""" Import common python packages """
import sys
import os
import numpy as np          # Mathematical package
import pandas as pd         # Time serie package
import matplotlib.pyplot as plt # Plotting package
sys.path.insert(0, '../src/')   # To be able to import from parent directory 

print("\n")
print("*****************************************************************************")
print("This script computes the peak picking selection of a cross correlation matrix \n")
print("*****************************************************************************")

""" Import wanted modules with every parent packages """
import DataFrom2Persons.Univariate.Continuous.Linear.WindowCrossCorrelation as WindowCrossCorrelation


""" Import Utils modules """
from utils.ExtractSignal import ExtractSignalFromCSV
from utils.ExtractSignal import ExtractSignalFromMAT
from utils.ResampleAndInterpolate import ResampleAndInterpolate
from utils import PeakPicking

'''
""" Define signals in pd.dataFrame format """
# preparing the input signals
N = 20             # number of samples
f = 1.0             # sinewave frequency (Hz)
Fs = 200            # sampling frequency (Hz)
n = np.arange(0,N)  # number of samples
# input signals
x = pd.DataFrame({'X':np.sin(2*3.14*f*n/Fs)})
y = pd.DataFrame({'Y':np.sin(2*3.14*2*f*n/Fs)})
'''

"""OR"""
""" Import signals from a .csv file """
filename = 'data_examples/2Persons_Univariate_Continuous_data_2.csv'
x = ExtractSignalFromCSV(filename, columns = ['x'], unit = 's')
y = ExtractSignalFromCSV(filename, columns = ['y'], unit = 's')

# Resample and Interpolate data to have constant frequency
x = ResampleAndInterpolate(x, rule='500ms', limit=5)
y = ResampleAndInterpolate(y, rule='500ms', limit=5)

'''
"""OR"""
""" Import signals from a .mat file """
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

""" Compute the method and get the result """
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

""" Get peaks of current result """
tau_max = 10        # the maximum lag at which correlation should be computed. It is in the range [0; (lx+ly-1)/2] (in samples)
tau_inc= 1          # amount of time elapsed between two cross-correlation (in samples)
threshold = 0.5     # minimal correlation magnitude acceptable for a peak (between -1 and 1)
lookahead = 2       # distance to look ahead from a peak candidate to determine if it is the actual peak. Default: 200
delta = 0           # this specifies a minimum difference between a peak and the following points, before a peak may be considered a peak. Default: 0
ele_per_sec = 2     # number of element in one second
plot = False        #if True the plot of peakpicking function is returned. Default: False
plot_on_mat =False  # if True the plot of peakpicking + correlation matrix function is returned. Default: False
sorted_peak = False # if True the peaks found will be organized by type of Lag and Magnitude (positive or negative). Default: False

# Compute peakPicking util method
try : 
    peak_res = PeakPicking.PeakPicking(cross_corr, tau_max, tau_inc, threshold, lookahead, delta, ele_per_sec, plot, plot_on_mat, sorted_peak)
except TypeError, err :
    print("TypeError in PeakPicking method : \n" + str(err))
    sys.exit(-1)
except ValueError, err :
    print("ValueError in PeakPicking method : \n" + str(err))
    sys.exit(-1)
except Exception, e :
    print("Exception in PeakPicking method : \n" + str(e))
    sys.exit(-1)

# Get figure 
try : 
    peak_figure = PeakPicking.PeakPicking_plot(peak_res, cross_corr, tau_max, ele_per_sec, plot_on_mat = True)
except TypeError, err :
    print("TypeError in PeakPicking computation : \n" + str(err))
    sys.exit(-1)
except ValueError, err :
    print("ValueError in PeakPicking computation : \n" + str(err))
    sys.exit(-1)
except Exception, e :
    print("Exception in PeakPicking computation : \n" + str(e))
    sys.exit(-1)

# Get stats 
peak_sorted = PeakPicking.PeakPicking_sortResult(peak_res)# Get statistics

""" Display result """
print("\n")
print("********************* \n")
print('Peak Picking result : ')
print("********************* \n")
print(peak_sorted)

raw_input("Push ENTER key to exit.")