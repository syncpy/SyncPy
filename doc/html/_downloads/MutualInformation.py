"""
Mutual Information example:
It Computes Mutual Information (MI) estimators starting from entropy estimates from k-nearest-neighbours distances.

"""

""" Import common python packages """
import sys
import os
import numpy as np              # Mathematical package
import pandas as pd             # Time serie package
import matplotlib.pyplot as plt # Plotting package
sys.path.insert(0, '../src/')   # To be able to import packages from parent directory 

print ("\n")
print("****************************************************************************\n")
print("This scripts computes two Mutual Information estimators from signals \n" +
      "by using k-nearest-neighbours approach.\n")
print("****************************************************************************\n")

""" Import wanted module with every parent packages """
import DataFrom2Persons.Univariate.Continuous.Nonlinear.MutualInformation as MutualInformation

""" Import Utils modules """
from utils.ExtractSignal import ExtractSignalFromCSV


""" Define signals in pd.dataFrame format """
print ("Two independent uniformly distributed signals: Mi estimator should be \n" + 
       "around 0 (negative values are due to statistical fluctuations)\n")
print("****************************************************************************\n")

# Create signals
n = 1000
x = pd.DataFrame(1.0*np.random.rand(n,1), range(0,n))
y = pd.DataFrame(1.0*np.random.rand(n,1), range(0,n))

'''
"""OR"""
""" Import signals from a .csv file """
#Data from files
filename = 'data_examples/2Persons_Univariate_Continuous_data.csv'

x = ExtractSignalFromCSV(filename, columns = ['x1'])
y = ExtractSignalFromCSV(filename, columns = ['x2'])
n = x.shape[0]
'''

"""Plot input signals"""
plt.ion()
f, axarr = plt.subplots(2, sharex=True)
axarr[0].set_title('Input signals')
axarr[0].set_xlabel('Samples')
axarr[1].set_xlabel('Samples')
axarr[0].plot(range(0,n), x, label="x")
axarr[1].plot(range(0,n), y, label="y", color='r')
axarr[0].legend(loc='best')
axarr[1].legend(loc='best')


""" Define class attributes of the wanted method """
n_neighbours = 10                   # the number of the nearest neighbours to be used
my_type = 1                         # the type of estimators
var_res = True                      # rescaling of the time series
noise = True                        # adding random noise to the time series


""" Instanciate the class with its attributes """
print("\n")

try : 
    c=MutualInformation.MutualInformation(n_neighbours,var_res,noise)
except TypeError, err :
    print("TypeError in MutualInformation constructor : \n" + str(err))
    sys.exit(-1)
except ValueError, err :
    print("ValueError in MutualInformation constructor : \n" + str(err))
    sys.exit(-1)
except Exception, e :
    print("Exception in MutualInformation constructor : \n" + str(e))
    sys.exit(-1)

print("An instance the class is now created with the following parameters:\n" +
      "n_neighbours = " + str(n_neighbours) + "\n" +
      "my_type = " + str(my_type) + "\n" +
      "var_res = " + str(var_res) + "\n" +
      "noise = " + str(noise))

""" Compute the method and get the result """
print("\n")
print("Computing...")

try : 
    res1= c.compute(x, y)
except TypeError, err :
    print("TypeError in MutualInformation computation : \n" + str(err))
    sys.exit(-1)
except ValueError, err :
    print("ValueError in MutualInformation computation : \n" + str(err))
    sys.exit(-1)
except Exception, e :
    print("Exception in MutualInformation computation : \n" + str(e))
    sys.exit(-1)

""" OTHER TRY WITH my_type = 2 """
my_type = 2

""" Instanciate the class with its attributes """
print("\n")

try : 
    c=MutualInformation.MutualInformation(n_neighbours,var_res,noise)
except TypeError, err :
    print("TypeError in MutualInformation constructor : \n" + str(err))
    sys.exit(-1)
except ValueError, err :
    print("ValueError in MutualInformation constructor : \n" + str(err))
    sys.exit(-1)
except Exception, e :
    print("Exception in MutualInformation constructor : \n" + str(e))
    sys.exit(-1)

print("An instance the class is now created with the following parameters:\n" +
      "n_neighbours = " + str(n_neighbours) + "\n" +
      "my_type = " + str(my_type) + "\n" +
      "var_res = " + str(var_res) + "\n" +
      "noise = " + str(noise))

""" Compute the method and get the result """
print("\n")
print("Computing...")

try : 
    res2= c.compute(x, y)
except TypeError, err :
    print("TypeError in MutualInformation computation : \n" + str(err))
    sys.exit(-1)
except ValueError, err :
    print("ValueError in MutualInformation computation : \n" + str(err))
    sys.exit(-1)
except Exception, e :
    print("Exception in MutualInformation computation : \n" + str(e))
    sys.exit(-1)


""" Display results """
print("\n")
print("****************************************\n")
print('MutualInformation complete result 1:\n')
print("****************************************\n")
print("MutualInformation estimator 1:")
print(res1)
print("\n")
print("MutualInformation estimator 2:")
print(res2)

#mixing matrix
C=np.random.rand(2,2)
x1 = pd.DataFrame(C[0,0]*x.iloc[:,0] + C[0,1]*y.iloc[:,0], x.index)
y1 = pd.DataFrame(C[1,0]*x.iloc[:,0] + C[1,1]*y.iloc[:,0], y.index)

print ("\n")
print("************************************************************************************************\n")
print ("We add some dependenty to the time series (new times series are linear combination of x and y):\n" +
       "Mi estimator should be now greater than 0 \n")
print("************************************************************************************************\n")

""" Define class attributes of the wanted method """

n_neighbours = 10                   # the number of the nearest neighbours to be used
my_type = 1                         # the type of estimators
var_res = True                      # rescaling of the time series
noise = True                        # adding random noise to the time series


""" Instanciate the class with its attributes """
print("\n")

try : 
    c=MutualInformation.MutualInformation(n_neighbours,var_res,noise)
except TypeError, err :
    print("TypeError in MutualInformation constructor : \n" + str(err))
    sys.exit(-1)
except ValueError, err :
    print("ValueError in MutualInformation constructor : \n" + str(err))
    sys.exit(-1)
except Exception, e :
    print("Exception in MutualInformation constructor : \n" + str(e))
    sys.exit(-1)

print("An instance the class is now created with the following parameters:\n" +
      "n_neighbours = " + str(n_neighbours) + "\n" +
      "my_type = " + str(my_type) + "\n" +
      "var_res = " + str(var_res) + "\n" +
      "noise = " + str(noise))

""" Compute the method and get the result """
print("\n")
print("Computing...")

try : 
    res1= c.compute(x1, y1)
except TypeError, err :
    print("TypeError in MutualInformation computation : \n" + str(err))
    sys.exit(-1)
except ValueError, err :
    print("ValueError in MutualInformation computation : \n" + str(err))
    sys.exit(-1)
except Exception, e :
    print("Exception in MutualInformation computation : \n" + str(e))
    sys.exit(-1)
    
    
my_type = 2

""" Instanciate the class with its attributes """
print("\n")

try : 
    c=MutualInformation.MutualInformation(n_neighbours,var_res,noise)
except TypeError, err :
    print("TypeError in MutualInformation constructor : \n" + str(err))
    sys.exit(-1)
except ValueError, err :
    print("ValueError in MutualInformation constructor : \n" + str(err))
    sys.exit(-1)
except Exception, e :
    print("Exception in MutualInformation constructor : \n" + str(e))
    sys.exit(-1)

print("An instance the class is now created with the following parameters:\n" +
      "n_neighbours = " + str(n_neighbours) + "\n" +
      "my_type = " + str(my_type) + "\n" +
      "var_res = " + str(var_res) + "\n" +
      "noise = " + str(noise))

""" Compute the method and get the result """
print("\n")
print("Computing...")

try : 
    res2= c.compute(x1, y1)
except TypeError, err :
    print("TypeError in MutualInformation computation : \n" + str(err))
    sys.exit(-1)
except ValueError, err :
    print("ValueError in MutualInformation computation : \n" + str(err))
    sys.exit(-1)
except Exception, e :
    print("Exception in MutualInformation computation : \n" + str(e))
    sys.exit(-1)

""" Display result """
print("\n")
print("**************************************** \n")
print('MutualInformation complete result 2:\n')
print("****************************************\n")
print("MutualInformation estimator 1:")
print(res1)
print("\n")
print("MutualInformation estimator 2:")
print(res2)

raw_input("Push ENTER key to exit.")
plt.close("all")
