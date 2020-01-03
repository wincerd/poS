#!/usr/bin/python3
#-*- coding:utf-8 -*-
import csv, codecs 
import os

from PyQt5 import QtCore, QtGui, QtWidgets, QtPrintSupport
from PyQt5.QtGui import QImage, QPainter,QStandardItemModel
from PyQt5.QtCore import QFile

class MyWindow(QtWidgets.QWidget):
    def __init__(self, aPath, parent=None):
        super(MyWindow, self).__init__(parent)
        self.isChanged = False
        self.fileName = ""
        self.fname = "Liste"
        self.model =  QtGui.QStandardItemModel(self)

        self.tableView = QtWidgets.QTableView(self)
        self.tableView.setStyleSheet(stylesheet(self))
        self.tableView.setModel(self.model)
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.setShowGrid(True)
        self.tableView.setGeometry(10, 50, 780, 645)
        self.tableView.verticalHeader().setSectionResizeMode(3)
        self.model.dataChanged.connect(self.finishedEdit)

        self.pushButtonLoad = QtWidgets.QPushButton(self)
        self.pushButtonLoad.setText("Load CSV")
        self.pushButtonLoad.clicked.connect(self.loadCsv)
        self.pushButtonLoad.setFixedWidth(60)
        self.pushButtonLoad.setStyleSheet(stylesheet(self))

        self.pushButtonWrite = QtWidgets.QPushButton(self)
        self.pushButtonWrite.setText("Save")
        self.pushButtonWrite.clicked.connect(self.saveOnQuit)
        self.pushButtonWrite.setFixedWidth(60)
        self.pushButtonWrite.setStyleSheet(stylesheet(self))

        self.pushButtonWrite2 = QtWidgets.QPushButton(self)
        self.pushButtonWrite2.setText("Save as ...")
        self.pushButtonWrite2.clicked.connect(self.writeCsv)
        self.pushButtonWrite2.setFixedWidth(60)
        self.pushButtonWrite2.setStyleSheet(stylesheet(self))

        self.pushButtonPreview = QtWidgets.QPushButton(self)
        self.pushButtonPreview.setText("Print Preview")
        self.pushButtonPreview.clicked.connect(self.handlePreview)
        self.pushButtonPreview.setFixedWidth(80)
        self.pushButtonPreview.setStyleSheet(stylesheet(self))

        self.pushButtonPrint = QtWidgets.QPushButton(self)
        self.pushButtonPrint.setText("Print")
        self.pushButtonPrint.clicked.connect(self.handlePrint)
        self.pushButtonPrint.setFixedWidth(60)
        self.pushButtonPrint.setStyleSheet(stylesheet(self))

        self.pushAddRow = QtWidgets.QPushButton(self)
        self.pushAddRow.setText("add Row")
        self.pushAddRow.clicked.connect(self.addRow)
        self.pushAddRow.setFixedWidth(60)
        self.pushAddRow.setStyleSheet(stylesheet(self))

        self.pushDeleteRow = QtWidgets.QPushButton(self)
        self.pushDeleteRow.setText("delete Row")
        self.pushDeleteRow.clicked.connect(self.removeRow)
        self.pushDeleteRow.setFixedWidth(70)
        self.pushDeleteRow.setStyleSheet(stylesheet(self))

        self.pushAddColumn = QtWidgets.QPushButton(self)
        self.pushAddColumn.setText("add Column")
        self.pushAddColumn.clicked.connect(self.addColumn)
        self.pushAddColumn.setFixedWidth(80)
        self.pushAddColumn.setStyleSheet(stylesheet(self))

        self.pushDeleteColumn = QtWidgets.QPushButton(self)
        self.pushDeleteColumn.setText("delete Column")
        self.pushDeleteColumn.clicked.connect(self.removeColumn)
        self.pushDeleteColumn.setFixedWidth(86)
        self.pushDeleteColumn.setStyleSheet(stylesheet(self))

        self.pushClear = QtWidgets.QPushButton(self)
        self.pushClear.setText("Clear")
        self.pushClear.clicked.connect(self.clearList)
        self.pushClear.setFixedWidth(60)
        self.pushClear.setStyleSheet(stylesheet(self))

        grid = QtWidgets.QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(self.pushButtonLoad, 0, 0)
        grid.addWidget(self.pushButtonWrite, 0, 1)
        grid.addWidget(self.pushButtonWrite2, 0, 2)
        grid.addWidget(self.pushAddRow, 0, 3)
        grid.addWidget(self.pushDeleteRow, 0, 4)
        grid.addWidget(self.pushAddColumn, 0, 5)
        grid.addWidget(self.pushDeleteColumn, 0, 6)
        grid.addWidget(self.pushClear, 0, 7)
        grid.addWidget(self.pushButtonPreview, 0, 8)
        grid.addWidget(self.pushButtonPrint, 0, 9, 1, 1, QtCore.Qt.AlignRight)
        grid.addWidget(self.tableView, 1, 0, 1, 10)
        self.setLayout(grid)

        item = QtGui.QStandardItem()
        self.model.appendRow(item)
        self.model.setData(self.model.index(0, 0), "", 0)
        self.tableView.resizeColumnsToContents()
        self.isChanged = False

        print("Welcome to CSV Reader")

        if len(sys.argv) > 1:
            print(sys.argv[1])
            self.fileName = sys.argv[1]
            self.loadCsvOnOpen(self.fileName)
            print(self.fileName + "loaded")
        else:
            print("no File")

    def loadCsvOnOpen(self, fileName):
        if fileName:
            print(fileName + " loaded")
            font = QtGui.QFont()
            font.setBold(True)
            ff = open(fileName, 'r')
            mytext = ff.read()
            ff.close()
            f = open(fileName, 'r')
            with f:
                i = int(1)
                self.fileName = fileName
                self.fname = os.path.splitext(str(fileName))[0].split("/")[-1]
                self.setWindowTitle(self.fname)
                if mytext.count(';') <= mytext.count('\t'):
                    reader = csv.reader(f, delimiter = '\t')
                    self.model.clear()
                    for row in reader:    
                        items = [QtGui.QStandardItem(field) for field in row]
                        self.model.appendRow(items)
                        self.model.setHeaderData(i - 1, QtCore.Qt.Horizontal, "Column " + str(i))
                        i = i + 1
                else:
                    reader = csv.reader(f, delimiter = ';')
                    self.model.clear()
                    for row in reader:    
                        items = [QtGui.QStandardItem(field) for field in row]
                        self.model.appendRow(items)
                        self.model.setHeaderData(i - 1, QtCore.Qt.Horizontal, "Column " + str(i))

                        i = i + 1
                self.tableView.selectRow(0)

                self.tableView.resizeColumnsToContents()
                self.isChanged = False

    def loadCsv(self, fileName):
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open CSV",
                (QtCore.QDir.homePath() + "/Dokumente/CSV"), "CSV (*.csv *.tsv *.txt)")
        if fileName:
            self.loadCsvOnOpen(fileName)

    def writeCsv(self):
        # find empty cells
        for row in range(self.model.rowCount()):
            for column in range(self.model.columnCount()):
                myitem = self.model.item(row,column)
                if myitem is None:
                    item = QtGui.QStandardItem("")
                    self.model.setItem(row, column, item)
        fileName, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save File", 
                        (QtCore.QDir.homePath() + "/Dokumente/CSV/" + self.fname + ".csv"),"CSV Files (*.csv)")
        if fileName:
            print(fileName)
            f = open(fileName, 'w')
            with f:
                writer = csv.writer(f, delimiter = '\t')
                for rowNumber in range(self.model.rowCount()):
                    fields = [self.model.data(self.model.index(rowNumber, columnNumber),
                                        QtCore.Qt.DisplayRole)
                    for columnNumber in range(self.model.columnCount())]
                    writer.writerow(fields)
                self.fname = os.path.splitext(str(fileName))[0].split("/")[-1]
                self.setWindowTitle(self.fname)
                self.isChanged = False

    def handlePrint(self):
        if self.model.rowCount() == 0:
            print("no rows")
        else:
            dialog = QtPrintSupport.QPrintDialog()
            if dialog.exec_() == QtWidgets.QDialog.Accepted:
                self.handlePaintRequest(dialog.printer())
                print("Document printed")

    def handlePreview(self):
        if self.model.rowCount() == 0:
            print("no rows")
        else:
            dialog = QtPrintSupport.QPrintPreviewDialog()
            dialog.setFixedSize(1000,700)
            dialog.paintRequested.connect(self.handlePaintRequest)
            dialog.exec_()
            print("Print Preview closed")

    def handlePaintRequest(self, printer):
        # find empty cells
        for row in range(self.model.rowCount()):
            for column in range(self.model.columnCount()):
                myitem = self.model.item(row,column)
                if myitem is None:
                    item = QtGui.QStandardItem("")
                    self.model.setItem(row, column, item)
        printer.setDocName(self.fname)
        document = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(document)
        model = self.tableView.model()
        tableFormat = QtGui.QTextTableFormat()
        tableFormat.setBorder(0.2)
        tableFormat.setBorderStyle(3)
        tableFormat.setCellSpacing(0);
        tableFormat.setTopMargin(0);
        tableFormat.setCellPadding(4)
        table = cursor.insertTable(model.rowCount(), model.columnCount(), tableFormat)
        print(self.model.horizontalHeaderItem(0).text())
        for row in range(table.rows()):
            for column in range(table.columns()):
                cursor.insertText(model.item(row, column).text())
                cursor.movePosition(QtGui.QTextCursor.NextCell)
        document.print_(printer)

    def removeRow(self):
        model = self.model
        indices = self.tableView.selectionModel().selectedRows() 
        for index in sorted(indices):
            model.removeRow(index.row())
            self.isChanged = True

    def addRow(self):
        item = QtGui.QStandardItem("")
        self.model.appendRow(item)
        self.isChanged = True

    def clearList(self):
        self.model.clear()
        self.isChanged = True

    def removeColumn(self):
        model = self.model
        indices = self.tableView.selectionModel().selectedColumns() 
        for index in sorted(indices):
            model.removeColumn(index.column())
            self.isChanged = True

    def addColumn(self):
        count = self.model.columnCount()
        print (count)
        self.model.setColumnCount(count + 1)
        self.model.setData(self.model.index(0, count), "", 0)
        self.tableView.resizeColumnsToContents()
        self.isChanged = True

    def finishedEdit(self):
        self.tableView.resizeColumnsToContents()
        self.isChanged = True

    def contextMenuEvent(self, event):
        self.menu = QtWidgets.QMenu(self)
        # copy
        copyAction = QtWidgets.QAction('Copy', self)
        copyAction.triggered.connect(lambda: self.copyByContext(event))
        # paste
        pasteAction = QtWidgets.QAction('Paste', self)
        pasteAction.triggered.connect(lambda: self.pasteByContext(event))
        # cut
        cutAction = QtWidgets.QAction('Cut', self)
        cutAction.triggered.connect(lambda: self.cutByContext(event))
        # delete selected Row
        removeAction = QtWidgets.QAction('delete Row', self)
        removeAction.triggered.connect(lambda: self.deleteRowByContext(event))
        # add Row after
        addAction = QtWidgets.QAction('insert new Row after', self)
        addAction.triggered.connect(lambda: self.addRowByContext(event))
        # add Row before
        addAction2 = QtWidgets.QAction('insert new Row before', self)
        addAction2.triggered.connect(lambda: self.addRowByContext2(event))
        # add Column before
        addColumnBeforeAction = QtWidgets.QAction('insert new Column before', self)
        addColumnBeforeAction.triggered.connect(lambda: self.addColumnBeforeByContext(event))
        # add Column after
        addColumnAfterAction = QtWidgets.QAction('insert new Column after', self)
        addColumnAfterAction.triggered.connect(lambda: self.addColumnAfterByContext(event))
        # delete Column
        deleteColumnAction = QtWidgets.QAction('delete Column', self)
        deleteColumnAction.triggered.connect(lambda: self.deleteColumnByContext(event))
        # add other required actions
        self.menu.addAction(copyAction)
        self.menu.addAction(pasteAction)
        self.menu.addAction(cutAction)
        self.menu.addSeparator()
        self.menu.addAction(addAction)
        self.menu.addAction(addAction2)
        self.menu.addSeparator()
        self.menu.addAction(addColumnBeforeAction)
        self.menu.addAction(addColumnAfterAction)
        self.menu.addSeparator()
        self.menu.addAction(removeAction)
        self.menu.addAction(deleteColumnAction)
        self.menu.popup(QtGui.QCursor.pos())

    def deleteRowByContext(self, event):
        for i in self.tableView.selectionModel().selection().indexes():
            row = i.row()
            self.model.removeRow(row)
            print("Row " + str(row) + " deleted")
            self.tableView.selectRow(row)
            self.isChanged = True

    def addRowByContext(self, event):
        for i in self.tableView.selectionModel().selection().indexes():
            row = i.row() + 1
            self.model.insertRow(row)
            print("Row at " + str(row) + " inserted")
            self.tableView.selectRow(row)
            self.isChanged = True

    def addRowByContext2(self, event):
        for i in self.tableView.selectionModel().selection().indexes():
            row = i.row()
            self.model.insertRow(row)
            print("Row at " + str(row) + " inserted")
            self.tableView.selectRow(row)
            self.isChanged = True

    def addColumnBeforeByContext(self, event):
        for i in self.tableView.selectionModel().selection().indexes():
            col = i.column()
            self.model.insertColumn(col)
            print("Column at " + str(col) + " inserted")
            self.isChanged = True

    def addColumnAfterByContext(self, event):
        for i in self.tableView.selectionModel().selection().indexes():
            col = i.column() + 1
            self.model.insertColumn(col)
            print("Column at " + str(col) + " inserted")
            self.isChanged = True

    def deleteColumnByContext(self, event):
        for i in self.tableView.selectionModel().selection().indexes():
            col = i.column()
            self.model.removeColumn(col)
            print("Column at " + str(col) + " removed")
            self.isChanged = True

    def copyByContext(self, event):
        for i in self.tableView.selectionModel().selection().indexes():
            row = i.row()
            col = i.column()
            myitem = self.model.item(row,col)
            if myitem is not None:
                clip = QtWidgets.QApplication.clipboard()
                clip.setText(myitem.text())

    def pasteByContext(self, event):
        for i in self.tableView.selectionModel().selection().indexes():
            row = i.row()
            col = i.column()
            myitem = self.model.item(row,col)
            clip = QtWidgets.QApplication.clipboard()
            myitem.setText(clip.text())
            self.isChanged = True

    def cutByContext(self, event):
        for i in self.tableView.selectionModel().selection().indexes():
            row = i.row()
            col = i.column()
            myitem = self.model.item(row,col)
            if myitem is not None:
                clip = QtWidgets.QApplication.clipboard()
                clip.setText(myitem.text())
                myitem.setText("")
                self.isChanged = True

    def closeEvent(self, event):
        if self.isChanged == True:
            quit_msg = "Do you want to save changes?"
            reply = QtWidgets.QMessageBox.question(self, 'Message', 
                     quit_msg, QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
            if reply == QtWidgets.QMessageBox.Yes:
                event.accept()
                self.saveOnQuit()
                app.quit()
            else:
                app.quit()
        else:
            app.quit()
        print("Goodbye ...")

    def saveOnQuit(self):
        if self.fileName == "":
            self.writeCsv()
        else:
            # find empty cells
            for row in range(self.model.rowCount()):
                for column in range(self.model.columnCount()):
                    myitem = self.model.item(row,column)
                    if myitem is None:
                        item = QtGui.QStandardItem("")
                        self.model.setItem(row, column, item)
            if self.fileName:
                print(self.fileName)
                f = open(self.fileName, 'w')
                with f:
                    writer = csv.writer(f, delimiter = '\t')
                    for rowNumber in range(self.model.rowCount()):
                        fields = [self.model.data(self.model.index(rowNumber, columnNumber),
                                            QtCore.Qt.DisplayRole)
                        for columnNumber in range(self.model.columnCount())]
                        writer.writerow(fields)
                    self.isChanged = False

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


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName('MyWindow')
    main = MyWindow('')
    main.setMinimumSize(820, 300)
    main.setGeometry(0,0,820,700)
    main.setWindowTitle("CSV Viewer")
    main.show()

sys.exit(app.exec_())
