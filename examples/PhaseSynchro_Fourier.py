"""
PhaseSynchro_Fourier example :
It computes the n:m synchronization index gamma2_nm as the intensity of the first Fourier mode of the cyclic relative phase two continuous univariate signals x and y
(in DataFrame format). Gamma2_nm ranges in [0,1] where 0 means no synchronization at all and 1 means perfect synchronization.
"""

""" Import common python packages """
import sys
import os
import numpy as np          # Mathematical package
import pandas as pd         # Time serie package
import matplotlib.pyplot as plt # Plotting package
sys.path.insert(0, '../src/')   # To be able to import packages from parent directory 

print("\n")
print("****************************************************************************")
print("This script computes the n:m synchronization index gamma2_nm as \n" + 
      "the intensity of the first Fourier mode of the cyclic relative phase \n" + 
      "of two continuous univariate signals x and y (in DataFrame format). \n" + 
      "Gamma2_nm ranges in [0,1] where 0 means no synchronization at all and 1 \n" + 
      "means perfect synchronization.")
print("****************************************************************************")

""" Import wanted module with every parent packages """
import DataFrom2Persons.Univariate.Continuous.Nonlinear.PhaseSynchro_Fourier as PhaseSynchro_Fourier


""" Define signals in pd.dataFrame format """

#Define parameters
N=1000
t=np.linspace(0,4*np.pi,N)


x=pd.DataFrame(np.sin(t), np.arange(0,N))
y=pd.DataFrame(np.sin(3*t+10), np.arange(0,N))


"""Plot input signals"""
plt.ion()
f, axarr = plt.subplots(2, sharex=True)
axarr[0].set_title('Input signals')
axarr[0].set_xlabel('Samples')
axarr[1].set_xlabel('Samples')
axarr[0].plot(range(0,N), x, label="x")
axarr[1].plot(range(0,N), y, label="y", color='r')
axarr[0].legend(loc='best')
axarr[1].legend(loc='best')


""" Define class attributes of the wanted method """
n =  2                     # integer of the order of synchronization
m  = 1                     # integer of the order of synchronization

""" Instantiate the class with its attributes """
print("\n")

try : 
    c=c=PhaseSynchro_Fourier.PhaseSynchro_Fourier(n ,m)
except TypeError, err :
    print("TypeError in PhaseSynchro_Fourier constructor : \n" + str(err))
    sys.exit(-1)
except ValueError, err :
    print("ValueError in PhaseSynchro_Fourier constructor : \n" + str(err))
    sys.exit(-1)
except Exception, e :
    print("Exception in PhaseSynchro_Fourier constructor : \n" + str(e))
    sys.exit(-1)


print("An instance of the class is now created with the following parameters:\n" +
      "n = " + str(n) + "\n" +
      "m = " + str(m))


""" Compute the method and get the result """
print("\n")
print("Computing...")

try : 
    res= c.compute(x, y)
except TypeError, err :
    print("TypeError in PhaseSynchro_Fourier computation : \n" + str(err))
    sys.exit(-1)
except ValueError, err :
    print("ValueError in PhaseSynchro_Fourier computation : \n" + str(err))
    sys.exit(-1)
except Exception, e :
    print("Exception in PhaseSynchro_Fourier computation : \n" + str(e))
    sys.exit(-1)



""" Display results """
print("\n")
print("****************************************\n")
print('PhaseSynchro_Fourier complete result:\n')
print("****************************************\n")
print("gamma2_nm:")
print(res)
print("\n")

raw_input("Push ENTER key to exit.")
plt.close("all")




