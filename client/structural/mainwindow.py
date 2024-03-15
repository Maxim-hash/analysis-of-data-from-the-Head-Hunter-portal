from tkinter import *
import socket
import config
from creational.singleton import Singleton

class Window(Tk, Singleton):
    def init(self):
        super().__init__() 
        self.title("HeadHunder client")
        self.geometry("1280x720")

        Label(self, text="Login").pack(pady=20)
        self.entry_login = Entry(width=40)
        self.entry_login.pack()
        self.l = Label(self)
        Button(self, text="Search", command=self.search).pack(pady=20)

    def search(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect((config.host_ip, config.port))

            msg = self.entry_login.get()
            sock.send(msg.encode(config.encoding))

            data = sock.recv(1024)
            if data:
                self.entry_login.delete(0, END)
                self.l['text'] = f"Your request: {data.decode(config.encoding)}"
                self.l.pack()
            #print(data.decode(config.encoding))
            sock.close()
        except:
            print("На сервере ведутся технические работы приносим свои извинение за предоставленные неудобства."
                  "\nПопробуйте повторить попытку через пару минут")
            sock.close()



    def __init__(self):
        pass