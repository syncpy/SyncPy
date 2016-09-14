#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
import webbrowser
from PyQt4 import QtWebKit
from PyQt4.QtCore import pyqtSlot
from string import Template
import os
import ConfigParser



class SyncpyAbout(QtGui.QDialog):
        def __init__(self, widget, config, section):
            super(SyncpyAbout, self).__init__(widget)
            self.templatePath = 'ui/about.html'


            f = open(self.templatePath, 'r')
            self.absolutePath, tail = os.path.split(os.path.abspath(self.templatePath))
            self.absolutePath = self.absolutePath.replace('\\', '/')

            template = Template(f.read())
            dic = dict(name=config.get(section, "app.name"),
                       version=config.get(section, "app.version"))
            html = template.safe_substitute(dic)

            layout = QtGui.QVBoxLayout(self)
            self.webView = QtWebKit.QWebView(self)
            self.setBaseSize(1000, 100)
            layout.addWidget(self.webView)

            self.webView.setHtml(html, QtCore.QUrl('file:///{0}/'.format(self.absolutePath)))

            self.webView.page().setLinkDelegationPolicy(QtWebKit.QWebPage.DelegateAllLinks)
            QtCore.QObject.connect(self.webView, QtCore.SIGNAL("linkClicked(QUrl)"), self.linkClicked)

        @pyqtSlot()
        def linkClicked(self, qUrl):
            webbrowser.open(qUrl.toString())

