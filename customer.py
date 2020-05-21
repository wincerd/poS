# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'customer.ui'
#
# Created by: PyQt5 UI code generator 5.14.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from db import database


class Customer_Dialog(QDialog):
    def __init__(self):    
        super(Customer_Dialog,self).__init__()
        
        Dialog = self        
        Dialog.setObjectName("Dialog")
        Dialog.resize(534, 300)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(90, 250, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(40, 30, 67, 17))
        self.label.setObjectName("label")
        self.label.setText("Name")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(40, 120, 67, 17))
        self.label_2.setObjectName("label_2")
        self.label_2.setText("Mobile")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(280, 30, 67, 17))
        self.label_3.setObjectName("label_3")
        self.label_3.setText("Balance")
        
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(130, 30, 113, 25))
        self.lineEdit.setObjectName("Name")
        self.lineEdit_2 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_2.setGeometry(QtCore.QRect(390, 30, 113, 25))
        self.lineEdit_2.setObjectName("Mobile")
        self.lineEdit_3 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_3.setGeometry(QtCore.QRect(130, 120, 113, 25))
        self.lineEdit_3.setObjectName("Balance")

        self.lineEdit_4 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_4.setGeometry(QtCore.QRect(390, 120, 113, 25))
        self.lineEdit_4.setObjectName("Balance")
        


        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        self.accepted.connect(self.saveData)


    def saveData(self):
        name =self.lineEdit.text()
        mobile =self.lineEdit_2.text()
        balance =self.lineEdit_3.text()
        typ = "customer"
        print(typ)
        new = database()        
        a = new.save_contact(name,mobile,balance,typ)
        print(a)
        

if __name__ == '__main__':  

    import sys

    app = QApplication(sys.argv)
    window = Customer_Dialog()
    window.show()
    sys.exit(app.exec_())
