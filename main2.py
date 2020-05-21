from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import( QTableView,QTableWidget,QTableWidgetItem, QHeaderView,QAbstractItemView,QScrollBar,
                             QDialog,QAction,QMessageBox,QWidget,QApplication,QMainWindow,QGridLayout,QMdiArea,
                             QTextEdit,QMdiSubWindow,QStyledItemDelegate,QLineEdit,QCompleter,QVBoxLayout)
from db import database



class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1420, 741)
        self.gridLayoutWidget = QtWidgets.QWidget(Form)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(730, 80, 561, 621))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        
        self.groupBox = QtWidgets.QGroupBox(self.gridLayoutWidget)
        self.groupBox.setObjectName("groupBox")
        
        self.cancel = QtWidgets.QPushButton(self.groupBox)
        self.cancel.setGeometry(QtCore.QRect(240, 0, 101, 25))
        self.cancel.setObjectName("cancel")
        
        self.save = QtWidgets.QPushButton(self.groupBox)
        self.save.setGeometry(QtCore.QRect(390, 0, 89, 25))
        self.save.setObjectName("pushButton")
        
        self.saveNew1 = QtWidgets.QPushButton(self.groupBox)
        self.saveNew1.setGeometry(QtCore.QRect(110, 0, 89, 25))
        self.saveNew1.setObjectName("saveNew1")
        
        self.gridLayout.addWidget(self.groupBox, 2, 1, 1, 1)

        self.groupBox_2 = QtWidgets.QGroupBox(self.gridLayoutWidget)
        self.groupBox_2.setObjectName("groupBox_2")
        
        self.comboBox = QtWidgets.QComboBox(self.groupBox_2)
        self.comboBox.setGeometry(QtCore.QRect(200, 4, 201, 31))
        self.comboBox.setObjectName("comboBox")
        
        self.label = QtWidgets.QLabel(self.groupBox_2)
        self.label.setGeometry(QtCore.QRect(90, 10, 67, 17))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.groupBox_2)
        self.label_2.setGeometry(QtCore.QRect(446, 7, 81, 20))
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.groupBox_2, 0, 1, 1, 1)


        self.tableView = self.SalesTble()
        


        self.gridLayout.addWidget(self.tableView, 1, 1, 1, 1)
        self.scrollArea = QtWidgets.QScrollArea(Form)
        self.scrollArea.setGeometry(QtCore.QRect(79, 99, 611, 581))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 609, 579))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.saveNew = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.saveNew.setGeometry(QtCore.QRect(120, 140, 89, 25))
        self.saveNew.setObjectName("saveNew")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(110, 56, 191, 31))
        self.label_3.setObjectName("label_3")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        
        self.cancel.setText(_translate("Form", "Cancel"))
        self.save.setText(_translate("Form", "Save"))
        self.saveNew1.setText(_translate("Form", "Save$new"))
        self.label.setText(_translate("Form", "TextLabel"))
        self.label_2.setText(_translate("Form", "TextLabel"))
        self.saveNew.setText(_translate("Form", "Save$new"))
        self.label_3.setText(_translate("Form", "TextLabel"))
    def SalesTble(self):
        self.tableView = QTableView(self.gridLayoutWidget)
        # self.layout.addWidget(self.Save, 0,1, 0,4)
##        self.tableView.setItemDelegate(Delegate())
        self.tableView.setStyleSheet(self.stylesheet())
        self.tableView.setGeometry(QtCore.QRect(580, 50, 491, 551))
        self.tableView.setObjectName("tableView")
        
        #self.tableView.setItemDelegate(TableItemCompleter())
        self.model =  QtGui.QStandardItemModel(0,4)
        nrow = self.model.rowCount()
        self.ncol = self.model.columnCount()
        item = QtGui.QStandardItem()
        self.model.itemChanged.connect(self.Itemchanged)
        number = self.model.columnCount() + 1
        
        self.model.setRowCount(50)
        self.model.appendRow(item)
        
        self.model.setHeaderData(0, QtCore.Qt.Horizontal,"id")
        self.model.setHeaderData(1, QtCore.Qt.Horizontal,"description")
        self.model.setHeaderData(2, QtCore.Qt.Horizontal,"quantity")
        self.model.setHeaderData(3, QtCore.Qt.Horizontal,"price")
        
        self.tableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableView.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.tableView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.tableView.setModel(self.model)
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.setShowGrid(True)
        self.tableView.verticalHeader().setSectionResizeMode(3)
        self.tableView.keyPressEvent = self.newOnkeyPressEvent

    def Itemchanged(self,e):
        data = self.data()   
##        ("colum changed",e.column(),e.row())
        print("data",data)
        length= len(data)
        ID = data[length - 1][0]
        if  ID != "":
            rcl = self.new.items_name(ID)
            print(rcl)
            for i in range(1,self.ncol):
                f = rcl[0][i]
                self.model.setData(self.model.index(e.row(), i), f, 0)     
            print("rcl",rcl)
        else:
            print("not string")
        v = self.new.item_list()
        rows = sorted(set(index.row() for index in
                      self.tableView.selectedIndexes()))
        for row in rows:
            print('Row %d is selected' % row)
        for i in data:
            print(i)
        return data
    def newOnkeyPressEvent(self,e):
        if e.key() == QtCore.Qt.Key_Escape:
            print ("User has pushed escape")
    def addRow(self):
        item = QtGui.QStandardItem("")
        self.model.appendRow(item)
        self.isChanged = True   
    def stylesheet(self):
        return """
        QTableView
        {
            border: 1px solid grey;
            border-radius: 0px;
            font-family: DroidSans;
            font-size: 11px;
            background-color: #f8f8f8;
            selection-color: #e9e9e9
        }
        QTableView::item:hover
        {   
            color: black;
            background:#CFCA59;            
        }
        
        QTableView::item:selected {
            color: #e9e9e9;
            background: #2F6299;
        } 
        QTableView QTableCornerButton::section {
            background: #D6D1D1;
            border: 1px outset black;
        }
        QPushButton
        {
            font-size: 11px;
        } 
        QPushButton::hover
        {
            font-size: 11px;
            border: 2px inset #353535;
            font-style: oblique;
            font-weight: bold;
            color: #90150A; 
            border-radius: 4px;
            background-color: #C5C5C5;
        } 
    """


import sys
class Main(QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        # build ui
        self.ui = Ui_Form()
        self.ui.setupUi(self)
    
    


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())
