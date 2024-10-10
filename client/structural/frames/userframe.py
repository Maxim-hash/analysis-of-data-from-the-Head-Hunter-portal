from tkinter import W
from tkinter import Frame, Label, Scrollbar
from structural.config import secret_key
from structural.src.tree import JournalTree

import jwt


class UserFrame(Frame):
    def __init__(self, master, search, token):
        super().__init__(master=master)
        self.token = token
        self.params = jwt.decode(token, secret_key, algorithms=["HS256"])
        self.search = search

    def makeUI(self, data):
        Label(self.master, text="Пользовательская панель", bg='white').pack()
        login = self.params["login"]
        Label(self.master, text=login, bg="white").pack(anchor=W)

        container = Frame(self.master)
        container.pack(expand=False, fill="both")

        tree = JournalTree(container)
        tree_data = [[i, data[i]["token"], data[i]["action"], data[i]["status"], data[i]["time"]] for i in data]
        tree.set_data(tree_data)

        tree.pack(side="left", expand=True, fill="both")

    def update(self):
        data = self.search(self.token, journal=self.params["login"])
        self.makeUI(data.data)