import sqlite3
class database():    
    def connect(self):
        try:
            sqliteConnection = sqlite3.connect('POS.db', timeout=20)
            self.cursor = sqliteConnection.cursor()
            print("Connected to SQLite")
        except sqlite3.Error as error:
            print("Failed to read data from sqlite table", error)
       
        return (self.cursor,sqliteConnection)
    def customers(self):
        sqlite_select_query = """SELECT customer_name,customer_number,customer_balance  from customers"""
        self.cursor.execute(sqlite_select_query)
        customers = self.cursor.fetchall()
        return customers
    def customer(self,name):
        ## use variable name
        sqlite_select_query = """SELECT id,customer_name,customer_number,customer_balance  from customers"""
        self.cursor.execute(sqlite_select_query)
        customer = self.cursor.fetchone()
        return customer
    def items(self):
        sqlite_select_query = """SELECT item_name,item_description,item_cost,item_price,item_number  from items"""
        self.cursor.execute(sqlite_select_query)
        items = self.cursor.fetchall()
        return items
    def item_list(self):
        sqlite_select_query = """SELECT item_name  from items"""
        self.cursor.execute(sqlite_select_query)
        items = self.cursor.fetchall()
        return items
        
    def items_name(self,name):
        ## use variable name
  
        sqlite_select_query = "SELECT item_name,item_description,item_cost,item_price,item_number  from items where items =(?)",((name,))
        self.cursor.execute(sqlite_select_query)
        items = self.cursor.fetchone()
        return items
    def sales(self):
        sqlite_select_query = """SELECT item_name,item_description,item_cost,item_price,item_number  from items"""
        self.cursor.execute(sqlite_select_query)
        items = self.cursor.fetchone()
        return items
    
    def main(self):
        self.connect()
if __name__=="__main__":
    new= database()
    new.main()
        


