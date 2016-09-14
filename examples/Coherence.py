"""
Coherence example :
It computes coherence fucntion between two monovariate signals (in DataFrame format) x and y.
"""

""" Import common python packages """

""" Import common python packages """
import sys
import os
import numpy as np          # Mathematical package
import pandas as pd         # Time serie package
import matplotlib.pyplot as plt # Plotting package
sys.path.insert(0, '../src/')   # To be able to import packages from parent directory 

print("\n")
print("****************************************************************************************")
print("This script computes the coherence of two continuous monovariate signals. \n" +
      "First input is a sum among a sinewave of 100 Hz frequency,  a cosinewave \n" +
      "of 200 Hz frequency and unformly distributed random noise. The second one\n" +
      "is a sub-multiple of the first one.")
print("****************************************************************************************")

""" Import wanted module with every parent packages """

import DataFrom2Persons.Monovariate.Continuous.Linear.Coherence as Coherence


""" Import Utils modules """
from utils import Standardize
from utils.ExtractSignal import ExtractSignalFromCSV


""" Define signals in pd.dataFrame format """
Fs=1000.0 # sampling frequency (Hz)

t=np.arange(0,1-1.0/Fs,1.0/Fs) #number or samples

# Create signals
x = pd.DataFrame({'X':np.cos(2*np.pi*100*t)+np.sin(2*np.pi*200*t)+np.random.randn(t.size)})
y = pd.DataFrame({'Y':0.5*np.cos(2*np.pi*100*t-np.pi/4)+0.35*np.sin(2*np.pi*200*t-np.pi/2)+0.5*np.random.randn(t.size)})


'''
"""OR"""
""" Import signals from a .csv file """
#Data from files
filename = 'data_examples/2Persons_Monovariate_Continuous_data.csv'

x = ExtractSignalFromCSV(filename, columns = ['x1'])
y = ExtractSignalFromCSV(filename, columns = ['x2'])
t=np.arange(0,x.shape[0])
'''


""" Plot input signals """
plt.ion()
f, axarr = plt.subplots(2, sharex=True)
axarr[0].set_title('Input signals')
axarr[0].set_xlabel('Samples')
axarr[1].set_xlabel('Samples')
axarr[0].plot(t, x, label="x")
axarr[1].plot(t, y, label="y", color='r')
axarr[0].legend(loc='best')
axarr[1].legend(loc='best')

""" Define class attributes of the wanted method """
Fs=1000.0       # sampling frequency (Hz)
NFFT = 100      # length of each epoch
detrend = 0     # remove constant detrending
noverlap = 80   # number of points of overlap between epochs
plot = True     # plot of the coherence function

""" Instanciate the class with its attributes """
print("\n")

try : 
    c = Coherence.Coherence(Fs, NFFT, detrend, noverlap, plot=True)
except TypeError, err :
    print("TypeError in Coherence constructor : \n" + str(err))
    sys.exit(-1)
except ValueError, err :
    print("ValueError in Coherence constructor : \n" + str(err))
    sys.exit(-1)
except Exception, e :
    print("Exception in Coherence constructor : \n" + str(e))
    sys.exit(-1)


print("An instance the class is now created with the following parameters:\n" +
      "NFFT = " + str(NFFT) + "\n" +
      "detrend = " + str(detrend) + "\n" +
      "noverlap= " + str(noverlap) + "\n" +
      "plot = " + str(plot))

""" Compute the method and get the result """
print("\n")
print("Computing...")

try : 
    res = c.compute(x,y)
except TypeError, err :
    print("TypeError in Coherence computation : \n" + str(err))
    sys.exit(-1)
except ValueError, err :
    print("ValueError in Coherence computation : \n" + str(err))
    sys.exit(-1)
except Exception, e :
    print("Exception in Coherence computation : \n" + str(e))
    sys.exit(-1)

""" Display result """
print("\n")
print("**************************************** \n")
print('Coherence complete result :')
print("****************************************\n")
print(res['Coherence'])
print(res['Frequency'])

raw_input("Push ENTER key to exit.")

