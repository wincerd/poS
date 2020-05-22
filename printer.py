import sys, os
from PyQt5 import QtGui,QtCore, QtWidgets, QtPrintSupport
from PyQt5.QtGui import QAbstractTextDocumentLayout, \
    QTextDocument, QPalette,QPageSize
from PyQt5.QtCore import QSizeF
class Window(QtWidgets.QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.setWindowTitle('Document Printer')
        self.list = QtWidgets.QListWidget()
        self.editor = QtWidgets.QTextEdit()
        
        self.editor.textChanged.connect(self.handleTextChanged)
##        self.editor.setFixedSize(self.list.sizeHintForColumn(0) + 2 * self.list.frameWidth(), self.list.sizeHintForRow(0) * self.list.count() + 2 *self.list.frameWidth())
        self.buttonOpen = QtWidgets.QPushButton('Open', self)
        self.buttonOpen.clicked.connect(self.handleOpen)
        self.buttonPrint = QtWidgets.QPushButton('Print', self)
        self.buttonPrint.clicked.connect(self.handlePrint)
        self.buttonPreview = QtWidgets.QPushButton('Preview', self)
        self.buttonPreview.clicked.connect(self.handlePreview)
        layout = QtWidgets.QGridLayout(self)
        layout.addWidget(self.editor, 0, 0, 1, 3)
        layout.addWidget(self.buttonOpen, 1, 0)
        layout.addWidget(self.buttonPrint, 1, 1)
        layout.addWidget(self.buttonPreview, 1, 2)
        self.handleTextChanged()
        self.handlecontent()
        self.handlePrint()
    def handlecontent(self):
        space = "&nbsp;"
        header =    '<h3  style="margin-left:1.5em">'+  space * 10 + "W.C wholesalers</h3><h3>" + space * 15  + "Shuja hse</h3><h6> "+ space * 16 +" Helena Road</h6>"
                    
        content =""" <table border="0" style="margin-left:1.5em">
              <tr>
                <th>Item</th>
                <th>description</th>
                <th>Quantity</th>
                <th>cost</th>
              </tr>
              <tr>
                <td>January</td>
                <td>$100</td>
                <td>$100</td>
                <td>$100</td>
              </tr>
              <tr>
                <td>February</td>
                <td>$80</td>
                <td>$80</td>
                <td>$80</td>
              </tr>
            </table> """
        math = "<h3>"+space * 20 +"Total " +space * 15 +  "amount</h3>" + "<h3>"+space * 20 +"Subtotal " +space * 8 +  "amount</h3>" 
        
        footer = "<h4>"+space * 10 +"mobile phone</h4>"
        self.editor.append(header)
        self.editor.append(content)
        self.editor.append(math)
        self.editor.append(footer)

    def handleOpen(self):
        path = QtWidgets.QFileDialog.getOpenFileName(
            self, 'Open file', '',
            'HTML files (*.html);;Text files (*.txt);;Pdf files (*.pdf)')[0]
        if path:
            file = QtCore.QFile(path)
            if file.open(QtCore.QIODevice.ReadOnly):
                stream = QtCore.QTextStream(file)
                text = stream.readAll()
                info = QtCore.QFileInfo(path)
                if info.completeSuffix() == 'html':
                    self.editor.setHtml(text)
                else:
                    self.editor.setPlainText(text)
##                file.close()

    def handlePrint(self):
##        width = 800
##        height = 263.520403
        self.printer = QtPrintSupport.QPrinter()
##        self.printer.setPageSize(QPageSize(QSizeF(width, height), QPageSize.Unit.Point, 'Cheque'))
##        self.printer.setFullPage(True)
        self.printer.NativeFormat
        dialog = QtPrintSupport.QPrintDialog()
        
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            print(self.editor)
            self.editor.print_(self.printer)

    def handlePreview(self):
        dialog = QtPrintSupport.QPrintPreviewDialog(self.printer)
        dialog.paintRequested.connect(self.editor.print_)
        dialog.exec_()

    def handleTextChanged(self):
        enable = not self.editor.document().isEmpty()
        self.buttonPrint.setEnabled(enable)
        self.buttonPreview.setEnabled(enable)
    def onSaveButtonClicked(self):
        reply = QtGui.QMessageBox.question(parent=self, title='Attention',
                                           text='File will be overwritten.\nDo you still want to proceed?',
                                           buttons=QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,
                                           defaultButton=QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            filename = self.inputFileLineEdit.text()
            length = self.lengthSpinBox.value()
            width = self.widthSpinBox.value()
            line_width = self.lineWidthSpinBox.value()
            rounded = self.cornersCheckBox.isChecked()
            corners_radius = self.cornersSpinBox.value()
            x = self.xSpinBox.value()
            y = self.ySpinBox.value()

            print( "Values are: ")
            print( "Filename: %s" % filename)
            print( "Length: %.2f Width: %.2f" % (length, width))
            print( "Line width: %.2f" % line_width)
            if corners_radius:
                print("Corner radius: %.2f" % corners_radius)
            print("x: %.2f y: %.2f" % (x, y))
    def onInputFileButtonClicked(self):
        filename, filter = QtGui.QFileDialog.getOpenFileName(parent=self, caption='Open file', dir='.', filter='Kicad PCB Files (*.txt)')

        if filename:
            self.inputFileLineEdit.setText(filename)


if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.resize(640, 480)
    window.show()
    sys.exit(app.exec_())
