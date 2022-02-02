"""
Correlation example:
It computes the linear correlation between two monovariate signals x and y (in DataFrame format) as a function of their delay tau.
It computes autocorrelation when y coincides with x. 
"""

""" Import common python packages """
import sys
import os
import numpy as np      # Mathematical package
import pandas as pd     # Time serie package
import matplotlib.pyplot as plt # Plotting package
sys.path.insert(0, '../src/')   # To be able to import packages from parent directory
sys.path.insert(0, '../src/Methods')

print ("\n")
print("***********************************************************************************************************************")
print("This scripts computes the recurrence matrix " )
print("************************************************************************************************************************")

import DataFrom2Persons.Univariate.Continuous.MachineLearning.oneclassSVMimitation as oneclassSVMimitation


"""
    :param vid1file 
        the name of first video located in the Data folder( Syncpy/src/samples )
    :type vid1file: file
        
    :param vid2file 
        the name of second video located in the Data folder( Syncpy/src/samples )
    :type vid2file: file
         
    :param K 
        number of words in the codebook or the codewords or visual vocabulary or K means number of clusters
    :type K: int
          
    :param DataPath 
        Where the Data is located in your computer
    :type DataPath: str
         
    :param threshold 
        threshold on oneClassSVM scores 
    :type threshold: float
        
"""


""" Define class attributes of the wanted method """
print("\n")
plot=True                           # plot 
vid1file= open("data_examples/jean.csv")
vid2file=open("data_examples/wail.csv")
K=30
thr=0.1 # threshold

""" Instanciate the class with its attributes """
print("\n")

try : 
   c=oneclassSVMimitation.oneclassSVMimitation(vid1file,vid2file,K,threshold=thr)   
except TypeError as err:
    print("TypeError in oneclassSVMimitation constructor : \n" + str(err))
    sys.exit(-1)
except  ValueError as err:
    print("ValueError in oneclassSVMimitation constructor : \n" + str(err))
    sys.exit(-1)
except Exception as e:
    print("Exception in oneclassSVMimitation constructor : \n" + str(e))
    sys.exit(-1)

print("An instance of the class is now created with the following parameters:\n" +
      "vid1file = " + str(vid1file) + "\n" +
      "plot = " + str(plot) + "\n" +
      "vid2file= " + str(vid2file) + "\n" +
      "K-dict = " + str(K) + "\n" +
      "threshold =" + str(thr))

""" Compute the method and get the result """
print("\n")
print("Computing...")

try : 
    res= c.compute()
except  TypeError as err :
    print("TypeError in oneclassSVMimitation computation : \n" + str(err))
    sys.exit(-1)
except ValueError as err :
    print("ValueError in oneclassSVMimitation computation : \n" + str(err))
    sys.exit(-1)
except   Exception as e :
    print("Exception in oneclassSVMimitation computation : \n" + str(e))
    sys.exit(-1)

""" Display result """
print("\n")
print("**************************************** \n")
print('Imitation complete result :')
print("****************************************\n")
print("Recurrence matrix array:")
print(res)
print("High density of ones means brighter colors !  \n")
print("Please keep in mind that the results depends on your choice of K and threshold--very important ! \n ")

c.plot_result()


input("Push ENTER key to exit.")
plt.close("all")




    
