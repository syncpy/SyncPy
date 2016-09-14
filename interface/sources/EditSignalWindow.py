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

import numpy as np
import pandas as pd
from PyQt4 import QtCore, QtGui

# Import Qt Ui classes
from Ui_EditSignalWindow import Ui_EditSignalWindow

from Signal import Signal
from utils import Normalize
from utils import ConvertContinueToBinary

large_font = QtGui.QFont()
large_font.setPointSize(12)
large_font.setBold(True)
large_font.setWeight(75)

class EditSignalWindow(QtGui.QMainWindow, Ui_EditSignalWindow):
    
    signalEdited = QtCore.pyqtSignal() #signal emitted when the signal is ready to send
    
    def __init__(self, signals_dict, selected_signal_name):
        self.signals_dict = signals_dict
        self.my_signal_name = selected_signal_name
        #Make a copy of the original signal
        self.my_signal = Signal(selected_signal_name,
                                self.signals_dict[selected_signal_name]._signal_data.copy(),
                                self.signals_dict[selected_signal_name]._signal_type,
                                self.signals_dict[selected_signal_name]._signal_data_type)
        
        super(EditSignalWindow, self).__init__()
        self.setupUi(self)
        self.initUI()
        
        
    def initUI(self):
        #Define slots
        self.radioButton_select_all_variables.toggled.connect(self.selectAllVariables)
        self.tableWidget_signal_preview.itemSelectionChanged.connect(self.updateVariableSelection)
        self.pushButton_rename_signal.clicked.connect(self.renameSignal)
        self.pushButton_resample_signal.clicked.connect(self.resampleSignal)
        self.pushButton_interpolate_signal.clicked.connect(self.interpolateSignal)
        self.pushButton_cut_signal.clicked.connect(self.cutSignal)
        self.pushButton_rename_variable.clicked.connect(self.renameVariable)
        self.pushButton_remove_variable.clicked.connect(self.removeVariable)
        self.pushButton_normalize_variable.clicked.connect(self.normalizeVariable)
        self.pushButton_convertIntoBinary.clicked.connect(self.convertVariableIntoBinary)
        self.pushButton_visualize.clicked.connect(self.visualizeSignal)
        self.pushButton_apply_changes.clicked.connect(self.applyChanges)
        
        # Display the name of the selected signal for edition
        self.label_selected_signal_name.setFont(large_font)
        self.label_selected_signal_name.setText(self.my_signal._signal_name)
        
        # Display signal preview
        self.displaySignalPreview()
        
        #Enabled buttons
        self.pushButton_rename_variable.setEnabled(False)
        self.pushButton_remove_variable.setEnabled(False)
        self.pushButton_normalize_variable.setEnabled(False)
        self.pushButton_convertIntoBinary.setEnabled(False)
        
        # Display the window
        self.show()
    
    
    def displaySignalPreview(self):
        self.tableWidget_signal_preview.setSelectionBehavior(QtGui.QAbstractItemView.SelectColumns)
        
        #Display a signal preview in table widget
        self.tableWidget_signal_preview.setColumnCount(1 + len(self.my_signal._signal_data.columns));
        self.tableWidget_signal_preview.setRowCount(10);
        
        #Display signal columns names
        Qcol_list = QtCore.QStringList()
        Qcol_list.append(self.my_signal._signal_data.index.name)
        for col_name in self.my_signal._signal_data.columns.values :
            Qcol_list.append(col_name)
        self.tableWidget_signal_preview.setHorizontalHeaderLabels(Qcol_list)
        
        # Display the 10 first lines of the signal
        for row_idx in range(10):
            item=QtGui.QTableWidgetItem()
            item.setText(QtCore.QString(str(self.my_signal._signal_data.index[row_idx])))
            self.tableWidget_signal_preview.setItem(row_idx, 0, item)
            col_idx = 1
            for value in self.my_signal._signal_data.iloc[row_idx,:] :
                item=QtGui.QTableWidgetItem()
                item.setText(QtCore.QString.number(value))
                self.tableWidget_signal_preview.setItem(row_idx, col_idx, item)
                col_idx += 1
                
        self.tableWidget_signal_preview.resizeColumnsToContents()

    
    def selectAllVariables(self, checked):
        if checked:
            self.tableWidget_signal_preview.selectAll()
        else:
            self.tableWidget_signal_preview.clearSelection()
    
    
    def updateVariableSelection(self):
        # Get selected variable in preview Tab widget
        selected_var_idx = [self.tableWidget_signal_preview.selectedIndexes()[i].column()
                            for i in range(len(self.tableWidget_signal_preview.selectedIndexes()))]
        selected_var_idx = sorted(set(selected_var_idx))

        if len(selected_var_idx) == 0:
            self.pushButton_rename_variable.setEnabled(False)
            self.pushButton_remove_variable.setEnabled(False)
            self.pushButton_normalize_variable.setEnabled(False)
            self.pushButton_convertIntoBinary.setEnabled(False)
        else:
            self.pushButton_rename_variable.setEnabled(True)
            self.pushButton_remove_variable.setEnabled(True)
            self.pushButton_normalize_variable.setEnabled(True)
            self.pushButton_convertIntoBinary.setEnabled(True)
       
        if len(selected_var_idx) >= len(self.my_signal._signal_data.columns):
            self.pushButton_remove_variable.setEnabled(False)
        
    
    def renameSignal(self):
        new_name, ok = QtGui.QInputDialog.getText(self, 'Rename Signal', 
            "Enter the new signal's name for " + self.my_signal._signal_name + " :")
        
        if ok:
            if str(new_name) in self.signals_dict.keys():
                mess = QtGui.QMessageBox.warning(self,
                                                'Warning Message',
                                                "This signal's name already exist.")
            else :
                self.my_signal._signal_name = str(new_name).strip()
                self.label_selected_signal_name.setFont(large_font)
                self.label_selected_signal_name.setText(self.my_signal._signal_name)

    
    
    def resampleSignal(self):
        rule, ok = QtGui.QInputDialog.getText(self, 'Resample Signal', 
            "Give a rule for the resampling (ex: 100ms) :")
        if ok : 
            self.my_signal._signal_data = self.signals_dict[self.my_signal_name]._signal_data.resample(rule=str(rule))
            self.displaySignalPreview()

    
    def interpolateSignal(self):
        limit, ok = QtGui.QInputDialog.getInt(self, 'Interpolate Signal', 
            "Give a maximal number of consecutive NaN values to fill :", value = 0, min = 0) 
        
        if ok :
            self.my_signal._signal_data = self.my_signal._signal_data.interpolate(limit=limit, inplace = False)
            self.displaySignalPreview()
    
    
    def cutSignal(self):
        index_begin, ok = QtGui.QInputDialog.getInt(self, 'Cut Signal', 
            "Give the first index of the cut signal :", value = 0, min = 0)
        
        if ok :
            index_end, ok2 = QtGui.QInputDialog.getInt(self, 'Cut Signal', 
            "Give the last index of the cut signal :", value = index_begin + 1, min = index_begin + 1)
            
            if ok2 :
                if index_end >= len(self.my_signal._signal_data.index) : 
                    reply = QtGui.QMessageBox.information(self, 'Info',
                                "The given last index is higher than the length of the signal. \n" +
                                "The cut will go up to the signal's end ")
                    index_end = len(self.my_signal._signal_data.index) - 1
                self.my_signal._signal_data = self.my_signal._signal_data[index_begin : index_end]
                self.displaySignalPreview()
            
            
    def renameVariable(self):
        # Get selected variable in preview Tab widget
        selected_var_idx = [self.tableWidget_signal_preview.selectedIndexes()[i].column()
                            for i in range(len(self.tableWidget_signal_preview.selectedIndexes()))]
        selected_var_idx = sorted(set(selected_var_idx))
        
        selected_variables = []
        for i in selected_var_idx:
            if i != 0: #ignore if TimeIndex is selected
                selected_variable = self.my_signal._signal_data.columns.values[i-1]
        
                new_name, ok = QtGui.QInputDialog.getText(self, 'Rename Variable ', 
                    "Enter the new variable's name for " + selected_variable + " :")
                if ok:
                    self.my_signal._signal_data.rename(columns={selected_variable : str(new_name).strip()}, inplace = True)
                    self.displaySignalPreview()
        
    
    def removeVariable(self):
        # Get selected variable in preview Tab widget
        selected_var_idx = [self.tableWidget_signal_preview.selectedIndexes()[i].column()
                            for i in range(len(self.tableWidget_signal_preview.selectedIndexes()))]
        selected_var_idx = sorted(set(selected_var_idx))
        
        selected_variables = []
        for i in selected_var_idx:
            if i != 0: #ignore if TimeIndex is selected
                selected_variable = self.my_signal._signal_data.columns.values[i-1]
        
                reply = QtGui.QMessageBox.question(self, 'Message',
                    "Do you want to remove "+ selected_variable +" variable?",
                    QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.Yes)
                
                if reply == QtGui.QMessageBox.Yes:
                    old_signal_type = self.my_signal._signal_type
                    old_signal_data_type = self.my_signal._signal_data_type
                    self.my_signal._signal_data.drop(selected_variable, axis=1, inplace=True)
                    
                    # Update signal type
                    new_signal_type = 0 if(len(self.my_signal._signal_data.columns) == 1) else 1
                    if old_signal_type != new_signal_type :
                        self.my_signal._signal_type = new_signal_type
                        reply = QtGui.QMessageBox.information(self, 'Info',
                                self.my_signal._signal_name + " is now a Monovariate signal. ")
                        
                    #Update signal data type
                    self.updateSignalDataType(old_signal_data_type)                                       
        self.displaySignalPreview()
        
        
    def normalizeVariable(self):
        # Get selected variable in preview Tab widget
        selected_var_idx = [self.tableWidget_signal_preview.selectedIndexes()[i].column()
                            for i in range(len(self.tableWidget_signal_preview.selectedIndexes()))]
        selected_var_idx = sorted(set(selected_var_idx))
        
        selected_variables = []
        for i in selected_var_idx:
            if i != 0: #ignore if TimeIndex is selected
                selected_variable = self.my_signal._signal_data.columns.values[i-1]
                
                min_value, min_ok = QtGui.QInputDialog.getInt(self, 'Normalize Variable', 
                "Give a minimal value for the normalization of " + selected_variable + " :", value = 0)
                if min_ok:
                    max_value, max_ok = QtGui.QInputDialog.getInt(self, 'Normalize Variable', 
                    "Give a maximal value for the normalization of " + selected_variable + " :", value = min_value + 1)
                    if max_ok:
                        self.my_signal._signal_data[selected_variable] = Normalize.Normalize(
                                            pd.DataFrame(self.my_signal._signal_data[selected_variable]),
                                            min_value, max_value)
                        self.displaySignalPreview()
    
    
    def convertVariableIntoBinary(self):
        # Get selected variable in preview Tab widget
        selected_var_idx = [self.tableWidget_signal_preview.selectedIndexes()[i].column()
                            for i in range(len(self.tableWidget_signal_preview.selectedIndexes()))]
        selected_var_idx = sorted(set(selected_var_idx))
        
        selected_variables = []
        for i in selected_var_idx:
            if i != 0: #ignore if TimeIndex is selected
                selected_variable = self.my_signal._signal_data.columns.values[i-1]
                
                mean_data = np.mean(self.my_signal._signal_data[selected_variable].values)
                thresh, ok = QtGui.QInputDialog.getDouble(self, 'Convert Variable into Binary', 
                    "Give a threshold for the conversion into binary of " + selected_variable + " :", value = mean_data)
                if ok:
                    reply = QtGui.QMessageBox.question(self, 'Message',
                            "Do you want to maximize " + selected_variable + " ?",
                            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.Yes)
                    if reply == QtGui.QMessageBox.Yes:
                        maximize = True
                    else:
                        maximize = False
                    
                    old_signal_data_type = self.my_signal._signal_data_type
                    self.my_signal._signal_data[selected_variable] = ConvertContinueToBinary.ConvertContinueToBinary(
                                            pd.DataFrame(self.my_signal._signal_data[selected_variable]),
                                            thresh, maximize)
                    
                    #Update signal data type
                    self.updateSignalDataType(old_signal_data_type)
                    self.displaySignalPreview()


    def updateSignalDataType(self, old_signal_data_type):
        # update signal data type
        is_categorical = True
        col_idx = 0
        while is_categorical and col_idx < len(self.my_signal._signal_data.columns) :
            number_val = len(sorted(set(self.my_signal._signal_data.iloc[:,col_idx])))
            if number_val > 2:
                is_categorical = False
            col_idx += 1;
        new_signal_data_type = 1 if(is_categorical) else 0
        
        if old_signal_data_type != new_signal_data_type :
            self.my_signal._signal_data_type = new_signal_data_type
            str_my_data_type = "Continuous" if(new_signal_data_type==0) else "Categorical"
            reply = QtGui.QMessageBox.information(self, 'Info',
                    self.my_signal._signal_name + " is now a " + str_my_data_type +" signal. ")
                        
        
    def visualizeSignal(self):
        # Get selected variable in preview Tab widget
        selected_var_idx = [self.tableWidget_signal_preview.selectedIndexes()[i].column()
                            for i in range(len(self.tableWidget_signal_preview.selectedIndexes()))]
        selected_var_idx = sorted(set(selected_var_idx))

        selected_variables = []
        for i in selected_var_idx:
            if i != 0: #ignore if TimeIndex is selected
                selected_variables.append(self.my_signal._signal_data.columns.values[i-1])
        if len(selected_variables) == 0 : 
            selected_variables = self.my_signal._signal_data.columns   
        self.my_signal.plot_signal(selected_variables)


    def applyChanges(self):
        self.close()
        
    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'Message',
            "Do you want to apply changes to "+ self.my_signal_name +" signal?",
            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.Yes)

        if reply == QtGui.QMessageBox.Yes:
            self.signalEdited.emit()
            event.accept() # let the window close
        else:
            event.accept() # let the window close
