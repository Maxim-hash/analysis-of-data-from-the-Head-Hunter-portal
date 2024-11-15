from tkinter import BOTH, DISABLED, HORIZONTAL, NORMAL, PanedWindow, ttk
from tkinter import Button, Frame, Label
from structural.frames import *
from structural.config import secret_key

import jwt


class MainForm(Frame):
    def __init__(self, master, token, search_func):
        super().__init__(master=master)
        self.search_func = search_func
        self.token = token
        self.user_info = self.decode_token(token)

        self.setup_ui()

    def decode_token(self, token):
        # Декодирование токена пользователя
        decoded = jwt.decode(token, secret_key, algorithms=["HS256"])
        return decoded

    def setup_ui(self):
        # Создаем PanedWindow с вертикальным разделением
        self.paned_window = PanedWindow(self, orient=HORIZONTAL)
        self.paned_window.pack(fill=BOTH, expand=True)

        # Создаем фрейм для управления (20%)
        self.control_frame = Frame(self.paned_window, width=200, height=600, bg='lightgray')
        self.control_frame.pack(fill=BOTH, expand=True)
        self.paned_window.add(self.control_frame, width=200)  # Устанавливаем ширину фрейма

        # Создаем фрейм для отображения контента (80%)
        self.display_frame = Frame(self.paned_window, bg='white')
        self.display_frame.pack(fill=BOTH, expand=True)
        self.paned_window.add(self.display_frame)  # Оставшееся пространство отдается этому фрейму

        self.admin_frame = AdminFrame(self.display_frame, self.search_func, self.token)
        self.user_frame = UserFrame(self.display_frame, self.search_func, self.token)
        self.change_password_frame = ChangePasswordFrame(self.display_frame, self.search_func, self.token)

        # Пример добавления элементов управления
        ttk.Label(self.control_frame, text="Панель управления").pack(pady=10)
        self.user_button = ttk.Button(self.control_frame, text="Пользовательская панель", state="disabled", command=self.show_initial_content)
        self.user_button.pack(pady=5, fill="x")
        self.change_password_button = ttk.Button(self.control_frame, text="Сменить пароль", command=self.change_password)
        
        # Добавление кнопки панели администратора
        if self.user_info.get('role') == 2:
            self.admin_button = ttk.Button(self.control_frame, text="Панель администратора", command=self.show_administator_content)
            self.admin_button.pack(pady=10, fill="x")

        self.change_password_button.pack(pady=5, fill="x")

        self.user_frame.update()

    def clear_display_frame(self):
        for widget in self.display_frame.winfo_children():
            widget.destroy()

    def change_password(self):
        self.clear_display_frame()
        self.user_button.config(state=NORMAL)
        self.change_password_frame.update()

    def show_initial_content(self):
        self.clear_display_frame()
        self.user_button.config(state=DISABLED)
        if self.user_info.get('role') == 2:
            self.admin_button.config(state=NORMAL)
        self.user_frame.update()

    def show_administator_content(self):
        self.clear_display_frame()
        self.user_button.config(state=NORMAL)
        self.admin_button.config(state=DISABLED)
        self.admin_frame.update()