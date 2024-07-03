from collections import Counter
from tkinter import *
from tkinter import ttk
from tkinter.ttk import Treeview
from structural.src.request_builder import *
from structural.src.graphs import *
from structural.src.request_context import *
from creational.singleton import Singleton
from structural.config import secret_key
from tkinter import messagebox
from scipy import stats
import jwt
import uuid

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
        Label(self.control_frame, text="Панель управления", bg='lightgray').pack(pady=10)
        self.user_button = Button(self.control_frame, text="Пользовательская панель", state="disabled", command=self.show_initial_content)
        self.user_button.pack(pady=5, fill="x")
        self.change_password_button = Button(self.control_frame, text="Сменить пароль", command=self.change_password)
        
        # Добавление кнопки панели администратора
        if self.user_info.get('role') == 2:
            self.admin_button = Button(self.control_frame, text="Панель администратора", command=self.show_administator_content)
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
        self.admin_button.config(state=NORMAL)
        self.user_frame.update()

    def show_administator_content(self):
        self.clear_display_frame()
        self.user_button.config(state=NORMAL)
        self.admin_button.config(state=DISABLED)
        self.admin_frame.update()

class ChangePasswordFrame(Frame):
    def __init__(self, master, search, token):
        super().__init__(master=master)
        self.token = token
        self.params = jwt.decode(token, secret_key, algorithms=["HS256"])
        self.search = search

    def makeUI(self):
        Label(self.master, text="Смена пароля").pack(side=TOP)
        Label(self.master, text="Введите новый пароль").pack(anchor=NW)
        self.entry_password1 = ttk.Entry(self.master, width=40, show="*")
        self.entry_password1.pack(padx=5, pady=5)
        Label(self.master, text="Подтвердите пароль").pack(anchor=NW)
        self.entry_password2 = ttk.Entry(self.master, width=40, show="*")
        self.entry_password2.pack(padx=5, pady=5)

        self.change_password_button = Button(self.master, text="Сменить пароль", command=self.change_password)
        self.change_password_button.pack()

    def change_password(self):
        password = self.entry_password1.get()
        password2 = self.entry_password2.get()

        if password != password2:
            messagebox.showerror("Ошибка", "Пароли не совпадают")
            return 
        
        data = self.search(self.token, "update", username=self.params["login"], new_password=password)
        messagebox.showinfo("Успех", data.data)

    def update(self):
        self.makeUI()

class UserFrame(Frame):
    def __init__(self, master, search, token):
        super().__init__(master=master)
        self.token = token
        self.params = jwt.decode(token, secret_key, algorithms=["HS256"])
        self.search = search

    def makeUI(self, data):
        Label(self.master, text="Пользовательская панель", bg='white').pack()
        login = self.params["login"]
        Label(self.master, text=login, bg="white").pack(anchor=W)

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

        # Размещение виджета Treeview в окне приложения
        tree.pack(side="left", expand=True, fill="both")

    def update(self):
        data = self.search(self.token, journal=self.params["login"])
        self.makeUI(data.data)

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

class SubForms(Frame):
    def __init__(self, master, data, callback):
        super().__init__(master=master)
        self.canvas = Canvas(self, borderwidth=0, background='white')
        self.scrollbar = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = Frame(self.canvas,background='white')

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.scrollable_frame_id = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        def onFrameConfigure(canvas):
            canvas.configure(scrollregion=canvas.bbox("all"))
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.bind("<Configure>", self.on_resize)
        self.scrollable_frame.bind("<Configure>", lambda event, canvas=self.canvas: onFrameConfigure(canvas))

        self.count_vacancy = Label(self.scrollable_frame, text='')
        self.close_button = ttk.Button(self.scrollable_frame, text='Закрыть', command=lambda: self.close_tab(self, callback))
        self.download_raw_data_button = ttk.Button(self.scrollable_frame, text="Выгрузить данные", command= lambda : self.download_raw_data(data))
        self.close_button.pack(anchor=NE)
        self.download_raw_data_button.pack(anchor=NE)
    
        self.show_stat(data)

    def on_resize(self, event):
        self.canvas.itemconfig(self.scrollable_frame_id, width=self.canvas.winfo_width())

    def download_raw_data(self, data: RequestContext):
        filename = f"{uuid.uuid4()}.json"

        with open(filename, "w", encoding='utf-8') as json_file:
            json.dump(data.data, json_file, ensure_ascii=False, indent=4)

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
        uniq_exp = data.getUniqExp()
        unic_emp = data.getUniqEmployer()
        tree = Treeview(self.scrollable_frame, columns=("Опыт работы", "Среднее зарплат", "Медиана Зарплат", "Мода зарплат", "Количество вакансий"), show="headings")

        # Установка заголовков столбцов
        tree.heading("Опыт работы", text="Опыт работы")
        tree.heading("Среднее зарплат", text="Среднее зарплат")
        tree.heading("Медиана Зарплат", text="Медиана Зарплат")
        tree.heading("Мода зарплат", text="Мода зарплат")
        tree.heading("Количество вакансий", text="Количество вакансий")

        # Установка ширины столбцов
        tree.column("Опыт работы", width=60)
        tree.column("Среднее зарплат", width=100)
        tree.column("Медиана Зарплат", width=100)
        tree.column("Мода зарплат", width=100)
        tree.column("Количество вакансий", width=100)

        # Добавление данных в таблицу
        for i in uniq_exp:
            filtered_by_exp_dataframe = data.filterDataByExp(i)
            salaries = [int(j) for j in filtered_by_exp_dataframe["salary"] if pd.notnull(j)]

            if not salaries:
                continue
            q1 = np.quantile(salaries, 0.25)  # 25% квантиль
            q3 = np.quantile(salaries, 0.75)  # 75% квантиль

            iqr = q3 - q1  # Межквартильный размах

            # Определение границ для отсечения выбросов
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr

            # Фильтрация выбросов
            filtered_salaries = [x for x in salaries if lower_bound <= x <= upper_bound]
            mean_salary = np.mean(filtered_salaries)
            median_salary = np.median(filtered_salaries)
            mode = stats.mode(filtered_salaries)

            tree_data = [i, mean_salary, median_salary, mode.mode, len(filtered_salaries)]
            tree.insert("", "end", values=tree_data)
        tree.pack(expand=True, fill="both")
        key_skills_frame = Frame(self.scrollable_frame)
        key_skills_frame.pack()
        texts = data.get_dataframe()["key_skills"].dropna().tolist()
        temp = [i for item in texts for i in item]
        key_skills_tree = Treeview(key_skills_frame, columns=("Ключевой навык", "Кол-во"), show="headings")
        key_skills_tree.heading("Ключевой навык", text="Ключевой навык")
        key_skills_tree.heading("Кол-во", text="Кол-во")

        # Установка ширины столбцов
        key_skills_tree.column("Ключевой навык", width=100)
        key_skills_tree.column("Кол-во", width=100)
        key_skill_data = Counter(temp).most_common(100)

        for i in key_skill_data:
            key_skills_tree.insert("", "end", values=i)
        key_skills_tree.pack(expand=True, fill="both", side=LEFT)
        pie_gramm = pieGramm(request)
        pie_gramm.draw(key_skills_frame, key_skill_data)

        emp_tree = Treeview(self.scrollable_frame, columns=("Компания", "Среднее зарплат", "Медиана Зарплат", "Мода зарплат", "Количество вакансий"), show="headings")

        # Установка заголовков столбцов
        emp_tree.heading("Компания", text="Компания")
        emp_tree.heading("Среднее зарплат", text="Среднее зарплат")
        emp_tree.heading("Медиана Зарплат", text="Медиана Зарплат")
        emp_tree.heading("Мода зарплат", text="Мода зарплат")
        emp_tree.heading("Количество вакансий", text="Количество вакансий")

        # Установка ширины столбцов
        emp_tree.column("Компания", width=60)
        emp_tree.column("Среднее зарплат", width=100)
        emp_tree.column("Медиана Зарплат", width=100)
        emp_tree.column("Мода зарплат", width=100)
        emp_tree.column("Количество вакансий", width=100)

        # Добавление данных в таблицу
        for i in unic_emp:
            filtered_by_emp_dataframe = data.filterDataByEmp(i)
            salaries = [int(j) for j in filtered_by_emp_dataframe["salary"] if pd.notnull(j)]

            if not salaries:
                continue
            q1 = np.quantile(salaries, 0.25)  # 25% квантиль
            q3 = np.quantile(salaries, 0.75)  # 75% квантиль

            iqr = q3 - q1  # Межквартильный размах

            # Определение границ для отсечения выбросов
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr

            # Фильтрация выбросов
            filtered_salaries = [x for x in salaries if lower_bound <= x <= upper_bound]
            mean_salary = np.mean(filtered_salaries)
            median_salary = np.median(filtered_salaries)
            mode = stats.mode(filtered_salaries)

            tree_data = [i, mean_salary, median_salary, mode.mode, len(filtered_salaries)]
            emp_tree.insert("", "end", values=tree_data)
        emp_tree.pack(anchor=W,expand=True, fill="both")

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
        answer = self.on_search(token=self.token, vacancy_name=vacancy_name, area=area, exp=exp)
        if answer.data:
            self.create_new_form(answer, vacancy_name)
        else:
            exp_key = get_key_exp(self.exp_meta, answer.context["exp"])
            messagebox.showerror("Результатов не найдено", f"По вашему запросу \n{answer.context['vacancy_name']}\n{answer.context['area']}\n{exp_key}\n не было найдено.\nПопробуйте другой запрос.")

def get_key_exp(exp_meta, exp):
    values = list(exp_meta.values())
    index = values.index(exp)

    key = list(exp_meta.keys())[index]

    return key