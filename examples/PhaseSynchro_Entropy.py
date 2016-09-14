"""
PhaseSynchro_Entropy example :
It computes the n:m synchronization index rho_nm by using a Shannon entropy based approach between two univariate signals x and y
(in pandas DataFrame format). Rho_nm ranges in [0,1] where 0 means no synchronization at all and 1 means perfect synchronization.
"""

""" Import common python packages """
import sys
import os
import numpy as np          # Mathematical package
import pandas as pd         # Time serie package
import matplotlib.pyplot as plt # Plotting package
sys.path.insert(0, '../src/')   # To be able to import packages from parent directory

print("\n")
print("********************************************************************************")
print("This script computes the n:m synchronization index rho_nm by \n" +
       "using a Shannon entropy based approach between two univariate signals x and y\n" +
       "(in pandas DataFrame format). Rho_nm ranges in [0,1] where 0 means \n" + 
       "no synchronization at all and 1 means perfect synchronization.")
print("********************************************************************************")

""" Import wanted module with every parent packages """
import Methods.DataFrom2Persons.Univariate.Continuous.Nonlinear.PhaseSynchro_Entropy as PhaseSynchro_Entropy


""" Define signals in pd.dataFrame format """

#Define parameters
N=1000
t=np.linspace(0,4*np.pi,N)


x=pd.DataFrame(np.sin(t), np.arange(0,N))
y=pd.DataFrame(np.sin(3*t+10), np.arange(0,N))

x.to_csv("D:/projets/SyncPy/Syncpy-2/examples/data_examples/Entropy_x.csv", sep=';', index=True, header=False)
y.to_csv("D:/projets/SyncPy/Syncpy-2/examples/data_examples/Entropy_y.csv", sep=';', index=True, header=False)


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
n =  3                     # integer of the order of synchronization
m  = 1                     # integer of the order of synchronization
nbins_mode = 'man'         # mode used to compute the nbins number
nbins = 50                 # number of bins
plot = False # plot of the distribution of the cyclci relative phase

""" Instantiate the class with its attributes """
print("\n")

try : 
    c=PhaseSynchro_Entropy.PhaseSynchro_Entropy(n ,m, nbins_mode, nbins,plot )
except TypeError, err :
    print("TypeError in PhaseSynchro_Entropy constructor : \n" + str(err))
    sys.exit(-1)
except ValueError, err :
    print("ValueError in PhaseSynchro_Entropy constructor : \n" + str(err))
    sys.exit(-1)
except Exception, e :
    print("Exception in PhaseSynchro_Entropy constructor : \n" + str(e))
    sys.exit(-1)


print("An instance of the class is now created with the following parameters:\n" +
      "n = " + str(n) + "\n" +
      "m = " + str(m) + "\n" +
      "nbins_mode = " + str(nbins_mode) + "\n" +
      "nbins = " + str(nbins)+ "\n" +
      "plot =" + str(plot))


""" Compute the method and get the result """
print("\n")
print("Computing...")

try : 
    res= c.compute([x, y])
except TypeError, err :
    print("TypeError in PhaseSynchro_Entropy computation : \n" + str(err))
    sys.exit(-1)
except ValueError, err :
    print("ValueError in PhaseSynchro_Entropy computation : \n" + str(err))
    sys.exit(-1)
except Exception, e :
    print("Exception in PhaseSynchro_Entropy computation : \n" + str(e))
    sys.exit(-1)



""" Display results """
print("\n")
print("****************************************\n")
print('PhaseSynchro_Entropy complete result:\n')
print("****************************************\n")
print("rho_nm:")
print(res)
print("\n")

raw_input("Push ENTER key to exit.")
plt.close("all")




