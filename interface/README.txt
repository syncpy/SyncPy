=================
SyncPy Interface
=================

Current folder contains folders and files to use SyncPy interface.
Interface is generated thanks to pyQt, a python librairy allowing 
to create Qt applications.

The graphical interface is a pyQT application conceived to assist 
users to choose and try several methods. More sepcifically, it 
allows users to:

1)load time series from files
2)visualize/modify these time series through the utils
3)choose a consistent method according to the data set
4)compute the selected method and visualize and/or save the result 
in a file (.csv format).

------------------------
How to Download PyQt4: 
------------------------

http://pyqt.sourceforge.net/Docs/PyQt4/installation.html 


------------------------
How to run the interface
------------------------

run _Interface.bat


---------------------
data_examples/ folder
---------------------

Contains files for trying the interface with toy data. 


---------------
sources/ folder
---------------

Contains sources files for generating the Interface. 
No modification are needed to be usable. 

sources/method_files/ folder contains .csv files of methods definitions to be 
able to use these methods in the interface. 
.csv files are parsed in the interface so file architecture must be 
excatly the same as already created (no modification needed). 

sources/ui_files/ folder contains input Qt files, in .ui format, and their output .py files. 

