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

import sys
import numpy as np
from PyQt4 import QtCore, QtGui

# Import Qt Ui classes
from Ui_MethodSelectionWindow import Ui_MethodSelectionWindow

from SynchronyMethod import SynchronyMethod

class MethodSelectionWindow(QtGui.QMainWindow, Ui_MethodSelectionWindow):
    
    methodChosen = QtCore.pyqtSignal() #signal emitted when the method is selected
       
    def __init__(self, methods_dict):
        self.methods_dict = methods_dict
        super(MethodSelectionWindow, self).__init__()
        self.setupUi(self)
        self.initUI()
        self.method_selected = ''
        
    def initUI(self):
        #Hide unvisible widgets
        
        #Define slots 
        self.radioButton_data_1a.toggled.connect(self.excludeOtherChoice)
        self.radioButton_data_1b.toggled.connect(self.excludeOtherChoice)
        self.radioButton_data_2a.toggled.connect(self.excludeOtherChoice)
        self.radioButton_data_2b.toggled.connect(self.excludeOtherChoice)
        self.radioButton_data_3a.toggled.connect(self.excludeOtherChoice)
        self.radioButton_data_3b.toggled.connect(self.excludeOtherChoice)
        self.comboBox_linear_methods.activated ['QString'].connect(self.editSelectedMethod)
        self.comboBox_nonlinear_methods.activated ['QString'].connect(self.editSelectedMethod)
        self.comboBox_machinelearning_methods.activated ['QString'].connect(self.editSelectedMethod)
        self.pushButton_valid_method_2.clicked.connect(self.validateMethod)
        
        #Update lists    
        self.chooseMethodInList()
        
        # Display the window
        self.show()
        
               
    def chooseMethodInList(self):    
        #Get data properties selected
        if(self.radioButton_data_1a.isChecked()): number_user_type = 0
        else : number_user_type = 1
        if(self.radioButton_data_2a.isChecked()): signal_type = 0
        else : signal_type = 1
        if(self.radioButton_data_3a.isChecked()): data_type = 0
        else : data_type = 1
        
        #Update linear combo box
        count_linear = 0
        count_nonlinear = 0
        count_machinelearning = 0 
        self.comboBox_linear_methods.clear()
        self.comboBox_nonlinear_methods.clear()
        self.comboBox_machinelearning_methods.clear()
        for method in self.methods_dict.keys():
            if(self.methods_dict[method]._method_number_user_type == number_user_type):
                if(self.methods_dict[method]._method_signal_type == signal_type):
                    if(self.methods_dict[method]._method_data_type == data_type):
                        if(self.methods_dict[method]._method_type == 0):
                            self.comboBox_linear_methods.addItem(self.methods_dict[method]._method_name)
                            self.comboBox_linear_methods.setItemData(count_linear, self.methods_dict[method]._method_description, QtCore.Qt.ToolTipRole)
                            count_linear += 1 
                        elif(self.methods_dict[method]._method_type == 1):
                            self.comboBox_nonlinear_methods.addItem(self.methods_dict[method]._method_name)
                            self.comboBox_nonlinear_methods.setItemData(count_nonlinear, self.methods_dict[method]._method_description, QtCore.Qt.ToolTipRole)
                            count_nonlinear += 1 
                        elif(self.methods_dict[method]._method_type == 2):
                            self.comboBox_machinelearning_methods.addItem(self.methods_dict[method]._method_name)
                            self.comboBox_machinelearning_methods.setItemData(count_machinelearning, self.methods_dict[method]._method_description, QtCore.Qt.ToolTipRole)
                            count_machinelearning += 1 

        
    def excludeOtherChoice(self, checked):
        sender = self.sender() #get the current sender of the slot
        if(sender == self.radioButton_data_1a):
            self.radioButton_data_1b.setChecked(not(checked))
        if(sender == self.radioButton_data_1b):
            self.radioButton_data_1a.setChecked(not(checked))
        if(sender == self.radioButton_data_2a):
            self.radioButton_data_2b.setChecked(not(checked))
        if(sender == self.radioButton_data_2b):
            self.radioButton_data_2a.setChecked(not(checked))
        if(sender == self.radioButton_data_3a):
            self.radioButton_data_3b.setChecked(not(checked))
        if(sender == self.radioButton_data_3b):
            self.radioButton_data_3a.setChecked(not(checked))
        
        #Update lists    
        self.chooseMethodInList()
            
            
    def editSelectedMethod(self, text):
         self.method_selected = text


    def validateMethod(self): 
        if(self.method_selected != "") : 
                self.close()
        else :
             mess = QtGui.QMessageBox.warning(self,
                                            'Warning Message',
                                            "You must choose a method")
    
    
    def closeEvent(self, event):
        if(self.method_selected == "") :
            reply = QtGui.QMessageBox.question(self, 'Message',
                "Do you want to quit without choosing a method?",
                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.Yes)

            if reply == QtGui.QMessageBox.Yes:
                event.accept() # let the window close
            else:
                event.ignore()
        else :
            reply = QtGui.QMessageBox.question(self, 'Message',
                "Do you want to use "+self.method_selected+" method?",
                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.Yes)
    
            if reply == QtGui.QMessageBox.Yes:
                self.methodChosen.emit()
                event.accept() # let the window close
            else:
                event.ignore()