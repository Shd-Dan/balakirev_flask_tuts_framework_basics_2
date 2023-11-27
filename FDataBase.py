import math
import re
import sqlite3
import time

from flask import url_for


class FDataBase():
    def __init__(self, db):
        self.__db = db
        self.__cursor = db.cursor()

    def getMenu(self):
        sql = '''SELECT * FROM mainmenu'''  # all data is got

        try:
            # data getting sql methods
            self.__cursor.execute(sql)
            result = self.__cursor.fetchall()
            if result:
                return result
        except:
            print("Data-base fetching error")
        return []  # for case of any exception empty list will be returned

    def addPost(self, title, text, url):
        try:
            # Checking if url already exists
            self.__cursor.execute('SELECT COUNT() as "count" FROM POSTS WHERE url LIKE "{url}"')
            result = self.__cursor.fetchone()
            if result['count'] > 0:
                print("Post with such url exists")
                return False
            #
            # URL path for images in directory, path is holded in DB
            base = url_for('static', filename='images_html')

            text = re.sub(r"(?P<tag><img\s+[^>]*src=)(?P<quote>[\"'])(?P<url>.+?)(?P=quote)>",
                          "\\g<tag>" + base + "/\\g<url>>", text)
            #
            post_time = math.floor(time.time())
            self.__cursor.execute("INSERT INTO posts VALUES(NULL, ?,?,?,?)", (title, text, url, post_time))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Adding post to DB error" + str(e))
            return False

        return True

    # id was changed to url fetching with argument 'alias'
    def getPost(self, alias):
        try:
            self.__cursor.execute(f'SELECT title, text FROM posts WHERE url LIKE "{alias}" LIMIT 1')
            result = self.__cursor.fetchone()
            if result:
                return result

        except sqlite3.Error as e:
            print("I could not get a post from DB, sorry :(" + str(e))

        return False, False

    # Method getPostsAnnounce returns the list of posts
    def getPostsAnnounce(self):
        try:
            self.__cursor.execute(f"SELECT id, title, text, url FROM posts ORDER BY time DESC")
            result = self.__cursor.fetchall()
            if result:
                return result
        except sqlite3.Error as e:
            print("Posts getting error" + str(e))

        return []

    def add_user(self, name, email, hash_psw):
        try:
            self.__cursor.execute(f"SELECT COUNT() as 'count' FROM users WHERE email LIKE '{email}'")
            result = self.__cursor.fetchone()
            if result['count'] > 0:
                print('Email exist')
                return False

            user_time = math.floor(time.time())
            self.__cursor.execute("INSERT INTO users VALUES(NULL, ?, ?, ?, NULL, ?)", (name, email, hash_psw, user_time))
            self.__db.commit()
        except sqlite3.Error as e:
            print("New user was not added " + str(e))
            return False

        return True

    # Function is used in UserLogin.py to fetch user data from database.
    def get_user(self, user_id):
        try:
            self.__cursor.execute(f"SELECT * FROM users WHERE ID = {user_id} LIMIT 1")
            result = self.__cursor.fetchone()
            if not result:
                print("User was not found")
                return False
            return result

        except sqlite3.Error as e:
            print('Error getting data from data-base (FDataBase.py:get_user)' + str(e))

        return False

    def get_user_by_email(self, email):
        try:
            self.__cursor.execute(f"SELECT * FROM users WHERE email = '{email}' LIMIT 1")
            result = self.__cursor.fetchone()
            if not result:
                print("User was not found (FDataBase.py:get_user_by_email)")
                return False
            return result

        except sqlite3.Error as e:
            print('Error getting data from data-base (FDataBase.py:get_user_by_email)' + str(e))
        return False
