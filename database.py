import sqlite3

class Database:
    
    # Initalizing the database for the website.
    def __init__(self, dbname) -> None:

        try:
            self.dbname = 'Database/' + dbname + '.db'

            self.table()
            
            with sqlite3.connect(self.dbname) as conn:
                cursor = conn.cursor()
                
                # Execute the query to get table names
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                
                # Fetch all the table names
                tables = cursor.fetchall()
            
                # Extract table names from the result
                self.tableNames = [i[0] for i in tables]
        except sqlite3.Error as e:
            print("Error:", e)

    def table(self) -> None:
        try:
            with sqlite3.connect(self.dbname) as conn:
                cursor = conn.cursor()
                
                # A table for the user credentials.
                cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    email TEXT NOT NULL,
                    username TEXT NOT NULL,
                    password TEXT NOT NULL,
                    location TEXT NOT NULL)''')
                
                # A table for saving the contact details.
                cursor.execute('''CREATE TABLE IF NOT EXISTS contact (
                    id INTEGER PRIMARY KEY, 
                    username TEXT NOT NULL, 
                    email TEXT NOT NULL,
                    mobile NUMBER NOT NULL,
                    subject TEXT NOT NULL,
                    message TEXT NOT NULL)''')
                
                # For storing all the orders that are placed.
                cursor.execute('''CREATE TABLE IF NOT EXISTS orders (
                                id INTEGER PRIMARY KEY,
                                product_name TEXT NOT NULL,
                                quantity NUMBER NOT NULL,
                                price NUMBER NOT NULL,
                                customer_id NUMBER NOT NULL,
                                name TEXT NOT NULL,
                                location TEXT NOT NULL,
                                cardNo NUMBER NOT NULL,
                                CVV NUMBER NOT NULL,
                                orderDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL)'''
                            )
                
        except sqlite3.Error as e:
            print("Error:", e)

    # Inserting the data into the database.
    def insert(self, tableName, data):
        try:
            with sqlite3.connect(self.dbname) as conn:
                cursor = conn.cursor()
                if tableName in self.tableNames:

                    # creating a new user account into the database.
                    if tableName == 'users':
                        cursor.execute(f'''INSERT INTO {tableName} (username, password, email, location) 
                                        VALUES (?, ?, ?, ?)''', (data))
                        
                    # storing the feeback of the users.
                    elif tableName == 'contact':
                        cursor.execute(f'''INSERT INTO {tableName} (username, email, mobile, subject, message)
                                       VALUES (?, ?, ?, ?, ?)''', (data))
                    
                    # placing the orders of the user.
                    elif tableName == 'orders':
                        cursor.execute(f'''INSERT INTO {tableName} (product_name, quantity, price, customer_id, name, location, cardNo, CVV)
                                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', (data))
                else:
                    print("Error: Verify the table name")
        except sqlite3.Error as e:
            print("Error:", e)

    # Displaying the contents of the table.
    def display(self, table_name):
        try:
            if table_name in self.tableNames:
                with sqlite3.connect(self.dbname) as conn:
                    cursor = conn.cursor()

                    # Execute the query to select all rows from the table
                    cursor.execute(f"SELECT * FROM {table_name};")
                    # Fetch all the rows
                    rows = cursor.fetchall()
                    
                    # Print column names
                    column_names = [description[0] for description in cursor.description]
                    print(column_names)
                    
                    # Print table contents
                    for row in rows:
                        print(row)
            else:
                print("Error: Verify the table name")
        except sqlite3.Error as e:
            print("Error:", e)

    def validate(self, table_name, data):
        try:
            if table_name in self.tableNames:
                if table_name == 'users':
                    
                    with sqlite3.connect(self.dbname) as conn:
                        cursor = conn.cursor()

                        cursor.execute(f"SELECT * FROM {table_name} where (username = ? or email = ?) and password = ?", data)
                        rows = cursor.fetchall()

                        if len(rows) == 0:
                            return False
                        else:
                            return True

        except sqlite3.Error as e:
            print("Error:", e)

    def isExist(self, table_name, data):
        try:
            if table_name in self.tableNames:
                if table_name == 'users':
                    
                    with sqlite3.connect(self.dbname) as conn:
                        cursor = conn.cursor()

                        cursor.execute(f"SELECT * FROM {table_name} where username = ? or email = ?", data)
                        rows = cursor.fetchall()

                        if len(rows) == 0:
                            return False
                        else:
                            return True
        except sqlite3.Error as e:
            print("Error:", e)

    def getId(self, tableName, value):
        try:
            if tableName in self.tableNames:
                with sqlite3.connect(self.dbname) as conn:
                    cursor = conn.cursor()

                    cursor.execute(f"SELECT id FROM {tableName} WHERE username = ? or email = ?", (value, value))
                    rows = cursor.fetchone()
                    if(rows):
                        return rows[0]
                    return "No user exists"
            else:
                print("Verify the table name")
        except sqlite3.Error as e:
            print("Error:", e)
            return -1
        
    

