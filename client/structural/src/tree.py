from tkinter import Scrollbar
from tkinter.ttk import Treeview
from typing import List


class Tree(Treeview):
    def __init__(self, container, columns_name: List = [], columns_size: List = []):
        super().__init__(container, columns=columns_name, show="headings")
        if columns_name:
            self.set_heading(columns_name)
        if columns_size:
            self.set_heading_size(columns_size)

        self.set_horizontal_scrollbar(container)
        self.set_vertical_scrollbar(container)

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

    def set_vertical_scrollbar(self, container):
        scrollbar_vertical = Scrollbar(container, orient="vertical", command=self.yview)
        self.configure(yscrollcommand=scrollbar_vertical.set)
        scrollbar_vertical.pack(side="right", fill="y")

    def set_horizontal_scrollbar(self, container):
        scrollbar_horizontal = Scrollbar(container, orient="horizontal", command=self.xview)
        self.configure(xscrollcommand=scrollbar_horizontal.set)
        scrollbar_horizontal.pack(side="bottom", fill="x")


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

class JournalTree(Tree):
    def __init__(self, container, columns_name: List = [], columns_size: List = []):
        columns_name = ["ID", "Login", "Action", "Status", "Time"]
        columns_size = [15, 30, 500, 20, 40]
        super().__init__(container, columns_name, columns_size)

class UserTree(Tree):
    def __init__(self, container, columns_name: List = [], columns_size: List = []):
        columns_name = ["Login", "Token" , "Status"]
        columns_size = [30, 500, 15]
        super().__init__(container, columns_name, columns_size)