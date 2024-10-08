from tkinter import NE, messagebox, Button, Frame, Label, Scrollbar
from tkinter.ttk import Treeview


class AdminFrame(Frame):
    def __init__(self, master, search, token):
        super().__init__(master=master)
        self.token = token
        self.search = search

    def makeUI(self, data):
        Label(self.master, text="Панель Администратора", bg='white').pack()
        
        Button(self.master, text="Обновить базу данных", command=self.update_database).pack(anchor=NE)

        journal_container = Frame(self.master, bg='white')
        journal_container.pack(expand=False, fill="both")
        self.selected_user = Label(journal_container, bg='white')
        self.selected_user_button = Button(journal_container, text="Заблокировать", command=self.ban_user)
        self.show_journal(journal_container, data)

        ban_list_container = Frame(self.master, bg='white')
        ban_list_container.pack(expand=False, fill="both")
        self.selected_banned_user = Label(ban_list_container, bg='white')
        self.selected_banned_user_button = Button(ban_list_container, text="Разблокировать", command=self.unban_user)
        self.show_banned_users(ban_list_container)

    def unban_user(self):
        data = self.search(self.token, "update", username = self.selected_banned_user["text"], new_status = 0)
        messagebox.showinfo("Успех", data.data)

    def update_database(self,):
        self.search(self.token, "update", database="")

    def show_banned_users(self, container):
        Label(container, text="Список заблокированных пользователей", bg='white').pack()
        data = self.search(self.token, user="", status=3).data

        tree = Treeview(container, columns=("Login", "Token", "Status"), show="headings")

        # Установка заголовков столбцов
        tree.heading("Login", text="Login")
        tree.heading("Token", text="Token")
        tree.heading("Status", text="Status")

        # Установка ширины столбцов
        tree.column("Login", width=30)
        tree.column("Token", width=500)
        tree.column("Status", width=15)

        # Добавление данных в таблицу
        for i in data:
            tree_data = [i, data[i]["token"], data[i]["mode_id"]]

            tree.insert("", "end", values=tree_data)
       
        # Создание вертикальной прокрутки
        scrollbar_vertical = Scrollbar(container, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar_vertical.set)
        scrollbar_vertical.pack(side="right", fill="y")

        # Создание горизонтальной прокрутки
        scrollbar_horizontal = Scrollbar(container, orient="horizontal", command=tree.xview)
        tree.configure(xscrollcommand=scrollbar_horizontal.set)
        scrollbar_horizontal.pack(side="bottom", fill="x")

        def item_selected(event):
            selected_people = ""
            for selected_item in tree.selection():
                item = tree.item(selected_item)
                person = item["values"][0]
                selected_people = f"{selected_people}{person}"
            self.selected_banned_user["text"]=selected_people
            self.selected_banned_user.pack()
            self.selected_banned_user_button.pack()
 
        tree.bind("<<TreeviewSelect>>", item_selected)

        # Размещение виджета Treeview в окне приложения
        tree.pack(side="left", expand=True, fill="both")


    def show_journal(self, container, data):
        Label(container, text="Журнал действий пользователей", bg='white').pack()
        tree = Treeview(container, columns=("ID", "Login", "Action", "Status", "Time"), show="headings")

        # Установка заголовков столбцов
        tree.heading("ID", text="ID")
        tree.heading("Login", text="Login")
        tree.heading("Action", text="Action")
        tree.heading("Status", text="Status")
        tree.heading("Time", text="Time")

        # Установка ширины столбцов
        tree.column("ID", width=15)
        tree.column("Login", width=30)
        tree.column("Action", width=500)
        tree.column("Status", width=20)
        tree.column("Time", width=40)

        # Добавление данных в таблицу
        for i in data:
            tree_data = [i, data[i]["token"], data[i]["action"], data[i]["status"], data[i]["time"]]

            tree.insert("", "end", values=tree_data)
       
        # Создание вертикальной прокрутки
        scrollbar_vertical = Scrollbar(container, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar_vertical.set)
        scrollbar_vertical.pack(side="right", fill="y")

        # Создание горизонтальной прокрутки
        scrollbar_horizontal = Scrollbar(container, orient="horizontal", command=tree.xview)
        tree.configure(xscrollcommand=scrollbar_horizontal.set)
        scrollbar_horizontal.pack(side="bottom", fill="x")

        def item_selected(event):
            selected_people = ""
            for selected_item in tree.selection():
                item = tree.item(selected_item)
                person = item["values"][1]
                selected_people = f"{selected_people}{person}"
            self.selected_user["text"]=selected_people
            self.selected_user.pack()
            self.selected_user_button.pack()
 
        tree.bind("<<TreeviewSelect>>", item_selected)

        tree.pack(side="left", expand=True, fill="both")

    def update(self):
        data = self.search(self.token, journal="%")
        self.makeUI(data.data)

    def ban_user(self):
        data = self.search(self.token, "update", username = self.selected_user["text"], new_status = 3)
        messagebox.showinfo("Успех", data.data)