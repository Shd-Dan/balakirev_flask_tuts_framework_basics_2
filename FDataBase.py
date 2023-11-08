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
