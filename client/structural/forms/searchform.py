from tkinter import BOTH, Entry, StringVar, messagebox
from tkinter import ttk
from tkinter import Button, Frame, Label

from structural.src.field import VacancyNameField, ExperienceField, RegionField 
from structural.src.request_context import RequestContext
from creational.singleton import Singleton
from structural.src.utils import get_key_exp
from structural.src.search import search

class SearchFormController:
    def __init__(self, create_new_form_func) -> None:
        self.create_new_form = create_new_form_func

    def get_results(self, **kwargs) -> RequestContext:
        response = search(**kwargs)
        return response
    
    def create_new_form(self, response, name) -> None:
        self.create_new_form(response, name)
    
class SearchFormUI:
    data = {"None" : None}

    def __init__(self, master, token) -> None:
        self.token = token
        self.root = ttk.Frame(master=master)
        self.vacancy_name_field = VacancyNameField(self.root)
        self.region_field = RegionField(self.root)
        self.experience_field = ExperienceField(self.root)

    def add_controller(self, controller) -> None:
        self.controller = controller
        
    def showUI(self) -> None:
        self.vacancy_name_field.draw()
        self.region_field.draw()
        self.experience_field.draw()

        ttk.Button(self.root, text="Поиск", command=self.on_button_clicked).pack(pady=10)

    def on_button_clicked(self) -> None:
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

    def pack(self) -> None:
        self.root.pack(expand=True, fill=BOTH)

class SearchForm(Singleton):
    def __init__(self, master, extension, token) -> None:
        super().__init__()
        self.token = token

        self.ui = SearchFormUI(master, token)
        self.controller = SearchFormController(extension)

        self.ui.add_controller(self.controller)

        self.ui.showUI()
        
    def pack(self) -> None:
        self.ui.pack()