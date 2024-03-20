from model.src.Orms import EmployerOrm, SalaryOrm, VacancyOrm

class Data_Formatter:
    def __init__(self, raw_data):
        self.format_factory = Formatter_Factory()
        self.raw_data = raw_data

    def format(self):
        models = {
            "salaryModel" : self.format_factory.format_salary,
            "vacancyModel" : self.format_factory.format_vacancy,
            "employerModel" : self.format_factory.format_employer
        }
        formatted_data = {key: [] for key in models.keys()}
        for i in self.raw_data:
            self.format_factory.set_raw_data(i["items"])
            for model_name, formatter_func in models.items():
                formatted_data[model_name].append(formatter_func())

        return formatted_data

    
    
class Formatter_Factory:
    def __init__(self):
        self.salary_foramtter = Salary_Formatter()
        self.employer_formatter = Employer_Formatter()
        self.vacancy_formatter = Vacansy_Formatter()

    def set_raw_data(self, raw_data):
        self.salary_foramtter.load_raw_data(raw_data)
        self.employer_formatter.load_raw_data(raw_data)
        self.vacancy_formatter .load_raw_data(raw_data)

    def format_salary(self):
        salary = self.salary_foramtter.format()
        return salary
    
    def format_employer(self):
        employer = self.employer_formatter.format()
        return employer
    
    def format_vacancy(self):
        vacancy = self.vacancy_formatter.format()
        return vacancy
    
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
        for i in self.raw_data:
            if i["salary"] == None:
                self.data.append(None)
                continue
            _id = i["id"]
            _from = i["salary"]["from"]
            _to = i["salary"]["to"] if i["salary"]["to"] else None
            _currency= i["salary"]["currency"]
            _gross = i["salary"]["gross"]
            self.data.append([_id, _from, _to, _currency, _gross])
        return self.data
    
class Employer_Formatter(Formatter):
    def __init__(self):
        super().__init__("Employer Formatter")

    def format(self):
        for i in self.raw_data:
            _id = i["employer"]["id"]
            _name = i["employer"]["name"]
            _accredited_it_employer = i["employer"]["accredited_it_employer"]
            _trusted = i["employer"]["trusted"]
            self.data.append([_id, _name, _accredited_it_employer, _trusted])
        return self.data

class Vacansy_Formatter(Formatter):
    def __init__(self):
        super().__init__("Vacancy Formatter")

    def format(self):
        for i in self.raw_data:
            _id = i["id"]
            _name = i["name"]
            _area = i["area"]["id"]
            _published_at = i["published_at"]
            _requirement = i["snippet"]["requirement"]
            _responsobility = i["snippet"]["responsibility"]
            _schedule = i["schedule"]["id"]
            _prof_roles = i["professional_roles"]["name"]
            _exp = i["experience"]["id"]
            _employment = i["id"]
            _employer_id = i["employer"]["id"]
            self.data.append([
                _id, 
                _name, 
                _area, 
                _published_at, 
                _requirement, 
                _responsobility, 
                _schedule, 
                _prof_roles, 
                _exp, 
                _employment, 
                _employer_id
            ])
        return self.data