from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from  PyQt5 import QtGui,QtCore
import random

def setup_consonants_vowels():
    letters = 'abcdefghijklmnopqrstuvwxyz'
    vowels = set(['a','e','i','o','u','A','E','I','O','U'])
    consonants = set([c for c in (letters + letters.upper()) if not c in vowels])
    return (consonants, vowels)

def count(text, letterset):
    n = 0
    for c in text:
        if c in letterset:
            n += 1
    return n 

class CompleterDelegate(QStyledItemDelegate):
    def __init__(self, parent=None, completerSetupFunction=None):
        super(CompleterDelegate, self).__init__(parent)
        self._completerSetupFunction = completerSetupFunction
    def createEditor(self, parent, option, index):
        print( "createEditor")
        editor = QLineEdit(parent)
        self._completerSetupFunction(editor, index)
        return editor
    def setEditorData(self, editor, index):
        print( "setEditorData")
        super(CompleterDelegate, self).setEditorData(editor, index)
    def closeEditor(self, editor, hint=None):
        print( "closeEditor")
        super(CompleterDelegate, self).closeEditor(editor, hint)
    def commitData(self, editor):
        print( "commitData")
        super(CompleterDelegate, self).commitData(editor)

class MainWindow(QWidget):
    def __init__(self, table_model, _completerSetupFunction=None, *args):
        QWidget.__init__(self, *args)
        # setGeometry(x_pos, y_pos, width, height)
        self.setGeometry(300, 200, 570, 450)
        self.setWindowTitle("QTableView + completer example")
        table_view = QTableView()
        table_view.setModel(table_model)
        # set column width to fit contents (set font first!)
        table_view.resizeColumnsToContents()
        table_view.resizeRowsToContents()
        
        if _completerSetupFunction is not None:
            delegate = CompleterDelegate(table_view, _completerSetupFunction)
            table_view.setItemDelegateForColumn(1, delegate)            

        layout = QVBoxLayout(self)
        layout.addWidget(table_view)
        self.setLayout(layout)
        
class ItemTableModel(QAbstractTableModel):
    def __init__(self, items, *args, **kwargs):
        super(ItemTableModel, self).__init__()
        self.items = items[:]
        self.header = ['#','Length','Letters','Consonants','Vowels']
        self.cset, self.vset = setup_consonants_vowels()
    def rowCount(self, parent):
        return len(self.items)
    def columnCount(self, parent):
        return len(self.header)
    def data(self, index, role):
        if not index.isValid():
            return None
        if role == Qt.DisplayRole:
            return self.getDisplayData(index)
        elif role == Qt.EditRole:
            return self.getDisplayData(index)
        else:
            return None
    def flags(self, index):
        if not index.isValid():
            return Qt.ItemIsEnabled
        sresult = super(ItemTableModel,self).flags(index)
        result = sresult | Qt.ItemIsEnabled | Qt.ItemIsSelectable
        if index.column() == 1:
            result = result | Qt.ItemIsEditable
        return Qt.ItemFlags(result)
    def setData(self, index, value, role=Qt.EditRole):
        try:
            self.items[index.row()] = value 
            left = self.createIndex(index.row(), 0)
            right = self.createIndex(index.row(), self.columnCount())
            self.dataChanged.emit(left, right)
            return True
        except:
            pass
        return False             
    def getDisplayData(self, index):
        item = self.items[index.row()]
        col = index.column()
        if col == 0:
            return index.row()+1
        elif col == 1:
            return item
        elif col == 2:
            return len(item)
        elif col == 3:
            return count(item, self.cset)
        elif col == 4:
            return count(item, self.vset)
    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.header[col]
        return None

if __name__ == '__main__':   
    base_items = '''
    Hydrogen
    Helium
    Lithium
    Beryllium
    Boron
    Carbon
    Nitrogen
    Oxygen
    Fluorine
    Neon
    Sodium
    Magnesium
    Aluminum
    Silicon
    Phosphorus
    Sulfur
    Chlorine
    Argon
    Potassium
    Calcium
    Scandium
    Titanium
    Vanadium
    Chromium
    Manganese
    Iron
    Cobalt
    Nickel
    Copper
    Zinc
    Gallium
    Germanium
    Arsenic
    Selenium
    Bromine
    Krypton
    '''.split()
    app = QApplication([])
    
    if False:
        deffact = QItemEditorFactory.defaultFactory()
        print( "default delegate factory = %s" % deffact)
        edt = deffact.createEditor(str,None)
        print( "editor: %s" % edt )
    
    def _completerSetupFunction(editor, index):
        print(editor)
        print( "completer setup: editor=%s, index=%s" % (editor, index))
        completer = QCompleter(base_items, editor)
        completer.setCompletionColumn(0)
        completer.setCompletionRole(QtCore.Qt.EditRole)
        completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        try:    
            editor.setCompleter(completer)
        except:
            pass

    table_model = ItemTableModel(base_items)
    win = MainWindow(table_model, _completerSetupFunction)
    win.show()
    app.exec_()
