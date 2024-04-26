import datetime
from model.src.Orms import EmployerOrm, SalaryOrm, VacancyOrm, AreaOrm

class Data_Formatter:
    modes = {
        "vacancy" : 0,
        "area" : 1 
    }
    
    def __init__(self, raw_data):
        self.format_factory = Formatter_Factory()
        self.raw_data = raw_data
        self.models = [
            {
            "employerModel" : self.format_factory.format_employer,
            "vacancyModel" : self.format_factory.format_vacancy,
            "salaryModel" : self.format_factory.format_salary
            },
            {
            "areaModel" : self.format_factory.format_area
            }
        ]

    def load_raw_data(self, raw_data):
        self.raw_data = raw_data

    def format(self, mode):
        if mode in self.modes:
            model = self.models[self.modes[mode]]
        else:
            raise ValueError("Unsupported mode type")

        formatted_data = {key: [] for key in model.keys()}
        for package in self.raw_data:
                self.format_factory.set_raw_data(package)
                for model_name, formatter_func in model.items():
                    items = formatter_func()
                    formatted_data[model_name].extend(set(items))
        return formatted_data

class Formatter_Factory:
    def __init__(self):
        self.salary_foramtter = Salary_Formatter()
        self.employer_formatter = Employer_Formatter()
        self.vacancy_formatter = Vacansy_Formatter()
        self.area_formatter = Area_Formattter()

    def set_raw_data(self, raw_data):
        self.salary_foramtter.load_raw_data(raw_data)
        self.employer_formatter.load_raw_data(raw_data)
        self.vacancy_formatter.load_raw_data(raw_data)
        self.area_formatter.load_raw_data(raw_data)

    def format_salary(self):
        salary = self.salary_foramtter.format()
        return salary
    
    def format_employer(self):
        employer = self.employer_formatter.format()
        return employer
    
    def format_vacancy(self):
        vacancy = self.vacancy_formatter.format()
        return vacancy
    
    def format_area(self):
        area = self.area_formatter.format()
        return area
    
class Formatter:
    def __init__(self, name):
        self.name = name
        self.data = []
    
    def get_name(self):
        return self.name
    
    def load_raw_data(self, raw_data):
        self.raw_data = raw_data

    def get_data(self):
        return self.data

class Salary_Formatter(Formatter):
    def __init__(self):
        super().__init__("Salary Formatter")

    def format(self):
        self.data = []
        for i in self.raw_data:
            _id = int(i["id"])
            if i["salary"] == None:
                self.data.append(SalaryOrm(id = _id, s_from =None, s_to = None, currency = None, gross = None))
                continue
            _from = int(i["salary"]["from"]) if i["salary"]["from"] else None
            _to = int(i["salary"]["to"]) if i["salary"]["to"] else None
            _currency= i["salary"]["currency"]
            _gross = i["salary"]["gross"]
            self.data.append(SalaryOrm(id=_id, s_from =_from, s_to = _to, currency = _currency, gross = _gross))
        return self.data
    
class Employer_Formatter(Formatter):
    def __init__(self):
        super().__init__("Employer Formatter")

    def format(self):
        self.data = []
        for i in self.raw_data:
            _name = i["employer"]["name"]
            if "accredited_it_employer" in i["employer"].keys() :
                _accredited_it_employer = i["employer"]["accredited_it_employer"]
            else:
                _accredited_it_employer = False
            _trusted = i["employer"]["trusted"]
            self.data.append(EmployerOrm(name = _name, accredited_it_employer = _accredited_it_employer, trusted = _trusted))
        return self.data
    
class Area_Formattter(Formatter):
    def __init__(self):
        super().__init__("Area Formatter")

    def format(self):
        self.data = []
        for i in self.raw_data:
            _id = int(i["id"])
            _parent_id = int(i["parent_id"]) if i["parent_id"] is not None else None
            _name = i["name"]
            parent = [AreaOrm(id = _id, parent_id = _parent_id, name = _name)]
            child = [j for j in self.dop_format(i["areas"])]
            parent.extend(child)
            self.data.extend(parent)

        return self.data

    def dop_format(self, b):
        if b == []:
            return  
        buffer = []
        for i in b:
            _id = int(i["id"])
            _parent_id = int(i["parent_id"]) if i["parent_id"] is not None else None
            _name = i["name"]
            temp = AreaOrm(id = _id, parent_id = _parent_id, name = _name)
            buffer.append(temp)
            if i["areas"] == []:
                continue
            buffer.extend(self.dop_format(i["areas"]))
        return buffer

class Vacansy_Formatter(Formatter):
    def __init__(self):
        super().__init__("Vacancy Formatter")

    def format(self):
        self.data = []
        for i in self.raw_data:
            _id = int(i["id"])
            _name = i["name"]
            _area = int(i["area"]["id"])
            _published_at = i["published_at"]
            _requirement = i["snippet"]["requirement"]
            _responsobility = i["snippet"]["responsibility"]
            _schedule = i["schedule"]["id"]
            _prof_roles = i["professional_roles"][0]["name"]
            _exp = i["experience"]["id"]
            _employment = i["id"]
            _employer_name = i["employer"]["name"]
            self.data.append(VacancyOrm(
                id = _id, 
                name = _name, 
                area_id = _area, 
                publishied_at = _published_at, 
                requirement = _requirement, 
                responsobility = _responsobility, 
                schedule = _schedule, 
                prof_roles = _prof_roles, 
                exp = _exp, 
                empoyment = _employment, 
                employers_name = _employer_name
            ))
        return self.data