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

'''----- To be able to import Ui files -----'''
import sys
sys.path.insert(0, 'ui_files/')

import os
import numpy as np
import pandas as pd
from PyQt4 import QtCore, QtGui
import csv

# Import Qt Ui classes
from Ui_MainWindow import Ui_MainWindow

# Import classes
from MethodSelectionWindow import MethodSelectionWindow
from AddSignalWindow import AddSignalWindow
from EditSignalWindow import EditSignalWindow
from SynchronyMethod import SynchronyMethod
from Signal import Signal 

large_font = QtGui.QFont()
large_font.setPointSize(12)
large_font.setBold(True)
large_font.setWeight(75)

        
class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        
        self.signals_dict = {}
        self.methods_dict = {}
         
        super(MainWindow, self).__init__()
        self.setupUi(self)
        
        self.initUI()
        self.initMethods()       
       
    """""""""""""""""""""""
    """"Initialization"""""
    """""""""""""""""""""""    
    def initUI(self):
        """Enable widgets"""
        #tab_signals
        self.pushButton_remove_signal.setEnabled(False)
        self.pushButton_edit_signal.setEnabled(False)
        
        self.updateSignalsTable()
        
        """Hide unvisible widgets"""
        #tab_methods
        self.label_choose_method.setVisible(False)
        self.comboBox_methods.setVisible(False)
        self.pushButton_valid_method.setVisible(False)
        self.label_method.setVisible(False)
        self.label_method_selected.setVisible(False)
        
        #tab_compute
        self.label_available_signals.setVisible(False)
        self.listWidget_available_signals.setVisible(False)
        self.label_select_parameters.setVisible(False)
        self.pushButton_compute_method.setVisible(False)
        self.label_choose_output.setVisible(False)
        self.label_choose_output_file.setVisible(False)
        self.lineEdit_output_folder.setVisible(False)
        self.lineEdit_output_filename.setVisible(False)
        self.pushButton_browse_output_folder.setVisible(False)
        self.pushButton_save_file.setVisible(False)
        
        """Define slots"""
        #tab_home
        self.pushButton_start.clicked.connect(self.letStart)
        
        #tab_signals
        self.pushButton_add_signal.clicked.connect(self.openAddSignalWindow)
        self.pushButton_remove_signal.clicked.connect(self.removeSignal)
        self.pushButton_edit_signal.clicked.connect(self.openEditSignalWindow)
        
        #tab_methods
        self.button_Yes.clicked.connect(self.chooseMethodInList)
        self.button_No.clicked.connect(self.openMethodSelectionWindow)
        self.pushButton_valid_method.clicked.connect(self.displaySelectedMethod)
        
        #tab_compute
        self.tabWidget.currentChanged.connect(self.updateComputeTab)
        self.listWidget_available_signals.itemClicked.connect(self.updateSelectedSignals)
        self.pushButton_compute_method.clicked.connect(self.computeSelectedMethod)
        self.pushButton_browse_output_folder.clicked.connect(self.browseOutputFolder)
        self.pushButton_save_file.clicked.connect(self.saveResult)
        
        # Initialize main window size
        screen = QtGui.QDesktopWidget().screenGeometry()
        self.setGeometry(screen.width()*1/6, screen.height()*1/8, screen.width()*2/3,screen.height()*3/4)
        
        self.show()
    
    
    """""""""""""""""""""""""""""
    """"tab_home Functions """"""
    """""""""""""""""""""""""""""
    def letStart(self):
       self.tabWidget.setCurrentIndex(1)
    
    
    """""""""""""""""""""""""""""
    """"tab_signal Functions"""""
    """""""""""""""""""""""""""""
    def openAddSignalWindow(self):
        self.newSignal = AddSignalWindow(self.signals_dict)
        self.newSignal.signalSaved.connect(self.addNewSignal)
    
    
    def addNewSignal(self) :
        self.signals_dict[self.newSignal.my_signal_name] = self.newSignal.my_signal
        self.updateSignalsTable()
    
    
    def removeSignal(self) :
        # Get selected signals in in the tab
        selected_signals_idx = [self.tableWidget_exisitng_signals.selectedIndexes()[i].row()
                            for i in range(len(self.tableWidget_exisitng_signals.selectedIndexes()))]
        selected_signals_idx = sorted(set(selected_signals_idx))
        
        #Remove the selected signals
        for i in selected_signals_idx:
            selected_signal_name = str(self.tableWidget_exisitng_signals.item(i,0).text())
            self.signals_dict.pop(selected_signal_name)
        self.updateSignalsTable()
    
    
    def openEditSignalWindow(self):
        # Get selected signals in in the tab
        selected_signals_idx = [self.tableWidget_exisitng_signals.selectedIndexes()[i].row()
                            for i in range(len(self.tableWidget_exisitng_signals.selectedIndexes()))]
        selected_signals_idx = sorted(set(selected_signals_idx))
        
        #Edit only the first signal
        if len(selected_signals_idx) > 0 : 
            selected_signal_name = str(self.tableWidget_exisitng_signals.item(selected_signals_idx[0],0).text())
            self.editedSignal = EditSignalWindow(self.signals_dict, selected_signal_name)
            self.editedSignal.signalEdited.connect(self.editSignal)

    
    def editSignal(self) :
        self.signals_dict.pop(self.editedSignal.my_signal_name)
        self.signals_dict[self.editedSignal.my_signal._signal_name] = self.editedSignal.my_signal
        
        self.updateSignalsTable()
        
        
    def updateSignalsTable(self):
        self.tableWidget_exisitng_signals.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        nb_signals = len(self.signals_dict)
        
        # Enable others buttons
        self.pushButton_remove_signal.setEnabled(False) if (nb_signals == 0) else self.pushButton_remove_signal.setEnabled(True)
        self.pushButton_edit_signal.setEnabled(False) if (nb_signals == 0) else self.pushButton_edit_signal.setEnabled(True)
            
        # Initialize table size
        self.tableWidget_exisitng_signals.setColumnCount(4);
        self.tableWidget_exisitng_signals.setRowCount(nb_signals);
        
        # Define columns name
        Qcol_list = QtCore.QStringList()
        Qcol_list.append("Name")
        Qcol_list.append("Variables")
        Qcol_list.append("Type")
        Qcol_list.append("Data Type")
        self.tableWidget_exisitng_signals.setHorizontalHeaderLabels(Qcol_list)
    
        # Update table 
        count = 0
        key_list = self.signals_dict.keys()
        key_list.sort()
        for key in key_list : 
            item=QtGui.QTableWidgetItem()
            item.setText(QtCore.QString(key))
            self.tableWidget_exisitng_signals.setItem(count, 0, item) # Signal's name
            
            str_my_variables = self.signals_dict[key]._signal_data.columns.values[0]
            for x in range(len(self.signals_dict[key]._signal_data.columns.values)-1):
                str_my_variables +=  ", " + self.signals_dict[key]._signal_data.columns.values[x+1]
            item=QtGui.QTableWidgetItem()    
            item.setText(QtCore.QString(str_my_variables))
            self.tableWidget_exisitng_signals.setItem(count, 1, item) # Variables
            
            str_my_signal_type = "Univariate" if(self.signals_dict[key]._signal_type==0) else "Multivariate"
            item=QtGui.QTableWidgetItem()
            item.setText(QtCore.QString(str_my_signal_type))
            self.tableWidget_exisitng_signals.setItem(count, 2, item) # Signal's type
            
            str_my_data_type = "Continuous" if(self.signals_dict[key]._signal_data_type==0) else "Categorical"
            item=QtGui.QTableWidgetItem()
            item.setText(QtCore.QString(str_my_data_type))
            self.tableWidget_exisitng_signals.setItem(count, 3, item) # Data type
            
            count +=1
        
        self.tableWidget_exisitng_signals.resizeColumnsToContents()
    
    
    """""""""""""""""""""""""""""  
    """"tab_methods Functions""""
    """""""""""""""""""""""""""""
    def initMethods(self):       
        for element in os.listdir('method_files'):
            if element.endswith('.csv'):
                input_data = pd.DataFrame()
                input_data = pd.read_csv('method_files/' + element, sep=',', index_col=0 )
                
                try : 
                    self.methods_dict[input_data.at['Name','Value']] = SynchronyMethod(input_data.at['Name','Value'],
                                                                                       input_data.at['Type','Value'],
                                                                                       input_data.at['Data_Type','Value'],
                                                                                       input_data.at['Signal_Type','Value'],
                                                                                       input_data.at['Number_User_Type','Value'],
                                                                                       input_data.at['Description','Value'])
                except ValueError, err_msg :
                    self.statusbar.clearMessage()
                    self.statusbar.showMessage("Cannot import method from" + element + " : " +  str(err_msg))
                    break
                except Exception, e :
                    self.statusbar.clearMessage()
                    self.statusbar.showMessage("Exception in import method from" + element + " : " +str(e))
                    break
                
                method_parameters = {}
                method_parameters_descr = {}
                for col in input_data.columns.values :
                    if(col != 'Value') :
                        method_parameters[input_data.at['Parameter_name',col]] = input_data.at['Parameter_type',col]
                        method_parameters_descr[input_data.at['Parameter_name',col]] = input_data.at['Parameter_description',col]
                
                try :     
                    self.methods_dict[input_data.at['Name','Value']].defineConstructorParameters(method_parameters)
                except ValueError, err_msg :
                    self.statusbar.clearMessage()
                    self.statusbar.showMessage("Cannot import attributes from " + element + " : " +  str(err_msg))
                    break
                except Exception, e :
                    self.statusbar.clearMessage()
                    self.statusbar.showMessage("Exception in import attributes from " + element + " : " +str(e))
                    break
                    
                try :
                    self.methods_dict[input_data.at['Name','Value']].defineParametersDescriptions(method_parameters_descr)
                except ValueError, err_msg :
                    self.statusbar.clearMessage()
                    self.statusbar.showMessage("Cannot import attributes description from " + element + " : " +  str(err_msg))
                    break
                except Exception, e :
                    self.statusbar.clearMessage()
                    self.statusbar.showMessage("Exception in import attributes description from " + element + " : " +str(e))
                    break
        
        count = 0
        key_list = self.methods_dict.keys()
        key_list.sort()
        for key in key_list :
            self.comboBox_methods.addItem(key)
            self.comboBox_methods.setItemData(count, self.methods_dict[key]._method_description, QtCore.Qt.ToolTipRole)
            count += 1 

        
    def chooseMethodInList(self):    
        self.label_choose_method.setVisible(True)
        self.comboBox_methods.setVisible(True)
        self.pushButton_valid_method.setVisible(True)
    
    
    def displaySelectedMethod(self):
        self.label_method.setVisible(True)
        self.label_method_selected.setFont(large_font)
        self.label_method_selected.setText(self.comboBox_methods.currentText())
        self.label_method_selected.setVisible(True)
    
    
    def displaySelectedMethod_2(self):
        self.label_method.setVisible(True)
        self.label_method_selected.setFont(large_font)
        self.label_method_selected.setText(self.selectionMethodWindow.method_selected)
        self.label_method_selected.setVisible(True)
    
    
    def openMethodSelectionWindow(self):
        self.label_choose_method.setVisible(False)
        self.comboBox_methods.setVisible(False)
        self.pushButton_valid_method.setVisible(False)
        self.label_method.setVisible(False)
        self.label_method_selected.setVisible(False)
        
        self.selectionMethodWindow = MethodSelectionWindow(self.methods_dict)
        self.selectionMethodWindow.methodChosen.connect(self.displaySelectedMethod_2)
        
    """""""""""""""""""""""""""""  
    """"tab_compute Functions""""
    """""""""""""""""""""""""""""    
    def updateComputeTab(self, index):
        if index == 3 :
            if str(self.label_method_selected.text()) != "" : 
                self.method_selected = self.methods_dict[str(self.label_method_selected.text())]
                self.label_selected_method.setFont(large_font)
                self.label_selected_method.setText(self.method_selected._method_name)
                
                self.createMethodParametersWidgets()
                self.updateAvailableSignals()
                
                self.pushButton_compute_method.setVisible(True)
                self.pushButton_compute_method.setEnabled(False)
                
                self.label_choose_output.setVisible(False)
                self.label_choose_output_file.setVisible(False)
                self.lineEdit_output_folder.setVisible(False)
                self.lineEdit_output_filename.setVisible(False)
                self.pushButton_browse_output_folder.setVisible(False)
                self.pushButton_save_file.setVisible(False)
                
            else :
                self.label_selected_method.setText("You must select a method in the Method Tab")
                self.label_available_signals.setVisible(False)
                self.listWidget_available_signals.setVisible(False)
                self.label_select_parameters.setVisible(False)
                self.pushButton_compute_method.setVisible(False)
                
                self.label_choose_output.setVisible(False)
                self.label_choose_output_file.setVisible(False)
                self.lineEdit_output_folder.setVisible(False)
                self.lineEdit_output_filename.setVisible(False)
                self.pushButton_browse_output_folder.setVisible(False)
                self.pushButton_save_file.setVisible(False)
            self.statusbar.clearMessage()
       
    
    def createMethodParametersWidgets(self):
        self.clearLayout(self.formLayout_method_parameters)
        
        parameters = self.method_selected._method_constructor_parameters
        
        key_list = parameters.keys()
        key_list.sort()
        for key in key_list :
            widget_param_name = QtGui.QLabel(key)
            widget_param_name.setToolTip(self.method_selected._method_parameters_description[key])
            
            if parameters[key] == bool :
                widget_param_type = QtGui.QRadioButton()
                widget_param_type.setAutoExclusive(False)
            elif parameters[key] == int :
                widget_param_type = QtGui.QSpinBox()
                widget_param_type.setRange(-2000000000, 2000000000)
            elif parameters[key] == float :
                widget_param_type = QtGui.QDoubleSpinBox()
                widget_param_type.setRange(-2000000000, 2000000000)
            elif parameters[key] == str :
                widget_param_type = QtGui.QLineEdit()
            else :
                widget_param_type = QtGui.QLabel()
                widget_param_type.setText("ERROR")      
            widget_param_type.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
            widget_param_type.setMinimumHeight(20)
            widget_param_type.setMaximumHeight(40)
            widget_param_type.setToolTip(self.method_selected._method_parameters_description[key])
            
            self.formLayout_method_parameters.addRow(widget_param_name, widget_param_type)
    
    
    def clearLayout(self, layout):
        if layout != None:
            while layout.count():
                child = layout.takeAt(0)
                if child.widget() is not None:
                    child.widget().deleteLater()
                elif child.layout() is not None:
                    clearLayout(child.layout())
     
          
    def updateAvailableSignals(self) :
        self.label_available_signals.setVisible(True)
        self.listWidget_available_signals.setVisible(True)
        self.label_select_parameters.setVisible(True)
        self.listWidget_available_signals.clear()
        self.available_signals_dict = {} #Initialize available signal dict 
        self.selected_signals_dict = {} #Initialize selected signal dict 
        key_list = self.signals_dict.keys()
        key_list.sort()
        for key in key_list : 
            if self.method_selected._method_signal_type == 0 : # Univariate signal, decompose multivariate with each variable
                for var in self.signals_dict[key]._signal_data.columns.values :
                    var_data_type = 1
                    number_val = len(sorted(set(self.signals_dict[key]._signal_data[var])))
                    if number_val > 2 :
                        var_data_type = 0
                    if self.method_selected._method_data_type == var_data_type :
                        item = QtGui.QListWidgetItem(self.signals_dict[key]._signal_name + " - " + var)
                        item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
                        item.setCheckState(QtCore.Qt.Unchecked)
                        self.listWidget_available_signals.addItem(item)
                        
                        self.available_signals_dict[self.signals_dict[key]._signal_name + " - " + var] = Signal(
                                                                  self.signals_dict[key]._signal_name + " - " + var,
                                                                  pd.DataFrame(self.signals_dict[key]._signal_data[var].values,
                                                                               self.signals_dict[key]._signal_data[var].index),
                                                                  self.signals_dict[key]._signal_type,
                                                                  var_data_type)            
            else :
                if self.method_selected._method_data_type == self.signals_dict[key]._signal_data_type :
                    item = QtGui.QListWidgetItem(self.signals_dict[key]._signal_name)
                    item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
                    item.setCheckState(QtCore.Qt.Unchecked)
                    self.listWidget_available_signals.addItem(item)
                    
                    self.available_signals_dict[key] = self.signals_dict[key]
                
            str_my_signal_type = "Univariate" if(self.method_selected._method_signal_type==0) else "Multivariate"
            str_my_data_type = "Continuous" if(self.method_selected._method_data_type==0) else "Categorical"
            self.label_available_signals.setText("Select signals : \n" +
                                                 "(The list presents only " +
                                                 str_my_signal_type + " and " +
                                                 str_my_data_type + " signals)")
    
    
    def updateSelectedSignals(self, item) :
        if item.checkState() == QtCore.Qt.Checked :
            if str(item.text()) in self.selected_signals_dict.keys() :
                self.selected_signals_dict.pop(str(item.text()))
            item.setCheckState(QtCore.Qt.Unchecked)
            
        else:
            if self.method_selected._method_number_user_type == 0 : 
                if len(self.selected_signals_dict.keys()) == 2 :
                    mess = QtGui.QMessageBox.warning(self,
                                            'Warning Message',
                                            "The selected method is for 2 users, you cannot select more than 2 signals")
                    return
                
            self.selected_signals_dict[str(item.text())] = self.available_signals_dict[str(item.text())]
            # Rename selected signal variable name if monovariate method
            if self.method_selected._method_signal_type == 0 : 
                self.selected_signals_dict[str(item.text())]._signal_data.columns = [str(item.text())]
            item.setCheckState(QtCore.Qt.Checked)
            
        if self.method_selected._method_number_user_type == 0 :    
            if len(self.selected_signals_dict) == 2 : 
                self.pushButton_compute_method.setEnabled(True)
            else :
                self.pushButton_compute_method.setEnabled(False)
        else :
            if len(self.selected_signals_dict)!= 0 : 
                self.pushButton_compute_method.setEnabled(True)
            else :
                self.pushButton_compute_method.setEnabled(False)
            
            
    def computeSelectedMethod(self) :
        # Reset unvisible widgets
        self.label_choose_output.setVisible(False)
        self.label_choose_output_file.setVisible(False)
        self.lineEdit_output_folder.setVisible(False)
        self.lineEdit_output_filename.setVisible(False)
        self.pushButton_browse_output_folder.setVisible(False)
        self.pushButton_save_file.setVisible(False)
        self.statusbar.clearMessage()
        
        # Get parameters values
        isViz = False
        parameters = self.method_selected._method_constructor_parameters
        parameters_values = {} 
        for count in range(0, self.formLayout_method_parameters.count(), 2):
            row_label = self.formLayout_method_parameters.itemAt(count).widget()
            row_widget = self.formLayout_method_parameters.itemAt(count+1).widget()
            if isinstance(row_widget, QtGui.QRadioButton) :
                if (str(row_label.text()) == "plot") :
                    isViz = row_widget.isChecked()
                else :
                    parameters_values[str(row_label.text())] = row_widget.isChecked()
            elif isinstance(row_widget, QtGui.QSpinBox) :
                parameters_values[str(row_label.text())] = row_widget.value()
            elif isinstance(row_widget, QtGui.QDoubleSpinBox) :
                parameters_values[str(row_label.text())] = row_widget.value()
            elif isinstance(row_widget, QtGui.QLineEdit) :
                parameters_values[str(row_label.text())] = str(row_widget.text())
        
        # Import the module for the selected method
        try : 
            self.method_selected.importMethodModule()
        except Exception, e :
            self.statusbar.clearMessage()
            self.statusbar.showMessage(str(e))
            return
        
        # Initialize the selected method with the parameters
        try :
            self.method_selected.initMethod(parameters_values)
        except Exception, e :
            self.statusbar.clearMessage()
            self.statusbar.showMessage(str(e))
            return
        
        # Compute
        signal_list = []
        for signal in self.selected_signals_dict.values() :
            signal_list.append(signal._signal_data)

        is_compute_ok = False
        try :    
            is_compute_ok = self.method_selected.computeMethod(signal_list)
        except Exception, e :
            self.statusbar.clearMessage()
            self.statusbar.showMessage(str(e))
            return
        
        #Vizualize results if plot is wanted
        if isViz :
            try :
                self.method_selected.visualizeResult()
            except Exception, e :
                self.statusbar.clearMessage()
                self.statusbar.showMessage(str(e))
                return
        
        if is_compute_ok :
            self.statusbar.clearMessage()
            self.label_choose_output.setVisible(True)
            self.label_choose_output_file.setVisible(True)
            self.lineEdit_output_folder.setVisible(True)
            self.lineEdit_output_filename.setVisible(True)
            self.pushButton_browse_output_folder.setVisible(True)
            self.pushButton_save_file.setVisible(True)
            
            #Define dafault filename :
            self.lineEdit_output_filename.setText(self.method_selected._method_name + '_Result')
            self.lineEdit_output_folder.setText(os.path.abspath('../'))
            
            
    def browseOutputFolder(self) :
        self.file_path = QtGui.QFileDialog.getExistingDirectory(None, 'Select a folder for saving result.')
        self.lineEdit_output_folder.setText(self.file_path)


    def saveResult(self):
        output_file_path = str(self.lineEdit_output_folder.text()) + "\\" + str(self.lineEdit_output_filename.text())
        
        if type(self.method_selected._compute_result) == pd.DataFrame : 
            # Record result into csv
            self.method_selected._compute_result.to_csv(output_file_path  + ".csv")
            
            if os.path.isfile(output_file_path  + ".csv") :
              reply = QtGui.QMessageBox.information(self, 'Info',
                                "The file " + str(self.lineEdit_output_filename.text()) + ".csv"
                                " has been saved in :\n" +
                                 str(self.lineEdit_output_folder.text()) + "\\")
        
        elif type(self.method_selected._compute_result) == dict:
            # Record result into csv
            with open(output_file_path  + ".csv", 'wb') as f:  # Just use 'w' mode in 3.x
                w = csv.DictWriter(f, self.method_selected._compute_result.keys())
                w.writeheader()
                w.writerow(self.method_selected._compute_result)
                
            if os.path.isfile(output_file_path  + ".csv") :
              reply = QtGui.QMessageBox.information(self, 'Info',
                                "The file " + str(self.lineEdit_output_filename.text()) + ".csv"
                                " has been saved in :\n" +
                                 str(self.lineEdit_output_folder.text()) + "\\")
                
        elif type(self.method_selected._compute_result) == tuple or type(self.method_selected._compute_result) == list :
            for i in range(len(self.method_selected._compute_result)):
                if type(self.method_selected._compute_result[i]) == pd.DataFrame :
                    # Record result into csv
                    self.method_selected._compute_result[i].to_csv(output_file_path + "_"  + str(i+1) + ".csv")
                    
                    if os.path.isfile(output_file_path  + "_"  + str(i) + ".csv") :
                      reply = QtGui.QMessageBox.information(self, 'Info',
                                        "The file " + str(self.lineEdit_output_filename.text()) + "_"  + str(i+1) + ".csv"
                                        " has been saved in :\n" +
                                         str(self.lineEdit_output_folder.text()) + "\\")
                      
                elif type(self.method_selected._compute_result[i]) == dict:
                    # Record result into csv
                    with open(output_file_path + "_"  + str(i+1) + ".csv", 'wb') as f:  # Just use 'w' mode in 3.x
                        w = csv.DictWriter(f, self.method_selected._compute_result[i].keys())
                        w.writeheader()
                        w.writerow(self.method_selected._compute_result[i])
                        
                    if os.path.isfile(output_file_path  + "_"  + str(i) + ".csv") :
                      reply = QtGui.QMessageBox.information(self, 'Info',
                                        "The file " + str(self.lineEdit_output_filename.text()) + str(i+1) + ".csv"
                                        " has been saved in :\n" +
                                         str(self.lineEdit_output_folder.text()) + "\\")
              
                else :
                    reply = QtGui.QMessageBox.warning(self, 'Warning',
                                        "The file " + str(self.lineEdit_output_filename.text()) + "_"  + str(i+1) + ".csv"
                                        " cannot be created")   
        else :
            reply = QtGui.QMessageBox.warning(self, 'Warning',
                                "The file " + str(self.lineEdit_output_filename.text()) + ".csv"
                                " cannot be created")
            
def main():   
    app = QtGui.QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()