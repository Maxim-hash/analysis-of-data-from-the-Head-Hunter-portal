from tkinter import Entry, Label, StringVar, font, ttk


class Field:
    def __init__(self, master) -> None:
        self.root = master
        self.style = ttk.Style()
        self.style.map('design.Toolbutton', foreground=[('selected', 'blue'), ('active','lightyellow'), ('!disabled','black')], font=[('!disabled','arial 16 bold')])
        self.font = font.Font(family= "helvetica", size=14, weight="normal")
    def draw(self) -> None:
        pass

class VacancyNameField(Field):
    def __init__(self, master):
        super().__init__(master)
        self.current_entry = StringVar()

    def draw(self) -> None:
        ttk.Label(self.root, text="Введите название вакансии:").pack(pady=10)
        self.entry_vacancy_name = ttk.Combobox(self.root, textvariable=self.current_entry, width= 30, font=self.font, height=100, values=["Honda", "Hyundai", "Wolkswagon", "Tata", "Renault", "Ford", "Chrevolet", "Suzuki","BMW", "Mercedes"])
        self.entry_vacancy_name.pack(pady=10)
 
class RegionField(Field):
    def __init__(self, master):
        super().__init__(master)
        self.current_entry = StringVar()

    def draw(self) -> None:
        ttk.Label(self.root, text="Введите название региона:").pack(pady=10)
        
        self.entry_area = ttk.Combobox(self.root, textvariable=self.current_entry, width= 30, font=self.font, height=100)
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
        ttk.Label(self.root, text="Опыт работы").pack(pady=10)
        for value in self.exp_meta:
            radiobutton_exp = ttk.Radiobutton(self.root, text=value, value=self.exp_meta[value], variable=self.selected_exp, style='design.Toolbutton')
            radiobutton_exp.pack(padx=5, pady=5)