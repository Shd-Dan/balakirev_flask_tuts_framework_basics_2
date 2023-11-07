import math
import sqlite3
import time


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

    def addPost(self, title, text):
        try:
            post_time = math.floor(time.time())
            self.__cursor.execute("INSERT INTO posts VALUES(NULL, ?,?,?)", (title, text, post_time))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Adding post to DB error" + str(e))
            return False

        return True