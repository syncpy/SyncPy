"""
BooleanTurnsActivity example :
Computes data turns statistics between two boolean monovariate signals (in DataFrame format) x and y :
x signal activity duration, y signal activity duration, pause duration, overlap duration,
x signal pause duration, y signal pause duration, pause duration between x and y activity,
synchrony ratios between x and y (defined by max_latency)
"""

""" Import common python packages """
import sys
import os
import numpy as np          # Mathematical package
import pandas as pd         # Time serie package
import matplotlib.pyplot as plt # Plotting package
sys.path.insert(0, '../src/')   # To be able to import packages from parent directory 

print("\n")
print("****************************************************************************************")
print("This script computes the boolean turn activty of two categorical monovariate signals \n")
print("****************************************************************************************")

""" Import wanted module with every parent packages """
import DataFrom2Persons.Monovariate.Categorical.Linear.BooleanTurnsActivity as BooleanTurnsActivity

""" Import Utils modules """
from utils.ExtractSignal import ExtractSignalFromELAN

""" Define signals in pd.dataFrame format """
'''
# Create signals
user0_data = pd.DataFrame({'X':[0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0]})
user1_data = pd.DataFrame({'Y':[0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1]})
'''

# Import signals from .csv file, example with an ELAN data file
filename = 'data_examples/ELAN_2Persons.csv'
user0_data = ExtractSignalFromELAN(filename, separator=';', total_duration = 240,
                                    ele_per_sec = 5, Actor = 'Maman', Action = 'all')
user1_data = ExtractSignalFromELAN(filename, separator=';', total_duration = 240,
                                    ele_per_sec = 5, Actor = 'Bebe', Action = 'all')

# plot input signals
ele_per_sec = 5
n = [float(x)/ele_per_sec for x in range(user0_data.size)] # create x axis values
plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111)
ax.grid(True)
ax.set_xlabel('Time (ms)')
ax.set_title('Input signals')
ax.set_ylim(0, 1.5)
ax.plot(n,[float(y)/2 for y in user0_data.values],'g.', label=user0_data.columns[0])
ax.plot(n, user1_data.values, 'b.', label=user1_data.columns[0])
plt.legend(bbox_transform=plt.gcf().transFigure)

""" Define class attributes of the wanted method """
max_latency = 3.0           # the maximal delay between the two signals activity to define synchrony (in second)
min_pause_duration = 0.01   # minimal time for defining a pause (in second)
ele_per_sec = 5             # number of element in one second. Default: 1
duration = -1               # total activity duration (in second). Default or -1 : len(x)*ele_per_sec

""" Instanciate the class with its attributes """
print("\n")

try : 
    turns = BooleanTurnsActivity.BooleanTurnsActivity(max_latency, min_pause_duration, ele_per_sec, duration)
except TypeError, err :
    print("TypeError in BooleanTurnsActivity constructor : \n" + str(err))
    sys.exit(-1)
except ValueError, err :
    print("ValueError in BooleanTurnsActivity constructor : \n" + str(err))
    sys.exit(-1)
except Exception, e :
    print("Exception in BooleanTurnsActivity constructor : \n" + str(e))
    sys.exit(-1)

print("An instance the class is now created with the following parameters:\n" +
      "maximal latency = " + str(max_latency) + "\n" +
      "minimal pause duration = " + str(min_pause_duration) + "\n" +
      "number of element per second = " + str(ele_per_sec) + "\n" +
      "duration = " + str(duration))

""" Compute the method and get the result """
try : 
    res_turns, turns_ratio = turns.compute(user0_data, user1_data)
except TypeError, err :
    print("TypeError in BooleanTurnsActivity computation : \n" + str(err))
    sys.exit(-1)
except ValueError, err :
    print("ValueError in BooleanTurnsActivity computation : \n" + str(err))
    sys.exit(-1)
except Exception, e :
    print("Exception in BooleanTurnsActivity computation : \n" + str(e))
    sys.exit(-1)

""" Display result """
print("\n")
print("**************************************** \n")
print('Boolean turns activity complete result :')
print("****************************************\n")
print(res_turns)
print(turns_ratio)

""" Get simple statistics of the result """
stats = res_turns.describe()

""" Display statistics result """
print("\n")
print("***********************************\n")
print('Boolean turns activity statistics :')
print("***********************************\n")
print(stats)

raw_input("Push ENTER key to exit.")
