# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'inventory.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.QtCore import (QFile, QFileInfo, QPoint, QSettings, QSignalMapper,
        QSize, QTextStream, Qt)
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtWidgets import (QAction, QApplication, QFileDialog, QMainWindow,
        QMdiArea, QMessageBox, QTextEdit, QWidget)

class Ui_MdiArea(QMainWindow):
    def __init__(self):
        super(Ui_MdiArea, self).__init__()
     
        self.resize(591, 585)
        self.mdiArea = QMdiArea()
        self.setCentralWidget(self.mdiArea)
        
        self.subwindow = QtWidgets.QMdiSubWindow(self.mdiArea)

        self.subwindow.setObjectName("subwindow")
        
        self.subwindow_2 = QtWidgets.QWidget(self.mdiArea)
        self.subwindow_2.setObjectName("subwindow_2")

    
if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    window = Ui_MdiArea()
    window.show()
    sys.exit(app.exec_())
