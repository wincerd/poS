from PyQt5 import QtGui,QtCore, QtWidgets, QtPrintSupport
from PyQt5.QtCore import QSize

app = QtWidgets.QApplication([])

window = QtWidgets.QWidget()
##window.setFixedSize(QSize(200,500))
editor = QtWidgets.QTextEdit(window)
editor.setFixedSize(QSize(200,500))
##lst = QtWidgets.QListWidget(window)
##lst.addItems(['Winnie Puh', 'Monday', 'Minnesota', 'Dracula Calsta Flockhart Meningitis', 'Once', '123345', 'Fin'])
##lst.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
##lst.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
##lst.setFixedSize(lst.sizeHintForColumn(0) + 2 * lst.frameWidth(), lst.sizeHintForRow(0) * lst.count() + 2 * lst.frameWidth())
##item =  QtWidgets.QListWidgetItem(lst)
class prin (object):
  """docstring for prin """
  def __init__(self):
    pass
  def 
    
    
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
editor.append(header)
editor.append(content)
editor.append(math)
editor.append(footer)
##lst.setItemWidget(item,editor)
##list_widget.setItemWidget(item, widget)

window.show()

app.exec_()
