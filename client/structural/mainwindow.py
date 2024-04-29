import socket
from tkinter import *
from tkinter import ttk
from structural import config
from creational.singleton import Singleton
from structural.src.request_builder import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import pandas as pd

class MainWindow(Tk, Singleton):
    def init(self):
        super().__init__() 
        self.title("HeadHunder client")
        self.geometry("1280x720")
        self.sub_forms = []

        self.makeUI()

    def makeUI(self):
        self.notebook = ttk.Notebook()
        self.notebook.pack(expand=True, fill=BOTH)
        self.settingFrame = ttk.Frame(self.notebook)
        self.main_frame = SearchForm(self.notebook, search, self.create_new_form)

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

    def __init__(self):
        pass

class SubForms(Frame):
    def __init__(self, master, data, callback):
        super().__init__(master=master)
        self.count_vacancy = Label(self, text='')
        self.result_labels = list()
        self.close_button = ttk.Button(self, text='Закрыть', command=lambda: self.close_tab(self, callback))
        self.close_button.pack(anchor=NE, padx=10, pady=10)
        self.show_stat(data)
        #self._update_result_labels(data)

    def close_tab(self, tab, callback):
        # Закрытие указанной вкладки
        index = self.master.index(tab)
        self.master.forget(index)
        callback(index)

    def show_stat(self, data:dict):
        df = pd.DataFrame(data.values(), index=data.keys())
        fig, ax = plt.subplots()
        ax.hist(df["salary"], bins=10, color="skyblue", edgecolor='black')
        ax.set_xlabel("Salary")
        ax.set_ylabel("Frequency")
        ax.set_title("Salary Distribution")

        sample_size = len(df["salary"])
        plt.text(0.5, 45, f'Sample Size: {sample_size}', fontsize=12, color='black')


        self.canvas = FigureCanvasTkAgg(fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()

    def _update_result_labels(self, result:dict):
        if self.result_labels != []:
            for i in self.result_labels:
                i["text"] = ''
                i.destroy()
            self.result_labels = []
        self.count_vacancy["text"] = f"Количество вакансий: {len(result)}"
        self.count_vacancy.pack(anchor=NW)
        self.result_labels.extend(list(map(lambda x: Label(self, text=x).pack(), result.values())))

class SearchForm(Frame, Singleton):
    def __init__(self, master, on_search, extension):
        super().__init__(master=master)
        self.on_search = on_search
        self.create_new_form = extension
        self.exp_meta = {
            "Не имеет значения" : "%",
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
        #items = result.split(",")
        for item in result:
            self.result_labels.append(Label(self, text=item))
            self.result_labels[-1].pack()


    def _on_search_clicked(self):
        vacancy_name = self.entry_vacancy_name.get()
        area = self.entry_area.get()
        exp = self.selected_exp.get()
        self.create_new_form(self.on_search(vacancy_name, area, exp), vacancy_name)
        #self._update_result_labels(self.on_search(vacancy_name, area, exp))

def search(vacancy_name, area, exp):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        sock.connect((config.host_ip, config.port))
        request_builder = JSONRequestBuilder(GetRequestTemplate(vacancy_name, area, exp))
       
        message = request_builder.build()
        sock.send(message.encode(config.encoding))
        answer = b""
        end_signal = b"<END>"
        while True:
            data = sock.recv(1024)
            answer += data
            if end_signal in data:
                break
        answer = answer.decode(config.encoding)
        answer = json.loads(answer[:-5])
        
        sock.close()
        return answer
    except Exception as error:
        print("Произошла ошибка:", error)
    except:
        print("На сервере ведутся технические работы приносим свои извинение за предоставленные неудобства."
            "\nПопробуйте повторить попытку через пару минут")
        sock.close()