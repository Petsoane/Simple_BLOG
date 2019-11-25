import sqlite3
from flask import session


class Database:
    def __init__(self, db_name):
        self.__conn = sqlite3.connect(db_name, check_same_thread=False)
    
    def congfig(self):
        sql_users = '''CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            name TEXT NOT NULL, 
            lastName TEXT NOT NULL, 
            email TEXT NOT NULL,
            sex TEXT NOT NULL DEFAULT 'bi-sexual',
            password TEXT NOT NULL,
            image_name TEXT NOT NULL DEFAULT 'default.png'
        )
        '''
        # Create the user table in the database
        self.__conn.execute(sql_users)


    # create a function to add users to the table
    def add_user(self, username, email, password, name, lastname):
        sql = 'INSERT INTO users (username, name, lastName, email, password) VALUES(?,?,?,?,?)'
        cur = self.__conn.cursor()
        cur.execute(sql, (username, name, lastname, email, password))
        self.__conn.commit()
    


    # Get all the users information.
    def get_information(self, username):
        sql = 'SELECT * FROM users WHERE username=?'
        keys = ('id', 'username', 'name', 'lastName', 'email', 'sex', 'password', 'image_name')
        cur = self.__conn.cursor()

        cur.execute(sql, (username,))
        ret = cur.fetchone()
        return dict(zip(keys, ret))

    # Check if the user exist.
    def user_exists(self, username, password):
        sql = 'SELECT * FROM users WHERE password=? AND username=?'
        cur = self.__conn.cursor()
        cur.execute(sql, (password, username))

        ret = cur.fetchone()
        return True if ret else False
    
    # check if the user name exists.
    def usename_unique(self, username):
        sql = 'SELECT * from users WHERE username=?'
        cur = self.__conn.cursor()
        cur.execute(sql, (username,))
        
        ret = cur.fetchone()
        return False if ret else True
    
    # Check if the email is unique
    def email_unique(self, email):
        sql = 'SELECT * from users WHERE email=?'
        cur = self.__conn.cursor()
        cur.execute(sql, (email,))
        
        ret = cur.fetchone()
        return False if ret else True

    # This function is used to run the sql commads the return one value.
    def run_ret(self, sql, args=None):
        cur = self.__conn.cursor()

        cur.execute(sql, args)
        return cur.fetchall()

    # This function runs the sql but does not return the value to the user
    def run(self, sql, args=None):
        cur = self.__conn.cursor()
        cur.execute(sql, args)
        self.__conn.commit()