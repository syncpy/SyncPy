"""
S_Estimator example :
Compute Synchronization Indexes for multiple monovariate signals (orgainized as a list).
"""

""" Import common python packages """
import sys
import os
import numpy as np              # Mathematical package
import pandas as pd             # Time serie package
import matplotlib.pyplot as plt # Plotting package
sys.path.insert(0, '../src/')       # To be able to import from parent directory
sys.path.insert(0, '../src/Methods')

print("\n")
print("*************************************************************************************")
print("This script computes Synchronization indexes for multiple monovariate signals \n" + 
      "(orgainized as a list) \n")
print("*************************************************************************************")

""" Import wanted module with every parent packages """
import Methods.DataFromManyPersons.Univariate.Continuous.Linear.S_Estimator as S_Estimator
from utils.ExtractSignal import ExtractSignalFromCSV
from utils.ExtractSignal import ExtractSignalFromMAT
from utils.Standardize import Standardize

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
filename = 'data_examples/2Persons_Multivariate_Continous_data.csv'
x = ExtractSignalFromCSV(filename, columns = ['Upper body mq'])
y = ExtractSignalFromCSV(filename, columns = ['Upper body mq.1'])

'''
"""OR"""
""" Import signals from a .mat file """
filename = 'data_examples/data_example_MAT.mat'
x = ExtractSignalFromMAT(filename, columns_index =[0,2], columns_wanted_names=['Time', 'GlobalBodyActivity0'])
y = ExtractSignalFromMAT(filename, columns_index =[10], columns_wanted_names=['GlobalBodyActivity1'])
'''

signals = [x,y]

N = signals[0].shape[0]
n = np.arange(0,N) 

""" Plot standardized input signals """
Signals = signals
plt.ion()

nrows = len(Signals)
figure, ax = plt.subplots(nrows, sharex=True)

idx = 0 
for col in  range(len(Signals)) :
    ax[idx].grid(True) # Display a grid
    ax[idx].set_title('Standardized signal for : ' + Signals[col].columns[0] + ' variable')
    ax[idx].plot(n, Signals[col].iloc[:,0])
    idx += 1
    
ax[idx-1].set_xlabel('Samples')

""" Define class attributes of the wanted method """
surr_nb_iter = 100
plot_surrogate = True 

""" Instanciate the class with its attributes """
print("\n")
try : 
    s_estimator = S_Estimator.S_Estimator(surr_nb_iter, plot_surrogate)
except TypeError, err :
    print("TypeError in S_Estimator constructor : \n" + str(err))
    sys.exit(-1)
except ValueError, err :
    print("ValueError in S_Estimator constructor : \n" + str(err))
    sys.exit(-1)
except Exception, e :
    print("Exception in S_Estimator constructor : \n" + str(e))
    sys.exit(-1)
    
print("An instance the class is now created with the following parameters:\n" +
      "surr_nb_iter = " + str(surr_nb_iter) + "\n"
      )

""" Compute the method and get the result """
print("\n")
print("Computing...")

try : 
    estimators = s_estimator.compute(signals)
except TypeError, err :
    print("TypeError in S_Estimator computation : \n" + str(err))
    sys.exit(-1)
except ValueError, err :
    print("ValueError in S_Estimator computation : \n" + str(err))
    sys.exit(-1)
except Exception, e :
    print("Exception in S_Estimator computation : \n" + str(e))
    sys.exit(-1)

""" Display result """
print("\n")
print('S_Estimator result :')
print("\n")

for i in estimators.keys():
    print(i + " : " + str(estimators[i]))
print("\n")

raw_input("Push ENTER key to exit.")
