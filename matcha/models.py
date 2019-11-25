from matcha import mysql
from flask import session


class Database:
    def __init__(self, db_name):
        self.__conn = mysql.connect()
    
    def congfig(self):
        sql_users = '''CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTO_INCREMENT,
            username VARCHAR(255) NOT NULL,
            name VARCHAR(255) NOT NULL, 
            lastName VARCHAR(255) NOT NULL, 
            email VARCHAR(255) NOT NULL,
            sex VARCHAR(255) NOT NULL DEFAULT 'bi-sexual',
            password VARCHAR(255) NOT NULL,
            image_name VARCHAR(255) NOT NULL DEFAULT 'default.png'
        )
        '''

        sql_post = '''CREATE TABLE IF NOT EXISTS posts(
            id INTEGER PRIMARY KEY AUTO_INCREMENT,
            title VARCHAR(255) NOT NULL,
            content VARCHAR(255) NOT NULL,
            author INTEGER NOT NULL,
            date_posted DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(author) REFERENCES users(id)
        )'''
        
        # Create the user table in the database
        curs = self.__conn.cursor()
        curs.execute(sql_users)
        curs.execute(sql_post)
        self.__conn.commit()


    # A function to add users to the table
    def add_user(self, username, email, password, name, lastname):
        sql = 'INSERT INTO users (username, name, lastName, email, password) VALUES(%s, %s,%s, %s, %s)'
        cur = self.__conn.cursor()
        cur.execute(sql, (username, name, lastname, email, password))
        self.__conn.commit()

    # A function to add a users post.
    def add_post(self, title, content, author):
        sql = 'INSERT INTO posts (title, content, author) VALUES(%s, %s, %s)'
        cur = self.__conn.cursor()
        cur.execute(sql, (title, content, author))
        self.__conn.commit()
    


    # Get all the users information.
    def get_information(self, username):
        sql = 'SELECT * FROM users WHERE username=%s'
        keys = ('id', 'username', 'name', 'lastName', 'email', 'sex', 'password', 'image_name')
        cur = self.__conn.cursor()

        cur.execute(sql, (username,))
        ret = cur.fetchone()
        return dict(zip(keys, ret))
    
    # Get one post from the database
    def get_post(self, post_id):
        sql = 'SELECT * FROM posts WHERE id=%s'
        keys = ('id', 'title', 'content', 'author','date_posted')
        a_keys = ('id', 'username', 'name', 'lastName', 'email', 'sex', 'password', 'image_name')

        cur = self.__conn.cursor()
        cur.execute(sql, (post_id,))
        post = dict(zip(keys, cur.fetchone()))

        sql = 'SELECT * FROM users WHERE id=%s'
        cur.execute(sql, post['author'])
        post['author'] = dict(zip(a_keys, cur.fetchone()))
        return post
    
    # Get posts for one user
    def  get_user_posts(self, user_id):
        sql = 'SELECT * FROM posts WHERE author=%s'
        keys = ('id', 'title', 'content', 'author', 'date_posted')
        a_keys = ('id', 'username', 'name', 'lastName', 'email', 'sex', 'password', 'image_name')
        posts = []

        cur = self.__conn.cursor()
        cur.execute(sql, (user_id,))
        ret = cur.fetchall()
        for post in ret:
            posts.append(dict(zip(keys, post)))

        sql = 'SELECT * FROM users WHERE id=%s'
        for post in posts:
            cur.execute(sql, (post['author'],))
            post['author'] = dict(zip(a_keys, cur.fetchone()))

        return (posts)
        


    # Check if the user exist.
    def user_exists(self, username, password):
        sql = 'SELECT * FROM users WHERE password=%s AND username=%s'
        cur = self.__conn.cursor()
        cur.execute(sql, (password, username))

        ret = cur.fetchone()
        return True if ret else False
    
    # check if the user name exists.
    def usename_unique(self, username):
        sql = 'SELECT * from users WHERE username=%s'
        cur = self.__conn.cursor()
        cur.execute(sql, (username,))
        
        ret = cur.fetchone()
        return False if ret else True
    
    # Check if the email is unique
    def email_unique(self, email):
        sql = 'SELECT * from users WHERE email=%s'
        cur = self.__conn.cursor()
        cur.execute(sql, (email,))
        
        ret = cur.fetchone()
        return False if ret else True

    def get_users(self):
        sql = 'SELECT * FROM users'
        keys = ('id', 'username', 'name', 'lastName', 'email', 'sex', 'password', 'image_name')
        cur = self.__conn.cursor()
        out = []

        cur.execute(sql)
        ret = cur.fetchall()
        for user in ret:
            out.append(dict(zip(keys, user)))
        return out


    def  get_posts(self):
        sql = 'SELECT * FROM posts'
        keys = ('id', 'title', 'content', 'author', 'date_posted')
        a_keys = ('id', 'username', 'name', 'lastName', 'email', 'sex', 'password', 'image_name')
        posts = []

        cur = self.__conn.cursor()
        cur.execute(sql)
        ret = cur.fetchall()
        for post in ret:
            posts.append(dict(zip(keys, post)))

        sql = 'SELECT * FROM users WHERE id=%s'
        for post in posts:
            cur.execute(sql, (post['author'],))
            post['author'] = dict(zip(a_keys, cur.fetchone()))

        return (posts)

    # This function is used to run the sql commads the return one value.
    def run_ret(self, sql, args=None):
        cur = self.__conn.cursor()

        if args:
            cur.execute(sql, args)
        else:
            cur.execute(sql)
        return cur.fetchall()

    # This function runs the sql but does not return the value to the user
    def run(self, sql, args=None):
        cur = self.__conn.cursor()
        cur.execute(sql, args)
        self.__conn.commit()