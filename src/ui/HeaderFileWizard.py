#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtCore import QStringList, QString
from PyQt4.QtGui import QTableWidgetItem
from scipy.io import loadmat, whosmat
from collections import OrderedDict
import numpy as np
import ConfigParser

# Main Window Class
class HeaderFileWizard(QtGui.QDialog):
    def __init__(self, widget, filename, config, signalsHeader = None, isHeaderInFile = True):
        super(HeaderFileWizard, self).__init__(widget)
        self.filename = filename
        self.isHeaderInFile = isHeaderInFile
        self.signalsHeader = signalsHeader
        self.config = config

        self.ui = uic.loadUi(self.getFromConfig("uiFile"), self)
        self.table = self.ui.tableWidget
        self.table.horizontalHeader().sectionDoubleClicked.connect(self.changeHorizontalHeader)
        # 0 continuous, 1 categorical
        self.signalsType = []
        self.originalHeader = []
        self.headerMap = {}
        self.isMatFile = False

        self.initUI()

    def hasHeaders(self):
        return self.ui.headersCheckBox.checkState() == QtCore.Qt.Checked

    def getFromConfig(self, attribute):
        return self.config.get(self.__class__.__name__, attribute)

    def findSeparator(self):
        with open(self.filename, 'r') as f:
            first_line = f.readline()
            if first_line.find(';') != -1:
                self.separator = ';'
            elif first_line.find(',') != -1:
                self.separator = ','
            elif first_line.find('\t') != -1:
                self.separator = '\t'
            else:
                self.separator = '\n'

    @staticmethod
    def strip(s):
        s = s.strip()
        return s

    @staticmethod
    def makeUniques(headers):
        headers = map(HeaderFileWizard.strip, headers)
        headers.reverse()
        for h in headers:
            c = headers.count(h)
            while c > 1:
                i = headers.index(h)
                headers[i] = headers[i] + "-" + str(c)
                c = headers.count(h)
        headers.reverse()
        return headers

    def initUI(self):
        if self.filename.endswith('.csv') or self.filename.endswith('.tsv'):
            self.loadFromCSV()
        elif self.filename.endswith('.mat'):
            self.isMatFile = True
            self.loadFromMAT()

        # find type of each signal
        # 0 continuous, 1 categorical
        start = 0
        if self.isHeaderInFile:
            start = 1

        for j in xrange(self.nbCols):
            signalUniques = []
            for i in xrange(start, self.nbRows):
                signalUniques.append(self.table.item(i, j).text())
            if len(set(signalUniques)) <= 10: #count uniques in list
                self.signalsType.append(1)
            else:
                self.signalsType.append(0)

    def loadFromMAT(self):
        matinfos = whosmat(str(self.filename))
        matfile = loadmat(str(self.filename))
        self.nbRows = 30#5
        self.nbCols = matinfos[0][1][1]
        self.table.setRowCount(self.nbRows)
        self.table.setColumnCount(self.nbCols)

        for val in matfile.values():
            if isinstance(val, np.ndarray):
                mdata = val

        for j in xrange(self.nbCols):
            headerLabel = str(mdata[0 ,j])
            item = QTableWidgetItem(headerLabel)
            item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable)
            self.table.setHorizontalHeaderItem(j, item)

        for i in xrange(self.nbRows):
                for j in xrange(self.nbCols):
                    item = QTableWidgetItem(str(mdata[i ,j]))
                    item.setFlags(QtCore.Qt.ItemIsSelectable)
                    self.table.setItem(i, j, item)

    def loadFromCSV(self):
        line = ""
        self.findSeparator()
        with open(self.filename, 'r') as f:
            headers = self.signalsHeader

            line = f.readline()
            linebckp = line.rstrip('\n')
            self.originalHeader = linebckp.split(self.separator)
            if len(headers) == 0:
                headers = filter(None, linebckp.split(self.separator))

            self.nbRows = 30#5
            self.nbCols = len(headers)
            self.table.setRowCount(self.nbRows)
            self.table.setColumnCount(self.nbCols)

            #makes header uniques
            headers = HeaderFileWizard.makeUniques(headers)

            for j in xrange(self.nbCols):
                headerLabel = headers[j].strip()
                item = QTableWidgetItem(headerLabel)
                item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable)
                self.table.setHorizontalHeaderItem(j, item)

            #self.table.setHorizontalHeaderLabels(headerList)

            for i in xrange(self.nbRows):
                line = f.readline()
                for j in xrange(self.nbCols):
                    values = line.split(self.separator)
                    if j < len(values):
                        item = QTableWidgetItem(values[j])
                        item.setFlags(QtCore.Qt.ItemIsSelectable)
                        self.table.setItem(i, j, item)
                    else:
                        break


    def changeHorizontalHeader(self, index):
        oldHeader = self.table.horizontalHeaderItem(index).text()
        newHeader, ok = QtGui.QInputDialog.getText(self,
                                                   'Change header label for column %d' % index,
                                                   'Header:',
                                                   QtGui.QLineEdit.Normal,
                                                   oldHeader)
        if ok:
            self.table.horizontalHeaderItem(index).setText(newHeader)

    def getHeaders(self):
        self.signalsHeader = []
        for j in xrange(self.nbCols):
            self.signalsHeader.append(str(self.table.takeHorizontalHeaderItem(j).text()))

        return self.signalsHeader

    def getHeaderMap(self):
        self.headerMap = OrderedDict()
        for j in xrange(self.nbCols):
            self.headerMap[str(self.signalsHeader[j])] = str(self.originalHeader[j])

        return self.headerMap

    def getSignalsType(self):
        return self.signalsType