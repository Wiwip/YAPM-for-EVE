# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(750, 372)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.groupBox = QtWidgets.QGroupBox(self.centralWidget)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 721, 261))
        self.groupBox.setObjectName("groupBox")
        self.pushButtonCopy = QtWidgets.QPushButton(self.groupBox)
        self.pushButtonCopy.setGeometry(QtCore.QRect(350, 210, 101, 31))
        self.pushButtonCopy.setObjectName("pushButtonCopy")
        self.pushButtonRefresh = QtWidgets.QPushButton(self.groupBox)
        self.pushButtonRefresh.setGeometry(QtCore.QRect(90, 210, 101, 31))
        self.pushButtonRefresh.setObjectName("pushButtonRefresh")
        self.listViewDestinationAccounts = QtWidgets.QListView(self.groupBox)
        self.listViewDestinationAccounts.setGeometry(QtCore.QRect(420, 90, 291, 111))
        self.listViewDestinationAccounts.setObjectName("listViewDestinationAccounts")
        self.comboBoxDestinationSettings = QtWidgets.QComboBox(self.groupBox)
        self.comboBoxDestinationSettings.setGeometry(QtCore.QRect(420, 60, 291, 22))
        self.comboBoxDestinationSettings.setObjectName("comboBoxDestinationSettings")
        self.comboBoxDestinationSelection = QtWidgets.QComboBox(self.groupBox)
        self.comboBoxDestinationSelection.setGeometry(QtCore.QRect(420, 30, 291, 22))
        self.comboBoxDestinationSelection.setObjectName("comboBoxDestinationSelection")
        self.comboBoxOriginSettings = QtWidgets.QComboBox(self.groupBox)
        self.comboBoxOriginSettings.setGeometry(QtCore.QRect(90, 60, 291, 22))
        self.comboBoxOriginSettings.setObjectName("comboBoxOriginSettings")
        self.listViewOriginAccounts = QtWidgets.QListView(self.groupBox)
        self.listViewOriginAccounts.setGeometry(QtCore.QRect(90, 90, 291, 111))
        self.listViewOriginAccounts.setObjectName("listViewOriginAccounts")
        self.comboBoxOriginSelection = QtWidgets.QComboBox(self.groupBox)
        self.comboBoxOriginSelection.setGeometry(QtCore.QRect(90, 30, 291, 22))
        self.comboBoxOriginSelection.setObjectName("comboBoxOriginSelection")
        self.pushButton = QtWidgets.QPushButton(self.groupBox)
        self.pushButton.setGeometry(QtCore.QRect(540, 210, 81, 31))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_2.setGeometry(QtCore.QRect(630, 210, 81, 31))
        self.pushButton_2.setObjectName("pushButton_2")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(10, 30, 71, 20))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(10, 60, 71, 20))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(10, 90, 71, 21))
        self.label_3.setObjectName("label_3")
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 750, 21))
        self.menuBar.setObjectName("menuBar")
        MainWindow.setMenuBar(self.menuBar)
        self.mainToolBar = QtWidgets.QToolBar(MainWindow)
        self.mainToolBar.setObjectName("mainToolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox.setTitle(_translate("MainWindow", "User Settings"))
        self.pushButtonCopy.setText(_translate("MainWindow", "Copy"))
        self.pushButtonRefresh.setText(_translate("MainWindow", "Refresh"))
        self.pushButton.setText(_translate("MainWindow", "Select All"))
        self.pushButton_2.setText(_translate("MainWindow", "Deselect All"))
        self.label.setText(_translate("MainWindow", "Installations"))
        self.label_2.setText(_translate("MainWindow", "Profiles"))
        self.label_3.setText(_translate("MainWindow", "User characters"))


