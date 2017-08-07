"""
Omega_Complexity example :
Compute Omega_Complexity for multiple monovariate signals (orgainized as a list).
"""

""" Import common python packages """
import sys
import os
import numpy as np              # Mathematical package
import pandas as pd             # Time serie package
import matplotlib.pyplot as plt # Plotting package
sys.path.insert(0, '../src/')       # To be able to import from parent directory

print("\n")
print("**********************************************************************")
print("This script computes Omega_Complexity for multiple monovariate signals \n" + 
      "(orgainized as a list) \n")
print("**********************************************************************")

""" Import wanted module with every parent packages """
import Methods.DataFromManyPersons.Univariate.Continuous.Linear.Omega_Complexity as Omega_Complexity
from Methods.utils.ExtractSignal import ExtractSignalFromCSV


'''
""" Define signals in pd.dataFrame format """
# preparing the input time series
N = 1000             # number of samples
f = 1.0             # sinewave frequency (Hz)
Fs = 200            # sampling frequency (Hz)
n = np.arange(0,N)  # number of samples
# input time series
x = pd.DataFrame({'X':np.sin(2*3.14*f*n/Fs)}, np.arange(0,N) )
y = pd.DataFrame(2.0*np.random.rand(N,1),np.arange(0,N))

'''
"""OR"""
""" Import signal from a .csv file """
filename = 'data_examples/2Persons_Multivariate_Continous_data.csv'
x = ExtractSignalFromCSV(filename, columns = ['Upper body mq'])
y = ExtractSignalFromCSV(filename, columns = ['Upper body mq.1'])
'''

"""OR"""
""" Import signal from a .mat file """
filename = 'data_examples/data_example_MAT.mat'
z = ExtractSignalFromMAT(filename, columns_index =[0,2], columns_wanted_names=['Time', 'GlobalBodyActivity0'])
t = ExtractSignalFromMAT(filename, columns_index =[10], columns_wanted_names=['GlobalBodyActivity1'])
'''

signals = [x,y]

N = signals[0].shape[0]
n = np.arange(0,N) 

""" Plot input signals """
plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111)
ax.grid(True)
ax.set_xlabel('Samples')
ax.set_title('input signals')
for i in range(len(signals)) :
    ax.plot(n, signals[i].iloc[:,0], label=signals[i].columns[0])
plt.legend(bbox_transform=plt.gcf().transFigure)

""" Define class attributes of the wanted method """

""" Instanciate the class with its attributes """
print("\n")
try : 
    omega_comp = Omega_Complexity.Omega_Complexity()
except TypeError, err :
    print("TypeError in Omega_Complexity constructor : \n" + str(err))
    sys.exit(-1)
except ValueError, err :
    print("ValueError in Omega_Complexity constructor : \n" + str(err))
    sys.exit(-1)
except Exception, e :
    print("Exception in Omega_Complexity constructor : \n" + str(e))
    sys.exit(-1)
    
print("An instance the class is now created \n")

""" Compute the method and get the result """
print("\n")
print("Computing...")

try : 
    omega = omega_comp.compute(signals)
except TypeError, err :
    print("TypeError in Omega_Complexity computation : \n" + str(err))
    sys.exit(-1)
except ValueError, err :
    print("ValueError in Omega_Complexity computation : \n" + str(err))
    sys.exit(-1)
except Exception, e :
    print("Exception in Omega_Complexity computation : \n" + str(e))
    sys.exit(-1)

""" Display result """
print("\n")
print('Omega_Complexity result :')
print("\n")

for i in omega.keys():
    print(i + " : " + str(omega[i]))
print("\n")

raw_input("Push ENTER key to exit.")
