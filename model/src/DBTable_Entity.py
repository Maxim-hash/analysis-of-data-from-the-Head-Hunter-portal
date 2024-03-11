from abc import ABC, abstractmethod

class DBTable_Entity(ABC):
    @abstractmethod
    def get_list_entry(self):
        pass