import socket
from tkinter import *
from structural import config
from creational.singleton import Singleton
from structural.src.request_builder import Requst_Builder

class Window(Tk, Singleton):
    def init(self):
        super().__init__() 
        self.title("HeadHunder client")
        self.geometry("1280x720")

        Label(self, text="Search").pack(pady=20)
        self.entry_vacancy_name = Entry(width=40)
        self.entry_vacancy_name.pack()
        self.l = Label(self)
        Button(self, text="Search", command=self.search).pack(pady=20)

    def search(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        request_builder = Requst_Builder("get")
        try:
            sock.connect((config.host_ip, config.port))

            vacancy_name = self.entry_vacancy_name.get()
            request_builder.add_item(vacancy_name)
            request = request_builder.build()
            sock.send(request.encode(config.encoding))

            data = sock.recv(1024)
            if data:
                self.entry_vacancy_name.delete(0, END)
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