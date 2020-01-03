
from PyQt5.QtCore import (QFile, QFileInfo, QPoint, QSettings, QSignalMapper,
        QSize, QTextStream, Qt)



from PyQt5 import QtCore, QtGui, QtWidgets,QtPrintSupport
from PyQt5.QtWidgets import( QTableView,QTableWidget,QTableWidgetItem, QHeaderView,QAbstractItemView,QScrollBar,
                             QDialog,QAction,QMessageBox,QWidget,QApplication,QMainWindow,QGridLayout,QMdiArea,QTextEdit,QMdiSubWindow,QStyledItemDelegate,QLineEdit,QCompleter)
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtSql import QSqlTableModel, QSqlDatabase
from addItems import Ui_Dialog
from db import database


import mdi_rc

class Ui_MainWindow(QMainWindow):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.mdiArea = QMdiArea()
        self.ni = Subwindow(self.mdiArea)
        self.panel = Ui_Dialog()
        self.mdiArea.addSubWindow(self.ni)
        self.mdiArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.mdiArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setCentralWidget(self.mdiArea)
        self.new = database()
        self.new.connect()

        self.mdiArea.subWindowActivated.connect(self.updateMenus)
        self.windowMapper = QSignalMapper(self)
        self.windowMapper.mapped[QWidget].connect(self.setActiveSubWindow)
        self.resize(1090, 781)
        self.createActions()
        self.createMenus()
        self.createToolBars()
        self.createStatusBar()
        self.updateMenus()
        self.setWindowTitle("MDI")
        self.subwindow = QtWidgets.QMdiSubWindow(self.mdiArea)
        self.subwindow.setObjectName("subwindow")
        self.sales()
        self.SalesTble()
        self.data()
        self.find_customers()
        

        
##        self.subwindow.hide()
    def createActions(self):
        self.menubuy = QAction("&menubuy",statusTip="Create a new file", triggered=self.win)
        self.login = QAction("&Login",statusTip="Login", triggered=self.sales)
        self.sell = QAction("&Sell",statusTip="Make a sale", triggered=self.sales)
        self.buy = QAction("&Buy",statusTip="Buy goods", triggered=self.Buy)
        self.bydy = QAction("&By day",statusTip="get report by Day", triggered=self.sales)
        self.bymnth = QAction("&By month",statusTip="get report by mounth", triggered=self.sales)
        self.byyear = QAction("&By year",statusTip="get report by year", triggered=self.sales)
        self.exit = QAction("&Exit",statusTip="exit the application", triggered=QApplication.instance().closeAllWindows)
        
        
    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.login)
        self.fileMenu.addAction(self.exit)
        self.fileMenu = self.menuBar().addMenu("&Sell")
        self.fileMenu.addAction(self.sell)
        self.fileMenu.addAction(self.buy)
        self.fileMenu = self.menuBar().addMenu("&Report")
        self.fileMenu.addAction(self.bydy)
        self.fileMenu.addAction(self.bymnth)
        self.fileMenu.addAction(self.byyear)
        self.fileMenu = self.menuBar().addMenu("&About")


    def closeEvent(self, event):
        self.mdiArea.closeAllSubWindows()
        if self.mdiArea.currentSubWindow():
            event.ignore()
        else:
            self.writeSettings()
            event.accept()

    def about(self):
        QMessageBox.about(self, "About MDI",
                "The <b>MDI</b> example demonstrates how to write multiple "
                "document interface applications using Qt.")

    def updateMenus(self):
        hasMdiChild = (self.activeMdiChild() is not None)
        
    def updateWindowMenu(self):
        self.windowMenu.clear()
        self.windowMenu.addAction(self.closeAct)
        
        windows = self.mdiArea.subWindowList()
        self.separatorAct.setVisible(len(windows) != 0)

        for i, window in enumerate(windows):
            child = window.widget()

            text = "%d %s" % (i + 1, child.userFriendlyCurrentFile())
            if i < 9:
                text = '&' + text

            action = self.windowMenu.addAction(text)
            action.setCheckable(True)
            action.setChecked(child is self.activeMdiChild())
            action.triggered.connect(self.windowMapper.map)
            self.windowMapper.setMapping(action, window)

    def createMdiChild(self):
        child = Sales()
        self.mdiArea.addSubWindow(child)

        child.copyAvailable.connect(self.cutAct.setEnabled)
        child.copyAvailable.connect(self.copyAct.setEnabled)

        return child
    def createToolBars(self):
        self.fileToolBar = self.addToolBar("File")
        self.fileToolBar.addAction(self.menubuy)
        self.fileToolBar.addAction(self.login)
    def createStatusBar(self):
        self.statusBar().showMessage("Ready")

    def readSettings(self):
        settings = QSettings('Trolltech', 'MDI Example')
        pos = settings.value('pos', QPoint(200, 200))
        size = settings.value('size', QSize(400, 400))
        self.move(pos)
        self.resize(size)

    def writeSettings(self):
        settings = QSettings('Trolltech', 'MDI Example')
        settings.setValue('pos', self.pos())
        settings.setValue('size', self.size())

    def activeMdiChild(self):
        activeSubWindow = self.mdiArea.activeSubWindow()
        if activeSubWindow:
            return activeSubWindow.widget()
        return None

    def findMdiChild(self, fileName):
        canonicalFilePath = QFileInfo(fileName).canonicalFilePath()

        for window in self.mdiArea.subWindowList():
            if window.widget().currentFile() == canonicalFilePath:
                return window
        return None

    def switchLayoutDirection(self):
        if self.layoutDirection() == Qt.LeftToRight:
            QApplication.setLayoutDirection(Qt.RightToLeft)
        else:
            QApplication.setLayoutDirection(Qt.LeftToRight)

    def setActiveSubWindow(self, window):
        if window:
            self.mdiArea.setActiveSubWindow(window)

    def sales(self):
        self.subwindow.show()
        self.subwindow.resize(1090, 781)
        self.Save = QtWidgets.QPushButton(self.subwindow)
        self.Save.setGeometry(QtCore.QRect(660, 620, 75, 23))
        self.Save.setObjectName("pushButton")
        
        self.SaveNew = QtWidgets.QPushButton(self.subwindow)
        self.SaveNew.setGeometry(QtCore.QRect(760, 620, 75, 23))
        self.SaveNew.setObjectName("SaveNew")
        
        self.Cancel = QtWidgets.QPushButton(self.subwindow)
        self.Cancel.setGeometry(QtCore.QRect(890, 620, 75, 23))
        self.Cancel.setObjectName("Cancel")
        self.Cancel.clicked.connect(self.data)
        
        
        self.customerLbl = QtWidgets.QLabel(self.subwindow)
        self.customerLbl.setGeometry(QtCore.QRect(580, 20, 71, 21))
        self.customerLbl.setText("Customers")
        self.customerLbl.setObjectName("label")
        
        self.customer2Lbl = QtWidgets.QLabel(self.subwindow)
        self.customer2Lbl.setGeometry(QtCore.QRect(910, 20, 121, 21))
        self.customer2Lbl.setText("Customers")
        self.customer2Lbl.setObjectName("customer2Lbl")
    def Buy(self):
        
        self.panel.show()

    def win(self):
        self.ni.show()

    def inventory(self):
        fileName = "."
        TabDialog(fileName)
        
   
    def SalesTble(self):
        self.tableView = QTableView(self.subwindow)
        self.tableView.setItemDelegateForColumn(0, (TableItemCompleter()))
##        self.tableView.setItemDelegate(Delegate())
        self.tableView.setStyleSheet(stylesheet(self))
        self.tableView.setGeometry(QtCore.QRect(580, 50, 491, 551))
        self.tableView.setObjectName("tableView")
        #self.tableView.setItemDelegate(TableItemCompleter())
        self.model =  QtGui.QStandardItemModel(0,4)
        nrow = self.model.rowCount()
        ncol = self.model.columnCount()
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
    
    def data(self):
        model = self.tableView.model()
        data = []
        datas = {}
        for row in range(self.model.rowCount()):
          data.append([])
          for column in range(self.model.columnCount()):
            index = self.model.index(row, column)
            # We suppose data are strings
            data[row].append(str(self.model.data(index)))
        d=[]
##        c = QtWidgets.QComboBox(self.tableView)
##        c.setEditable(True)
##        c.addItems(['aell11','bell12','cell13','cell14','zell15',])
##        self.tableView.setIndexWidget(self.model.index(0, 0),c)
        v = self.new.item_list() 
        print(v)
        for raw in data:
            count = 0
            for i in raw:
                if i == 'None':
                    count = count + 1
            if count < 4:
                x= (row,column)
                print(x)
                d.append(raw)

        return d        
        
    def Itemchanged(self,e):
        data = self.data()

        print("eee",e.column(),e.row())
        v = self.new.item_list()
        
        rows = sorted(set(index.row() for index in
                      self.tableView.selectedIndexes()))
        for row in rows:
            print('Row %d is selected' % row)
        for i in data:
            print(i)

        return data

    def find_customers(self):
        self.comboBox = QtWidgets.QComboBox(self.subwindow)
        self.comboBox.setGeometry(QtCore.QRect(640, 20, 191, 22))
        self.comboBox.setEditable(True)
        self.comboBox.setObjectName("comboBox")
        
        data = self.new.customers()
        print(data)
        for i in data:
            self.comboBox.addItem(i[0])
            
        
    def newOnkeyPressEvent(self,e):
        if e.key() == QtCore.Qt.Key_Escape:
            print ("User has pushed escape")
    def addRow(self):
        item = QtGui.QStandardItem("")
        self.model.appendRow(item)
        self.isChanged = True       
class Mwindow(QMdiArea):
    def __init__(self, parent=None):
        super().__init__(parent=None)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
class Subwindow(QMdiSubWindow):
    def __init__(self, parent=None):
        super(Subwindow, self).__init__(parent=None)
        self.resize(635, 378)
class TableItemCompleter(QStyledItemDelegate):
    def __init__(self, parent = None):
        super(TableItemCompleter, self).__init__(parent)
        self.new = database()
        self.new.connect()

    def createEditor(self, parent, styleOption, index):
        editor = QLineEdit(parent)
        completion_ls =[]
        data = self.new.item_list()
        for i in data:
            for b in i:
                completion_ls.append(b)
        autoComplete = QCompleter(completion_ls)
        editor.setCompleter(autoComplete)
        return editor

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

if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    window = Ui_MainWindow()
    window.show()   
    Mwindow = Mwindow()
    Subwindow =Subwindow(Mwindow)
    Ui_Dialog =Ui_Dialog()
    sys.exit(app.exec_())
