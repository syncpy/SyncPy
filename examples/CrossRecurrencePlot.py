"""
CrossRecurrencePlot example :
It computes the (cross) recurrence between two uni/multi-variate signals x and y(in DataFrame format).
"""

""" Import common python packages """
import sys
import os
import numpy as np              # Mathematical package
import pandas as pd             # Time serie package
import matplotlib.pyplot as plt # Plotting package
sys.path.insert(0, '../src/')   # To be able to import packages from parent directory 

print("\n")
print("**************************************************************")
print("This script computes ...\n")
print("**************************************************************")

""" Import wanted module  """
from utils import CrossRecurrencePlot

""" Define signals in pd.dataFrame format """

#Define parameters
N=1000
t=np.linspace(0,4*np.pi,N)

#Create signals
x=pd.DataFrame(3.0*np.sin(t+0.0001), np.arange(0,N))
y=pd.DataFrame(4.0*np.cos(t+0.0001), np.arange(0,N))


""" Define parameters of the wanted method """
m=1                       # the mebedding dimension
t=1                       # the delay between data
e=0.1                     # the threshold for recurrence
distance= 'euclidean'     # the distance method to be used
standardization= True     # standardization of the time series to mean 0 and variance 1
plot = True               # plot of the (cross)recurrence matrix 


""" Call CrossRecurrencePlot utils method """
print("\n")

try : 
    c =CrossRecurrencePlot.CrossRecurrencePlot(x,y, m, t, e,distance, standardization, plot)
except TypeError, err :
    print("TypeError in CrossRecurrencePlot : \n" + str(err))
    sys.exit(-1)
except ValueError, err :
    print("ValueError in CrossRecurrencePlot : \n" + str(err))
    sys.exit(-1)
except Exception, e :
    print("Exception in CrossRecurrencePlot : \n" + str(e))
    sys.exit(-1)


raw_input("Push ENTER key to exit.")
plt.close("all")




