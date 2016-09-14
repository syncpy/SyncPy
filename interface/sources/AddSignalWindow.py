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

import sys
import os
import numpy as np
import pandas as pd
from PyQt4 import QtCore, QtGui

# Import Qt Ui classes
from Ui_AddSignalWindow import Ui_AddSignalWindow

from ImportSignalFromELANWindow import ImportSignalFromELANWindow
from ImportSignalFromMATWindow import ImportSignalFromMATWindow
from Signal import Signal 

from utils.ExtractSignal import ExtractSignalFromCSV

class AddSignalWindow(QtGui.QMainWindow, Ui_AddSignalWindow):
    
    signalSaved = QtCore.pyqtSignal() #signal emitted when the signal is ready to send
    
    def __init__(self, signals_dict):
        self.signals_dict = signals_dict
        
        super(AddSignalWindow, self).__init__()
        self.setupUi(self)
        self.initUI()
        
        
    def initUI(self):
        #Hide unvisible widgets
        self.radioButton_csv_ELAN_file.setVisible(False)
        self.radioButton_csv_file.setVisible(False)
        self.radioButton_mat_file.setVisible(False)
        self.label_time_unit.setVisible(False)
        self.lineEdit_time_unit.setVisible(False)
        self.pushButton_import_file.setVisible(False)
        self.label_signal_preview.setVisible(False)
        self.tableWidget_signal_preview.setVisible(False)
        self.label_select_variables.setVisible(False)
        self.radioButton_select_all_variables.setVisible(False)
        self.label_signal_name.setVisible(False)
        self.lineEdit_signal_name.setVisible(False)
        self.pushButton_visualize.setVisible(False)
        self.pushButton_save_signal.setVisible(False)
        
        #Define slots
        self.pushButton_browse.clicked.connect(self.browseFiles)
        self.pushButton_import_file.clicked.connect(self.importFile)
        self.lineEdit_file_path.textChanged.connect(self.resetImport)
        self.radioButton_csv_ELAN_file.clicked.connect(self.defineTimeUnit)
        self.radioButton_csv_file.clicked.connect(self.defineTimeUnit)
        self.radioButton_mat_file.clicked.connect(self.defineTimeUnit) 
        self.radioButton_select_all_variables.toggled.connect(self.selectAllVariables)
        self.tableWidget_signal_preview.itemSelectionChanged.connect(self.updateVariableSelection)
        self.pushButton_visualize.clicked.connect(self.visualizeSignal)
        self.pushButton_save_signal.clicked.connect(self.saveSignal)
        
        # Display the window
        self.show()
    
    def browseFiles(self):
        self.file_path = QtGui.QFileDialog.getOpenFileName(None, 'Select a file.', "*.csv;;*.mat")
        self.lineEdit_file_path.setText(self.file_path)

        self.radioButton_csv_file.setVisible(True)
        self.radioButton_csv_ELAN_file.setVisible(True)
        self.radioButton_mat_file.setVisible(True)
        self.pushButton_import_file.setVisible(True)
        
        self.radioButton_csv_ELAN_file.setChecked(False)
        
        
        """ DEBUG """ 
        self.lineEdit_time_unit.setText("ms")
        
        if str(self.lineEdit_file_path.text()).find(".mat") != -1 :
            self.radioButton_csv_file.setChecked(False)
            self.radioButton_mat_file.setChecked(True)
            self.label_time_unit.setVisible(False)
            self.lineEdit_time_unit.setVisible(False)
        else :
            self.radioButton_csv_file.setChecked(True)
            self.radioButton_mat_file.setChecked(False)
            self.label_time_unit.setVisible(True)
            self.lineEdit_time_unit.setVisible(True)
              
        
    def importFile(self):
        if self.lineEdit_file_path.text() == "" :
            mess = QtGui.QMessageBox.warning(self,
                        'Warning Message',
                        "You must enter a file complete path")
            return
        if (os.path.isfile(self.lineEdit_file_path.text()) == False):
            mess = QtGui.QMessageBox.warning(self,
                        'Warning Message',
                        "You must enter an existing file path")
            return
    
        if self.radioButton_csv_file.isChecked() :
            if self.lineEdit_time_unit.text() == "" :
                mess = QtGui.QMessageBox.warning(self,
                            'Warning Message',
                            "You must define a time unit.")
                return
            self.importCsvFile()
            
        elif self.radioButton_csv_ELAN_file.isChecked() :
            self.importFileFromELAN()
            
        elif self.radioButton_mat_file.isChecked() :
            self.importFileFromMat()    
        
            
                
    def defineTimeUnit(self, checked):
        sender = self.sender() #get the current sender of the slot
        if sender == self.radioButton_csv_file:
            if self.radioButton_csv_file.isChecked() :
                self.label_time_unit.setVisible(True)
                self.lineEdit_time_unit.setVisible(True)
            else :
                self.label_time_unit.setVisible(False)
                self.lineEdit_time_unit.setVisible(False)
            self.radioButton_csv_ELAN_file.setChecked(not(checked))
            self.radioButton_mat_file.setChecked(not(checked))
            
        if sender == self.radioButton_csv_ELAN_file:
            if self.radioButton_csv_ELAN_file.isChecked() :
                self.label_time_unit.setVisible(False)
                self.lineEdit_time_unit.setVisible(False)
            else:
                self.label_time_unit.setVisible(True)
                self.lineEdit_time_unit.setVisible(True)
            self.radioButton_csv_file.setChecked(not(checked))    
            self.radioButton_mat_file.setChecked(not(checked))
            
        if sender == self.radioButton_mat_file:
            if self.radioButton_mat_file.isChecked() :
                self.label_time_unit.setVisible(False)
                self.lineEdit_time_unit.setVisible(False)
            else:
                self.label_time_unit.setVisible(True)
                self.lineEdit_time_unit.setVisible(True)
            self.radioButton_csv_file.setChecked(not(checked))
            self.radioButton_csv_ELAN_file.setChecked(not(checked))
        
        self.resetImport()
        
            
    def importCsvFile(self):
        self.data_unit = str(self.lineEdit_time_unit.text())
        self.input_data = ExtractSignalFromCSV(str(self.file_path), unit = self.data_unit)
        
        self.displaySignalPreview()

        self.label_signal_name.setVisible(True)
        self.lineEdit_signal_name.setVisible(True)
        self.pushButton_visualize.setVisible(True)
        self.pushButton_save_signal.setVisible(True)
        
        """ DEBUG """ 
        self.lineEdit_signal_name.setText("mySignal")
        
    
    def importFileFromELAN(self):
        self.importELAN = ImportSignalFromELANWindow(self.lineEdit_file_path.text())
        self.importELAN.ELANimported.connect(self.saveELANInputData)              

    def importFileFromMat(self):
        self.importMAT = ImportSignalFromMATWindow(self.lineEdit_file_path.text())
        self.importMAT.MATimported.connect(self.saveMATInputData)    
    

    def resetImport(self):
        self.label_signal_preview.setVisible(False)
        self.tableWidget_signal_preview.setVisible(False)
        self.label_select_variables.setVisible(False)
        self.radioButton_select_all_variables.setVisible(False)
        self.label_signal_name.setVisible(False)
        self.lineEdit_signal_name.setVisible(False)
        self.pushButton_visualize.setVisible(False)
        self.pushButton_save_signal.setVisible(False)
        
        
    def saveELANInputData(self):
        self.input_data = self.importELAN.input_signal
        self.data_unit = "ms"
        
        self.displaySignalPreview()

        self.label_signal_name.setVisible(True)
        self.lineEdit_signal_name.setVisible(True)
        self.pushButton_visualize.setVisible(True)
        self.pushButton_save_signal.setVisible(True)
        
        
    def saveMATInputData(self):
        self.input_data = self.importMAT.input_signal
        self.data_unit = self.importMAT.my_unit
        
        self.displaySignalPreview()

        self.label_signal_name.setVisible(True)
        self.lineEdit_signal_name.setVisible(True)
        self.pushButton_visualize.setVisible(True)
        self.pushButton_save_signal.setVisible(True)    
    
        
    def displaySignalPreview(self):
        self.tableWidget_signal_preview.setSelectionBehavior(QtGui.QAbstractItemView.SelectColumns)
        
        #Display a signal preview in table widget
        self.tableWidget_signal_preview.setColumnCount(1 + len(self.input_data.columns));
        self.tableWidget_signal_preview.setRowCount(10);
        
        #Display signal columns names
        Qcol_list = QtCore.QStringList()
        Qcol_list.append('Time ('+str(self.data_unit)+')')
        for col_name in self.input_data.columns.values :
            Qcol_list.append(col_name)
        self.tableWidget_signal_preview.setHorizontalHeaderLabels(Qcol_list)
        
        # Display the 10 first lines of the signal
        for row_idx in range(10):
            item=QtGui.QTableWidgetItem()
            item.setText(QtCore.QString(str(self.input_data.index[row_idx])))
            self.tableWidget_signal_preview.setItem(row_idx, 0, item)
            col_idx = 1
            for value in self.input_data.iloc[row_idx,:] :
                item=QtGui.QTableWidgetItem()
                item.setText(QtCore.QString.number(value))
                self.tableWidget_signal_preview.setItem(row_idx, col_idx, item)
                col_idx += 1      
        self.tableWidget_signal_preview.resizeColumnsToContents()
        
        self.label_signal_preview.setVisible(True)
        self.tableWidget_signal_preview.setVisible(True)
        self.label_select_variables.setVisible(True)
        self.radioButton_select_all_variables.setVisible(True)
        
        self.updateVariableSelection()

    
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

        self.selected_variables = []
        for i in selected_var_idx:
            if i != 0: #ignore if TimeIndex is selected
                self.selected_variables.append(self.input_data.columns.values[i-1])

        # Update data_type
        is_categorical = True
        col_idx = 0
        while is_categorical and col_idx < len(selected_var_idx) :
            number_val = len(sorted(set(self.input_data.iloc[:,selected_var_idx[col_idx]-1])))
            if number_val > 2:
                is_categorical = False
            col_idx += 1;
         
        if(is_categorical) : self.my_data_type = 1
        else : self.my_data_type = 0
        
        
    def createMySignal(self):
        self.updateVariableSelection()
        if len(self.tableWidget_signal_preview.selectedIndexes()) == 0:
            mess = QtGui.QMessageBox.warning(self,
                                            'Warning Message',
                                            "You must select at least one variable for the signal.")
            return False
        if str(self.lineEdit_signal_name.text()) == "":
            mess = QtGui.QMessageBox.warning(self,
                                            'Warning Message',
                                            "You must define a signal name.")
            return False
        
        if str(self.lineEdit_signal_name.text()) in self.signals_dict.keys():
            mess = QtGui.QMessageBox.warning(self,
                                            'Warning Message',
                                            "This signal's name already exist.")
            return False
        
        # Keep input data in case of modifications
        self.my_signal_data = self.input_data.copy() 

        # Modify signal to corresponds to selected type
        self.my_signal_data = self.my_signal_data.loc[:,self.selected_variables]
        self.my_signal_data = pd.DataFrame(self.my_signal_data.values, self.my_signal_data.index, self.selected_variables)

        # get signal's type
        if(len(self.my_signal_data.columns) == 1):
            self.my_signal_type = 0 # Univariate signal
        else:
            self.my_signal_type = 1 # Multivariate signal
        
        # Get signal's name
        self.my_signal_name = str(self.lineEdit_signal_name.text()).strip()
        
        #Create a new Signal instance
        self.my_signal = Signal(self.my_signal_name, self.my_signal_data, self.my_signal_type, self.my_data_type)
        
        return True
                
                
    def visualizeSignal(self):
        # Keep input data in case of modifications
        viz_signal_data = self.input_data.copy()
        if len(self.selected_variables) > 0 : 
            viz_signal_data = viz_signal_data.loc[:,self.selected_variables]
            viz_signal_data = pd.DataFrame(viz_signal_data.values, viz_signal_data.index, self.selected_variables)
            
            # get signal's type
            viz_signal_type = 0 if(len(viz_signal_data.columns) == 1) else 1
            
            viz_signal = Signal(str(self.lineEdit_signal_name.text()), viz_signal_data, viz_signal_type, self.my_data_type)
            viz_signal.plot_signal()
        else :
            mess = QtGui.QMessageBox.warning(self,
                            'Warning Message',
                            "You must define at least one variable to plot.")
            return

        
    def saveSignal(self):
        created = self.createMySignal()
        
        if created : 
            # Open message box to present signals informations
            mess = QtGui.QMessageBox()
            mess.setWindowTitle('New Signal created')
            mess.setText("The signal "+ self.my_signal_name + " has been created")
            str_my_signal_type = "Univariate" if(self.my_signal_type==0) else "Multivariate"
            str_my_data_type = "Continuous" if(self.my_data_type==0) else "Categorical"
            str_my_variables = self.selected_variables[0]
            for x in range(len(self.selected_variables)-1):
                str_my_variables += ", " + self.selected_variables[x+1]
            mess.setInformativeText("Variables : " +str_my_variables + "\n" +
                                    "Signal type : " + str_my_signal_type + "\n" +
                                    "Data type : " + str_my_data_type+ "\n" +
                                    "\n"+
                                    "Do you want to add the signal ?")
            yesButton = mess.addButton(QtGui.QMessageBox.Yes)
            noButton = mess.addButton(QtGui.QMessageBox.No)
            mess.exec_()
        
            if mess.clickedButton() == yesButton:
                self.signalSaved.emit()  
                
    
    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'Message',
            "Do you want to quit?",
            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.Yes)

        if reply == QtGui.QMessageBox.Yes:
            event.accept() # let the window close
        else:
            event.ignore()
