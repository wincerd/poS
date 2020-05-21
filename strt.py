from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from PyQt5 import QtCore, QtGui, QtWidgets,QtPrintSupport
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtSql import QSqlTableModel, QSqlDatabase
from addItems import Ui_Dialog
from db import database
from main import Ui_Form
from customer import Customer_Dialog
from supplier import Supplier_Dialog


import mdi_rc

class FlowLayout(QtWidgets.QLayout):
    def __init__(self, parent=None, margin=-1, hspacing=-1, vspacing=-1):
        super(FlowLayout, self).__init__(parent)
        self._hspacing = hspacing
        self._vspacing = vspacing
        self._items = []
        self.setContentsMargins(margin, margin, margin, margin)

    def __del__(self):
        del self._items[:]

    def addItem(self, item):
        self._items.append(item)

    def horizontalSpacing(self):
        if self._hspacing >= 0:
            return self._hspacing
        else:
            return self.smartSpacing(
                QtWidgets.QStyle.PM_LayoutHorizontalSpacing)

    def verticalSpacing(self):
        if self._vspacing >= 0:
            return self._vspacing
        else:
            return self.smartSpacing(
                QtWidgets.QStyle.PM_LayoutVerticalSpacing)

    def count(self):
        return len(self._items)

    def itemAt(self, index):
        if 0 <= index < len(self._items):
            return self._items[index]

    def takeAt(self, index):
        if 0 <= index < len(self._items):
            return self._items.pop(index)

    def expandingDirections(self):
        return QtCore.Qt.Orientations(0)

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        return self.doLayout(QtCore.QRect(0, 0, width, 0), True)

    def setGeometry(self, rect):
        super(FlowLayout, self).setGeometry(rect)
        self.doLayout(rect, False)

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        size = QtCore.QSize()
        for item in self._items:
            size = size.expandedTo(item.minimumSize())
        left, top, right, bottom = self.getContentsMargins()
        size += QtCore.QSize(left + right, top + bottom)
        return size

    def doLayout(self, rect, testonly):
        left, top, right, bottom = self.getContentsMargins()
        effective = rect.adjusted(+left, +top, -right, -bottom)
        x = effective.x()
        y = effective.y()
        lineheight = 0
        for item in self._items:
            widget = item.widget()
            hspace = self.horizontalSpacing()
            if hspace == -1:
                hspace = widget.style().layoutSpacing(
                    QtWidgets.QSizePolicy.PushButton,
                    QtWidgets.QSizePolicy.PushButton, QtCore.Qt.Horizontal)
            vspace = self.verticalSpacing()
            if vspace == -1:
                vspace = widget.style().layoutSpacing(
                    QtWidgets.QSizePolicy.PushButton,
                    QtWidgets.QSizePolicy.PushButton, QtCore.Qt.Vertical)
            nextX = x + item.sizeHint().width() + hspace
            if nextX - hspace > effective.right() and lineheight > 0:
                x = effective.x()
                y = y + lineheight + vspace
                nextX = x + item.sizeHint().width() + hspace
                lineheight = 0
            if not testonly:
                item.setGeometry(
                    QtCore.QRect(QtCore.QPoint(x, y), item.sizeHint()))
            x = nextX
            lineheight = max(lineheight, item.sizeHint().height())
        return y + lineheight - rect.y() + bottom

    def smartSpacing(self, pm):
        parent = self.parent()
        if parent is None:
            return -1
        elif parent.isWidgetType():
            return parent.style().pixelMetric(pm, None, parent)
        else:
            return parent.spacing()


class Button(QtWidgets.QPushButton):
    def __init__(self,text):
        super(Button,self).__init__(text)
        self.word = text


        
class Ui_MainWindow(QMainWindow):
    count = 0
    a= []
    def __init__(self,parent=None):
        super().__init__(parent)
        self.counter = 0
        self.row = 0
        self.mdiArea = QMdiArea()
        self.setCentralWidget(self.mdiArea)
        self.layout = QtWidgets.QGridLayout(self)
        self.ni = Subwindow(self.mdiArea)
        self.panel = Ui_Dialog()
        self.wind = Ui_Form()

        
        self.mdiArea.addSubWindow(self.ni)
        self.mdiArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.mdiArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        self.setCentralWidget(self.mdiArea)
        self.new = database()
        
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


        self.gridLayoutWidget = QtWidgets.QWidget(self.subwindow)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(730, 80, 561, 621))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        
        
        self.groupBox = QtWidgets.QGroupBox(self.gridLayoutWidget)
        self.groupBox.setObjectName("groupBox")
        self.groupBox.setMinimumSize(QtCore.QSize(0, 100))
        
        self.gridLayout.addWidget(self.groupBox, 2, 1, 1, 1)

        self.groupBox_2 = QtWidgets.QGroupBox(self.gridLayoutWidget)
        self.groupBox_2.setObjectName("groupBox_2")
    
        self.gridLayout.addWidget(self.groupBox_2, 0, 1, 1, 1)

        self.sales()
        self.SalesTble()
        self.data()
        self.find_customers()
        self.side()
##        self.subwindow.hide()
    def createActions(self):
        self.menubuy = QAction("&menubuy",statusTip="Create a new file", triggered=self.win)
        self.login = QAction("&Login",statusTip="Login", triggered=self.sales)
        self.sell = QAction("&Sell",statusTip="Make a sale", triggered=self.sales)
        self.buy = QAction("&Buy",statusTip="Buy goods", triggered=self.Buy)
        self.Add_customer = QAction("&Add customer",statusTip="Buy goods", triggered=self.customer)
        self.Add_supplier =QAction("&Add Supplier",statusTip="Buy goods", triggered=self.supplier)
        self.bydy = QAction("&By day",statusTip="get report by Day", triggered=self.sales)
        self.bymnth = QAction("&By month",statusTip="get report by mounth", triggered=self.sales)
        self.byyear = QAction("&By year",statusTip="get report by year", triggered=self.sales)
        self.exit = QAction("&Exit",statusTip="exit the application", triggered=QApplication.instance().closeAllWindows)
        
        
    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.login)
        self.fileMenu.addAction(self.exit)
        self.fileMenu = self.menuBar().addMenu("&Actions")
        self.fileMenu.addAction(self.sell)
        self.fileMenu.addAction(self.buy)
        self.fileMenu.addAction(self.Add_supplier)
        self.fileMenu.addAction(self.Add_customer)
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
        
        self.Save = QtWidgets.QPushButton(self.groupBox)
        self.Save.setGeometry(QtCore.QRect(110, 60, 89, 25))
        self.Save.setText("Save")
        self.Save.setObjectName("pushButton")
        self.Save.clicked.connect(self.save_data)
        
        self.SaveNew = QtWidgets.QPushButton(self.groupBox)
        self.SaveNew.setGeometry(QtCore.QRect(240, 60, 101, 25))
        self.SaveNew.setText("Save&new")
        self.SaveNew.setObjectName("SaveNew")
        
        self.Cancel = QtWidgets.QPushButton(self.groupBox)
        self.Cancel.setGeometry(QtCore.QRect(390, 60, 89, 25))
        self.Cancel.setObjectName("Cancel")
        self.Cancel.setText("Cancel")
        self.Cancel.clicked.connect(self.data)

        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setGeometry(QtCore.QRect(270, 10, 67, 17))
        self.label_4.setObjectName("Total")
        self.label_4.setText("Total")


        self.lineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit.setGeometry(QtCore.QRect(380, 10, 113, 25))
        self.lineEdit.setObjectName("Totaltxt")

        
        
        self.customerLbl = QtWidgets.QLabel(self.groupBox_2)
        self.customerLbl.setGeometry(QtCore.QRect(90, 10, 67, 17))
        self.customerLbl.setText("Customers")
        self.customerLbl.setObjectName("label")
        
        self.customer2Lbl = QtWidgets.QLabel(self.groupBox_2)
        self.customer2Lbl.setGeometry(QtCore.QRect(446, 7, 81, 20))
        self.customer2Lbl.setText("Customers")
        self.customer2Lbl.setObjectName("customer2Lbl")
        
        
    def customer(self):
        self.customer = Customer_Dialog()
        self.customer.show()
    def supplier(self):
        self.supplier = Supplier_Dialog()
        self.supplier.show()
    def Buy(self):
        self.panel.show()

    def win(self):
        self.ni.show()

    def inventory(self):
        fileName = "."
        TabDialog(fileName)
    def side(self):
        completion_ls =[]
        text = self.new.item_list()
        for b in text:
            print("b",b[0])
            completion_ls.append(b[0])
        self.scrollArea = QtWidgets.QScrollArea(self.subwindow)
        self.scrollArea.setGeometry(QtCore.QRect(79, 99, 611, 581))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 609, 579))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        layout = FlowLayout(self.scrollArea)
        self.words = []
        self.button_map = {}
        for word in completion_ls:
            self.lbl = Button(word)
            self.lbl.setFont(QtGui.QFont('SblHebrew', 18))
            self.lbl.clicked.connect(lambda arg, text = str(self.lbl.text()): self.commander(text))
            self.words.append(self.lbl)
            self.saveButton(self.lbl)
            layout.addWidget(self.lbl)
        
        
        
    def findButtonByText(self,text):
         """
         Returns the QPushButton instance
         :param text: the button text
         :return the QPushButton object 
         """
         return button_map[text]
    def saveButton(self,obj):
         """
         Saves the button in the map
         :param  obj: the QPushButton object
         """
         self.button_map[obj.text()] = obj
    def commander(self,word):
        exPopup = self.dial(word)
        
        
   
    def SalesTble(self):
        self.tableView = QTableView(self.subwindow)
        self.gridLayout.addWidget(self.tableView, 1, 1, 1, 1)
        self.tableView.setStyleSheet(stylesheet(self))
        self.tableView.setGeometry(QtCore.QRect(580, 50, 491, 551))
        self.tableView.setObjectName("tableView")
        self.model =  QtGui.QStandardItemModel(0,5)
        self.nrow = self.model.rowCount()
        self.ncol = self.model.columnCount()
        item = QtGui.QStandardItem()
        self.model.itemChanged.connect(self.Itemchanged)
        number = self.model.columnCount() + 1
        
        self.model.setRowCount(50)
        self.model.appendRow(item)
        
        self.model.setHeaderData(0, QtCore.Qt.Horizontal,"id")
        self.model.setHeaderData(1, QtCore.Qt.Horizontal,"name")
        self.model.setHeaderData(2, QtCore.Qt.Horizontal,"price")
        self.model.setHeaderData(3, QtCore.Qt.Horizontal,"quantity")
        self.model.setHeaderData(4, QtCore.Qt.Horizontal,"amount")

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
        for row in range(self.model.rowCount()):
          data.append([])
          for column in range(self.model.columnCount()):
            index = self.model.index(row, column)
            # We suppose data are strings
            data[row].append(str(self.model.data(index)))
        
        self.tableView.setItemDelegate(TableItemCompleter(self.tableView))
        d=[]
        for raw in data:
            count = 0
            for i in raw:
                if i == 'None':
                    count = count + 1
            if count < 5:
                x= (row,column)
                d.append(raw)
        return d        
    def save_data(self):
        data = self.data()
        self.new.make_sale(data)
        for i in range(0,self.ncol- 2):
                f = ''
                self.model.setData(self.model.index(self.nrow, i), f, 0)
        self.counter = 0
    def Itemchanged(self,e):
        #  number of columns in the table which  are not empty
        print("changed")
        data = self.data()
        # lineEdit
        sm = []
        for i in data:
            if  i[3] != 'None' and i[2] != 'None':
                print("deb",i[3])
                sm.append(float(i[2])* float(i[3]))
                i[4] = float(i[2])* float(i[3])
        s = sum(sm)
        self.lineEdit.setText(str(s))
        print("counterr",self.counter)
        # ("colum changed",e.column(),e.row())
        length= len(data)
        ID = data[length - 1][1]
        if  ID != "":
            #  get list of items with name
            rcl = self.new.items_name(ID)
            print("iemz",rcl)
            #for i in  range  number of columns
            for i in range(0,self.ncol- 2):
                f = rcl[0][i]
                self.model.setData(self.model.index(e.row(), i), f, 0)
            rows = sorted(set(index.row() for index in
                      self.tableView.selectedIndexes()))
            row = 0
            for row in rows:
                row = row
                print('Row %d is selected' % row)
            #value of the last edited row
            ttl=  data[row][-1]
            if ttl == 'None':
                ttl = 0
            print("ttl",ttl)
            self.model.setData(self.model.index(row, 4),ttl, 0)
        else:
            print("not string")
        v = self.new.item_list()
        
        for i in data:
            print(i)
        return data


    def find_customers(self):
        self.comboBox = QtWidgets.QComboBox(self.groupBox_2)
        self.layout.addWidget(self.comboBox,0,2)
        self.comboBox.setGeometry(QtCore.QRect(200, 4, 201, 31))
        self.comboBox.setEditable(True)
        self.comboBox.setObjectName("comboBox")      
        data = self.new.customers()
        for i in data:
            self.comboBox.addItem(i[0])
            
        
    def newOnkeyPressEvent(self,e):
        if e.key() == QtCore.Qt.Key_Escape:
            print ("User has pushed escape")
    def addRow(self):
        item = QtGui.QStandardItem("")
        self.model.appendRow(item)
        self.isChanged = True       

    def dial(self,name):
        length = len(self.data())
        if length == 0:
            self.counter = self.counter + 1
        else:
            length  + 1 
        self.counter = length
        self.dialog = QDialog(self)
        self.dialog.setGeometry(100, 200, 100, 100)
        self.count  = 0
        self.name = name
        self.grid  =  QGridLayout(self.dialog)
        self.label = QLabel(self.name)
        self.btn = QtWidgets.QPushButton()
        self.btn.setObjectName("kilo1")
        self.btn.setText("1 Kg")
        self.btn.clicked.connect(lambda arg, text = name,num = 1: self.calculate(text,num))
        self.btn1 = QtWidgets.QPushButton()
        self.btn1.setObjectName("half")
        self.btn1.setText("1/2")
        self.btn1.clicked.connect(lambda arg, text = name,num = 0.5: self.calculate(text,num))
        self.btn2 = QtWidgets.QPushButton()
        self.btn2.setObjectName("quater")
        self.btn2.setText("1/4")
        self.btn2.clicked.connect(lambda arg, text = name,num = 0.25: self.calculate(text,num))
        self.btn3 = QtWidgets.QPushButton()
        self.btn3.setObjectName("3quater")
        self.btn3.setText("3/4")
        self.btn3.clicked.connect(lambda arg, text = name,num = 0.75: self.calculate(text,num))
        self.btn4 = QtWidgets.QPushButton()
        self.btn4.setObjectName("rem")
        self.btn4.setText("-")
        self.btn4.clicked.connect(lambda arg, text = name,num = -1: self.calculate(text,num))
        self.btn5 = QtWidgets.QPushButton()
        self.btn5.setObjectName("add")
        self.btn5.setText("+")
        self.btn5.clicked.connect(lambda arg, text = name,num = "+1": self.calculate(text,num))
        self.grid.addWidget(self.btn,0,0)
        self.grid.addWidget(self.btn1,0,1)
        self.grid.addWidget(self.btn2,1,0)
        self.grid.addWidget(self.btn3,1,1)
        self.grid.addWidget(self.btn4,2,0)
        self.grid.addWidget(self.btn5,2,1)
        self.dialog.show()
    def calculate(self,name,num):
        if num == -1:
            if len(self.a) > 1 :
                self.a.pop()
                self.count = self.a[-1]
            else:
                self.a = []
                self.count= 0
        elif num == "+1":
            if len(self.a) != 0:
                self.count = self.count +self.a[-1]
                self.a.append(self.count)
        else:
            self.count = self.count + num
            self.a.append(self.count)

        self.callback(self.a,name)

        return(self.a,name)
    def callback(self,dick,name):
        print(self.counter,"count")
        dat = self.data()
        print(dat)
        length = len(self.data())
        self.model.setData(self.model.index(self.counter, 1), name, 0)
        self.model.setData(self.model.index(self.counter, 3), dick[-1], 0)        

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
    def createEditor(self, parent, styleOption, index):
        # editor = QLineEdit(parent)
        editor = QtWidgets.QComboBox(parent)
        editor.setEditable(True)
        completion_ls =[]
        data = self.new.item_list()
        for b in data:
            print("b",b[0])
            completion_ls.append(b[0])
        editor.addItems(completion_ls)
        autoComplete = QCompleter(completion_ls)
        autoComplete.setCompletionColumn(1)
        autoComplete.setCompletionRole(QtCore.Qt.EditRole)
        autoComplete.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        editor.setCompleter(autoComplete)
        return editor
    def setEditorData(self, editor, index):
        print( "setEditorData")
        super().setEditorData(editor, index)
    def closeEditor(self, editor, hint=None):
        print( "closeEditor")
        super().closeEditor(editor, hint)
    def commitData(self, editor):
        print( "commitData")
        super().commitData(editor)
    

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
class Button(QtWidgets.QPushButton):
    def __init__(self,text):
        super(Button,self).__init__(text)
        self.word = text
    

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = Ui_MainWindow()
    window.show()   
    Mwindow = Mwindow()
    Subwindow =Subwindow(Mwindow)
    Ui_Dialog =Ui_Dialog()
    sys.exit(app.exec_())
