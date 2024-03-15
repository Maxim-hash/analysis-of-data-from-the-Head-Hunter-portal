from tkinter import *
from tkinter import ttk
import socket
from config import *
from creational.singleton import Singleton



class AutorizationWindow(Tk, Singleton):
    def init(self):
        super().__init__() 
        self.title("Панель авторизации")
        self.geometry("400x300")
        Label(self, text="Login").pack(pady=20)
        self.entry_login = ttk.Entry(width=40)
        self.entry_login.pack()
        Label(self, text="Password").pack(pady=20)
        self.entry_password = ttk.Entry(width=40, show="*")
        self.entry_password.pack()
        ttk.Button(self, text="Log in", command=self.login).pack(pady=20)

    def login(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect((host_ip, port))

            msg = f"{self.entry_login.get()}, {self.entry_password.get()}"
            sock.send(msg.encode(encoding))

            resp = sock.recv(1024)
            self.data = resp.decode(encoding)
            if self.data == f"b'{self.entry_login.get()}, {self.entry_password.get()}' WAS HANDELED":
                self.destroy()
                sock.close()
            else:
                self.entry_login.delete(0, END)
                self.entry_password.delete(0, END)
            #print(self.data.decode(encoding))
        except:
            print("На сервере ведутся технические работы приносим свои извинение за предоставленные неудобства."
                  "\nПопробуйте повторить попытку через пару минут")
            sock.close()


    def __init__(self):
        pass