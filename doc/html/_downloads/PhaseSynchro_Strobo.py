"""
PhaseSynchro_Strobo example :
It computes the n:m synchronization index lambda_nm by using a stroboscopic approach between two continuous univariate signals x and y
(in DataFrame format).
"""

""" Import common python packages """
import sys
import os
import numpy as np          # Mathematical package
import pandas as pd         # Time serie package
import matplotlib.pyplot as plt # Plotting package
sys.path.insert(0, '../src/')   # To be able to import packages from parent directory 

print("\n")
print("**************************************************************")
print("This script computes the n:m synchronization index lambda_nm by \n" + 
      "using a stroboscopic approach between two continuous univariate \n" +
      "signals x and y (in DataFrame format).\n")
print("**************************************************************")

""" Import wanted module with every parent packages """
import DataFrom2Persons.Univariate.Continuous.Nonlinear.PhaseSynchro_Strobo as PhaseSynchro_Strobo


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
n = 3                   # integer of the order of synchronization
m  = 1                  # integer of the order of synchronization
nbins_mode = 'man'      # mode used to compute the nbins number
nbins = 10              # number of bins



""" Instantiate the class with its attributes """
print("\n")

try : 
    c=c=PhaseSynchro_Strobo.PhaseSynchro_Strobo(n,m,nbins_mode, nbins)
except TypeError, err :
    print("TypeError in PhaseSynchro_Strobo constructor : \n" + str(err))
    sys.exit(-1)
except ValueError, err :
    print("ValueError in PhaseSynchro_Strobo constructor : \n" + str(err))
    sys.exit(-1)
except Exception, e :
    print("Exception in PhaseSynchro_Strobo constructor : \n" + str(e))
    sys.exit(-1)


print("An instance of the class is now created with the following parameters:\n" +
      "n = " + str(n) + "\n" +
      "m = " + str(m) + "\n" +
      "nbins_mode = " + str(nbins_mode) + "\n" +
      "nbins = " + str(nbins))


""" Compute the method and get the result """
print("\n")
print("Computing...")

try : 
    res= c.compute(x, y)
except TypeError, err :
    print("TypeError in PhaseSynchro_Strobo computation : \n" + str(err))
    sys.exit(-1)
except ValueError, err :
    print("ValueError in PhaseSynchro_Strobo computation : \n" + str(err))
    sys.exit(-1)
except Exception, e :
    print("Exception in PhaseSynchro_Strobo computation : \n" + str(e))
    sys.exit(-1)



""" Display results """
print("\n")
print("****************************************\n")
print('PhaseSynchro_Strobo complete result:\n')
print("****************************************\n")
print("lambda_nm:")
print(res)
print("\n")

raw_input("Push ENTER key to exit.")
plt.close("all")




