import socket
from tkinter import *
from tkinter import ttk
from creational.singleton import Singleton
from structural.forms import MainForm, SubForms, SearchForm
from structural.src.search import search

class MainWindow(Tk, Singleton):
    def init(self, token):
        super().__init__() 
        self.title("HeadHunder client")
        self.geometry("1280x720")
        self.sub_forms = []
        self.makeUI(token)

    def makeUI(self, token):
        self.notebook = ttk.Notebook()
        self.notebook.pack(expand=True, fill=BOTH)
        self.settingFrame = MainForm(self.notebook, token, search)
        self.main_frame = SearchForm(self.notebook, search, self.create_new_form, token)

        self.settingFrame.pack(expand=True, fill=BOTH)
        self.main_frame.pack(expand=True, fill=BOTH)

        self.notebook.add(self.settingFrame, text="Настройки")
        self.notebook.add(self.main_frame, text="Главная")

    def create_new_form(self, result, form_name):
        self.sub_forms.append(SubForms(self.notebook, result, self.delete_form))
        self.sub_forms[-1].pack(expand=True, fill=BOTH)
        self.notebook.add(self.sub_forms[-1], text=form_name)
        self.notebook.select(len(self.sub_forms) + 1)

    def delete_form(self, index):
        self.sub_forms.pop(index - 2)

    def __init__(self, token):
        pass
