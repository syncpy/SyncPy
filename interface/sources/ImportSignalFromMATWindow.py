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

'''----- To be able to import parent directories -----'''
import sys
sys.path.insert(0, '../../src/')

import os
import numpy as np
import pandas as pd
from PyQt4 import QtCore, QtGui

# Import Qt Ui classes
from Ui_ImportSignalFromMATWindow import Ui_ImportSignalFromMATWindow

from utils.ExtractSignal import ExtractSignalFromMAT


class ImportSignalFromMATWindow(QtGui.QMainWindow, Ui_ImportSignalFromMATWindow):
    
    MATimported = QtCore.pyqtSignal() #signal emitted when the signal is ready to send
    
    def __init__(self, filename):
        self.filename = str(filename)
        super(ImportSignalFromMATWindow, self).__init__()
        self.setupUi(self)
        self.initUI()
        
        
    def initUI(self):
        #Define slots
        self.pushButton_addColumn.clicked.connect(self.addColumnName)
        self.pushButton_removeColumn.clicked.connect(self.removeColumnName)
        self.radioButton_select_all.toggled.connect(self.selectAllVariables)
        self.tableWidget_input_preview.itemSelectionChanged.connect(self.updateVariableSelection)
        self.pushButton_Import.clicked.connect(self.importMATfile)
        
        """ DEBUG """ 
        #Define default values
        self.lineEdit_unit.setText("ms")
        
        #update file preview
        self.displayTabWidgetFilePreview()
        
        # Display the window
        self.show()
    
        
    def displayTabWidgetFilePreview(self):
        
        #Display a signal preview in table widget
        self.my_unit = str(self.lineEdit_unit.text())
        if self.my_unit == "":
            self.my_unit = "ms"
            
        self.input_data = ExtractSignalFromMAT(filename = self.filename, unit = self.my_unit)
        
        #Display a signal preview in table widget
        self.tableWidget_input_preview.setColumnCount(1 + len(self.input_data.columns));
        self.tableWidget_input_preview.setRowCount(10);
        
        #Display signal columns names
        Qcol_list = QtCore.QStringList()
        Qcol_list.append('Time ('+str(self.my_unit)+')')
        for col_name in self.input_data.columns.values :
            Qcol_list.append(col_name)
        self.tableWidget_input_preview.setHorizontalHeaderLabels(Qcol_list)
        
        # Display the 10 first lines of the signal
        for row_idx in range(10):
            item=QtGui.QTableWidgetItem()
            item.setText(QtCore.QString(str(self.input_data.index[row_idx])))
            self.tableWidget_input_preview.setItem(row_idx, 0, item)
            col_idx = 1
            for value in self.input_data.iloc[row_idx,:] :
                item=QtGui.QTableWidgetItem()
                item.setText(QtCore.QString.number(value))
                self.tableWidget_input_preview.setItem(row_idx, col_idx, item)
                col_idx += 1      
        self.tableWidget_input_preview.resizeColumnsToContents()        
        self.tableWidget_input_preview.setSelectionBehavior(QtGui.QAbstractItemView.SelectColumns)
        
        
        #Display a signal preview in table widget
        self.tableWidget_input_preview.setColumnCount(len(self.input_data.columns)+1);
        
        self.updateVariableSelection()
        
    
    def selectAllVariables(self, checked):
        if checked:
            self.tableWidget_input_preview.selectAll()
        else:
            self.tableWidget_input_preview.clearSelection()
    
    
    def updateVariableSelection(self):
        # Get selected variable in preview Tab widget
        selected_var_idx = [self.tableWidget_input_preview.selectedIndexes()[i].column()
                            for i in range(len(self.tableWidget_input_preview.selectedIndexes()))]
        selected_var_idx = sorted(set(selected_var_idx))

        self.selected_variables = []
        for i in selected_var_idx:
            if i != 0: #ignore if TimeIndex is selected
                self.selected_variables.append(int(self.input_data.columns.values[i-1]))    
        
            
    def addColumnName(self):
        # Get selected variable in preview Tab widget
        selected_var_idx = [self.listWidget_columns_names.selectedIndexes()[i].row()
                            for i in range(len(self.listWidget_columns_names.selectedIndexes()))]
        selected_var_idx = sorted(set(selected_var_idx))

        self.updateVariableSelection()
        
        if len(self.listWidget_columns_names) == len(self.selected_variables):
            mess = QtGui.QMessageBox.warning(self,
                        'Warning Message',
                        "You cannot add a new colomn name without selecting a new variable.")
            return
        
        new_col, ok = QtGui.QInputDialog.getText(self, 'Add a new column label', 
                    "Enter the new column name :")
        if ok :
            if len(selected_var_idx) == 0 : 
                self.listWidget_columns_names.addItem(new_col)
            else :
                self.listWidget_columns_names.insertItem(selected_var_idx[0]+1, new_col)
        
    
    def removeColumnName(self):
         # Get selected variable in preview Tab widget
        selected_var_idx = [self.listWidget_columns_names.selectedIndexes()[i].row()
                            for i in range(len(self.listWidget_columns_names.selectedIndexes()))]
        selected_var_idx = sorted(set(selected_var_idx))
        for i in selected_var_idx :
            self.listWidget_columns_names.takeItem(i)
        
        
    def importMATfile(self):
        if self.lineEdit_unit.text() == "" :
            mess = QtGui.QMessageBox.warning(self,
                        'Warning Message',
                        "You must define an time unit (ex:'ms').")
            return
        else :
            self.my_unit = str(self.lineEdit_unit.text())
        
        if len(self.listWidget_columns_names) != 0 :     
            if len(self.listWidget_columns_names) != len(self.selected_variables):
                mess = QtGui.QMessageBox.warning(self,
                            'Warning Message',
                            "You have selected "+ str(len(self.selected_variables))
                            + " variables and defined " + str(len(self.listWidget_columns_names))
                            + " variable names.\nImpossible to import.")
                return
            else: 
                columns_names = [str(self.listWidget_columns_names.item(i).text()) for i in range(self.listWidget_columns_names.count())]
        else :
            columns_names = [str(i) for i in self.selected_variables]
            
        self.input_signal = ExtractSignalFromMAT(  filename = self.filename,
                                                    columns_index=self.selected_variables, 
                                                    columns_wanted_names = columns_names,
                                                    unit = self.my_unit)
        
        self.MATimported.emit()
        self.close()
    
        