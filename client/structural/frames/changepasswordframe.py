from tkinter import NW, TOP, messagebox
from tkinter import ttk
from tkinter import Button, Frame, Label
from structural.config import secret_key
import jwt

class ChangePasswordFrame(Frame):
    def __init__(self, master, search, token):
        super().__init__(master=master)
        self.token = token
        self.params = jwt.decode(token, secret_key, algorithms=["HS256"])
        self.search = search

    def makeUI(self):
        ttk.Label(self.master, text="Смена пароля").pack(side=TOP)
        ttk.Label(self.master, text="Введите новый пароль").pack(anchor=NW)
        self.entry_password1 = ttk.Entry(self.master, width=40, show="*")
        self.entry_password1.pack(padx=5, pady=5)
        ttk.Label(self.master, text="Подтвердите пароль").pack(anchor=NW)
        self.entry_password2 = ttk.Entry(self.master, width=40, show="*")
        self.entry_password2.pack(padx=5, pady=5)

        self.change_password_button = ttk.Button(self.master, text="Сменить пароль", command=self.change_password)
        self.change_password_button.pack()

    def change_password(self):
        password = self.entry_password1.get()
        password2 = self.entry_password2.get()

        if password != password2:
            messagebox.showerror("Ошибка", "Пароли не совпадают")
            return 
        
        data = self.search(self.token, "update", username=self.params["login"], new_password=password)
        messagebox.showinfo("Успех", data.data)

    def update(self):
        self.makeUI()

