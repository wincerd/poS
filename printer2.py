
class tryout():
    def printViaHtml(self):
        html = u""
        for statement in self.statements:
            date = QDate.currentDate().toString(DATE_FORMAT)
            address = Qt.escape(statement.address).replace(",", "<br>")
            contact = Qt.escape(statement.contact)
            balance = statement.balance()
            html += ("<p align=right><img src=':/logo.png'></p>"
                     "<p align=right>Greasy Hands Ltd."
                     "<br>New Lombard Street"
                     "<br>London<br>WC13 4PX<br>%s</p>"
                     "<p>%s</p><p>Dear %s,</p>" "<p>The balance of your account is %s.") % ( date, address, contact,QString("$ %L1").arg(float(balance), 0, "f", 2))
            if balance < 0:
                html += (" <p><font color=red><b>Please remit the " "amount owing immediately.</b></font>")
            else:
                html += (" We are delighted to have done business " "with you.")
                html += ("</p><p>&nbsp;</p><p>"
##         for date, amount in statement.transactions:
##           color, status = "black", "Credit"
##           if amount < 0:
##                color, status = "red", "Debit"
##                html += ("<tr><td align=right>%s</td>" "<td>%s</td><td align=right>" "<font color=%s>%s</font></td></tr>" % ( date.toString(DATE_FORMAT), status, color, QString("$ %L1").arg(
##                                                                                     "<table border=1 cellpadding=2 " "cellspacing=2><tr><td colspan=3>" "Transactions</td></tr>")float(abs(amount)), 0, "f", 2)))
##                html += ("</table></p><p style='page-break-after=always;'>" "We hope to continue doing " "business with you,<br>Yours sincerely," "<br><br>K.&nbsp;Longrey, Manager</p>")
    def statements(self):
        address = "12,345,678"
        contact = "me"
        balance = 123456
        transactions = []
    

dialog = QPrintDialog(self.printer, self) if dialog.exec_():

document = QTextDocument()

document.setHtml(html)

document.print_(self.printer)

