# SyncPy Python Library

Current folder contains folders to use SyncPy python library. 


##	Presentation
------------------------

SyncPy is a novel open-source analytic library for investigating 
synchrony in a fast and exhaustive way. It stems from work and 
discussions among researchers on synchrony in different domains 
as engineering, computer science and psychology. SyncPy is mainly 
aimed at helping researchers to explore, try and compare in an easy 
way and with a single tool synchrony methods starting from signals. 
Signals are synthetic or experimental time series organized as pandas 
DataFrames.

The library has been conceived to investigate synchrony in human-human/
human machine interaction, however, although it focuses on interpersonal 
synchrony, all the methods are exploitable in other contexts.

SyncPy functionalities include three main components:
- utils package
- graphical interface
- synchrony methods package
- The utils package contains functionals of general utility directly used 
by the synchrony methods or to preprocess the input signals.

The graphical interface is a pyQT application conceived to assist users 
to choose and try several methods. More sepcifically, it allows users to:
1) load time series from files
2) visualize/modify these time series through the utils
3) choose a consistent method according to the data set
4) compute the selected method and
5) visualize and/or save the result in a file (.csv format).

SyncPy library is currently under development in the framework of the 
SMART Labex Project (http://www.smart-labex.fr)

## Version 

Version number : 1.4
Last update : 28/01/2016


## Dependencies
------------------------

- Matplotlib: http://matplotlib.org/downloads.html
- NetworkX: https://networkx.github.io/download.html
- Numpy and Scipy: http://www.scipy.org/scipylib/download.html
- Pandas: http://pandas.pydata.org/pandas-docs/stable/install.html
- Statsmodels and Patsy: http://statsmodels.sourceforge.net/install.html 

For the interface: 
- PyQt : http://pyqt.sourceforge.net/Docs/PyQt4/installation.html 


# Organization
------------------------

- src\ : folder of source files, organized in a 4 levels tree; 
- doc\ : Contains SyncPy documentation, in html and pdf format;
- examples\ : Contains fully functional examples of use of SyncPy modules; 
- interface\ : folder of the asssitive interface. 


# Authors 
------------------------

- Giovanna Varni 
- Marie Avril 
- contact: syncpy@isir.upmc.fr 


# Licence
------------------------

 This software is governed by the CeCILL-B license under French law
and abiding by the rules of distribution of free software. You can 
use, modify and/ or redistribute the software under the terms of the 
CeCILL-B license as circulated by CEA, CNRS and INRIA at the
following URL "http://www.cecill.info".


#   References 
------------------------

Please cite this paper if you are using SyncPy for your own research :
    
    Giovanna Varni, Marie Avril, Adem Usta, Mohamed Chetouani.
    SyncPy - A unified analytic library for synchrony.
    Accepted at First International Workshop on Modeling INTEPERsonal SynchrONy @ICMI 2015 Conference. 