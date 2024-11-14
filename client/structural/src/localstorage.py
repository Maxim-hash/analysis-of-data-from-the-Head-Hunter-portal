import sqlite3
from sqlite3 import Error

class Singleton(object):
    def __new__(cls, *args, **kwds):
        it = cls.__dict__.get("__it__")
        if it is not None:
              return it
        cls.__it__ = it = object.__new__(cls)
        it.init(*args, **kwds)
        return it
    def init(self, *args, **kwds):
        pass

class LocalStorage(Singleton):
    __db_name__ = "database.db"
    
    def __init__(self) -> None:
        self.setConnection()

    def __del__(self) -> None:
        print("connection closed")
        self.connection.close()

    def setConnection(self) -> None:
        try:
            self.connection = sqlite3.connect(self.__db_name__)
        except Error:
            print(Error)

    def getUsers(self) -> list:
        cursor = self.connection.cursor()

        query = f"SELECT * FROM Users"

        cursor.execute(query)
        users = cursor.fetchall()

        return users
    
    def createUser(self, newuser, password):
        cursor = self.connection.cursor()

        query = "INSERT INTO Users (username, password) VALUES (?, ?)" 
        cursor.execute(query, (newuser, password))

        self.connection.commit()
    
    def createTables(self):
        cursor = self.connection.cursor()
        
        query = """
                CREATE TABLE IF NOT EXISTS Users (
                id INTEGER PRIMARY KEY,
                username TEXT NOT NULL,
                password TEXT NOT NULL)
            """
        
        cursor.execute(query)
        query = """
                CREATE TABLE IF NOT EXISTS Journal (
                id INTEGER PRIMARY KEY,
                username TEXT NOT NULL,
                action TEXT NOT NULL)
            """
        cursor.execute(query)
        self.connection.commit



a = LocalStorage()

a.createTables()
a.createUser("OLEG", "dqwpffewgf")

print(a.getUsers())