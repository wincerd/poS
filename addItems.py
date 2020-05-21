# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'add_items.ui'
#
# Created by: PyQt5 UI code generator 5.14.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget,QDialog,QApplication
from db import database


class Ui_Dialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent=None)
        Dialog =self
        Dialog.setObjectName("Dialog")
        Dialog.resize(635, 378)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(160, 320, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        
        self.comboBox = QtWidgets.QComboBox(Dialog)
        self.comboBox.setGeometry(QtCore.QRect(110, 30, 211, 27))
        self.comboBox.setObjectName("comboBox")
        
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(110, 110, 211, 31))
        self.lineEdit.setObjectName("desc")

        
        self.lineEdit_2 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_2.setGeometry(QtCore.QRect(340, 190, 81, 27))
        self.lineEdit_2.setObjectName("name")
        
        
        self.lineEdit_4 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_4.setGeometry(QtCore.QRect(430, 110, 151, 31))
        self.lineEdit_4.setObjectName("cost")
        
        self.lineEdit_3 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_3.setGeometry(QtCore.QRect(500, 190, 81, 27))
        self.lineEdit_3.setObjectName("price")
        
        self.comboBox_2 = QtWidgets.QComboBox(Dialog)
        self.comboBox_2.setGeometry(QtCore.QRect(110, 190, 131, 27))
        self.comboBox_2.setObjectName("comboBox_2")
        
        
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 30, 67, 17))
        self.label.setObjectName("label")
        self.label.setText("1")
        
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(20, 120, 67, 17))
        self.label_2.setObjectName("label_2")
        self.label_2.setText("descript")
        
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(350, 120, 67, 17))
        self.label_3.setObjectName("label_3")
        self.label_3.setText("name")
        
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(20, 190, 67, 17))
        self.label_4.setObjectName("label_4")
        self.label_4.setText("Category")
        
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(270, 190, 67, 17))
        self.label_5.setObjectName("label_5")
        self.label_5.setText("cost")
        
        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(430, 190, 67, 17))
        self.label_6.setObjectName("label_6")
        self.label_6.setText("Price")

        
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        self.accepted.connect(self.saveData)

    def saveData(self):
        descript =self.lineEdit.text()
        cost =self.lineEdit_3.text()
        price =self.lineEdit_2.text()
        name = self.lineEdit_4.text()
        new = database()
        
        new.save_item(descript,name,price,cost)
        
        
        
if __name__ == '__main__':  

    import sys

    app = QApplication(sys.argv)
    window = Ui_Dialog()
    window.show()
    sys.exit(app.exec_())
