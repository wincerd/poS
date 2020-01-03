# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'START.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1091, 781)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tableView = QtWidgets.QTableView(self.centralwidget)
        self.tableView.setGeometry(QtCore.QRect(580, 50, 491, 551))
        self.tableView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.tableView.setObjectName("tableView")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(660, 620, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(760, 620, 75, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(890, 620, 75, 23))
        self.pushButton_3.setObjectName("pushButton_3")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(640, 20, 191, 22))
        self.comboBox.setObjectName("comboBox")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(580, 20, 71, 21))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(910, 20, 121, 21))
        self.label_2.setObjectName("label_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1091, 21))
        self.menubar.setObjectName("menubar")
        self.menufile = QtWidgets.QMenu(self.menubar)
        self.menufile.setObjectName("menufile")
        self.menusale = QtWidgets.QMenu(self.menubar)
        self.menusale.setObjectName("menusale")
        self.menubuy = QtWidgets.QMenu(self.menubar)
        self.menubuy.setObjectName("menubuy")
        self.menureport = QtWidgets.QMenu(self.menubar)
        self.menureport.setObjectName("menureport")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionexit = QtWidgets.QAction(MainWindow)
        self.actionexit.setObjectName("actionexit")
        self.actionexit_2 = QtWidgets.QAction(MainWindow)
        self.actionexit_2.setObjectName("actionexit_2")
        self.actionDaily = QtWidgets.QAction(MainWindow)
        self.actionDaily.setObjectName("actionDaily")
        self.actionWeekly = QtWidgets.QAction(MainWindow)
        self.actionWeekly.setObjectName("actionWeekly")
        self.actionYear_to_date = QtWidgets.QAction(MainWindow)
        self.actionYear_to_date.setObjectName("actionYear_to_date")
        self.menufile.addAction(self.actionexit)
        self.menufile.addAction(self.actionexit_2)
        self.menureport.addAction(self.actionDaily)
        self.menureport.addAction(self.actionWeekly)
        self.menureport.addAction(self.actionYear_to_date)
        self.menubar.addAction(self.menufile.menuAction())
        self.menubar.addAction(self.menusale.menuAction())
        self.menubar.addAction(self.menubuy.menuAction())
        self.menubar.addAction(self.menureport.menuAction())

        self.retranslateUi(MainWindow)
        self.tableView.entered['QModelIndex'].connect(self.label.update)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "SAVE"))
        self.pushButton_2.setText(_translate("MainWindow", "CANCLE"))
        self.pushButton_3.setText(_translate("MainWindow", "PRINT"))
        self.label.setText(_translate("MainWindow", "Customer"))
        self.label_2.setText(_translate("MainWindow", "TextLabel"))
        self.menufile.setTitle(_translate("MainWindow", "FILE"))
        self.menusale.setTitle(_translate("MainWindow", "SALE"))
        self.menubuy.setTitle(_translate("MainWindow", "BUY"))
        self.menureport.setTitle(_translate("MainWindow", "REPORT"))
        self.actionexit.setText(_translate("MainWindow", "logout"))
        self.actionexit_2.setText(_translate("MainWindow", "exit"))
        self.actionDaily.setText(_translate("MainWindow", "Daily"))
        self.actionWeekly.setText(_translate("MainWindow", "Weekly"))
        self.actionYear_to_date.setText(_translate("MainWindow", "Year_to_date"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
