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
from Ui_ImportSignalFromELANWindow import Ui_ImportSignalFromELANWindow

from utils.ExtractSignal import ExtractSignalFromELAN


class ImportSignalFromELANWindow(QtGui.QMainWindow, Ui_ImportSignalFromELANWindow):
    
    ELANimported = QtCore.pyqtSignal() #signal emitted when the signal is ready to send
    
    def __init__(self, filename):
        self.filename = str(filename)
        super(ImportSignalFromELANWindow, self).__init__()
        self.setupUi(self)
        self.initUI()
        
        
    def initUI(self):
        #Define slots
        self.lineEdit_separator.textChanged.connect(self.displayTabWidgetFilePreview)
        self.pushButton_addColumn.clicked.connect(self.addColumnName)
        self.pushButton_removeColumn.clicked.connect(self.removeColumnName)
        self.pushButton_Import.clicked.connect(self.importELANfile)
        
        """ DEBUG """ 
        #Define default values
        self.lineEdit_separator.setText(";")
        self.spinBox_ele_per_second.setValue(5)
        self.listWidget_columns_names.addItem('Actor')
        self.listWidget_columns_names.addItem(' ')
        self.listWidget_columns_names.addItem('t_begin')
        self.listWidget_columns_names.addItem('t_end')
        self.listWidget_columns_names.addItem('duration')
        self.listWidget_columns_names.addItem('Action')
        self.listWidget_columns_names.addItem('video') 
        self.lineEdit_Actor.setText('Maman')
        self.lineEdit_Action.setText('all')
        
        #update file preview
        self.displayTabWidgetFilePreview()
        
        # Display the window
        self.show()
    
    
    def displayTabWidgetColumnsName(self):
        columns_names = [str(self.listWidget_columns_names.item(i).text()) for i in range(self.listWidget_columns_names.count())]
        Qcol_list = QtCore.QStringList()
        self.tableWidget_input_preview.setHorizontalHeaderLabels(Qcol_list)
        
        for col_name in columns_names :
            Qcol_list.append(col_name)
        for empt in range(len(columns_names), self.tableWidget_input_preview.columnCount()) :
            Qcol_list.append("")
            
        self.tableWidget_input_preview.setHorizontalHeaderLabels(Qcol_list)
        self.tableWidget_input_preview.resizeColumnsToContents()
        
        
    def displayTabWidgetFilePreview(self):
        input_data = pd.DataFrame()
        if str(self.lineEdit_separator.text()) != "" : 
            input_data = pd.read_csv(self.filename, str(self.lineEdit_separator.text()))
        else : 
            input_data = pd.read_csv(self.filename)
        
        #Display a signal preview in table widget
        self.tableWidget_input_preview.setColumnCount(len(input_data.columns));
        self.tableWidget_input_preview.setRowCount(10);
        
        self.displayTabWidgetColumnsName()
        
        # Display the 5 first lines of the signal
        for row_idx in range(10):
            item=QtGui.QTableWidgetItem()
            item.setText(QtCore.QString(str(input_data.index[row_idx])))
            col_idx = 0
            for value in input_data.iloc[row_idx,:] :
                item=QtGui.QTableWidgetItem()
                if isinstance(value, str) :
                    item.setText(QtCore.QString(value))
                else :
                    item.setText(QtCore.QString.number(value))
                self.tableWidget_input_preview.setItem(row_idx, col_idx, item)
                col_idx += 1        
        self.tableWidget_input_preview.resizeColumnsToContents()
        
        
    def addColumnName(self):
        # Get selected variable in preview Tab widget
        selected_var_idx = [self.listWidget_columns_names.selectedIndexes()[i].row()
                            for i in range(len(self.listWidget_columns_names.selectedIndexes()))]
        selected_var_idx = sorted(set(selected_var_idx))
        
        new_col, ok = QtGui.QInputDialog.getText(self, 'Add a new column label', 
                    "Enter the new column name :")
        if ok :
            if len(selected_var_idx) == 0 : 
                self.listWidget_columns_names.addItem(new_col)
            else :
                self.listWidget_columns_names.insertItem(selected_var_idx[0]+1, new_col)
        
        self.displayTabWidgetColumnsName()
        
    
    def removeColumnName(self):
         # Get selected variable in preview Tab widget
        selected_var_idx = [self.listWidget_columns_names.selectedIndexes()[i].row()
                            for i in range(len(self.listWidget_columns_names.selectedIndexes()))]
        selected_var_idx = sorted(set(selected_var_idx))
        for i in selected_var_idx :
            self.listWidget_columns_names.takeItem(i)
        
        self.displayTabWidgetColumnsName()
        
        
    def importELANfile(self):
        if self.lineEdit_separator.text() == "" :
            mess = QtGui.QMessageBox.warning(self,
                        'Warning Message',
                        "You must define a file separator.")
            return
        else :
            sep = str(self.lineEdit_separator.text())
        
        if self.spinBox_ele_per_second.value() <= 0 :
            mess = QtGui.QMessageBox.warning(self,
                        'Warning Message',
                        "You must define a striclty positive number of elements.")
            return
        else :
            ele_per_sec = self.spinBox_ele_per_second.value()
        
        if self.listWidget_columns_names.count() == 0 :
            mess = QtGui.QMessageBox.warning(self,
                        'Warning Message',
                        "You must define all columns names")
            return
        else: 
            columns_names = [str(self.listWidget_columns_names.item(i).text()) for i in range(self.listWidget_columns_names.count())]

        if self.lineEdit_Actor.text() == "" :
            mess = QtGui.QMessageBox.warning(self,
                        'Warning Message',
                        "You must define an Actor label.")
            return
        else :
            my_Actor = str(self.lineEdit_Actor.text())
            
        if self.lineEdit_Action.text() == "" :
            mess = QtGui.QMessageBox.warning(self,
                        'Warning Message',
                        "You must define an Action label.")
            return
        else :
            my_Action = str(self.lineEdit_Action.text())    
            
        self.input_signal = ExtractSignalFromELAN(  filename = self.filename,
                                                    separator = sep,
                                                    columns_name = columns_names,
                                                    total_duration = 0,
                                                    ele_per_sec = ele_per_sec,
                                                    Actor = my_Actor,
                                                    Action = my_Action)
        
        self.ELANimported.emit()
        self.close()
    
        