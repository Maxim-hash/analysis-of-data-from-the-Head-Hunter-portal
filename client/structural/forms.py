from tkinter import *
from tkinter import ttk
from tkinter.ttk import Treeview
from structural.src.request_builder import *
from structural.src.graphs import *
from structural.src.request_context import *
from creational.singleton import Singleton
from structural.config import secret_key
import jwt

class MainForm(Frame):
    def __init__(self, master, token, search_func):
        super().__init__(master=master)
        self.search_func = search_func
        self.token = token
        self.user_info = self.decode_token(token)
        #self.admin_panel = None  # Инициализируем панель как None, пока она не открыта
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
        # Пример добавления элементов управления
        Label(self.control_frame, text="Панель управления", bg='lightgray').pack(pady=10)
        self.user_button = Button(self.control_frame, text="Пользовательская панель", state="disabled", command=self.show_initial_content)
        self.user_button.pack(pady=5, fill="x")

        # Добавление кнопки панели администратора
        if self.user_info.get('role') == 2:
            self.admin_button = Button(self.control_frame, text="Панель администратора", command=self.show_administator_content)
            self.admin_button.pack(pady=10, fill="x")
        Label(self.display_frame, text="Пользовательская панель", bg='white').pack(side=TOP)

    def clear_display_frame(self):
        for widget in self.display_frame.winfo_children():
            widget.destroy()

    def show_initial_content(self):
        self.clear_display_frame()
        Label(self.display_frame, text="Пользовательская панель", bg='white').pack(side=TOP)
        self.user_button.config(state=DISABLED)
        self.admin_button.config(state=NORMAL)

    def show_administator_content(self):
        self.clear_display_frame()
        self.admin_frame.update()
        self.user_button.config(state=NORMAL)
        self.admin_button.config(state=DISABLED)

class AdminFrame(Frame):
    def __init__(self, master, search, token):
        super().__init__(master=master)
        self.token = token
        self.search = search

    def makeUI(self, data):
        Label(self.master, text="Панель Администратора", bg='white').pack()
        container = Frame(self.master)
        container.pack(expand=False, fill="both")
        #  Создание виджета Treeview
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
            tree_data = [i]
            tree_data.extend(list(data[i].values()))
            tree_data[1], tree_data[3] = tree_data[3], tree_data[1]
            tree_data[2], tree_data[4] = tree_data[4], tree_data[2]

            tree.insert("", "end", values=tree_data)
       
        # Создание вертикальной прокрутки
        scrollbar_vertical = Scrollbar(container, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar_vertical.set)
        scrollbar_vertical.pack(side="right", fill="y")

        # Создание горизонтальной прокрутки
        scrollbar_horizontal = Scrollbar(container, orient="horizontal", command=tree.xview)
        tree.configure(xscrollcommand=scrollbar_horizontal.set)
        scrollbar_horizontal.pack(side="bottom", fill="x")

        # Размещение виджета Treeview в окне приложения
        tree.pack(side="left", expand=True, fill="both")

    def update(self):
        data = self.search(self.token, journal="")
        self.makeUI(data.data)

class SubForms(Frame):
    def __init__(self, master, data, callback):
        super().__init__(master=master)
        self.canvas = Canvas(self)
        self.scrollbar = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = Frame(self.canvas)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        def onFrameConfigure(canvas):
            canvas.configure(scrollregion=canvas.bbox("all"))
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        self.scrollable_frame.bind("<Configure>", lambda event, canvas=self.canvas: onFrameConfigure(canvas))

        self.count_vacancy = Label(self.scrollable_frame, text='')
        self.close_button = ttk.Button(self.scrollable_frame, text='Закрыть', command=lambda: self.close_tab(self, callback))
        self.close_button.pack(anchor=NE)
    
        self.show_stat(data)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def close_tab(self, tab, callback):
        # Закрытие указанной вкладки
        index = self.master.index(tab)
        self.master.forget(index)
        callback(index)

    def show_stat(self, request:RequestContext):
        data = DataTransmitter(request.data)
        base_histogram1 = BaseHistogram(request)
        base_histogram1.draw(self.scrollable_frame)
        uniq_exp = data.getUniqMeta()
        exp_histograms = []
        for i in uniq_exp:
            exp_histograms.append(BaseHistogram(request))
            exp_histograms[-1].set_data_frame(data.filterDataByExp(i))
            exp_histograms[-1].draw(self.scrollable_frame)        
        #base_histogram2 = BaseHistogram(request)
        #base_histogram2.draw(self.scrollable_frame)

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
    def __init__(self, master, on_search, extension, token):
        super().__init__(master=master)
        self.token = token
        self.on_search = on_search
        self.create_new_form = extension
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

        for item in result:
            self.result_labels.append(Label(self, text=item))
            self.result_labels[-1].pack()

    def _on_search_clicked(self):
        vacancy_name = self.entry_vacancy_name.get()
        area = self.entry_area.get()
        exp = self.selected_exp.get()
        self.create_new_form(self.on_search(token=self.token, vacancy_name=vacancy_name, area=area, exp=exp), vacancy_name)
