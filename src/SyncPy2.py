# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test_interface.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

import json
import os
import subprocess
import sys
import time

sys.path.insert(0, '.')
sys.path.insert(0, 'Methods')

from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtCore import pyqtSlot
from PyQt4.QtGui import QStyle, QFileDialog

#from src import Method
import matplotlib
matplotlib.use('Qt4Agg')
from ui.HeaderFileWizard import HeaderFileWizard
from ui.MethodWidget import MethodWidget
from ui.OutLog import OutLog
from ui.Tools import Tools
from ui.SyncpyAbout import SyncpyAbout
import matplotlib.pyplot as plot
import pandas as pd
import webbrowser
from scipy.io import loadmat
from collections import OrderedDict
import ConfigParser

from Methods.utils.ExtractSignal import ExtractSignalFromCSV
from Methods.utils.ExtractSignal import ExtractSignalFromMAT

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
class SyncPy2(QtGui.QMainWindow):
    COLOR_GREY = QtGui.QColor(200, 200, 200)

    def __init__(self):
        QtGui.QDialog.__init__(self)
        geo = QtGui.QDesktopWidget().availableGeometry()
        self.maxHeight = geo.height() - 100
        self.maxWidth = geo.width() - 50

        self.sessionHasBeenLoaded = False
        self.lastSavedSessionFilename = ""
        self.selectedDirectory = ""
        self.outputDirectory = ""
        self.methodUsed = ""
        self.columnSeparator = ","
        self.signalsHeader = []
        self.filesSelected = []
        self.nFilesSelected = 0
        self.signalsSelected = []
        self.nSignalsSelected = 0
        self.signalsRefreshed = False
        self.signals = []
        self.dataFiles = []
        self.recreateMethodList = False
        self.firstFile = ""
        self.filesHasHeaders = False


        self.syncpyplatform = ""
        self.plotImgPath = ""
        self.headerMap = OrderedDict()
        if sys.platform == 'darwin':
            os.system("export LC_ALL=en_US.UTF-8")
            os.system("export LANG=en_US.UTF-8")
            self.syncpyplatform = "m"
        elif sys.platform == 'win32':
            self.syncpyplatform = "w"
        elif sys.platform == 'linux2':
            self.syncpyplatform = "u"

        #load config file
        self.config = ConfigParser.RawConfigParser()
        self.config.read('conf.ini')
        self.appVersion = self.getFromConfig('app.version')
        self.appName = self.getFromConfig('app.name')
        self.syncpyver = self.getFromConfig('sessionVersion')

        self.plotImgPath = self.getFromConfig("plotImgPath")

        self.ui = uic.loadUi(self.getFromConfig("uiFile"), self)
        QtCore.QMetaObject.connectSlotsByName(self)

        table = self.ui.inputSignalsWidget
        table.setColumnCount(3)
        headers = QtCore.QStringList("Name")
        headers.append("Type")
        headers.append("Plot")
        table.setHorizontalHeaderLabels(headers)

        # --------- Add standards icons to main button ---------
        self.ui.startPushButton.setEnabled(False)
        self.ui.stopPushButton.setEnabled(False)
        self.ui.startPushButton.setIcon(QtGui.qApp.style().standardIcon(QStyle.SP_CommandLink))
        self.ui.stopPushButton.setIcon(QtGui.qApp.style().standardIcon(QStyle.SP_BrowserStop))
        self.ui.openOutputPushButton.setIcon(QtGui.qApp.style().standardIcon(QStyle.SP_DirIcon))
        self.ui.headerWizardButton.setIcon(QtGui.qApp.style().standardIcon(QStyle.SP_FileDialogContentsView))

        # --------- redirect outputs to log widget ---------
        sys.stdout = OutLog(self.ui.outputPrintEdit, sys.stdout)
        sys.stderr = OutLog(self.ui.outputPrintEdit, sys.stderr, QtCore.Qt.red)

        # --------- Add Method widget ---------
        self.ui.methodWidget = MethodWidget(self.ui.methodsArgsGroupBox)

        # --------- Events connections ---------
        QtCore.QObject.connect(self.ui.methodsTreeWidget, QtCore.SIGNAL('itemClicked(QTreeWidgetItem*, int)'),
                               self.treeItemSelected)
        self.ui.openOutputPushButton.clicked.connect(self.openOutputFolder)
        self.ui.plotSignalsButton.clicked.connect(self.plotSignals)
        self.ui.startPushButton.clicked.connect(self.computeBtnEvent)
        self.ui.stopPushButton.clicked.connect(self.ui.methodWidget.stopComputeProcess)
        self.ui.actionSaveSession.triggered.connect(self.saveSession)
        self.ui.actionGIT.triggered.connect(self.openGIT)
        self.ui.actionAbout.triggered.connect(self.openAbout)
        self.ui.actionSaveSessionOver.triggered.connect(self.resaveSession)
        self.ui.actionLoadSession.triggered.connect(self.loadSession)
        self.ui.clearLogPushButton.clicked.connect(self.clearLogBtnEvent)
        self.ui.inputFolderToolButton.clicked.connect(self.setInputFolder)
        self.ui.outputFolderToolButton.clicked.connect(self.outputFolderButtonEvent)
        self.ui.toolBox.currentChanged.connect(self.changeSelectedTab)
        self.ui.headerWizardButton.clicked.connect(self.headerWizardEvent)
        self.ui.exportSignalsButton.clicked.connect(self.exportSelectedSignals)

        #QtCore.QObject.connect(self.ui.inputFileslistView, QtCore.SIGNAL('pressed(QModelIndex)'), self.checkFileItemFromRowClick)
        QtCore.QObject.connect(self.ui.inputSignalsWidget, QtCore.SIGNAL('pressed(QModelIndex)'), self.checkSignalItemFromCellClick)
        #QtCore.QObject.connect(self.ui.inputSignalsWidget, QtCore.SIGNAL('pressed(QModelIndex)'), self.selectItem)
        # right click menu on toolbox
        #self.ui.toolBox.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        #QtCore.QObject.connect(self.ui.toolBox, QtCore.SIGNAL("customContextMenuRequested(QPoint)"),self.openMenuToolbox)
        self.ui.inputFileslistView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        QtCore.QObject.connect(self.ui.inputFileslistView, QtCore.SIGNAL("customContextMenuRequested(QPoint)"),
                               self.openMenuToolbox)

        self.ui.inputSignalsWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        QtCore.QObject.connect(self.ui.inputSignalsWidget, QtCore.SIGNAL("customContextMenuRequested(QPoint)"),
                               self.openMenuToolbox)

        #self.ui.methodWidget.currentMethod.finished.connect(self.enableButtons)

        QtCore.QObject.connect(self.ui.methodWidget, QtCore.SIGNAL('computationFinished()'),
                               self.enableButtons)

        self.ui.inputSignalsWidget.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)

        self.ui.show()
        self.ui.toolBox.setCurrentIndex(0)
        self.warnForGoingBack(False)

        self.showStatus("{0} (v {1}) successfully loaded".format(self.appName, self.appVersion))

        #To-Do finish implementing Tools.plotSignals()
        self.ui.signalsStackedCheckBox.hide()

    def showStatus(self, msg):
        self.ui.statusbar.showMessage(msg)

    def getFromConfig(self, attribute):
        return self.config.get(self.__class__.__name__, attribute)

    def closeEvent(self, event):
        plot.close("all")
        event.accept()

    @pyqtSlot()
    def openGIT(self):
        webbrowser.open(self.getFromConfig('github'))

    @pyqtSlot()
    def openAbout(self):
        SyncpyAbout(self, self.config, self.__class__.__name__).open()

    @pyqtSlot()
    def openMenuToolbox(self, position):
        #if method tab, drop
        if self.ui.toolBox.currentIndex() == 2:
            return

        # Create a menu
        menu = QtGui.QMenu("Menu", self)
        menu.addAction("Check All", self.selectAll)
        menu.addAction("Uncheck All", self.unselectAll)
        # Show the context menu.
        menu.exec_(self.ui.toolBox.mapToGlobal(position))

    @pyqtSlot()
    def treeItemSelected(self, item, col):
        fullPath = item.text(1)
        if fullPath != '':
            self.ui.methodWidget.clearArgumentList()
            self.methodUsed = fullPath
            self.ui.methodDescriptionTextEdit.setPlainText(self.ui.methodWidget.populateArguments(str(fullPath)))
            self.ui.startPushButton.setEnabled(True)

    @pyqtSlot()
    def computeBtnEvent(self):
        # load selected signals from selected files
        self.signals = []

        ismat = False
        for f in self.filesSelected:
            if f.endswith('.mat'):
                matfile = loadmat(f)
                ismat = True
            for s in self.signalsSelected:
                if not ismat:
                    if not self.filesHasHeaders:
                        self.signals.append(ExtractSignalFromCSV(str(f), separator=self.columnSeparator, unit='ms', columns=s, header=False, headerValues=self.signalsHeader))
                    else:
                        self.signals.append(ExtractSignalFromCSV(str(f), separator=self.columnSeparator, unit='ms', columns=[str(self.headerMap[s])]))
                else:
                    ci = self.signalsHeader.index(s)
                    cn = str(self.signalsHeader[ci])
                    self.signals.append(ExtractSignalFromMAT(str(f), columns_index=ci, columns_wanted_names=[cn], matfile=matfile))

        self.ui.methodWidget.compute(self.signals)

        self.ui.stopPushButton.setEnabled(True)
        self.ui.startPushButton.setEnabled(False)
        self.ui.toolBox.setEnabled(False)

        self.showStatus("Computing...")

    def loadSignal(self, file, name):
        signal = None
        ismat = False
        if file.endswith('.mat'):
            matfile = loadmat(file)
            ismat = True

        if not ismat:
            if not self.filesHasHeaders:
                signal = ExtractSignalFromCSV(str(file), separator=self.columnSeparator, unit='ms', columns=name,
                                              header=False,
                                              headerValues=self.signalsHeader)
            else:
                signal = ExtractSignalFromCSV(str(file), separator=self.columnSeparator, unit='ms',
                                              columns=[str(self.headerMap[name])])
        else:
            ci = self.signalsHeader.index(name)
            cn = str(self.signalsHeader[ci])
            signal = ExtractSignalFromMAT(str(file), columns_index=ci, columns_wanted_names=[cn],
                                          matfile=matfile)
        return signal

    @pyqtSlot()
    def plotSignals(self):
        files = self.getSelectedFiles()
        names = self.getSignalsToPlot()
        if self.ui.signalsStackedCheckBox.isChecked():
            signals = []
            for f in self.getSelectedFiles():
                for name in names:
                    signal = self.loadSignal(f, name)
                    signals.append(signal)
            Tools.plotSignals(signals, files, names)
        else:
            for f in files:
                for s in names:
                    signal = self.loadSignal(f, s)
                    Tools.plotOneSignal(signal, s, f)

    @pyqtSlot()
    def clearLogBtnEvent(self):
        self.ui.outputPrintEdit.clear()

    @pyqtSlot()
    def enableButtons(self):
        self.ui.stopPushButton.setEnabled(False)
        self.ui.startPushButton.setEnabled(True)
        self.ui.toolBox.setEnabled(True)
        self.saveOutputsToFile()
        self.showStatus("")

    @pyqtSlot()
    def setSignalsRefreshed(self):
        self.signalsRefreshed = True

    @pyqtSlot()
    def headerWizardEvent(self):
        self.firstFile = None
        model = self.ui.inputFileslistView.model()
        if model is None:
            return
        for index in range(0, model.rowCount()):
            item = model.item(index)
            if item.checkState() == QtCore.Qt.Checked:
                self.firstFile = self.selectedDirectory + '/' + item.text()
                break

        if self.firstFile is None:
            return

        isHeaderInFile = self.filesHasHeaders
        headerWizardDialog = HeaderFileWizard(self, str(self.firstFile), self.config, self.signalsHeader, isHeaderInFile)
        if headerWizardDialog.exec_() == QtGui.QDialog.Accepted:
            self.signalsHeader = headerWizardDialog.getHeaders()
            self.filesHasHeaders = headerWizardDialog.hasHeaders()

            if not headerWizardDialog.isMatFile:
                self.columnSeparator = headerWizardDialog.separator
                self.headerMap = headerWizardDialog.getHeaderMap()

            table = self.ui.inputSignalsWidget

            # timeFound = False
            # for h in self.signalsHeader:
            #     if "time" in h.lower():
            #         timeFound = True
            #
            # if not timeFound:
            #     print "Error: No Time data in input file"
            #     return
            #
            # table.setRowCount(len(self.signalsHeader)-1)
            table.setRowCount(len(self.signalsHeader))

            # add signals header to the view
            if len(self.signalsHeader) > 0:
                i = 0
                for h in self.signalsHeader:
#                   if "time" in h.lower():
#                        continue
                    item = QtGui.QTableWidgetItem(h)

                    if not("time" in h.lower()):
                        item.setCheckState(0)
                        item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsUserCheckable)
                    else:
                        item.setBackground(SyncPy2.COLOR_GREY)
                    table.setItem(i, 0, item)
                    combo = QtGui.QComboBox()
                    combo.addItem("continuous")
                    if not ("time" in h.lower()):
                        combo.addItem("categorical")

                    combo.setCurrentIndex(headerWizardDialog.signalsType[i])
                    QtCore.QObject.connect(combo, QtCore.SIGNAL("currentIndexChanged(QString)"), self.setSignalsRefreshed)
                    table.setCellWidget(i, 1, combo)
                    icon = QtGui.QIcon(QtGui.QPixmap(self.plotImgPath))
                    item = QtGui.QTableWidgetItem(icon, "")
                    if not ("time" in h.lower()):
                        item.setCheckState(0)
                        item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsUserCheckable)
                    else:
                        item.setBackground(SyncPy2.COLOR_GREY)
                    table.setItem(i, 2, item)
                    i += 1
                self.showStatus("Signals loaded.")

    @pyqtSlot()
    def outputFolderButtonEvent(self):
        self.outputDirectory = os.path.relpath(str(QtGui.QFileDialog.getExistingDirectory(self, "Select Output Directory")))
        self.ui.outputFolderText.setPlainText(self.outputDirectory)

    @pyqtSlot()
    def setInputFolder(self):
        # if load session, load data folder
        if self.sessionHasBeenLoaded:
            self.selectedDirectory = self.loadedSession["InputFolder"]
            self.outputDirectory = self.loadedSession["OutputDirectory"]
            self.columnSeparator = str(self.loadedSession["ColumnSeparator"])
        else:
            dir = QtGui.QFileDialog.getExistingDirectory(self, "Select Directory")
            if dir:
                self.selectedDirectory = os.path.relpath(str(dir))

        if not self.selectedDirectory:
            return

        if not self.outputDirectory:
            self.outputDirectory = self.selectedDirectory

        self.ui.outputFolderText.setPlainText(self.outputDirectory)

        self.dataFiles = []
        self.dataFiles += [os.path.join(self.selectedDirectory, f)
                           for f in os.listdir(self.selectedDirectory)
                           if f.endswith('.csv') or f.endswith('.mat') or f.endswith('.tsv')]
        dataNames = []
        dataNames += [f for f in os.listdir(self.selectedDirectory) if f.endswith('.csv') or f.endswith('.mat') or f.endswith('.tsv')]
        model = QtGui.QStandardItemModel(self.ui.inputFileslistView)
        for f in dataNames:
            item = QtGui.QStandardItem(f)
            item.setCheckable(True)
            item.setEditable(False)
            model.appendRow(item)
        self.ui.inputFileslistView.setModel(model)

        # if load session check files used last time
        if self.sessionHasBeenLoaded:
            self.filesSelected = []
            for i in range(0,len(dataNames)):
                for lf in self.loadedSession["Files"]:
                    fname = os.path.basename(lf)
                    if dataNames[i] == fname:
                        item = model.item(i)
                        item.setCheckState(2)
                        self.filesSelected.append(self.dataFiles[i])

        self.clearSignals()
        self.sessionHasBeenLoaded = False

    @pyqtSlot()
    def openOutputFolder(self):
        if not self.outputDirectory:
            return

        outFolder = self.outputDirectory
        if self.syncpyplatform == "m":
            subprocess.call(['open', outFolder])
        elif self.syncpyplatform == "w":
            subprocess.call(['explorer', outFolder])
        else:
            subprocess.call(['xdg-open', outFolder])

    #0 unchecked, 2 checked
    def setItemsCheckState(self, state):
        if self.ui.toolBox.currentIndex() == 0:
            self.clearSignals()
            self.sessionHasBeenLoaded = False
            model = self.ui.inputFileslistView.model()
            if model is None:
                return
            for index in range(model.rowCount()):
                item = model.item(index)
                item.setCheckState(state)

        if self.ui.toolBox.currentIndex() == 1:
            table = self.ui.inputSignalsWidget
            col = table.currentColumn()
            for i in xrange(0, table.rowCount()):
                item = table.item(i, col)
                item.setCheckState(state)

    @pyqtSlot()
    def selectAll(self):
        self.setItemsCheckState(2)

    @pyqtSlot()
    def unselectAll(self):
        self.setItemsCheckState(0)

    # @pyqtSlot()
    # def checkFileItemFromRowClick(self, index):
    #
    #     model = QtCore.QModelIndex()
    #
    #     if self.ui.toolBox.currentIndex() == 0:
    #         self.clearSignals()
    #         self.sessionHasBeenLoaded = False
    #         model = self.ui.inputFileslistView.model()
    #
    #     if model is None:
    #         return
    #
    #     item = model.item(index.row())
    #     item.setCheckState(QtCore.Qt.Unchecked if item.checkState() == QtCore.Qt.Checked else QtCore.Qt.Checked)
    #     model.reset()

    @pyqtSlot()
    def checkSignalItemFromCellClick(self, index):

        if self.ui.toolBox.currentIndex() == 1:
            table = self.ui.inputSignalsWidget
            item = table.item(index.row(), index.column())
            if item.background() != SyncPy2.COLOR_GREY:
                item.setCheckState(QtCore.Qt.Unchecked if item.checkState() == QtCore.Qt.Checked else QtCore.Qt.Checked)

    def warnForGoingBack(self, warn):
        self.ui.warningWidget.setShown(warn)

    @pyqtSlot()
    def changeSelectedTab(self):
        if self.ui.toolBox.currentIndex() == 0:
            self.ui.startPushButton.setEnabled(False)
            self.ui.stopPushButton.setEnabled(False)

            oldNSignals = self.nSignalsSelected
            if oldNSignals == 0 and len(self.getSelectedSignals()) != 0:
                self.warnForGoingBack(True)
            elif len(self.getSelectedSignals()) == oldNSignals and len(self.getSelectedFiles()) > 0 and len(self.getSelectedSignals()) > 0:
                self.warnForGoingBack(True)
            else:
                self.warnForGoingBack(False)
                self.recreateMethodList = True

        # --------- populate signals ----------
        if self.ui.toolBox.currentIndex() == 1:
            if len(self.getSelectedFiles()) == 0:
                self.showStatus("Select at least one input file first")
            self.ui.startPushButton.setEnabled(False)
            self.ui.stopPushButton.setEnabled(False)

            #if self.methodUsed != "":
            oldNSignals = self.nSignalsSelected
            if len(self.getSelectedSignals()) == oldNSignals and len(self.getSelectedFiles()) > 0 and len(self.getSelectedSignals()) > 0:
                self.warnForGoingBack(True)
            else:
                self.warnForGoingBack(False)
                self.recreateMethodList = True

            if len(self.signalsHeader) == 0:
                self.headerWizardEvent()

        # --------- populate Methods ----------
        if self.ui.toolBox.currentIndex() == 2:

            oldNSignals = self.nSignalsSelected
            if self.signalsRefreshed or len(self.getSelectedSignals()) != oldNSignals \
                    or self.sessionHasBeenLoaded:
                self.recreateMethodList = True

            if self.nSignalsSelected == 0:
                self.showStatus("Select at least one signal first")
            self.warnForGoingBack(False)

            if self.recreateMethodList:
                self.ui.methodDescriptionTextEdit.setPlainText("")
                self.ui.methodWidget.clearArgumentList()
                self.ui.methodsTreeWidget.clear()
                self.createMethodList()
                self.recreateMethodList = False
                #self.methodUsed = fullPath
                #self.ui.methodDescriptionTextEdit.setPlainText(self.ui.methodWidget.populateArguments(str(fullPath)))
            else:
                self.selectMethodInTree()

            self.signalsRefreshed = False

        self.sessionHasBeenLoaded = False

    def selectMethodInTree(self):
        methodList = self.ui.methodsTreeWidget.findItems(os.path.basename(str(self.methodUsed)),
                                                         QtCore.Qt.MatchRecursive | QtCore.Qt.MatchExactly)
        for m in methodList:
            if m.text(1) == self.methodUsed:
                self.ui.methodsTreeWidget.scrollToItem(methodList[0])
                m.setSelected(True)
                self.treeItemSelected(m, 0)

    def getSelectedFiles(self):
        # number of files selected
        self.nFilesSelected = 0
        model = self.ui.inputFileslistView.model()
        if model is None:
            return []
        self.filesSelected = []
        for index in range(model.rowCount()):
            item = model.item(index)
            if item.checkState() == QtCore.Qt.Checked:
                self.filesSelected.append(self.dataFiles[index])
                self.nFilesSelected += 1
        return self.filesSelected

    def getSelectedSignals(self):
        # number of signals selected
        self.nSignalsSelected = 0
        self.typeSum = 0
        table = self.ui.inputSignalsWidget
        self.signalsSelected = []
        for index in range(table.rowCount()):
            item = table.item(index, 0)
            if item.checkState() == QtCore.Qt.Checked:
                self.signalsSelected.append(str(item.text()))
                self.nSignalsSelected += 1
                type = table.cellWidget(index, 1).currentText()
                if str(type) == "categorical":
                    self.typeSum += 1
        return self.signalsSelected

    def getSignalsToPlot(self):
        # number of signals selected
        table = self.ui.inputSignalsWidget

        signalsToPlot = []
        for index in range(table.rowCount()):
            item = table.item(index, 2)
            if item.checkState() == QtCore.Qt.Checked:
                label = table.item(index, 0)
                signalsToPlot.append(str(label.text()))
        return signalsToPlot

    @pyqtSlot()
    def resaveSession(self):
        if self.lastSavedSessionFilename:
            self.saveSession(self.lastSavedSessionFilename)

    @pyqtSlot()
    def saveSession(self, fname=None):
        if fname == None:
            fname = QFileDialog.getSaveFileName(self, "Save Session File", ".", "Session Files (*.session)")
            if self.syncpyplatform == "u":
                fname += ".session"
        if not fname:
            return

        self.ui.actionSaveSessionOver.setText("Save over '" + os.path.basename(str(fname)) + "'")
        session = {}

        session["SyncPyVer"] = self.syncpyver
        session["SyncPyPlat"] = self.syncpyplatform

        session["FileContainsHeader"] = self.filesHasHeaders
        session["InputFolder"] = self.selectedDirectory
        session["OutputDirectory"] = self.outputDirectory

        session["Files"] = []
        for f in self.getSelectedFiles():
            session["Files"].append(f)

        # saving signals

        session["HeaderMap"] = self.headerMap

        session["Signals"] = []
        table = self.ui.inputSignalsWidget
        for i in xrange(0, table.rowCount()):
            item = table.item(i, 0)
            checkState = item.checkState()
            type = table.cellWidget(i, 1).currentText()
            plotState = table.item(i, 2).checkState()
            session["Signals"].append({'label': str(item.text()),
                                       'type': str(type),
                                       'plotState': plotState,
                                       'checkState': checkState})

        session["Method"] = str(self.methodUsed)
        session["ColumnSeparator"] = str(self.columnSeparator)
        session["MethodArgs"] = self.ui.methodWidget.getArgumentsAsDictionary()
        session["ToolBoxIndex"] = self.ui.toolBox.currentIndex()

        with open(fname, 'w') as f:
            json.dump(session, f, indent=4)
            self.lastSavedSessionFilename = fname
            self.ui.actionSaveSessionOver.setEnabled(True)
            f.close()

    @pyqtSlot()
    def loadSession(self):
        self.loadedSession = {}
        fname = QFileDialog.getOpenFileName(self,"Open Session File", ".", "Session Files (*.session)")
        if fname:
            with open(fname, 'r') as f:
                self.loadedSession = json.load(f, object_pairs_hook=OrderedDict)
                self.lastSavedSessionFilename = fname
                self.sessionHasBeenLoaded = True
                self.ui.actionSaveSessionOver.setEnabled(True)
                f.close()
        if not self.loadedSession:
            return

        if self.loadedSession["SyncPyVer"] != self.syncpyver:
            print "Unable to load session, SyncPy version mismatch (session "+self.loadedSession["SyncPyVer"]+" vs current "+self.syncpyver+")"
            return

        if self.loadedSession["SyncPyPlat"] != self.syncpyplatform:
            message = "Unable to load session, SyncPy platform mismatch (session created on "
            if self.loadedSession["SyncPyPlat"] == "u":
                message += "Linux "
            elif self.loadedSession["SyncPyPlat"] == "w":
                message += "Windows "
            elif self.loadedSession["SyncPyPlat"] == "m":
                message += "Mac "
            message += "and current platform is "

            if self.syncpyplatform == "u":
                message += "Linux"
            elif self.syncpyplatform == "w":
                message += "Windows"
            elif self.syncpyplatform == "m":
                message += "Mac"

            message += ")"

            print message
            return

        self.ui.actionSaveSessionOver.setText("Save over '" + os.path.basename(str(fname)) + "'")

        #populate file list
        try:
            self.setInputFolder()
        except:
            print "Error loading session: Unable to find input files"
            self.sessionHasBeenLoaded = False
            self.ui.actionSaveSessionOver.setEnabled(False)
            return

        self.filesHasHeaders = self.loadedSession["FileContainsHeader"]

        #populate signal list
        self.signalsSelected = []
        table = self.ui.inputSignalsWidget
        table.setRowCount(len(self.loadedSession["Signals"]))
        i = 0

        for sig in self.loadedSession["Signals"]:
            item = QtGui.QTableWidgetItem(sig["label"])
            item.setCheckState(sig["checkState"])
            if sig["checkState"] == QtCore.Qt.Checked:
                self.signalsSelected.append(sig["label"])
            item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsUserCheckable)
            table.setItem(i, 0, item)
            combo = QtGui.QComboBox()
            combo.addItem("continuous")
            combo.addItem("categorical")
            combo.setCurrentIndex(0 if sig["type"] == "continuous" else 1)
            table.setCellWidget(i,1,combo)
            icon = QtGui.QIcon(QtGui.QPixmap(self.plotImgPath))
            item = QtGui.QTableWidgetItem(icon,"")
            item.setCheckState(sig["plotState"])
            item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsUserCheckable)
            table.setItem(i, 2, item)
            i += 1

        #populate method list

        self.ui.toolBox.setCurrentIndex(int(self.loadedSession["ToolBoxIndex"]))

        self.ui.methodsTreeWidget.clear()
        self.createMethodList()
        self.methodUsed = self.loadedSession["Method"]
        self.selectMethodInTree()

        self.ui.methodWidget.setArgumentsWithDictionary(self.loadedSession["MethodArgs"])

        self.headerMap = self.loadedSession["HeaderMap"]

        for i in xrange(0, len(self.headerMap)):
            self.signalsHeader.append(self.headerMap.keys()[i])


    def clearSignals(self):
            self.warnForGoingBack(False)
            self.methodUsed = ""
            model = self.ui.inputSignalsWidget.model()
            if model is not None:
                while model.rowCount() > 0:
                    model.removeRow(0)
            self.signalsHeader = []
            plot.close("all")

    def saveOutputsToFile(self):
        methodName = str(self.methodUsed).rsplit('/', 1)[1].rsplit('.', 1)[0]
        currDay = time.strftime("%Y%m%d")
        currTime = time.strftime("%H%M%S")
        outDirName = self.outputDirectory+'/syncpy_out-'+currDay
        if not(os.path.exists(outDirName)):
            os.mkdir(outDirName)
        outFile = open(outDirName+'/'+currTime+'-'+methodName+'-log.txt', 'w')

        outFile.write("Data files used:\n")
        for f in self.filesSelected:
            outFile.write("\t"+f+"\n")

        outFile.write("\n\nSignals used:\n")
        for s in self.signalsSelected:
            outFile.write("\t"+s+"\n")

        outFile.write("\n\nMethod used:\n")
        outFile.write("\t"+self.methodUsed+"\n")

        outFile.write("\n\nResults:\n")

        res = self.ui.methodWidget.getResult()
        outFile.write("\t" + str(res) + "\n")

        #outFile.write("\n\nLog output:\n")
        #outFile.write(self.ui.outputPrintEdit.toPlainText())
        outFile.close()

        try:
            for i in plot.get_fignums():
                f = plot.figure(i)
                #f.set_canvas(plot.gcf().canvas)
                #currTime = time.strftime("%d%m%Y%H%M%S")
                filename = methodName+"-Figure"+str(i)+".png"
                outFile = os.path.abspath(outDirName+"/"+filename)
                print "Saving fig to: %s" % outFile
                f.savefig(outFile)
        except Exception, ex:
            print "Exception while saving plot to '{0}'\n{1}".format(filename, ex.message)

    def createMethodList(self):
        #self.ui.methodsTreeWidget.clear()
        rootFolder = "Methods"

        # number of files selected
        self.getSelectedFiles()
        if self.nFilesSelected == 0:
            return

        # number of signals selected
        self.getSelectedSignals()
        if self.nSignalsSelected == 0:
            return

        onlyUtils = False
        # populate root folder
        if self.nFilesSelected == 1 :
            if self.nSignalsSelected == 1:
                print "Error: No method available for one signal only"
                return
            elif self.nSignalsSelected == 2:
                rootFolder += "/DataFrom2Persons/Univariate"
            elif self.nSignalsSelected > 2:
                #ici on propose toutes les methodes et l'utilisateur doit choisir si uni ou multivariate
                rootFolder += "/DataFrom2Persons"
        elif self.nFilesSelected == 2:
            if self.nSignalsSelected == 1:
                rootFolder += "/DataFrom2Persons/Univariate"
            elif self.nSignalsSelected > 1:
                rootFolder += "/DataFrom2Persons/Multivariate"
        elif self.nFilesSelected > 2:
            if self.nSignalsSelected > 0:
                rootFolder += "/DataFromManyPersons"

        if self.typeSum == 0:
            rootFolder += "/Continuous"
        elif self.typeSum == self.nSignalsSelected:
            rootFolder += "/Categorical"

        rootItem = QtGui.QTreeWidgetItem(self.ui.methodsTreeWidget, [rootFolder])
        self.loadMethodsFromFolder(rootFolder, rootItem)

    def loadMethodsFromFolder(self, curPath, tree):
        folderIcon = QtGui.qApp.style().standardIcon(QStyle.SP_DirIcon)
        methodIcon = QtGui.qApp.style().standardIcon(QStyle.SP_MediaPlay)
        for (path, subdirs, files) in os.walk(curPath, topdown=True):
            if curPath == path:
                for directory in subdirs:
                    item = QtGui.QTreeWidgetItem(tree, [directory])
                    item.setIcon(0, folderIcon)
                    self.loadMethodsFromFolder(path + '/' + directory, item)

                for name in files:
                    if (not name.startswith("__")) and name.endswith(".py"):
                        methodName = name
                        item = QtGui.QTreeWidgetItem(tree, [methodName])
                        #storing full path hidden for convenience
                        item.setText(1, curPath+'/'+methodName)
                        item.setIcon(0, methodIcon)

    def exportSelectedSignals(self):
        table = self.ui.inputSignalsWidget
        selectedSignalsHeader = []
        # give filename
        self.getSelectedFiles()

        firstTime = True

        fileNumber = 1

        for index in range(table.rowCount()):
            item = table.item(index, 0)
            ismat = False
            for f in self.getSelectedFiles():
                if f.endswith('.mat'):
                    matfile = loadmat(f)
                    ismat = True
                if item.checkState() == QtCore.Qt.Checked:
                    s = str(item.text())
                    if not ismat:
                        if not self.filesHasHeaders:
                            signal = ExtractSignalFromCSV(str(f), separator=self.columnSeparator, unit='ms', columns=s, header=False,
                                                     headerValues=self.signalsHeader)
                        else:
                            signal = ExtractSignalFromCSV(str(f), separator=self.columnSeparator, unit='ms', columns=[str(self.headerMap[s])])
                    else:
                        ci = self.signalsHeader.index(s)
                        cn = str(self.signalsHeader[ci])
                        signal = ExtractSignalFromMAT(str(f), columns_index=ci, columns_wanted_names=[cn], matfile=matfile)


                    if firstTime:
                        seletedSignals = pd.DataFrame(index=signal.index)
                        firstTime = False

                    #seletedSignals.insert(col,s,signal)
                    #col += 1
                    seletedSignals[s+str(fileNumber)] = signal
                    fileNumber += 1

        fileName = ''

        fileName = QtGui.QFileDialog.getSaveFileName(self)

        if not fileName:
            print "Error export signals: No filename provided"
            return
        else:
            if not fileName.endsWith('.csv'):
                fileName = fileName+'.csv'
            seletedSignals.to_csv(path_or_buf=fileName,header=True,sep=';')


if __name__ == "__main__":
    import sys
    # on Linux set X11 windows thread safe or crash
    if sys.platform == 'linux2':
        QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_X11InitThreads)
    app = QtGui.QApplication(sys.argv)
    #MainWindow = QtGui.QMainWindow()
    ui = SyncPy2()
    #ui.show()
    sys.exit(app.exec_())
