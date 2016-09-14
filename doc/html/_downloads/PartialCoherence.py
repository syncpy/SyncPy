"""
PartialCoherence example :
Compute Partial Coherence for multiple monovariate signals (orgainized as a list).
"""

""" Import common python packages """
import sys
import os
import numpy as np              # Mathematical package
import pandas as pd             # Time serie package
import matplotlib.pyplot as plt # Plotting package
sys.path.insert(0, '../src')       # To be able to import from parent directory

print("\n")
print("***********************************************************************")
print("This script computes Partial Coherence for multiple monovariate signals \n" + 
      "(organized as a list) \n")
print("***********************************************************************")

""" Import wanted module with every parent packages """
import DataFromManyPersons.Monovariate.Continuous.Linear.PartialCoherence as PartialCoherence
from utils.ExtractSignal import ExtractSignalFromCSV
from utils.ExtractSignal import ExtractSignalFromMAT

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
filename = 'data_examples/2Persons_Multivariate_Continous_data.csv'
x = ExtractSignalFromCSV(filename, columns = ['Upper body mq'])
y = ExtractSignalFromCSV(filename, columns = ['Upper body mq.1'])
z = ExtractSignalFromCSV(filename, columns = ['Left Hand mq'])
a = ExtractSignalFromCSV(filename, columns = ['Left Hand mq.1'])

'''
"""OR"""
""" Import signal from a .mat file """
filename = 'data_examples/data_example_MAT.mat'
x = ExtractSignalFromMAT(filename, columns_index =[0,2], columns_wanted_names=['Time', 'GlobalBodyActivity0'])
y = ExtractSignalFromMAT(filename, columns_index =[10], columns_wanted_names=['GlobalBodyActivity1'])
'''

signals = [x,y,z,a]

N = signals[0].shape[0]
n = np.arange(0,N) 

""" Plot input signals """
plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111)
ax.grid(True)
ax.set_xlabel('Samples')
ax.set_title('Input signals')
for i in range(len(signals)) :
    ax.plot(n, signals[i].iloc[:,0], label=signals[i].columns[0])
plt.legend(bbox_transform=plt.gcf().transFigure)

""" Define class attributes of the wanted method """
fs = 1.0        # sampling frequency of the input DataFrame in Hz
NFFT = 256      # length of each epoch
detrend = 1     # specifies which kind of detrending should be computed on data. 0 stands for constant detrending; 1 stands for linear detrending
noverlap = 0    # number of points to overlap between epochs

""" Instanciate the class with its attributes """
print("\n")
try : 
    pc = PartialCoherence.PartialCoherence(fs, NFFT, detrend, noverlap)
except TypeError, err :
    print("TypeError in PartialCoherence constructor : \n" + str(err))
    sys.exit(-1)
except ValueError, err :
    print("ValueError in PartialCoherence constructor : \n" + str(err))
    sys.exit(-1)
except Exception, e :
    print("Exception in PartialCoherence constructor : \n" + str(e))
    sys.exit(-1)
    
print("An instance the class is now created with the following parameters:\n" +
      "fs = " + str(fs) + "\n" +
      "NFFT = " + str(NFFT) + "\n" +
      "detrend = " + str(detrend) + "\n" +
      "noverlap = " + str(noverlap) + "\n"
      )

""" Compute the method and get the result """
print("\n")
print("Computing...")

try : 
    partial_coherence = pc.compute(*signals)
except TypeError, err :
    print("TypeError in PartialCoherence computation : \n" + str(err))
    sys.exit(-1)
except ValueError, err :
    print("ValueError in PartialCoherence computation : \n" + str(err))
    sys.exit(-1)
except Exception, e :
    print("Exception in PartialCoherence computation : \n" + str(e))
    sys.exit(-1)

""" Display result """
print("\n")
print('PartialCoherence computed for theses signals indexes :')
print("\n")

for i in partial_coherence.keys():
    print(str(sorted(partial_coherence[i].keys())) + " given " + str(i)+ ", ")
    print("\n")

raw_input("Push ENTER key to exit.")
