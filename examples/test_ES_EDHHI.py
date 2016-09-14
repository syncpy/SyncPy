# -*-coding:Latin-1 -*
'''To be able to import parent directories'''
import sys
sys.path.insert(0, '../src/')

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import DataFrom2Persons.Univariate.Categorical.Nonlinear.EventSync as EventSync

print("***************************************************************************************")
print("This scripts computes the synchronisation and time delay pattern between two monovariate\n time series of events expressed as Python Pandas DataFrame.\n Data are from the SMART Project-EDHHI (Engagement During Human-Humanoid Interaction) and \n are events extracted from the arms/body movements of a human and a robot performing a task together")
print("***************************************************************************************")


raw_input("Push ENTER key to continue.")



#input time series
print("\n")
print("Reading the input signals...")

df_r=pd.read_csv('EDHHI_Data/good_sync_robot.csv',sep='\n')
df_h=pd.read_csv('EDHHI_Data/good_sync_peak.csv',sep='\n')


s=np.arange(0,df_h.shape[0])


plt.ion()
f, axarr = plt.subplots(2, sharex=True)
axarr[0].set_title('Input signals')
axarr[0].set_xlabel('Samples')
axarr[1].set_xlabel('Samples')
axarr[0].stem(s,df_h,label="human")
axarr[1].stem(s, df_r, label="i-cub")
axarr[0].legend(loc='best')
axarr[1].legend(loc='best')

raw_input("Push ENTER key to continue.")
print("\n")

print("An instance of ES is now created with the following parameters: type is set to 'tot' and a prefixed constant tau equal to 4 is used to compute Q and q.")

print("\n")
print("Computing...")


c1=EventSync.ES('tot',0,35)
res1=c1.compute(df_h,df_r)
if res1:
    print ("Value of Q and q: %f and %f"%(res1[0],res1[1]))
    print("\n")

raw_input("Push ENTER key to continue.")

print("A new instance of ES is now created with the following parameters: type is set to 'tsl', a prefixed constant tau equal to 4 is used to compute Q and q. Plot is set to True")
print("\n")
print("Computing...")

c2=EventSync.ES('tsl',0,35,0,True)
res2=c2.compute(df_h,df_r)


raw_input("Push ENTER key to exit.")
plt.close("all")

