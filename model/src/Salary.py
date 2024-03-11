from model.src.DBTable_Entity import DBTable_Entity

class Salary(DBTable_Entity):
    def __init__(self, name, sal):
       self.name = name
       self.sal = sal

    def get_list_entry(self):
        return [self.name, self.sal]



sal = Salary("asd", 123454)

print(sal.get_list_entry())

