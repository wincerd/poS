from PyQt5 import QtWidgets, QtCore

class Delegate(QtWidgets.QItemDelegate):
    def __init__(self, owner, choices):
        super().__init__(owner)
        self.items = choices
    def createEditor(self, parent, option, index):
        self.editor = QtWidgets.QComboBox(parent)
        self.editor.addItems(self.items)
        return self.editor
    def paint(self, painter, option, index):
        value = index.data(QtCore.Qt.DisplayRole)
        style = QtWidgets.QApplication.style()
        opt = QtWidgets.QStyleOptionComboBox()
        opt.text = str(value)
        opt.rect = option.rect
        style.drawComplexControl(QtWidgets.QStyle.CC_ComboBox, opt, painter)
        QtWidgets.QItemDelegate.paint(self, painter, option, index)
    def setEditorData(self, editor, index):
        value = index.data(QtCore.Qt.DisplayRole)
        num = self.items.index(value)
        editor.setCurrentIndex(num)
    def setModelData(self, editor, model, index):
        value = editor.currentText()
        model.setData(index, QtCore.Qt.DisplayRole, QtCore.QVariant(value))
    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)

class Model(QtCore.QAbstractTableModel):
    def __init__(self, table):
        super().__init__()
        self.table = table
    def rowCount(self, parent):
        return len(self.table)
    def columnCount(self, parent):
        return len(self.table[0])
    def flags(self, index):
        return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            return self.table[index.row()][index.column()]
    def setData(self, index, value, role):
        if role == QtCore.Qt.EditRole:
            self.table[index.row()][index.column()] = value
        return True

class Main(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        # set combo box choices:
        choices = ['apple', 'orange', 'banana']
        # create table data:
        table   = []
        table.append(['A', choices[0]])
        table.append(['B', choices[0]])
        table.append(['C', choices[0]])
        table.append(['D', choices[0]])
        # create table view:
        self.model     = Model(table)
        self.tableView = QtWidgets.QTableView()
        self.tableView.setModel(self.model)
        self.tableView.setItemDelegateForColumn(1, Delegate(self,choices))
        # make combo boxes editable with a single-click:
        for row in range( len(table) ):
            self.tableView.openPersistentEditor(self.model.index(row, 1))
        # initialize
        self.setCentralWidget(self.tableView)
        self.setWindowTitle('Delegate Test')
        self.show()

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    main = Main()
    app.exec_()