from localstorage import LocalStorage
#from creational.singleton import Singleton

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


class LocalStorageManager(Singleton):
    __current_user__ : str

    def __init__(self):
        self.database = LocalStorage()
        self.database.createTables()

    @classmethod
    def set_current_user(cls, currentUser):
        cls.__current_user__ = currentUser

    @classmethod
    def is_exist_current_user(cls):
        if hasattr(cls, "__current_user__"):
            return True
        
        return False
    
    def createUser(self, username, password):
        user = self.database.getUser(username)
        if user:
            return 
        
        if password:
            self.database.createUser(username, password)

    def createEntry(self, entry):
        if self.is_exist_current_user():
            self.database.createJournalEntry(self.__current_user__, entry)

    def getUsers(self):
        users = self.database.getUsers()

        return users
    
    def getEntries(self):
        if self.is_exist_current_user():
            entries = self.database.getJournalEntries(self.__current_user__)

            return entries
        
    def cleanTables(self):
        self.database.deleteFromTables()

    

lsm = LocalStorageManager()
#lsm.cleanTables()
username = "ALLA"
lsm.createUser(username, "dqfwqwfg")
lsm.set_current_user(username)
for entry in lsm.getEntries():
    print(entry)

print(lsm.getUsers())