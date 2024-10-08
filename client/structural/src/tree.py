from tkinter.ttk import Treeview
from typing import List


class Tree(Treeview):
    def __init__(self, container, columns_name: List = [], columns_size: List = []):
        super().__init__(container, columns=columns_name, show="headings")
        if columns_name:
            self.set_heading(columns_name)
        if columns_size:
            self.set_heading_size(columns_size)

    def set_heading_size(self,columns_name: List = [], column_size: List = []):
        if column_size and not len(column_size) > len(columns_name): 
            for i in range(len(column_size)):
                self.column(columns_name[i], column_size[i])

    def set_heading(self, columns_heading: List = []):
        if columns_heading:
            for i in columns_heading:
                self.heading(i, text = i)

    def set_data(self, data:List):
        for i in data:
            self.insert("", "end", values=i)

class ExperienceTree(Tree):
    def __init__(self, container, columns_name: List = [], columns_size: List = []):
        columns_name = ["Опыт работы", "Среднее зарплат", "Медиана Зарплат", "Мода зарплат", "Количество вакансий"]
        columns_size = [60, 100, 100, 100, 100]
        super().__init__(container, columns_name, columns_size)

class EmployerTree(Tree):
    def __init__(self, container, columns_name: List = [], columns_size: List = []):
        columns_name = ["Компания", "Среднее зарплат", "Медиана Зарплат", "Мода зарплат", "Количество вакансий"]
        columns_size = [60, 100, 100, 100, 100]
        super().__init__(container, columns_name, columns_size)