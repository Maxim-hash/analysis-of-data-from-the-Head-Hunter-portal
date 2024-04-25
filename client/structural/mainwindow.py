import socket
from tkinter import *
from tkinter import ttk
from structural import config
from creational.singleton import Singleton
from structural.src.request_builder import Requst_Builder

class MainWindow(Tk, Singleton):
    def init(self):
        super().__init__() 
        self.title("HeadHunder client")
        self.geometry("1280x720")

        self.makeUI()

    def makeUI(self):
        self.notebook = ttk.Notebook()
        self.notebook.pack(expand=True, fill=BOTH)
        self.settingFrame = ttk.Frame(self.notebook)
        self.vacancy_name_frame = SearchForm(self.notebook, search)
        self.add_new_form = ttk.Frame(self.notebook)

        self.settingFrame.pack(expand=True, fill=BOTH)
        self.vacancy_name_frame.pack(expand=True, fill=BOTH)
        self.add_new_form.pack(expand=True, fill=BOTH)
        self.notebook.add(self.settingFrame, text="Действия")
        self.notebook.add(self.vacancy_name_frame, text="Новая вкладка")
        self.notebook.add(self.add_new_form, text="+")

    def __init__(self):
        pass

class SearchForm(Frame, Singleton):
    def __init__(self, master, on_search):
        super().__init__(master=master)
        self.on_search = on_search
        self.exp_meta = {
            "Не имеет значения" : "",
            "От 1 года до 3 лет" : "between1And3",
            "Нет опыта" : "noExperience",
            "От 3 до 6 лет" : "between3And6",
            "Более 6 лет" : "moreThan6"
        }
        self.selected_exp = StringVar(value=self.exp_meta["Не имеет значения"])

        self.makeUI()

    def makeUI(self):
        self.result_labels = list()

        Label(self, text="Введите название вакансии:").pack(pady=10)
        self.entry_vacancy_name = Entry(self)
        self.entry_vacancy_name.pack(pady=10)

        Label(self, text="Введите название региона:").pack(pady=10)
        self.entry_area = Entry(self)
        self.entry_area.pack(pady=10)
        
        Label(self, text="Опыт работы").pack(pady=10)
        for value in self.exp_meta:
            radiobutton_exp = ttk.Radiobutton(self, text=value, value=self.exp_meta[value], variable=self.selected_exp)
            radiobutton_exp.pack(padx=5, pady=5)

        Button(self, text="Поиск", command=self._on_search_clicked).pack(pady=10)

    def _update_result_labels(self, result):
        if self.result_labels != []:
            for i in self.result_labels:
                i["text"] = ''
                i.destroy()
            self.result_labels = []
        items = result.split(",")
        for item in items:
            self.result_labels.append(Label(self, text=item))
            self.result_labels[-1].pack()


    def _on_search_clicked(self):
        vacancy_name = self.entry_vacancy_name.get()
        area = self.entry_area.get()
        exp = self.selected_exp.get()
        self._update_result_labels(self.on_search(vacancy_name, area, exp))


def search(vacancy_name, area, exp):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    request_builder = Requst_Builder("get")
    try:
        sock.connect((config.host_ip, config.port))

        request_builder.add_item((vacancy_name, area, exp))
        request = request_builder.build()
        sock.send(request.encode(config.encoding))

        data = sock.recv(2048)
        if data:
            return f"Your request: {data.decode(config.encoding)}"
        sock.close()
    except:
        print("На сервере ведутся технические работы приносим свои извинение за предоставленные неудобства."
            "\nПопробуйте повторить попытку через пару минут")
        sock.close()