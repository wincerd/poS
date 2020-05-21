import sys
from PyQt5 import QtCore

from PyQt5 import QtWidgets


class Ui_Qwid(object):
    def setupUi(self, Qwid):
        Qwid.setObjectName("Qwid")
        Qwid.resize(423, 795)
        Qwid.setWindowTitle("Softs de secours")
        self.gridLayoutWidget = QtWidgets.QWidget(Qwid)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(-1, 9, 431, 791))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")


class Widget(QtWidgets.QWidget, Ui_Qwid):
    def __init__(self, parent=None):
        super(Widget, self).__init__(parent=parent)
        self.setupUi(self)

        self.les_soft = {'key1': 'url1', 'key2': 'url2', 'key3': 'url3', 'key4': 'url4',
                         'key5': 'key5', 'key6': 'url6', 'key7': 'url7', 'key8': 'url8'}

        for key, val in self.les_soft.items():
            self.btn = QtWidgets.QPushButton(key)
            self.gridLayout.addWidget(self.btn)
            self.btn.clicked.connect(self.download)

    def download(self):
        key = self.sender().text()
        print(key)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = Widget()
    w.show()
    sys.exit(app.exec_())
