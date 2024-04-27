import socket
from tkinter import *
from tkinter import ttk
from structural.config import *
from creational.singleton import Singleton
from structural.src.request_builder import *

class AutorizationWindow(Tk, Singleton):
    def init(self, on_success=None):
        self.on_success = on_success
        super().__init__() 
        self.errorLabel = Label(self)
        self.title("Панель авторизации")
        self.geometry("400x300")
        Label(self, text="Login").pack(padx=5, pady=5)
        self.entry_login = ttk.Entry(width=40)
        self.entry_login.pack(padx=5, pady=5)
        Label(self, text="Password").pack(padx=5, pady=5)
        self.entry_password = ttk.Entry(width=40, show="*")
        self.entry_password.pack(padx=5, pady=5)
        ttk.Button(self, text="Log in", command=self.login).pack(padx=5, pady=5)
        ttk.Button(self, text="Registration", command=self.auth).pack(padx=5, pady=5)

    def login(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            sock.connect((host_ip, port))

            login = self.entry_login.get()
            password = self.entry_password.get()
            builder = JSONRequestBuilder(LoginRequestTemplate(login, password))
            message = builder.build()
            sock.send(message.encode(encoding))

            resp = sock.recv(1024)
            self.data = resp.decode(encoding)
            if self.data == "200":
                sock.close()
                self.on_success()
            else:
                self.errorLabel['text'] = "Ошибка в ведённых данных"
                self.entry_password.delete(0, END)
                self.errorLabel.pack()
        except:
            self.entry_login.delete(0, END)
            self.entry_password.delete(0, END)
            sock.close()
            print("На сервере ведутся технические работы приносим свои извинение за предоставленные неудобства."
                  "\nПопробуйте повторить попытку через пару минут")
            
    def auth(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect((host_ip, port))
            login = self.entry_login.get()
            password = self.entry_password.get()
            builder = JSONRequestBuilder(AuthRequestTemplate(login, password))
            message = builder.build()
            sock.send(message.encode(encoding))

            resp = sock.recv(1024)
            self.data = resp.decode(encoding)
            if self.data == "200":
                sock.close()
                self.on_success()
            else:
                self.errorLabel['text'] = "Такой пользователь уже зарегистрирован"
                self.entry_login.delete(0, END)
                self.entry_password.delete(0, END)
                self.errorLabel.pack()
        except:
            self.entry_login.delete(0, END)
            self.entry_password.delete(0, END)
            sock.close()
            print("На сервере ведутся технические работы приносим свои извинение за предоставленные неудобства."
                  "\nПопробуйте повторить попытку через пару минут")
    def __init__(self, *args):
        pass