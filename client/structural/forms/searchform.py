from tkinter import BOTH, Entry, StringVar, messagebox
from tkinter import ttk
from tkinter import Button, Frame, Label

from creational.singleton import Singleton
from structural.src.utils import get_key_exp
from structural.src.search import search

class SearchFormController:
    def __init__(self, create_new_form_func) -> None:
        self.create_new_form = create_new_form_func

    def get_results(self, **kwargs):
        response = search(**kwargs)
        return response
    
    def create_new_form(self, response, name):
        self.create_new_form(response, name)
    
class SearchFormUI:
    data = {"None" : None}

    def __init__(self, master, token) -> None:
        self.token = token
        self.root = Frame(master=master)
        self.vacancy_name_field = VacancyNameField(self.root)
        self.region_field = RegionField(self.root)
        self.experience_field = ExperienceField(self.root)

    def add_controller(self, controller) -> None:
        self.controller = controller
        
    def showUI(self) -> None:
        self.vacancy_name_field.draw()
        self.region_field.draw()
        self.experience_field.draw()

        Button(self.root, text="Поиск", command=self.on_button_clicked).pack(pady=10)

    def on_button_clicked(self):
        self.data = {
            "token" : self.token,
            "vacancy_name" : self.vacancy_name_field.entry_vacancy_name.get(),
            "area" : self.region_field.entry_area.get(),
            "exp" : self.experience_field.selected_exp.get()
        }

        response = self.controller.get_results(**self.data)

        if response.data:
            self.controller.create_new_form(response, self.data["vacancy_name"])
        else:
            exp_key = get_key_exp(self.experience_field.exp_meta, response.context["exp"])
            messagebox.showerror("Результатов не найдено", f"По вашему запросу \n{response.context['vacancy_name']}\n{response.context['area']}\n{exp_key}\n не было найдено.\nПопробуйте другой запрос.")

    def pack(self):
        self.root.pack(expand=True, fill=BOTH)

class Field:
    def __init__(self, master) -> None:
        self.root = master
    def draw(self):
        pass

class VacancyNameField(Field):
    def draw(self):
        Label(self.root, text="Введите название вакансии:").pack(pady=10)
        self.entry_vacancy_name = Entry(self.root)
        self.entry_vacancy_name.pack(pady=10)
 
class RegionField(Field):
    def draw(self):
        Label(self.root, text="Введите название региона:").pack(pady=10)
        self.entry_area = Entry(self.root)
        self.entry_area.pack(pady=10)

class ExperienceField(Field):
    def __init__(self, master) -> None:
        super().__init__(master)
        self.exp_meta = {
            "Не имеет значения" : "",
            "От 1 года до 3 лет" : "between1And3",
            "Нет опыта" : "noExperience",
            "От 3 до 6 лет" : "between3And6",
            "Более 6 лет" : "moreThan6"
        }
        self.selected_exp = StringVar(value=self.exp_meta["Не имеет значения"])
        
    def draw(self):
        Label(self.root, text="Опыт работы").pack(pady=10)
        for value in self.exp_meta:
            radiobutton_exp = ttk.Radiobutton(self.root, text=value, value=self.exp_meta[value], variable=self.selected_exp)
            radiobutton_exp.pack(padx=5, pady=5)

class SearchForm(Singleton):
    def __init__(self, master, extension, token):
        super().__init__()
        self.token = token

        self.ui = SearchFormUI(master, token)
        self.controller = SearchFormController(extension)

        self.ui.add_controller(self.controller)

        self.ui.showUI()
        
    def pack(self):
        self.ui.pack()