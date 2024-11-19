

from model.src import API_Grabber
from model.src.Orms import SalaryOrm, VacancyOrm
from model.src.database_handler import Database_handler
from model.src.utils import get_salary


class RequestHandler:
    def __init__(self):
        self.db_handler = Database_handler()

    def proccess(self):
        raise NotImplementedError("This method should be implemented in a subclass")
    

class VacancyRequestHandler(RequestHandler):
    def __init__(self):
        self.api_grabber = API_Grabber()

    def proccess(self, decoded_data):
        result = self.db_handler.select(decoded_data, VacancyOrm)
        
        ids = [item.id for item in result]
        skills_data = self.api_grabber.get_skills_data(ids)
        skills = {vacancy_id : {"key_skills" : [skill["name"] for skill in skills_data[vacancy_id]]} for vacancy_id in ids}

        salary = []
        for item in result:
            salary.extend(self.db_handler.select(item, SalaryOrm))
        result_salary = get_salary(salary)

        answer = {}
        for item_vac, item_sal, item_skill in zip(result, result_salary, skills):
            object = {**(item_vac.__dict__), **item_sal, **skills[item_skill]}
            object.pop('_sa_instance_state', None)
            answer[f"{object['id']}"] = object.copy()
            answer[f"{object['id']}"].pop("id", None)

        return self.answer
    