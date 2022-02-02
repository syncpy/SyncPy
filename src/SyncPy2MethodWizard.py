# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test_interface.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

import sys
import importlib
import re


from PyQt5 import QtCore, QtGui, uic
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QStandardItem
from PyQt5.QtWidgets import QFileDialog
from .Method import Method, MethodArg, MethodArgList
from string import Template
from .ui.SyncpyAbout import SyncpyAbout

import configparser

sys.path.insert(0, '.')
sys.path.insert(0, 'Methods')

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

# Main Window Class
class SyncPy2MethodWizard(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QDialog.__init__(self)

        self.config = configparser.RawConfigParser()
        self.config.read('conf.ini')

        self.ui = uic.loadUi("ui/SyncpyMethodWizard.ui", self)
        QtCore.QMetaObject.connectSlotsByName(self)

        self.appVersion = self.getFromConfig('app.version')
        self.appName = self.getFromConfig('app.name')

        table = self.ui.argsTable
        table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        QtCore.QObject.connect(table, QtCore.SIGNAL("customContextMenuRequested(QPoint)"),
                               self.openMenuToolbox)
        QtCore.QObject.connect(self.ui.argTypeComboBox, QtCore.SIGNAL("currentIndexChanged(int)"),
                               self.setDefaultArgument)

        self.model = QtGui.QStandardItemModel()
        self.model.setColumnCount(4)
        headers = []
        headers.append("Name")
        headers.append("Type")
        headers.append("Default value")
        headers.append("Hint")
        self.model.setHorizontalHeaderLabels(headers)
        table.setModel(self.model)
        table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)

        self.highlighter = ui.PythonSyntax.PythonHighlighter(self.ui.codePlainTextEdit.document())

        self.showStatus("{0} (v {1}) successfully loaded".format(self.appName, self.appVersion))
        self.ui.show()

    def getFromConfig(self, attribute):
        return self.config.get(self.__class__.__name__, attribute)

    @pyqtSlot()
    def setDefaultArgument(self):
        type = self.ui.argTypeComboBox.currentText()
        if type == "bool":
            self.ui.argDefaultLineEdit.setText("False")
        elif type == "int":
            self.ui.argDefaultLineEdit.setText("0")
        elif type == "float":
            self.ui.argDefaultLineEdit.setText("0.0")
        elif type == "list":
            self.ui.argDefaultLineEdit.setText("['arg1','arg2']")
        elif type == "str":
            self.ui.argDefaultLineEdit.setText("'arg'")


    @pyqtSlot()
    def addArgument(self):
        name = self.ui.argNameLineEdit.text()
        default = self.ui.argDefaultLineEdit.text()
        type = self.ui.argTypeComboBox.currentText()
        hint = self.ui.argHintLineEdit.text()

        if name.trimmed().isEmpty() or default.trimmed().isEmpty():
            self.showStatus("Cannot add argument: name or default value empty")
            return
        for i in range(self.model.rowCount()):
            item = self.model.item(i)
            if item.text() == name.replace( " ", "" ):
                self.showStatus("Cannot add argument: argument already existing")
                return

        item = [QStandardItem(name.replace( " ", "" )), QStandardItem(type), QStandardItem(default.replace( " ", "" )), QStandardItem(hint)]


        self.model.appendRow(item)
        self.showStatus("Method argument added")


    @pyqtSlot()
    def generatePy(self):
        name = self.ui.nameTextEdit.text()
        author = self.ui.authorTextEdit.text()
        desc = self.ui.descriptionTextEdit.toPlainText()

        type = self.ui.variatComboBox.currentText()
        categ = self.ui.categoryComboBox.currentText()
        sigNumber = self.ui.inputSignalNumberComboBox.currentText()

        rowCount = self.model.rowCount()
        colCount = self.model.columnCount()
        argList = MethodArgList()
        for i in range(0, rowCount):
            argList.append(self.model.item(i, 0).text()
                           , self.model.item(i, 2).text()
                           , self.model.item(i, 1).text()
                           , self.model.item(i, 3).text())

        self.generatePython(name, author, desc, type, categ, sigNumber, argList)


    def generatePython(self,name, author, descr, type, categ, sigNumber, argList):
        argsListStr = ""
        argListStrInit = ""

        for arg in argList.getMethodArgs():

            argsListStr += "argsList.append('{0}', {1}, {2}, '{3}')\n   ".format(arg.label,
                                                                           arg.value,
                                                                           arg.type,
                                                                           arg.hint)
            argListStrInit += ", {0}={1}".format(arg.label, arg.value)

        argListStrInit = "def __init__(self{0}, ** kwargs):".format(argListStrInit)

        f = open('ui/MethodTemplate.txt', 'r')
        template = Template(f.read())
        dic = dict(name=name, author=author, descr=descr.replace("\n", "\n   "), type=type, categ=categ,
                   argsListStr=argsListStr,
                   argListStrInit=argListStrInit)
        pythonStr = template.safe_substitute(dic)

        self.ui.codePlainTextEdit.setPlainText(pythonStr)

        self.showStatus("Python code generated")


    def openMenuToolbox(self, position):
        row = self.ui.argsTable.indexAt(position).row()

        menu = QtGui.QMenu("Menu", self)
        menu.addAction("delete row", lambda: self.deleteRow(row))
        # Show the context menu.
        menu.exec_(self.ui.argsTable.mapToGlobal(position))

    @pyqtSlot()
    def deleteRow(self, rowNum):
        self.model.removeRow(rowNum)

    def showStatus(self, msg):
        self.ui.statusbar.showMessage(msg)

    def savePy(self):
        name = self.ui.nameTextEdit.text()

        folder = self.getFolder()

        folder += "/"+name+".py"

        filename = QFileDialog.getSaveFileName(self, "Save Method in Python file", folder,
                                             'Python File (*.py)')

        if filename != "":
            f = open(filename, 'w')
            f.write(self.ui.codePlainTextEdit.toPlainText())
            f.close()
            self.showStatus("File '{0}' written".format(filename))

    def getFolder(self):
        type = self.ui.variatComboBox.currentText()
        categ = self.ui.categoryComboBox.currentText()
        sigNumber = self.ui.inputSignalNumberComboBox.currentText()
        linear = self.ui.linearComboBox.currentText()

        folder = "Methods"
        if sigNumber == "1":
            folder += "/utils"
        elif sigNumber == "2":
            folder += "/DataFrom2Persons"
        else:
            folder += "/DataFromManyPersons"

        if sigNumber != "1":
            folder += "/" + type
            folder += "/" + categ
            folder += "/" + linear

        return folder

    @pyqtSlot()
    def openAbout(self):
        SyncpyAbout(self, self.config, self.__class__.__name__).open()

    @pyqtSlot()
    def loadFromExistingMethod(self):
        folder = self.getFolder()
        filename = QFileDialog.getOpenFileName(self, "Open existing Method from a Python file", folder,
                                    'Python File (*.py)')

        if filename != "":
            f = open(filename, 'r')
            pythonStr = f.read()
            f.close()

            self.ui.codePlainTextEdit.setPlainText(pythonStr)

            #Author
            authorIndex = pythonStr.find(".. moduleauthor:: ")
            if authorIndex > -1:
                authorEndIndex = pythonStr.index("\n", authorIndex)
                author = pythonStr[authorIndex +len(".. moduleauthor:: "):authorEndIndex]
                self.ui.authorTextEdit.setText(author)

            # class & module name
            lastIndex = filename.lastIndexOf('/')
            folderSelected = filename.left(lastIndex)

            basename = filename.mid(lastIndex+1)
            folder = folderSelected.mid(folderSelected.indexOf("/Methods")+1)
            lst = basename.split(".py")
            className = lst[0]
            self.ui.nameTextEdit.setText(className)

            moduleToLoad = folder.replace('/','.')+'.'+className
            path = moduleToLoad.split('.')
            # category, type, number of signals
            if path[1] == 'DataFrom2Persons':
                self.ui.inputSignalNumberComboBox.setCurrentIndex(self.ui.inputSignalNumberComboBox.findText("2"))
            elif path[1] == 'DataFromManyPersons':
                self.ui.inputSignalNumberComboBox.setCurrentIndex(self.ui.inputSignalNumberComboBox.findText(">2"))
            else:
                self.ui.inputSignalNumberComboBox.setCurrentIndex(self.ui.inputSignalNumberComboBox.findText("1"))

            if len(path) > 2:
                self.ui.variatComboBox.setCurrentIndex(self.ui.variatComboBox.findText(path[2]))
                if len(path) > 3:
                    self.ui.categoryComboBox.setCurrentIndex(self.ui.categoryComboBox.findText(path[3]))
                    if len(path) > 4:
                        self.ui.linearComboBox.setCurrentIndex(self.ui.linearComboBox.findText(path[4]))

            # dynamic instrospection of the Class
            print("Loading Class {0}".format(moduleToLoad))
            currentMethod = getattr(importlib.import_module(str(moduleToLoad)), str(className))

            if currentMethod.__doc__:
                self.ui.descriptionTextEdit.setPlainText(currentMethod.__doc__.strip().replace("\n    ", "\n"))

            self.model.removeRows(0, self.model.rowCount())

            arguments = currentMethod.getArguments()
            if arguments:
                for arg in arguments:
                    p = re.compile("<type '(\w+)'>")
                    m = p.match(str(arg.type))
                    type = m.group(1)
                    if type == "str":
                        value = "'{0}'".format(arg.value)
                    else:
                        value = "{0}".format(arg.value)
                    item = [QStandardItem(arg.label),
                            QStandardItem(QString(str(m.group(1)))),
                            QStandardItem(QString(value)),
                            QStandardItem(arg.hint)]
                    self.model.appendRow(item)

            self.showStatus("Method {0} imported".format(filename))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    print((sys.argv))
    MainWindow = QtGui.QMainWindow()
    ui = SyncPy2MethodWizard()

    sys.exit(app.exec_())
