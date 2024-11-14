from structural.src.localstorage import LocalStorage
from creational.singleton import Singleton

class LocalStorageManager(Singleton):
    __current_user__ : str

    def __init__(self):
        self.database = LocalStorage()

    @classmethod
    def set_current_user(cls, currentUser):
        cls.__current_user__ = currentUser

    def getUsers(self):
        users = self.database.getUsers()

        return users
    
    def getEntries(self):
        entries = self.database.getJournalEntry()

        return entries