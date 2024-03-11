from model.src.Area import Area
from model.src.Employer import Employer
from model.src.Salary import Salary
from model.src.Vacancy import Vacancy
import json
import requests

class API_Grabber():
    def __init__(self, per_page = 100) -> None:
        self.url = f"https://api.hh.ru/vacancies?per_page={per_page}"
        self.per_page = per_page

    def set_quantity_pagination(self):
        response = requests.get(self.url).json()
        self.quantity_pagination = round(response['found'] / self.per_page, 0) + 1

    def get_data(self):
        data = list()
        page = 0
        while page <= self.quantity_pagination:
            response = requests.get(self.url, timeout=5).json()
            data.append(response)
            page += 1

        return data
    