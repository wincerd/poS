import MySQLdb
from datetime import datetime,date,timedelta


try:
    from .dbconnect import connection 
    c,conn = connection()    
except:
    from .dbconnect import connect
    c,conn = connect()
    c.execute('''
        CREATE DATABASE  IF NOT EXISTS pos;
    ''')

class Journal():
    ACCOUNT_TYPES = ('asset', 'liability', 'equity', 'revenue', 'expense')
    def __init__(self):
        '''Initialize the database.'''
        try: 
            c.execute('''
        SELECT  * from users;''')
        except:
            c.execute('''
            CREATE DATABASE  IF NOT EXISTS pos;
            USE pos;
            CREATE TABLE IF NOT EXISTS `Account` (
            `ID` int NOT NULL AUTO_INCREMENT,
            `name` text,
            `typ` varchar(20) NOT NULL,
            PRIMARY KEY (ID)
            ) ENGINE=InnoDB DEFAULT CHARSET=latin1;
            CREATE TABLE IF NOT EXISTS `contact` (
            `c_id` int NOT NULL AUTO_INCREMENT,
            `name` varchar(100) DEFAULT NULL,
            `mobile` int(11) DEFAULT NULL,
            `type` varchar(20) NOT NULL,
            PRIMARY KEY (c_id)
            ) ENGINE=InnoDB DEFAULT CHARSET=latin1;
            CREATE TABLE IF NOT EXISTS `journal` (
            `ID` int NOT NULL AUTO_INCREMENT,
            `dat` varchar(50) DEFAULT NULL,
            `debit` varchar(11) NOT NULL,
            `credit` varchar(11) NOT NULL,
            `amount` int(11) NOT NULL,
            PRIMARY KEY (ID)
            ) ENGINE=InnoDB DEFAULT CHARSET=latin1;
    CREATE TABLE IF NOT EXISTS `Posting` (
            `ID` int NOT NULL AUTO_INCREMENT,
            `account_id` text,
            `journal_id` text,
            `amount` int(11) DEFAULT NULL,
            PRIMARY KEY (ID)
            ) ENGINE=InnoDB DEFAULT CHARSET=latin1;
            CREATE TABLE IF NOT EXISTS `products` (
            `name` varchar(50) NOT NULL,
            `product_num` int NOT NULL AUTO_INCREMENT,
            `category` varchar(50) NOT NULL,
            `description` varchar(50) NOT NULL,
            `cog` int(6) NOT NULL,
            `price` int(6) NOT NULL,
            `account` varchar(50) NOT NULL,
            PRIMARY KEY (product_num)
            ) ENGINE=InnoDB DEFAULT CHARSET=latin1;
            CREATE TABLE IF NOT EXISTS `sale` (
            `ID` int NOT NULL AUTO_INCREMENT,
            `item` varchar(50) NOT NULL,
            `data` varchar(50) NOT NULL,
            `description` varchar(50) NOT NULL,
            `size` int(6) NOT NULL,
            `Date` int(50) NOT NULL,
            PRIMARY KEY (ID),
            `amount` int(6) NOT NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=latin1;
            CREATE TABLE IF NOT EXISTS `users` (
            `username` varchar(100) NOT NULL,
            `userpass` varchar(100) NOT NULL,
            `email` varchar(100) NOT NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=latin1;
            ''')
    def init_acc(self):
        '''make default accounts'''
        accounts = [(1, "sale","asset" ),(2, "inventory","asset" ),(3, "wages","expense" ),(4, "cash","asset" ),(5, "utilities","expense" ),(6, "rent","expense" )]
        for account in accounts:
            self.create_account(account[0],account[1],account[2])
    def drop(self):
        '''Reset the ledger.'''
        self.db.executescript('''
        DROP TABLE IF EXISTS users;
        DROP TABLE IF EXISTS sale;
        DROP TABLE IF EXISTS Posting;
        DROP TABLE IF EXISTS products;
        DROP TABLE IF EXISTS journal;
        DROP TABLE IF EXISTS contacts;
        
        ''')
        self.db.commit()
    def record_transaction(self, accounts,amount):
        c,conn  = connection()
        self.accounts = accounts
        self.amount = amount
        #select individual  accounts from posted data
        dr = self.accounts[0]
        cr = self.accounts[1]
        #check if  accounts exists
        for account in self.accounts:
            c.execute("""select * from Account where name =%s""", (account,))
            b = c.fetchall()
        if b == ():
            print("failed")
        else:
            dat =(self.Date()).strftime("%Y%m%d")
            c.execute("select ID from journal where ID =( SELECT MAX(ID) FROM journal)")
            ID= c.fetchone()
            if ID == None:
                ID = 1
            c.execute("""INSERT INTO journal(dat,debit,credit,amount)
                VALUES (%s,%s,%s,%s)""",(dat,dr,cr,self.amount,))
            for account in self.accounts:
                c.execute("select ID from Posting where ID =( SELECT MAX(ID) FROM Posting)")
                jID= c.fetchone()
                if jID == None:
                    jID = 1
                else:
                    for ID in jID:
                        jID = int(ID)+ 1
                c.execute('''INSERT INTO Posting (ID,journal_id,account_id,amount)
                    VALUES (%s,%s,%s,%s)''',(jID,ID,account,amount,))
            conn.commit()
            conn.close()
    def create_account(self, ID , name, Type):
        '''Create an account with a given code and name.'''
        c,conn  = connection()
        if Type not     in self.ACCOUNT_TYPES:
            raise ValueError('unknown account type {}'.format(Type))
        if self.get_account(name):
            raise LedgerError('The account "{}" already exists'.format(name))
        c.execute("""INSERT INTO Account(ID, name, typ)
                VALUES (%s,%s, %s)""", (ID, name, Type,))
        conn.commit()        
    def get_balance_sheet(self):
        '''Return a balance sheet.'''
        c,conn  = connection()
        assets = self.acc("asset")
        liability =self.acc("liability")
        equity = self.acc('equity')
        revenue= self.acc('revenue')
        expense= self.acc('expense')
        return (assets, liability, equity, revenue, expense)
##    def balance_sheet_total(self):
##        total = self.get_balance_sheet()
##        ttl =[]
##        for records in total:
##            for account in records:
##		ttl.append(records[account])
##	
        
    def acc(self,Type):
        ''' Return the balance of accounts by types '''
        c,conn  = connection()
        c.execute("""select name from Account where typ =%s""", (Type,))
        acnt = c.fetchall()
        data = {}
        for name in acnt:
            name =str(name).replace("('","").replace("',)","")
            balance = self.get_account_balance(name)
            data[name]=balance
        return data
    def Date(self):
        #get the date today as a string
        date =datetime.now()
        return date 
    def month(self,month= "today"):
        if month == "today":
            month =int((self.Date()).strftime("%m"))
            print(month)
        else:
            month= month
            print(type(month))
        year =int((self.Date()).strftime("%Y"))
        day = timedelta(days=1)
        month =int(month)
        date1 = date(year, month, 1)
        dates = []
        number =[]
        d = date1
        while d.month == month:
            dates.append(d)
            d += day
            number.append((d).strftime("%d"))
        return dates,number
    def week(self):
         day = self.Date()
         week= ([day + timedelta(days=i) for i in range(0 - day.weekday(), 7 - day.weekday())])
         return week
    def year(self):
        pass
        

    def get_income_statement(self, start_date=0, end_date=0):
        '''Return an income statement.'''
        """Sales (revenue)– cost of goods sold – selling, general, administrative expenses (SGA)– depreciation/ amortization= earnings before interest and taxes (EBIT)
        – interest and tax expenses= profit/loss"""
        #get the total sale for the period
        c,conn  = connection()
        if start_date ==0 :
            c.execute("select dat from journal where ID =( SELECT MIN(ID) FROM journal)")
            start_date= c.fetchone()
        if end_date ==0 :
            end_date =(self.Date()).strftime("%Y%m%d")
        sale= self.get_account_balance("sale",start_date, end_date)
        #get the total of goods sold
        c.execute("""select cog from sale  where Date >= %s and Date < %s""", (start_date,end_date,))
        cog = c.fetchall()
        cog_total = []
        for  i in cog:
            for x in i:
                cog_total.append(x)
        #remove none from list
        cog_total = [0 if v is None else v for v in cog_total]
        cog = sum(cog_total)                        
        #get the total for expense
        total_expense=self.acc("expense")
        #get the total for all expense accounts
        total_expense = sum(total_expense.values())
        #get the statment value
        statment = sale-(cog+total_expense)
        return (sale,cog,total_expense,statment)
    def get_account(self, name):
        '''Return the account identified by the specified name.'''
        c,conn  = connection()
        c.execute("""select * from Account where name =%s""", (name,))
        row=c.fetchone()
        if row is None:
            return None
        return Account(row[0], row[1], row[2])
    def get_account_balance(self,name,start_date= 0,end_date= 0):
        c,conn  = connection()
        if start_date ==0 :
            c.execute("select dat from journal where ID =( SELECT MIN(ID) FROM journal)")
            start_date= c.fetchone()
        if end_date ==0 :
            end_date =(self.Date()).strftime("%Y%m%d")
        a=c.execute("""select amount from journal  where dat >= %s and dat <= %s and debit = %s """, (start_date,end_date,name,))
        debit_total =c.fetchall()
        total = []
        for  i in debit_total:
            for x in i:
                total.append(x)
        debit_total =(sum(total))
        
        c.execute("""select amount  from journal where dat >= %s and dat <= %s and credit = %s """, (start_date,end_date,name,))
        credit_total = c.fetchall()
        total = []
        for  i in credit_total:
            for x in i:
                total.append(x)
        credit_total =(sum(total))
        total = debit_total-credit_total
        return(total)
    def get_lastproductid(self, name):
        c,conn  = connection()
        c.execute("select * from products where product_num=( SELECT MAX(product_num) FROM products)")
        row=c.fetchone()
        if row is None:
            return None
        else:
            return row

