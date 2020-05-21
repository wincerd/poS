import sqlite3
from datetime import datetime
class database():    
    def __init__(self):
        try:
            self.conn= sqlite3.connect('POS.db', timeout=20)
            self.c = self.conn.cursor()
            print("Connected to SQLite")
        except sqlite3.Error as error:
            print("Failed to read data from sqlite table", error)
       
        
    def customers(self):
        sqlite_select_query = """SELECT name,mobile,balance  from contact"""
        self.c.execute(sqlite_select_query)
        customers = self.c.fetchall()
        return customers
    def customer(self,name):
        ## use variable name
        sqlite_select_query = """SELECT c_id,name,mobile,balance  from contact"""
        self.c.execute(sqlite_select_query)
        customer = self.c.fetchone()
        return customer
    def items(self):
        sqlite_select_query = """SELECT name,description,cog,price ,product_num  from products"""
        self.c.execute(sqlite_select_query)
        items = self.c.fetchall()
        return items
    def item_list(self):
        sqlite_select_query = """SELECT name  from products"""
        self.c.execute(sqlite_select_query)
        items = self.c.fetchall()
        return items
    def item_details(self):
        sqlite_select_query = """SELECT  * from products"""
        self.c.execute(sqlite_select_query)
        items = self.c.fetchall()
        return items
    def items_name(self,name):
        self.c.execute('SELECT product_num ,name,price  FROM products WHERE name=(?)', (name,))
        items = self.c.fetchall()
        return items
    def sales(self):
        sqlite_select_query = """SELECT name,description,cog,price,product_num  from products"""
        self.c.execute(sqlite_select_query)
        items = self.c.fetchone()
        return items
    def product_num(self):
        self.c.execute("select product_num from products where product_num=(SELECT MAX(product_num) FROM products)")
        data = self.parse_none(self.c.fetchone())
        return data
        
    def save_item(self,name,description,cog,price):
        product_num = self.product_num() + 1
        self.c.execute("""INSERT INTO products (name,description,cog,price,product_num) VALUES (?, ?, ?, ?, ?)""",
                          (name,description,cog,price,product_num))
        self.conn.commit()
        return {"success","true"}
    def save_contact(self,name,mobile,balance,typ):
        self.c.execute("""INSERT INTO contact (name,mobile,balance,Typ) VALUES (?, ?, ?, ?)""",
                          (name,mobile,balance,typ))
        self.conn.commit()
        return {"success","true"}
        
        
    def make_sale(self,data):
        dat = datetime.now()
        for i in data:
            i.append(dat)
            self.c.execute("""INSERT INTO sale (product_num,name,description,quantity,amount,Dat) VALUES (?, ?, ?, ?, ?,?)""",
                          i)
        self.conn.commit()
        return {"success","true"}

    def parse_none(self,data):
        if data == None:
            data = 1
        else:
            data = int(data[0]) 
        return data
    def main(self):
        self.connect()


