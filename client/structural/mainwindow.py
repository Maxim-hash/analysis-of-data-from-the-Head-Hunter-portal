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

        vacancy_name_frame = Vacancy_Name_Frame()
        vacancy_name_frame.pack(padx=5, pady=5)

    def __init__(self):
        pass

class Vacancy_Name_Frame(Frame):
    def __init__(self):
        super().__init__(borderwidth=1, relief=SOLID, padx=8, pady=10)
        Label(self, text="Наименование вакансии").pack(padx=5, pady=5)
        self.entry_vacancy_name = Entry(self, width = 40,)
        self.entry_vacancy_name.pack(anchor=W, fill=X, padx=5, pady=5)
        self.l = Label(self)
        button = Button(self, text="Поиск", command=self.search).pack(anchor=E, padx=5, pady=5)
        
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
                    self.l.pack(anchor=NW, fill=X, padx=5, pady=5)
                #print(data.decode(config.encoding))
                sock.close()
            except:
                print("На сервере ведутся технические работы приносим свои извинение за предоставленные неудобства."
                    "\nПопробуйте повторить попытку через пару минут")
                sock.close()