import sqlite3
from hashlib import sha256


"""Commands to open and close the database"""
class Database():
    def open_database(self):
        self.conn = sqlite3.connect("Database.db")
        self.cur = self.conn.cursor()
        
    def close_database(self):
        self.conn.commit()
        self.conn.close()
        
def hash_password(password):
    return sha256(password.encode()).hexdigest()
        
"""Commands to create and manipulate the users table"""
class User(Database):
    def create_table(self):
        self.open_database()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS users (
            UserID INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL)""")
        self.conn.close()
        
    def add_user(self, name, username, password):
        self.open_database()
        try:
            self.cur.execute("INSERT INTO users VALUES (NULL, ?, ?, ?)", (name, username, hash_password(password)))
            success = True
        except sqlite3.IntegrityError:
            success = False
        self.close_database()
        return success
    
    def validate_user(self, username, password):
        self.open_database()
        self.cur.execute("SELECT password FROM users WHERE username = ?", (username,))
        row = self.cur.fetchall()
        self.conn.close()
        if len(row) == 0:
            return False
        return row[0][0] == hash_password(password)
    
    def set_session_id(self, password):
        Database.open_database(self)
        self.cur.execute("SELECT Userid FROM users WHERE password = ?", (hash_password(password),))
        row = self.cur.fetchall()
        self.conn.close()
        if len(row) == 0:
            return False
        return row[0][0]
    
    
User().create_table()