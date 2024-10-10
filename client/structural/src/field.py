from tkinter import Entry, Label, StringVar, ttk


class Field:
    def __init__(self, master) -> None:
        self.root = master
    def draw(self) -> None:
        pass

class VacancyNameField(Field):
    def draw(self) -> None:
        Label(self.root, text="Введите название вакансии:").pack(pady=10)
        self.entry_vacancy_name = Entry(self.root)
        self.entry_vacancy_name.pack(pady=10)
 
class RegionField(Field):
    def draw(self) -> None:
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
        
    def draw(self) -> None:
        Label(self.root, text="Опыт работы").pack(pady=10)
        for value in self.exp_meta:
            radiobutton_exp = ttk.Radiobutton(self.root, text=value, value=self.exp_meta[value], variable=self.selected_exp)
            radiobutton_exp.pack(padx=5, pady=5)