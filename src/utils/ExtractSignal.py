### This file is a part of the Syncpy library.
### Copyright 2015, ISIR / Universite Pierre et Marie Curie (UPMC)
### Main contributor(s): Giovanna Varni, Marie Avril,
### syncpy@isir.upmc.fr
### 
### This software is a computer program whose for investigating
### synchrony in a fast and exhaustive way. 
### 
### This software is governed by the CeCILL-B license under French law
### and abiding by the rules of distribution of free software.  You
### can use, modify and/ or redistribute the software under the terms
### of the CeCILL-B license as circulated by CEA, CNRS and INRIA at the
### following URL "http://www.cecill.info".

### As a counterpart to the access to the source code and rights to
### copy, modify and redistribute granted by the license, users are
### provided only with a limited warranty and the software's author,
### the holder of the economic rights, and the successive licensors
### have only limited liability.
### 
### In this respect, the user's attention is drawn to the risks
### associated with loading, using, modifying and/or developing or
### reproducing the software by the user in light of its specific
### status of free software, that may mean that it is complicated to
### manipulate, and that also therefore means that it is reserved for
### developers and experienced professionals having in-depth computer
### knowledge. Users are therefore encouraged to load and test the
### software's suitability as regards their requirements in conditions
### enabling the security of their systems and/or data to be ensured
### and, more generally, to use and operate it in the same conditions
### as regards security.
### 
### The fact that you are presently reading this means that you have
### had knowledge of the CeCILL-B license and that you accept its terms.

import numpy as np
import pandas as pd

from scipy.io import loadmat  # this is the SciPy module that loads mat-files

def ExtractSignalFromCSV(filename, separator=',', unit='ms', columns=['all']):
    """
    It extracts a signal from a .csv file (organized by columns, with first one corresponding to time index)
    
    :param filename:
        complete path + filename to the csv file.
    :type filename: str
    
    :param separator:
        separator between columns in the csv file. Default: ','
    :type separator: str
    
    :param unit:
        Time unit for the index. Default = 'ms'
    :type unit: str
    
    :param columns:
        array containing columns name of index wanted for the signal.
        Default: 'all' 
    :type columns: list
    
    :returns: pd.DataFrame
            -- Extracted signal
    """
    
    #if only one column is given as str, convert it in list
    if isinstance(columns, str) or isinstance(columns, int):
        columns = [columns]

    ' Raise error if parameters are not in the correct type '
    try :
        if not(isinstance(filename, str)): raise TypeError("Requires filename to be a str.")
        if not(isinstance(separator, str)): raise TypeError("Requires separator to be a str.")
        if not(isinstance(unit, str)): raise TypeError("Requires unit to be a str.")
        if not(isinstance(columns, list)): raise TypeError("Requires columns to be a list.")
        for i in range(len(columns)):
            if not(isinstance(columns[i],int)) and not(isinstance(columns[i],str)) : raise TypeError("Requires columns values to be a str or int.")
    except TypeError, err_msg:
        raise TypeError(err_msg)
        return
    
    #Test if the filename containts the extension
    if filename.find('.csv') == -1 :
        filename += '.csv'
        
    input_data = pd.DataFrame()
    input_data = pd.read_csv(filename, sep = separator)
    
    input_data.set_index(input_data.columns[0], inplace = True)
    input_data.index = pd.to_datetime(input_data.index,  unit=unit) # Convert time into DateTime format
    input_data.index.names = ['Time (' + unit +')']

    if columns != ['all'] :
        signal = pd.DataFrame(input_data[columns], input_data.index)
    else :
        signal = input_data

    return signal


def ExtractSignalFromELAN(filename, separator=',', unit='s', columns_name = ['Actor', ' ', 't_begin', 't_end', 'duration', 'Action', 'video'],
             total_duration = 0, ele_per_sec = 1, Actor = '', Action = 'all'):
    """
    It extracts a boolean signal from ELAN output annotations.
    It returns a boolean signal, a DataFrame with milliseconds timestamps.
    The freqency of timestamps is defined by 'ele_per_sec'.
    The signal is True between two timestamps if in the file, the actor defined in 'Actor' pararameter is doing the action
    defined in 'Action'. 
    
    :param filename:
        complete path + filename to the csv file out from ELAN
    :type filename: str
    
    :param separator:
        separator between columns in the csv file. Default: ','
    :type separator: str
    
    :param unit:
        Time unit for the index. Default = 's'
    :type unit: str
    
    :param columns_name:
        array containing the names of each columns in ELAN File in the correct order
        It must contain at lest these exacts elements : 'Actor', 't_begin', 't_end', 'Action'
        if a colunm is empty, give '' as name. Default: ['Actor', ' ', 't_begin', 't_end', 'duration', 'Action', 'video']
    :type columns_name: list
    
    :param total_duration:
        the total duration attempted for the signal, in time unit given by 'unit'.
        If zero is given, the total duration will be computed as the end of the last event recorded in ELAN file. Default: 0 
    :type total_duration: int
    
    :param ele_per_sec:
        Number of element wanted per second in the computed signal. Default = 1
    :type ele_per_sec: int
    
    :param Actor:
        Name of the Actor in the ELAN annotation file
    :type Actor: str
    
    :param Action:
        Name of the Action in the ELAN annotation file. Default ='all'
    :type Action: str

    :returns: pd.DataFrame
            -- Monovariate boolean signal, with 1 at timestamps corresponding to the Action of the Actor, timestamps in ms
    """
    
    ' Raise error if parameters are not in the correct type '
    try :
        if not(isinstance(filename, str)): raise TypeError("Requires filename to be a str.")
        if not(isinstance(separator, str)): raise TypeError("Requires separator to be a str.")
        if not(isinstance(columns_name, list)): raise TypeError("Requires columns_name to be a list.")
        for i in range(len(columns_name)):
            if not(isinstance(columns_name[i],str)) : raise TypeError("Requires columns_name for index " + str(i) + "values to be a str or str.")
        if not(isinstance(total_duration, int)): raise TypeError("Requires total_duration to be an int.")
        if not(isinstance(ele_per_sec, int)): raise TypeError("Requires ele_per_sec to be an int.")
        if not(isinstance(Actor, str)): raise TypeError("Requires Actor to be a str.")
        if not(isinstance(Action, str)): raise TypeError("Requires Action to be an str.")
    except TypeError, err_msg:
        raise TypeError(err_msg)
        return
    
    #Test if the filename containts the extension
    if filename.find('.csv') == -1 :
        filename += '.csv'
        
    input_data = pd.DataFrame()
    input_data = pd.read_csv(filename, sep = separator)

    'Rename columns to correct use'
    input_data.columns = columns_name
    
    'if total_duration undefined, get the last t-end of the ELAN data'
    if total_duration == 0 : 
        total_duration = input_data['t_end'][input_data.index[-1]]

    'Intialize boolean signals'
    if unit == 's':
        coef = 1000
    else:
        coef = 1
    time_index = [float(i)/ele_per_sec*coef for i in range(int(np.floor(total_duration*ele_per_sec)))]
    
    time_column_name = Actor
    if(Action != 'all') : 
        time_column_name = time_column_name + '_' + Action
    
    boolean_signal = pd.DataFrame({'Time' : pd.Series(time_index),
                                    time_column_name : pd.Series([0]*len(time_index))})
    boolean_signal.set_index('Time', inplace = True)
    
    'Convert ELAN event into boolean activity'
    for idx in input_data.index :        
        idx_begin = int(np.floor(input_data.at[idx,'t_begin']*coef))
        idx_end =  int(np.floor(input_data.at[idx,'t_end']*coef))
        
        if idx_begin < total_duration*coef and idx_end > total_duration*coef :
            idx_end = total_duration*coef
            
        if(input_data.at[idx,'Actor'] == Actor):
            if Action == 'all' or input_data.at[idx,'Action'] == Action :
                boolean_signal[idx_begin : idx_end] = 1
                    
    boolean_signal.index = pd.to_datetime(boolean_signal.index, unit='ms') #Convert time into DateTime format
    boolean_signal.index.names = ['Time (ms)']

    return boolean_signal


def ExtractSignalFromMAT(filename, columns_index=['all'], columns_wanted_names=['all'], unit='ms'):
    """
    It extracts a signal from a .mat MATLAB file (organized by columns, with first one corresponding to time index)
    
    :param filename:
        complete path + filename to the mat file.
    :type filename: str

    :param columns_index:
        array containing columns indexes of index wanted for the signal.
        Default: 'all' 
    :type columns_index: list
    
    :param columns_wanted_names:
        array containing columns names wanted for the signal.
        Default: 'all' ('0', '1' ...)
    :type columns_wanted_names: list
    
    :param unit:
        Time unit for the index. Default = 'ms'
    :type unit: str
    
    :returns: pd.DataFrame
            -- Extracted signal
    """
    
    #if only one column is given as str, convert it in list
    if isinstance(columns_index, int):
        columns_index = [columns_index]
    if isinstance(columns_wanted_names, str):
        columns_wanted_names = [columns_wanted_names]

    ' Raise error if parameters are not in the correct type '
    try :
        if not(isinstance(filename, str)): raise TypeError("Requires filename to be a str.")
        if not(isinstance(columns_index, list)): raise TypeError("Requires columns_index to be a list.")
        for i in range(len(columns_index)):
            if columns_index != ['all'] and not(isinstance(columns_index[i],int)): raise TypeError("Requires columns_index values to be int.")
        if not(isinstance(columns_wanted_names, list)): raise TypeError("Requires columns_wanted_names to be a list.")
        for i in range(len(columns_wanted_names)):
            if columns_wanted_names != ['all'] and not(isinstance(columns_wanted_names[i],str)): raise TypeError("Requires columns_wanted_names values to be str.")
        if not(isinstance(unit, str)): raise TypeError("Requires unit to be a str.")
    except TypeError, err_msg:
        raise TypeError(err_msg)
        return
     
    try :
        if columns_index != ['all'] and columns_wanted_names != ['all'] and len(columns_index)!=len(columns_wanted_names) : raise ValueError("If columns indexes are defined, columns_wanted_names must have the same size")
        if  columns_wanted_names != ['all'] and len(columns_index)!=len(columns_wanted_names) : raise ValueError("columns_wanted_names must have the same size as columns_index")
    except ValueError, err_msg:
            raise ValueError(err_msg)
            return 
            
    #Test if the filename containts the extension
    idx = filename.find('.mat')
    if idx != -1 :
        filename = filename[0:idx]
        
    mat = loadmat(filename)  # load mat-file
    
    # get array data
    for val in mat.values():
        if isinstance(val, np.ndarray):
            mdata = val
    
    #mdata = mat[filename]  # get array data
    
    dict_data = {}
    dict_data.update({'Time ('+ unit +')' : pd.Series(mdata[: ,0])})
    
    if columns_index == ['all'] :
        columns_index = [x for x in range(mdata.shape[1])]
    
    if columns_wanted_names == ['all'] :
        columns_wanted_names = [str(x) for x in range(len(columns_index))]
        
    for idx in range(len(columns_index)) :
        if columns_index[idx] != 0 : # ignore first index corresponding to time colums
            dict_data.update({columns_wanted_names[idx] : pd.Series(mdata[:, columns_index[idx]])})
    
    signal = pd.DataFrame(dict_data)
    signal.set_index('Time ('+ unit +')', inplace = True)
    signal.index = pd.to_datetime(signal.index,  unit=unit) #Convert time into DateTime format 
    signal.index.names = ['Time ('+ unit +')']
    
    return signal
