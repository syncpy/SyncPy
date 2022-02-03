SyncPy Python Library
=============================

The SyncPy Python Library is an ongoing open-source project conceived and developed at
the Institut des Systèmes Intelligentes et Robotique (ISIR) at the Université
Sorbonne Université, Paris 6, France.

SyncPy library is currently under development in the framework of the 
SMART Labex Project (http://www.smart-labex.fr)

*This fork has minor edits to make it work with Python 3*

Motivation
------------------------

SyncPy is a novel open-source analytic library for investigating 
synchrony in a fast and exhaustive way. It stems from work and 
discussions among researchers on synchrony in different domains 
as engineering, computer science and psychology. 

SyncPy is mainly aimed at helping researchers to explore, try and compare in an easy 
way and with a single tool synchrony methods starting from signals. 
Signals are synthetic or experimental time series organized as Python 
pandas DataFrames.

The library has been conceived to investigate synchrony in human-human/
human machine interaction, however, although it focuses on interpersonal 
synchrony, all the methods are exploitable in other contexts.

Architecture
------------------------

SyncPy includes three main components:
- Utils package
- Graphical interface
- Synchrony methods package


The utils package contains functionals of general utility directly used 
by the synchrony methods or to preprocess the input signals.

The graphical interface is a pyQT application conceived to assist users 
to choose and try several methods. More specifically, it allows users to:
1) load time series from files
2) visualize these time series
3) choose a consistent method according to the data set
4) compute the selected method and
5) visualize and/or save the result in a file (.csv format, .png format).

The synchrony methods package contains the methods to compute synchrony. 
The methods are organized following the structure described in the paper: 
"SyncPy - A unified analytic library for synchrony" (see References).


Version 
------------------------

Version number : 3.0
Last update : 03/02/2022


Changes from previous version
-----------------------------

News :
- Migrating from Python 2.7, PyQt4 to Python 3.x, PyQt5

Issues in "examples" folder :
- DAE -> migrating from tensorflow 1.x to tensorflow 2.x requires work
- oneclassSVM -> use of svm.OneClassSVM evolved and the kernel parameter seems to have evolved
- S_Estimator -> error in computing


Installation
------------------------
- Install Python 3.x, preferably from Anaconda : https://www.anaconda.com/products/individual
- Clone or donwload this repository
- install dependecies : pip install -r requirements.txt
- Then you can run .py files from "examples" folder or for use with UI src/Syncpy2.py

Requirements
------------------------
- Python 3.9
- Mathplotlib 3.5.1

Dependencies
------------------------

- Matplotlib: http://matplotlib.org/downloads.html
 - If you are Working with Matplotlib in a virtual environment 
	see 'Working with Matplotlib in Virtual environments' in the Matplotlib FAQ
- NetworkX: https://networkx.github.io/download.html
- Numpy and Scipy: http://www.scipy.org/scipylib/download.html
- Pandas: http://pandas.pydata.org/pandas-docs/stable/install.html
- Statsmodels and Patsy: http://statsmodels.sourceforge.net/install.html


Organization
------------------------
- installers\ : it contains the installers for the following operating systems: Windows, Mac OSX and Linux. 
- src\ : it contains the source files of syncpy methods and UI; 
- doc\ : it contains the SyncPy documentation, in html and pdf format;
- examples\ : it contains fully functional examples of use of SyncPy modules; 


Warning
------------------------
Any uncritical application of the utils and methods of this library 
can produce pitfalls. 


Authors 
------------------------
- Marie Avril
- Mohamed Chetouani
- Philippe Gauthier
- David Reversat
- Giovanna Varni


Contact
------------------------
For any questions, bugs reporting and comments don't hesitate to contact us: syncpy(AT)isir.upmc.fr



Licence
------------------------

 This software is governed by the CeCILL-B license under French law
and abiding by the rules of distribution of free software. You can 
use, modify and/ or redistribute the software under the terms of the 
CeCILL-B license as circulated by CEA, CNRS and INRIA at the
following URL "http://www.cecill.info".


References 
------------------------

Please cite this paper if you are using SyncPy for your own research :
    
    Giovanna Varni, Marie Avril, Adem Usta, Mohamed Chetouani.
    *SyncPy - A unified analytic library for synchrony.*
    Accepted at First International Workshop on Modeling INTEPERsonal SynchrONy @ICMI 2015 Conference. 


