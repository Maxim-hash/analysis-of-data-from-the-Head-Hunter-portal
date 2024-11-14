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
    """Storage for keeping local data"""

    __db_name__ = "database.db"
    
    def __init__(self) -> None:
        self.setConnection()

    def __del__(self) -> None:
        print("connection closed")
        self.connection.close()

    def setConnection(self) -> None:
        """Create connection with sqlite engine"""

        try:
            self.connection = sqlite3.connect(self.__db_name__)
        except Error:
            print(Error)

    def getUsers(self) -> list:
        """Get all users"""

        cursor = self.connection.cursor()

        query = "SELECT username, password FROM Users"

        cursor.execute(query)
        users = cursor.fetchall()

        return users
    
    def getUser(self, username):
        """Get user by current username"""

        cursor = self.connection.cursor()

        query = f"SELECT username, password FROM Users WHERE username='{username}'"

        cursor.execute(query)
        user = cursor.fetchone()

        return user
    
    def createUser(self, newUser, password):
        """Creating user in Users"""

        cursor = self.connection.cursor()

        query = "INSERT INTO Users (username, password) VALUES (?, ?)" 
        cursor.execute(query, (newUser, password))

        self.connection.commit()

    def createJournalEntry(self, currentUser, entry):
        """Creating entry in Journal"""

        cursor = self.connection.cursor()

        query = "INSERT INTO Journal (username, action) VALUES (?, ?)"
        cursor.execute(query, (currentUser, entry))

        self.connection.commit()

    def getJournalEntries(self, currentUser):
        """Get entries from Journal"""

        cursor = self.connection.cursor()

        query = f"SELECT action FROM Journal WHERE username='{currentUser}'"
        cursor.execute(query)
        raw_entries = cursor.fetchall()
        entries = [entry[0] for entry in raw_entries]

        return entries
    
    def createTables(self):
        """Creating tables in database"""

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


    def cleanTables(self):
        """Delete all data from tables"""

        cursor = self.connection.cursor()

        query = "DELETE FROM Users"
        cursor.execute(query)

        query = "DELETE FROM Journal"
        cursor.execute(query)

        self.connection.commit()
