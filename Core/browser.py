#!/usr/bin/python3.7
# coding: utf-8

from PyQt5.QtWidgets import QWidget, QGridLayout, QMessageBox, QPushButton, QMenu
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QIcon

from Core.Widgets.browserWidget import BrowserWidget
from Core.Widgets.urlInput import UrlInput
from Core.Widgets.tabWidget import TabWidget
from Core.Widgets.pushButton import PushButton
from Core.Utils.dbUtils import DBConnection


class Browser(QWidget):
    def __init__(self):
        super(Browser, self).__init__()
        self.dbConnection = DBConnection("data.db")
        self.dbConnection.createDB()
        self.createUI()
        self.show()

    def setTitle(self):
        self.setWindowTitle(self.browserWidget.title() + " - Browthon")
        self.tabWidget.setTitle()
        self.dbConnection.executeWithoutReturn("""INSERT INTO history(name, url) VALUES(?, ?)""", (self.browserWidget.title(), self.browserWidget.url().toString()))
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_R or event.key() == Qt.Key_F5:
            self.browserWidget.reload()
        elif event.key() == Qt.Key_N:
            self.tabWidget.requestsAddTab()
        elif event.key() == Qt.Key_Q:
            self.tabWidget.requestsRemoveTab(self.tabWidget.currentIndex())
    
    def closeEvent(self, event):
        if self.tabWidget.count() == 0:
            self.dbConnection.disconnect()
            event.accept()
        elif self.tabWidget.count() != 1:
            if QMessageBox().question(self, "Quitter ?", "Voulez vous quitter tous les onglets ?", QMessageBox.Yes, QMessageBox.No) == 16384:
                self.dbConnection.disconnect()
                event.accept()
            else:
                event.ignore()
                self.tabWidget.requestsRemoveTab(self.tabWidget.currentIndex())
        else:
            if QMessageBox().question(self, "Quitter ?", "Voulez vous quitter Browthon ?", QMessageBox.Yes, QMessageBox.No) == 16384:
                self.dbConnection.disconnect()
                event.accept()
            else:
                event.ignore()

    def createUI(self):
        self.grid = QGridLayout()

        self.urlInput = UrlInput(self)
        self.back = PushButton("", QIcon("Icons/NavigationBar/back.png"))
        self.forward = PushButton("", QIcon("Icons/NavigationBar/forward.png"))
        self.reload = PushButton("", QIcon("Icons/NavigationBar/reload.png"))
        self.home = PushButton("", QIcon("Icons/NavigationBar/home.png"))
        self.parameter = PushButton("", QIcon("Icons/NavigationBar/param.png"))
        self.parameterMenu = QMenu()
        self.tabWidget = TabWidget(self)

        self.tabWidget.requestsAddTab()

        self.parameterMenu.addAction("Historique", lambda: print("Historique"))
        self.parameterMenu.addAction("Favoris", lambda: print("Favoris"))
        self.parameterMenu.addSeparator()
        self.parameterMenu.addAction("Paramètres", lambda: print("Paramètres"))
        self.parameterMenu.addSeparator()
        self.parameterMenu.addAction("Informations", lambda: print("Informations"))

        self.reload.clicked.connect(self.browserWidget.reload)
        self.back.clicked.connect(self.browserWidget.back)
        self.forward.clicked.connect(self.browserWidget.forward)
        self.home.clicked.connect(lambda: self.urlInput.enterUrlGiven(self.dbConnection.executeWithReturn("""SELECT home FROM parameters""")[0][0]))
        self.parameter.setMenu(self.parameterMenu)

        self.grid.addWidget(self.back, 0, 0)
        self.grid.addWidget(self.reload, 0, 1)
        self.grid.addWidget(self.forward, 0, 2)
        self.grid.addWidget(self.urlInput, 0, 3)
        self.grid.addWidget(self.home, 0, 4)
        self.grid.addWidget(self.parameter, 0, 5)
        self.grid.addWidget(self.tabWidget, 1, 0, 1, 6)

        self.setLayout(self.grid)
        self.setGeometry(100, 100, 1200, 1200)
        self.setWindowTitle('Browthon')