from PyQt4 import QtCore, QtGui

import importlib
import ast
import time
import numpy as np          # Mathematical package
import pandas as pd         # Time serie package
from Method import Method
from PyQt4.QtCore import pyqtSlot, pyqtSignal
from PyQt4.QtGui import QStyle
import multiprocessing
import sys
import matplotlib.pyplot as plt
import pickle
import os
from pprint import pformat, pprint
import csv

def debug(farg, *args):
    pass
    #print farg
    #for arg in args:
    #   print arg


class ArgumentQTextEdit(QtGui.QWidget):
    def __init__(self, label, type, parent = None):
        super(QtGui.QWidget, self).__init__(parent)
        self.type = type
        self.timer = None
        self.isValid = False
        self.label = label
        # horizontal layout
        horizontalLayout = QtGui.QHBoxLayout(self)
        horizontalLayout.setContentsMargins(0, 0, 0, 0)
        #self.setStyleSheet("QLabel { background-color : red}")
        #horizontalLayout.setAlignment(QtCore.Qt.AlignVCenter)
        if type==str or type==int or type==float:
            self.editWidget = QtGui.QTextEdit()
            self.editWidget.setObjectName("textEdit-" + label)
            self.editWidget.setAutoFillBackground(True)
            self.editWidget.setMaximumSize(QtCore.QSize(16777215, 24))
            self.editWidget.setAcceptRichText(False)
            self.editWidget.textChanged.connect(self.textChangedEvent)

        elif type==bool:
            self.editWidget = QtGui.QCheckBox()
            self.editWidget.setObjectName("checkBox-" + label)

        elif type==list:
            self.editWidget = QtGui.QComboBox()
            self.editWidget.setObjectName("comboBox-" + label)

        elif type==file:
            self.editWidget = QtGui.QPushButton()
            self.editWidget.setObjectName("pushButton-" + label)
            self.editWidget.setMaximumSize(QtCore.QSize(200, 24))
            #self.editWidget.setSizePolicy(QtCore.QSizePolicy.MinimumExpanding)
            self.editWidget.setStyleSheet("QPushButton { text-align: right; }")
            self.editWidget.setLayoutDirection(QtCore.Qt.RightToLeft)
            QtCore.QObject.connect(self.editWidget, QtCore.SIGNAL("clicked()"), self.selectFileDialog)

        horizontalLayout.addWidget(self.editWidget)
        
        # control
        self.controlWidget = QtGui.QLabel()
        self.controlWidget.setObjectName("control-" + label)
        self.controlWidget.setMaximumSize(QtCore.QSize(24, 24))
        horizontalLayout.addWidget(self.controlWidget)

        self.setLayout(horizontalLayout)

    @pyqtSlot()
    def selectFileDialog(self):
        fileName = fileName = QtGui.QFileDialog.getOpenFileName(self,
                        "Select a data file", "", "data File (*.*)")
        self.setText(fileName)
        self.textChangedEvent()


    @pyqtSlot()
    def textChangedEvent(self):
        if self.timer is not None:
            self.timer.stop()
            self.timer.deleteLater()

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.checkArgument)
        self.timer.setSingleShot(True)
        self.timer.start(1000)

    @pyqtSlot()
    def checkArgument(self):
        textValue = self.toPlainText()
        castingTo = self.type
        try:
            if castingTo == file and textValue == "":
                raise ValueError(self.label + " can't be empty")
            elif self.label:
                castingTo(textValue)
            else:
                raise ValueError(self.label+" can't be empty")
            self.controlWidget.setPixmap(MethodWidget.getOkPixmap())
            self.isValid = True
        except ValueError as e:
            self.isValid = False
            self.controlWidget.setPixmap(MethodWidget.getKoPixmap())
            self.controlWidget.setToolTip(e.message)

    def toPlainText(self):
        if self.type==file:
            return self.editWidget.text()
        else:
            return self.editWidget.toPlainText()

    def setPlainText(self, s):
        if self.type==file:
            return self.editWidget.setText(s)
        else:
            self.editWidget.setPlainText(s)

    def setText(self, s):
        self.editWidget.setText(s)

    def setCheckState(self, s):
        self.editWidget.setCheckState(s)

    def checkState(self):
        return self.editWidget.checkState()

    def addItem(self, s):
        self.editWidget.addItem(s)

    def isChecked(self):
        return self.editWidget.isChecked()

    def currentText(self):
        return self.editWidget.currentText()

    def count(self):
        return self.editWidget.count()

    def setCurrentIndex(self,index):
        self.editWidget.setCurrentIndex(index)

    def itemText(self,i):
        return self.editWidget.itemText(i)


class MethodWidget(QtGui.QWidget):

    currentMethod = None#Method()

    computationFinished = pyqtSignal()

    @staticmethod
    def getOkPixmap():
        return QtGui.qApp.style().standardIcon(QStyle.SP_DialogApplyButton).pixmap(12, 12)

    @staticmethod
    def getKoPixmap():
        return QtGui.qApp.style().standardIcon(QStyle.SP_DialogCancelButton).pixmap(12, 12)

    def __init__(self, parent=None):
        super(MethodWidget, self).__init__(parent)
        self.parent = parent
        self.verticalLayout = QtGui.QVBoxLayout(parent)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        #self.setSizePolicy(QtGui.QSizePolicy.Maximum,QtGui.QSizePolicy.Maximum)
        self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)

        self.verticalLayout.addLayout(self.formLayout)

        self.computeCheckTimer = QtCore.QTimer()

        QtCore.QObject.connect(self.computeCheckTimer, QtCore.SIGNAL("timeout()"), self.isComputing)

        self.isFocused = False
        # hashmaps to easy access to values
        self.widgetsValue = {}
        self.argumentsMap = {}
        self.methodResults = {}


    def name(self):
        return "MethodWidget"

    def toolTip(self):
        return ""

    def whatsThis(self):
        return ""

    def setMethod(self, name):
        self.name = name

    def populateArguments(self, methodPath):
        """
        :param methodPath: To the "Method" .py file that will be computed
        """
        self.moduleToLoad = methodPath.replace("/", ".")
        self.moduleToLoad = self.moduleToLoad.replace("\\", ".")
        # remove .py
        self.moduleToLoad = self.moduleToLoad[:-3]

        module_name, class_name = self.moduleToLoad.rsplit(".", 1)

        # dynamic load
        self.__class__.currentMethod = getattr(importlib.import_module(self.moduleToLoad), class_name)

        arguments = self.__class__.currentMethod.getArguments()
        self.buildForm(arguments)

        doc = self.__class__.currentMethod.__doc__
        if doc:
            doc = doc.replace('\n    ', '\n').strip()
        else:
            doc = ""
        return doc

    def clearArgumentList(self):
        self.widgetsValue.clear()
        self.argumentsMap.clear()
        layout = self.formLayout
        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().setParent(None)

    def buildForm(self, arguments):
        """ Build form widget for Method arguments UI
        """
        currentData = self.getArgumentsAsDictionary()

        # clear previous children
        layout = self.formLayout
        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().setParent(None)

        self.widgetsValue = {}
        self.argumentsMap = {}

        # create new children for arguments
        i = 0
        for argument in arguments:
            # label
            label = QtGui.QLabel(self.parent)
            label.setObjectName("label-"+argument.label)
            label.setText(argument.label)
            label.setMinimumSize(QtCore.QSize(24, 24))
            layout.setWidget(i, QtGui.QFormLayout.LabelRole, label)

            # textedit
            textEdit = ArgumentQTextEdit(argument.label, argument.type, self.parent)

            if argument.type==str or argument.type==int or argument.type==float or argument.type == file:
                if currentData[argument.label]:
                    textEdit.setText(str(currentData[argument.label]))
                else:
                    textEdit.setText(str(argument.value))
            elif argument.type==bool:
                if currentData[argument.label]:
                    textEdit.setCheckState(2)
                else:
                    textEdit.setCheckState(0)
            elif argument.type==list:
                for item in argument.value:
                    textEdit.addItem(str(item))
                if len(argument.value) != len(currentData[argument.label]):
                    for i in xrange(0, len(argument.value)):
                        if(textEdit.itemText(i) == currentData[argument.label]):
                            textEdit.setCurrentIndex(i)



            textEdit.setToolTip(argument.hint)
            if argument.hidden:
                label.setVisible(False)
                textEdit.setVisible(False)
                textEdit.setDisabled(True)

            #layout.setWidget(i, QtGui.QFormLayout.FieldRole, textEdit)
            layout.setWidget(i, QtGui.QFormLayout.FieldRole, textEdit)

            self.widgetsValue[argument.label] = textEdit
            self.argumentsMap[argument.label] = argument
            i += 1

    def getArgumentsAsDictionary(self):
        """ get methods arguments values from widgets and return as dictionary
        """
        argumentsAsDictionary = None
        if self.currentMethod:
            argumentsAsDictionary = self.currentMethod.getArgumentsAsDictionary()
            if argumentsAsDictionary:
                for arg in argumentsAsDictionary:
                    if self.widgetsValue.has_key(arg):
                        if self.widgetsValue[arg].type == bool:
                            if self.widgetsValue[arg].checkState() == 2:
                                #argumentsAsDictionary[arg] = self.widgetsValue[arg].checkState()
                                argumentsAsDictionary[arg] = True
                            else:
                                argumentsAsDictionary[arg] = False
                        elif self.widgetsValue[arg].type == list:
                            argumentsAsDictionary[arg] = str(self.widgetsValue[arg].currentText())
                        elif self.widgetsValue[arg].type == file:
                            textValue = self.widgetsValue[arg].toPlainText()
                            if textValue:
                                argumentsAsDictionary[arg] = file(textValue)
                        else:
                            textValue = self.widgetsValue[arg].toPlainText()
                            castingTo = self.argumentsMap[arg].type
                            argumentsAsDictionary[arg] = castingTo(textValue)


        return argumentsAsDictionary

    def setArgumentsWithDictionary(self, argumentsAsDictionary):
        """ set methods arguments values from widgets and return as dictionary
        """
        #for arg in argumentsAsDictionary:
        #    self.widgetsValue[arg].setPlainText(str(argumentsAsDictionary[arg]))
        if self.currentMethod:
            methodArguments = None
            methodArguments = self.currentMethod.getArgumentsAsDictionary()
            if argumentsAsDictionary and methodArguments:
                for arg in argumentsAsDictionary:
                    if self.widgetsValue.has_key(arg):
                        if self.widgetsValue[arg].type == bool:
                            if argumentsAsDictionary[arg] == True:
                                self.widgetsValue[arg].setCheckState(2)
                            else:
                                self.widgetsValue[arg].setCheckState(0)
                        elif self.widgetsValue[arg].type == list:
                            for i in xrange(0, len(methodArguments[arg])):
                                if(self.widgetsValue[arg].itemText(i) == argumentsAsDictionary[arg]):
                                    self.widgetsValue[arg].setCurrentIndex(i)
                        else:
                            self.widgetsValue[arg].setPlainText(str(argumentsAsDictionary[arg]))


    def compute(self, signals, outputBasename):
        try:
            dictionary = self.getArgumentsAsDictionary()
            self.computeProcess = self.currentMethod(**dictionary)

        except Exception, e:
            print >> sys.stderr, "Error: "+str(e)
            self.computationFinished.emit()
            return

        self.computeProcess.errorRaised = False
        self.computeProcess.setOutputFilename(outputBasename)
        self.computeProcess.resQueue = multiprocessing.Queue(0)

        self.methodResults = {}
        self.computationInterrupted = False

        self.computeProcess.start(signals, self.computeProcess.resQueue)
        self.computeCheckTimer.start(1000)

    def printResult(self, stdout):
        if stdout == sys.stdout:
            print >>stdout, "Results : " + self.getResult()
        else:
            print >>stdout, "Error : " + self.getResult()

    def getResult(self):
        s = "["
        original = np.get_printoptions()
        np.set_printoptions(precision=3, threshold=np.inf)
        if type(self.methodResults) is list:
            for key in self.methodResults.keys():
                s += key + " : " + pformat(self.methodResults[key]) + ", "
        elif type(self.methodResults) is tuple:
            for val in self.methodResults:
                s += pformat(val) + ", "
        else:
            s += pformat(self.methodResults)
        np.set_printoptions(**original)
        s += "]"
        return s

    @pyqtSlot()
    def stopComputeProcess(self):
        self.computeProcess.terminate()
        self.computationInterrupted = True


    @pyqtSlot()
    def isComputing(self):
        stdout = sys.stdout
        #if not self.currentMethod.computationInProgress:
        if self.computeProcess.is_alive():
            if self.computeProcess.resQueue.qsize() > 0:
                self.computeProcess.terminate()
                time.sleep(0.1)
        if not self.computeProcess.is_alive():
            self.computeCheckTimer.stop()
            if self.computationInterrupted:
                print "Computation interrupted!"
            elif self.computeProcess.resQueue.get(): #get if error occured
                stdout = sys.stderr

            filename = self.computeProcess.resQueue.get()
            time.sleep(2)
            self.methodResults = pickle.load(file(filename))
            self.printResult(stdout)
            os.remove(filename)

            if self.computeProcess._plot:
                for f in os.listdir(os.path.dirname(os.path.realpath(__file__))+"/../"):
                    if f.endswith(".plot"):
                        debug("Ploting results from: " + str(f))
                        try:
                            fig = pickle.load(file(str(f)))
                        except Exception, e:
                            print >> sys.stderr, "Error: " + str(e)
                        try:
                            debug("Removing file: " + str(f))
                            #delete all plot files
                            os.remove(f)
                        except Exception, e:
                            print >> sys.stderr, "Error: " + str(e)

                plt.ion()
                plt.show()
            debug("Process finished")
            self.computationFinished.emit()


    def event(self, event):
        if event.type() == 11: #mouse leave boundaries
            if self.isFocused:
                #print "mouse leave boundaries"
                self.isFocused = False
            return True
        elif event.type() == 2: #mosue pressed
            #print "mouse pressed"
            self.isFocused = True
            return True
        return False
