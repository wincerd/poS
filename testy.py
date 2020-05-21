import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget, QListWidget, QListWidgetItem, QLabel, QApplication, QDialog,QGridLayout


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
    
        

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, text, parent=None):
        super(MainWindow, self).__init__(parent)
        
        self.mainArea = QtWidgets.QScrollArea(self)
        self.mainArea.setWidgetResizable(True)
        widget = QtWidgets.QWidget(self.mainArea)
        widget.setMinimumWidth(50)
        layout = FlowLayout(widget)
        self.words = []
        self.button_map = {}
        for word in text.split():
            label = Button(word)
            label.setFont(QtGui.QFont('SblHebrew', 18))
            
            label.clicked.connect(lambda arg, text = str(label.text()): self.commander(text))
            self.words.append(label)
            self.saveButton(label)
            layout.addWidget(label)
        self.mainArea.setWidget(widget)
        self.setCentralWidget(self.mainArea)
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
        exPopup = ExamplePopup(word, self)
        exPopup.setGeometry(100, 200, 100, 100)
        exPopup.show()

class ExamplePopup(QDialog):
    count = 0
    a= []
    def __init__(self, name, parent=None):
        super().__init__(parent)
        self.count  = 0
        self.name = name
        grid  =  QGridLayout()
        self.label = QLabel(self.name, self)
        self.btn = QtWidgets.QPushButton(self)
        self.btn.setObjectName("kilo1")
        self.btn.setText("1 Kg")
        self.btn.clicked.connect(lambda arg, text = name,num = 1: self.calculate(text,num))
        self.btn1 = QtWidgets.QPushButton(self)
        self.btn1.setObjectName("half")
        self.btn1.setText("1/2")
        self.btn1.clicked.connect(lambda arg, text = name,num = 0.5: self.calculate(text,num))
        self.btn2 = QtWidgets.QPushButton(self)
        self.btn2.setObjectName("quater")
        self.btn2.setText("1/4")
        self.btn2.clicked.connect(lambda arg, text = name,num = 0.25: self.calculate(text,num))
        self.btn3 = QtWidgets.QPushButton(self)
        self.btn3.setObjectName("3quater")
        self.btn3.setText("3/4")
        self.btn3.clicked.connect(lambda arg, text = name,num = 0.75: self.calculate(text,num))
        self.btn4 = QtWidgets.QPushButton(self)
        self.btn4.setObjectName("rem")
        self.btn4.setText("-")
        self.btn4.clicked.connect(lambda arg, text = name,num = -1: self.calculate(text,num))
        self.btn5 = QtWidgets.QPushButton(self)
        self.btn5.setObjectName("add")
        self.btn5.setText("+")
        self.btn5.clicked.connect(lambda arg, text = name,num = "+1": self.calculate(text,num))
        grid.addWidget(self.btn,0,0)
        grid.addWidget(self.btn1,0,1)
        grid.addWidget(self.btn2,1,0)
        grid.addWidget(self.btn3,1,1)
        grid.addWidget(self.btn4,2,0)
        grid.addWidget(self.btn5,2,1)
        self.setLayout(grid)
    def calculate(self,name,num):
        if num == -1:
            if len(ExamplePopup.a) > 1 :
                ExamplePopup.a.pop()
                ExamplePopup.count = ExamplePopup.a[-1]
            else:
                ExamplePopup.a = []
                ExamplePopup.count= 0

        elif num == "+1":
            if len(ExamplePopup.a) != 0:
                ExamplePopup.count = ExamplePopup.count +ExamplePopup.a[-1]
                ExamplePopup.a.append(ExamplePopup.count)
        else:
            ExamplePopup.count = ExamplePopup.count + num
            ExamplePopup.a.append(ExamplePopup.count)
        print(ExamplePopup.a,name)

        

        
if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow('Harry Potter is a series of fantasy literature')
    window.show()
    sys.exit(app.exec_())
